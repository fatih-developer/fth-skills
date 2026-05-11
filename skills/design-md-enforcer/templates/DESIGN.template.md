---
name: "{{brand_name}} Design System"
version: "1.0.0"
source_url: "{{source_url}}"
generated_from: "visible website analysis"
status: "draft"
avoid_clone: true
---

# DESIGN.md

## 1. Design Intent

This document defines the visual language, design tokens, UI patterns and implementation rules for `{{brand_name}}`.

The system is derived from the visible design characteristics of the reference URL. It should be used to create original interfaces with similar quality, rhythm and consistency, not to produce a pixel-perfect clone.

## 2. Observed vs Inferred

### Observed

- {{observed_summary}}

### Inferred

- {{inferred_summary}}

### Limitations

- {{limitations}}

## 3. Visual Personality

- **Style direction:** {{style_direction}}
- **Visual density:** {{visual_density}}
- **Corner style:** {{corner_style}}
- **Shadow depth:** {{shadow_depth}}
- **Contrast level:** {{contrast_level}}
- **Layout rhythm:** {{layout_rhythm}}
- **Brand feel:** {{brand_feel}}

## 4. Color System

### Core Colors

| Token | Value | Usage |
|---|---:|---|
| `--bg` | `{{color_bg}}` | Main page background |
| `--bg-elevated` | `{{color_bg_elevated}}` | Elevated backgrounds |
| `--surface` | `{{color_surface}}` | Cards, panels, modals |
| `--surface-2` | `{{color_surface_2}}` | Secondary surfaces |
| `--border` | `{{color_border}}` | Borders and dividers |
| `--text` | `{{color_text}}` | Primary text |
| `--text-muted` | `{{color_text_muted}}` | Secondary text |
| `--primary` | `{{color_primary}}` | Primary actions, links, active states |
| `--primary-hover` | `{{color_primary_hover}}` | Primary hover state |
| `--accent` | `{{color_accent}}` | Highlights and supporting accents |

### Semantic Colors

| Token | Value | Usage |
|---|---:|---|
| `--success` | `{{color_success}}` | Success state |
| `--warning` | `{{color_warning}}` | Warning state |
| `--danger` | `{{color_danger}}` | Error/destructive state |
| `--info` | `{{color_info}}` | Informational state |

## 5. Typography

### Font Family

```css
font-family: {{font_family}};
```

### Type Scale

| Role | Size | Line Height | Weight | Usage |
|---|---:|---:|---:|---|
| Display | `{{font_display_size}}` | `{{font_display_line}}` | `{{font_display_weight}}` | Hero headlines |
| H1 | `{{font_h1_size}}` | `{{font_h1_line}}` | `{{font_h1_weight}}` | Page titles |
| H2 | `{{font_h2_size}}` | `{{font_h2_line}}` | `{{font_h2_weight}}` | Section titles |
| H3 | `{{font_h3_size}}` | `{{font_h3_line}}` | `{{font_h3_weight}}` | Card titles |
| Body | `{{font_body_size}}` | `{{font_body_line}}` | `{{font_body_weight}}` | Main content |
| Small | `{{font_small_size}}` | `{{font_small_line}}` | `{{font_small_weight}}` | Labels, captions |

## 6. Spacing System

Use a consistent spacing scale. Prefer these values instead of arbitrary spacing.

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
```

## 7. Radius System

```css
--radius-sm: {{radius_sm}};
--radius-md: {{radius_md}};
--radius-lg: {{radius_lg}};
--radius-xl: {{radius_xl}};
```

Usage:

- Small controls: `--radius-sm`
- Buttons and inputs: `--radius-md`
- Cards and panels: `--radius-lg`
- Hero panels and large surfaces: `--radius-xl`

## 8. Shadow System

```css
--shadow-sm: {{shadow_sm}};
--shadow-md: {{shadow_md}};
--shadow-lg: {{shadow_lg}};
```

Use shadows sparingly. Prefer borders for structure and shadows for elevation.

## 9. Layout Rules

- Container max width: `{{container_width}}`
- Page horizontal padding: `{{page_padding}}`
- Grid system: `{{grid_system}}`
- Section vertical spacing: `{{section_spacing}}`
- Responsive behavior: `{{responsive_behavior}}`

## 10. Component Rules

### Buttons

- Primary buttons use `--primary` background and white text.
- Hover state uses `--primary-hover`.
- Minimum height: `44px`.
- Border radius: `--radius-md`.
- Use clear visual hierarchy between primary and secondary actions.

### Cards

- Use `--surface` background.
- Use `--border` for structure.
- Use `--radius-lg` or `--radius-xl`.
- Internal padding should usually be `24px` or `32px`.

### Forms

- Inputs use `--bg-elevated` background.
- Border color: `--border`.
- Focus ring should use `--primary` with low opacity.
- Labels should be smaller and semibold/bold.

### Badges

- Use rounded pill shape.
- Use semantic colors with soft background.
- Keep badge text short.

## 11. Motion

- Motion style: {{motion_style}}
- Hover transitions should be subtle: `120ms-200ms ease`.
- Avoid excessive animation.

## 12. Accessibility Rules

- Maintain sufficient text/background contrast.
- Interactive elements must have visible focus states.
- Do not rely only on color for status.
- Minimum tap target height: `44px`.
- Use semantic HTML whenever possible.

## 13. Agent Instructions

When generating UI:

1. Read this file before making visual changes.
2. Use only the defined design tokens.
3. Do not invent random colors, spacing, radius or shadow values.
4. Prefer existing component patterns.
5. If a new component is needed, derive it from the closest existing pattern.
6. Generate a preview before applying the design to production code.
7. State clearly when a design decision is inferred rather than observed.
