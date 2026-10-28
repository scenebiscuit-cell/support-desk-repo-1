# Pharos Support Desk — instructions for GitHub Copilot

These are the same project rules Claude Code follows (see `CLAUDE.md`). Read `DESIGN.md` before any visual change and `README.md` for the story.

A portfolio demo by Nick Lax (nlaxatx@gmail.com) for AI support-ops freelancing. Pharos is a **fictional project-management app for small teams**. Never reintroduce the old booking/reminders company.

## What's here
- `docs/` 12 help articles · `macros/macros.json` 23 macros · `data/` sample (20) and unseen (36) tickets with hand labels
- `support_ops/` Python engine: BM25 search (`kb.py`), rules triage + LLM prompt (`triage_engine.py`), taxonomy, macros
- `chat.py`, `triage.py`, `export_macros.py` — CLI tools (Python stdlib only, no pip installs)
- `demo/template.html` → **generated** `demo/index.html` and `index.html` (site home): agent demo (help chat, agent desk with triage, macros)
- `portal/template.html` → **generated** `portal/index.html`: public help center (Ask the Keeper, Contact support, My requests). Never show triage data, macros, or internal notes there.
- `shared/desk-store.js`: the request store both pages share via localStorage (key `pharos-desk-v1`); `build_demo.py` inlines it at `/*__DESK_STORE__*/`. The agent desk (Agent desk tab) is modeled on Jira Service Management.
- `worker/worker.template.js` → **generated** `worker/worker.js`: Cloudflare Worker (Llama 3.3 70B) with daily caps, origin lock, and a voice guard that cleans AI drafts
- `DESIGN.md` is the design system (lapis + gold, papyrus page, IBM Plex, canvas wave masthead). Follow it.

## Workflow
1. Edit templates and Python sources only — never hand-edit the generated files.
2. `python build_demo.py` (rebuilds all pages and `worker/worker.js`)
3. Tests, all must pass:
   - `node tests/parity.js` — the page's JS triage must match the Python rules engine exactly (0 mismatches). JS search/triage in `demo/template.html` mirrors `support_ops/`; change both together.
   - `node tests/worker_voice.mjs` — Worker draft cleanup
   - `python -m http.server 8000` then `node tests/e2e_desk.js` — portal → agent desk → portal loop (Playwright)
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

## Where things stand (Oct 2026)
Live: https://scenebiscuit-cell.github.io/support-desk-repo-1/ (agent demo) and `/portal/` (customer help portal).
Done: docs-grounded chat, Jira-style agent desk (live requests, SLA, internal notes, KB sharing), customer portal (contact support, My requests),
AI drafting via the Cloudflare Worker, lapis/gold design with wave + fish masthead, mobile pass, DuckDuckGo/Android WebView fixes, favicon and link previews.
Results: rules triage 100% on 20 sample tickets, 78% category / 72% priority on 36 unseen tickets.

## Open tasks Nick may ask for help with
- Add the walkthrough video link to README.md (replace "Walkthrough video: *coming soon*").
- Score the AI layer on the 36 unseen tickets with Ollama on Nick's PC and add that number next to the rules baseline in README.md, PITCH.md, and the How it works chart:
  `python triage.py --backend ollama --model qwen2.5:14b --eval --tickets data/holdout_tickets.json --labels data/holdout_labels.json --out output/holdout`
- Security safety net: route any mention of an unrecognized login straight to security (README "What I'd do next"). This is a rules change made because of a known failure class, so say so in the PR and report the unseen-set number before and after.
- If DuckDuckGo on Android still scrolls oddly, Nick will share a screen recording; keep fixes inside the responsive rules in DESIGN.md.

## Working with Nick
- He reviews every pull request on GitHub before merging. Explain changes in plain language.
- Paste full commands and steps in replies rather than referring to "earlier".
