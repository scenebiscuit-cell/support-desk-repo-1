/**
 * Pharos demo AI endpoint, running on Cloudflare Workers AI.
 *
 *   GET  /health   -> readiness and remaining daily allowance
 *   POST /chat     -> { input } and returns { text }
 *   POST /triage   -> { input } and returns { text }
 *
 * build_demo.py generates worker.js and injects the same system prompts used by
 * the demo's chat and triage engines. Edit this template, not worker.js.
 */
const DEFAULT_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast";
const PROMPTS = {"triage": "You are a support operations assistant for Pharos, an online booking and reminders app for small service businesses. You triage incoming support tickets and draft replies that a human agent reviews before sending.\n\nRules:\n- Use only facts found in the HELP CENTER EXCERPTS and MACROS. Never invent features, prices, dates, or policies.\n- Follow the refund policy exactly. Never promise a refund the policy does not allow.\n- Write the reply as the agent will send it after taking the actions the chosen macro describes.\n- Never ask the customer for their password.\n- Security reports: thank the reporter, say it has been escalated, point them to security@pharos.example, and do not confirm or discuss details.\n- Spam or vendor pitches: draft_reply must be an empty string.\n- Answer every question the customer asked. If something is not supported, say so plainly and offer the closest workaround from the docs.\n- Match the customer's emotion: acknowledge frustration specifically, without over-apologizing.\n- Plain language, short paragraphs, numbered steps when there are steps. Under 180 words. Sign off as \"Alex\" then \"Pharos Support\" on the next line.\n\nPriority guide:\n- urgent: Pharos down for many users, or a security issue\n- high: the business is losing bookings or money right now, can't access their account with clients waiting, double charges, repeated failures, or a frustrated customer threatening to leave\n- normal: a how-to question or a single problem with a workaround\n- low: feature requests, praise, spam\n\nReturn one JSON object with exactly these keys:\ncategory: one of billing, refund, cancellation, calendar_sync, reminders, booking_setup, payments, account_access, staff, data_privacy, outage, security, feature_request, presales, feedback, spam\npriority: one of low, normal, high, urgent\nsentiment: one of negative, neutral, positive\nchurn_risk: true or false\nmacro_id: the id of the macro your reply is based on\ntags: a list of 2 to 5 short snake_case tags\nsummary: one sentence telling the agent what the customer needs\ndraft_reply: the reply text\nneeds_human: true if a person must do something before replying (refund, identity check, escalation, investigation)\ncited_articles: list of help-center slugs you relied on\nconfidence: a number from 0 to 1", "chat": "You are the help-center assistant for Pharos, an online booking and reminders app for small service businesses.\n\nAnswer the customer's question using ONLY the HELP CENTER EXCERPTS below.\n- If the excerpts don't contain the answer, reply exactly: HANDOFF\n- Never guess at prices, policies, or features that aren't in the excerpts.\n- Be brief and friendly: 2 to 6 sentences, or short numbered steps.\n- Use the exact menu paths from the docs, like Settings > Billing.\n- End with one line: \"Source: <article title>\"."};
const SIZE_LIMITS = {
  chat: { maxInput: 8000, maxTokens: 400 },
  triage: { maxInput: 14000, maxTokens: 900 },
};

export default {
  async fetch(req, env, ctx) {
    const allowed = String(env.ALLOWED_ORIGINS || "")
      .split(",")
      .map(origin => origin.trim().replace(/\/$/, ""))
      .filter(Boolean);
    const origin = req.headers.get("Origin") || "";
    const okOrigin = allowed.includes(origin);
    const cors = {
      "Access-Control-Allow-Origin": okOrigin ? origin : (allowed[0] || "null"),
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
      "Vary": "Origin",
    };
    const json = (body, status = 200) => new Response(JSON.stringify(body), {
      status,
      headers: { ...cors, "Content-Type": "application/json" },
    });

    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const path = new URL(req.url).pathname.replace(/\/$/, "") || "/";
    const perVisitor = Number(env.PER_VISITOR_DAILY) || 10;
    const global = Number(env.GLOBAL_DAILY) || 40;
    const day = new Date().toISOString().slice(0, 10);
    const model = env.MODEL || DEFAULT_MODEL;

    if (path === "/health" || path === "/") {
      if (!env.AI || !env.LIMITS) {
        return json({
          ok: false,
          error: "not_configured",
          message: "Add the AI and LIMITS bindings in the Worker's settings.",
        }, 503);
      }
      const used = await count(env, `all:${day}`);
      return json({
        ok: true,
        model,
        remaining_today: Math.max(0, global - used),
        per_visitor_daily: perVisitor,
      });
    }
    if (req.method !== "POST" || (path !== "/chat" && path !== "/triage")) {
      return json({ error: "not_found" }, 404);
    }
    if (!okOrigin) {
      return json({
        error: "forbidden_origin",
        message: "This AI endpoint only serves the Pharos demo site.",
      }, 403);
    }
    if (!env.AI || !env.LIMITS) {
      return json({ error: "not_configured", message: "The demo's AI isn't set up yet." }, 503);
    }

    const kind = path.slice(1);
    let body;
    try {
      body = await req.json();
    } catch {
      return json({ error: "bad_request", message: "Send JSON with an `input` field." }, 400);
    }
    const input = typeof body?.input === "string" ? body.input.trim() : "";
    if (!input) return json({ error: "bad_request", message: "Missing input." }, 400);
    if (input.length > SIZE_LIMITS[kind].maxInput) {
      return json({ error: "too_long", message: "That request is too long for the demo." }, 413);
    }

    const visitor = await sha256(`${req.headers.get("CF-Connecting-IP") || "unknown"}|${day}`);
    const visitorKey = `v:${day}:${visitor.slice(0, 24)}`;
    const globalKey = `all:${day}`;
    const [visitorUsed, globalUsed] = await Promise.all([
      count(env, visitorKey),
      count(env, globalKey),
    ]);
    if (globalUsed >= global) {
      return json({
        error: "daily_limit",
        message: "The demo has used today's free AI answers. It resets at midnight UTC.",
      }, 429);
    }
    if (visitorUsed >= perVisitor) {
      return json({
        error: "visitor_limit",
        message: `You've used your ${perVisitor} AI answers for today. The docs-only mode still works.`,
      }, 429);
    }
    ctx.waitUntil(Promise.all([
      bump(env, visitorKey, visitorUsed),
      bump(env, globalKey, globalUsed),
    ]));

    try {
      const result = await env.AI.run(model, {
        messages: [
          { role: "system", content: PROMPTS[kind] },
          { role: "user", content: input },
        ],
        max_tokens: SIZE_LIMITS[kind].maxTokens,
        temperature: 0.2,
      });
      const response = result?.response;
      const text = typeof response === "string"
        ? response
        : response
          ? JSON.stringify(response)
          : "";
      return json({ text, model, remaining_today: Math.max(0, global - globalUsed - 1) });
    } catch (error) {
      console.error("Workers AI request failed:", error);
      return json({
        error: "model_error",
        message: "The AI model didn't answer. Try again in a moment.",
      }, 502);
    }
  },
};

async function count(env, key) {
  return Number(await env.LIMITS.get(key)) || 0;
}

async function bump(env, key, current) {
  await env.LIMITS.put(key, String(current + 1), { expirationTtl: 60 * 60 * 48 });
}

async function sha256(value) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, "0")).join("");
}
