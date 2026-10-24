---
title: Deposits and payments
slug: deposits-and-payments
category: Payments
---

# Deposits and payments

Pharos can collect deposits or full payment when clients book, through Stripe or Square. Pharos doesn't hold your money. Payments go straight to your Stripe or Square account.

## Connect Stripe or Square

Go to **Settings > Payments > Connect** and sign in to Stripe or Square. You can connect one payment provider at a time.

## Require a deposit

Open a service under **Services**, turn on **Require payment at booking**, and choose a fixed deposit (for example, $25) or a percentage of the price. Clients can't complete the booking until the deposit is paid.

## No-show and late-cancellation fees

Turn on **Card on file** under **Settings > Payments**. Clients enter a card when they book but aren't charged. If they no-show or cancel inside your cancellation window, open the appointment and click **Charge fee**. You must state the fee on your booking page; Pharos adds your policy text automatically.

## Refunding a client's deposit

Open the appointment and click **Refund deposit**. Refunds go back through Stripe or Square. Pharos support can't refund your clients' payments for you, because the money is in your payment account, not ours.

## Deposit wasn't collected

1. Check that **Settings > Payments** says *Connected* in green. If it says *Action needed*, Stripe or Square needs more information from you; log in to their dashboard.
2. Check that the service has **Require payment at booking** turned on. The setting is per service.
3. Bookings you add yourself from the calendar skip payment by design. Only bookings clients make on the booking page collect a deposit.

## Payment processing fees

Stripe and Square charge their own processing fees. Pharos doesn't add any extra fee on payments.
