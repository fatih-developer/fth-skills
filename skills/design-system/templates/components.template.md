# components.md

## Purpose

Reusable component definitions derived from the reference design language.

Each component should be implemented using the tokens in `DESIGN.md` and `tokens.css`.

## Button

### Primary Button

Usage: Main call-to-action.

Visual rules:

- Background: `--primary`
- Text: white or strongest contrast token
- Hover: `--primary-hover`
- Radius: `--radius-md`
- Height: minimum `44px`
- Padding: `12px 18px` or `12px 20px`
- Font weight: 700 or 800

States:

- Hover: slightly darker background or subtle lift
- Active: reduce lift, slightly darker
- Focus: visible primary focus ring
- Disabled: low opacity and no pointer interaction

## Secondary Button

Usage: Alternative action.

Visual rules:

- Background: `--surface`
- Text: `--text`
- Border: `--border`
- Radius: `--radius-md`

## Card

Usage: Group related information.

Visual rules:

- Background: `--surface`
- Border: `1px solid var(--border)`
- Radius: `--radius-lg` or `--radius-xl`
- Padding: `24px` or `32px`
- Shadow: `--shadow-sm` or `--shadow-md`

Structure:

```txt
Card
├── Optional icon/media
├── Title
├── Description/body
└── Optional action
```

## Input

Visual rules:

- Background: `--bg-elevated`
- Border: `--border`
- Text: `--text`
- Placeholder: `--text-muted`
- Radius: `--radius-md`
- Height: minimum `44px`
- Padding: `12px 14px`

Focus:

- Border: `--primary`
- Ring: primary at 12-18% opacity

## Badge

Usage: Compact status or category labels.

Visual rules:

- Shape: pill
- Padding: `6px 10px`
- Font size: `12px`
- Font weight: 700-900
- Use semantic soft background and strong foreground

## Alert

Types:

- Info
- Success
- Warning
- Danger

Rules:

- Include icon or label when useful.
- Never rely only on color.
- Use semantic token backgrounds with accessible text.

## Navbar

Rules:

- Height should usually be `64px-80px`.
- Use brand mark + navigation + action area.
- Inactive links use `--text-muted`.
- Active links use `--text` or `--primary`.
- On mobile, collapse links into menu if needed.

## Hero Section

Rules:

- Strong headline.
- Muted supporting paragraph.
- One primary CTA and optional secondary CTA.
- Generous vertical spacing.
- Optional visual panel or product preview.

## Feature Grid

Rules:

- Use 2-4 columns on desktop.
- Collapse to 1 column on mobile.
- Each feature card should have a consistent icon/title/body pattern.

## Modal

Rules:

- Surface background.
- Radius: `--radius-xl`.
- Shadow: `--shadow-lg`.
- Clear title and actions.
- Escape and overlay close behavior when implemented.

## Table

Rules:

- Use borders or subtle row dividers.
- Header text should be smaller and bold.
- Align numbers consistently.
- Use badges for statuses.

## Empty State

Rules:

- Use simple icon or illustration.
- Clear title.
- Helpful explanation.
- One recommended action.
