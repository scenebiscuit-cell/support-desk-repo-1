# Selling it: listing copy, talking points, next steps

Starting drafts. Edit the voice to sound like you, and set prices you're comfortable defending.

## Upwork / Contra service listing

**Title:** I'll set up and tune AI support in the helpdesk you already use, measured on your real tickets

**Overview:**
Help desks like Freshdesk and Zendesk now sell AI, but it only answers as well as the help articles and rules behind it. Most small teams switch it on, watch it give vague or wrong answers, and go back to doing everything by hand. I set it up properly, inside the tool you already pay for:

- **A help-center chatbot** that answers only from your docs, links the article, and hands off to your team when it isn't sure. No made-up answers.
- **Ticket triage** that tags every ticket by topic and urgency, flags customers at risk of leaving, and drafts an on-policy reply your team reviews and sends.
- **A macro library** of consistent replies for your most common requests, imported into your helpdesk.

I come from enterprise technical support and regulatory compliance, so I build for accuracy and policy first: refunds, account access, and security issues always stay with a person. I measure accuracy against your real past tickets before anything goes live.

**See it working:** [Live demo](https://scenebiscuit-cell.github.io/support-desk-repo-1/) · [Customer help portal](https://scenebiscuit-cell.github.io/support-desk-repo-1/portal/) · [Code and results](https://github.com/scenebiscuit-cell/support-desk-repo-1)  
**Contact:** Nick Lax · nlaxatx@gmail.com

### Why work with me

| | Turning on the AI add-on yourself | A setup-only gig | Working with me |
|---|---|---|---|
| Help articles and replies | Used as they are | Usually used as they are | Rewritten where the AI needs better answers |
| Accuracy | Unknown until customers complain | Rarely measured | Scored on your own past tickets, before and after |
| Risky cases (refunds, security, account access) | Depends on default settings | Depends on the setup | Always routed to a person, with a safety net for the high-risk ones |
| After launch | You maintain it | Handoff and done | Optional monthly upkeep |

- **Proof before go-live.** You see a before-and-after accuracy score on your own tickets, not a promise.
- **The content gets fixed, not just the settings.** Most bad AI answers come from thin or outdated help articles, so that's where I start.
- **No new software and no lock-in.** Everything lives in the helpdesk you already use (Freshdesk, Zendesk, Help Scout, or a shared Gmail inbox), and you own all of it.
- **Your AI fees go further.** Help desks bill AI by the conversation or resolution, so answers that actually solve the problem are worth paying for.
- **Private option.** If customer data can't go to a cloud AI provider, triage can run on your own computer instead. This matters for regulated businesses, such as cannabis retailers and other compliance-heavy services.

### Packages (starting points, set prices you're comfortable defending)

| Package | What's included | Typical timeline |
|---|---|---|
| Audit | Review your help articles and 50–100 past tickets: the top questions, the gaps, and how often the current setup gets it right. You get a short report and a plan. | About 1 week |
| Setup | Audit + rewrite the top help articles, build the macro library, configure triage and the AI bot in your helpdesk, set the handoff rules, and test on your past tickets with a before-and-after score. Includes a walkthrough call with your team. | 2–3 weeks |
| Monthly upkeep | Monthly accuracy check, new macros, and article updates as your product changes. | Ongoing, cancel anytime |

**Questions to ask buyers:** Which helpdesk do you use? How many tickets a week? Where do your help articles live? Have you tried the built-in AI yet, and what went wrong? Can customer data go to a cloud AI provider, or does it need to stay local?

## Interview talking points (CS / support roles)

- "I built AI ticket deflection for a demo SaaS: a docs-grounded chatbot that cites sources and hands off when it's not confident."
- "I built triage that sorts by real business impact (outages and security first, then teams that are blocked or losing money) and flags churn risk from tone and intent."
- "I measured it. My keyword baseline scored 100% on the 20 tickets I wrote it against but 78% on 36 unseen ones. A local AI model raised that to 83%, and it understood intent the rules missed, like a seat overcharge being a refund request. But both missed the same two suspicious-login reports, so I added a deterministic security safety net in front of both: with it, the AI reaches 89%, and that class of incident can't be misrouted again. That's how I'd evaluate an AI support tool before trusting it with customers."
- "I modeled the workflow on Jira Service Management: a customer raises a request in the help portal (with article suggestions to deflect it), it lands in the agent queue already triaged with an SLA clock, and the agent replies or adds internal notes. The customer sees the reply in their portal."
- "I designed it so AI drafts and people decide: refunds, identity verification, and security reports always route to a human."
- "Macros encode policy. Each one sets tags, priority, and status, and carries an internal note, so new agents give the same answer veterans do."

## Next steps (suggested order)

1. Record the Loom walkthrough and add the link to the README. Buyers on Upwork respond to video.
2. Post the listing above on Upwork and Contra, with the live demo, help portal, and GitHub links.
3. Add the project to your resume and LinkedIn using one of the talking points above.
4. Offer the Audit to one or two small businesses at a low intro price in exchange for a testimonial, then use their before-and-after score as a case study.
5. Optional: push the AI accuracy past 90% honestly (see `.github/copilot-instructions.md`).
