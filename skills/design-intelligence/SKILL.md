---
name: design-intelligence
description: "Deprecated alias that routes to design-system (PAGE and REVIEW modes). Use only when the user explicitly invokes $design-intelligence; otherwise use design-system, which now covers page strategy, section architecture, and 12-category ui reviews."
---

# design-intelligence (Alias)

This skill was merged into `design-system` together with the new palette and typography research (FOUNDATIONS). Page strategy, section architecture, and 12-category UI reviews now live in its PAGE and REVIEW modes.

## What to do

1. If `design-system` is installed, invoke it and run its PAGE and REVIEW modes. Everything this skill used to do is there, with the same `DESIGN.md` token names.
2. If it is not installed, suggest the install command and do not run it without the user's approval:

   ```bash
   npx skills add fatih-developer/fth-skills --skill design-system
   ```

3. If the user declines, do the task directly: follow any existing `DESIGN.md`, use tokens instead of hardcoded values, keep colors flat (no gradients), check text contrast at 4.5:1, and state which checks you could not run.
