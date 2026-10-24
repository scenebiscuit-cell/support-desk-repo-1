#!/usr/bin/env python3
"""Triage a batch of support tickets: category, priority, tags, macro, and a draft reply.

Examples
  python triage.py                                  # offline rules engine, no AI
  python triage.py --backend ollama                 # local model via Ollama
  python triage.py --backend ollama --model qwen2.5:7b
  python triage.py --backend anthropic              # Claude API (set ANTHROPIC_API_KEY)
  python triage.py --eval                           # also score against data/labels.json
  python triage.py --eval --tickets data/holdout_tickets.json --labels data/holdout_labels.json --out output/holdout

Writes output/triage_results.json, output/triage_results.csv and output/triage_report.md
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

from support_ops.kb import KnowledgeBase
from support_ops.llm import LLMError, get_llm
from support_ops.macros import load_macros
from support_ops.triage_engine import llm_triage, rules_triage, summarize, to_json

ROOT = Path(__file__).resolve().parent


def write_csv(results: list[dict], path: Path) -> None:
    cols = ["ticket_id", "category", "priority", "sentiment", "churn_risk", "needs_human", "macro_id",
            "tags", "summary", "confidence", "engine", "draft_reply"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in results:
            w.writerow([" ".join(r[c]) if c == "tags" else r[c] for c in cols])


def write_report(results: list[dict], tickets: dict, summary: dict, path: Path, engine: str, seconds: float) -> None:
    lines = [
        "# Triage report", "",
        f"Engine: **{engine}**  ·  Tickets: **{summary['tickets']}**  ·  Time: {seconds:.1f}s", "",
        f"- Ready to send after a quick review: **{summary['ready_to_send']}**",
        f"- Need a person to act first (refund, identity check, escalation): **{summary['needs_human']}**",
        f"- Spam closed automatically: **{summary['auto_closed_spam']}**",
        f"- Churn risk flagged: **{', '.join(summary['churn_risk']) or 'none'}**", "",
    ]
    if "accuracy" in summary:
        a = summary["accuracy"]
        lines += [f"**Accuracy vs. hand labels:** category {a['category']:.0%}, priority {a['priority']:.0%}", ""]
        for m in a["misses"]:
            lines.append(f"- {m['ticket_id']}: got {m['got'][0]}/{m['got'][1]}, expected {m['expected'][0]}/{m['expected'][1]}")
        lines.append("")
    lines += ["## Queue (sorted by priority)", "", "| Ticket | Priority | Category | Macro | Human? | Subject |",
              "|---|---|---|---|---|---|"]
    order = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
    for r in sorted(results, key=lambda r: order[r["priority"]]):
        subj = tickets[r["ticket_id"]]["subject"].replace("|", "/")
        lines.append(f"| {r['ticket_id']} | {r['priority']} | {r['category']} | {r['macro_id']} | "
                     f"{'yes' if r['needs_human'] else 'no'} | {subj} |")
    lines += ["", "## Drafts", ""]
    for r in sorted(results, key=lambda r: order[r["priority"]]):
        t = tickets[r["ticket_id"]]
        lines += [f"### {r['ticket_id']} · {t['subject']}", "",
                  f"*{t['customer']['name']}, {t['customer'].get('business', '')} ({t['customer'].get('plan', '')})*  ",
                  f"**{r['priority']}** · {r['category']} · {r['sentiment']} · macro {r['macro_id']} · "
                  f"tags: {', '.join(r['tags'])}", "", f"> {t['body']}", "", "**Draft reply:**", "",
                  "```", r["draft_reply"] or "(no reply: closed as spam)", "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--backend", choices=["rules", "ollama", "anthropic"], default="rules")
    p.add_argument("--model", help="Model name for the backend (e.g. llama3.1:8b or qwen2.5:7b)")
    p.add_argument("--tickets", default=str(ROOT / "data" / "tickets.json"))
    p.add_argument("--out", default=str(ROOT / "output"))
    p.add_argument("--agent-name", default="Alex")
    p.add_argument("--eval", action="store_true", help="Score results against hand labels")
    p.add_argument("--labels", default=str(ROOT / "data" / "labels.json"), help="Labels file for --eval")
    p.add_argument("--only", help="Comma-separated ticket ids to run, e.g. T-1003,T-1007")
    args = p.parse_args()

    kb = KnowledgeBase.from_dir(ROOT / "docs")
    macros = load_macros(ROOT / "macros" / "macros.json")
    tickets = json.loads(Path(args.tickets).read_text(encoding="utf-8"))
    if args.only:
        wanted = set(args.only.split(","))
        tickets = [t for t in tickets if t["id"] in wanted]

    try:
        llm = get_llm(args.backend, args.model)
    except LLMError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    engine = "rules" if llm is None else f"{llm.name}:{llm.model}"
    print(f"Triaging {len(tickets)} tickets with {engine} ...")

    results, start = [], time.time()
    for t in tickets:
        r = rules_triage(t, kb, macros, args.agent_name) if llm is None else llm_triage(t, kb, macros, llm, args.agent_name)
        results.append(r)
        flag = " (fallback to rules)" if r["engine"].startswith("rules (fallback") else ""
        print(f"  {t['id']}  {r['priority']:<7} {r['category']:<16} {r['macro_id']}{flag}")
    seconds = time.time() - start

    labels = None
    if args.eval:
        labels = {k: v for k, v in json.loads(Path(args.labels).read_text()).items() if not k.startswith("_")}
    summary = summarize(results, labels)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "triage_results.json").write_text(to_json({"engine": engine, "summary": summary, "results": results}), encoding="utf-8")
    write_csv(results, out / "triage_results.csv")
    write_report(results, {t["id"]: t for t in tickets}, summary, out / "triage_report.md", engine, seconds)

    print(f"\nReady to send: {summary['ready_to_send']}  ·  Needs a person: {summary['needs_human']}  ·  "
          f"Spam closed: {summary['auto_closed_spam']}  ·  Churn risk: {', '.join(summary['churn_risk']) or 'none'}")
    if "accuracy" in summary:
        a = summary["accuracy"]
        print(f"Accuracy vs. labels: category {a['category']:.0%}, priority {a['priority']:.0%}")
    print(f"Wrote {out / 'triage_report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
