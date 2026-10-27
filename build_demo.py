#!/usr/bin/env python3
"""Build the Pharos pages and the Cloudflare Worker from this project's docs, macros, tickets, and prompts.

Writes:
  index.html           the agent demo (help chat, ticket triage, macros), served at the site root
  demo/index.html      the same demo page
  portal/index.html    the public customer help portal (help chat only, no ticket data)
  worker/worker.js     the Cloudflare Worker, with the prompts built in

  python build_demo.py                                   # triage with the offline rules engine
  python build_demo.py --results output/triage_results.json --unseen-results output/holdout/triage_results.json
        # show results from AI runs instead (after running triage.py with --backend ollama)
  python build_demo.py --cloud-url https://pharos-ai.yourname.workers.dev
        # point the pages at a different Worker (pass "" to turn live AI off)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

import chat
from support_ops import kb as kbmod
from support_ops import taxonomy as tx
from support_ops.kb import KnowledgeBase
from support_ops.macros import load_macros
from support_ops.triage_engine import SYSTEM_PROMPT, rules_triage, summarize

ROOT = Path(__file__).resolve().parent
AGENT = "Alex"
CHAT_MAX_INPUT = 8000
WORKER_MARKER = "const WORKER_URL = /*__WORKER_URL__*/"


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


def replace_once(text: str, marker: str, value: str, where: str) -> str:
    if text.count(marker) != 1:
        raise RuntimeError(f"Expected exactly one {marker!r} in {where}, found {text.count(marker)}")
    return text.replace(marker, value)


def set_worker_url(text: str, worker_url: str, where: str) -> str:
    """Rewrite `const WORKER_URL = /*__WORKER_URL__*/"...";` with the configured Worker address."""
    lines = text.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if WORKER_MARKER in line]
    if len(hits) != 1:
        raise RuntimeError(f"Expected exactly one WORKER_URL marker in {where}, found {len(hits)}")
    i = hits[0]
    before, _ = lines[i].split(WORKER_MARKER, 1)
    end = "\n" if lines[i].endswith("\n") else ""
    lines[i] = f"{before}{WORKER_MARKER}{json.dumps(worker_url)};{end}"
    return "".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--results", help="triage_results.json for the sample tickets (default: run rules engine)")
    p.add_argument("--unseen-results", help="triage_results.json for the unseen tickets (e.g. output/holdout/triage_results.json)")
    p.add_argument("--docs-url", default="https://github.com/scenebiscuit-cell/support-desk-repo-1/blob/main/docs",
                   help="Where the pages' 'Source' links point (the help articles in your GitHub repo)")
    p.add_argument("--cloud-url", default="https://pharos-ai-worker.scenebiscuit.workers.dev",
                   help='HTTPS address of your Cloudflare Worker (pass "" to turn live AI off)')
    args = p.parse_args()

    worker_url = (args.cloud_url or "").rstrip("/")
    if worker_url:
        u = urlparse(worker_url)
        if u.scheme != "https" or not u.netloc or u.path not in ("", "/") or u.query or u.fragment:
            p.error("--cloud-url must be an HTTPS origin, such as https://pharos-ai-worker.example.workers.dev")

    kb = KnowledgeBase.from_dir(ROOT / "docs")
    macros = load_macros(ROOT / "macros" / "macros.json")
    docs_url = args.docs_url.rstrip("/")
    prompts_shown = {
        "triage": SYSTEM_PROMPT.format(agent_name=AGENT, categories=", ".join(tx.CATEGORIES)),
        "chat": chat.SYSTEM,
    }
    data = {
        "kb": {
            "stopwords": sorted(kbmod.STOPWORDS), "synonyms": kbmod.SYNONYMS, "phrases": kbmod.PHRASES,
            "chunks": [{**c.to_dict(), "url": f"{docs_url}/{c.slug}.md"} for c in kb.chunks],
            "articles": len({c.slug for c in kb.chunks}), "docs_url": docs_url,
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
                              kb, macros, Path(args.unseen_results) if args.unseen_results else None),
        },
        "prompts": prompts_shown,
        "thresholds": {"min_score": chat.MIN_SCORE, "min_coverage": chat.MIN_COVERAGE,
                       "strong": chat.STRONG_COVERAGE_SCORE},
        "agent": AGENT,
        "cloud_url": worker_url,
    }

    # Agent demo: demo/index.html, plus a copy at the site root for GitHub Pages.
    template = (ROOT / "demo" / "template.html").read_text(encoding="utf-8")
    template = set_worker_url(template, worker_url, "demo/template.html")
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out = replace_once(template, "/*__DEMO_DATA__*/null", blob, "demo/template.html")
    # demo/ sits one folder down, so its portal link needs to climb back out.
    (ROOT / "demo" / "index.html").write_text(out.replace('href="portal/"', 'href="../portal/"'), encoding="utf-8")
    # GitHub Pages serves the root file as-is, so give it a doctype (keeps browsers out of quirks mode).
    root_page = '<!doctype html>\n<html lang="en">\n' + out + "\n</html>\n"
    (ROOT / "index.html").write_text(root_page, encoding="utf-8")

    # Public portal: help-center content only, never tickets or macros.
    portal = (ROOT / "portal" / "template.html").read_text(encoding="utf-8")
    portal = set_worker_url(portal, worker_url, "portal/template.html")
    portal_data = {"kb": data["kb"], "thresholds": data["thresholds"], "max_input": CHAT_MAX_INPUT}
    portal_blob = json.dumps(portal_data, ensure_ascii=False).replace("</", "<\\/")
    portal_out = replace_once(portal, "/*__PORTAL_DATA__*/null", portal_blob, "portal/template.html")
    (ROOT / "portal" / "index.html").write_text(portal_out, encoding="utf-8")

    # Worker: the system prompts live server-side, so visitors can't repurpose the model.
    prompts = {"chat": chat.SYSTEM,
               "triage": prompts_shown["triage"] + "\n\nRespond with a single JSON object and nothing else."}
    wt = (ROOT / "worker" / "worker.template.js").read_text(encoding="utf-8")
    wt = replace_once(wt, "/*__CHAT_MAX_INPUT__*/8000", str(CHAT_MAX_INPUT), "worker/worker.template.js")
    wt = replace_once(wt, "/*__PROMPTS__*/null", json.dumps(prompts, ensure_ascii=False, indent=2),
                      "worker/worker.template.js")
    (ROOT / "worker" / "worker.js").write_text(wt, encoding="utf-8")

    s = data["sets"]
    print(f"Built index.html + demo/index.html ({len(out) // 1024} KB): {len(kb.chunks)} doc sections, "
          f"{len(macros)} macros, {len(s['sample']['tickets'])} + {len(s['unseen']['tickets'])} tickets "
          f"({s['sample']['engine']})")
    print(f"Built portal/index.html ({len(portal_out) // 1024} KB): help-center content only")
    print(f"Built worker/worker.js · live AI via {worker_url or 'nothing (live AI off)'}")


if __name__ == "__main__":
    main()
