---
name: ecosystem-database
description: "Route database work — schema design, access policies, query performance, migrations, compliance, connection pooling — through the right fth-skills database skills in order. Use when the user wants to design tables, fix a slow query, change or migrate a schema, mask or trace data, scale connections, or asks which database skills to use."
---

# 🗄️ Database Ecosystem

This skill is the entry point of its ecosystem. It chooses a workflow, checks which member skills are installed, runs them in order with explicit handoffs, and degrades gracefully when a member is missing. The workflow map lives in `references/workflows.json`; the handoff format lives in `references/handoff-contract.md`.

## Catalog

<!-- BEGIN GENERATED: ecosystem-catalog (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Domain:** Database Domain — Model, secure, optimize, migrate, and operate SQL databases (PostgreSQL, MySQL, SQLite) with data integrity first.

**Philosophy:** Data integrity and safe change beat feature speed. Every destructive or locking operation on a shared database needs a reviewed plan and an explicit confirmation.

| Skill | Role | Handoff artifact |
|---|---|---|
| `@schema-architect` | Derives normalized schemas and DDL from business requirements. | `docs/database-report/schema-architect-output.json` |
| `@access-policy-designer` | Designs RLS, column-level security, and RBAC/ABAC policies. | `docs/database-report/access-policy-output.json` |
| `@seed-data-generator` | Generates referentially intact seed and test data. | `docs/database-report/seed-data-output.json` |
| `@query-explainer` | Explains EXPLAIN/EXPLAIN ANALYZE plans in plain language. | `docs/database-report/query-explainer-output.json` |
| `@index-advisor` | Recommends missing, composite, covering, or removable indexes. | `docs/database-report/index-advisor-output.json` |
| `@query-budget-enforcer` | Sets query cost budgets and N+1 detection rules. | `docs/database-report/query-budget-output.json` |
| `@schema-diff-analyzer` | Detects schema drift between environments and plans safe syncs. | `docs/database-report/schema-diff-output.json` |
| `@migration-strategist` | Plans zero-downtime expand/contract migrations and backfills. | `docs/database-report/migration-strategist-output.json` |
| `@data-masker` | Detects PII and masks production data for non-production use. | `docs/database-report/data-masking-output.json` |
| `@data-lineage-tracer` | Traces upstream and downstream lineage of tables and columns. | `docs/database-report/data-lineage-output.json` |
| `@pgbouncer-architect` | Sizes and configures PgBouncer connection pooling for PostgreSQL. | inline handoff block |
| `@sqlite` | Expert guidance for SQLite, libSQL/Turso, D1, WAL, FTS5, and sqlite-vec. | inline handoff block |
<!-- END GENERATED: ecosystem-catalog -->

## Router Protocol

<!-- BEGIN GENERATED: ecosystem-router (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
Follow this protocol whenever this ecosystem is invoked.

1. **Match.** Compare the request with each workflow's *When* phrases. Pick one workflow, or route straight to a single member skill when the request is narrow. If two workflows fit equally, ask one question to choose. If the request belongs to another domain, use the ecosystem index in `@ecosystem-orchestration`.
2. **Preflight.** Find out which step skills are installed: check the skills your host lists, or run `python <skill-dir>/scripts/install_all.py --status --workflow <id>` (`<skill-dir>` is the folder containing this `SKILL.md`). Show a short plan: step, skill, installed or missing, condition, expected artifact.
3. **Missing skills never block.** Offer once: (a) install them — `install_all.py --workflow <id>` prints the commands and only runs them with `--execute` after the user agrees; or (b) continue in fallback mode — perform the step yourself using its *Does* and *Done when* columns and label that output `fallback`.
4. **Conditions.** Skip optional steps whose condition does not hold, and say which steps you skipped and why.
5. **Execute.** Run steps in order. Steps that share a parallel group are independent and may run concurrently (`@parallel-planner`). Pass artifacts as described in `references/handoff-contract.md`. Check each step's *Done when* before moving on.
6. **Gates.** Before any destructive, irreversible, or production-impacting action, stop at `@checkpoint-guardian`, or ask for explicit confirmation when it is not installed.
7. **Failures.** When a step misses its *Done when*, hand off to `@error-recovery`. Without it, retry once with a changed approach, then report the blocker with evidence instead of guessing.
8. **State.** Keep a run log (workflow id, step, status, artifact). Record it with `@memory-ledger` when installed, and write a `@session-transfer` handoff if the run will continue in another session.
9. **Finish.** Summarize artifacts, skipped steps, open risks, and the most relevant next workflow.

**Skip this protocol** when the user names one specific skill (invoke it directly) or asks a quick factual question that needs no workflow.
<!-- END GENERATED: ecosystem-router -->

## Workflows

<!-- BEGIN GENERATED: ecosystem-workflows (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
### 1. New Schema Design Flow (`db-new-schema`)

**When:** “design a database”; “create tables”; “model the data”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@sqlite` *(optional)* | Apply SQLite-specific type, PRAGMA, and migration rules. | SQLite constraints are reflected in the design. | Target engine is SQLite, libSQL, Turso, or D1 | — |
| 2 | `@schema-architect` | Normalize the model and produce dialect-specific DDL. | Every table has a primary key, constraints, and justified normalization level. | — | — |
| 3 | `@access-policy-designer` | Add RLS, column security, and role policies to the new tables. | Each table with tenant or user data has an explicit policy. | — | — |
| 4 | `@seed-data-generator` | Generate seed data in dependency order. | Seed script loads without foreign-key errors. | — | — |

### 2. Performance Optimization Flow (`db-performance`)

**When:** “fix a slow query”; “optimize the database”; “why is the database slow”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@query-explainer` | Read the execution plan and name the bottleneck node. | Bottleneck identified with row estimates vs actuals. | — | — |
| 2 | `@index-advisor` | Recommend indexes that remove the bottleneck; flag unused indexes. | Each recommendation cites the query it fixes and its write cost. | — | — |
| 3 | `@query-budget-enforcer` *(optional)* | Set budgets and N+1 detection so the regression cannot return. | Budgets and alert thresholds are defined. | — | — |

### 3. Database Evolution Flow (`db-evolution`)

**When:** “change a table”; “migrate the schema”; “sync environments”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@schema-diff-analyzer` | Diff source and target schemas and rate each change's risk. | Every change is rated safe, warning, or dangerous. | — | — |
| 2 | `@migration-strategist` | Plan expand/contract migrations, backfills, and rollback. | Plan has up, down, backfill, and verification steps. | — | — |
| 3 | `@checkpoint-guardian` | Confirm before any migration runs against a shared or production database. | User explicitly approved the HIGH RISK step. | — | — |

### 4. Compliance & Lineage Flow (`db-compliance`)

**When:** “GDPR or KVKK review”; “mask production data”; “where does this data go”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@data-lineage-tracer` | Map where sensitive columns come from and flow to. | Upstream and downstream dependencies are listed. | — | `compliance` |
| 2 | `@data-masker` | Detect PII and choose masking strategies per column. | Every PII column has a masking rule. | — | `compliance` |

### 5. Connection Scaling Flow (`db-scaling`)

**When:** “too many connections”; “set up PgBouncer”; “size the connection pool”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@pgbouncer-architect` | Analyze workload, pick pool mode, size pools, and generate config. | Pool sizes are derived from server capacity and ORM constraints. | — | — |
| 2 | `@query-budget-enforcer` *(optional)* | Cap long-running queries that would starve the pool. | Statement timeouts and budgets are set. | — | — |

### Direct handoffs

- `@index-advisor` → `@migration-strategist`: Index creation needs a non-locking rollout on a large table.
- `@data-masker` → `@seed-data-generator`: Masked data should be replaced by synthetic fixtures.
- `@migration-strategist` → `@breaking-change-detector`: The schema change alters a public API contract.
<!-- END GENERATED: ecosystem-workflows -->
