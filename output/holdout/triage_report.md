# Triage report

Engine: **rules**  ·  Tickets: **36**  ·  Time: 0.0s

- Ready to send after a quick review: **12**
- Need a person to act first (refund, identity check, escalation): **23**
- Spam closed automatically: **1**
- Churn risk flagged: **H-15, H-34**

**Accuracy vs. hand labels:** category 78%, priority 72%

- H-02: got integrations/high, expected feature_request/low
- H-09: got notifications/normal, expected notifications/high
- H-10: got refund/normal, expected workspace_setup/normal
- H-11: got billing/normal, expected refund/high
- H-12: got account_access/normal, expected security/urgent
- H-14: got billing/normal, expected refund/high
- H-20: got account_access/normal, expected account_access/high
- H-25: got workspace_setup/normal, expected feature_request/low
- H-30: got billing/normal, expected billing/high
- H-33: got bug/normal, expected bug/high
- H-34: got cancellation/high, expected notifications/high
- H-35: got account_access/normal, expected security/urgent

## Queue (sorted by priority)

| Ticket | Priority | Category | Macro | Human? | Subject |
|---|---|---|---|---|---|
| H-23 | urgent | outage | M17 | yes | Is Pharos down? |
| H-24 | urgent | security | M18 | yes | Possible XSS in task comments |
| H-01 | high | billing | M22 | yes | Everything is read-only |
| H-02 | high | integrations | M06 | yes | offline on the phone app |
| H-04 | high | account_access | M11 | no | too many attempts |
| H-19 | high | bug | M10 | no | File uploads failing |
| H-34 | high | cancellation | M05 | yes | We're switching to a competitor unless this gets fixed |
| H-03 | normal | integrations | M06 | yes | Due dates not on my Google Calendar |
| H-05 | normal | presales | M20 | yes | Nonprofit pricing? |
| H-06 | normal | notifications | M07 | yes | emails going to junk |
| H-07 | normal | cancellation | M04 | yes | close account |
| H-08 | normal | bug | M10 | no | video won't attach |
| H-09 | normal | notifications | M07 | yes | 400 emails overnight?! |
| H-10 | normal | refund | M03 | yes | reuse our refund requests board |
| H-11 | normal | billing | M22 | yes | Billed for wrong plan |
| H-12 | normal | account_access | M11 | no | Login I don't recognize |
| H-13 | normal | billing | M22 | yes | Can I pay by invoice instead of card? |
| H-14 | normal | billing | M22 | yes | Charged for 14 seats, we only have 9 |
| H-15 | normal | cancellation | M05 | yes | Close our account |
| H-16 | normal | integrations | M06 | yes | GitHub PRs not linking to tasks |
| H-17 | normal | notifications | M07 | yes | Way too many emails |
| H-18 | normal | workspace_setup | M09 | yes | How do I make a project private? |
| H-20 | normal | account_access | M12 | no | Locked out after new phone |
| H-21 | normal | seats | M13 | no | Adding a client as a guest |
| H-22 | normal | data_privacy | M15 | no | Delete my personal data |
| H-25 | normal | workspace_setup | M09 | yes | Gantt view? |
| H-26 | normal | presales | M20 | yes | Questions before we sign up |
| H-29 | normal | seats | M14 | no | Transfer ownership |
| H-30 | normal | billing | M22 | yes | Card declined, account suspended? |
| H-31 | normal | data_privacy | M16 | no | Export all our projects |
| H-32 | normal | integrations | M06 | yes | Google Calendar not showing due dates |
| H-33 | normal | bug | M10 | no | Tasks disappeared from a board |
| H-35 | normal | account_access | M11 | no | Weird login from another country |
| H-36 | normal | refund | M02 | yes | Refund for annual plan we just bought |
| H-27 | low | feedback | M21 | no | Just wanted to say thanks |
| H-28 | low | spam | M23 | no | Get 10,000 leads this month |

## Drafts

### H-23 · Is Pharos down?

*Grace Obi, Obi Consulting (Team)*  
**urgent** · outage · neutral · macro M17 · tags: outage, incident

> None of the boards are loading for anyone on my team, and two other agencies I know say the same. Just a spinning wheel.

**Draft reply:**

```
Hi Grace,

Thank you for letting us know so quickly, and I'm sorry. I know your team can't work while Pharos is down. Our engineers are on it right now.

You can follow live updates at status.pharos.example and subscribe there for an alert the moment it's fixed. I've also linked your ticket to the incident, so I'll update you here directly.

Best,
Alex
Pharos Support
```

### H-24 · Possible XSS in task comments

*Ivan Petrov,  ()*  
**urgent** · security · neutral · macro M18 · tags: security, vulnerability_report

> Hi, I'm a security researcher. I found a way to run JavaScript through a crafted task comment. I'd like to report it responsibly. Who should I send details to?

**Draft reply:**

```
Hi Ivan,

Thank you for contacting Pharos, and for reporting this responsibly and keeping it private. I've escalated it to our security team, and they'll review it as a priority.

Please send the reproduction steps to security@pharos.example rather than replying here, and our security team will follow up with you directly. We'd appreciate you holding off on any public disclosure while we investigate and fix it.

Thanks again for helping keep our customers safe.

Best,
Alex
Pharos Support
```

### H-01 · Everything is read-only

*Dana Fowler, Fowler Legal Ops (Team)*  
**high** · billing · neutral · macro M22 · tags: billing, prorated_charges

> This morning none of us can edit anything in Pharos. There's a banner saying the workspace is read-only. I think my card expired last week. I updated it an hour ago but we still can't edit, and my team is just sitting here.

**Draft reply:**

```
Hi Dana,

Thank you for contacting Pharos. I can see how that was a surprise, so here's what happened.

Plans are billed per member. When someone joins partway through the month, we charge for the days left in that month, and that charge lands on your next invoice. That's the prorated line you're seeing, and it won't repeat. Going forward, your bill reflects your current number of members.

[[fill in: credit line]]

Two tips: removing someone credits their unused time to your next invoice, and clients or contractors who only need to view and comment can join as free guests.

Best,
Alex
Pharos Support
```

### H-02 · offline on the phone app

*Leo Martins, Martins Field Services (Team)*  
**high** · integrations · neutral · macro M06 · tags: integrations

> My crews work in buildings with no signal. Is there any way the mobile app can work offline and sync later? Right now they write stuff on paper and re-enter it.

**Draft reply:**

```
Hi Leo,

Thank you for contacting Pharos, and I'm sorry about the trouble. I'm checking the [[fill in: integration]] log for your workspace now and will follow up with what I find.

In the meantime, these cause most integration problems and only take a minute to check:
1. A red "Reconnect" banner under Settings > Integrations. Access can expire after a password change or when the person who connected it leaves the workspace. Click Reconnect and sign in again.
2. For Slack, make sure the Pharos app is still in the channel. If not, type /invite @Pharos there.
3. For GitHub, check that the repository is still selected under Settings > Integrations > GitHub > Repositories.

Talk soon,
Alex
Pharos Support
```

### H-04 · too many attempts

*Paul Grady, Grady HVAC (Team)*  
**high** · account_access · neutral · macro M11 · tags: account_access, password_reset

> It says too many attempts and won't let me in. I'm presenting the project plan to a customer in 20 minutes and it's all in there.

**Draft reply:**

```
Hi Paul,

Thank you for contacting Pharos. I'll help you get back in. Reset emails come from security@pharos.example and only go to the exact address your account was created with, so if you signed up with a different email, that's where it went.

Try requesting the reset with your other address, and use the link within an hour, since it expires after that. If you can't get into that inbox anymore, just let me know and I'll walk you through verifying your account another way.

Best,
Alex
Pharos Support
```

### H-19 · File uploads failing

*Jordan Hale, Hale Media (Business)*  
**high** · bug · neutral · macro M10 · tags: bug

> Every time I try to attach a PDF to a task I get 'Upload failed'. Images work fine. Client review is tomorrow and I need these files in.

**Draft reply:**

```
Hi Jordan,

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

### H-34 · We're switching to a competitor unless this gets fixed

*Nina Kowal, Kowal Art (Team)*  
**high** · cancellation · negative · macro M05 · tags: cancellation, churn_risk

> Third time this month notifications just stop for a whole day. We rely on them. If this happens again we're moving to another tool.

**Draft reply:**

```
Hi Nina,

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

### H-03 · Due dates not on my Google Calendar

*Imani Wright, Wright Wellness Co. (Team)*  
**normal** · integrations · neutral · macro M06 · tags: integrations

> I connected my Google Calendar last week but none of my task due dates are showing up on it. I'd really like to see them next to my meetings.

**Draft reply:**

```
Hi Imani,

Thank you for contacting Pharos, and I'm sorry about the trouble. I'm checking the [[fill in: integration]] log for your workspace now and will follow up with what I find.

In the meantime, these cause most integration problems and only take a minute to check:
1. A red "Reconnect" banner under Settings > Integrations. Access can expire after a password change or when the person who connected it leaves the workspace. Click Reconnect and sign in again.
2. For Slack, make sure the Pharos app is still in the channel. If not, type /invite @Pharos there.
3. For GitHub, check that the repository is still selected under Settings > Integrations > GitHub > Repositories.

Talk soon,
Alex
Pharos Support
```

### H-05 · Nonprofit pricing?

*Ruth Okafor, Eastside Free Clinic (Trial)*  
**normal** · presales · neutral · macro M20 · tags: presales, trial

> We're a volunteer-run free clinic (501c3) using the trial to organize our outreach events. Is there any discount for nonprofits before we commit to a plan?

**Draft reply:**

```
Hi Ruth,

Thank you for contacting Pharos! I'm so glad you're enjoying the trial. Happy to help you pick the right plan.

[[fill in: answers]]

You can compare all the plans at help.pharos.example/plans-and-pricing, and paying annually gets you two months free.

If anything else comes up, just reply here.

Best,
Alex
Pharos Support
```

### H-06 · emails going to junk

*Sofia Reyes, Reyes Brand Studio (Team)*  
**normal** · notifications · neutral · macro M07 · tags: notifications, email

> A couple of people on my team said the emails from Pharos land in their junk folder, so they miss when they're assigned something. Anything I can do?

**Draft reply:**

```
Hi Sofia,

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

### H-07 · close account

*Walt Hughes, Hughes Restoration (Team)*  
**normal** · cancellation · positive · macro M04 · tags: cancellation

> Retiring at the end of the year. Please close my account and delete everything when the time comes. Thanks for the good service.

**Draft reply:**

```
Hi Walt,

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

### H-08 · video won't attach

*Mei Chen, Chen Visuals (Team)*  
**normal** · bug · neutral · macro M10 · tags: bug

> I'm trying to attach a 250 MB video file to a task for client review and it just says Upload failed every time. Smaller images work fine.

**Draft reply:**

```
Hi Mei,

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

### H-09 · 400 emails overnight?!

*Dre Washington, Washington Creative (Business)*  
**normal** · notifications · negative · macro M07 · tags: notifications, email

> Everyone on my team woke up to hundreds of Pharos emails, one for every single comment on our big launch project. People are furious and some are talking about turning email off entirely. What happened and how do I stop this?

**Draft reply:**

```
Hi Dre,

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

### H-10 · reuse our refund requests board

*Ava Lindqvist, Lindqvist Interiors (Team)*  
**normal** · refund · neutral · macro M03 · tags: refund, policy_decline

> We have a project called Refund Requests with columns we really like. Can I reuse that setup for new projects so I don't rebuild it every time?

**Draft reply:**

```
Hi Ava,

Thank you for contacting Pharos. I wish I had better news: on monthly plans, we aren't able to refund part of a month. The good news is that nothing shuts off early. You'll keep full access through the end of the period you've already paid for.

If you'd like to make sure you aren't charged again, I'm happy to cancel for you, or you can do it anytime under Settings > Billing > Cancel plan.

And if something on our end didn't work the way it should have, please tell me. I'd like to take another look.

Best,
Alex
Pharos Support
```

### H-11 · Billed for wrong plan

*Ray Dominguez, Dominguez Landscape (Team)*  
**normal** · billing · neutral · macro M22 · tags: billing, prorated_charges

> We're on the Team plan but this month's invoice charged us $20 per person for Business. We never upgraded. Please correct it.

**Draft reply:**

```
Hi Ray,

Thank you for contacting Pharos. I can see how that was a surprise, so here's what happened.

Plans are billed per member. When someone joins partway through the month, we charge for the days left in that month, and that charge lands on your next invoice. That's the prorated line you're seeing, and it won't repeat. Going forward, your bill reflects your current number of members.

[[fill in: credit line]]

Two tips: removing someone credits their unused time to your next invoice, and clients or contractors who only need to view and comment can join as free guests.

Best,
Alex
Pharos Support
```

### H-12 · Login I don't recognize

*Beth Sorensen, Sorensen Counseling Group (Business)*  
**normal** · account_access · neutral · macro M11 · tags: account_access, password_reset

> Under recent activity I see a login from another country at 2am yesterday. That wasn't me or anyone on my team. What should I do?

**Draft reply:**

```
Hi Beth,

Thank you for contacting Pharos. I'll help you get back in. Reset emails come from security@pharos.example and only go to the exact address your account was created with, so if you signed up with a different email, that's where it went.

Try requesting the reset with your other address, and use the link within an hour, since it expires after that. If you can't get into that inbox anymore, just let me know and I'll walk you through verifying your account another way.

Best,
Alex
Pharos Support
```

### H-13 · Can I pay by invoice instead of card?

*Owen Price, Price Studio (Team)*  
**normal** · billing · neutral · macro M22 · tags: billing, prorated_charges

> Our finance team wants to pay annually by bank transfer instead of a credit card. Is that possible and how do we set it up?

**Draft reply:**

```
Hi Owen,

Thank you for contacting Pharos. I can see how that was a surprise, so here's what happened.

Plans are billed per member. When someone joins partway through the month, we charge for the days left in that month, and that charge lands on your next invoice. That's the prorated line you're seeing, and it won't repeat. Going forward, your bill reflects your current number of members.

[[fill in: credit line]]

Two tips: removing someone credits their unused time to your next invoice, and clients or contractors who only need to view and comment can join as free guests.

Best,
Alex
Pharos Support
```

### H-14 · Charged for 14 seats, we only have 9

*Leah Moss, Moss & Co (Business)*  
**normal** · billing · neutral · macro M22 · tags: billing, prorated_charges

> Our latest invoice bills us for 14 seats but there are only 9 people in our workspace. We removed 5 people last month. Please refund the difference.

**Draft reply:**

```
Hi Leah,

Thank you for contacting Pharos. I can see how that was a surprise, so here's what happened.

Plans are billed per member. When someone joins partway through the month, we charge for the days left in that month, and that charge lands on your next invoice. That's the prorated line you're seeing, and it won't repeat. Going forward, your bill reflects your current number of members.

[[fill in: credit line]]

Two tips: removing someone credits their unused time to your next invoice, and clients or contractors who only need to view and comment can join as free guests.

Best,
Alex
Pharos Support
```

### H-15 · Close our account

*Tom Becker, Becker Print (Team)*  
**normal** · cancellation · neutral · macro M05 · tags: cancellation, churn_risk

> We've moved our projects to another tool and won't be renewing. Please cancel our subscription at the end of this billing period.

**Draft reply:**

```
Hi Tom,

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

### H-16 · GitHub PRs not linking to tasks

*Priya Nair, Nair Design (Team)*  
**normal** · integrations · neutral · macro M06 · tags: integrations

> When we mention a task ID in a GitHub pull request it used to link automatically. Since Monday nothing links anymore. Did something change?

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

### H-17 · Way too many emails

*Carlos Ruiz, Ruiz Architecture (Business)*  
**normal** · notifications · neutral · macro M07 · tags: notifications, email

> I'm getting an email for every single comment on every project. How do I turn these down to just things I'm assigned to?

**Draft reply:**

```
Hi Carlos,

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

### H-18 · How do I make a project private?

*Mei Lin, Lin Labs (Team)*  
**normal** · workspace_setup · neutral · macro M09 · tags: workspace_setup, how_to

> I want a project only three of us can see while we plan a surprise for the rest of the team. How do I do that?

**Draft reply:**

```
Hi Mei,

Thank you for contacting Pharos. Happy to help with that.

[[fill in: answer]]

There's more detail in our guide to projects, boards, and templates: help.pharos.example/projects-and-boards

Best,
Alex
Pharos Support
```

### H-20 · Locked out after new phone

*Sam Ortiz, Ortiz Co (Team)*  
**normal** · account_access · neutral · macro M12 · tags: account_access, 2fa_reset, identity_verification

> I got a new phone and my authenticator app didn't transfer, so I can't get past two-factor. I have a deadline this afternoon. Please help me get back in.

**Draft reply:**

```
Hi Sam,

Thank you for contacting Pharos. I'll get you back in as quickly as I can. To keep your account safe, I just need to confirm it's you first. Please reply from this email address with:

1. The name of your Pharos workspace
2. If you're the workspace owner, the last 4 digits of the card on file

As soon as that checks out, I'll reset two-factor authentication so you can log in. Once you're in, set it up on your new phone under Profile > Security, and save the backup codes. They'll get you in if this ever happens again.

We'll never ask for your password.

Best,
Alex
Pharos Support
```

### H-21 · Adding a client as a guest

*Ava Green, Green Room Events (Team)*  
**normal** · seats · neutral · macro M13 · tags: seats, plan_limit, upsell

> We want our client to see one project but not the rest of our workspace. Can we add them as a guest and does that cost a seat?

**Draft reply:**

```
Hi Ava,

Thank you for contacting Pharos, and congratulations on growing your team! The Free plan includes up to 3 members, so you have two options:

1. Upgrade to Team ($10 per member a month) for unlimited members and projects. It takes effect right away: Settings > Billing > Change plan.
2. If the new person only needs to view and comment on certain projects, you can invite them as a guest instead. Guests are free on paid plans.

Happy to help with either one.

Best,
Alex
Pharos Support
```

### H-22 · Delete my personal data

*Noah Fischer, Fischer Law (Business)*  
**normal** · data_privacy · neutral · macro M15 · tags: data_privacy, deletion_request

> I left Fischer Law last week. Under GDPR I'm asking you to delete my personal data from Pharos.

**Draft reply:**

```
Hi Noah,

Thank you for contacting Pharos, and for handling this so carefully. Here's how it works:

1. A workspace admin removes the person under Settings > Members.
2. On their profile, click Anonymize. Their name is replaced on past comments and activity, and their personal details are removed.
3. On our side, removed data is cleared from active systems right away and fully purged from backups within 90 days.

Since Pharos handles your workspace data on your behalf, that's all you need to do, and you can let them know it's done. If they've made a formal request and you'd like written confirmation, just let me know.

Best,
Alex
Pharos Support
```

### H-25 · Gantt view?

*Lucy Tran, Tran Films (Team)*  
**normal** · workspace_setup · positive · macro M09 · tags: workspace_setup, how_to

> Do you have a Gantt chart or timeline view? We'd really love one for production schedules.

**Draft reply:**

```
Hi Lucy,

Thank you for contacting Pharos. Happy to help with that.

[[fill in: answer]]

There's more detail in our guide to projects, boards, and templates: help.pharos.example/projects-and-boards

Best,
Alex
Pharos Support
```

### H-26 · Questions before we sign up

*Ben Carter,  ()*  
**normal** · presales · neutral · macro M20 · tags: presales, trial

> We're a 12-person agency comparing tools. Do you offer a discount for annual billing and can we try the Business plan features during the trial?

**Draft reply:**

```
Hi Ben,

Thank you for contacting Pharos! I'm so glad you're enjoying the trial. Happy to help you pick the right plan.

[[fill in: answers]]

You can compare all the plans at help.pharos.example/plans-and-pricing, and paying annually gets you two months free.

If anything else comes up, just reply here.

Best,
Alex
Pharos Support
```

### H-29 · Transfer ownership

*Ethan Moore, Moore Build (Business)*  
**normal** · seats · neutral · macro M14 · tags: seats, ownership_transfer, identity_verification

> I'm leaving the company and need to hand workspace ownership to my colleague Kate before Friday. How do I do that?

**Draft reply:**

```
Hi Ethan,

Thank you for contacting Pharos. Normally the current owner transfers ownership, but since they aren't reachable, we can take care of it for you after a quick verification.

Please reply with one of these showing your name and the business name:
- A business license or registration
- A recent business invoice or bank statement

Once a team lead approves it, usually within one business day, I'll move ownership to your login, since you're already an admin.

Best,
Alex
Pharos Support
```

### H-30 · Card declined, account suspended?

*Hana Sato, Sato UX (Team)*  
**normal** · billing · neutral · macro M22 · tags: billing, prorated_charges

> My card was declined on renewal and now we got an email saying the workspace will be suspended. I've added a new card. Will we lose anything?

**Draft reply:**

```
Hi Hana,

Thank you for contacting Pharos. I can see how that was a surprise, so here's what happened.

Plans are billed per member. When someone joins partway through the month, we charge for the days left in that month, and that charge lands on your next invoice. That's the prorated line you're seeing, and it won't repeat. Going forward, your bill reflects your current number of members.

[[fill in: credit line]]

Two tips: removing someone credits their unused time to your next invoice, and clients or contractors who only need to view and comment can join as free guests.

Best,
Alex
Pharos Support
```

### H-31 · Export all our projects

*Leo Brooks, Brooks Agency (Team)*  
**normal** · data_privacy · neutral · macro M16 · tags: data_export

> We need a full export of every project and task for our records. What format do we get and how long does it take?

**Draft reply:**

```
Hi Leo,

Thank you for contacting Pharos. You can export everything yourself in a couple of minutes:

1. Go to Settings > Data > Export (owners and admins only).
2. Choose one project or the whole workspace.
3. Pick CSV for spreadsheets or JSON to keep comments and history. Larger exports arrive by email as a link within 15 minutes, with attachments in a separate ZIP.

Best,
Alex
Pharos Support
```

### H-32 · Google Calendar not showing due dates

*Zoe Clark, Clark PR (Business)*  
**normal** · integrations · neutral · macro M06 · tags: integrations

> I connected Google Calendar but none of our task due dates show up. It's been a day. Am I missing a step?

**Draft reply:**

```
Hi Zoe,

Thank you for contacting Pharos, and I'm sorry about the trouble. I'm checking the [[fill in: integration]] log for your workspace now and will follow up with what I find.

In the meantime, these cause most integration problems and only take a minute to check:
1. A red "Reconnect" banner under Settings > Integrations. Access can expire after a password change or when the person who connected it leaves the workspace. Click Reconnect and sign in again.
2. For Slack, make sure the Pharos app is still in the channel. If not, type /invite @Pharos there.
3. For GitHub, check that the repository is still selected under Settings > Integrations > GitHub > Repositories.

Talk soon,
Alex
Pharos Support
```

### H-33 · Tasks disappeared from a board

*Marco Bianchi, Bianchi Foods (Team)*  
**normal** · bug · neutral · macro M10 · tags: bug

> About 20 tasks vanished from our Launch board overnight. Nobody deleted them as far as we know. This is our main board for a launch next week.

**Draft reply:**

```
Hi Marco,

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

### H-35 · Weird login from another country

*Omar Haddad, Haddad Tech (Business)*  
**normal** · account_access · neutral · macro M11 · tags: account_access, password_reset

> I got an alert that someone logged into my account from a country I've never been to. I didn't do this. What should I do?

**Draft reply:**

```
Hi Omar,

Thank you for contacting Pharos. I'll help you get back in. Reset emails come from security@pharos.example and only go to the exact address your account was created with, so if you signed up with a different email, that's where it went.

Try requesting the reset with your other address, and use the link within an hour, since it expires after that. If you can't get into that inbox anymore, just let me know and I'll walk you through verifying your account another way.

Best,
Alex
Pharos Support
```

### H-36 · Refund for annual plan we just bought

*Ella Ward, Ward Events (Team)*  
**normal** · refund · neutral · macro M02 · tags: refund, annual_plan

> We bought the annual Team plan 10 days ago by mistake, we meant to pick monthly. Can we get a refund and switch?

**Draft reply:**

```
Hi Ella,

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

### H-27 · Just wanted to say thanks

*Rosa Diaz, Diaz Studio (Team)*  
**low** · feedback · positive · macro M21 · tags: feedback, positive

> Your new board templates saved us hours this week. The team loves them. No question, just a thank you!

**Draft reply:**

```
Hi Rosa,

Thank you so much for writing in. This genuinely made our whole team's day, and I've shared it with everyone here.

If you ever have a minute, a short review on Capterra or G2 helps other small teams find us. No pressure at all.

Thanks for being part of Pharos,
Alex
Pharos Support
```

### H-28 · Get 10,000 leads this month

*Growth Hacker, LeadsBlast ()*  
**low** · spam · neutral · macro M23 · tags: spam

> Hi there, we help SaaS companies like yours 10x their pipeline with our premium lead lists. Book a call this week for 50% off.

**Draft reply:**

```
(no reply: closed as spam)
```
