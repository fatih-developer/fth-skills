---
name: design-md-enforcer
description: "Create and enforce DESIGN.md design-system specifications: extract tokens from a URL or codebase, define color, type, spacing, and component roles, and lint implementations against them to prevent drift. Use when the user wants a design system, design tokens, a DESIGN.md file, or to check UI code for design consistency."
---

# Design MD Enforcer

## Purpose

The `design-md-enforcer` skill ensures that both human developers and AI agents follow a unified design system specification called `DESIGN.md`.

It serves two primary functions:
1. **Extraction:** Analyzing the visible design language of a public URL and converting it into an AI-agent-friendly design system package.
2. **Enforcement:** Enforcing a system where design reasoning and raw values (hex codes, sizes) are bound together using **token roles**, preventing drift between style guides and code.

## Core Philosophy: Logic Meets Values

1. **Tokens are Roles, Not Just Variables:**
   A token is not just a hex code; it represents a specific purpose or role in the design system.
   - Example: `primary` is not just `#0A1F1C`; it is the "main ink, text color" role.
   - Example: `body_main` is not just `18px`; it is the "default body copy" role.

2. **Components Reference Roles:**
   UI components must never hardcode static hex values. They must reference the token roles. If the role's value changes, all components referencing it are automatically updated.

3. **Reasoning is Required (Thematic Storytelling):**
   Every design decision must be accompanied by its reasoning and a thematic style reference. For example, don't just list colors; describe the overall aesthetic (e.g., "> Midnight Command Center. Imagine a high-tech dashboard glowing softly in a dark room...").

## When To Use This Skill

Use this skill when the user asks to:
- Extract a website's design language from a URL.
- Create a `DESIGN.md` specification from a reference site or for a new project.
- Enforce design rules when an AI agent or developer is creating new UI components.
- Validate color contrasts and design standards (e.g., WCAG).
- Refactor a tailwind or CSS config into a proper `DESIGN.md` unified spec.

## Resource Usage

This skill contains pre-built templates and examples to help you generate accurate outputs. Always use them as your primary reference:
- Read `templates/` (relative to this skill directory: `components.template.md`, `DESIGN.template.md`, `UI_RULES.template.md`, `review-checklist.template.md`, `preview.template.html`, `tokens.template.css`, `tailwind.theme.template.json`) for the exact structure of `DESIGN.md`, `preview.html`, and token files.
- Review `examples/` (`example-input.yaml`, `example-design-analysis.json`) if you are unsure how a high-quality output should look.

## Workflow 1: Extracting Design from a URL

When asked to extract a design from a URL, follow these steps:

### 1. Collect Evidence (Non-Browser LLM Support)
If you do not have native browser capabilities (like a visual subagent), you MUST use alternative methods:
- Fetch the raw HTML and extract inline styles, CSS variable declarations (`:root`), and class names.
- Ask the user to provide screenshots of the website and use vision models to extract hex codes, fonts, and border radii.
- Ask the user to paste the CSS file content.
- Be explicit about what was observed vs inferred. If you cannot render the site visually, state the limitations.

### 2. Output Generation Rules (Strict Pathing)
Do not output files directly to the root workspace. Always generate the extracted design system inside a dedicated standard folder:
**`/design-md/<site-name>/`**

You MUST produce the following minimum files in this folder:
- `/design-md/<site-name>/DESIGN.md`: The core specification using detailed markdown tables and reasoning.
- `/design-md/<site-name>/preview.html`: A standalone HTML file demonstrating the extracted components (Hero section, Button variants, Cards, Form controls, Color swatches, etc.) so the user can visually verify the system.

## Workflow 2: Enforcing the Specification

### 1. Structure of DESIGN.md

When generating or updating a `DESIGN.md` file, you MUST use detailed Markdown tables and incorporate thematic reasoning.

**Theme / Style Reference Example:**
```markdown
# AuthKit — Style Reference
> Midnight Command Center. Imagine a high-tech dashboard glowing softly in a dark room, with frosted glass elements reflecting minimal light.

**Theme:** dark
```

**Tokens Table Example:**
Do not use simple lists for tokens in the body. Use a strict Markdown table format with `Name | Value | Role`.

```markdown
## Colors

| Name | Value | Role |
|---|---|---|
| Midnight Abyss | `#05060f` | Page backgrounds, elevated card backgrounds, deep shadows. |
| Ghost White | `#ffffff` | Primary text for headings and high-contrast elements, icon fills. |
| Storm Gray | `#2f343` | Subtle shadows, secondary background for interactive states. |
| Comet | `#d8ecf8` | Primary body text, prominent links, and headings; high readability. |
| Celestial Light | `#b6d9fc` | Focus states for interactive elements, subtle highlights. |
```

**Components Block:**
Use YAML (or standard markdown code blocks) to define components inheriting these tokens.
```yaml
components:
  button_primary:
    background: "{tokens.colors.Comet}"
    text: "{tokens.colors.Midnight Abyss}"
```

### 2. Validation & Linting Requirements

When you or another agent create or modify design tokens and components, you MUST validate the decisions:
- **Contrast Check:** Verify that text colors over background colors pass WCAG accessibility standards (minimum 4.5:1 for normal text).
- **Token Integrity:** Ensure that components only reference existing tokens defined in the `DESIGN.md` tables.
- **Role Consistency:** Check that the assigned token role makes logical sense for the component.

If a validation fails, you must catch the error, correct the color or token reference, and explain the correction.

### 3. Component Hierarchy & Overrides

When defining components, promote the use of inheritance (`extends`). Instead of redefining every property for a hover state, extend the base component and only override the properties that change.

## Agent Behavior

- **Never hardcode hex colors or px sizes** directly in HTML/CSS/Tailwind classes if a token exists for it.
- **If a token does not exist**, propose adding it to `DESIGN.md` along with its reasoning and role before using it in a component.
- Always read `DESIGN.md` before making any UI changes to understand the established roles and reasoning.
- Act as the strict gatekeeper: reject any UI code generation that violates the `DESIGN.md` specification.

## Scope vs Related Skills

| Need | Skill |
|---|---|
| Page strategy, section architecture, or a 12-category UI review | `@design-intelligence` |
| Design tokens and `DESIGN.md` as the source of visual truth, token linting, extracting a design system from a URL | `@design-md-enforcer` |
| Implementing a user-facing feature with product thinking and every UX state handled | `@claude-style-coding` |

When more than one applies, run them in the order of the *Product Page Build Flow* in `@ecosystem-web`: tokens → page strategy → implementation.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-web` — Web, Design & Delivery.

**Workflows:**
- **Product Page Build Flow** (`web-build-page`, step 1 of 4): next → `@design-intelligence`.
- **UI Review Flow** (`web-review`, step 2 of 2): last step → summarize the workflow outcome.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-web`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
