---
version: 1
slug: "portal-index-html"
primary_target: "portal/index.html"
related_targets: ["portal/template.html"]
---

## Scope and visitor mode
Public end-user help portal at `/portal/`; Operate.

## Audience and task
Pharos customers (a project-management app for small teams) want a reliable answer; ask in plain language, verify the cited help content, and find the documented support contact when the articles do not answer.

## Content and proof
The portal searches the existing public help-center articles, sends relevant excerpts to the same grounded chat Worker, and reveals the cited passage inside the conversation. A short “How it works” section explains this demo.

## Constraints
Show only chat and the brief explainer; do not ship ticket, macro, triage, or staff data. Do not imply this demo creates tickets, accesses accounts, or connects to a real Pharos support team. Preserve the lighthouse design, system light/dark theme, responsive layout, keyboard access, and reduced-motion behavior. Warn users not to enter passwords or payment details.

## Chosen direction
One centered, single-column help conversation under the same lapis-and-gold wave masthead as the agent demo; the source passage expands within each answer, with a link to the full article, and the explainer sits below the chat.

## Memorable moment
A visitor can open an answer’s source and verify the exact help-center passage without leaving the conversation.

## Unresolved decisions
None.
