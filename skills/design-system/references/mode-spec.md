# SPEC Mode — DESIGN.md and Tokens

`DESIGN.md` is the single source of visual truth for people and agents. Tokens are **roles**, not raw values, and every decision carries its reason.

## Principles

1. **Tokens are roles.** `--primary` is "main action and current selection", not just `#1f5d4c`. `--fs-body` is "default reading size", not just `16px`.
2. **Components reference roles.** Components never hardcode hex or pixel values; changing a role updates every component that uses it.
3. **Reasoning is required.** Each color and type decision states why it fits this product, with the evidence from `design-research.md`. Describe the intended feel in product terms, for example:

   ```markdown
   # Rota Kargo — Style Reference
   > Freight paperwork, calm operations. Off-white document paper, container-green actions,
   > signal amber only for exceptions. Compact label-like headlines; highly legible body text
   > for addresses and tracking codes.
   ```

   Avoid atmosphere copy that describes effects instead of the product ("glowing", "frosted glass", "futuristic command center").

## Workflow A — From chosen direction to DESIGN.md

1. Run `build_specimen.py <directions.json> --export <id> --out-dir design/`. It writes `DESIGN.md` (intent, rationale, evidence, color and type tables, open checks), `tokens.css`, `tailwind.theme.json`, and `design-tokens.json`.
2. Complete `DESIGN.md` from `templates/DESIGN.template.md`: components (`templates/components.template.md`), layout and UI rules (`templates/UI_RULES.template.md`), and the review checklist (`templates/review-checklist.template.md`).
3. Render `templates/preview.template.html` with the tokens so the team sees buttons, forms, cards, and states in the real system.

## Workflow B — Extract a design system from a URL

1. Run `scan_site.py <url>` for measured colors, fonts, and gradient use. If you can render the page (browser tool or screenshots), add radius, spacing, and component observations; otherwise ask for screenshots or CSS.
2. Write the package to `design-md/<site-name>/` with at least `DESIGN.md` and `preview.html`. Separate **observed** from **inferred** values and state limitations. See `examples/example-input.yaml` and `examples/example-design-analysis.json` (its `Inter` value is an observed fact about the analyzed site, not a recommendation).
3. The extraction documents a reference; it does not license a clone. Mark `avoid_clone: true` in the frontmatter.

## Structure rules for DESIGN.md

- Token tables use `Token | Value | Role` (or light/dark value columns); no loose lists of hex codes.
- Components are declared in YAML or tables that reference tokens, and use inheritance (`extends`) for variants such as hover or disabled instead of repeating every property.
- A "Rules" section lists: no gradients (or the documented brand exception), color never the only signal, one primary action per view, and the contrast results.

## Validation and linting

When you or another agent create or change tokens or components:

- **Contrast:** text 4.5:1, large text and UI boundaries 3:1; rerun `build_specimen.py` or `colorlib.py contrast`.
- **Token integrity:** components reference only tokens defined in `DESIGN.md`.
- **Role consistency:** a token's use matches its role (no `--danger` for decoration, no `--accent` as a second primary).
- **Drift:** search the code for hardcoded hex values, `px` font sizes, and `linear-gradient(`/`radial-gradient(`/`conic-gradient(` that bypass tokens.

If a check fails, fix the value or the reference and explain the correction.

## Agent behavior

- Read `DESIGN.md` before any UI change.
- Never hardcode a color or size when a token exists; if a token is missing, propose it in `DESIGN.md` with its role and reason first.
- Reject UI changes that violate `DESIGN.md`, and say which rule they break.
