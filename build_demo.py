#!/usr/bin/env python3
"""Build demo/index.html: one self-contained page with the help chat, triage queue,
and macro library, using the real docs, macros, and triage results from this project.

  python build_demo.py                                   # triage with the offline rules engine
  python build_demo.py --results output/triage_results.json
        # show results from an AI run instead (e.g. after: python triage.py --backend ollama)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import chat
from support_ops import kb as kbmod
from support_ops import taxonomy as tx
from support_ops.kb import KnowledgeBase
from support_ops.macros import load_macros
from support_ops.triage_engine import SYSTEM_PROMPT, rules_triage, summarize

ROOT = Path(__file__).resolve().parent
AGENT = "Alex"


def run_set(tickets_path: Path, labels_path: Path, kb, macros, results_path: Path | None):
    tickets = json.loads(tickets_path.read_text(encoding="utf-8"))
    labels = {k: v for k, v in json.loads(labels_path.read_text()).items() if not k.startswith("_")}
    engine = "rules"
    if results_path and results_path.exists():
        data = json.loads(results_path.read_text(encoding="utf-8"))
        by_id = {r["ticket_id"]: r for r in data["results"]}
        if all(t["id"] in by_id for t in tickets):
            results, engine = [by_id[t["id"]] for t in tickets], data["engine"]
        else:
            results = [rules_triage(t, kb, macros, AGENT) for t in tickets]
    else:
        results = [rules_triage(t, kb, macros, AGENT) for t in tickets]
    return {"tickets": tickets, "results": results, "engine": engine,
            "summary": summarize(results, labels), "labels": labels}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--results", help="triage_results.json for the sample tickets (default: run rules engine)")
    args = p.parse_args()

    kb = KnowledgeBase.from_dir(ROOT / "docs")
    macros = load_macros(ROOT / "macros" / "macros.json")
    data = {
        "kb": {
            "stopwords": sorted(kbmod.STOPWORDS), "synonyms": kbmod.SYNONYMS, "phrases": kbmod.PHRASES,
            "chunks": [c.to_dict() for c in kb.chunks], "articles": len({c.slug for c in kb.chunks}),
        },
        "macros": macros,
        "taxonomy": {
            "categories": tx.CATEGORIES, "priorities": tx.PRIORITIES, "default_priority": tx.DEFAULT_PRIORITY,
            "keywords": tx.KEYWORDS, "urgency": tx.URGENCY_WORDS, "negative": tx.NEGATIVE_WORDS,
            "positive": tx.POSITIVE_WORDS, "churn": tx.CHURN_WORDS,
        },
        "sets": {
            "sample": run_set(ROOT / "data" / "tickets.json", ROOT / "data" / "labels.json", kb, macros,
                              Path(args.results) if args.results else None),
            "unseen": run_set(ROOT / "data" / "holdout_tickets.json", ROOT / "data" / "holdout_labels.json",
                              kb, macros, None),
        },
        "prompts": {
            "triage": SYSTEM_PROMPT.format(agent_name=AGENT, categories=", ".join(tx.CATEGORIES)),
            "chat": chat.SYSTEM,
        },
        "thresholds": {"min_score": chat.MIN_SCORE, "min_coverage": chat.MIN_COVERAGE,
                       "strong": chat.STRONG_COVERAGE_SCORE},
        "agent": AGENT,
    }
    template = (ROOT / "demo" / "template.html").read_text(encoding="utf-8")
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out = template.replace("/*__DEMO_DATA__*/null", blob)
    (ROOT / "demo" / "index.html").write_text(out, encoding="utf-8")
    s = data["sets"]
    print(f"Built demo/index.html ({len(out) // 1024} KB): {len(kb.chunks)} doc sections, {len(macros)} macros, "
          f"{len(s['sample']['tickets'])} + {len(s['unseen']['tickets'])} tickets ({s['sample']['engine']})")


if __name__ == "__main__":
    main()
