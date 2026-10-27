# Triage report

Engine: **rules**  ·  Tickets: **20**  ·  Time: 0.0s

- Ready to send after a quick review: **10**
- Need a person to act first (refund, identity check, escalation): **9**
- Spam closed automatically: **1**
- Churn risk flagged: **T-1002, T-1003, T-1019**

**Accuracy vs. hand labels:** category 100%, priority 100%


## Queue (sorted by priority)

| Ticket | Priority | Category | Macro | Human? | Subject |
|---|---|---|---|---|---|
| T-1007 | urgent | outage | M17 | yes | URGENT Pharos won't load |
| T-1020 | urgent | security | M18 | yes | Security issue in task comments |
| T-1001 | high | refund | M01 | yes | Charged twice this month?? |
| T-1003 | high | integrations | M06 | yes | Slack integration broke AGAIN - third time this month |
| T-1004 | high | notifications | M07 | no | Nobody is getting email notifications |
| T-1006 | high | account_access | M12 | no | Locked out - new phone |
| T-1019 | high | cancellation | M05 | yes | Moving to another tool |
| T-1002 | normal | cancellation | M04 | no | where is the cancel button |
| T-1005 | normal | presales | M20 | yes | Questions before I pay |
| T-1008 | normal | refund | M02 | yes | Refund for annual plan |
| T-1011 | normal | bug | M10 | no | Tasks disappeared from our board |
| T-1012 | normal | seats | M13 | no | Can't add a 4th person |
| T-1013 | normal | data_privacy | M15 | no | Former employee requesting deletion of their information |
| T-1015 | normal | workspace_setup | M08 | no | Client sees due dates a day early |
| T-1016 | normal | account_access | M11 | no | password reset not working |
| T-1017 | normal | billing | M22 | yes | Why is my bill $135? |
| T-1018 | normal | seats | M14 | no | Need to take over account - previous owner left |
| T-1009 | low | feature_request | M19 | yes | Dependencies? |
| T-1010 | low | spam | M23 | no | Partnership opportunity - 10x your organic traffic |
| T-1014 | low | feedback | M21 | no | Thank you! |

## Drafts

### T-1007 · URGENT Pharos won't load

*Ben Carter, Carter Build Co. (40 members) (Business)*  
**urgent** · outage · negative · macro M17 · tags: outage, incident

> Pharos won't load for anyone on our team. We've been getting a 502 error for the last 30 minutes on laptops and phones. We have a site handoff at 10 and all our checklists are in there. Is Pharos down??

**Draft reply:**

```
Hi Ben,

Thank you for letting us know so quickly, and I'm sorry. I know your team can't work while Pharos is down. Our engineers are on it right now.

You can follow live updates at status.pharos.example and subscribe there for an alert the moment it's fixed. I've also linked your ticket to the incident, so I'll update you here directly.

Best,
Alex
Pharos Support
```

### T-1020 · Security issue in task comments

*J. Alvarez, Independent researcher (None)*  
**urgent** · security · neutral · macro M18 · tags: security, vulnerability_report

> Hello, I found that task comments don't escape HTML when rendered in the activity feed, so a script posted in a comment runs for anyone who views the feed. This looks like stored XSS. I haven't shared this publicly. Happy to send steps to reproduce privately.

**Draft reply:**

```
Hi J.,

Thank you for contacting Pharos, and for reporting this responsibly and keeping it private. I've escalated it to our security team, and they'll review it as a priority.

Please send the reproduction steps to security@pharos.example rather than replying here, and our security team will follow up with you directly. We'd appreciate you holding off on any public disclosure while we investigate and fix it.

Thanks again for helping keep our customers safe.

Best,
Alex
Pharos Support
```

### T-1001 · Charged twice this month??

*Maria Delgado, Brightside Creative (Team)*  
**high** · refund · neutral · macro M01 · tags: refund, billing_error

> Hi, I just looked at our bank statement and Pharos charged us $80 twice on October 3rd. Same amount, same day. We only have one workspace. Can you please fix this and refund the extra charge? Invoice numbers are PHR-88213 and PHR-88214. Thanks, Maria

**Draft reply:**

```
Hi Maria,

Thank you for contacting Pharos. Sorry about that! The extra charge was an error on our end, and I've refunded it in full.

Depending on your bank, it should show up within 5 to 7 business days. Your plan isn't affected, and there's nothing else you need to do. If you don't see it by then, just reply here and I'll follow up.

Best,
Alex
Pharos Support
```

### T-1003 · Slack integration broke AGAIN - third time this month

*Priya Raman, Lotus Digital Agency (Business)*  
**high** · integrations · negative · macro M06 · tags: integrations, churn_risk

> This is getting ridiculous. Our Slack channel for the Hartwell client project stopped getting task updates again yesterday, and nobody noticed a blocker for a full day. This is the third time this month I've had to reconnect it. I'm paying for your most expensive plan and I'm seriously looking at other tools now. I need this fixed today.

**Draft reply:**

```
Hi Priya,

Thank you for contacting Pharos, and I'm sorry about the trouble. I'm checking the [[fill in: integration]] log for your workspace now and will follow up with what I find.

In the meantime, these cause most integration problems and only take a minute to check:
1. A red "Reconnect" banner under Settings > Integrations. Access can expire after a password change or when the person who connected it leaves the workspace. Click Reconnect and sign in again.
2. For Slack, make sure the Pharos app is still in the channel. If not, type /invite @Pharos there.
3. For GitHub, check that the repository is still selected under Settings > Integrations > GitHub > Repositories.

Talk soon,
Alex
Pharos Support
```

### T-1004 · Nobody is getting email notifications

*James Whitfield, Whitfield Architecture (Team)*  
**high** · notifications · neutral · macro M07 · tags: notifications, email

> Hello, since about the 15th nobody on our team is getting email notifications when they're assigned a task or mentioned. In-app notifications still show up. We've missed two deadlines this week because people didn't know work was waiting on them. Nothing changed on our end that I know of. Can you look into it?

**Draft reply:**

```
Hi James,

Thank you for contacting Pharos, and I'm sorry this has caused missed work. I'm checking our email delivery log for your workspace now.

A few settings that usually explain it:
1. Email is turned on for each notification type under Profile > Notifications.
2. Daily digest is off. When it's on, individual emails pause.
3. Do not disturb (the moon icon by your profile picture) is off.
4. Your company's email filter isn't blocking notifications@pharos.example. Your IT team can allow our domain.

If you can send a screenshot of one teammate's notification settings, that'll help me get to the bottom of it faster.

Best,
Alex
Pharos Support
```

### T-1006 · Locked out - new phone

*Tom Becker, Becker Consulting (Team)*  
**high** · account_access · neutral · macro M12 · tags: account_access, 2fa_reset, identity_verification

> I got a new phone over the weekend and now I can't log in because the 6 digit code app was on my old phone. I never saved any backup codes. I have a client deliverable due tomorrow and all my notes are in Pharos. Please help ASAP.

**Draft reply:**

```
Hi Tom,

Thank you for contacting Pharos. I'll get you back in as quickly as I can. To keep your account safe, I just need to confirm it's you first. Please reply from this email address with:

1. The name of your Pharos workspace
2. If you're the workspace owner, the last 4 digits of the card on file

As soon as that checks out, I'll reset two-factor authentication so you can log in. Once you're in, set it up on your new phone under Profile > Security, and save the backup codes. They'll get you in if this ever happens again.

We'll never ask for your password.

Best,
Alex
Pharos Support
```

### T-1019 · Moving to another tool

*Elena Petrova, Petrova Films (Team)*  
**high** · cancellation · negative · macro M05 · tags: cancellation, churn_risk

> Honestly the integration problems and the surprise charges have been frustrating, so I'm going to switch to a different tool next month. I need to get all our projects, tasks, and files out first. How do I export everything, and then how do I cancel?

**Draft reply:**

```
Hi Elena,

Thank you for contacting Pharos, and for being honest with us. I'm sorry we haven't been what you needed. I've passed your feedback straight to our product team.

Getting your data out is easy:
1. Go to Settings > Data > Export.
2. Choose the whole workspace and pick JSON to keep comments and history, or CSV for spreadsheets.
3. Larger exports arrive by email as a download link within 15 minutes, with attachments in a separate ZIP.

When you're ready, cancel under Settings > Billing > Cancel plan. You'll keep access until the end of your billing period.

Before you go, I'd be glad to look at [[fill in: pain point]] with you. It's often a quick fix. And if you'd rather not pay for now, your workspace can drop to the Free plan and keep all your projects.

Either way, I'm here if you need anything.

Best,
Alex
Pharos Support
```

### T-1002 · where is the cancel button

*Derek Olsen, North Loop Dev (Team)*  
**normal** · cancellation · neutral · macro M04 · tags: cancellation, churn_risk

> I've looked everywhere in settings and there is no cancel option. The owner asked me to cancel our subscription because we're switching to the project tool that comes with our CRM. How do I do it?

**Draft reply:**

```
Hi Derek,

Thank you for contacting Pharos. You're not missing anything: the Cancel plan option only appears for the workspace owner, so admin and member logins won't see it.

The owner can cancel in a minute or two:
1. Log in and go to Settings > Billing > Cancel plan.
2. Pick a reason and confirm.
3. The plan stays active until the end of the current billing period, then the workspace moves to the Free plan. Nothing is deleted.

If it's easier, the owner can reply to this email from their own address and I'll take care of it.

We're sorry to see you go, and thank you for using Pharos.

Best,
Alex
Pharos Support
```

### T-1005 · Questions before I pay

*Alicia Moreno, Moreno Studio (Trial)*  
**normal** · presales · positive · macro M20 · tags: presales, trial

> Hi! I'm on the trial and loving it so far. Two questions before I pick a plan: can my clients see their own projects without paying for a seat? And can I make some projects private so only two of us can see them?

**Draft reply:**

```
Hi Alicia,

Thank you for contacting Pharos! I'm so glad you're enjoying the trial. Happy to help you pick the right plan.

[[fill in: answers]]

You can compare all the plans at help.pharos.example/plans-and-pricing, and paying annually gets you two months free.

If anything else comes up, just reply here.

Best,
Alex
Pharos Support
```

### T-1008 · Refund for annual plan

*Grace Kim, Kim Design Co. (Team)*  
**normal** · refund · negative · macro M02 · tags: refund, annual_plan

> Hello, I paid for the annual Team plan 12 days ago, but unfortunately I have to close my studio at the end of the month for family reasons. Is it possible to get a refund for the rest of the year? I'm sorry for the trouble. Grace

**Draft reply:**

```
Hi Grace,

Thank you for contacting Pharos, and please don't apologize. I'm sorry things have changed, and I hope all is well with you.

Since you're within 30 days of your annual payment, you're eligible for a refund for the rest of the year. I'll take care of everything:
1. I'll cancel the annual plan and refund the unused days.
2. The refund will reach your card in 5 to 7 business days.
3. Your workspace stays fully active until [[fill in: end date]], so you can wrap up any open projects.

If you'd like a copy of your projects, you can export them anytime under Settings > Data > Export.

Wishing you all the best,
Alex
Pharos Support
```

### T-1011 · Tasks disappeared from our board

*Linda Park, Park Events (Team)*  
**normal** · bug · neutral · macro M10 · tags: bug

> This morning a whole column of tasks on our Fall Gala board just vanished. There were about 15 tasks in the Vendors column and now it's empty. Nobody on my team says they deleted anything. Where did they go?

**Draft reply:**

```
Hi Linda,

Thank you for contacting Pharos, and sorry for the scare. This is usually recoverable, so let's track it down.

For missing tasks, check these first:
1. Click Clear filters at the top of the board. A saved view can hide tasks.
2. Turn on Show archived in the view menu. Completed tasks can be archived automatically.
3. Look in Projects > Trash. Deleted tasks stay there for 30 days and can be restored.

For a file that won't upload, attachments can be up to 100 MB on paid plans. Larger files, like videos, can be attached from Google Drive instead.

If none of that solves it, reply with a screenshot and roughly when it happened, and I'll dig into your workspace activity.

Best,
Alex
Pharos Support
```

### T-1012 · Can't add a 4th person

*Chris Nguyen, Urban Mane Marketing (Free)*  
**normal** · seats · neutral · macro M13 · tags: seats, plan_limit, upsell

> Trying to invite a new hire and it says we've reached our member limit. There are only 3 of us at the moment. What are my options?

**Draft reply:**

```
Hi Chris,

Thank you for contacting Pharos, and congratulations on growing your team! The Free plan includes up to 3 members, so you have two options:

1. Upgrade to Team ($10 per member a month) for unlimited members and projects. It takes effect right away: Settings > Billing > Change plan.
2. If the new person only needs to view and comment on certain projects, you can invite them as a guest instead. Guests are free on paid plans.

Happy to help with either one.

Best,
Alex
Pharos Support
```

### T-1013 · Former employee requesting deletion of their information

*Nadia Hassan, Clearpath HR (Business)*  
**normal** · data_privacy · neutral · macro M15 · tags: data_privacy, deletion_request

> A former employee emailed asking us to delete all of their personal information from our systems, including our project management tool. How do we do that in Pharos, and does it remove them from your servers too?

**Draft reply:**

```
Hi Nadia,

Thank you for contacting Pharos, and for handling this so carefully. Here's how it works:

1. A workspace admin removes the person under Settings > Members.
2. On their profile, click Anonymize. Their name is replaced on past comments and activity, and their personal details are removed.
3. On our side, removed data is cleared from active systems right away and fully purged from backups within 90 days.

Since Pharos handles your workspace data on your behalf, that's all you need to do, and you can let them know it's done. If they've made a formal request and you'd like written confirmation, just let me know.

Best,
Alex
Pharos Support
```

### T-1015 · Client sees due dates a day early

*Rosa Jimenez, Jimenez Web Works (Team)*  
**normal** · workspace_setup · neutral · macro M08 · tags: workspace_setup, time_zone

> I'm in Austin. Our client in London is a guest on our project, and she says every due date shows a day earlier than what I set. A task I set for the 14th shows the 13th for her. Why are the dates different?

**Draft reply:**

```
Hi Rosa,

Thank you for contacting Pharos. When due dates are off by a day for someone else, it's almost always time zones, and it's an easy fix.

Due dates show in each person's own time zone, so:
1. Ask everyone, including guests, to check their time zone under Profile > Preferences.
2. For tasks shared across time zones, set a specific due time (like 5:00 PM your time) instead of an all-day date. That keeps the date from slipping to the day before for people ahead or behind you.

Happy to help if anything still looks off.

Best,
Alex
Pharos Support
```

### T-1016 · password reset not working

*Kevin Shah, Shah CPA (Team)*  
**normal** · account_access · neutral · macro M11 · tags: account_access, password_reset

> I clicked forgot password like 5 times and never got an email. Checked spam. My login email might be my old gmail though, not sure.

**Draft reply:**

```
Hi Kevin,

Thank you for contacting Pharos. I'll help you get back in. Reset emails come from security@pharos.example and only go to the exact address your account was created with, so if you signed up with a different email, that's where it went.

Try requesting the reset with your other address, and use the link within an hour, since it expires after that. If you can't get into that inbox anymore, just let me know and I'll walk you through verifying your account another way.

Best,
Alex
Pharos Support
```

### T-1017 · Why is my bill $135?

*Hannah Lee, Lee & Co Accounting (Team)*  
**normal** · billing · negative · macro M22 · tags: billing, prorated_charges

> We have 10 people on the Team plan so I expected $100, but this month's invoice is $135. There's a line that says prorated member charges. I had no idea adding people mid-month cost extra. Can you explain and can I get that taken off?

**Draft reply:**

```
Hi Hannah,

Thank you for contacting Pharos. I can see how that was a surprise, so here's what happened.

Plans are billed per member. When someone joins partway through the month, we charge for the days left in that month, and that charge lands on your next invoice. That's the prorated line you're seeing, and it won't repeat. Going forward, your bill reflects your current number of members.

[[fill in: credit line]]

Two tips: removing someone credits their unused time to your next invoice, and clients or contractors who only need to view and comment can join as free guests.

Best,
Alex
Pharos Support
```

### T-1018 · Need to take over account - previous owner left

*Marcus Bell, Bell Engineering (Business)*  
**normal** · seats · neutral · macro M14 · tags: seats, ownership_transfer, identity_verification

> Our operations manager set up our Pharos workspace and was the owner on it. She left the company last month and isn't responding to us. I'm the company owner and an admin in the workspace. How do I get ownership moved to me so I can manage billing?

**Draft reply:**

```
Hi Marcus,

Thank you for contacting Pharos. Normally the current owner transfers ownership, but since they aren't reachable, we can take care of it for you after a quick verification.

Please reply with one of these showing your name and the business name:
- A business license or registration
- A recent business invoice or bank statement

Once a team lead approves it, usually within one business day, I'll move ownership to your login, since you're already an admin.

Best,
Alex
Pharos Support
```

### T-1009 · Dependencies?

*Sam Ortiz, Inkwell Media (Team)*  
**low** · feature_request · positive · macro M19 · tags: feature_request

> Love the app. Any chance you'll add task dependencies to the timeline view? When one task slips I have to move everything after it by hand. Right now I'm tracking it in a spreadsheet lol

**Draft reply:**

```
Hi Sam,

Thank you for contacting Pharos, and for the kind words! That's a great idea, and I've passed it to our product team along with how you'd use it, which really helps them decide what to build next.

[[fill in: roadmap status]]

You can vote on and follow ideas at ideas.pharos.example, and see what's coming at ideas.pharos.example/roadmap.

Best,
Alex
Pharos Support
```

### T-1010 · Partnership opportunity - 10x your organic traffic

*Kevin from RankRocket, RankRocket SEO (None)*  
**low** · spam · neutral · macro M23 · tags: spam

> Hi there, I came across pharos.example and noticed you're missing out on huge organic traffic. Our team guarantees first-page Google rankings in 30 days. Can I send over a free audit? Reply YES to get started.

**Draft reply:**

```
(no reply: closed as spam)
```

### T-1014 · Thank you!

*Owen Brooks, Brooks Sound Studio (Team)*  
**low** · feedback · positive · macro M21 · tags: feedback, positive

> Just wanted to say thanks. We switched from sticky notes and a group chat three months ago and we haven't dropped a single client request since. The timeline view alone has saved me hours. Great product!

**Draft reply:**

```
Hi Owen,

Thank you so much for writing in. This genuinely made our whole team's day, and I've shared it with everyone here.

If you ever have a minute, a short review on Capterra or G2 helps other small teams find us. No pressure at all.

Thanks for being part of Pharos,
Alex
Pharos Support
```
