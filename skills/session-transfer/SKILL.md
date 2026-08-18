---
name: session-transfer
description: 'Create and resume agent-aware session handoffs across Codex, Claude Code, OpenCode, and unknown runtimes. Triggers on save state, create handoff, resume latest session, context pressure, /goal completion, or continue where we left off. Persists indexed, immutable handoffs so a new session can continue without chat or terminal history.'
---

# Session Transfer

Persist substantial work as an immutable, indexed handoff so a later session — or a different coding agent — can continue without reconstructing chat or terminal history.

## Mode Selection

**CREATE** — save state, pause, context is getting full, `/goal` is closing, or an automatic trigger fires.

**RESUME** — continue previous work, load the latest session, or resume unfinished work on a topic.

Do not treat this skill as Codex-only. Detect the active runtime, then write under that agent’s directory.

## Agent Detection

Before CREATE or RESUME, detect the active runtime. Do **not** pick Codex, Claude Code, or OpenCode just because `.codex`, `.claude`, or `.opencode` already exist (a repo may contain all three).

Signal priority:

1. Runtime / environment signals (`CODEX_*`, `CLAUDECODE` / `CLAUDE_CODE*`, `OPENCODE*`)
2. Agent-specific execution or configuration context
3. Explicit user instruction (`--agent`, or “create this as a Claude handoff”)
4. Reliable agent self-identification
5. Existing agent directory only as a weak supporting signal — never the sole reason
6. Fallback: unknown / future runtime → `.agent`

Directory mapping:

| Runtime | Directory |
|---------|-----------|
| Codex | `.codex` |
| Claude Code | `.claude` |
| OpenCode | `.opencode` |
| Unknown / future | `.agent` |

## Storage Layout

```text
<agent-dir>/
├── INDEX.md
├── handoffs.jsonl
└── handoffs/
    └── YYYY-MM-DD-HHmm.md

.session-transfer/
└── INDEX.md
```

Examples: `.codex/handoffs/2026-08-18-1704.md`, `.claude/handoffs/2026-08-18-1830.md`.

Use local project time when reliable. Timestamped files are immutable history — never overwrite an older one. On collision append a deterministic suffix (`-2`, `-3`, …). Older `YYYY-MM-DD-HHMMSS-slug.md` files stay readable for RESUME.

`.session-transfer/INDEX.md` is the primary navigation layer: current/recommended handoff, last source agent, topic, status, branch if known, next recommended action, recent cross-agent handoffs. Keep it compact. Do not copy full handoff bodies into any index. Do not invent git, repo, or agent fields you cannot verify.

Each agent `INDEX.md` is a lightweight current + recent table. `handoffs.jsonl` is one compact JSON object per line (fields only when known): `id`, `created`, `agent`, `topic`, `status`, `trigger`, `branch`, `commit`, `file`, `previous_session`, `resumed_from`, `goal_status`.

## Status and Triggers

Status: `completed` | `in-progress` | `partial` | `blocked` | `interrupted`

Trigger: `manual` | `goal-completion` | `substantial-work` | `context-pressure` | `agent-transfer` | `interrupted`

Optional `goal_status` may track `/goal` outcome separately. Do not invent extra statuses or triggers.

## CREATE

Run the shipped helper (it detects the agent, writes the handoff, appends JSONL, and rewrites both indexes):

```bash
python skills/session-transfer/scripts/create_handoff.py <topic> --status <status> --trigger <trigger>
```

Useful flags: `--agent`, `--workspace`, `--branch`, `--commit`, `--goal-status`, `--next-action`, `--continues-from`, `--resumed-from`. Pass known fields; omit unknown ones.

1. Detect the runtime (priority above).
2. Inspect current repo/work state needed for an accurate handoff (git branch/commit/modified files when available).
3. Determine status and trigger from the vocabularies above.
4. Write `handoffs/YYYY-MM-DD-HHmm.md` (suffix on collision).
5. Append one JSONL line.
6. Update `<agent-dir>/INDEX.md` and `.session-transfer/INDEX.md`.
7. Reply with a concise confirmation only unless the user asks for the full document:

```text
Session handoff created.
Status: completed
Handoff: .codex/handoffs/2026-08-18-1709.md
Global index updated: .session-transfer/INDEX.md
```

Fill the handoff so a fresh session can continue without chat/terminal history. Use `references/handoff-template.md`. Include compact YAML metadata when known (`session_id`, `created`, `source_agent`, `source_model`, `trigger`, `status`, `goal_status`, `topic`, `working_directory`, `branch`, `commit`, `previous_session`, `resumed_from`). Prefer precise file paths, decisions, verification outcomes (passed / failed / not run), remaining work, and a single **Next Recommended Action**.

Then validate:

```bash
python skills/session-transfer/scripts/validate_handoff.py <handoff-file>
```

Do not finalize if secrets are detected or the score is below 70. After a cross-agent resume, the next CREATE must record lineage: `source_agent`, `resumed_from`, `previous_session`.

## RESUME

Prefer fast, low-context navigation. Do not scan every historical handoff unless indexes are missing.

```bash
python skills/session-transfer/scripts/resume_handoff.py
python skills/session-transfer/scripts/list_handoffs.py
python skills/session-transfer/scripts/check_staleness.py <handoff-file>
```

1. Read `.session-transfer/INDEX.md` first when present.
2. Prefer the current agent’s relevant unfinished handoff.
3. Otherwise resume the latest compatible cross-agent handoff (Codex ↔ Claude Code ↔ OpenCode ↔ `.agent`).
4. Read only the selected handoff initially.
5. Inspect current git/repo state. Verify referenced files still exist. Detect changes after the handoff (`check_staleness.py`: FRESH / SLIGHTLY_STALE / STALE / VERY_STALE).
6. Continue from **Next Recommended Action** only after reconciliation. Never blindly trust a stale handoff over the repository.

If the global index is missing or corrupted: fall back to agent `INDEX.md`, then JSONL / handoff metadata. Reconstruct the smallest needed index with the resume `--recover` path (or `recover_indexes`); never delete timestamped handoffs. If JSONL and Markdown indexes disagree, verify against actual handoff files and repo state.

Follow `references/resume-checklist.md`. For chained work, read the newest handoff first; open a predecessor only if needed.

## Automatic CREATE

Not purely manual. At most **one automatic handoff per logical work boundary**.

Treat work as substantial when any of these apply: feature/module implemented; architecture, schema/migration, API contract, auth/security, or deploy/infra changed; 5+ meaningful files; multi-phase work; meaningful build/test/debug; large context; continuation would otherwise require reconstructing state. A critical one-file architecture, migration, security, or contract change still qualifies.

Do **not** auto-CREATE for a tiny copy change, simple formatting, or an isolated low-impact fix.

A large `/goal` with many substeps gets one handoff at the end, not one after every substep. Intermediate auto-handoffs only when: context pressure, agent change, interruption, an explicit checkpoint, or an explicit user request.

### Context pressure

When the runtime indicates remaining context is low enough to threaten reliable completion, persist before continuing or stopping:

```yaml
trigger: context-pressure
status: in-progress
```

Do not hard-code a percentage that only works for one agent. If there is no context signal, use session-length / complexity indicators — do not invent a percent.

### `/goal` completion contract

Every `/goal` that performed meaningful work (completed, partial, blocked, or interrupted/aborted) must run CREATE and succeed at persistence/indexing before the goal is considered closed. Do not add or depend on other goal-workflow skills.

```text
/goal → implement → verify → determine status → session-transfer CREATE → indexes → concise reply

Implementation ✓
Verification   ✓
Handoff        ✓
Index update   ✓
----------------
GOAL DONE      ✓
```

## Recovery

Indexes are navigation. Timestamped handoffs are history. If an index is missing, stale, or corrupted: do not delete handoffs; rebuild the smallest index from JSONL / handoff metadata; report the repair concisely.

## Token efficiency

Read the global index before history. Read one selected handoff before older sessions. Keep indexes and JSONL compact. Do not print the full handoff after CREATE. Prefer repo verification over replaying chat.

## Usage examples

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

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/create_handoff.py <topic>` | CREATE: immutable handoff + JSONL + indexes |
| `scripts/resume_handoff.py` | RESUME: select current-agent or cross-agent handoff |
| `scripts/list_handoffs.py [path]` | List handoffs across agent dirs |
| `scripts/validate_handoff.py <file>` | Completeness, quality, secrets |
| `scripts/check_staleness.py <file>` | Whether repo state still matches |

## Resources

- `references/handoff-template.md` — required sections and metadata
- `references/resume-checklist.md` — reconcile before continuing
