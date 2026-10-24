# Triage report

Engine: **rules**  ·  Tickets: **12**  ·  Time: 0.0s

- Ready to send after a quick review: **3**
- Need a person to act first (refund, identity check, escalation): **9**
- Spam closed automatically: **0**
- Churn risk flagged: **none**

**Accuracy vs. hand labels:** category 50%, priority 58%

- H-01: got booking_setup/high, expected billing/high
- H-02: got calendar_sync/high, expected feature_request/low
- H-03: got booking_setup/normal, expected calendar_sync/normal
- H-04: got account_access/normal, expected account_access/high
- H-06: got reminders/high, expected reminders/normal
- H-10: got payments/normal, expected booking_setup/normal
- H-11: got billing/normal, expected refund/high
- H-12: got account_access/normal, expected security/urgent

## Queue (sorted by priority)

| Ticket | Priority | Category | Macro | Human? | Subject |
|---|---|---|---|---|---|
| H-01 | high | booking_setup | M09 | no | Page says not taking bookings |
| H-02 | high | calendar_sync | M06 | yes | recurring lessons |
| H-06 | high | reminders | M07 | yes | confirmation emails going to spam |
| H-09 | high | reminders | M07 | no | texts at 3am?! |
| H-03 | normal | booking_setup | M09 | yes | Outlook events not blocking my availability |
| H-04 | normal | account_access | M11 | yes | too many attempts |
| H-05 | normal | presales | M20 | yes | Nonprofit pricing? |
| H-07 | normal | cancellation | M04 | yes | close account |
| H-08 | normal | payments | M10 | yes | refund a patient's deposit |
| H-10 | normal | payments | M10 | yes | embed not showing on squarespace |
| H-11 | normal | billing | M22 | yes | Billed for wrong plan |
| H-12 | normal | account_access | M11 | no | Login I don't recognize |

## Drafts

### H-01 · Page says not taking bookings

*Dana Fowler, Fowler Mediation (Solo)*  
**high** · booking_setup · neutral · macro M09 · tags: booking_setup, booking_page_error

> My booking page suddenly says this business isn't taking bookings right now. I think my card expired last week. I updated it this morning but the page still says the same thing. Clients are emailing me asking what's going on.

**Draft reply:**

```
Hi Dana,

Sorry your booking page isn't loading. Let's get it back up. A few quick checks:

1. Status page: https://status.pharos.example shows any active incidents.
2. Account status: a paused or past-due account shows "This business isn't taking bookings right now."
3. Try the page in a private browser window to rule out extensions.

If it still fails, please reply with the page URL, a screenshot, and roughly when it started, and I'll dig in right away.

Alex
Pharos Support
```

### H-02 · recurring lessons

*Leo Martins, Martins Guitar School (Team)*  
**high** · calendar_sync · neutral · macro M06 · tags: calendar_sync, double_booking

> Is there a way for students to book the same slot every week for a semester? Booking 16 separate lessons is a pain for parents.

**Draft reply:**

```
Hi Leo,

I'm really sorry about the double booking. That's exactly what Pharos is supposed to prevent, and I understand how frustrating it is in front of your clients.

I'm pulling the sync log for [[fill in: staff name]]'s calendar now. In the meantime, these are the most common causes, and it's worth a 2-minute check:

1. The calendar event is set to "Free" instead of "Busy." Only Busy events block the booking page.
2. The calendar holding that event isn't selected under Settings > Calendar sync > Calendars to check.
3. The connection expired (often after a password change). If you see a red "Reconnect" banner in Settings > Calendar sync, click it and sign in again.

I'll follow up today with what the log shows and what we're doing about it.

Guide: https://help.pharos.example/calendar-sync

Alex
Pharos Support
```

### H-06 · confirmation emails going to spam

*Sofia Reyes, Reyes Brow Bar (Team)*  
**high** · reminders · neutral · macro M07 · tags: reminders, sms

> A couple of clients told me the appointment emails from you are landing in their junk folder. Is there anything I can do on my end?

**Draft reply:**

```
Hi Sofia,

Thanks for flagging this, and I'm sorry about the no-shows. Since email reminders are still going out, this is almost always an SMS-specific setting. I'm checking your account now. Here's what I'm looking at:

1. Whether a monthly SMS cap is set under Settings > Reminders > SMS limit. Once it's reached, texts stop until next month.
2. The delivery status in Clients > [client] > Messages (Sent, Delivered, Failed, or Opted out).
3. Whether clients replied STOP, which unsubscribes them from all texts.

If you can send a screenshot of the Messages tab for one patient who didn't get a text, that will speed things up.

Guide: https://help.pharos.example/reminders

Alex
Pharos Support
```

### H-09 · texts at 3am?!

*Dre Washington, Cuts by Dre (Team)*  
**high** · reminders · negative · macro M07 · tags: reminders, sms

> Three of my clients got reminder texts at 3 in the morning last night. One of them was pretty mad at me. This is embarrassing. What happened and how do I make sure it never happens again?

**Draft reply:**

```
Hi Dre,

Thanks for flagging this, and I'm sorry about the no-shows. Since email reminders are still going out, this is almost always an SMS-specific setting. I'm checking your account now. Here's what I'm looking at:

1. Whether a monthly SMS cap is set under Settings > Reminders > SMS limit. Once it's reached, texts stop until next month.
2. The delivery status in Clients > [client] > Messages (Sent, Delivered, Failed, or Opted out).
3. Whether clients replied STOP, which unsubscribes them from all texts.

If you can send a screenshot of the Messages tab for one patient who didn't get a text, that will speed things up.

Guide: https://help.pharos.example/reminders

Alex
Pharos Support
```

### H-03 · Outlook events not blocking my availability

*Imani Wright, Wright Wellness (Team)*  
**normal** · booking_setup · neutral · macro M09 · tags: booking_setup, booking_page_error

> I connected my Microsoft 365 calendar last week. My Pharos appointments show up in Outlook fine, but my Outlook meetings aren't blocking time on my booking page. Nobody has booked over them yet but I'm nervous.

**Draft reply:**

```
Hi Imani,

Sorry your booking page isn't loading. Let's get it back up. A few quick checks:

1. Status page: https://status.pharos.example shows any active incidents.
2. Account status: a paused or past-due account shows "This business isn't taking bookings right now."
3. Try the page in a private browser window to rule out extensions.

If it still fails, please reply with the page URL, a screenshot, and roughly when it started, and I'll dig in right away.

Alex
Pharos Support
```

### H-04 · too many attempts

*Paul Grady, Grady HVAC (Solo)*  
**normal** · account_access · neutral · macro M11 · tags: account_access, password_reset

> It says too many attempts and won't let me in. I have a customer coming in 20 minutes and need to see what job it is.

**Draft reply:**

```
Hi Paul,

Sorry you're stuck. Reset emails come from security@pharos.example and only go to the exact email your login was created with, so if you signed up with an older address, the email went there.

Try requesting the reset using your other email address. The link expires after 1 hour, so use it right away. If you no longer have access to that inbox, reply from it if you can, or let me know and I'll walk you through verifying your account.

Guide: https://help.pharos.example/account-security

Alex
Pharos Support
```

### H-05 · Nonprofit pricing?

*Ruth Okafor, Eastside Free Clinic (Trial)*  
**normal** · presales · neutral · macro M20 · tags: presales, trial

> We're a volunteer-run free clinic (501c3). Is there any discount for nonprofits before we commit to a plan?

**Draft reply:**

```
Hi Ruth,

So glad you're enjoying the trial! Happy to help you pick the right plan.

[[fill in: answers]]

You can compare plans here: https://help.pharos.example/plans-and-pricing. And if you pay annually, you get two months free.

Any other questions, just reply here.

Alex
Pharos Support
```

### H-07 · close account

*Walt Hughes, Hughes Bike Repair (Solo)*  
**normal** · cancellation · positive · macro M04 · tags: cancellation

> Retiring at the end of the year. Please close my account and delete everything when the time comes. Thanks for the good service.

**Draft reply:**

```
Hi Walt,

Thanks for reaching out. The Cancel plan option only shows up for the account owner, which is probably why you can't find it. Staff and admin logins don't have billing access.

The account owner can cancel in a few clicks:
1. Log in and go to Settings > Billing > Cancel plan.
2. Pick a reason and confirm.
3. The plan stays active until the end of the current billing period.

If the owner prefers, they can reply to this email from the owner's email address and I'll take care of it for them.

Full guide: https://help.pharos.example/change-or-cancel-plan

Best,
Alex
Pharos Support
```

### H-08 · refund a patient's deposit

*Mei Chen, Chen Acupuncture (Team)*  
**normal** · payments · neutral · macro M10 · tags: payments, deposit

> A patient had a family emergency and I want to give back her $40 deposit. Can you refund it to her? We use Square.

**Draft reply:**

```
Hi Mei,

Thanks for the details. Since Stripe shows Connected, there are two usual reasons a deposit gets skipped:

1. Deposits are set per service. Open Services > [[fill in: service name]] and make sure "Require payment at booking" is turned on.
2. Bookings added by your team from the calendar skip payment by design. Only bookings clients make on the booking page collect a deposit.

For this Friday's appointment, you can send the client a payment link from the appointment, or turn on Card on file so you can charge a no-show fee.

Guide: https://help.pharos.example/deposits-and-payments

Alex
Pharos Support
```

### H-10 · embed not showing on squarespace

*Ava Lindqvist, Lindqvist Interior Design (Plus)*  
**normal** · payments · neutral · macro M10 · tags: payments, deposit

> I pasted the embed code into a code block on my Squarespace site but nothing shows up, just a blank space.

**Draft reply:**

```
Hi Ava,

Thanks for the details. Since Stripe shows Connected, there are two usual reasons a deposit gets skipped:

1. Deposits are set per service. Open Services > [[fill in: service name]] and make sure "Require payment at booking" is turned on.
2. Bookings added by your team from the calendar skip payment by design. Only bookings clients make on the booking page collect a deposit.

For this Friday's appointment, you can send the client a payment link from the appointment, or turn on Card on file so you can charge a no-show fee.

Guide: https://help.pharos.example/deposits-and-payments

Alex
Pharos Support
```

### H-11 · Billed for wrong plan

*Ray Dominguez, Dominguez Mobile Detailing (Team)*  
**normal** · billing · neutral · macro M22 · tags: billing, sms_overage

> We're on the Team plan but this month's invoice charged us $99 for Plus. We never upgraded. Please correct it.

**Draft reply:**

```
Hi Ray,

I understand the surprise, and I'm sorry it wasn't clearer. Here's what happened: your Team plan includes 1,000 SMS reminders a month. Texts beyond that are $0.02 each, and last month's extra texts were added to this invoice.

To make sure it doesn't happen again:
1. Set a monthly cap under Settings > Reminders > SMS limit. Texts stop when you hit it.
2. Send one reminder per appointment instead of two, or keep texts under 160 characters (longer ones count as two messages).

[[fill in: credit line]]

Guide: https://help.pharos.example/plans-and-pricing

Alex
Pharos Support
```

### H-12 · Login I don't recognize

*Beth Sorensen, Sorensen Counseling (Plus)*  
**normal** · account_access · neutral · macro M11 · tags: account_access, password_reset

> Under recent activity I see a login from another country at 2am yesterday. That wasn't me or anyone on my team. What should I do?

**Draft reply:**

```
Hi Beth,

Sorry you're stuck. Reset emails come from security@pharos.example and only go to the exact email your login was created with, so if you signed up with an older address, the email went there.

Try requesting the reset using your other email address. The link expires after 1 hour, so use it right away. If you no longer have access to that inbox, reply from it if you can, or let me know and I'll walk you through verifying your account.

Guide: https://help.pharos.example/account-security

Alex
Pharos Support
```
