# Pharos Support Desk

**AI support operations for a small software company: a help-center chatbot that only answers from the docs, ticket triage that drafts on-policy replies, and a macro library, with every result measured against hand-labeled tickets.**

*Created by Nick Lax · nlaxatx@gmail.com*

**[Live demo](https://scenebiscuit-cell.github.io/support-desk-repo-1/)** · **[Customer help portal](https://scenebiscuit-cell.github.io/support-desk-repo-1/portal/)** · **Walkthrough video:** *coming soon*

![The Pharos Support Desk demo](screenshots/hero.png)

## The problem

Small support teams lose hours every week to the same three things: sorting the inbox, rewriting the same replies, and answering questions that are already in the help center. AI can help with all three, but only if it doesn't make things up, doesn't promise refunds it can't give, and keeps a person in charge of anything risky.

Pharos is a fictional project-management app for small teams. I built its support operation the way I'd build one for a real client: from the help articles and policies outward, and measured before trusting.

## What I built

| | What it does | Guardrail |
|---|---|---|
| **Help-center chatbot ("the Keeper")** | Searches 12 help articles and answers from them, citing the source | Answers only when the docs clearly cover the question; otherwise hands off to a person instead of guessing |
| **Ticket triage** | Tags each ticket with category, priority, sentiment, and churn risk, picks the best macro, and drafts a reply | Refunds, outages, and security reports are always flagged for a person; drafts are never auto-sent |
| **Macro library** | 23 on-policy replies with tags, status actions, and internal notes; exports to CSV for any helpdesk | One consistent policy answer, whoever is on shift |
| **Customer help portal** | The public-facing version of the chatbot, with no ticket or staff data | Warns visitors not to share passwords or payment details |

![Help chat with its search trace](screenshots/help-chat.png)

*The chat shows which help-center sections matched, how strongly, and why it answered or handed off.*

## How it works

1. **Search.** Help articles are split into sections and ranked with BM25 keyword search, plus synonyms and phrases ("can't log in" → login). It's fast, free, and explainable.
2. **Confidence gate.** The bot only answers when the best match clears a relevance bar. Below it, the question goes to a person.
3. **Triage, two layers.** A rules engine gives an instant, free baseline. An AI layer (Llama 3.3 70B on Cloudflare Workers AI, a local model through Ollama, or Claude) reads the ticket with the matching help sections and candidate macros, and returns structured JSON. If the AI fails or returns bad JSON, that ticket falls back to the rules.
4. **Voice guard.** AI drafts are cleaned up server-side before an agent sees them: stock phrases like "I understand your frustration" are removed, every draft opens with "Thank you for contacting Pharos," and it ends with one consistent sign-off.
5. **Cost and abuse limits.** The live AI runs on a small Cloudflare Worker that only serves this site, keeps the prompts server-side, caps input size, and limits each visitor to 10 AI answers a day (40 for the whole demo). That keeps it on Cloudflare's free tier.

![Ticket triage with an escalation and draft reply](screenshots/triage.png)

## Results

Every ticket has a hand label (correct category and priority), so accuracy is scored, not eyeballed. The **unseen** tickets were written and labeled after the rules were finished, and the rules were never tuned on them.

| Test set | Tickets | Routed to the right category | Right priority |
|---|---|---|---|
| Sample (rules written alongside these) | 20 | **100%** (20/20) | 100% |
| **Unseen** | **36** | **78%** (28/36) | 72% (26/36) |

![Accuracy chart](screenshots/accuracy.png)

**What the misses taught me.** Of the 36 unseen tickets, the rules flagged every refund and outage for a person. They missed two security reports ("someone logged into my account from another country"), which looked like ordinary login problems. Keyword rules can't tell those apart; reading intent is exactly the job of the AI layer, and it's why I'd measure any AI support tool on unseen tickets before trusting it.

![The public help portal answering with a cited source](screenshots/portal.png)

## What I'd do next

- **Score the AI layer on the same 36 unseen tickets** and put that number next to the rules baseline.
- **Add a security safety net:** route any mention of an unrecognized login straight to security, whatever the rest of the ticket says.
- **Use embeddings** for search once a help center grows past a few dozen articles.
- **Connect a real helpdesk** (Zendesk, Help Scout, or Freshdesk) so tags, macros, and drafts land where agents already work.
- **Track deflection:** what share of chat questions got answered without a ticket, and how many handoffs turned out to be covered by the docs.

---

# Running it

Everything is Python standard library. Nothing to `pip install`.

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
node tests/parity.js           # the web page's triage matches the Python engine exactly
node tests/worker_voice.mjs    # the Worker's draft cleanup
```

See **Results** above for the current numbers. To score an AI backend on the unseen set, add `--backend ollama` (or `anthropic`) to the second command.

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
data/holdout_tickets.json 36 unseen tickets       data/holdout_labels.json  their hand labels
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
screenshots/              images used in this README
tests/                   parity and Worker voice tests
worker/                  Cloudflare Worker for free live AI: worker.template.js → worker.js, wrangler.toml, README.md
.github/workflows/        deploys the Worker when worker/ changes
output/                  generated reports
```

## Known limits

- Search is keyword-based (BM25 with synonyms), not embeddings. It's fast and free and works well for a help center this size; a client with hundreds of articles may want embeddings.
- The chatbot's handoff thresholds were tuned on a handful of questions. Re-check them against real customer questions.
- Drafts are for an agent to review, never to auto-send. The design keeps refunds, identity checks, and security reports with people.
- Pharos, its customers, and all domains (`*.example`) are fictional.
