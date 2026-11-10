// Checks the Worker's real-email path with fake messages: the allowlist, the MIME reader, storage, and /inbox.
// Run after `python build_demo.py`:   node tests/worker_email.mjs
import w from "../worker/worker.js";

const store = {};
const LIMITS = {
  get: async k => store[k],
  put: async (k, v) => { store[k] = v; },
};
const env = { ALLOWED_ORIGINS: "https://x.io", LIMITS, EMAIL_ALLOWLIST: "nick@example.com, Other@Example.com",
  INBOX_KEY: "test-key-123", INBOX_ADDRESS: "support@demo.example" };
const ctx = { waitUntil(p) { return p; } };
let fails = 0;
function check(name, ok, detail = "") { if (!ok) { fails++; console.log("FAIL", name, detail); } else console.log("ok  ", name); }

function message(from, raw, extraHeaders = {}) {
  const bytes = new TextEncoder().encode(raw.replace(/\n/g, "\r\n"));
  const m = { from, to: "support@demo.example", rawSize: bytes.length, rejected: null,
    headers: new Headers(extraHeaders), raw: new Response(bytes).body, setReject(reason) { m.rejected = reason; } };
  return m;
}
const mails = () => JSON.parse(store["mail:recent"] || "[]");
async function inbox(key, since = 0, origin = "https://x.io") {
  const headers = { Origin: origin }; if (key != null) headers["X-Inbox-Key"] = key;
  const r = await w.fetch(new Request(`https://w/inbox?since=${since}`, { headers }), env, ctx);
  return { status: r.status, body: await r.json() };
}

// 1. A Gmail-style email: multipart/alternative, quoted-printable plain text, an HTML twin, a quoted reply and a signature.
const gmail = `From: Nick Example <nick@example.com>
To: support@demo.example
Subject: Login I don't recognize
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="000000000000abc123"

--000000000000abc123
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

I got an email about a login from another country last night. That wasn=E2=80=99t me.
What should I do? This line is long enough that Gmail wraps it with a soft =
line break.

--
Nick

On Mon, Nov 9, 2026 at 9:00 AM Support <support@demo.example> wrote:
> Earlier message that should not be included.

--000000000000abc123
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

<div>I got an email about a login from another country last night.</div>

--000000000000abc123--
`;
let m = message("nick@example.com", gmail);
await w.email(m, env, ctx);
let got = mails();
check("allowlisted sender is accepted", !m.rejected && got.length === 1, m.rejected || "");
check("subject and sender are read", got[0]?.subject === "Login I don't recognize" && got[0]?.from.name === "Nick Example" && got[0]?.from.email === "nick@example.com", JSON.stringify(got[0]));
check("plain text is decoded (quoted-printable, UTF-8, soft breaks)", got[0]?.body.includes("That wasn’t me.") && got[0]?.body.includes("soft line break."), got[0]?.body);
check("signature and quoted reply are dropped", !/Earlier message|wrote:|^Nick$/m.test(got[0]?.body || "x"), got[0]?.body);

// 2. A stranger is rejected and nothing is stored.
m = message("stranger@elsewhere.com", gmail.replace("nick@example.com", "stranger@elsewhere.com"));
await w.email(m, env, ctx);
check("unknown sender is rejected", !!m.rejected && mails().length === 1);

// 3. A forged header: allowed envelope sender, but the From header names someone else.
m = message("nick@example.com", gmail.replace("Nick Example <nick@example.com>", "Boss <ceo@elsewhere.com>"));
await w.email(m, env, ctx);
check("mismatched From header is rejected", !!m.rejected && mails().length === 1);

// 4. Mail that failed the sending domain's checks is rejected.
m = message("nick@example.com", gmail, { "Authentication-Results": "mx.cloudflare.net; dmarc=fail header.from=example.com" });
await w.email(m, env, ctx);
check("DMARC failure is rejected", !!m.rejected && mails().length === 1);

// 5. Base64 body, encoded subject, allowlist entry in different capitals.
const b64 = s => Buffer.from(s, "utf8").toString("base64");
const encoded = `From: =?UTF-8?B?${b64("Zoë Other")}?= <other@example.com>
Subject: =?UTF-8?Q?Charged_twice_=E2=80=93_refund=3F?=
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: base64

${b64("We were charged twice this month. Can you refund one?\n\n> old quote")}
`;
m = message("other@example.com", encoded);
await new Promise(r => setTimeout(r, 2));
await w.email(m, env, ctx);
got = mails();
check("base64 body and encoded headers are decoded", !m.rejected && got[1]?.subject === "Charged twice – refund?" && got[1]?.from.name === "Zoë Other" && got[1]?.body === "We were charged twice this month. Can you refund one?", JSON.stringify(got[1]));

// 6. An HTML-only email falls back to readable text.
const html = `From: nick@example.com
Subject: HTML only
Content-Type: text/html; charset=utf-8

<html><body><p>Our Zapier zap stopped working.</p><p>It says &quot;authentication failed&quot;.</p></body></html>
`;
m = message("nick@example.com", html);
await new Promise(r => setTimeout(r, 2));
await w.email(m, env, ctx);
got = mails();
check("HTML-only email becomes text", !m.rejected && got[2]?.body === 'Our Zapier zap stopped working.\nIt says "authentication failed".', JSON.stringify(got[2]?.body));

// 7. Oversized mail is rejected.
m = message("nick@example.com", gmail); m.rawSize = 300 * 1024;
await w.email(m, env, ctx);
check("oversized email is rejected", !!m.rejected && mails().length === 3);

// 8. /inbox: key required, origin locked, `since` filters.
let r = await inbox(null);
check("/inbox without a key is refused", r.status === 401);
r = await inbox("wrong-key");
check("/inbox with a wrong key is refused", r.status === 401);
r = await inbox("test-key-123", 0, "https://evil.example");
check("/inbox from another site is refused", r.status === 403);
r = await inbox("test-key-123");
check("/inbox returns the stored emails in order", r.status === 200 && r.body.emails.length === 3 && r.body.emails[0].subject === "Login I don't recognize" && r.body.address === "support@demo.example", JSON.stringify(r.body).slice(0, 200));
const firstAt = Number(r.body.emails[0].id.split(":")[0]);
r = await inbox("test-key-123", firstAt);
check("/inbox?since= skips emails already seen", r.status === 200 && r.body.emails.length === 2);

// 9. With no INBOX_KEY configured, the endpoint doesn't exist and email is refused without an allowlist.
const bare = { ALLOWED_ORIGINS: "https://x.io", LIMITS };
const off = await w.fetch(new Request("https://w/inbox", { headers: { Origin: "https://x.io" } }), bare, ctx);
check("/inbox is off when no key is configured", off.status === 404);
m = message("nick@example.com", gmail);
await w.email(m, bare, ctx);
check("email is refused when no allowlist is configured", !!m.rejected);

// 10. Daily cap.
store[`mailcount:${new Date().toISOString().slice(0, 10)}`] = "40";
m = message("nick@example.com", gmail);
await w.email(m, env, ctx);
check("daily cap is enforced", !!m.rejected && mails().length === 3);

console.log(fails ? `${fails} failed` : "all passed");
process.exit(fails ? 1 : 0);
