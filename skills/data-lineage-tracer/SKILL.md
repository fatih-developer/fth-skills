---
name: data-lineage-tracer
description: Traces the data source (Data Lineage) of any column or table. Identifies views, triggers, stored procedures, and ETL pipelines involved.
---

# Data Lineage Tracer Protocol

This skill answers the critical question: *"If I change this column, who dies?"* It traces the flow of data backward (Upstream) to its source, and forward (Downstream) to its consumers.

**Core assumption:** Data does not exist in a vacuum. It flows through Views, Materialized Views, Stored Procedures, Triggers, and ORM boundaries.

---

## 0. Context Intake

Before designing, make sure you have the inputs below. Read the previous workflow step's artifact first if it exists. Ask only for what is missing, in a single message, and state any assumption you make instead of blocking.

- Target table or column to trace.
- Where the definitions live: migrations, views, dbt models, ETL code, or live catalog access.
- Whether live introspection is allowed or only static files.

## 1. Upstream & Downstream Mapping (Static vs Dynamic)

- **Default (Static):** Analyze based on provided `.sql`, schema files, and application ORM code (e.g. Prisma models).
- **Dynamic (On-Demand):** Only connect to the database to inspect dynamic dependencies (e.g. live `pg_views` or `information_schema.triggers`) if requested explicitly.
If assessing `reporting.daily_sales.total_amount`:
- Is it a physical physical or a computed column?
- Does a `VIEW` project it directly from `public.orders`?
- Is it populated via a daily `INSERT INTO ... SELECT` cron job?

### Downstream Tracing (Who uses it?)
If dropping `public.users.phone_number`:
- Is there a `VIEW` that will become invalid (breaking the DB)?
- Is there a Database Trigger relying on it?
- Is there an ORM/GraphQL endpoint or REST Serializer exposing it?

## 2. Dependency Risk Assessment
Categorize the objects affected by a hypothetical change:
- **Hard Dependencies (DB Level):** Views, Materialized Views, Foreign Keys, Stored Procedures. (Will hard-crash the database operations).
- **Soft Dependencies (App Level):** ORM models, API serializers, BI tool dashboards. (Will crash the app layer).

## 3. Visual Output Generation

Provide a clear trace map using Markdown or Mermaid.js so the developer can visualize the blast radius.

**Outputs.** In *file mode* — the user wants artifacts, or this skill runs as a step of an ecosystem workflow — write both files below to `docs/database-report/`. In *inline mode* — a quick question — answer in the chat and end with the JSON below as a *Handoff* block instead of creating files.

1. **Human-Readable Markdown (`docs/database-report/data-lineage-report.md`)**
```markdown
### 🗺️ Data Lineage for `orders.customer_id`

**Upstream (Writers):**
- ⬅️ Written by `process_payment()` Stored Procedure.
- ⬅️ Populated via API Endpoint `POST /api/v1/checkout`.

**Downstream (Readers/Dependents):**
- ➡️ `VIEW analytics.monthly_cohorts` (Hard dependency - will BREAK if column is dropped).
- ➡️ `TRIGGER sync_to_crm_on_update` (Hard dependency).
- ➡️ Metabase BI Dashboard (Soft dependency).

### ⚠️ Blast Radius Warning
If you rename or modify the type of `customer_id`:
1. The `monthly_cohorts` view must be re-created via `CREATE OR REPLACE VIEW`.
2. The trigger `sync_to_crm_on_update` must be updated to reference the new name.
```

2. **Machine-Readable JSON (`docs/database-report/data-lineage-output.json`)**
```json
{
  "skill": "data-lineage-tracer",
  "target": "orders.customer_id",
  "upstream": ["process_payment()", "POST /api/v1/checkout"],
  "downstream": [
    {"type": "hard", "entity": "VIEW analytics.monthly_cohorts"},
    {"type": "hard", "entity": "TRIGGER sync_to_crm_on_update"}
  ],
  "blast_radius_risk": "High"
}
```

*(Optional: Output a Mermaid graph if requested for complex ETL chains)*
```mermaid
graph TD;
    API-->public.orders;
    public.orders-->VIEW_monthly_sales;
    VIEW_monthly_sales-->BI_Dashboard;
```

---

## When to Skip

- The column is local to one table with no views, triggers, jobs, or downstream consumers.

## Guardrails
- **Incomplete Context:** Database artifacts (views, triggers) are reliable to trace inside static SQL files. Remind the user that external soft dependencies (like Metabase or random Python scripts) cannot be guaranteed by DB introspection alone.
- **Transitive Dependencies:** Ensure you trace at least 2 levels deep (e.g., Table A drives View B, View B drives View C).

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-database` — Database Domain.

**Workflows:**
- **Compliance & Lineage Flow** (`db-compliance`, step 1 of 2): last step → once it passes, complete the workflow and report the outcome.

**Handoff contract:** pass results to the next skill through `docs/database-report/data-lineage-output.json` with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-database`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
