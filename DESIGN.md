---
name: Pharos Support Desk
description: A lighthouse-guided support operations demo for finding answers and reviewing ticket work.
colors:
  lapis-night: "#0c1f4a"
  lapis: "#14397a"
  deep-ocean: "#0a4766"
  band-ink: "#ffffff"
  gold: "#ebc874"
  papyrus: "#ebdfc9"
  sheet: "#f6eedf"
  tint: "#f0e5d1"
  ink: "#1d1f2a"
  muted-ink: "#5b5547"
  rule: "#d5c4a3"
  lapis-action: "#1d4f91"
  lapis-soft: "#e0e8f4"
  pass-green: "#1f7a46"
  warn-amber: "#a15c00"
  fail-red: "#b4261b"
  dark-lapis-night: "#07163a"
  dark-lapis: "#0d2a5a"
  dark-ocean: "#072f48"
  dark-gold: "#e6c36a"
  dark-paper: "#0a0f1c"
  dark-sheet: "#111829"
  dark-tint: "#161e33"
  dark-ink: "#ebe6d9"
  dark-muted: "#a39e90"
  dark-rule: "#263049"
  dark-action: "#8fb3ec"
  dark-action-soft: "#1a2a4d"
typography:
  display:
    fontFamily: '"IBM Plex Sans Condensed", "Arial Narrow", "Helvetica Neue", Arial, sans-serif'
    fontSize: "clamp(34px, 5.2vw, 56px)"
    fontWeight: 700
    lineHeight: 1
  body:
    fontFamily: '"IBM Plex Sans", "Helvetica Neue", Arial, sans-serif'
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: '"IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace'
    fontSize: "11.5px"
    fontWeight: 500
    letterSpacing: ".09em"
rounded:
  sm: "4px"
  md: "8px"
  pill: "999px"
spacing:
  compact: "8px"
  standard: "16px"
  section: "24px"
components:
  button-primary:
    backgroundColor: "{colors.lapis-action}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "9px 18px"
  pane:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
---

# Design System: Pharos Support Desk

## Overview

**Creative North Star: "The lighthouse of Alexandria over open water."**

Pharos takes its name from the lighthouse of Alexandria, so the palette is ocean and ancient Egypt: lapis lazuli and deep-ocean blues, Egyptian gold, and a papyrus page. The masthead is a plain lapis-to-ocean gradient (no grid) with a quiet animated gold wireframe sea whose swells roll slowly toward the reader, with occasional light spray. The sea fades out behind the headline so text stays easy to read, and a "Pause waves" control sits inline at the end of the masthead eyebrow, styled like the eyebrow (gold mono caps in a thin pill), and stops it (remembered per visitor). The lighthouse's beam sweeps across the water and turns toward the mouse while the pointer is over the masthead.

Below the masthead the page is a calm operations console: a frosted sticky tab bar, then each tool as a pair of panels (the work on the left, the "why" on the right). The agent demo (`index.html`, `demo/`) and the public help portal (`portal/`) share this system.

**Key Characteristics:**
- Lapis-to-ocean gradient masthead (no grid lines) with a subtle canvas wave animation; the Pause waves control is inline in the eyebrow line.
- Lighthouse mark beside the product name; its lamp is the beam's origin.
- Papyrus page, off-white panels, 2px ink rules under section and panel headings.
- Gold is for the masthead and highlights; lapis carries actions and selection.

## Colors

### Primary
- **Lapis** (#14397a), **Lapis Night** (#0c1f4a), **Deep Ocean** (#0a4766): the masthead gradient.
- **Gold** (#ebc874): masthead eyebrow, headline numbers, wave lines, beam, lighthouse bands.
- **Lapis Action** (#1d4f91): primary buttons, links, active tab, user chat bubbles.
- **Lapis Soft** (#e0e8f4): selected controls and focus halos.

### Semantic (unchanged by the theme)
- **Pass** (#1f7a46), **Warn** (#a15c00), **Fail** (#b4261b): verdict stamps, priorities, handoffs. Category tags keep their own hues; the turquoise "account" tag doubles as Egyptian faience.

### Neutral
- **Sand** (#ebdfc9): page ground. **Sheet** (#f6eedf, warm off-white sand): panels. **Tint** (#f0e5d1): inputs, chips, bot bubbles. No pure white surfaces in the light theme; keep it calm and beachy.
- **Ink** (#1d1f2a), **Muted Ink** (#5b5547, warm driftwood), **Rule** (#d5c4a3).

### Dark theme
Night-sea navy page (#0a0f1c) and panels (#111829), warm parchment text (#ebe6d9), a darker lapis masthead, the same gold (#e6c36a), and a light lapis action color (#8fb3ec).

### Named Rules
**The Gold Rule.** Gold lives in the masthead and in highlights (headline numbers, the live marker). It never carries body text on a light background.

**The Lapis Rule.** Lapis carries actions and selected state everywhere below the masthead.

## Typography

**Display Font:** IBM Plex Sans Condensed. **Body Font:** IBM Plex Sans. **Label/Mono Font:** IBM Plex Mono.

### Hierarchy
- **Headline** (700, clamp 34–56px, line-height 1): product name in the masthead.
- **Section** (700, 26px) with a muted subtitle, over a 2px ink rule.
- **Panel title** (700, 21px) over a 2px ink rule.
- **Body** (400, 15px, 1.5).
- **Label** (500–600, 11–11.5px mono, tracked uppercase): eyebrows, speaker labels, metadata.

## Layout

Centered 1240px container (920px for the portal) with 16px safe-area-aware gutters. The masthead holds the eyebrow, lighthouse and headline, tagline, credit row, and headline stats. A frosted sticky nav holds the section tabs, command palette (Ctrl K) and theme switch. Chat and triage use two panels on wide screens and stack on phones.

## Motion

- **Wave sea:** canvas perspective mesh, 17 rows, slow swell; low-contrast lines (alpha .06–.26), a small forward lean on near crests, sparse spray (capped at 70). Masked to fade toward the text side. Keep it quiet: it's background, not content. Color is read from `--band-hi`, so it follows the theme.
- **Sea life (`shared/sea-life.js`):** every 7–13 s, one wireframe fish (outline, spine, ribs, fin, eye; gold ink at about half opacity) jumps in an arc on the right side of the water, or a splash bursts. Each entry and exit throws a few droplets and two flat ripple rings. One event at a time; none for reduced motion or while paused.
- **Beam:** radial-gradient wedge from the lighthouse lamp; sweeps on its own, eases toward the mouse while the pointer is over the masthead (fine pointers only).
- Pauses when the masthead is off screen, the tab is hidden, or the visitor clicks Pause waves (WCAG 2.2.2). Reduced-motion users get one still frame and no button.

## Components

- **Buttons:** 8px radius, 1.5px rule border, 700 weight; primary is lapis fill. Masthead buttons are translucent pills with a gold border.
- **Chips and pills:** mono, pill-shaped, tint fill with a rule border; priorities use solid semantic fills.
- **Panels:** sheet fill, 1px rule, 8px radius, light shadow; header has a 2px ink rule.
- **Chat:** bot bubbles are tint with a 4px lapis left edge; handoffs switch to the warn colors; user bubbles are solid lapis.
- **Verdict stamps:** bordered blocks with a 5px top edge in the semantic color.

## How it works tab

- **Flow steps:** 16px-radius cards with a soft lapis tint fading into the sheet, a numbered badge (gold numeral on a lapis disc), and a 2px lift on hover. "Review" is gold-tinted with a gold badge; "Out" is ocean-tinted. Two columns on phones.
- **Notes as bento cards:** sheet cards with a 3px lapis → ocean → gold top line and a small gold dot before each heading.
- **Feature card ("Try both sides"):** the masthead's lapis-and-ocean gradient with a faint gold glow, gold heading, and a gold primary button, so the hands-on demo stands out.

## Service desk (Jira Service Management model)

- **Agent desk issue view:** two columns. Main: header (key · channel · plan), a conversation timeline (customer messages on tint, agent replies with a 4px lapis edge, internal notes on warn-soft with a dashed border, system events as small mono lines), the verdict stamp, the macro note, then the composer with **Reply to customer** / **Add internal note** tabs. Sidebar on tint: status select, assignee, SLA box (left edge green/amber/red), request details, labels, knowledge base with "Share with customer". Stacks below 1100px.
- **Status lozenges:** small mono caps. Waiting for support = info, In progress = lapis, Waiting for customer = warn, Resolved/Closed = pass.
- **Portal:** a pill nav (Ask the Keeper · Contact support · My requests with a gold count badge), a request form in a card, suggested articles in a dashed lapis box, and My requests as a list then a thread. Customers never see internal notes.
- **SLA targets** come from the Contact support article: Business 4 business hours, Team 1 business day, Free 2 business days, outages and security around the clock (clock hours in the demo).

## Responsive rules (phones)

- Header stats sit in a 3-column row; the tagline drops to 15px. On phones the eyebrow shortens to "AI help desk demo" and Pause waves becomes just a gold ❚❚ / ▶ icon (36px tap area) at the right end of that line; the label stays as its accessible name.
- Sticky nav: tabs scroll sideways with a fade hint; the Ctrl K palette is hidden (keyboard feature) and "Portal ↗" stays visible.
- Agent desk: the queue switcher is a 2x2 grid; tapping a ticket scrolls to it, with "Back to the queue".
- Suggested questions scroll sideways in one row so the conversation stays in view.
- Tap targets are at least 40px tall on touch or narrow screens; inputs are 16px so iOS doesn't zoom on focus.
- Portal nav uses short labels (Ask · Contact · My requests) in three equal segments.

## Do's and Don'ts

### Do:
- **Do** keep AI answers, sources, ticket state, and human-review boundaries easy to identify.
- **Do** keep the masthead art decorative (`aria-hidden`) and out of the focus order.
- **Do** honor reduced motion and keep every control usable without a mouse.
- **Do** keep the agent demo and portal visually identical in palette and type.

### Don't:
- **Don't** reintroduce the old teal/mint palette or Bricolage Grotesque.
- **Don't** use gold for text on papyrus or white.
- **Don't** put ticket, triage, or macro data on the public portal.
- **Don't** invent real-world customers, metrics, or outcomes for the fictional demo.
