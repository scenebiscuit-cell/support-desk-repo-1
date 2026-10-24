"""Ticket triage: classify, prioritize, tag, pick a macro, and draft a reply.

Two engines share one output shape:
  rules_triage  keyword rules + macro fill-in (no AI)
  llm_triage    an LLM grounded in help-center excerpts and macros, with the
                rules result as a safety net if the model returns bad output
"""
from __future__ import annotations

import json

from . import taxonomy as tx
from .kb import KnowledgeBase, tokenize
from .llm import extract_json
from .macros import by_id, choose_macro, fill

SLUG_TO_CATEGORY = {
    "billing-and-refunds": "billing", "plans-and-pricing": "presales", "change-or-cancel-plan": "cancellation",
    "booking-page": "booking_setup", "getting-started": "booking_setup", "calendar-sync": "calendar_sync",
    "reminders": "reminders", "deposits-and-payments": "payments", "staff-and-permissions": "staff",
    "account-security": "account_access", "data-export-and-deletion": "data_privacy",
    "contact-support": "feature_request",
}

ALWAYS_HUMAN = {"refund", "security", "outage"}


def _ticket_text(ticket: dict) -> str:
    return f"{ticket.get('subject', '')}\n{ticket.get('body', '')}"


def _bump(priority: str, to_at_least: str) -> str:
    return max(priority, to_at_least, key=tx.PRIORITIES.index)


def _sentiment(t: str) -> str:
    neg = sum(t.count(w) for w in tx.NEGATIVE_WORDS)
    pos = sum(t.count(w) for w in tx.POSITIVE_WORDS)
    if neg > pos:
        return "negative"
    if pos > neg:
        return "positive"
    return "neutral"


def rules_triage(ticket: dict, kb: KnowledgeBase, macros: list[dict], agent_name: str) -> dict:
    text = _ticket_text(ticket)
    t = text.lower()

    scores = {cat: sum(w for phrase, w in rules if phrase in t) for cat, rules in tx.KEYWORDS.items()}
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    (category, top), (_, second) = ranked[0], ranked[1]
    hits = kb.search(text, k=3)
    if top == 0:
        # No keyword matched: fall back to whichever help article fits best.
        category = SLUG_TO_CATEGORY.get(hits[0][0].slug, "presales") if hits else "presales"
    confidence = round(top / (top + second), 2) if top else 0.3

    sentiment = _sentiment(t)
    churn_risk = any(w in t for w in tx.CHURN_WORDS) and (sentiment == "negative" or category == "cancellation")

    priority = tx.DEFAULT_PRIORITY.get(category, "normal")
    if category == "refund" and any(w in t for w in ("twice", "duplicate", "double charge")):
        priority = _bump(priority, "high")
    if category not in ("spam", "feedback", "feature_request") and any(w in t for w in tx.URGENCY_WORDS):
        priority = _bump(priority, "high")
    if churn_risk and sentiment == "negative":
        priority = _bump(priority, "high")

    macro_id = choose_macro(category, text, churn_risk)
    macro = by_id(macros)[macro_id]
    first_name = ticket["customer"]["name"].split()[0]
    draft, missing = fill(macro["body"], {"customer_first_name": first_name, "agent_name": agent_name})

    tags = list(dict.fromkeys(macro["actions"].get("tags", []) + (["churn_risk"] if churn_risk else [])))
    return {
        "ticket_id": ticket["id"],
        "engine": "rules",
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "churn_risk": churn_risk,
        "tags": tags,
        "macro_id": macro_id,
        "macro_title": macro["title"],
        "summary": ticket.get("subject", ""),
        "draft_reply": draft,
        "unfilled_placeholders": missing,
        "needs_human": bool(category in ALWAYS_HUMAN or missing or confidence < 0.6),
        "cited_articles": [h[0].slug for h in hits[:2]],
        "confidence": confidence,
    }


SYSTEM_PROMPT = """You are a support operations assistant for Pharos, an online booking and reminders app for small service businesses. You triage incoming support tickets and draft replies that a human agent reviews before sending.

Rules:
- Use only facts found in the HELP CENTER EXCERPTS and MACROS. Never invent features, prices, dates, or policies.
- Follow the refund policy exactly. Never promise a refund the policy does not allow.
- Write the reply as the agent will send it after taking the actions the chosen macro describes.
- Never ask the customer for their password.
- Security reports: thank the reporter, say it has been escalated, point them to security@pharos.example, and do not confirm or discuss details.
- Spam or vendor pitches: draft_reply must be an empty string.
- Answer every question the customer asked. If something is not supported, say so plainly and offer the closest workaround from the docs.
- Match the customer's emotion: acknowledge frustration specifically, without over-apologizing.
- Plain language, short paragraphs, numbered steps when there are steps. Under 180 words. Sign off as "{agent_name}" then "Pharos Support" on the next line.

Priority guide:
- urgent: Pharos down for many users, or a security issue
- high: the business is losing bookings or money right now, can't access their account with clients waiting, double charges, repeated failures, or a frustrated customer threatening to leave
- normal: a how-to question or a single problem with a workaround
- low: feature requests, praise, spam

Return one JSON object with exactly these keys:
category: one of {categories}
priority: one of low, normal, high, urgent
sentiment: one of negative, neutral, positive
churn_risk: true or false
macro_id: the id of the macro your reply is based on
tags: a list of 2 to 5 short snake_case tags
summary: one sentence telling the agent what the customer needs
draft_reply: the reply text
needs_human: true if a person must do something before replying (refund, identity check, escalation, investigation)
cited_articles: list of help-center slugs you relied on
confidence: a number from 0 to 1"""


def build_llm_prompt(ticket: dict, kb: KnowledgeBase, macros: list[dict], suggested_macro: str) -> str:
    text = _ticket_text(ticket)
    hits = kb.search(text, k=4)
    excerpts = "\n\n".join(f"[{c.slug} > {c.heading}]\n{(c.intro + chr(10)) if c.intro else ''}{c.text}" for c, _, _ in hits)

    # Candidate macros: the rules engine's pick plus the best text matches.
    q = set(tokenize(text))
    scored = sorted(macros, key=lambda m: len(q & set(tokenize(m["title"] + " " + m["body"]))), reverse=True)
    candidates = [by_id(macros)[suggested_macro]] + [m for m in scored if m["id"] != suggested_macro][:3]
    cand_text = "\n\n".join(
        f"[{m['id']}] {m['title']} (category: {m['category']})\nInternal note: {m.get('internal_note', '')}\n{m['body']}"
        for m in candidates
    )
    catalog = "\n".join(f"{m['id']}: {m['title']}" for m in macros)
    c = ticket["customer"]
    return f"""TICKET {ticket['id']}
From: {c['name']} <{c['email']}>
Business: {c.get('business', '')}
Plan: {c.get('plan', '')}
Channel: {ticket.get('channel', '')}
Subject: {ticket.get('subject', '')}

{ticket.get('body', '')}

HELP CENTER EXCERPTS
{excerpts}

CANDIDATE MACROS (full text)
{cand_text}

ALL MACROS
{catalog}"""


def llm_triage(ticket: dict, kb: KnowledgeBase, macros: list[dict], llm, agent_name: str) -> dict:
    baseline = rules_triage(ticket, kb, macros, agent_name)
    system = SYSTEM_PROMPT.format(agent_name=agent_name, categories=", ".join(tx.CATEGORIES))
    prompt = build_llm_prompt(ticket, kb, macros, baseline["macro_id"])
    try:
        raw = llm.complete(system, prompt, json_mode=True)
        out = extract_json(raw)
    except Exception as e:  # bad JSON, timeout, model not pulled...
        baseline["engine"] = f"rules (fallback: {type(e).__name__}: {str(e)[:120]})"
        return baseline

    result = dict(baseline)
    result["engine"] = f"{llm.name}:{llm.model}"
    if out.get("category") in tx.CATEGORIES:
        result["category"] = out["category"]
    if out.get("priority") in tx.PRIORITIES:
        result["priority"] = out["priority"]
    if out.get("sentiment") in ("negative", "neutral", "positive"):
        result["sentiment"] = out["sentiment"]
    if isinstance(out.get("churn_risk"), bool):
        result["churn_risk"] = out["churn_risk"]
    macro_map = by_id(macros)
    if out.get("macro_id") in macro_map:
        result["macro_id"] = out["macro_id"]
        result["macro_title"] = macro_map[out["macro_id"]]["title"]
    if isinstance(out.get("tags"), list) and out["tags"]:
        result["tags"] = [str(x) for x in out["tags"]][:6]
    if isinstance(out.get("summary"), str) and out["summary"].strip():
        result["summary"] = out["summary"].strip()
    if isinstance(out.get("draft_reply"), str):
        result["draft_reply"] = out["draft_reply"].strip()
        result["unfilled_placeholders"] = []
    if isinstance(out.get("cited_articles"), list):
        valid = {c.slug for c in kb.chunks}
        result["cited_articles"] = [s for s in out["cited_articles"] if s in valid] or result["cited_articles"]
    try:
        result["confidence"] = round(float(out.get("confidence", result["confidence"])), 2)
    except (TypeError, ValueError):
        pass
    result["needs_human"] = bool(out.get("needs_human", False)) or result["category"] in ALWAYS_HUMAN
    result["rules_baseline"] = {"category": baseline["category"], "priority": baseline["priority"],
                                "macro_id": baseline["macro_id"]}
    return result


def summarize(results: list[dict], labels: dict | None = None) -> dict:
    from collections import Counter

    s = {
        "tickets": len(results),
        "by_category": dict(Counter(r["category"] for r in results).most_common()),
        "by_priority": {p: sum(r["priority"] == p for r in results) for p in reversed(tx.PRIORITIES)},
        "churn_risk": [r["ticket_id"] for r in results if r["churn_risk"]],
        "needs_human": sum(r["needs_human"] for r in results),
        "ready_to_send": sum(not r["needs_human"] and r["category"] != "spam" for r in results),
        "auto_closed_spam": sum(r["category"] == "spam" for r in results),
    }
    if labels:
        scored = [r for r in results if r["ticket_id"] in labels]
        if scored:
            s["accuracy"] = {
                "category": round(sum(r["category"] == labels[r["ticket_id"]]["category"] for r in scored) / len(scored), 3),
                "priority": round(sum(r["priority"] == labels[r["ticket_id"]]["priority"] for r in scored) / len(scored), 3),
                "misses": [
                    {"ticket_id": r["ticket_id"], "got": [r["category"], r["priority"]],
                     "expected": [labels[r["ticket_id"]]["category"], labels[r["ticket_id"]]["priority"]]}
                    for r in scored
                    if r["category"] != labels[r["ticket_id"]]["category"]
                    or r["priority"] != labels[r["ticket_id"]]["priority"]
                ],
            }
    return s


def to_json(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)
