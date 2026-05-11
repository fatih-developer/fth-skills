# UI_RULES.md

## Purpose

Operational rules for AI coding agents applying the design system defined in `DESIGN.md`.

These rules are stricter than the design document. They define what the agent must and must not do during implementation.

## Mandatory Pre-Work

Before any UI-related change:

1. Read `DESIGN.md`.
2. Read `components.md`.
3. Check existing components before creating new ones.
4. Identify which tokens are needed.
5. Do not start implementation until visual rules are clear.

## Token Usage Rules

### Must Do

- Use CSS variables or Tailwind tokens from the design system.
- Use semantic token names like `primary`, `surface`, `text-muted`, `border`.
- Use spacing from the defined scale.
- Use radius from the defined radius scale.
- Use shadow from the defined shadow scale.

### Must Not Do

- Do not hard-code new hex colors in components.
- Do not invent new spacing values unless explicitly approved.
- Do not mix unrelated visual styles.
- Do not introduce one-off shadows.
- Do not add a new font without approval.

## Component Rules

### Button

- Use existing button variants first.
- Primary action: solid primary background.
- Secondary action: surface background with border.
- Destructive action: danger token.
- Minimum height: 44px.
- Include hover, active, disabled and focus states.

### Card

- Use consistent padding.
- Use border and/or subtle shadow.
- Avoid overcrowding content.
- Maintain clear title, body and action hierarchy.

### Form

- Every input must have a label or accessible name.
- Focus states must be visible.
- Error states must include text, not only color.
- Disabled states must be visually clear.

### Navigation

- Active state must be visible.
- Use muted text for inactive links.
- Keep spacing consistent.
- Avoid adding decorative complexity without purpose.

## Layout Rules

- Use max-width containers.
- Keep page sections visually separated.
- Use responsive grids.
- Do not create cramped layouts.
- Prefer 12-column or auto-fit grids depending on project type.

## Responsive Rules

- Desktop first visual richness is acceptable, but mobile must remain clean.
- Navigation may collapse on small screens.
- Multi-column grids should collapse to one column on mobile.
- Cards and forms must remain readable below 400px width.

## Accessibility Rules

- Maintain sufficient contrast.
- Add focus-visible styles.
- Use semantic HTML.
- Avoid tiny click targets.
- Do not remove outlines unless replacing with an accessible focus ring.

## Review Before Completion

Before finalizing any UI task, verify:

- No random visual values were introduced.
- The UI matches the design tone.
- Buttons, cards, forms and typography are consistent.
- Responsive behavior works.
- Empty/loading/error states are handled when relevant.
- The implementation does not copy protected brand assets unless the user owns them.
