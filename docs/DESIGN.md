# Deliberate — Design Documentation

## Overview

Deliberate is a multi-agent deliberation system where three AI models (Solver, Challenger, Scout) debate every question in structured rounds before producing a synthesized answer.

This document covers the visual design system and the four screens of the product.

---

## Design System

### Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Near-black | `#131210` | Primary backgrounds (hero, nav, dark sections) |
| Warm off-white | `#F7F4EF` | Light section backgrounds, primary text on dark |
| Amber accent | `#C85C1A` | CTA buttons, active states, accent labels |
| Muted gray | `#EDEAE3` | Secondary section backgrounds |
| Dark surface | `#1E1C19` | Input boxes, terminal panels, cards on dark bg |
| Border dark | `#2A2825` | Dividers and borders on dark backgrounds |
| Secondary text | `#7A7268` | Body text on light backgrounds |
| Muted text | `#5A5650` | Secondary text on dark backgrounds |

### Typography

| Role | Font | Weight | Size |
|------|------|--------|------|
| Display / wordmark | Archivo Black | 400 | 52–80px |
| Section headings | Archivo Black | 400 | 40–48px |
| Card headings | Archivo Black | 400 | 20–22px |
| UI labels / nav | Inter Tight | 500–700 | 11–14px |
| Body text | Inter | 400 | 13–17px |
| Code snippets | JetBrains Mono | 400–500 | 13px |

### Spacing Rhythm

- **Section padding**: 100px top/bottom, 80px left/right
- **Section-to-header gap**: 56px
- **Card internal padding**: 32–36px
- **Card gap**: 16–24px
- **Element gap within cards**: 10–20px

### Visual Direction

Editorial minimalism — alternating dark/light sections create rhythm without repetition. One intense amber accent moment per section. Heavy display type contrasted against light body copy. Information lives on surfaces, not boxed in excessive card chrome.

---

## Screens

### 1. Landing Page (`index.html`)

The marketing/documentation page. Seven sections:

1. **Nav** — Wordmark + Multi-Agent badge + nav links + "Run a query" CTA
2. **Hero** — Dark background. Large display headline. Question input with auto-detected type pills and submit button.
3. **Pipeline** — Four role cards (Solver → Challenger → Scout → Synthesizer) with arrows.
4. **Workflows** — Four workflow types (A–D) showing debate strategy, round count, and examples.
5. **Output** — Split layout: feature bullets left, terminal-style output panel right.
6. **Models** — Free (Groq) vs Paid (Anthropic/OpenAI) preset cards with code snippets.
7. **CTA** — Full-width amber banner.

### 2. Ask Screen

Single-purpose app screen for entering a question.

- Centered layout on dark background
- Large headline: "What do you want to deliberate?"
- Input box with auto-detected question type badge and Workflow label
- Model preset selector below input
- Example prompt chips at the bottom

**Key UX detail**: Question type (Analytical / Factual / Creative / Judgment) and workflow are detected and shown inline before submission — sets expectations.

### 3. Deliberating Screen

Live in-progress state shown while models are running.

- **Left sidebar (380px)**: Question recap + round progress tracker + model list
- **Right main panel**: Tabbed by role (Solver / Challenger / Scout), showing streamed text
- **Round tracker states**: Completed (green check) / Active (amber pulse) / Pending (dimmed)
- **Live indicator**: Amber dot + "Deliberating · Round N of N" in nav center

**Key UX detail**: The streaming cursor (amber block) and "Challenger responding…" label communicate real-time activity without loading spinners.

### 4. Answer Screen

Full results view after deliberation completes.

- **Left sidebar (380px)**: Question recap + verdict badge + models used + follow-up input
- **Right main panel**: Final answer (large, amber left-border) + full reasoning trace
- **Reasoning trace**: Round-by-round expandable cards (R1 / R2 / R3) with per-role summaries
- **Verdict badge**: HIGH / MEDIUM / LOW CONFIDENCE with convergence note

**Key UX detail**: The reasoning trace makes the deliberation transparent — users can see exactly why the Solver changed its position from rewrite to incremental migration.

---

## Component Patterns

### Role Color Coding (consistent across all screens)

- **Solver** — Amber (`#C85C1A`) label
- **Challenger** — Warm brown (`#8A7A6A`) label
- **Scout** — Muted blue-gray (`#6A7A8A`) label

### Question Type Pills

```
ANALYTICAL  FACTUAL  CREATIVE  JUDGMENT
```

Active pill: amber background + amber text
Inactive pill: dark surface + muted text

### Confidence Badge

```
● HIGH CONFIDENCE    All 3 models converged
```

Green for HIGH, amber for MEDIUM, muted for LOW.

### Terminal Panel

Dark surface (`#1E1C19`), three muted dots header, amber left-border on answer text, monospace trace rows.

---

## File Structure

```
docs/
├── index.html    Landing page (deployed to GitHub Pages)
└── DESIGN.md     This file
```

---

## Deployment

The landing page is deployed via GitHub Pages from the `docs/` folder of the `main` branch.

Live URL: `https://shikhar127.github.io/multi-agent-system/`
