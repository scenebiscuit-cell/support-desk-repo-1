// Checks the Worker's admin password check, used by the agent desk's "Clear requests".
// Run after `python build_demo.py`:   node tests/worker_admin.mjs
import w from "../worker/worker.js";

const store = {};
const LIMITS = { get: async k => store[k], put: async (k, v) => { store[k] = v; } };
const env = { ALLOWED_ORIGINS: "https://x.io", LIMITS, ADMIN_PASSWORD: "test-admin-pw" };
const ctx = { waitUntil(p) { return p; } };
let fails = 0;
function check(name, ok, detail = "") { if (!ok) { fails++; console.log("FAIL", name, detail); } else console.log("ok  ", name); }

async function verify(password, { origin = "https://x.io", e = env, ip = "1.2.3.4", raw } = {}) {
  const r = await w.fetch(new Request("https://w/admin/verify", { method: "POST",
    headers: { "Content-Type": "application/json", Origin: origin, "CF-Connecting-IP": ip },
    body: raw ?? JSON.stringify({ password }) }), e, ctx);
  return { status: r.status, body: await r.json() };
}
const tries = () => Object.entries(store).filter(([k]) => k.startsWith("admintry:")).reduce((n, [, v]) => n + Number(v), 0);

let r = await verify("test-admin-pw");
check("the right password is accepted", r.status === 200 && r.body.ok === true, JSON.stringify(r));
check("a right password doesn't count as a try", tries() === 0);

r = await verify("nope");
check("a wrong password is refused", r.status === 401 && r.body.error === "bad_password", JSON.stringify(r));
check("a wrong password counts as a try", tries() === 1);
check("the reply never contains the password", !JSON.stringify(r.body).includes("test-admin-pw"));

r = await verify("");
check("an empty password is refused", r.status === 401);
r = await verify("test-admin-pw ");
check("a near miss is refused", r.status === 401);
r = await verify(undefined, { raw: "not json" });
check("a malformed request is refused", r.status === 400);

r = await verify("test-admin-pw", { origin: "https://evil.example" });
check("another site can't use the check", r.status === 403);

const bare = { ALLOWED_ORIGINS: "https://x.io", LIMITS };
r = await verify("anything", { e: bare });
check("the check is off when no password is configured", r.status === 404);

// After 8 wrong tries in a day, that visitor is locked out, even with the right password.
for (let i = 0; i < 8; i++) await verify("guess-" + i, { ip: "9.9.9.9" });
r = await verify("test-admin-pw", { ip: "9.9.9.9" });
check("too many wrong tries locks that visitor out for the day", r.status === 429, JSON.stringify(r));
r = await verify("test-admin-pw", { ip: "5.5.5.5" });
check("other visitors are not locked out", r.status === 200);

console.log(fails ? `${fails} failed` : "all passed");
process.exit(fails ? 1 : 0);
