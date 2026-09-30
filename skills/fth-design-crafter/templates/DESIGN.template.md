---
version: "alpha"
name: "{{Product}} — {{Direction name}}"
description: "{{One line: who it is for and how it should feel}}"
colors:
  background: "{{#hex}}"
  on-background: "{{#hex}}"
  surface: "{{#hex}}"
  on-surface: "{{#hex}}"
  on-surface-variant: "{{#hex}}"
  surface-container: "{{#hex}}"
  outline-variant: "{{#hex}}"
  outline: "{{#hex}}"
  primary: "{{#hex}}"
  on-primary: "{{#hex}}"
  primary-hover: "{{#hex}}"
  primary-container: "{{#hex}}"
  on-primary-container: "{{#hex}}"
  secondary: "{{#hex}}"
  on-secondary: "{{#hex}}"
  success: "{{#hex}}"
  on-success: "{{#hex}}"
  warning: "{{#hex}}"
  on-warning: "{{#hex}}"
  error: "{{#hex}}"
  on-error: "{{#hex}}"
  # Repeat every role with a -dark suffix (background-dark, on-surface-dark, ...) when the product has a dark theme.
typography:
  headline-display: {fontFamily: "{{Heading family}}", fontSize: "{{px}}", fontWeight: 700, lineHeight: 1.1, letterSpacing: "-0.02em"}
  headline-lg: {fontFamily: "{{Heading family}}", fontSize: "{{px}}", fontWeight: 700, lineHeight: 1.1}
  headline-md: {fontFamily: "{{Heading family}}", fontSize: "{{px}}", fontWeight: 700, lineHeight: 1.15}
  headline-sm: {fontFamily: "{{Heading family}}", fontSize: "{{px}}", fontWeight: 600, lineHeight: 1.2}
  title-md: {fontFamily: "{{Heading family}}", fontSize: "{{px}}", fontWeight: 600, lineHeight: 1.25}
  body-lg: {fontFamily: "{{Body family}}", fontSize: "{{px}}", fontWeight: 400, lineHeight: 1.55}
  body-md: {fontFamily: "{{Body family}}", fontSize: "16px", fontWeight: 400, lineHeight: 1.55}
  body-sm: {fontFamily: "{{Body family}}", fontSize: "{{px}}", fontWeight: 400, lineHeight: 1.55}
  label-lg: {fontFamily: "{{Body family}}", fontSize: "{{px}}", fontWeight: 600, lineHeight: 1.2}
  label-md: {fontFamily: "{{Body family}}", fontSize: "{{px}}", fontWeight: 600, lineHeight: 1.2}
  label-sm: {fontFamily: "{{Body family}}", fontSize: "{{px}}", fontWeight: 600, lineHeight: 1.2}
rounded:
  none: "0px"
  sm: "{{px}}"
  md: "{{px}}"
  lg: "{{px}}"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  gutter: "24px"
  margin: "16px"
  max-width: "{{1200px}}"
components:
  button-primary: {backgroundColor: "{colors.primary}", textColor: "{colors.on-primary}", typography: "{typography.label-lg}", rounded: "{rounded.md}", padding: "12px", height: "44px"}
  button-primary-hover: {backgroundColor: "{colors.primary-hover}", textColor: "{colors.on-primary}"}
  button-secondary: {backgroundColor: "{colors.surface}", textColor: "{colors.on-surface}", typography: "{typography.label-lg}", rounded: "{rounded.md}", padding: "12px", height: "44px"}
  card: {backgroundColor: "{colors.surface}", textColor: "{colors.on-surface}", rounded: "{rounded.lg}", padding: "24px"}
  input: {backgroundColor: "{colors.background}", textColor: "{colors.on-surface}", typography: "{typography.body-md}", rounded: "{rounded.md}", padding: "12px", height: "44px"}
  input-border: {backgroundColor: "{colors.outline}", height: "1px"}
  divider: {backgroundColor: "{colors.outline-variant}", height: "1px"}
  tag: {backgroundColor: "{colors.primary-container}", textColor: "{colors.on-primary-container}", typography: "{typography.label-sm}", rounded: "{rounded.full}"}
  badge-success: {backgroundColor: "{colors.success}", textColor: "{colors.on-success}", typography: "{typography.label-sm}", rounded: "{rounded.sm}"}
  badge-warning: {backgroundColor: "{colors.warning}", textColor: "{colors.on-warning}", typography: "{typography.label-sm}", rounded: "{rounded.sm}"}
  badge-error: {backgroundColor: "{colors.error}", textColor: "{colors.on-error}", typography: "{typography.label-sm}", rounded: "{rounded.sm}"}
  focus-highlight: {backgroundColor: "{colors.secondary}", textColor: "{colors.on-secondary}", width: "3px"}
---

<!--
Template for DESIGN.md (google-labs-code/design.md, version alpha). Prefer generating the file with
`scripts/build_specimen.py <directions.json> --export <id>`; use this template for URL extraction or hand edits.
Rules: keep the eight sections below in this order; refer to tokens in prose as {colors.primary};
flat colors only; run `scripts/lint_design_md.py DESIGN.md` (and `npx @google/design.md lint DESIGN.md`) before handing off.
-->

# {{Product}}

## Overview

{{One specific real-world reference, e.g. "A port's bill of lading and container stowage plan: printed forms on off-white paper, stamped in one ink." Not adjectives like "modern, clean, premium".}}

{{Who uses it, in what situation, on which devices, and what the interface must help them do.}}

{{Theme note: light is the default; every color has a -dark twin used when [data-theme="dark"] is set or the system prefers dark.}}

## Colors

{{One sentence about the palette's logic (flat colors; where the primary hue comes from; competitor stance).}}

- **{{Descriptive name}}** {colors.background} (`{{#hex}}`): the page canvas.
- **{{Descriptive name}}** {colors.surface} (`{{#hex}}`): cards, panels, dialogs.
- **{{Descriptive name}}** {colors.on-surface} (`{{#hex}}`): all headings and body text.
- **{{Descriptive name}}** {colors.primary} (`{{#hex}}`): the one main action per view.
- **{{Descriptive name}}** {colors.secondary} (`{{#hex}}`): focus rings and highlights.
- State colors {colors.success}, {colors.warning}, {colors.error}: state only, always with a label or icon.

## Typography

- **{{Heading family}}** for headings: {{why it fits the reference}}.
- **{{Body family}}** for body and UI: {{why it reads well here}}.
- {typography.body-md} is the default reading size; {typography.label-lg} for buttons; {typography.label-md} for form labels and table headers.
- All families support Turkish (latin-ext): ğ Ğ ş Ş ı İ and ₺.

## Layout

{{Grid model, breakpoints, maximum width {spacing.max-width}, spacing rhythm using {spacing.sm}, {spacing.md}, {spacing.lg}, density.}}

## Elevation & Depth

{{How hierarchy is shown without effects: tonal layers {colors.background} → {colors.surface} → {colors.surface-container}, hairline {colors.outline-variant} borders; where (if anywhere) a shadow is allowed. No gradients, glow, glass, or blur.}}

## Shapes

{{Corner strategy: controls {rounded.md}, cards {rounded.lg}, badges {rounded.sm}, pills {rounded.full}; what stays square.}}

## Components

{{Buttons, inputs, focus, cards, tags and badges, tables, plus domain components (e.g. tracking timeline). Note that `input-border` and `divider` carry border colors in backgroundColor because the format has no border property.}}

## Do's and Don'ts

- Do {{the rule that protects the reference most}}.
- Do keep every color flat; hierarchy comes from tone, type, space, and borders.
- Don't use gradients, glow, glass or blur effects, or decorative 3D shapes.
- Don't introduce colors or font sizes that are not tokens in this file.
- Don't {{the most likely drift for this product}}.

## Evidence

{{Direction id and date; why this direction; sources (competitor scan, type-in-use references, domain materials); open checks. For a URL extraction, separate observed values from inferred ones and state limitations.}}
