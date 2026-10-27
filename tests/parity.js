// Checks that the page's JavaScript triage gives the same answers as the Python rules engine.
// Run after `python build_demo.py`:   node tests/parity.js
const fs = require("fs"), path = require("path");
const html = fs.readFileSync(path.join(__dirname, "..", "demo", "index.html"), "utf8");
let code = [...html.matchAll(/<script(?: [^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]).sort((a, b) => b.length - a.length)[0];
const a = code.indexOf("/* ---------- header: wireframe sea");          // drop the canvas animation; it needs a real browser
if (a >= 0) code = code.slice(0, a) + code.slice(code.indexOf("})();", a) + 5);
const mk = () => new Proxy(function () {}, { get: (t, k) => k === "innerHTML" || k === "value" || k === "textContent" ? "" : k === "dataset" ? {} : k === "hash" ? "" : mk(), set: () => true, apply: () => mk() });
const G = {
  document: { documentElement: mk(), hidden: false, querySelector: () => mk(), querySelectorAll: () => [], createElement: () => mk(), getElementById: () => mk(), addEventListener() {}, body: mk(), activeElement: null },
  navigator: { platform: "Win" }, innerWidth: 1000, location: { hash: "" }, fetch: () => Promise.reject(new TypeError("offline")),
  AbortController: class { abort() {} get signal() { return {}; } }, history: { replaceState() {} }, window: {},
  matchMedia: () => ({ matches: true, addEventListener() {} }), ResizeObserver: class { observe() {} }, MutationObserver: class { observe() {} },
  IntersectionObserver: class { observe() {} }, getComputedStyle: () => ({ getPropertyValue: () => "" }), requestAnimationFrame: () => 0,
  devicePixelRatio: 1, addEventListener() {}, scrollTo() {}, localStorage: { getItem() { return null; }, setItem() {} },
};
for (const [k, v] of Object.entries(G)) Object.defineProperty(globalThis, k, { value: v, configurable: true, writable: true });
const m = { exports: {} };
new Function("module", "require", code + "\n;module.exports={search,rulesTriage,D};")(m, require);
const { rulesTriage, D } = m.exports;
let mism = 0;
for (const set of ["sample", "unseen"]) for (const t of D.sets[set].tickets) {
  const js = rulesTriage(t), py = D.sets[set].results.find(r => r.ticket_id === t.id);
  for (const k of ["category", "priority", "sentiment", "churn_risk", "macro_id", "needs_human", "draft_reply"])
    if (JSON.stringify(js[k]) !== JSON.stringify(py[k])) { mism++; console.log(t.id, k, js[k], "vs", py[k]); }
  if (js.cited_articles.join() !== py.cited_articles.join()) { mism++; console.log(t.id, "cited", js.cited_articles, py.cited_articles); }
}
console.log("mismatches:", mism);
process.exit(mism ? 1 : 0);
