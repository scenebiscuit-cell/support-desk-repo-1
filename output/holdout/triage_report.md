# Triage report

Engine: **rules**  ·  Tickets: **12**  ·  Time: 0.0s

- Ready to send after a quick review: **3**
- Need a person to act first (refund, identity check, escalation): **9**
- Spam closed automatically: **0**
- Churn risk flagged: **none**

**Accuracy vs. hand labels:** category 67%, priority 67%

- H-02: got integrations/high, expected feature_request/low
- H-09: got notifications/normal, expected notifications/high
- H-10: got refund/normal, expected workspace_setup/normal
- H-11: got billing/normal, expected refund/high
- H-12: got account_access/normal, expected security/urgent

## Queue (sorted by priority)

| Ticket | Priority | Category | Macro | Human? | Subject |
|---|---|---|---|---|---|
| H-01 | high | billing | M22 | yes | Everything is read-only |
| H-02 | high | integrations | M06 | yes | offline on the phone app |
| H-04 | high | account_access | M11 | no | too many attempts |
| H-03 | normal | integrations | M06 | yes | Due dates not on my Google Calendar |
| H-05 | normal | presales | M20 | yes | Nonprofit pricing? |
| H-06 | normal | notifications | M07 | yes | emails going to junk |
| H-07 | normal | cancellation | M04 | yes | close account |
| H-08 | normal | bug | M10 | no | video won't attach |
| H-09 | normal | notifications | M07 | yes | 400 emails overnight?! |
| H-10 | normal | refund | M03 | yes | reuse our refund requests board |
| H-11 | normal | billing | M22 | yes | Billed for wrong plan |
| H-12 | normal | account_access | M11 | no | Login I don't recognize |

## Drafts

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
