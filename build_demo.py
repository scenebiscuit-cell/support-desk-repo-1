#!/usr/bin/env python3
"""Build the demo page and Cloudflare Worker from the project's source prompts and data.

  python build_demo.py                                   # triage with the offline rules engine
  python build_demo.py --results output/triage_results.json
        # show results from an AI run instead (e.g. after: python triage.py --backend ollama)
  python build_demo.py --cloud-url https://worker.example.workers.dev
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
    p.add_argument("--cloud-url", help="HTTPS root URL of the deployed Cloudflare Worker")
    args = p.parse_args()

    kb = KnowledgeBase.from_dir(ROOT / "docs")
    macros = load_macros(ROOT / "macros" / "macros.json")
    prompts = {
        "triage": SYSTEM_PROMPT.format(agent_name=AGENT, categories=", ".join(tx.CATEGORIES)),
        "chat": chat.SYSTEM,
    }
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
        "prompts": prompts,
        "thresholds": {"min_score": chat.MIN_SCORE, "min_coverage": chat.MIN_COVERAGE,
                       "strong": chat.STRONG_COVERAGE_SCORE},
        "agent": AGENT,
    }
    worker_url = args.cloud_url.rstrip("/") if args.cloud_url else read_worker_url(ROOT / "index.html")
    if worker_url:
        parsed = urlparse(worker_url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.path not in ("", "/") or parsed.query or parsed.fragment:
            p.error("--cloud-url must be an HTTPS origin, such as https://pharos-ai-worker.example.workers.dev")

    template = (ROOT / "demo" / "template.html").read_text(encoding="utf-8")
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = replace_worker_url(template, worker_url)
    out = template.replace("/*__DEMO_DATA__*/null", blob)
    (ROOT / "demo" / "index.html").write_text(out, encoding="utf-8")
    portal_template = (ROOT / "portal" / "template.html").read_text(encoding="utf-8")
    portal_data = {"kb": data["kb"], "thresholds": data["thresholds"], "max_input": CHAT_MAX_INPUT}
    portal_blob = json.dumps(portal_data, ensure_ascii=False).replace("</", "<\\/")
    portal_marker = "/*__PORTAL_DATA__*/null"
    if portal_template.count(portal_marker) != 1:
        raise RuntimeError("Expected exactly one PORTAL_DATA marker in portal/template.html")
    portal_template = replace_worker_url(portal_template, worker_url)
    portal_out = portal_template.replace(portal_marker, portal_blob)
    (ROOT / "portal" / "index.html").write_text(portal_out, encoding="utf-8")
    root_page = (ROOT / "index.html").read_text(encoding="utf-8")
    (ROOT / "index.html").write_text(replace_worker_url(root_page, worker_url), encoding="utf-8")
    worker_template = (ROOT / "worker" / "worker.template.js").read_text(encoding="utf-8")
    limit_marker = "/*__CHAT_MAX_INPUT__*/8000"
    if worker_template.count(limit_marker) != 1:
        raise RuntimeError("Expected exactly one CHAT_MAX_INPUT marker in worker/worker.template.js")
    worker_template = worker_template.replace(limit_marker, str(CHAT_MAX_INPUT))
    prompt_json = json.dumps(prompts, ensure_ascii=False).replace("</", "<\\/")
    prompt_marker = "/*__PROMPTS__*/{}"
    if worker_template.count(prompt_marker) != 1:
        raise RuntimeError("Expected exactly one PROMPTS marker in worker/worker.template.js")
    worker = worker_template.replace(prompt_marker, prompt_json)
    (ROOT / "worker" / "worker.js").write_text(worker, encoding="utf-8")
    s = data["sets"]
    print(f"Built demo/index.html ({len(out) // 1024} KB): {len(kb.chunks)} doc sections, {len(macros)} macros, "
          f"{len(s['sample']['tickets'])} + {len(s['unseen']['tickets'])} tickets ({s['sample']['engine']})")
    print(f"Built portal/index.html ({len(portal_out) // 1024} KB): help-center content only")
    print(f"Built worker/worker.js and index.html (Cloudflare Worker URL: {worker_url or 'not configured'})")


def read_worker_url(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    marker = 'const WORKER_URL = /*__WORKER_URL__*/'
    for line in text.splitlines():
        if marker in line:
            value = line.split(marker, 1)[1].strip().rstrip(";")
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                break
    return ""


def replace_worker_url(text: str, worker_url: str) -> str:
    marker = 'const WORKER_URL = /*__WORKER_URL__*/'
    replacement = f"{marker}{json.dumps(worker_url)}"
    lines = text.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if marker in line]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one WORKER_URL marker, found {len(matches)}")
    index = matches[0]
    before, after = lines[index].split(marker, 1)
    value = after.strip().rstrip(";")
    try:
        json.loads(value)
    except json.JSONDecodeError as exc:
        raise RuntimeError("WORKER_URL marker must be followed by a JSON string") from exc
    lines[index] = f"{before}{replacement};\n" if lines[index].endswith("\n") else f"{before}{replacement}"
    return "".join(lines)


if __name__ == "__main__":
    main()
