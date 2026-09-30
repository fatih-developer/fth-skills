---
name: design-system
description: "Build and enforce a product-specific design system: research competitors and real-world type, propose 2-3 flat-color palette and font-pairing directions beyond overused defaults, demo them side by side, then write DESIGN.md and tokens, design pages on top, and review implementations against them. Use when the user wants a color palette, font or typography choices, a design system, design tokens or DESIGN.md, a landing page or dashboard design, or a UI/design review; also for Turkish requests like 'renk paleti', 'font önerisi', 'tipografi', 'tasarım sistemi'."
---

# Design System

One skill for the whole visual system: **FOUNDATIONS** decides color and type from evidence, **SPEC** writes it down as `DESIGN.md` and tokens, **PAGE** designs screens on top of it, **REVIEW** checks pages and code against it.

The goal is a system that belongs to this product. It must not look like a template or like typical AI output, including Claude's own habits (warm cream + terracotta, serif-heavy "editorial" defaults).

## Pick the mode

| Request | Mode | Read |
|---|---|---|
| Colors, palette, fonts, typography, "make it look like us", new brand look | FOUNDATIONS | `references/research-protocol.md`, `references/color-method.md`, `references/typography-method.md`, `references/font-sources.md` |
| DESIGN.md (google-labs-code/design.md format), tokens, Tailwind theme, extract a system from a URL, lint and enforce | SPEC | `references/mode-spec.md` |
| Design a page, landing, dashboard, screen structure | PAGE | `references/mode-page.md`, `references/page-rules.md`, `references/page-examples.md` |
| Review, audit, critique a page or UI code | REVIEW | `references/mode-review.md`, `references/review-rubric.md` |

A full run goes FOUNDATIONS → SPEC → PAGE → REVIEW. Start later only when the earlier output already exists (for example, an approved `DESIGN.md`).

## Non-negotiables

1. **Evidence before taste.** Every color and font choice cites a source: project assets, competitor scan, type-in-use reference, or domain material. Write it in `design-research.md`.
2. **Flat color only.** No gradients in tokens, fills, text, or backgrounds. A brand-mandated gradient is a documented exception with a flat fallback.
3. **Beyond defaults.** Overused families (Inter, Roboto, Open Sans, Poppins, Montserrat, Lato, …), AI-favorite families (Space Grotesk, Fraunces, Instrument Serif, Geist, Manrope, Plus Jakarta Sans, Satoshi, …), and template colors (indigo/violet SaaS accents, slate navy + cyan, cream + terracotta) need an explicit reason. The lists live in `scripts/ai_defaults.json`.
4. **Measured, not claimed.** Contrast, Turkish glyph support, font weights, and competitor colors come from the scripts or real renders. Say when something is unverified.
5. **Choices for the user.** Offer 2-3 genuinely different directions and let the user choose; do not present one palette as the answer.
6. **Existing brand wins.** Keep established brand colors and fonts; build the system around them.

## FOUNDATIONS workflow

1. **Collect project evidence:** product, audience, market and language, logo, brand colors, current CSS. For an SVG logo, read its fills and any `font-family`.
2. **Scan (announce first):** 3-5 competitor or category sites with `scan_site.py`, 2-3 typography-in-use references, and the domain's materials. Skip the live scan when the user declines or no network is available, and say so. Details: `references/research-protocol.md`.
3. **Find fonts:** translate the product and logo into type traits, then `find_fonts.py search` / `check`. Details: `references/typography-method.md`.
4. **Build 2-3 directions:** each with one specific real-world `reference` sentence, a competitor stance, neutrals, one `primary`, at most one `secondary`, semantic states, a dark theme, a heading/body pairing, and a type scale. Color roles use DESIGN.md names (`background`, `surface`, `on-surface`, `outline-variant`, `primary`, `on-primary`, `secondary`, `success`, `warning`, `error`). Write them to `design/directions.json` using `templates/directions.template.json`.
5. **Check and demo:** `build_specimen.py design/directions.json --landscape design/landscape.json --out design/specimen.html`. Fix every FAIL; answer every WARN in the rationale.
6. **Present:** a short comparison (stance, fonts, primary, why, open warnings) plus the specimen. When the host can publish or show HTML, show `specimen.html`; otherwise give its path.
7. **After the user chooses:** go to SPEC and export the chosen direction as a spec-compliant `DESIGN.md`.

Write the research note from `templates/design-research.template.md`.

## Outputs

| File | Mode | Contents |
|---|---|---|
| `design/design-research.md` | FOUNDATIONS | Evidence, landscape, defaults avoided, directions, decision |
| `design/directions.json` | FOUNDATIONS | The 2-3 directions (input to the scripts) |
| `design/specimen.html` | FOUNDATIONS | Side-by-side demo of the directions on real UI, light and dark |
| `design/DESIGN.md` | SPEC | google-labs-code/design.md format: YAML front-matter tokens (colors with `-dark` twins, typography, rounded, spacing, components) + Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts, Evidence |
| `design/tokens.css`, `design/tailwind.theme.json` | SPEC | CSS variables named like the official export (`--color-*`, `--text-*`, …) with light, dark, and `prefers-color-scheme`; Tailwind v3 theme bound to them |
| `design/preview.html` | SPEC | The system rendered from `templates/preview.template.html` |
| Page strategy, section architecture, rule check | PAGE | In the reply, or a doc when requested |
| Scores, issues, recommendation | REVIEW | In the reply, or a report when requested |

For extracting a reference site, SPEC writes to `design-md/<site-name>/` instead, filling `templates/DESIGN.template.md`. Checklist before handoff: `templates/review-checklist.template.md`. Extraction examples: `examples/example-input.yaml`, `examples/example-design-analysis.json`.

## Scripts

Standard-library Python; run from the project root with `<skill-dir>` as the folder of this file.

| Script | Purpose |
|---|---|
| `scripts/scan_site.py <urls…> [--json]` | Colors (by frequency), fonts, gradient use per site; with several sites, occupied and free accent hues |
| `scripts/find_fonts.py search / check / css` | Google Fonts candidates beyond the top 60 and default lists, Turkish (latin-ext) check, weights, axes, css2 URL |
| `scripts/build_specimen.py <directions.json>` | Contrast, gradient, default, similarity, competitor, and font checks; `specimen.html`; `--export <id>` writes DESIGN.md, tokens.css, tailwind.theme.json (via `scripts/design_md.py`) and lints the result |
| `scripts/lint_design_md.py <DESIGN.md> [--official]` | Mirrors the official design.md linter and adds no-gradient, dark-twin, prose-reference, placeholder, and default-font rules; `--official` also runs `npx @google/design.md lint` |
| `scripts/colorlib.py ramp / contrast / oklch / distance` | Tonal ramps, WCAG contrast, OKLCH values, perceptual distance |
| `scripts/ai_defaults.json` | Overused fonts, AI-favorite fonts, template colors and pairs, popularity cutoff |

`find_fonts.py` caches Google Fonts metadata for 7 days in `~/.cache/fth-skills/`; `build_specimen.py` reuses that cache for font checks and never goes online itself.

## When to skip

- A one-off color or font question with no system behind it: answer directly, still avoiding the defaults above.
- Implementation of an already-approved design: hand off to `@claude-style-coding`.
- Only removing an AI look from an existing design without a new system: `@anti-ai-slop-design`.

## Scope vs Related Skills

| Need | Skill |
|---|---|
| Palette, typography, DESIGN.md, tokens, page strategy, UI review | `@design-system` |
| Implementing a user-facing feature with product thinking and every UX state handled | `@claude-style-coding` |
| Removing generic AI aesthetics from an existing design, image brief, or page | `@anti-ai-slop-design` |
| Mobile screen-reader and touch accessibility audit | `@accessibility-enforcer` |

`design-intelligence` and `design-md-enforcer` are deprecated aliases of this skill.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-web` — Web, Design & Delivery.

**Workflows:**
- **Palette & Typography Flow** (`web-foundations`, step 1 of 4): next → `@anti-ai-slop-design` *(optional)*.
- **Palette & Typography Flow** (`web-foundations`, step 3 of 4): next → `@claude-style-coding` *(optional)*.
- **Product Page Build Flow** (`web-build-page`, step 1 of 5): next → `@design-system`.
- **Product Page Build Flow** (`web-build-page`, step 2 of 5): next → `@anti-ai-slop-design` *(optional)*.
- **UI Review Flow** (`web-review`, step 1 of 2): last step → once it passes, complete the workflow and report the outcome.
- **Remove the AI Look Flow** (`web-de-slop`, step 2 of 3): next → `@claude-style-coding` *(optional)*.

**Direct handoffs:**
- `@anti-ai-slop-design` — A direction or page relies on generic AI/SaaS visuals.
- `@accessibility-enforcer` — The system will be used in a mobile app.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-web`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
