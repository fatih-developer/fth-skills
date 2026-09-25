---
name: index-advisor
description: "Recommend database indexes from real queries and schema: missing, composite, covering, partial, and unused indexes, with column order rationale and write-cost trade-offs. Use when the user has slow queries, sequential scans, high database CPU, or asks which indexes to add or drop."
---

# Index Advisor Protocol

This skill focuses on making database reads remarkably fast while minimizing write amplification and storage bloat. It recommends standard, composite, partial, and covering indexes based on actual or predicted query workload.

**Core principle:** Indexes are not free. Every index accelerates reads but slows down writes, inserts, and consumes disk space.

---

## 0. Context Intake

Before designing, make sure you have the inputs below. Read the previous workflow step's artifact first if it exists. Ask only for what is missing, in a single message, and state any assumption you make instead of blocking.

- The slow queries (text plus frequency) and ideally their `EXPLAIN ANALYZE` output or `query-explainer-output.json`.
- Table sizes and write volume for the affected tables.
- Existing indexes (schema dump or `\d table`).

## 1. Analysis Phase (Static vs. Dynamic)
- **Default (Static):** Analyze based on provided SQL queries, schema files, or output from `schema-architect`.
- **Dynamic (On-Demand):** Only connect to a live database to run `EXPLAIN` or read actual index usage statistics if the user explicitly requests it.

## 2. Optimization Methodology

### The B-Tree Ordering Rule for Composites
For Composite Indexes, always apply the rule of **Equality, Sort, Range**:
1. **Equality:** Fields used in `=` or `IN`.
2. **Sort:** Fields used in `ORDER BY`.
3. **Range:** Fields used in `>`, `<`, or `BETWEEN`.

*Example Query:* 
`SELECT * FROM orders WHERE tenant_id = 5 AND status = 'active' ORDER BY created_at DESC LIMIT 10`
*Recommended Optimal Index:* `(tenant_id, status, created_at DESC)`

### Index Type Selection
Select the correct index type according to the target database engine:
- **B-Tree:** Default for standard lookups, strings, and integers.
- **Partial/Filtered Indexes:** Highly recommended for sparse data or booleans (e.g., `WHERE status = 'pending'`).
- **GIN / GiST:** For full-text search, arrays, and geospatial data in PostgreSQL.
- **BRIN:** For large sequential time-series data chunks.

## 3. The "Drop" Recommendation
Optimization isn't just about adding new indexes. Identify candidates for removal:
- **Redundant Indexes:** An index on `(A)` is entirely redundant and should be dropped if you just created an index on `(A, B)`.
- **Unused Indexes:** Flag non-system indexes with low usage rates.

## 4. Expected Output Structure

**Outputs.** In *file mode* — the user wants artifacts, or this skill runs as a step of an ecosystem workflow — write both files below to `docs/database-report/`. In *inline mode* — a quick question — answer in the chat and end with the JSON below as a *Handoff* block instead of creating files.

1. **Human-Readable Markdown (`docs/database-report/index-advisor-report.md`)**
````markdown
### 🚀 Index Optimization Report
- **Query Addressed:** [Identify specific SQL query]
- **Applied Rule:** Equality, Sort, Range match.
- **Expected Impact:** Prevention of sequential scan of 1M rows.

#### 🌟 REQUIRED FIX
```sql
CREATE INDEX CONCURRENTLY idx_orders_tenant_status_date 
ON orders (tenant_id, status, created_at DESC);
```
#### 🗑️ CLEANUP
```sql
DROP INDEX CONCURRENTLY idx_orders_tenant;
```
````

2. **Machine-Readable JSON (`docs/database-report/index-advisor-output.json`)**
```json
{
  "skill": "index-advisor",
  "recommended_indexes": [
    {"table": "orders", "columns": ["tenant_id", "status", "created_at"], "type": "B-Tree", "action": "CREATE"}
  ],
  "redundant_indexes": [
    {"table": "orders", "index_name": "idx_orders_tenant", "action": "DROP"}
  ]
}
```

---

## When to Skip

- The table is tiny, the bottleneck is outside the database (network, N+1 in application), or no query is identified yet (run `@query-explainer` first).

## Guardrails
- **Don't Over-Index:** Warn the user if a single table acquires more than 5-7 indexes or if indexes combined overlap the table size.
- **Zero-Downtime:** ALWAYS recommend `CREATE INDEX CONCURRENTLY` in PostgreSQL to avoid locking the table taking down production operations.
- **High Cardinality Check:** Only index where selectivity is high; indexing a boolean col `(is_active)` without a partial clause is an anti-pattern.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-database` — Database Domain.

**Workflows:**
- **Performance Optimization Flow** (`db-performance`, step 2 of 3): next → `@query-budget-enforcer` *(optional)*.

**Direct handoffs:**
- `@migration-strategist` — Index creation needs a non-locking rollout on a large table.

**Handoff contract:** pass results to the next skill through `docs/database-report/index-advisor-output.json` with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-database`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
