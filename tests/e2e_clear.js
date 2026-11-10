const {chromium}=require('playwright');
// End-to-end check of "Clear requests" on the agent desk, including the admin password step, with a
// stand-in for the Worker. Needs Playwright (npm i -D playwright).
// Serve the repo root first:  python -m http.server 8000   then:  node tests/e2e_clear.js
const B=process.env.PHAROS_URL || 'http://localhost:8000/';
const ok=(c,m)=>{console.log((c?'ok   ':'FAIL ')+m); if(!c) process.exitCode=1;};
(async()=>{const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:1280,height:900},colorScheme:'light',reducedMotion:'reduce'});
const errs=[], sent=[]; const PW='test-admin-pw'; let adminStatus=0;   // 0 = judge the password; otherwise force this status
const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'Content-Type, X-Inbox-Key','Access-Control-Allow-Methods':'GET, POST, OPTIONS'};
await ctx.route('**/localhost:11434/**', r=>r.abort());
await ctx.route('**/*workers.dev/**', r=>{ const q=r.request(), u=new URL(q.url());
  if (q.method()==='OPTIONS') return r.fulfill({status:204,headers:cors});
  if (u.pathname==='/admin/verify'){ const pw=(JSON.parse(q.postData()||'{}')).password; sent.push(pw);
    const status=adminStatus || (pw===PW?200:401);
    return r.fulfill({status,headers:cors,contentType:'application/json',body:JSON.stringify(status===200?{ok:true}:{error:'x'})}); }
  return r.abort(); });
const desk=await ctx.newPage(), portal=await ctx.newPage();
for (const p of [desk,portal]) p.on('pageerror',e=>errs.push(String(e)));
async function raise(subject, body){
  await portal.goto(B+'portal/#new'); await portal.waitForTimeout(400);
  await portal.fill('#rf-name','Jamie Rivera'); await portal.fill('#rf-email','jamie@rivera.example');
  await portal.fill('#rf-subj',subject); await portal.fill('#rf-body',body);
  await portal.click('#req-form button[type="submit"]'); await portal.waitForTimeout(500);
}
await desk.goto(B+'#triage'); await desk.waitForTimeout(600);
await desk.click('#set-seg [data-set="live"]'); await desk.waitForTimeout(200);
ok(!(await desk.$('#clear-req')),'no Clear requests control while the queue is empty');

// Two requests: one from the portal (a refund), one simulated email.
await raise('I was charged twice this month','We were billed twice for the Team plan. Please refund the extra charge.');
await desk.waitForTimeout(500);
await desk.click('#sim-email'); await desk.waitForTimeout(400);
ok((await desk.$$('.qitem')).length===2,'two live requests before clearing');
const firstRow=await desk.textContent('.qitem[data-id="PH-101"]');
ok(firstRow.toLowerCase().includes('refund'),'PH-101 starts as a refund request');

// Asking first, and Cancel keeps everything.
await desk.click('#clear-req'); await desk.waitForTimeout(150);
ok((await desk.textContent('.clear-ask')).includes('Clear all 2 live requests'),'clicking asks for confirmation with the count');
ok(await desk.$eval('#clear-pw',e=>e.type==='password' && document.activeElement===e),'it asks for the admin password, with the box focused');
ok((await desk.$$('.qitem')).length===2,'nothing is cleared until confirmed');
await desk.click('#clear-no'); await desk.waitForTimeout(150);
ok(!!(await desk.$('#clear-req')) && (await desk.$$('.qitem')).length===2,'Cancel keeps the requests');

// No password, then a wrong password: nothing is cleared.
await desk.click('#clear-req'); await desk.click('#clear-yes'); await desk.waitForTimeout(300);
ok(sent.length===0 && (await desk.$$('.qitem')).length===2,'an empty password is not sent and clears nothing');
await desk.fill('#clear-pw','wrong-guess'); await desk.press('#clear-pw','Enter'); await desk.waitForTimeout(500);
ok(sent.at(-1)==='wrong-guess' && (await desk.textContent('#clear-msg')).includes("isn't right"),'a wrong password shows a message');
ok((await desk.$$('.qitem')).length===2 && !!(await desk.$('#clear-pw')),'a wrong password clears nothing and keeps the form open');
adminStatus=429; await desk.fill('#clear-pw',PW); await desk.click('#clear-yes'); await desk.waitForTimeout(500);
ok((await desk.textContent('#clear-msg')).includes('Too many tries') && (await desk.$$('.qitem')).length===2,'a lockout shows a message and clears nothing');
adminStatus=0;
// Cancel forgets what was typed.
await desk.click('#clear-no'); await desk.click('#clear-req'); await desk.waitForTimeout(150);
ok(await desk.inputValue('#clear-pw')==='' && (await desk.textContent('#clear-msg'))==='','Cancel forgets the typed password and the message');

// The right password: the queue empties on the desk and in the portal.
await desk.fill('#clear-pw',PW); await desk.click('#clear-yes'); await desk.waitForTimeout(500);
ok(!(await desk.content()).includes(PW),'the password is not left anywhere in the page');
ok((await desk.$$('.qitem')).length===0 && !!(await desk.$('.qempty')),'the live queue is empty after confirming');
ok(!(await desk.$('#clear-req')),'the control hides again');
ok(!(await desk.textContent('#set-seg [data-set="live"]')).match(/\d/),'the Live requests count is gone');
ok((await desk.textContent('#toast-root')).includes('Cleared 2 live requests'),'a message confirms what was cleared');
await portal.goto(B+'portal/#requests'); await portal.waitForTimeout(400);
ok((await portal.textContent('#req-list')).includes("haven't raised any requests"),'the portal shows no requests either');

// Numbering restarts, and the new PH-101 gets its own triage, not the old one's.
await raise("Login I don't recognize","I got an email about a login from another country last night. That wasn't me.");
await desk.waitForTimeout(600);
const rows=await desk.$$('.qitem');
const newRow=rows.length?await rows[0].textContent():'';
ok(rows.length===1 && newRow.includes('PH-101'),'the next request is PH-101 again');
ok(newRow.toLowerCase().includes('security') && !newRow.toLowerCase().includes('refund') && await rows[0].getAttribute('data-p')==='urgent','the new PH-101 is triaged fresh (security, urgent)');
await rows[0].click(); await desk.waitForTimeout(300);
ok((await desk.textContent('#detail')).includes("That wasn't me."),'its detail shows the new message');
// Sample tickets are untouched.
await desk.click('#set-seg [data-set="sample"]'); await desk.waitForTimeout(200);
ok((await desk.$$('.qitem')).length===20,'sample tickets are untouched');

ok(errs.length===0,'no page errors'+(errs.length?': '+errs.join(' | '):''));
await b.close();})();
