---
title: Appointment reminders (SMS and email)
slug: reminders
category: Reminders
---

# Appointment reminders (SMS and email)

Reminders are the easiest way to cut no-shows. Businesses that turn on SMS reminders see about a third fewer no-shows.

## Turn on reminders

Go to **Settings > Reminders**. Email reminders are on by default. Turn on SMS reminders and choose when they go out: 48 hours, 24 hours, or 2 hours before the appointment (you can pick more than one).

## Edit reminder messages

Click **Edit template** next to each reminder. You can use placeholders like `{client_first_name}`, `{service}`, `{date}`, `{time}`, and `{reschedule_link}`. SMS messages over 160 characters count as two messages.

## SMS reminders aren't being delivered

Check these in order:

1. **SMS is turned on** under **Settings > Reminders**.
2. **You haven't hit your SMS limit.** If you set a monthly SMS cap, reminders stop once you hit it. See your usage under **Settings > Reminders > Usage**.
3. **The client's number is valid** and includes the country code for numbers outside the US and Canada.
4. **The client didn't opt out.** If a client replies STOP to any Pharos text, they're unsubscribed from all texts and we can't override that. They can reply START to opt back in.
5. **The appointment was booked after the reminder time.** If someone books 1 hour ahead, the 24-hour reminder won't send.

## Delivery log

Every reminder has a delivery status under **Clients > [client name] > Messages**: Sent, Delivered, Failed, or Opted out. Include a screenshot of this log if you contact support.

## Email reminders going to spam

Ask clients to add `reminders@pharos.example` to their contacts. On the Plus plan, you can send email reminders from your own domain under **Settings > Reminders > Sender domain**.
