---
name: react-flow-migration
description: Migrate React Flow codebases to modern @xyflow/react architecture. Use when users ask to upgrade old flow implementations, replace deprecated APIs, align types, preserve persisted graph data, or execute a low-risk migration plan with verification steps.
---

# React Flow Migration Protocol

Execute a safe migration in small, reviewable steps.

## Required Outputs

1. Produce current-state inventory (package versions, API usage, custom node/edge contracts).
2. Produce migration map (deprecated API to target API).
3. Apply ordered migration patches with compatibility notes.
4. Produce post-migration verification checklist and residual risks.

## Workflow

1. Inventory and baseline.
   - Detect current dependency (`reactflow` legacy or `@xyflow/react`).
   - Enumerate imports, hook usage, event handlers, and persistence format.
2. Define migration plan.
   - Map each legacy API to target API.
   - Flag breaking changes that affect runtime behavior.
3. Migrate types first.
   - Introduce shared node/edge type modules.
   - Remove `any` from node and edge data payloads where possible.
4. Migrate runtime wiring.
   - Update handlers (`onNodesChange`, `onEdgesChange`, `onConnect`) and edge creation flow.
   - Stabilize `nodeTypes` and `edgeTypes` references.
5. Preserve persisted data.
   - Validate serialized graph schema compatibility.
   - Add a lightweight migration guard for old payload versions when needed.
6. Verify and report.
   - Run available checks.
   - Report migrated files, behavior changes, and unresolved risks.

## Guardrails

- Prefer compatibility layers over large rewrites when delivery risk is high.
- Keep graph ids stable to avoid breaking edge references.
- Avoid changing product behavior unless it is an explicit bug fix.
- Document every breaking change and required manual follow-up.

## References

- Use `references/MIGRATION_CHECKLIST.md` for ordered execution.
- Use `references/API_RENAMES.md` for legacy-to-modern mapping.
- Use `references/EXAMPLES.md` for migration request patterns.

## Templates

- Use `templates/migration-plan.md.tmpl` as a patch-by-patch migration plan.
- Use `templates/compat-adapter.ts.tmpl` when temporary backward compatibility is required.
