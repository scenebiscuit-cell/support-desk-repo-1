# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Support agents exploring a help-desk demo and end users seeking answers in its public help portal.

## Product Purpose

Pharos Support Desk demonstrates support operations for Pharos, a fictional project-management app for small teams, alongside an end-user portal for finding source-grounded help-center answers.

## Positioning

The support-operations demo pairs AI-assisted chat and ticket triage with visible knowledge sources, a rules-based baseline, and editable support macros. The public portal presents only the help chat and a concise explanation of how it works.

## Operating Context

Support agents explore sample and holdout support tickets, search help content, review triage recommendations, and inspect reply macros. End users ask questions in the public portal and inspect the cited help-center passage.

## Capabilities and Constraints

- The site includes chat, ticket triage, macros, and a guide to the demo's workflow.
- `/portal/` is a public, chat-only end-user surface with a short “How it works” section; it must not expose ticket, triage, or macro data.
- Cloud AI requests go to the Pharos Cloudflare Worker; the app also supports its existing offline and sample modes.
- The public portal may answer only from help-center excerpts and must not imply real account access or support-ticket creation.
- Demo ticket data is fictional and must remain clearly labeled as such.
- Preserve the existing content, request/response behavior, keyboard access, responsive layout, and reduced-motion support.

## Brand Commitments

The product is named Pharos. The lighthouse is its explicit guiding metaphor.

## Evidence on Hand

The repository contains the working demo, support knowledge base, sample and holdout tickets, triage results, and macros. Ticket data is labeled fictional; no customer testimonials or commercial claims are established.

## Product Principles

- Keep support tasks clear and easy to scan.
- Show the knowledge sources behind answers.
- Preserve human review and editing of AI-assisted triage and drafts.
- Distinguish demonstrations and fictional data from real customer outcomes.
