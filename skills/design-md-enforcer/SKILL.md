---
name: design-md-enforcer
description: "Deprecated alias that routes to fth-design-crafter (SPEC mode). Use only when the user explicitly invokes $design-md-enforcer; otherwise use fth-design-crafter, which now covers design.md, design tokens, extracting a design system from a url, and token linting."
---

# design-md-enforcer (Alias)

This skill was merged into `fth-design-crafter` together with the new palette and typography research (FOUNDATIONS). DESIGN.md, design tokens, extracting a design system from a URL, and token linting now live in its SPEC mode.

## What to do

1. If `fth-design-crafter` is installed, invoke it and run its SPEC mode. Everything this skill used to do is there, with the same `DESIGN.md` token names.
2. If it is not installed, suggest the install command and do not run it without the user's approval:

   ```bash
   npx skills add fatih-developer/fth-skills --skill fth-design-crafter
   ```

3. If the user declines, do the task directly: follow any existing `DESIGN.md`, use tokens instead of hardcoded values, keep colors flat (no gradients), check text contrast at 4.5:1, and state which checks you could not run.
