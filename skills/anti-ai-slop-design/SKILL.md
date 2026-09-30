---
name: anti-ai-slop-design
description: "Create, review, or refine product interfaces, web designs (landing pages, corporate sites, portfolios, e-commerce, SaaS marketing pages, and responsive web apps), dashboards, visual concepts, and image-generation briefs to remove generic AI aesthetics and strengthen product-specific hierarchy. Use when users ask for anti-slop design, less shiny/neon/futuristic visuals, more natural or deliberate design, or removal of generic AI/SaaS patterns. Apply to new web designs, existing website redesigns, design reviews, and requested frontend implementation; do not trigger for unrelated backend changes or ordinary prose editing."
---

# Anti-AI-Slop Design

Make visual decisions follow the product, audience, task, and brand. An AI-enabled product does not require AI-looking design. Apply these principles independently or alongside a visualization, product-design, image-generation, or implementation skill.

## Workflow

1. Inspect the supplied screenshot, mockup, existing design, brief, or relevant project context before judging it. For repository work, inspect the smallest useful set of screens, components, tokens, and product documents.
2. Identify the primary user task, focal information, established brand, supported functionality, and requested scope. Distinguish observed defects from assumptions; without a visible artifact, give guidance rather than pretending to audit a screen.
3. Find the few generic patterns that most weaken meaning, hierarchy, or usability. Explain their concrete effect when a review is requested.
4. Choose one coherent correction based on product context. Preserve functioning information architecture, interactions, exact required wording, and unrelated regions.
5. Match the output to the request: report findings for an audit; return a usable brief for a prompt request; generate an image for a requested raster concept when an image tool is available; edit code only when implementation is requested. Use the relevant tool or skill for execution and verification.
6. Verify the result against the acceptance checks below. Make conservative, reversible choices when routine creative details are missing. Ask only if uncertainty materially changes product meaning, identity, or required content.

## Remove generic defaults

Avoid these choices unless an explicit request, established brand, or clear functional purpose justifies them:

- Cyan/purple decorative gradients, neon outlines, bloom, lens flare, and atmospheric glow.
- Dark navy plus electric cyan as an automatic palette for AI products.
- Glowing brains, cubes, orbs, neural meshes, holograms, data tunnels, particles, and floating 3D blobs.
- Glassmorphism, glossy plastic materials, impossible reflections, and excessively polished corporate stock imagery.
- Every section enclosed in a rounded card; identical card sizes, spacing, radii, and visual importance.
- Symmetrical dashboard mosaics, decorative charts, and excessive pills, badges, chips, or status dots.
- Gradient text, enormous vague headlines, generic SaaS section formulas, and decorative microtext.
- Invented testimonials, metrics, integration logos, customer counts, or unsupported capabilities.
- Decorative parallax, animated gradients, and identical entrance animations on everything.

Do not turn this list into blanket bans. Cards, dark mode, gradients, and animation can serve real purposes. Judge the pattern in context.

## Replace with deliberate design

- Make the main task and its next action clear before adding decoration.
- Use actual product surfaces, domain entities, supported flows, and specific interface copy.
- Preserve existing brand tokens and typography. Do not reject Inter, vivid color, playful illustration, or dark mode merely because they are common.
- Without a brand system, start with neutral surfaces, one primary accent, and restrained semantic feedback colors.
- Build hierarchy through type, alignment, contrast, density, grouping, and space. Vary component scale according to importance.
- Use flat sections, dividers, tables, panels, or cards according to function; use subtle elevation only when needed.
- Use color to communicate action, selection, success, warning, or error. Keep nonsemantic saturation under control.
- Keep labels legible, icons consistent, and screen proportions appropriate to the device.
- Preserve accessibility: adequate contrast, visible focus, usable targets, and cues beyond color alone. Check these in the implementation when available; do not claim exact compliance from a mockup.
- Leave space empty when content is unavailable. Clearly identify illustrative sample data if the task needs examples; never present it as actual product evidence.
- Use natural lighting, plausible materials, ordinary environments, and believable poses when imagery needs people or physical objects.
- Use motion to communicate state, causality, hierarchy, or feedback.

Anti-slop does not mean compulsory beige, monochrome, minimalism, arbitrary asymmetry, or elaborate visual complexity. Preserve expression that belongs to the product.

## Copy within visuals

Use concrete nouns, direct verbs, established domain terms, and short action labels. Remove vague future-facing claims, inflated superlatives, fake-profound contrasts, and unsupported social proof. Keep exact established copy when the user requires it.

## Output-specific rules

### Websites and responsive web design

- Start from the visitor's intent and page goal: understand an offer, evaluate evidence, browse products, contact a business, or complete a purchase. Make the main action explicit.
- Build page structure from actual content and decision order. Do not automatically insert hero + logo strip + three feature cards + testimonials + pricing + FAQ. Include each section only when it answers a real visitor question.
- Design the hero around a concrete offer, a clear action, and relevant product imagery or domain evidence. Do not use giant vague headlines, decorative dashboard mockups, fake customer logos, or invented conversion claims.
- Preserve the site's identity across navigation, headings, buttons, forms, product listings, detail pages, and footer. Choose grids, editorial sections, lists, or cards by content; do not force every page into a bento layout.
- Use genuine product photos, supplied screenshots, or relevant illustration when available. Keep supporting imagery subordinate to the message and task.
- Design mobile behavior explicitly: readable text, sensible wrapping, reachable actions, usable menus, stacked content in meaningful order, and no accidental horizontal overflow. Adapt layouts to content rather than shrinking the desktop screenshot.
- For e-commerce, prioritize product information, price, variants, delivery/return information when supplied, and purchase controls. For service sites, prioritize the service, audience, credible evidence, and contact path. Do not invent missing policies or guarantees.
- In requested code work, implement layout and interaction with semantic HTML, project components, CSS and existing tokens. Use image generation for supporting raster assets rather than generating a whole webpage as the implementation.
- Check keyboard navigation, focus, form labels, contrast, image sizing, and reduced-motion behavior where applicable. Avoid decorative effects that harm readability or page responsiveness.
- When a runnable page is available, inspect desktop and mobile renders and exercise the main navigation/action within the authorized scope. Report mockup-only review and untested behavior honestly.

### UI and dashboards

Start from the user's operational decision. Every displayed metric or chart must answer a plausible question and have supported or clearly illustrative data. Show believable navigation, forms, tables, and states only where relevant. Keep data and design consistent across screens.

### Architecture and flows

Use Mermaid or SVG for precise diagrams and standard plotting tools for exact data charts. Show readable labels, directional connectors, supported components, and meaningful system boundaries. Avoid glowing pipelines, invented infrastructure, and a radiant central AI symbol.

### Raster visuals and generation briefs

Use image generation for requested raster concepts, illustrations, or hero imagery. Include objective, product context, composition, hierarchy, exact text, supported content, brand/semantic colors, plausible lighting/materials, specific exclusions, and aspect ratio in the brief. Avoid dumping the internal brief unless requested. Inspect local reference images before editing them and preserve unaffected regions.

### Existing designs

For a request to remove the AI look, first remove unjustified glow and gradients, flatten excessive gloss, reduce nonsemantic saturation, replace abstract AI motifs with product content, simplify badges/cards, and restore meaningful hierarchy. Preserve the product's identity and functionality.

## Scope vs Related Skills

| Need | Skill |
|---|---|
| Page strategy, section architecture, or a 12-category UI review | `@design-intelligence` |
| Design tokens and `DESIGN.md` as the source of visual truth, token linting, extracting a design system from a URL | `@design-md-enforcer` |
| Implementing a user-facing feature with product thinking and every UX state handled | `@claude-style-coding` |
| Removing generic AI aesthetics (glow, neon gradients, fake proof, uniform cards) and restoring product-specific hierarchy | `@anti-ai-slop-design` |

This skill is a corrective lens: it can run alone for an audit or "remove the AI look" request, or as a pass inside the other three. When more than one applies, follow the *Product Page Build Flow* in `@ecosystem-web`: tokens → page strategy → anti-slop check → implementation.

## Acceptance checks

Before delivery, confirm:

1. The product's main task is apparent without relying on a logo or generic slogan.
2. Effects support brand or meaning rather than substitute for hierarchy.
3. Components have purposeful grouping and importance rather than uniform decorative treatment.
4. Copy, data, claims, logos, and integrations are supported or explicitly illustrative.
5. Typography, contrast, content density, and device proportions are usable; web layouts preserve content order and actions on mobile.
6. The correction preserves requested scope and established identity.
7. The result avoids both generic AI spectacle and forced blandness.

For an audit, lead with the largest visible problem and recommend the few highest-impact changes. For creation or editing, deliver the result and briefly state meaningful changes and actual verification. Never claim checks that were not performed.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-web` — Web, Design & Delivery.

**Workflows:**
- **Product Page Build Flow** (`web-build-page`, step 3 of 5): next → `@claude-style-coding`.
- **UI Review Flow** (`web-review`, step 3 of 3): last step → once it passes, complete the workflow and report the outcome.
- **Remove the AI Look Flow** (`web-de-slop`, step 1 of 3): next → `@design-md-enforcer` *(optional)*.

**Direct handoffs:**
- `@ugc-crafter` — Imagery needs authentic, smartphone-style people or product shots.
- `@accessibility-enforcer` — The design is a mobile app screen.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-web`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
