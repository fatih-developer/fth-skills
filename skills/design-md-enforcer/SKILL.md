---
name: design-md-enforcer
description: Enforce and manage DESIGN.md specifications, combining design reasoning with token roles to prevent drift and ensure component consistency.
---

# Design MD Enforcer

## Purpose

The `design-md-enforcer` skill ensures that both human developers and AI agents follow a unified design system specification called `DESIGN.md`.

In traditional web development, design reasoning (style guides) and configuration values (like Tailwind config) are separated, leading to drift. This skill enforces a system where reasoning and raw values (hex codes, sizes) are bound together using **token roles**, and components reference these roles instead of hardcoding raw values.

## Core Philosophy: Logic Meets Values

1. **Tokens are Roles, Not Just Variables:**
   A token is not just a hex code; it represents a specific purpose or role in the design system.
   - Example: `primary` is not just `#0A1F1C`; it is the "main ink, text color" role.
   - Example: `body_main` is not just `18px`; it is the "default body copy" role.

2. **Components Reference Roles:**
   UI components must never hardcode static hex values. They must reference the token roles. If the role's value changes, all components referencing it are automatically updated.

3. **Reasoning is Required:**
   Every design decision must be accompanied by its reasoning (Why was this color chosen? What emotion does it reflect? Why this typography?).

## When To Use This Skill

Use this skill when the user asks to:
- Create a `DESIGN.md` specification for a new or existing project.
- Enforce design rules when an AI agent or developer is creating new UI components.
- Audit existing components to ensure they use proper token roles instead of hardcoded values.
- Validate color contrasts and design standards (e.g., WCAG).
- Refactor a tailwind or CSS config into a proper `DESIGN.md` unified spec.

## Workflow & Enforcements

### 1. Structure of DESIGN.md

When generating or updating a `DESIGN.md` file, always use the following structured format containing Front Matter (YAML) for tokens and components, followed by Markdown for reasoning.

```markdown
---
tokens:
  colors:
    primary:
      value: "#0A1F1C"
      role: "main ink, text color"
    accent:
      value: "#E27B58"
      role: "buttons and highlights"
    neutral:
      value: "#F5F5F5"
      role: "canvas and surfaces"
  typography:
    body_main:
      family: "sans-serif"
      size: "18px"
      role: "default body copy"

components:
  button_primary:
    background: "{tokens.colors.accent}"
    text: "{tokens.colors.primary}"
  button_primary_hover:
    extends: "button_primary"
    background: "{tokens.colors.primary}"
    text: "{tokens.colors.neutral}"
---

# Design System Reasoning

## Colors
**Deep Midnight Forest Green (Primary):** This color serves as the main ink of the project. It provides trust and maximizes readability for all main text and headings.

**Earthy Terracotta (Accent):** The preferred highlight color for call-to-actions (CTAs) and buttons. It represents natural energy and focus.

## Typography
The project's voice should be clear and friendly. Therefore, a sans-serif, easy-to-read 18px font is used for the main body copy.
```

### 2. Validation & Linting Requirements

When you or another agent create or modify design tokens and components, you MUST validate the decisions:
- **Contrast Check:** Verify that text colors over background colors pass WCAG accessibility standards (minimum 4.5:1 for normal text).
- **Token Integrity:** Ensure that components only reference existing tokens defined in the `tokens` block.
- **Role Consistency:** Check that the assigned token role makes logical sense for the component (e.g., don't use an `error` token for a standard 'continue' button).

If a validation fails, you must catch the error, correct the color or token reference, and explain the correction.

### 3. Component Hierarchy & Overrides

When defining components, promote the use of inheritance (`extends`). Instead of redefining every property for a hover state, extend the base component and only override the properties that change.

```yaml
components:
  card_base:
    background: "{tokens.colors.neutral}"
    border_radius: "8px"
  card_interactive:
    extends: "card_base"
    shadow: "0px 4px 12px rgba(0,0,0,0.1)"
```

## Agent Behavior

- **Never hardcode hex colors or px sizes** directly in HTML/CSS/Tailwind classes if a token exists for it.
- **If a token does not exist**, propose adding it to `DESIGN.md` along with its reasoning and role before using it in a component.
- Always read `DESIGN.md` before making any UI changes to understand the established roles and reasoning.
- Act as the strict gatekeeper: reject any UI code generation that violates the `DESIGN.md` specification.
