---
name: Pharos Support Desk
description: A lighthouse-guided support operations demo for finding answers and reviewing ticket work.
colors:
  sea-deep: "#08232f"
  sea-current: "#104252"
  sea-ink: "#edf7f4"
  sea-muted: "#b2ceca"
  lantern-amber: "#f5bc52"
  lantern-soft: "#f8edcf"
  mist: "#e7f0ed"
  paper: "#fffdf7"
  inset: "#e4eeeb"
  ink: "#102e39"
  muted-ink: "#405d65"
  rule: "#bfd0cd"
  harbor-teal: "#0d6874"
  harbor-teal-soft: "#d7eae6"
  human-green: "#276d56"
  urgent-red: "#a9332b"
  dark-sea: "#081a21"
  dark-surface: "#122a32"
  dark-inset: "#0e222a"
  dark-ink: "#e5f1ee"
  dark-muted: "#afc5c2"
  dark-rule: "#2b474d"
  dark-teal: "#78c7c1"
  dark-teal-soft: "#1d4147"
typography:
  display:
    fontFamily: '"Bricolage Grotesque", "Avenir Next", "Segoe UI", sans-serif'
    fontSize: "clamp(26px, 2.2vw + 14px, 36px)"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-.025em"
  body:
    fontFamily: '"IBM Plex Sans", "Segoe UI", system-ui, sans-serif'
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: '"IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace'
    fontSize: "11px"
    fontWeight: 500
    letterSpacing: ".08em"
rounded:
  sm: "6px"
  md: "8px"
  lg: "12px"
spacing:
  compact: "8px"
  standard: "16px"
  section: "24px"
components:
  button-primary:
    backgroundColor: "{colors.harbor-teal}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "7px 12px"
  pane:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
---

# Design System: Pharos Support Desk

## Overview

**Creative North Star: “A steady light over open water.”**

Pharos is a support-agent demo whose lighthouse metaphor makes guidance tangible: a warm beacon moves toward the visitor while the work surface stays calm, readable, and grounded. The visual world pairs deep marine blue and sea-glass teal with lantern amber, plus a subtle wave-wireframe mesh confined to the masthead above the amber divider.

The interface remains an operations console, not a marketing page. Ticket queues, source traces, chat, and editable reply drafts retain familiar controls and clear hierarchy. The lighthouse illustration and pointer-following beam provide the memorable signature without obscuring task content. Light and dark themes use the same marine-and-amber roles.

**Key Characteristics:**
- Lighthouse icon with a pointer-directed beam on fine-pointer devices.
- Subtle wave-wireframe mesh in sea-glass teal, confined to the masthead.
- Sea-glass accents and warm amber reserved for active guidance.
- Clear, responsive two-pane work areas and high-contrast content surfaces.

## Colors

Marine blues and teals establish the sea; lantern amber is the signal color; pale mist and paper keep dense support content easy to scan.

### Primary
- **Harbor Teal** (#0d6874): Primary actions and links in the light theme.
- **Harbor Teal Soft** (#d7eae6): Selected controls and active rows in the light theme.
- **Lantern Amber** (#f5bc52): Active tab marker, masthead signal, and attention cues.

### Secondary
- **Sea Deep** (#08232f): Masthead and prominent dark surfaces.
- **Sea Current** (#104252): Secondary masthead tone.
- **Human Green** (#276d56): Resolved or safe outcomes.
- **Urgent Red** (#a9332b): Urgent status and risk.

### Neutral
- **Mist** (#e7f0ed): Light-theme page ground.
- **Paper** (#fffdf7): Primary content surfaces.
- **Inset** (#e4eeeb): Recessed content and conversation area.
- **Ink** (#102e39): Primary text.
- **Muted Ink** (#405d65): Supporting text.
- **Rule** (#bfd0cd): Borders and separators.

### Named Rules
**The Beacon Rule.** Amber identifies a live focus, active selection, or guidance cue; it does not replace ordinary text contrast.

**The Sea-Glass Rule.** Teal carries actions and selected state. Use its lighter surface for selection rather than adding a thick colored rail.

## Typography

**Display Font:** Bricolage Grotesque (with Avenir Next and Segoe UI fallbacks)<br>
**Body Font:** IBM Plex Sans (with Segoe UI and system fallbacks)<br>
**Label/Mono Font:** IBM Plex Mono

**Character:** A confident, rounded display face distinguishes section names, while the workhorse body face keeps long support messages comfortable. Monospaced labels are reserved for compact metadata and measured values.

### Hierarchy
- **Headline** (700, 26–36px, 1.05): Product name in the masthead; scales down to 23px on narrow screens.
- **Title** (700, 16–21px): Panel and ticket titles.
- **Body** (400, 15px, 1.55): Main copy, chat, and support content.
- **Label** (500, 11px, tracked uppercase): State labels, search trace, and compact metadata.

## Layout

The page uses a centered 1180px maximum-width container with safe-area-aware side padding. The masthead groups the lighthouse mark and product identity before the demo statistics; section tabs lead directly into the active tool. Chat and triage use two-pane layouts on wider screens and stack below 860px. Narrow screens reduce the beacon mark and preserve horizontally scrollable tabs; triage fields reduce to two columns below 560px.

## Elevation & Depth

Depth comes primarily from tonal surfaces and thin borders. Panes use a restrained offset shadow (`0 8px 18px -16px color-mix(in srgb,var(--sea) 60%,transparent)`) to separate them from the mist-colored page ground. Selected queue rows use a one-pixel inset outline instead of a thick side stripe.

## Shapes

The silhouette is practical and softly chamfered: 6px chips, 8px controls, and 10–12px panels. Borders remain thin; chat bubbles use a single squared corner to distinguish speaker direction. The lighthouse is drawn as a custom inline SVG, not an external icon asset.

## Components

### Buttons
- **Shape:** 8px radius.
- **Primary:** Harbor teal fill with white text; 7px by 12px padding.
- **Hover / Focus:** Border shifts toward the action color; keyboard focus uses a visible 2px outline with offset.
- **Secondary:** Paper surface and a thin rule border.
- **Segmented controls:** Inactive choices use a filled inset surface; on dark headers they use a translucent sea-foam fill.
- **Disabled / completed:** Reduced to 78% opacity so they remain recognizable without appearing actionable.

### Chips
- **Style:** Inset surface, muted text, compact monospaced label.
- **State:** Selected controls use the teal-soft surface; priority and category colors remain semantic.

### Cards / Containers
- **Corner Style:** 12px pane radius; 10px common radius elsewhere.
- **Background:** Paper in light mode, dark surface in dark mode.
- **Shadow Strategy:** Low, offset separation; no ambient glow.
- **Border:** One-pixel rule.
- **Internal Padding:** 12–18px according to content density.

### Inputs / Fields
- **Style:** Paper/dark-surface fill with a one-pixel rule and 8px radius.
- **Focus:** Two-pixel accent outline with offset.
- **Disabled:** Reduced opacity and a non-interactive cursor.

### Navigation
- **Style:** Scrollable horizontal tabs with transparent backgrounds.
- **Active:** Ink text and a 2px lantern-amber underline.
- **Responsive:** Tabs stay in one row and scroll horizontally rather than compressing labels.

### Lighthouse Beacon
The masthead lighthouse is decorative and hidden from assistive technology. On devices with a fine pointer and no reduced-motion preference, its amber beam rotates toward the mouse position across the page. Touch and reduced-motion users receive a stable beam.

## Do's and Don'ts

### Do:
- **Do** keep AI answers, sources, ticket state, and human-review boundaries easy to identify.
- **Do** use the sea/teal/amber roles consistently across light and dark themes.
- **Do** keep the lighthouse illustration decorative and outside the task's focus order.
- **Do** honor reduced-motion preferences and avoid pointer-only functionality for app controls.

### Don't:
- **Don't** use amber as a substitute for readable text contrast.
- **Don't** hide important state or actions inside the masthead illustration.
- **Don't** use a thick colored side stripe to signal the selected queue item.
- **Don't** invent real-world customers, metrics, or outcomes for the fictional demo.
