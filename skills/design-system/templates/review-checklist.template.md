# UI Review Checklist

Use this checklist before applying a generated design to a real project.

## Source Analysis

- [ ] URL was accessible.
- [ ] Desktop screenshot was reviewed.
- [ ] Mobile screenshot was reviewed.
- [ ] DOM/CSS/computed styles were reviewed where possible.
- [ ] Observed and inferred decisions are separated.
- [ ] Limitations are documented.

## Tokens

- [ ] `DESIGN.md` front matter follows the design.md spec (colors, typography, rounded, spacing, components).
- [ ] Color roles use the spec names (`background`, `surface`, `on-surface`, `outline`, `primary`, `on-primary`, `secondary`, `error`, ...).
- [ ] Every color has a `-dark` twin when a dark theme exists.
- [ ] Colors are flat; no gradient values anywhere.
- [ ] Typography levels use the recommended names (`headline-*`, `body-*`, `label-*`).
- [ ] `scripts/lint_design_md.py DESIGN.md` reports 0 errors and 0 warnings.
- [ ] `npx @google/design.md lint DESIGN.md` agrees (when Node is available).
- [ ] No unnecessary one-off values are included.

## Components

- [ ] Button variants are defined.
- [ ] Card style is defined.
- [ ] Form controls are defined.
- [ ] Badge/status styles are defined.
- [ ] Navigation pattern is defined when relevant.
- [ ] Layout/grid rules are defined.
- [ ] Empty/loading/error states are considered.

## Accessibility

- [ ] Text contrast is acceptable.
- [ ] Focus states are visible.
- [ ] Tap targets are at least 44px where possible.
- [ ] Status is not communicated by color alone.
- [ ] Semantic HTML is preferred.

## Preview

- [ ] `preview.html` was generated.
- [ ] Light theme was checked.
- [ ] Dark theme was checked if available.
- [ ] Mobile layout was checked.
- [ ] Components look visually consistent.
- [ ] Preview does not copy protected brand assets.

## Implementation Readiness

- [ ] `DESIGN.md` is ready: Overview opens with a specific reference, sections are in spec order, Do's and Don'ts are specific.
- [ ] `tokens.css` is ready (light, dark, and `prefers-color-scheme`).
- [ ] `tailwind.theme.json` is ready if Tailwind v3 is used, or `npx @google/design.md export --format css-tailwind` for Tailwind v4.
- [ ] `preview.html` renders from `tokens.css`.
