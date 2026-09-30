# Color Method (FOUNDATIONS)

Build color as a small system of roles derived from the product, the brand, and the competitive position. Colors are **flat fills**; the system has no gradients.

## 1. Inputs

- Brand colors and logo fills (read `fill`/`stroke` values from an SVG logo; sample raster logos and say the values are estimates).
- Domain materials from the research note.
- Competitor landscape (`landscape.json`): occupied and free accent hues.
- Constraints: dark mode required, data-dense UI, print or signage use, color-vision deficiency, cultural meaning in the target market.

## 2. Positioning against competitors

Pick one stance per direction and write it down:

| Stance | When | How |
|---|---|---|
| Differentiate by hue | The category shares one or two accent hues | Choose a primary from a free hue zone in `landscape.json` |
| Follow convention, differentiate elsewhere | Trust depends on a category color (health, finance, public sector) | Keep the conventional hue family; change neutral temperature, chroma level, typography, and shape |
| Keep the brand | An established brand color exists | Keep it; tune neutrals and semantic colors around it for contrast |

Offer 2-3 directions that differ in stance or hue, not three shades of the same idea.

## 3. Build order

1. **Neutrals first.** Background, surface, border, text, muted text. Tint them very slightly toward the primary hue or the domain material (OKLCH chroma below about 0.015) so they do not read as framework grey. Avoid the warm-cream + terracotta look and the slate-navy + cyan look (see `scripts/ai_defaults.json`).
2. **One primary.** The main action and selection color. It must pass 4.5:1 with its `on-primary` text and 3:1 against the background.
3. **At most one accent.** A different job from primary (focus ring, highlight, data emphasis). Never a second competing call to action.
4. **Semantic states.** Success, warning, danger (and info if needed) from stable hue families, each at least 3:1 against the background; use them only for state, always with a label or icon.
5. **Dark theme.** Not an inversion: raise lightness of chromatic roles, lower their chroma, use near-black neutrals with a slight tint rather than pure `#000`, and recheck every pair.

Use `python <skill-dir>/scripts/colorlib.py ramp <hex>` when a role needs a tonal scale (50-950) and `colorlib.py contrast <fg> <bg>` for spot checks.

## 4. Rules

- **No gradients.** Not in tokens, not in buttons, not as backgrounds or text fills. If an existing brand mandates one, keep it out of the token system, document it as a brand exception in `DESIGN.md`, and give a flat fallback color.
- **Proportion:** most of the surface is neutral; primary is a minority; accent is rare (60-30-10 is a starting heuristic, not a rule).
- **Saturation budget:** high chroma only where it carries meaning (primary action, state).
- **Color is never the only signal** for state, errors, links, or selection.
- **Contrast:** text 4.5:1 (7:1 preferred for long reading), large text and UI boundaries 3:1. `build_specimen.py` checks all role pairs and derives `border-strong` for inputs.

## 5. Validation

Run `build_specimen.py` on the directions file. Fix every `FAIL`. Treat `WARN` (template-default colors, directions too similar, cliché pairs) as a prompt to justify or change. Treat `INFO` about competitor hues as a positioning question to answer in the rationale.
