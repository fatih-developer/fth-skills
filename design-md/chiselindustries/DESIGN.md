---
version: "alpha"
name: "Chisel Industries — reference extraction"
description: "Dark, high-contrast industrial site: ink-black canvas, white type, one teal accent, square sections and 4px controls."
omitted:
  - section: spacing
    reason: "Spacing scale was not measured in the original extraction; only button padding (12px 24px) was observed."
colors:
  background: "#111111"
  on-background: "#FFFFFF"
  surface: "#111111"
  on-surface: "#FFFFFF"
  outline-variant: "#333333"
  primary: "#FFFFFF"
  on-primary: "#111111"
  secondary: "#F2EFED"
  tertiary: "#3B8E9A"
  on-tertiary: "#111111"
typography:
  headline-lg:
    fontFamily: "Montserrat"
    fontWeight: 700
  label-nav:
    fontFamily: "Montserrat"
    fontWeight: 700
    letterSpacing: "0.05em"
  body-md:
    fontFamily: "Inter"
    fontWeight: 400
  label-lg:
    fontFamily: "Inter"
    fontWeight: 600
rounded:
  none: "0px"
  sm: "4px"
components:
  nav:
    backgroundColor: "{colors.background}"
    textColor: "{colors.on-background}"
    typography: "{typography.label-nav}"
  section:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.none}"
  button-ghost:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.sm}"
    padding: "12px"
  button-ghost-hover:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  brand-mark:
    backgroundColor: "{colors.background}"
    textColor: "{colors.secondary}"
  hero-accent:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
  divider:
    backgroundColor: "{colors.outline-variant}"
    height: "1px"
---

# Chisel Industries

## Overview

A master craftsman's blueprint: sharp, intentional, and enduring, set against the textures of the built world (wood, steel, stone) instead of a sterile "tech" look.

A dark, high-contrast marketing site. Full-bleed photography carries the craft; the interface stays quiet around it, with white type on an ink-black canvas and a single teal accent. This file documents a reference site for study; it is not a license to clone it.

## Colors

- **Ink** {colors.background} (`#111111`): the page canvas and every section background.
- **Canvas** {colors.on-background} (`#FFFFFF`): all typography and the ghost-button outline; the primary interactive color ({colors.primary}).
- **Accent** {colors.secondary} (`#F2EFED`): the brand logo and soft highlights.
- **Attention** {colors.tertiary} (`#3B8E9A`): a cinematic teal reserved for hero focus and a few UI accents.
- **Subtle** {colors.outline-variant} (`#333333`): borders of secondary elements. It is only 1.5:1 against Ink, so it must not carry text.

## Typography

- **Montserrat** 700 for hero titles ({typography.headline-lg}) and all-caps navigation ({typography.label-nav}).
- **Inter** 400 for body text ({typography.body-md}) and 600 for button labels ({typography.label-lg}).
- Font sizes were not measured in the original extraction; measure them before reusing this file for production.

## Layout

Full-bleed sections alternate photography and text. Text sits over dark overlays on imagery so contrast holds. Navigation is transparent over the hero.

## Elevation & Depth

Flat. Depth comes from photography and dark overlays, not shadows. No gradients or glow in the interface itself.

## Shapes

Section containers are square ({rounded.none}); buttons use a small {rounded.sm} radius.

## Components

- **Buttons:** `button-ghost` — transparent on Ink with a 2px {colors.primary} border, {typography.label-lg}, padding 12px 24px; on hover it fills (`button-ghost-hover`).
- **Navigation:** `nav` — transparent, high-contrast all-caps labels; hover lowers opacity to 0.7.
- **Sections:** `section` — full-bleed imagery with dark overlays for text readability.
- **Accents:** `hero-accent` — the teal bar under the hero; `brand-mark` — the logo in Accent.

## Do's and Don'ts

- Do keep white type on Ink; the contrast is the brand.
- Do keep Attention teal rare: one element per view.
- Don't use Subtle (#333333) for text; it fails contrast on Ink. Use Canvas at reduced emphasis only if contrast stays at 4.5:1.
- Don't round section containers or add shadows and gradients to the interface.

## Evidence

Converted on 2026-09-30 from the earlier `design-md-enforcer` extraction into the google-labs-code/design.md format.

- **Observed:** the five colors, the Montserrat/Inter pairing and weights, ghost-button styling (2px border, 4px radius, 12px 24px padding), transparent navigation with opacity hover, full-bleed sections with dark overlays, square section containers.
- **Inferred:** role mapping (Canvas as `primary`, Accent as `secondary`, Attention as `tertiary`), the craftsman's-blueprint reference.
- **Not measured:** font sizes, line heights, spacing scale (listed under `omitted`).
- **Accessibility note:** Subtle (#333333) on Ink (#111111) is 1.49:1; the original extraction listed it for secondary text, which fails WCAG.
- **Fonts:** Montserrat and Inter are among the most used families on the web; they are recorded here because the site uses them, not as a recommendation.
