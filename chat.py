#!/usr/bin/env python3
"""Help-center chatbot that answers only from the Pharos docs, cites its sources,
and hands off to a human when the docs don't cover the question.

Examples
  python chat.py                               # interactive, offline (shows the best doc section)
  python chat.py --backend ollama              # interactive, local model writes the answer
  python chat.py --ask "how do I cancel?"      # one question, then exit

Handoffs are appended to output/handoffs.jsonl so an agent can pick them up.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from support_ops.kb import KnowledgeBase, tokenize
from support_ops.llm import LLMError, get_llm

ROOT = Path(__file__).resolve().parent

# Tuned on the sample questions in README.md: below these, the docs probably don't answer it.
MIN_SCORE = 3.0          # BM25 score of the best match
MIN_COVERAGE = 0.5       # share of the question's words found in that match
STRONG_COVERAGE_SCORE = 2.5  # a lower score is fine when every word matched
FOLLOW_UP = re.compile(r"^(what about|how about|and|also|same for|what if)\b", re.I)
HUMAN_PATTERN = re.compile(r"\b(human|agent|person|representative|real person|talk to someone|call me)\b", re.I)

SYSTEM = """You are the help-center assistant for Pharos, project management software for small teams.

Answer the customer's question using ONLY the HELP CENTER EXCERPTS below.
- If the excerpts don't contain the answer, reply exactly: HANDOFF
- Never guess at prices, policies, or features that aren't in the excerpts.
- Be brief, warm, and human: 2 to 6 sentences, or short numbered steps. Use contractions.
- Don't repeat the customer's question back to them. Answer it.
- Use the exact menu paths from the docs, like Settings > Billing.
- End with one line: "Source: <article title>"."""


def answer(question: str, kb: KnowledgeBase, llm, history: list[str]) -> dict:
    if HUMAN_PATTERN.search(question):
        return {"type": "handoff", "reason": "asked for a person", "text": None, "sources": []}

    # Follow-ups like "what about annual?" borrow the previous question's words.
    follow_up = bool(history) and FOLLOW_UP.match(question) and len(tokenize(question)) <= 3
    query = f"{history[-1]} {question}" if follow_up else question
    hits = kb.search(query, k=3)
    def confident(score: float, coverage: float) -> bool:
        if coverage >= 1.0:
            return score >= STRONG_COVERAGE_SCORE
        return score >= MIN_SCORE and coverage >= MIN_COVERAGE

    if not hits or not confident(hits[0][1], hits[0][2]):
        return {"type": "handoff", "reason": "not covered by the docs", "text": None,
                "sources": [h[0].to_dict() for h in hits[:1]]}

    top = hits[0][0]
    if llm is None:
        sections = [top]
        # A close second match from the same article usually completes the answer.
        if len(hits) > 1 and hits[1][0].slug == top.slug and hits[1][1] >= 0.6 * hits[0][1]:
            sections.append(hits[1][0])
        intro = f"{top.intro}\n\n" if top.intro else ""
        text = f"From \"{top.title}\":\n\n{intro}" + "\n\n".join(f"{c.heading}\n{c.text}" for c in sections)
        return {"type": "answer", "text": text, "sources": [top.to_dict()],
                "related": [h[0].to_dict() for h in hits[1:] if h[0].slug != top.slug]}

    excerpts = "\n\n".join(f"[{c.title} > {c.heading}]\n{c.intro}\n{c.text}".replace("\n\n", "\n") for c, _, _ in hits)
    reply = llm.complete(SYSTEM, f"HELP CENTER EXCERPTS\n{excerpts}\n\nCUSTOMER QUESTION\n{question}").strip()
    if reply.upper().startswith("HANDOFF"):
        return {"type": "handoff", "reason": "model found no answer in the docs", "text": None,
                "sources": [h[0].to_dict() for h in hits]}
    return {"type": "answer", "text": reply, "sources": [h[0].to_dict() for h in hits]}


def log_handoff(question: str, reason: str, transcript: list[dict]) -> Path:
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    path = out / "handoffs.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"created_at": datetime.now().isoformat(timespec="seconds"),
                            "question": question, "reason": reason, "transcript": transcript}) + "\n")
    return path


def show(result: dict, question: str, transcript: list[dict]) -> None:
    if result["type"] == "handoff":
        log_handoff(question, result["reason"], transcript)
        if result["reason"] == "asked for a person":
            print("\nKeeper: Sure. I've passed this conversation to our support team, and they'll reply by email. "
                  "They answer within 1 business day (4 business hours on the Business plan).")
        else:
            print("\nKeeper: I'm not certain about that one, so I've passed your question to our support team "
                  "rather than guess. They reply within 1 business day (4 business hours on the Business plan).")
        print(f"     [handoff logged: {result['reason']}]\n")
        return
    print(f"\nKeeper: {result['text']}")
    if result["sources"]:
        print(f"     Read more: {result['sources'][0]['url']}")
    print()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--backend", choices=["rules", "ollama", "anthropic"], default="rules")
    p.add_argument("--model")
    p.add_argument("--ask", help="Ask one question and exit")
    args = p.parse_args()

    kb = KnowledgeBase.from_dir(ROOT / "docs")
    try:
        llm = get_llm(args.backend, args.model)
    except LLMError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    transcript: list[dict] = []
    history: list[str] = []
    if args.ask:
        res = answer(args.ask, kb, llm, history)
        transcript.append({"role": "user", "text": args.ask})
        show(res, args.ask, transcript)
        return 0

    print("Ask the Keeper — Pharos Help (type 'quit' to exit)\n")
    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if q.lower() in {"quit", "exit", "q"}:
            break
        if not q:
            continue
        transcript.append({"role": "user", "text": q})
        try:
            res = answer(q, kb, llm, history)
        except LLMError as e:
            print(f"\n[backend error: {e}]\n")
            continue
        history.append(q)
        transcript.append({"role": "bot", "text": res.get("text") or "(handoff)"})
        show(res, q, transcript)
    return 0


if __name__ == "__main__":
    sys.exit(main())
