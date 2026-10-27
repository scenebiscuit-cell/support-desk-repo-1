/* ---------- shared ticket store ----------
   The customer portal (/portal/) and the agent desk (/) are on the same site, so they share requests through
   this browser's localStorage. build_demo.py inlines this file into both pages; edit it here, not in the pages.
   Each visitor gets a private sandbox: nothing leaves the browser. */
const DESK_KEY = "pharos-desk-v1";
const STATUS = {
  open: "Waiting for support", progress: "In progress", customer: "Waiting for customer",
  resolved: "Resolved", closed: "Closed",
};
const REQUEST_TYPES = ["Billing and refunds", "Technical problem", "Account and login", "Integrations", "Feature request", "Something else"];
const Desk = (() => {
  const blank = () => ({ v: 1, seq: 100, requests: [], state: {}, deflected: 0, profile: null });
  let mem = blank();
  function load() {
    try {
      const v = JSON.parse(localStorage.getItem(DESK_KEY) || "null");
      mem = v && Array.isArray(v.requests) && v.state ? { ...blank(), ...v } : blank();
    } catch (e) { /* storage blocked: keep working in memory */ }
    return mem;
  }
  function save() { try { localStorage.setItem(DESK_KEY, JSON.stringify(mem)); } catch (e) {} }
  load();
  return {
    get data() { return mem; },
    reload: load,
    update(fn) { load(); fn(mem); save(); return mem; },
    nextKey(m) { m.seq += 1; return `PH-${m.seq}`; },
    // A ticket's conversation and status. Sample tickets start as a single customer message.
    stateOf(t) {
      return mem.state[t.id] || { status: "open", assignee: null, first_response_at: null,
        thread: [{ who: "customer", name: t.customer?.name || "Customer", text: t.body, at: t.created_at }] };
    },
    ensure(m, t) {
      if (!m.state[t.id]) m.state[t.id] = JSON.parse(JSON.stringify(this.stateOf(t)));
      return m.state[t.id];
    },
  };
})();
function ago(iso) {
  const ms = Date.now() - new Date(iso).getTime();
  if (!isFinite(ms)) return "";
  const m = Math.round(ms / 60000);
  if (m < 1) return "just now";
  if (m < 60) return `${m} min ago`;
  const h = Math.round(m / 60);
  if (h < 24) return `${h} h ago`;
  return new Date(iso).toLocaleDateString(undefined, { month: "short", day: "numeric" });
}
