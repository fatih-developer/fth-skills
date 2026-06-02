# Tool Profiles

Use these notes to tune the artifact to the target model or tool. Prefer stable behavioral guidance over fast-changing version trivia.

## ChatGPT

- Strong with structured prompts and explicit output contracts.
- Works best when the prompt separates role, task, constraints, and output shape.
- Use concise instructions unless the workflow is truly multi-step.

## Claude

- Strong with long-form reasoning, careful writing, and policy-sensitive tasks.
- Benefits from precise goals, bounded autonomy, and explicit stop conditions.
- For agentic tasks, define escalation and failure handling clearly.

## Gemini

- Useful for broad synthesis and long-context tasks.
- Keep sections clearly labeled.
- Avoid over-compressing instructions when many context sources are involved.

## Grok

- Prefer direct instructions and a visible task boundary.
- Keep prompts concrete and avoid relying on hidden conventions.

## Cursor

- Optimize for incremental edits, file awareness, and validation steps.
- Good prompts include codebase constraints, target files, and expected checks.

## Claude Code

- Good prompts define exploration, modification boundaries, validation expectations, and final reporting shape.
- Mention safety limits, test expectations, and scope control.

## Copilot

- Keep prompts compact and local to the coding task.
- Favor clear inline constraints and examples over long policy blocks.

## Midjourney

- Emphasize subject, composition, lighting, mood, texture, and camera language.
- Keep prompt dense and visual.
- State aspect ratio or framing requirements explicitly when needed.

## DALL-E

- Use plain, specific language.
- Strongly define subject, background, mood, and excluded elements.
- Prefer human-readable style guidance over shorthand-only syntax.

## Flux

- Works well with crisp visual descriptions and deliberate style constraints.
- Include composition, materials, lighting, and realism level.

## Calibration Pattern

When the user names a target model or tool:

1. preserve the core goal
2. adapt prompt structure to that tool
3. adjust verbosity
4. adjust how output contracts are expressed
5. adjust tool and workflow instructions if the target is an agentic environment
