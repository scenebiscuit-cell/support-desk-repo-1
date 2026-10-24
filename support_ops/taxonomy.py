"""Ticket categories, priorities, and the keyword rules used by the offline engine."""
from __future__ import annotations

CATEGORIES = {
    "billing": "Invoices, charges, payment methods, SMS overage, plan prices",
    "refund": "Customer wants money back: duplicate charge, annual plan refund",
    "cancellation": "Wants to cancel, close the account, or is leaving for a competitor",
    "calendar_sync": "Google/Outlook sync, double bookings, availability not blocked",
    "reminders": "SMS or email reminders not sending, reminder templates",
    "booking_setup": "Booking page, services, availability, time zone, wrong appointment times",
    "payments": "Stripe/Square, deposits, card on file, no-show fees for the business's clients",
    "account_access": "Can't log in, password reset, 2FA, locked account",
    "staff": "Staff invites, roles, plan seat limits, ownership transfer",
    "data_privacy": "Data export, client data deletion, account deletion, privacy questions",
    "outage": "Pharos is down or broken for many users at once",
    "security": "Vulnerability report, suspicious activity, compromised account",
    "feature_request": "Asking for a feature that doesn't exist",
    "presales": "Trial or prospective customer asking questions before buying",
    "feedback": "Praise or general feedback with no problem to solve",
    "spam": "Vendor pitches, marketing, not a real support request",
}

PRIORITIES = ["low", "normal", "high", "urgent"]

# Default priority before modifiers are applied.
DEFAULT_PRIORITY = {
    "outage": "urgent", "security": "urgent",
    "calendar_sync": "high", "reminders": "high",
    "feature_request": "low", "feedback": "low", "spam": "low",
}

# Keyword rules: (phrase, weight). Phrases are matched against lowercase text.
KEYWORDS: dict[str, list[tuple[str, float]]] = {
    "refund": [("refund", 3), ("charged twice", 4), ("double charge", 4), ("duplicate charge", 4),
               ("charged me", 1.5), ("money back", 3), ("twice", 1)],
    "billing": [("invoice", 2), ("bill", 2), ("overage", 3), ("charge", 1), ("payment method", 2),
                ("card declined", 3), ("receipt", 2), ("price", 1), ("$", 0.5)],
    "cancellation": [("cancel", 3), ("cancel our subscription", 3), ("switch to", 2), ("switching", 2),
                     ("moving to another", 3), ("close my account", 3), ("different booking app", 3),
                     ("other booking tools", 1)],
    "calendar_sync": [("double book", 4), ("google calendar", 3), ("outlook", 3), ("sync", 3),
                      ("same slot", 2), ("same time slot", 1)],
    "reminders": [("reminder", 3), ("text message", 2), ("texts", 1), ("sms", 1.5), ("no-show", 1)],
    "booking_setup": [("booking page", 1.5), ("time zone", 4), ("timezone", 4), ("hour early", 4),
                      ("an hour", 2), ("confirmation email said", 3), ("wrong time", 4), ("availability", 2),
                      ("times different", 3), ("came early", 3)],
    "payments": [("deposit", 4), ("stripe", 3), ("square", 3), ("no-show fee", 3), ("card on file", 3)],
    "account_access": [("log in", 3), ("login", 3), ("password", 3), ("locked out", 4), ("2fa", 4),
                       ("6 digit code", 4), ("backup code", 3), ("two-factor", 4), ("can't sign in", 4)],
    "staff": [("stylist", 2), ("invite", 2), ("staff", 2), ("reached my limit", 4), ("owner", 2),
              ("ownership", 4), ("admin", 1.5), ("take over account", 4), ("new hire", 2)],
    "data_privacy": [("delete", 2.5), ("personal information", 3), ("export", 3), ("gdpr", 4),
                     ("privacy", 3), ("my data", 2), ("client info", 1.5)],
    "outage": [("is pharos down", 6), ("down??", 4), ("error page", 3), ("all three of our locations", 3),
               ("everyone", 1), ("outage", 5), ("not loading", 2)],
    "security": [("xss", 6), ("vulnerability", 6), ("security issue", 5), ("exploit", 5),
                 ("hacked", 5), ("suspicious login", 5), ("steps to reproduce", 2)],
    "feature_request": [("any chance you'll add", 5), ("feature request", 5), ("would love if", 4),
                        ("please add", 4), ("waitlist", 3), ("do you plan", 3), ("roadmap", 3)],
    "presales": [("trial", 3), ("before i pay", 4), ("before i pick a plan", 4), ("do you support", 2),
                 ("considering", 2), ("thinking about signing up", 4)],
    "feedback": [("thank you!", 3), ("just wanted to say thanks", 6), ("great product", 4), ("love it", 2)],
    "spam": [("seo", 4), ("first-page google", 5), ("partnership opportunity", 4), ("free audit", 5),
             ("reply yes", 4), ("10x", 3), ("guarantee", 2)],
}

URGENCY_WORDS = ["asap", "urgent", "immediately", "right now", "today", "tomorrow", "can't see my schedule",
                 "customers are calling", "clients showed up", "showed up"]
NEGATIVE_WORDS = ["ridiculous", "frustrat", "unacceptable", "again", "terrible", "worst", "disappointed",
                  "burned", "angry", "annoy", "no idea", "seriously", "??", "sorry for the trouble"]
POSITIVE_WORDS = ["love", "loving", "thank you", "thanks", "great", "awesome", "amazing", "appreciate"]
CHURN_WORDS = ["looking at other", "switch to", "switching", "moving to another", "different booking app",
               "cancel", "competitor", "leaving"]
