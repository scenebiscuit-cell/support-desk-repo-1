# Triage report

Engine: **rules**  ·  Tickets: **20**  ·  Time: 0.0s

- Ready to send after a quick review: **9**
- Need a person to act first (refund, identity check, escalation): **10**
- Spam closed automatically: **1**
- Churn risk flagged: **T-1002, T-1003, T-1019**

**Accuracy vs. hand labels:** category 100%, priority 100%


## Queue (sorted by priority)

| Ticket | Priority | Category | Macro | Human? | Subject |
|---|---|---|---|---|---|
| T-1007 | urgent | outage | M17 | yes | URGENT booking page is down |
| T-1020 | urgent | security | M18 | yes | Security issue in booking page intake form |
| T-1001 | high | refund | M01 | yes | Charged twice this month?? |
| T-1003 | high | calendar_sync | M06 | yes | Double booked AGAIN - this is the third time |
| T-1004 | high | reminders | M07 | no | Text reminders stopped going out |
| T-1006 | high | account_access | M12 | no | Locked out - new phone |
| T-1015 | high | booking_setup | M08 | no | Client came an hour early |
| T-1019 | high | cancellation | M05 | yes | Moving to another tool |
| T-1002 | normal | cancellation | M04 | no | where is the cancel button |
| T-1005 | normal | presales | M20 | yes | Questions before I pay |
| T-1008 | normal | refund | M02 | yes | Refund for annual plan |
| T-1011 | normal | payments | M10 | yes | Deposit wasn't collected |
| T-1012 | normal | staff | M13 | no | Can't add new stylist |
| T-1013 | normal | data_privacy | M15 | no | Client requesting deletion of her information |
| T-1016 | normal | account_access | M11 | no | password reset not working |
| T-1017 | normal | billing | M22 | yes | Why is my bill $95? |
| T-1018 | normal | staff | M14 | no | Need to take over account - previous owner left |
| T-1009 | low | feature_request | M19 | yes | Waitlist? |
| T-1010 | low | spam | M23 | no | Partnership opportunity - 10x your organic traffic |
| T-1014 | low | feedback | M21 | no | Thank you! |

## Drafts

### T-1007 · URGENT booking page is down

*Ben Carter, Carter Auto Care (3 locations) (Plus)*  
**urgent** · outage · negative · macro M17 · tags: outage, incident

> Our booking page has been showing an error page for the last 30 minutes at all three of our locations. Customers are calling us saying they can't book. I checked on my phone and on my laptop, same thing. Is Pharos down??

**Draft reply:**

```
Hi Ben,

Thank you for reporting this so quickly, and I'm sorry. I know every minute your booking page is down costs you bookings. Our engineering team is aware and actively working on it.

You can follow live updates at https://status.pharos.example and subscribe there for an alert the moment it's resolved. I've linked your ticket to the incident, so I'll also update you here directly.

In the meantime, if customers call, you can add their bookings manually from your Pharos calendar if the dashboard is loading for you.

Alex
Pharos Support
```

### T-1020 · Security issue in booking page intake form

*J. Alvarez, Independent researcher (None)*  
**urgent** · security · neutral · macro M18 · tags: security, vulnerability_report

> Hello, I found that the custom intake question field on booking pages doesn't escape HTML, so a script entered as an answer runs when the business views the booking in the dashboard. This looks like stored XSS. I haven't shared this publicly. Happy to send steps to reproduce privately.

**Draft reply:**

```
Hi J.,

Thank you for reporting this responsibly and for keeping it private. I've escalated it to our security team, who will review it as a priority.

Please send the reproduction steps to security@pharos.example rather than replying here, and our security team will follow up with you directly. We'd appreciate you continuing to hold off on public disclosure while we investigate and fix it.

Thanks again for helping keep our customers safe.

Alex
Pharos Support
```

### T-1001 · Charged twice this month??

*Maria Delgado, Brightside Salon (Team)*  
**high** · refund · neutral · macro M01 · tags: refund, duplicate_charge

> Hi, I just looked at my bank statement and Pharos charged me $49 twice on October 3rd. Same amount, same day. I only have one account. Can you please fix this and refund the extra charge? Invoice numbers are PHR-88213 and PHR-88214. Thanks, Maria

**Draft reply:**

```
Hi Maria,

I'm sorry about the double charge, and thanks for sending the invoice numbers. That made it quick to find. I've confirmed the duplicate and refunded the extra charge in full. You'll see it back on your statement in 5 to 7 business days, depending on your bank.

Your plan isn't affected, and you don't need to do anything else. If the refund hasn't shown up by then, reply here and I'll chase it down.

Best,
Alex
Pharos Support
```

### T-1003 · Double booked AGAIN - this is the third time

*Priya Raman, Lotus Pilates Studio (Plus)*  
**high** · calendar_sync · negative · macro M06 · tags: calendar_sync, double_booking, churn_risk

> This is getting ridiculous. Yesterday two clients showed up for the same 6pm slot with my instructor Jess. Jess had a dentist appointment on her Google Calendar at that time too, so she wasn't even supposed to be available. This is the third time this month. I'm paying for your most expensive plan and I'm seriously looking at other booking tools now. I need this fixed today.

**Draft reply:**

```
Hi Priya,

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

### T-1004 · Text reminders stopped going out

*James Whitfield, Whitfield Physio (Team)*  
**high** · reminders · neutral · macro M07 · tags: reminders, sms

> Hello, since about the 15th none of our patients are getting text reminders. Email reminders still work. We've had 4 no-shows this week, which never happens. Nothing changed on our end that I know of. Can you look into it?

**Draft reply:**

```
Hi James,

Thanks for flagging this, and I'm sorry about the no-shows. Since email reminders are still going out, this is almost always an SMS-specific setting. I'm checking your account now. Here's what I'm looking at:

1. Whether a monthly SMS cap is set under Settings > Reminders > SMS limit. Once it's reached, texts stop until next month.
2. The delivery status in Clients > [client] > Messages (Sent, Delivered, Failed, or Opted out).
3. Whether clients replied STOP, which unsubscribes them from all texts.

If you can send a screenshot of the Messages tab for one patient who didn't get a text, that will speed things up.

Guide: https://help.pharos.example/reminders

Alex
Pharos Support
```

### T-1006 · Locked out - new phone

*Tom Becker, Becker Tutoring (Solo)*  
**high** · account_access · neutral · macro M12 · tags: account_access, 2fa_reset, identity_verification

> I got a new phone over the weekend and now I can't log in because the 6 digit code app was on my old phone. I never saved any backup codes. I have sessions booked tomorrow and I can't see my schedule. Please help ASAP.

**Draft reply:**

```
Hi Tom,

I can help you get back in. Because two-factor authentication protects your account, I need to verify it's you before I remove it. Please reply from this email address with:

1. The last 4 digits of the card on file
2. The date of your most recent Pharos invoice

As soon as that checks out, I'll reset 2FA so you can log in, then you can set it up on your new phone under Settings > Account > Security. Be sure to save the backup codes this time. They'll get you in if this happens again.

We will never ask for your password.

Alex
Pharos Support
```

### T-1015 · Client came an hour early

*Rosa Jimenez, Rosa Massage Therapy (Team)*  
**high** · booking_setup · neutral · macro M08 · tags: booking_setup, time_zone

> I'm in Austin. A new client showed up at 9am for a 10am massage and her confirmation email said 9am. My calendar in Pharos says 10. Another client said the same thing last week. Why are the times different?

**Draft reply:**

```
Hi Rosa,

Sorry about the mix-up with your clients. When confirmation times are off by exactly an hour, it's almost always the business time zone setting.

Please check Settings > Business profile > Business time zone. For Austin, it should be Central Time (America/Chicago). If it's set to a different zone, change it and click Save. Existing appointments keep their correct calendar time, and new confirmations will show the right time.

For anyone already booked, I'd suggest a quick note to confirm their time, just in case.

Guide: https://help.pharos.example/getting-started

Alex
Pharos Support
```

### T-1019 · Moving to another tool

*Elena Petrova, Petrova Photography (Team)*  
**high** · cancellation · negative · macro M05 · tags: cancellation, churn_risk

> Honestly the calendar sync issues and the extra text fees have been frustrating, so I'm going to switch to a different booking app next month. I need to get all my client info and appointment history out first. How do I export everything, and then how do I cancel?

**Draft reply:**

```
Hi Elena,

I'm sorry Pharos hasn't been working the way you need, and thank you for telling us why. That feedback goes straight to our product team.

To get your data out:
1. Go to Settings > Data > Export.
2. Export clients, appointments, and payments (pick "All time" for the date range).
3. Large exports are emailed to you as a download link within 15 minutes.

To cancel afterward, go to Settings > Billing > Cancel plan. You keep access until the end of your billing period.

Before you go: if [[fill in: pain point]] is the main issue, I'd be glad to look at it with you. It's often a settings fix. And if you just need a break, you can pause the account for up to 3 months at $5/month and keep everything as it is.

Either way, I'm here to help.

Alex
Pharos Support
```

### T-1002 · where is the cancel button

*Derek Olsen, Fade & Co Barbers (Team)*  
**normal** · cancellation · neutral · macro M04 · tags: cancellation, churn_risk

> I've looked everywhere in settings and there is no cancel option. The shop owner asked me to cancel our subscription because we're switching to the POS system's built-in booking. How do I do it?

**Draft reply:**

```
Hi Derek,

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

### T-1005 · Questions before I pay

*Alicia Moreno, Moreno Yoga (Trial)*  
**normal** · presales · positive · macro M20 · tags: presales, trial

> Hi! I'm on the trial and loving it so far. Two questions before I pick a plan: can I use my own website address for the booking page instead of the pharos one? And do you support group classes where 12 people book the same time slot?

**Draft reply:**

```
Hi Alicia,

So glad you're enjoying the trial! Happy to help you pick the right plan.

[[fill in: answers]]

You can compare plans here: https://help.pharos.example/plans-and-pricing. And if you pay annually, you get two months free.

Any other questions, just reply here.

Alex
Pharos Support
```

### T-1008 · Refund for annual plan

*Grace Kim, Kim Nail Lounge (Team)*  
**normal** · refund · negative · macro M02 · tags: refund, annual_plan

> Hello, I paid for the annual Team plan 12 days ago, but unfortunately I have to close my shop at the end of the month for family reasons. Is it possible to get a refund for the rest of the year? I'm sorry for the trouble. Grace

**Draft reply:**

```
Hi Grace,

Thanks for letting us know, and no need to apologize at all. Because you're within 30 days of your annual payment, you're eligible for a pro-rated refund for the unused part of the year.

Here's what happens next:
1. I'll cancel the annual plan and process the refund for the unused days.
2. The refund will reach your card in 5 to 7 business days.
3. Your booking page stays active until [[fill in: end date]] so you can finish out your current bookings.

If you'd like to keep a copy of your client list, you can export it any time under Settings > Data > Export: https://help.pharos.example/data-export-and-deletion

Wishing you and your family the best,
Alex
Pharos Support
```

### T-1011 · Deposit wasn't collected

*Linda Park, Park Family Dental (Team)*  
**normal** · payments · negative · macro M10 · tags: payments, deposit

> We require a $50 deposit for whitening appointments, but a patient just booked one for Friday and wasn't asked to pay anything. Stripe shows connected. What happened? We've been burned by no-shows on these before.

**Draft reply:**

```
Hi Linda,

Thanks for the details. Since Stripe shows Connected, there are two usual reasons a deposit gets skipped:

1. Deposits are set per service. Open Services > [[fill in: service name]] and make sure "Require payment at booking" is turned on.
2. Bookings added by your team from the calendar skip payment by design. Only bookings clients make on the booking page collect a deposit.

For this Friday's appointment, you can send the client a payment link from the appointment, or turn on Card on file so you can charge a no-show fee.

Guide: https://help.pharos.example/deposits-and-payments

Alex
Pharos Support
```

### T-1012 · Can't add new stylist

*Chris Nguyen, Urban Mane Studio (Team)*  
**normal** · staff · neutral · macro M13 · tags: staff, plan_limit, upsell

> Trying to invite our 11th stylist and it says I've reached my limit. We hired two new people this month. What are my options?

**Draft reply:**

```
Hi Chris,

Congrats on growing the team! The Team plan includes up to 10 staff calendars, so the 11th invite is hitting that limit. You have two options:

1. Upgrade to Plus ($99/month) for unlimited staff, plus multiple locations and priority support. Upgrades take effect immediately and you only pay the pro-rated difference: Settings > Billing > Change plan.
2. Free up a seat: if anyone has left, deactivate them under Team. Deactivated staff don't count toward the limit, and their history is kept.

Guide: https://help.pharos.example/staff-and-permissions

Alex
Pharos Support
```

### T-1013 · Client requesting deletion of her information

*Nadia Hassan, Clear Skin Clinic (Plus)*  
**normal** · data_privacy · neutral · macro M15 · tags: data_privacy, deletion_request

> One of our former clients emailed asking us to delete all of her personal information from our systems, including our booking system. How do we do that in Pharos, and does it remove her from your servers too?

**Draft reply:**

```
Hi Nadia,

Good question, and thanks for handling this carefully. Here's how it works:

1. Open the client in Pharos and click Delete client. This removes their contact details and cancels any future appointments.
2. Past appointments stay in your reports as "Deleted client," with no personal details attached.
3. On our side, deleted data is removed from active systems right away and fully purged from backups within 90 days.

Because Pharos processes client data on your behalf, deleting it in your account is all that's needed. You can let the client know it's been taken care of.

Guide: https://help.pharos.example/data-export-and-deletion

Alex
Pharos Support
```

### T-1016 · password reset not working

*Kevin Shah, Shah CPA (Solo)*  
**normal** · account_access · neutral · macro M11 · tags: account_access, password_reset

> I clicked forgot password like 5 times and never got an email. Checked spam. My login email might be my old gmail though, not sure.

**Draft reply:**

```
Hi Kevin,

Sorry you're stuck. Reset emails come from security@pharos.example and only go to the exact email your login was created with, so if you signed up with an older address, the email went there.

Try requesting the reset using your other email address. The link expires after 1 hour, so use it right away. If you no longer have access to that inbox, reply from it if you can, or let me know and I'll walk you through verifying your account.

Guide: https://help.pharos.example/account-security

Alex
Pharos Support
```

### T-1017 · Why is my bill $95?

*Hannah Lee, Lee Fitness Coaching (Team)*  
**normal** · billing · negative · macro M22 · tags: billing, sms_overage

> My plan is $49 but this month's invoice is $95.20. I see a line for SMS overage. I had no idea texts cost extra. That's almost double what I expected. Can you explain and can I get that taken off?

**Draft reply:**

```
Hi Hannah,

I understand the surprise, and I'm sorry it wasn't clearer. Here's what happened: your Team plan includes 1,000 SMS reminders a month. Texts beyond that are $0.02 each, and last month's extra texts were added to this invoice.

To make sure it doesn't happen again:
1. Set a monthly cap under Settings > Reminders > SMS limit. Texts stop when you hit it.
2. Send one reminder per appointment instead of two, or keep texts under 160 characters (longer ones count as two messages).

[[fill in: credit line]]

Guide: https://help.pharos.example/plans-and-pricing

Alex
Pharos Support
```

### T-1018 · Need to take over account - previous owner left

*Marcus Bell, Bell Veterinary Clinic (Plus)*  
**normal** · staff · neutral · macro M14 · tags: staff, ownership_transfer, identity_verification

> Our practice manager set up our Pharos account and was the owner on it. She left the clinic last month and isn't responding to us. I'm the clinic owner and an admin on the account. How do I get ownership moved to me so I can manage billing?

**Draft reply:**

```
Hi Marcus,

Thanks for explaining. Normally the current owner transfers ownership themselves, but since they've left and aren't reachable, we can handle it for you after a quick verification.

Please reply with one of these showing your name and the business name:
- A business license or registration
- A recent business invoice or bank statement

Once a team lead approves it (usually within one business day), I'll move ownership to your login, since you're already an admin.

Guide: https://help.pharos.example/staff-and-permissions

Alex
Pharos Support
```

### T-1009 · Waitlist?

*Sam Ortiz, Inkwell Tattoo Studio (Team)*  
**low** · feature_request · positive · macro M19 · tags: feature_request

> Love the app. Any chance you'll add a waitlist? When my artists are booked out, people want to get notified if someone cancels. Right now I'm keeping a list in my notes app lol

**Draft reply:**

```
Hi Sam,

Thanks for the idea, and for the kind words! I've logged your request with our product team along with how you'd use it, which really helps them prioritize.

[[fill in: roadmap status]]

You can vote on and follow ideas at https://ideas.pharos.example, and see what we're building at https://ideas.pharos.example/roadmap.

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

*Owen Brooks, Brooks Piano Lessons (Solo)*  
**low** · feedback · positive · macro M21 · tags: feedback, positive

> Just wanted to say thanks. I switched from a paper calendar three months ago and my no-shows have basically disappeared thanks to the text reminders. My students' parents love being able to reschedule themselves. Great product!

**Draft reply:**

```
Hi Owen,

This made our whole team's day. Thank you for taking the time to write! It's great to hear the reminders are cutting your no-shows and that families like rescheduling on their own.

If you ever have a minute, a short review on Capterra or G2 helps other small businesses find us. No pressure at all.

Thanks for being a Pharos customer,
Alex
Pharos Support
```
