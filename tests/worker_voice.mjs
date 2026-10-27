// Checks the Worker's draft cleanup (greeting, opening line, banned phrases, single sign-off) with a fake model.
// Run after `python build_demo.py`:   node tests/worker_voice.mjs
import w from "../worker/worker.js";
const store = {};
const env = { ALLOWED_ORIGINS: "https://x.io", LIMITS: { get: async k => store[k], put: async (k, v) => { store[k] = v; } },
  AI: { run: async () => ({ response: globalThis.NEXT }) } };
let fails = 0;
async function draft(text, from = "Hannah Ruiz", category = "refund") {
  globalThis.NEXT = JSON.stringify({ category, draft_reply: text });
  const r = await w.fetch(new Request("https://w/triage", { method: "POST", headers: { Origin: "https://x.io", "Content-Type": "application/json" },
    body: JSON.stringify({ input: `TICKET T\nFrom: ${from} <h@e.com>\nSubject: x\n\nbody` }) }), env, { waitUntil() {} });
  return JSON.parse((await r.json()).text).draft_reply;
}
function check(name, out, ok) { if (!ok) { fails++; console.log("FAIL", name, "\n" + out + "\n"); } else console.log("ok  ", name); }
const END = "\n\nBest,\nAlex\nPharos Support";
let o = await draft("Thank you for contacting Pharos. I've refunded it. Just reply here. Best,");
check("adds greeting, single sign-off", o, o.startsWith("Hi Hannah,\n\n") && o.endsWith("Just reply here." + END));
o = await draft("Thank you for contacting Pharos. Export under Settings > Data. Wishing you all the best,\n\nAlex\nPharos Support");
check("strips 'wishing you all the best'", o, o.endsWith("Settings > Data." + END));
o = await draft("Hi Hannah,\n\nThanks for reaching out! I understand your frustration. The fix is in Settings > Integrations.\n\nBest,\nAlex\nPharos Support");
check("removes banned phrases, adds opening", o, o === "Hi Hannah,\n\nThank you for contacting Pharos. The fix is in Settings > Integrations." + END);
o = await draft("", "Spam Bot", "spam");
check("spam stays empty", o, o === "");
console.log(fails ? `${fails} failed` : "all passed");
process.exit(fails ? 1 : 0);
