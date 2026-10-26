# Pharos Cloudflare Worker

`worker.js` is generated from `worker.template.js` by `python build_demo.py`.
The builder injects `chat.SYSTEM` and the formatted `support_ops.triage_engine.SYSTEM_PROMPT`,
so the Cloudflare endpoints stay aligned with the demo's existing prompt sources.

## Bindings

The Worker requires:

- `AI`: Workers AI binding in `wrangler.toml`.
- `LIMITS`: a Cloudflare KV namespace for hashed visitor and global daily counters.

The `LIMITS` namespace is configured in `wrangler.toml`. To list namespaces or
create one for a new Cloudflare account:

```powershell
npx.cmd wrangler kv namespace list
npx.cmd wrangler kv namespace create LIMITS
```

If a `LIMITS` namespace already exists, reuse its ID instead of creating another.
Do not commit API tokens or secrets. The required non-secret variables are already
defined in `wrangler.toml`.

## Deploy

From the repository root:

```powershell
python build_demo.py
cd worker
npx.cmd wrangler deploy
```

The GitHub Actions workflow deploys on pushes to `main` that change `worker/**`, or
when manually dispatched. Configure the repository secrets `CLOUDFLARE_API_TOKEN`
and `CLOUDFLARE_ACCOUNT_ID` for that workflow.

The Worker serves `GET /health`, `POST /chat`, and `POST /triage`. Chat and triage
requests use `{ "input": "..." }` and successful AI responses use `{ "text": "..." }`.
Only the configured origin may use the AI endpoints. Inputs and model output token
counts are capped, and daily requests are limited globally and per visitor.
