# Selling it: listing copy, talking points, next steps

Starting drafts. Edit the voice to sound like you, and set prices you're comfortable defending.

## Upwork / Contra service listing

**Title:** I'll set up AI ticket triage, a help-center chatbot, and support macros for your small business

**Overview:**
Small support teams lose hours every week sorting the inbox, rewriting the same replies, and answering questions that are already in the help center. I set up three things that fix that:

- **A help-center chatbot** that answers only from your docs, links the article, and hands off to your team when it isn't sure. No made-up answers.
- **Ticket triage** that tags every ticket by topic and urgency, flags customers at risk of leaving, and drafts an on-policy reply your team reviews and sends.
- **A macro library** of consistent replies for your most common requests, ready to import into your helpdesk.

I come from enterprise technical support and regulatory compliance, so I build for accuracy and policy first: refunds, account access, and security issues always stay with a person. I measure accuracy against your real past tickets before anything goes live.

It can run on the AI provider of your choice, or entirely on your own computer if your customer data can't leave the building.

**See a live demo:** [link to your published demo page]  
**Contact:** Nick Lax · nlaxatx@gmail.com

**Packages (starting points, adjust to your market):**

| Package | What's included |
|---|---|
| Starter | Macro library: up to 20 replies written from your docs and past tickets, CSV for your helpdesk |
| Standard | Starter + ticket triage tuned on 50 of your past tickets, with an accuracy report |
| Premium | Standard + help-center chatbot on your docs, handoff to your inbox, 2 weeks of tuning |

**Questions to ask buyers:** Which helpdesk do you use? How many tickets a week? Where do your help articles live? Can customer data go to a cloud AI provider, or does it need to stay local?

## Interview talking points (CS / support roles)

- "I built AI ticket deflection for a demo SaaS: a docs-grounded chatbot that cites sources and hands off when it's not confident."
- "I built triage that sorts by real business impact (outages and security first, then customers losing bookings or money) and flags churn risk from tone and intent."
- "I measured it. My keyword baseline scored 100% on tickets I wrote it against and 50% on unseen ones. That gap is why the LLM layer exists, and it's how I'd evaluate any AI support tool before trusting it." (Swap in your Ollama/Claude number once you run it.)
- "I designed it so AI drafts and people decide: refunds, identity verification, and security reports always route to a human."
- "Macros encode policy. Each one sets tags, priority, and status, and carries an internal note, so new agents give the same answer veterans do."

## Next steps (suggested order)

1. Run the unseen set with Ollama on your 3060 Ti machine and note the accuracy: `python triage.py --backend ollama --eval --tickets data/holdout_tickets.json --labels data/holdout_labels.json --out output/holdout`
2. Rebuild the demo page with AI drafts (`build_demo.py --results ...`) and republish.
3. Record a 2-minute Loom walking through the demo page. Buyers on Upwork respond to video.
4. Put the code on GitHub (public repo) and link it from your listing and resume.
5. Add the project to your resume under a "Projects" line using one of the talking points above.
6. Offer the Starter package to one or two local Austin businesses at a low intro price in exchange for a testimonial.
