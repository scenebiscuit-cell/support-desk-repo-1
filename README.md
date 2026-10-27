# Pharos Support Desk — AI support-ops demo

*Created by Nick Lax · nlaxatx@gmail.com*

A working AI support-operations package for **Pharos**, a made-up project-management app for small teams. It has three parts:

1. **Help-center chatbot** (`chat.py`) — answers only from the company's docs, cites the article, and hands off to a person when the docs don't cover the question.
2. **Ticket triage** (`triage.py`) — tags each ticket with category, priority, sentiment, and churn risk, picks the right macro, and drafts a reply. Refunds, identity checks, and escalations are flagged for a human.
3. **Macro library** (`macros/`) — 23 on-policy replies with tags, priority/status actions, and internal notes. Exports to CSV and Markdown.

Plus two web pages, built from the real data in this folder:

- **Agent demo** (`index.html`, also at `demo/index.html`) puts all three tools in one shareable page.
- **Customer help portal** (`portal/index.html`) is what a customer would see: just the Keeper chat, no tickets or macros.

Everything is Python standard library. Nothing to `pip install`.

---

## Quick start (Windows, Mac, or Linux, Python 3.10+)

```bash
cd support-ops-demo

python triage.py --eval          # triage the 20 sample tickets with the offline rules engine
python chat.py                   # chat with the help center (type 'quit' to exit)
python export_macros.py          # regenerate macros.csv and macros.md
python build_demo.py             # rebuild demo/index.html
```

Results land in `output/`: `triage_report.md` (the readable one), `triage_results.csv`, `triage_results.json`.

## Three ways to run

| Backend | Command | Cost | Notes |
|---|---|---|---|
| Offline rules | `--backend rules` (default) | Free | Keyword rules + macro fill-in. Instant. Good baseline, brittle on new phrasing. |
| Local model | `--backend ollama` | Free | Runs on your own GPU through Ollama. Ticket data never leaves the machine. |
| Claude API | `--backend anthropic` | Pennies per ticket | Best drafts. Needs an API key. |

**Ollama (local):**

```bash
ollama pull llama3.1:8b          # or qwen2.5:7b, which is good at structured JSON
python triage.py --backend ollama --eval
python triage.py --backend ollama --model qwen2.5:7b --eval
python chat.py --backend ollama
```

An 8B model fits in 8 GB of VRAM. Set `OLLAMA_HOST` if Ollama runs on another machine on your network (e.g. `http://192.168.1.50:11434`).

**Claude API:**

```powershell
# PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python triage.py --backend anthropic --eval
```

Set `ANTHROPIC_MODEL` to change the model.

If a model returns bad JSON or times out, that ticket falls back to the rules engine and the run keeps going. The report marks which tickets fell back.

## Measuring it

Every ticket set has hand labels, so accuracy is scored rather than eyeballed.

```bash
python triage.py --eval                                                    # sample set
python triage.py --eval --tickets data/holdout_tickets.json --labels data/holdout_labels.json --out output/holdout
```

Current offline rules results:

| Set | Tickets | Category | Priority |
|---|---|---|---|
| Sample (rules were written alongside these) | 20 | 100% | 100% |
| Unseen (written after, rules not tuned on them) | 12 | 67% | 67% |

The gap is the point. Keyword rules break on new phrasing (a question about reusing a board named "Refund Requests" gets tagged as a refund; "sync later" in a mobile-offline feature request gets tagged as an integration problem; a suspicious-login report gets treated as a password reset). That's the job the LLM layer does. **Run the unseen set with Ollama or Claude and put that number in your pitch.**

## The demo page

`demo/index.html` is self-contained. Open it in a browser, or share the published version.

- **Help chat** shows which doc sections matched, how strongly, and why the bot answered or handed off.
- **Ticket triage** shows the queue sorted by priority, each ticket's tags, and the draft. "Try your own" triages any pasted ticket in the browser.
- **Macro library** is searchable and copyable.
- **AI mode**: when the page is opened inside Claude (claude.ai), "AI answer" and "Draft with AI" buttons appear and use the viewer's own Claude account. Everywhere else, the page runs on the offline engine, so it always works.

To show AI-written drafts in the queue, run triage with a model, then rebuild:

```bash
python triage.py --backend ollama
python build_demo.py --results output/triage_results.json
```

## Live AI for every visitor (free, Cloudflare)

Both pages call a small Cloudflare Worker that runs Llama 3.3 70B on Cloudflare's free Workers AI allowance, with per-visitor and daily limits so it stays free. The Worker for this repo is live at `https://pharos-ai-worker.scenebiscuit.workers.dev`, and `.github/workflows/deploy-worker.yml` redeploys it whenever anything in `worker/` changes on `main`. See **`worker/README.md`** for details.

`build_demo.py` regenerates `worker/worker.js` with the Keeper and triage instructions built in. The Worker also cleans up AI drafts before they reach the page: it removes stock phrases ("I understand your frustration", "rest assured"…), opens with "Thank you for contacting Pharos.", and signs off as Alex. To point the pages at a different Worker:

```bash
python build_demo.py --cloud-url https://pharos-ai.YOUR-SUBDOMAIN.workers.dev
```

## Public help portal

`portal/index.html` is the customer-facing help page, published at `/portal/`. It has only the help chat and a short explanation of how answers are grounded in the help center; it never includes ticket, triage, or macro data. When the Worker is configured, the portal sends the question and the matching article excerpts to `/chat`; if the Worker is unavailable, it shows the matching help-center passage instead. `python build_demo.py` regenerates it from `portal/template.html`.

## Live local AI on the demo page

When you open the demo page on a computer running Ollama, a **Local AI** toggle appears in the chat, and a **Draft with local AI** button appears on each ticket. Everything runs on that computer's GPU. Visitors without Ollama see the normal page.

One-time setup on Windows so Ollama accepts requests from the page:

1. Quit Ollama (right-click its icon in the system tray, then Quit).
2. Open Start, search "environment variables", and choose **Edit environment variables for your account**.
3. Click **New**. Name: `OLLAMA_ORIGINS`. Value: your GitHub Pages address, like `https://yourname.github.io` (no trailing slash). Click OK.
4. Start Ollama again.

Then open your GitHub Pages link in Chrome or Edge. If the browser asks to allow access to devices on your local network, click Allow.

## Adapting it for a client

1. Replace `docs/*.md` with their help articles (keep the small front-matter block and `## ` section headings).
2. Rewrite `macros/macros.json` with their policies and voice. Run `export_macros.py` for a CSV they can import or review.
3. Put 20–50 of their real past tickets in `data/tickets.json` and label them in `data/labels.json`. Hold back a few as an unseen set.
4. Edit categories and keywords in `support_ops/taxonomy.py`.
5. Run `--eval` with each backend and show them the numbers.

## Project layout

```
docs/                    12 help-center articles (Markdown)
data/tickets.json        20 sample tickets        data/labels.json          their hand labels
data/holdout_tickets.json 12 unseen tickets       data/holdout_labels.json  their hand labels
macros/                  macros.json (source), macros.csv, macros.md
support_ops/kb.py        doc chunking + BM25 search
support_ops/llm.py       Ollama / Anthropic backends (stdlib HTTP)
support_ops/taxonomy.py  categories, priorities, keyword rules
support_ops/macros.py    macro selection, placeholder fill, exports
support_ops/triage_engine.py  rules + LLM triage, prompt, scoring
triage.py  chat.py  export_macros.py  build_demo.py
demo/template.html → demo/index.html and index.html (the GitHub Pages home page)
portal/template.html → portal/index.html (public help portal)
DESIGN.md, PRODUCT.md     design system and product notes
worker/                  Cloudflare Worker for free live AI: worker.template.js → worker.js, wrangler.toml, README.md
.github/workflows/        deploys the Worker when worker/ changes
output/                  generated reports
```

## Known limits

- Search is keyword-based (BM25 with synonyms), not embeddings. It's fast and free and works well for a help center this size; a client with hundreds of articles may want embeddings.
- The chatbot's handoff thresholds were tuned on a handful of questions. Re-check them against real customer questions.
- Drafts are for an agent to review, never to auto-send. The design keeps refunds, identity checks, and security reports with people.
- Pharos, its customers, and all domains (`*.example`) are fictional.
