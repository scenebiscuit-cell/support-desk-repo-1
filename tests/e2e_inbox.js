const {chromium}=require('playwright');
// End-to-end check of the real-email inbox on the agent desk, with a stand-in for the Worker.
// Needs Playwright (npm i -D playwright). Serve the repo root first:  python -m http.server 8000   then:  node tests/e2e_inbox.js
const B=process.env.PHAROS_URL || 'http://localhost:8000/', O=process.argv[2] || require('os').tmpdir();
const ok=(c,m)=>{console.log((c?'ok   ':'FAIL ')+m); if(!c) process.exitCode=1;};
const KEY='test-inbox-key';
(async()=>{const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:1280,height:900},colorScheme:'light',reducedMotion:'reduce'});
const errs=[], calls=[]; let mail=[], status=200;
const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'Content-Type, X-Inbox-Key','Access-Control-Allow-Methods':'GET, POST, OPTIONS'};
await ctx.route('**/localhost:11434/**', r=>r.abort());
await ctx.route('**/*workers.dev/**', r=>{ const q=r.request(), u=new URL(q.url());
  if (q.method()==='OPTIONS') return r.fulfill({status:204,headers:cors});
  if (u.pathname==='/health') return r.fulfill({status:200,headers:cors,contentType:'application/json',body:JSON.stringify({ok:true,model:'test',remaining_today:40,per_visitor_daily:10})});
  if (u.pathname==='/inbox'){ calls.push({key:q.headers()['x-inbox-key'],since:Number(u.searchParams.get('since'))});
    if (status!==200) return r.fulfill({status,headers:cors,contentType:'application/json',body:'{"error":"bad_key"}'});
    const since=Number(u.searchParams.get('since'))||0;
    return r.fulfill({status:200,headers:cors,contentType:'application/json',body:JSON.stringify({ok:true,address:'support@demo.example',emails:mail.filter(e=>Number(e.id.split(':')[0])>since)})}); }
  return r.abort(); });

// 1. A visitor without the key never asks for the inbox.
const visitor=await ctx.newPage(); visitor.on('pageerror',e=>errs.push(String(e)));
await visitor.goto(B+'#triage'); await visitor.waitForTimeout(1200);
ok(calls.length===0,'a desk without the key never checks the inbox');
await visitor.click('#set-seg [data-set="live"]'); await visitor.waitForTimeout(200);
ok(!(await visitor.$('.inbox-on')),'no "Real inbox connected" label without the key');
await visitor.close();

// 2. Connect with the key: it leaves the address bar, the desk opens on Live requests, and polling starts.
const desk=await ctx.newPage(); desk.on('pageerror',e=>errs.push(String(e)));
await desk.goto(B+'#inbox='+KEY); await desk.waitForTimeout(1500);
ok(!desk.url().includes(KEY) && desk.url().endsWith('#triage'),'the key is removed from the address bar');
ok(calls.length>0 && calls.every(c=>c.key===KEY),'the desk sends the key when it checks the inbox');
ok(await desk.$eval('#set-seg [data-set="live"]',e=>e.getAttribute('aria-pressed'))==='true','desk opens on Live requests');
ok((await desk.textContent('.inbox-on')).includes('support@demo.example'),'label shows the real inbox address');

// 3. An email arrives: it becomes a live request, triaged by the same rules.
const at=Date.now()+1000;
mail=[{id:at+':abcd1234',at:new Date(at).toISOString(),from:{name:'Nick <b>Tester</b>',email:'nick@example.com'},subject:"Login I don't recognize",
  body:"I got an email about a login from another country last night. That wasn't me. What should I do?"}];
await desk.waitForSelector('.qitem',{timeout:9000});
const bold=await desk.evaluate(()=>[...document.querySelectorAll('#detail b, #queue b, #toast-root b')].some(e=>e.textContent.trim()==='Tester'));
const toastText=await desk.textContent('#toast-root');
const row=await desk.$('.qitem');
ok(!!row && (await row.textContent()).includes("Login I don't recognize"),'the email appears in Live requests');
ok((await row.textContent()).includes('via email'),'request is labelled as email');
ok(await row.getAttribute('data-p')==='urgent' && (await row.textContent()).toLowerCase().includes('security'),'triaged as security, urgent');
const detail=await desk.textContent('#detail');
ok(detail.includes('Email to support@demo.example became request PH-101'),'timeline records the email arriving');
ok(detail.includes("That wasn't me."),'the message body is shown');
ok(!bold && toastText.includes('Nick <b>Tester</b>'),'sender name is shown as text, not HTML');
await desk.screenshot({path:O+'/inbox-desk.png'});

// 4. The same email is not imported twice, and `since` moves forward.
await desk.waitForTimeout(5500);
ok((await desk.$$('.qitem')).length===1,'no duplicate after the next check');
ok(calls.at(-1).since>=at,'later checks only ask for newer emails');
await desk.reload(); await desk.waitForTimeout(1500);
await desk.click('#set-seg [data-set="live"]'); await desk.waitForTimeout(300);
ok((await desk.$$('.qitem')).length===1,'still one request after a reload');

// 5. A rejected key disconnects cleanly.
status=401; await desk.waitForTimeout(6000);
ok(!(await desk.$('.inbox-on')),'a rejected key disconnects the inbox');
const n=calls.length; await desk.waitForTimeout(5500);
ok(calls.length===n,'and the desk stops checking');
ok((await desk.$$('.qitem')).length===1,'requests already received are kept');

ok(errs.length===0,'no page errors'+(errs.length?': '+errs.join(' | '):''));
await b.close();})();
