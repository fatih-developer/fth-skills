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

- [ ] Color tokens are compact and reusable.
- [ ] Typography scale is documented.
- [ ] Spacing scale is documented.
- [ ] Radius scale is documented.
- [ ] Shadow scale is documented.
- [ ] Semantic colors are documented.
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

- [ ] `DESIGN.md` is ready.
- [ ] `UI_RULES.md` is ready.
- [ ] `components.md` is ready.
- [ ] `tokens.css` is ready.
- [ ] `tailwind.theme.json` is ready if Tailwind is used.
- [ ] Agent instructions are clear.
