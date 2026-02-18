# Example Usage

## Example 1: Existing project repair

User request:
- "Use react-flow skill, inspect my flow editor, and fix broken edge updates."

Expected behavior:
- Produce a short audit.
- Identify the broken handler wiring.
- Apply minimal patch to `onConnect` and state update flow.
- Provide quick verification steps.

## Example 2: Performance-focused pass

User request:
- "Audit React Flow rendering performance and apply safe fixes."

Expected behavior:
- Identify unstable `nodeTypes` / `edgeTypes` references.
- Identify expensive custom nodes lacking memoization.
- Apply low-risk optimizations.
- Report residual risks for very large graph workloads.

## Example 3: From scratch setup

User request:
- "Create a typed React Flow starter with one custom node and deterministic layout."

Expected behavior:
- Generate baseline files from templates.
- Keep strict typing for node and edge models.
- Include working connect behavior and starter layout helper.