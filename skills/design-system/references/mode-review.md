# REVIEW Mode — Page Review and Token Lint

Review an existing page, screen, or implementation against the page rubric and against `DESIGN.md`.

## Step 1 — Gather information

- **Live URL:** render it if you can (browser tool), otherwise run `scan_site.py <url>` and ask for screenshots. State what you could and could not observe.
- **Code:** read the components, styles, and token files; identify the framework.
- **Image:** describe layout and patterns; do not claim measured values from an image.

## Step 2 — Score 12 categories (1-5)

| # | Category | Score | Justification |
|---|---|---|---|
| 1 | Message clarity | | |
| 2 | Hero focus | | |
| 3 | CTA clarity | | |
| 4 | Structure fits content | | |
| 5 | Visual hierarchy | | |
| 6 | Mobile usability | | |
| 7 | Touch comfort | | |
| 8 | Performance safety | | |
| 9 | Accessibility quality | | |
| 10 | Motion usefulness | | |
| 11 | Visual consistency | | |
| 12 | Advanced effects justification | | |

Detailed guidance per category: `references/review-rubric.md`.

## Step 3 — System lint

- **Tokens:** hardcoded hex values, off-scale font sizes, or radii that bypass `DESIGN.md`.
- **Gradients:** any `linear-gradient(`, `radial-gradient(`, or `conic-gradient(` outside a documented brand exception.
- **Contrast:** measure text/background pairs from the actual CSS (`colorlib.py contrast`).
- **Defaults:** overused or AI-favorite fonts (`find_fonts.py check`) and template-default colors (`scripts/ai_defaults.json`) without a stated reason.
- **Turkish text:** fallback glyphs in headings or buttons (a different-looking `ğ` or `İ` means the font lacks latin-ext).

## Step 4 — Classify issues

- **Critical:** damages clarity, usability, accessibility, performance, or the conversion path (hidden value proposition, unreadable contrast, missing primary CTA, broken mobile flow, no keyboard access, layout shift).
- **Important:** weakens quality without breaking the page (inconsistent spacing, token drift, weak secondary hierarchy, heavy media, mixed card patterns).
- **Nice to improve:** polish (proof order, CTA wording, type rhythm).

## Step 5 — Recommendation

```
## Final Recommendation: approve | revise | redesign
- approve: no critical issues; clear and usable
- revise: no structural failure, but important issues weaken it
- redesign: structurally confused, broken hero strategy, poor mobile, or systemic token drift
```

Lead with the largest problem and the few highest-impact fixes. Never report a check you did not run.
