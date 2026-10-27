# Pharos Support Desk — notes for Claude Code

A portfolio demo by Nick Lax (nlaxatx@gmail.com) for AI support-ops freelancing. Pharos is a **fictional project-management app for small teams**. Never reintroduce the old booking/reminders company.

## What's here
- `docs/` 12 help articles · `macros/macros.json` 23 macros · `data/` sample (20) and unseen (12) tickets with hand labels
- `support_ops/` Python engine: BM25 search (`kb.py`), rules triage + LLM prompt (`triage_engine.py`), taxonomy, macros
- `chat.py`, `triage.py`, `export_macros.py` — CLI tools (Python stdlib only, no pip installs)
- `demo/template.html` → **generated** `demo/index.html` and `index.html` (site home): agent demo (help chat, triage, macros)
- `portal/template.html` → **generated** `portal/index.html`: public customer help portal (chat only — never ticket/macro data)
- `worker/worker.template.js` → **generated** `worker/worker.js`: Cloudflare Worker (Llama 3.3 70B) with daily caps, origin lock, and a voice guard that cleans AI drafts
- `DESIGN.md` is the design system (lapis + gold, papyrus page, IBM Plex, canvas wave masthead). Follow it.

## Workflow
1. Edit templates and Python sources only — never hand-edit the generated files.
2. `python build_demo.py` (rebuilds all pages and `worker/worker.js`)
3. Tests, all must pass:
   - `node tests/parity.js` — the page's JS triage must match the Python rules engine exactly (0 mismatches). JS search/triage in `demo/template.html` mirrors `support_ops/`; change both together.
   - `node tests/worker_voice.mjs` — Worker draft cleanup
   - `python triage.py --eval` — sample set should stay at 100% category/priority. Report the unseen-set number (`--tickets data/holdout_tickets.json --labels data/holdout_labels.json --out output/holdout`); don't tune rules on the unseen tickets.
4. For visual changes, screenshot the pages with Playwright (desktop + 390px phone, light + dark).

## Hard rules
- **Never modify `worker/wrangler.toml` or `.github/workflows/`.** They hold the live Cloudflare config.
- Never commit API keys, tokens, or secrets.
- Don't push to `main`. Work on a branch and open a pull request for Nick to review. Pushing `worker/**` to main redeploys the live Worker.
- Keep the pages self-contained: inline CSS/JS, fonts only from Google Fonts, no build tools or frameworks.
- Keep `[hidden]{display:none!important}`, reduced-motion support, keyboard access, and the 16px phone gutter.

## Reply voice (drafts, macros, and the Worker's cleanup)
- Open with "Thank you for contacting Pharos." Never "Thanks for reaching out."
- Don't restate the customer's problem. No corporate filler ("I understand your frustration", "we apologize for any inconvenience", "rest assured").
- Billing mistakes: one short, kind apology ("Sorry about that!"), then what was done. Not groveling.
- Greeting "Hi {first name}," and sign-off "Best,\nAlex\nPharos Support".
- Refunds, identity checks, and security reports always set `needs_human`.
