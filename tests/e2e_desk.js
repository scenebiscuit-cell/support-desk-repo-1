const {chromium}=require('playwright');
// End-to-end check of the customer portal <-> agent desk loop. Needs Playwright (npm i -D playwright).
// Serve the repo root first:  python -m http.server 8000   then:  node tests/e2e_desk.js
const B=process.env.PHAROS_URL || 'http://localhost:8000/', O=process.argv[2] || require('os').tmpdir();
const ok=(c,m)=>{console.log((c?'ok   ':'FAIL ')+m); if(!c) process.exitCode=1;};
(async()=>{const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:1280,height:900},colorScheme:'light',reducedMotion:'reduce'});
const errs=[]; await ctx.route('**/*workers.dev/**', r=>r.abort()); await ctx.route('**/localhost:11434/**', r=>r.abort());
const desk=await ctx.newPage(), portal=await ctx.newPage();
for (const p of [desk,portal]) p.on('pageerror',e=>errs.push(String(e)));
await desk.goto(B+'#triage'); await desk.waitForTimeout(600);
ok(await desk.$eval('#tab-triage',e=>e.textContent)==='Agent desk','tab renamed');
await portal.goto(B+'portal/'); await portal.waitForTimeout(500);
// handoff -> contact support
await portal.fill('#question','Do you sell gift cards?'); await portal.press('#question','Enter'); await portal.waitForTimeout(700);
const cta=await portal.$('.msg-cta'); ok(!!cta,'handoff offers Contact support');
await cta.click(); await portal.waitForTimeout(400);
ok(!(await portal.$eval('#view-new',e=>e.hidden)),'form view opens');
ok((await portal.inputValue('#rf-subj')).includes('gift cards'),'subject prefilled from question');
// deflection suggestions
await portal.fill('#rf-subj','Slack stopped posting task updates'); await portal.waitForTimeout(500);
ok(!(await portal.$eval('#rf-sugs',e=>e.hidden)),'article suggestions appear while typing');
await portal.selectOption('#rf-type','Integrations'); await portal.fill('#rf-name','Jamie Rivera'); await portal.fill('#rf-email','jamie@rivera.example');
await portal.selectOption('#rf-plan','Business');
await portal.fill('#rf-body','Our #client-work Slack channel stopped getting task updates yesterday. Nothing changed on our end.');
await portal.click('#req-form button[type=submit]'); await portal.waitForTimeout(500);
const done=await portal.textContent('#req-done'); ok(done.includes('PH-101'),'request PH-101 created'); ok(done.includes('4 business hours'),'SLA promise shown');
// desk sees it live
await desk.waitForTimeout(600);
ok((await desk.textContent('#set-seg [data-set="live"]')).includes('1'),'desk live count updates via storage event');
await desk.click('#set-seg [data-set="live"]'); await desk.waitForTimeout(400);
ok((await desk.textContent('#detail')).includes('Slack stopped posting task updates'),'issue view opens the request');
ok((await desk.textContent('.sla-box')).includes('left'),'SLA countdown shown: '+(await desk.textContent('.sla-box b')));
ok((await desk.inputValue('#cmp')).length>40,'reply prefilled with draft');
await desk.screenshot({path:O+'/agent-desk.png'});
// internal note
await desk.click('.ctabs [data-mode="note"]'); await desk.fill('#cmp','Checked Slack app logs: token revoked on their side. Ask them to reconnect.'); await desk.click('[data-note]'); await desk.waitForTimeout(300);
ok((await desk.textContent('.timeline')).includes('token revoked'),'internal note in agent timeline');
// share KB + send
const share=await desk.$('[data-share]'); if (share){ await share.click(); await desk.waitForTimeout(200); {const v=await desk.inputValue('#cmp'); ok(v.includes('This article walks through it') && v.indexOf('This article') < v.lastIndexOf('Alex'),'KB article shared above the sign-off');} }
let send=await desk.$('[data-send]'); await send.click(); await desk.waitForTimeout(200);
if (await desk.$('[data-send][data-sure="1"]')) { await desk.click('[data-send]'); }
await desk.waitForTimeout(400);
// portal shows reply
await portal.goto(B+'portal/#requests'); await portal.waitForTimeout(500);
ok((await portal.textContent('#req-list')).includes('Reply from support'),'portal shows reply status');
ok((await portal.$eval('#req-count',e=>e.hidden))===false,'nav badge shows waiting reply');
await portal.click('.rq'); await portal.waitForTimeout(400);
const th=await portal.textContent('.thread'); ok(th.includes('Pharos Support'),'agent reply visible to customer'); ok(!th.includes('token revoked'),'internal note hidden from customer');
await portal.screenshot({path:O+'/portal-request.png', fullPage:true});
await portal.fill('#rr-text','Reconnected it and updates are flowing again. Thanks!'); await portal.click('#req-reply button[type=submit]'); await portal.waitForTimeout(500);
// desk: back to waiting for support
await desk.click('#set-seg [data-set="live"]'); await desk.waitForTimeout(400);
ok((await desk.textContent('#queue')).includes('Waiting for support'),'customer reply reopens ticket for support');
// simulate email
await desk.click('#sim-email'); await desk.waitForTimeout(400);
ok((await desk.textContent('#detail')).includes('PH-102') && (await desk.textContent('#detail')).includes('via email'),'simulated email becomes PH-102');
// status change to resolved
await desk.selectOption('#st-sel','resolved'); await desk.waitForTimeout(300);
ok((await desk.textContent('.timeline')).includes('Status changed to Resolved'),'status change logged');
// sample set still works + undo toast
await desk.click('#set-seg [data-set="sample"]'); await desk.waitForTimeout(300);
ok((await desk.$$('.qitem')).length===20,'sample queue intact');
// phone layout
const ph=await ctx.newPage(); ph.on('pageerror',e=>errs.push(String(e))); await ph.setViewportSize({width:390,height:844});
await ph.goto(B+'#triage'); await ph.waitForTimeout(500); await ph.click('#set-seg [data-set="live"]').catch(()=>{}); await ph.waitForTimeout(300);
ok(await ph.evaluate(()=>document.documentElement.scrollWidth<=390),'no sideways scroll on phone (desk)');
await ph.goto(B+'portal/#new'); await ph.waitForTimeout(400);
ok(await ph.evaluate(()=>document.documentElement.scrollWidth<=390),'no sideways scroll on phone (portal form)');
await ph.screenshot({path:O+'/phone-portal-form.png'});
ok(errs.length===0,'no page errors '+JSON.stringify(errs));
await b.close();})();
