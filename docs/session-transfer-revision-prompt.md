# Session Transfer Skill Revision Prompt

Update the existing `session-transfer` skill to support agent-aware, indexed, automatic session handoffs across Codex, Claude Code, OpenCode, and unknown/future agents.

The goal is to turn `session-transfer` from a simple manual session-summary skill into a reusable **session continuity protocol** that can automatically persist, index, discover, and resume substantial development work across different coding agents.

## 1. Preserve the Existing Skill Intent

Keep the original purpose of `session-transfer`:

- Capture the state of meaningful work before a session ends or context is lost.
- Allow a new session or another agent to continue with minimal ambiguity.
- Support explicit CREATE and RESUME behavior.
- Avoid requiring the next agent to reconstruct the entire terminal/chat history.

Do not unnecessarily rewrite unrelated parts of the skill.

---

## 2. Agent-Aware Storage

Before creating a handoff, detect the active agent/runtime.

Use this directory mapping:

- Codex → `.codex`
- Claude Code → `.claude`
- OpenCode → `.opencode`
- Unknown / unsupported runtime → `.agent`

Do not identify the active runtime only from the existence of a directory. A repository may contain `.codex`, `.claude`, and `.opencode` at the same time.

Use signals in this priority order where available:

1. Runtime/environment signals
2. Agent-specific execution/configuration context
3. Explicit user instruction
4. Reliable agent self-identification
5. Existing agent directory only as a weak supporting signal
6. Fallback to `.agent`

The skill must remain portable and must not become Codex-specific.

---

## 3. Handoff Directory Structure

For the detected agent, use:

```text
<agent-dir>/
├── INDEX.md
├── handoffs.jsonl
└── handoffs/
    └── YYYY-MM-DD-HHmm.md
```

Examples:

```text
.codex/handoffs/2026-08-18-1704.md
.claude/handoffs/2026-08-18-1830.md
.opencode/handoffs/2026-08-19-0915.md
```

Use local project time where reliably available.

The timestamped handoff file is immutable session history. Do not overwrite an older timestamped handoff.

If a timestamp collision occurs, append a safe deterministic suffix.

---

## 4. Global Session Transfer Index

Create and maintain a cross-agent index:

```text
.session-transfer/
└── INDEX.md
```

This is the primary navigation/state layer for RESUME.

It should contain at minimum:

- current/recommended handoff
- active or last source agent
- topic
- status
- branch if available
- next recommended action
- recent handoffs across all supported agents

Do not duplicate the full handoff contents in the global index.

The global index should allow a new agent to find the correct continuation without scanning every handoff file.

---

## 5. Agent-Specific INDEX.md

Each agent directory should maintain its own `INDEX.md`.

Example information:

```markdown
# Codex Session Index

Last updated: 2026-08-18 19:42

## Current Session

- Handoff: `handoffs/2026-08-18-1940.md`
- Topic: Dashboard UI
- Status: In Progress
- Branch: main
- Next Action: Complete filtering integration

## Recent Sessions

| Date | Session | Topic | Status | Branch |
|---|---|---|---|---|
| 2026-08-18 19:40 | `2026-08-18-1940` | Dashboard UI | In Progress | main |
| 2026-08-18 18:30 | `2026-08-18-1830` | Auth API | Completed | main |
```

Keep this file lightweight.

Do not require reading all handoff files to rebuild the current state during normal RESUME.

---

## 6. Machine-Readable Registry

Maintain:

```text
<agent-dir>/handoffs.jsonl
```

Use JSONL rather than one large JSON document.

Each line should represent one handoff and contain compact metadata, for example:

```json
{"id":"2026-08-18-1940","created":"2026-08-18T19:40:00+03:00","agent":"codex","topic":"dashboard-ui","status":"in-progress","trigger":"substantial-work","branch":"main","file":"handoffs/2026-08-18-1940.md","previous_session":"2026-08-18-1830"}
```

Include fields only when known; do not fabricate repository state.

Recommended fields:

- `id`
- `created`
- `agent`
- `topic`
- `status`
- `trigger`
- `branch`
- `commit`
- `file`
- `previous_session`
- `resumed_from`
- `goal_status`

The registry should make it easy to identify:

- latest session
- latest unfinished session
- sessions by topic
- sessions by branch
- sessions by agent
- cross-agent handoff chains

---

## 7. Handoff Metadata

Each handoff should contain a compact metadata section.

Include when available:

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

Do not invent values that cannot be verified.

---

## 8. Standard Handoff Content

A created handoff must be detailed enough for a fresh agent session to continue without terminal/chat transcript access.

Use this structure unless the existing skill has an equivalent or better structure:

```markdown
# Session Handoff

## Metadata

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

Clearly distinguish:
- passed
- failed
- not run

## Issues / Risks

Known defects, blockers, uncertainty, or risky assumptions.

## Remaining Work

Concrete unfinished work.

## Next Recommended Action

The single best next action for the next agent/session.

## Resume Instructions

Only special instructions required to continue safely.
```

Avoid verbose narrative that does not help continuation.

---

## 9. CREATE Mode

CREATE must:

1. Detect the active runtime/agent.
2. Inspect the current repository/work state needed for an accurate handoff.
3. Determine the session status.
4. Generate a timestamped immutable handoff.
5. Append/update the agent `handoffs.jsonl`.
6. Update the agent `INDEX.md`.
7. Update `.session-transfer/INDEX.md`.
8. Return only a concise terminal/chat confirmation unless the user explicitly asks for the full handoff content.

Example final response:

```text
Session handoff created.
Status: completed
Handoff: .codex/handoffs/2026-08-18-1709.md
Global index updated: .session-transfer/INDEX.md
```

Do not print the entire handoff to the terminal by default.

---

## 10. RESUME Mode

RESUME must prioritize fast, low-context navigation.

Default algorithm:

1. Read `.session-transfer/INDEX.md` first if it exists.
2. Identify the current/recommended/latest relevant handoff.
3. Prefer the current agent's relevant unfinished handoff when appropriate.
4. If there is no suitable current-agent handoff, allow cross-agent resume.
5. Read only the selected handoff initially.
6. Inspect current git/repository state.
7. Verify that referenced files/state still match reality.
8. Detect changes made after the handoff.
9. Continue from `Next Recommended Action` only after reconciliation.

Never blindly trust a stale handoff over the current repository.

If the global index is missing or corrupted, fall back to agent indexes and then handoff metadata.

Do not scan every historical handoff unless necessary.

---

## 11. Cross-Agent Resume

The skill must explicitly support:

```text
Codex → Claude Code
Claude Code → Codex
Codex → OpenCode
OpenCode → Claude Code
etc.
```

A new agent should be able to resume the latest compatible handoff created by a different agent.

When a new handoff is later created, record lineage using fields such as:

```yaml
source_agent: claude
resumed_from: .codex/handoffs/2026-08-18-1704.md
previous_session: 2026-08-18-1704
```

The handoff chain must remain discoverable even when the active agent changes.

---

## 12. Automatic Trigger Policy

`session-transfer` must not be purely manual.

Add an explicit automatic-trigger policy.

Automatically invoke CREATE when meaningful work reaches a logical boundary.

### Substantial Work Trigger

Treat work as substantial when one or more of these apply:

- a feature/module was implemented
- architecture materially changed
- database schema/migration changed
- API contract changed
- authentication/security behavior changed
- deployment/infrastructure changed
- 5+ meaningful files were modified
- implementation required multiple phases
- a meaningful build/test/debug cycle was performed
- the session consumed substantial context
- remaining work must continue later
- interruption would force the next agent to reconstruct important state

The number of files is only one signal. A critical one-file architectural, migration, security, or contract change can still require a handoff.

Do not generate automatic handoffs for trivial edits such as a tiny copy change, simple formatting, or an isolated low-impact fix.

---

## 13. Logical Boundary / Anti-Spam Rule

Use this principle:

> One automatic handoff per logical work boundary.

A large goal with many implementation substeps should normally create one handoff at the end, not one after every substep.

Create intermediate handoffs only when:

- context pressure threatens reliable continuation
- the active agent is changing
- the work is being interrupted
- a major checkpoint needs explicit persistence
- the user explicitly requests one

Prevent handoff spam.

---

## 14. Mandatory `/goal` Completion Contract

Integrate `session-transfer` as a required terminal step for `/goal` workflows.

Every `/goal` execution that performed meaningful work must end with CREATE before the goal is considered closed.

This applies when the goal is:

- completed
- partially completed
- blocked
- interrupted/aborted after meaningful work

Suggested lifecycle:

```text
/goal
  ↓
Understand goal
  ↓
Inspect repository
  ↓
Implement
  ↓
Test / verify
  ↓
Determine final status
  ↓
session-transfer CREATE
  ↓
Update indexes
  ↓
Concise final response
```

Define the completion contract as:

```text
Implementation ✓
Verification   ✓
Handoff        ✓
Index update   ✓
----------------
GOAL DONE      ✓
```

Do not mark the goal complete before persistence/indexing succeeds.

Important: do not introduce or depend on unrelated goal workflow skills. Keep this integration limited to the `session-transfer` terminal handoff contract.

---

## 15. Context-Pressure Trigger

If the runtime exposes context pressure or remaining-context information, create an in-progress handoff before context exhaustion threatens reliable completion.

Do not hard-code a percentage that only works for one agent.

Use a portable rule:

> When the runtime indicates remaining context is becoming low enough to threaten reliable completion, persist an in-progress handoff before continuing, switching sessions, or terminating.

If the runtime provides no context signal, rely on reasonable session-length/complexity indicators without pretending to know a percentage.

Use:

```yaml
trigger: context-pressure
status: in-progress
```

when applicable.

---

## 16. Trigger Types

Normalize trigger metadata to values such as:

```text
manual
goal-completion
substantial-work
context-pressure
agent-transfer
interrupted
```

Add more only if they provide real value.

---

## 17. Status Model

Use a simple, consistent status model.

Preferred values:

```text
completed
in-progress
partial
blocked
interrupted
```

For `/goal`, optionally maintain `goal_status` separately when useful.

Do not create unnecessary status complexity.

---

## 18. Recovery and Self-Healing

Index files are navigation/state aids; timestamped handoffs are historical records.

If an index is missing, stale, or corrupted:

1. Do not delete handoffs.
2. Reconstruct the smallest necessary index from available handoff metadata / JSONL.
3. Preserve history.
4. Report the repair concisely.

If `handoffs.jsonl` and Markdown indexes disagree, verify against actual handoff files and repository state instead of silently guessing.

---

## 19. Token / Context Efficiency

This revision should explicitly optimize for coding-agent context usage.

Rules:

- Read global index before handoff history.
- Read one selected handoff before exploring older sessions.
- Do not load every historical handoff by default.
- Keep indexes compact.
- Keep registry entries compact.
- Avoid repeating full handoff content in indexes.
- Avoid printing long handoffs to terminal/chat after CREATE.
- Prefer precise repository verification over replaying chat history.

The system should make long Codex/Claude/OpenCode sessions easier to transfer without excessive token usage.

---

## 20. Compatibility

Do not assume only Codex, Claude Code, and OpenCode will exist.

Implement the mapping in a way that can be extended later.

Unknown agents must safely use:

```text
.agent/
```

The skill must work even when the repository contains multiple agent-specific directories.

---

## 21. Documentation Update

Update the skill documentation/README if one exists.

Document at minimum:

- CREATE
- RESUME
- automatic triggers
- `/goal` completion behavior
- supported agent directories
- `.session-transfer/INDEX.md`
- agent `INDEX.md`
- `handoffs.jsonl`
- timestamp naming
- cross-agent resume
- context-pressure behavior
- fallback behavior

Include concise examples:

```text
Use session-transfer to create a handoff.
```

```text
Use session-transfer to resume the latest session.
```

```text
Use session-transfer to resume the latest unfinished billing work.
```

```text
/goal ... 
# session-transfer runs as the terminal persistence step
```

---

## 22. Verification Requirements

After modifying the skill, verify the result against these scenarios:

### Scenario A — Codex CREATE
Expected:

```text
.codex/handoffs/<timestamp>.md
.codex/INDEX.md
.codex/handoffs.jsonl
.session-transfer/INDEX.md
```

### Scenario B — Claude CREATE
Expected:

```text
.claude/handoffs/<timestamp>.md
.claude/INDEX.md
.claude/handoffs.jsonl
.session-transfer/INDEX.md
```

### Scenario C — Cross-Agent RESUME
A Claude session can resume a Codex handoff without scanning every Codex handoff.

### Scenario D — Goal Completion
A substantial `/goal` cannot close without a persisted handoff and updated indexes.

### Scenario E — Partial/Blocked Goal
The handoff is still generated with the correct status and remaining work.

### Scenario F — Context Pressure
An in-progress handoff is created before the session becomes unreliable.

### Scenario G — Trivial Edit
No automatic handoff is created.

### Scenario H — Index Missing
The skill can safely rebuild navigation from historical records without deleting them.

### Scenario I — Multiple Agent Folders Exist
The runtime is not misidentified merely because `.codex`, `.claude`, or `.opencode` directories already exist.

---

## 23. Final Deliverables

Complete the revision, do not stop at a proposal.

At minimum:

1. Update the existing `session-transfer` skill file(s).
2. Update README/documentation if present.
3. Preserve useful existing behavior.
4. Add agent-aware paths.
5. Add timestamped immutable handoffs.
6. Add per-agent indexes.
7. Add per-agent JSONL registries.
8. Add global `.session-transfer/INDEX.md`.
9. Add cross-agent resume behavior.
10. Add automatic substantial-work trigger.
11. Add mandatory `/goal` terminal handoff rule.
12. Add context-pressure persistence.
13. Add anti-spam/logical-boundary behavior.
14. Add recovery rules.
15. Verify the scenarios above.

At the end, provide a concise summary of:
- files changed
- major behavior changes
- verification performed
- any remaining limitations

Do not merely describe what should change. Apply the changes to the skill.
