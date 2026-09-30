# SPEC Mode — DESIGN.md (google-labs-code/design.md format)

`DESIGN.md` is the single source of visual truth for people and agents. It follows the open **design.md** specification (github.com/google-labs-code/design.md, version `alpha`): machine-readable tokens in YAML front matter, and human-readable rationale in a Markdown body with eight fixed sections.

> The spec's own philosophy: the prose is where the design lives. A specific reference ("a port's bill of lading printed on off-white paper") carries more than a list of adjectives ("modern, clean, premium"); tokens are the exact values the prose applies.

## 1. File structure

```
---                      # YAML front matter (tokens, normative)
version: "alpha"
name: "…"
description: "…"
colors:        {role: "#hex", …, role-dark: "#hex"}
typography:    {level: {fontFamily, fontSize, fontWeight, lineHeight, letterSpacing}}
rounded:       {none, sm, md, lg, full}
spacing:       {xs, sm, md, lg, xl, gutter, margin, max-width}
components:    {name: {backgroundColor, textColor, typography, rounded, padding, height, width}}
---

## Overview            (alias: Brand & Style)
## Colors
## Typography
## Layout              (alias: Layout & Spacing)
## Elevation & Depth   (alias: Elevation)
## Shapes
## Components
## Do's and Don'ts
## Evidence            (fth-skills addition; unknown sections are allowed after the eight)
```

Sections may be omitted, but those present must keep this order, and a heading may appear only once. List intentionally omitted token groups under `omitted:` with a reason.

## 2. Token rules

- **Colors** use Material-3-style role names so agents and the official linter recognize them: `background`, `on-background`, `surface`, `on-surface`, `on-surface-variant`, `surface-container`, `outline-variant`, `outline`, `primary`, `on-primary`, `primary-container`, `on-primary-container`, `secondary`, `on-secondary`, `error`, `on-error`, plus `success`/`warning` (with `on-*`) and `primary-hover`. `primary` is required. Values are single flat colors; hex is preferred.
- **Dark theme:** the spec has no theme mechanism, so every color has a `-dark` twin in the same `colors` map (`surface-dark`), and components have `-dark` variants that reference them (`button-primary-dark`). Do not put dark colors under a custom top-level key; the official linter flags token-like unknown keys and exports ignore them.
- **Typography** uses the recommended level names: `headline-display`, `headline-lg`, `headline-md`, `headline-sm`, `title-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm` (and `code-md` when there is a mono family). `fontSize` and `letterSpacing` need `px`, `em`, or `rem`; `lineHeight` is a unitless multiplier.
- **Components** reference tokens with `{colors.primary}`, `{typography.label-lg}`, `{rounded.md}`. Every color should be referenced by at least one component (the official `orphaned-tokens` rule), and every `backgroundColor`/`textColor` pair must reach 4.5:1 (`contrast-ratio`). The format has no border property; `input-border` and `divider` carry border colors in `backgroundColor`.
- **Variants** are separate components with related names: `button-primary`, `button-primary-hover`.

## 3. Prose rules

- **Overview** opens with one specific real-world reference (the `reference` field of the direction), then audience and situation, then the theme note.
- **Colors** gives each core role a descriptive name, its token (`{colors.primary}`), its hex, and its job; then the light/dark table and measured contrast.
- **Typography** names each family with the reason it fits, the Google Fonts URL, and which level is used where.
- **Layout, Elevation & Depth, Shapes, Components** refer to tokens instead of repeating raw values.
- **Do's and Don'ts** is short and specific: the rules that protect the reference plus the drifts most likely for this product. Always include: flat colors only, no gradients/glow/glass, no values outside the tokens.
- **Evidence** records direction id, date, rationale, sources, and open checks.

## Workflow A — From the chosen direction

1. Run `build_specimen.py <directions.json> --export <id> --out-dir design/`. It writes `DESIGN.md`, `tokens.css` (CSS variables named like the official `css-tailwind` export: `--color-*`, `--font-*`, `--text-*`, `--leading-*`, `--font-weight-*`, `--radius-*`, `--spacing-*`, with a dark-theme switch), and `tailwind.theme.json` (Tailwind v3, bound to those variables), then lints `DESIGN.md`.
2. Edit the prose where the product needs more (domain components, layout specifics, extra don'ts). Keep token edits in the front matter, not in the prose.
3. Lint again: `python <skill-dir>/scripts/lint_design_md.py design/DESIGN.md --official`. Fix every error; treat warnings as blockers before handoff.
4. Optional exports with the official CLI: `npx @google/design.md export --format css-tailwind design/DESIGN.md` (Tailwind v4 `@theme`) or `--format dtcg` (W3C design tokens).
5. Render `templates/preview.template.html` next to `tokens.css` so the team sees buttons, forms, cards, and states in the real system.

## Workflow B — Extract a design system from a URL

1. Run `scan_site.py <url>` for measured colors, fonts, and gradient use. If you can render the page, add radius, spacing, and component observations; otherwise ask for screenshots or CSS.
2. Fill `templates/DESIGN.template.md` and write it to `design-md/<site-name>/DESIGN.md` with a `preview.html`. Put observed vs inferred values and limitations in `## Evidence`. `examples/example-input.yaml` and `examples/example-design-analysis.json` show the intermediate analysis (its `Inter` value is an observed fact about that site, not a recommendation).
3. An extraction documents a reference; it does not license a clone.
4. The linter rejects unfilled `{{placeholders}}`, so a half-filled template cannot be handed off.

## Validation and drift

When you or another agent change tokens or components:

- **Lint:** `lint_design_md.py` mirrors the official rules (broken references, missing primary or typography, section order, duplicate sections, contrast, orphaned tokens, units) and adds fth-skills rules (no gradients, complete `-dark` twins, prose references that resolve, unfilled placeholders, default fonts).
- **Role consistency:** a token's use matches its role (no `error` for decoration, no `secondary` as a second primary action).
- **Code drift:** search the code for hardcoded hex values, `px` font sizes outside the scale, and `linear-gradient(`/`radial-gradient(`/`conic-gradient(` that bypass tokens.
- **Version changes:** compare two versions with `npx @google/design.md diff DESIGN.md DESIGN-v2.md`.

## Agent behavior

- Read `DESIGN.md` before any UI change.
- Never hardcode a color or size when a token exists; if a token is missing, add it to the front matter with a role and a reason in the prose first.
- Reject UI changes that violate `DESIGN.md` and name the rule they break.
