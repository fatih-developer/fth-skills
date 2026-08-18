# Handoff Template

CREATE writes an immutable `YYYY-MM-DD-HHmm.md` (or `-N` on collision). Fill sections from verified session state. Omit metadata fields you cannot verify. Do not paste secrets.

```markdown
# Session Handoff

## Metadata

```yaml
session_id: 2026-08-18-1940
created: 2026-08-18T19:40:00+03:00
source_agent: codex
source_model: gpt-5.6
trigger: goal-completion
status: completed
goal_status: completed
topic: billing-system
working_directory: ...
branch: feat/billing
commit: ...
previous_session: 2026-08-18-1704
resumed_from: .claude/handoffs/2026-08-18-1830.md
```

## Objective

What this session was trying to accomplish.

## Current State

The actual repository/project state at handoff time.

## Work Completed

Meaningful completed work.

## Files Changed

Created, modified, deleted, or otherwise important files.

## Architecture & Decisions

Important technical/product decisions and why they were made.

## Database Changes

Schema, migrations, seed, queries, persistence changes, if relevant.

## API Changes

Endpoints, contracts, validation, auth behavior, if relevant.

## Frontend Changes

Pages, components, state, UI behavior, if relevant.

## Commands Executed

Only commands useful to continue or verify the work.

## Verification

Build, lint, typecheck, tests, manual verification, deployment checks.

Clearly distinguish: passed / failed / not run.

## Issues / Risks

Known defects, blockers, uncertainty, or risky assumptions.

## Remaining Work

Concrete unfinished work.

## Next Recommended Action

The single best next action for the next agent/session.

## Resume Instructions

Only special instructions required to continue safely.
```

When filling:

1. Be specific — paths and line numbers beat narrative.
2. Prioritize Current State, Next Recommended Action, and Resume Instructions.
3. Record lineage after a cross-agent resume (`source_agent`, `resumed_from`, `previous_session`).
4. Never invent branch, commit, or agent fields.
5. Leave irrelevant optional sections as `Not recorded.` rather than guessing.
