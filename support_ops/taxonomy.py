"""Ticket categories, priorities, and the keyword rules used by the offline engine."""
from __future__ import annotations

CATEGORIES = {
    "billing": "Invoices, seat charges, prorated charges, payment methods, failed payments, plan prices",
    "refund": "Customer wants money back: duplicate charge, wrong plan charged, annual plan refund",
    "cancellation": "Wants to cancel, close the workspace, or is leaving for a competitor",
    "integrations": "Slack, GitHub, Google Drive, calendar sync, Zapier not connecting or syncing",
    "notifications": "Email, in-app, or Slack notifications missing, too many, or going to spam",
    "workspace_setup": "Projects, boards, templates, custom fields, private projects, due dates and time zones",
    "bug": "Something in the product isn't working as expected: missing tasks, failed uploads, errors",
    "account_access": "Can't log in, password reset, 2FA, locked account, SSO",
    "seats": "Inviting members or guests, member limits, roles, ownership transfer",
    "data_privacy": "Data export or import, personal data deletion requests, workspace deletion, privacy",
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
    "feature_request": "low", "feedback": "low", "spam": "low",
}

# Keyword rules: (phrase, weight). Phrases are matched against lowercase text.
KEYWORDS: dict[str, list[tuple[str, float]]] = {
    "refund": [("refund", 3), ("charged twice", 4), ("double charge", 4), ("duplicate charge", 4),
               ("charged us", 1.5), ("charged me", 1.5), ("money back", 3), ("twice", 1)],
    "billing": [("invoice", 2), ("bill", 2), ("prorated", 3), ("charge", 1), ("payment method", 2),
                ("card declined", 3), ("payment failed", 3), ("receipt", 2), ("price", 1), ("$", 0.5),
                ("read-only", 2)],
    "cancellation": [("cancel", 3), ("cancel our subscription", 3), ("switch to", 2), ("switching", 2),
                     ("moving to another", 3), ("close my account", 3), ("close our workspace", 3),
                     ("different tool", 3), ("other tools", 1)],
    "integrations": [("slack", 3), ("github", 3), ("google drive", 3), ("zapier", 3), ("integration", 3),
                     ("reconnect", 2), ("google calendar", 3), ("outlook", 2), ("sync", 2), ("webhook", 2)],
    "notifications": [("notification", 3), ("notified", 2), ("digest", 2), ("@mention", 2), ("mentioned", 1.5)],
    "workspace_setup": [("template", 3), ("time zone", 4), ("timezone", 4), ("due date", 2), ("a day early", 4),
                        ("day earlier", 4), ("custom field", 3), ("private project", 3), ("recurring task", 3),
                        ("columns", 1)],
    "bug": [("disappeared", 4), ("vanished", 4), ("missing", 2), ("bug", 3), ("upload failed", 4),
            ("won't upload", 4), ("glitch", 3), ("broken", 2), ("error when", 2)],
    "account_access": [("log in", 3), ("login", 3), ("password", 3), ("locked out", 4), ("2fa", 4),
                       ("6 digit code", 4), ("backup code", 3), ("two-factor", 4), ("can't sign in", 4),
                       ("too many attempts", 4)],
    "seats": [("invite", 2), ("member limit", 4), ("seat", 2), ("owner", 2), ("ownership", 4), ("admin", 1.5),
              ("take over account", 4), ("guest", 2), ("new hire", 2)],
    "data_privacy": [("delete", 2.5), ("personal information", 3), ("personal data", 3), ("export", 3),
                     ("gdpr", 4), ("privacy", 3), ("my data", 2)],
    "outage": [("is pharos down", 6), ("down??", 4), ("502", 3), ("won't load for anyone", 5),
               ("anyone on our team", 2), ("outage", 5), ("not loading", 2)],
    "security": [("xss", 6), ("vulnerability", 6), ("security issue", 5), ("exploit", 5),
                 ("hacked", 5), ("suspicious login", 5), ("steps to reproduce", 2)],
    "feature_request": [("any chance you'll add", 5), ("feature request", 5), ("would love if", 4),
                        ("please add", 4), ("dependencies", 3), ("do you plan", 3), ("roadmap", 3)],
    "presales": [("trial", 3), ("before i pay", 4), ("before i pick a plan", 4), ("before we pick a plan", 4),
                 ("do you support", 2), ("considering", 2), ("evaluating", 3)],
    "feedback": [("thank you!", 3), ("just wanted to say thanks", 6), ("great product", 4), ("love it", 2)],
    "spam": [("seo", 4), ("first-page google", 5), ("partnership opportunity", 4), ("free audit", 5),
             ("reply yes", 4), ("10x", 3), ("guarantee", 2)],
}

URGENCY_WORDS = ["asap", "urgent", "immediately", "right now", "today", "tomorrow", "missed two deadlines",
                 "missed a deadline", "due tomorrow", "sitting here", "in 20 minutes", "clients are waiting"]
NEGATIVE_WORDS = ["ridiculous", "frustrat", "unacceptable", "again", "terrible", "worst", "disappointed",
                  "furious", "angry", "annoy", "no idea", "seriously", "??", "sorry for the trouble"]
POSITIVE_WORDS = ["love", "loving", "thank you", "thanks", "great", "awesome", "amazing", "appreciate"]
CHURN_WORDS = ["looking at other", "switch to", "switching", "moving to another", "different tool",
               "cancel", "competitor", "leaving"]


# Security safety net: reports of a login or activity the customer doesn't recognize always go to security
# (urgent, a person first), whatever the keyword rules or an AI model decided. Added after both engines
# routed two such unseen tickets (H-12, H-35) as ordinary login problems. Lowercase regular expressions;
# the page uses the same list (build_demo.py passes it through), so keep them JavaScript-compatible.
SECURITY_OVERRIDE = [
    r"\blog ?ins? (?:i|we) (?:don'?t|do not|didn'?t|did not) recogni[sz]e",
    r"\b(?:log ?in|logged in|sign[- ]?in|signed in)s? from (?:another|a different|a foreign|an unknown|a strange) (?:country|location|city|device)",
    r"\bsomeone (?:else )?(?:has )?(?:logged|signed) (?:in|into)",
    r"\bunrecogni[sz]ed (?:log ?in|sign[- ]?in|device|location)",
    r"\bsuspicious (?:log ?in|sign[- ]?in|activity)",
]
