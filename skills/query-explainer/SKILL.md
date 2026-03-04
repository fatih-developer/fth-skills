---
name: query-explainer
description: Translates execution plans (EXPLAIN ANALYZE) into human-readable language. Explains why Seq Scan is bad and when Hash Join is optimal.
---

# Query Explainer Protocol

This skill bridges the gap between raw database optimizer output and human-readable performance tuning. It reads `EXPLAIN (ANALYZE, BUFFERS)` and translates the nodes and costs into concrete actions.

**Core assumption:** A developer should not need to be a DBA to understand why their query takes 3 seconds and what to do about it.

---

## 1. Plan Ingestion & Translation (Static vs Dynamic)
- **Default (Static):** Analyze based on user-provided EXPLAIN text/JSON outputs. 
- **Dynamic (On-Demand):** Only connect to a live database to execute `EXPLAIN (ANALYZE, BUFFERS)` directly if the user explicitly authorizes it and provides the target query.
- When evaluating the plan structurally:
  - **Cost vs Actual:** Differentiate between planner estimates (`cost=0.00..10.00`) and reality (`actual time=0.015..0.020`).
  - **Data Volume:** Note discrepancies between `rows=1000000` (estimated) and `loops=1` actual rows fetched (this indicates bad statistics).

## 2. Identify Bottleneck Nodes
Highlight the most expensive parts of the query:
- 🐌 **Sequential Scans (Seq Scan):** Acceptable on tiny tables. Disastrous on millions of rows.
- 🐌 **Nested Loops over many rows:** Indicates missing indexes on the joined columns.
- 🐌 **Filesort / External Merge Disk:** The database ran out of `work_mem` and had to sort on disk. This is a critical performance killer.
- 🐌 **High Disk I/O:** Look for high `shared read` blocks compared to `shared hit` (buffers).

## 3. Human-Readable Output Generation

Provide an intuitive breakdown of the issue.

**Required Outputs (Must write BOTH to `docs/database-report/`):**

1. **Human-Readable Markdown (`docs/database-report/query-explainer-report.md`)**
```markdown
### 📊 Plan Summary
- **Total Execution Time:** 2350.45 ms
- **Biggest Bottleneck:** `Seq Scan` on the `orders` table (took 2100 ms, 89% of the time).

### 🔍 What the Database Actually Did
1. It scanned **every single row** (1.5 million rows) in the `orders` table to find records where `status = 'pending'`.
2. It then joined these results with the `users` table. Because there was no index to help sort them, it had to sort them in memory (`Sort Method: external merge disk`).

### 💡 How to Fix It
**Action 1: Add a Missing Index**
The planner is begging for an index on `status`. Wait, run `index-advisor` to be sure, but here is a quick fix:
`CREATE INDEX CONCURRENTLY idx_orders_status ON orders(status) WHERE status = 'pending';`

**Action 2: Increase work_mem (Optional)**
If this is a data-warehouse query, the sort spilled to disk because it needed 45MB of memory but only had 4MB. Temporarily increasing `work_mem` for the session might help.
```

2. **Machine-Readable JSON (`docs/database-report/query-explainer-output.json`)**
```json
{
  "skill": "query-explainer",
  "execution_time_ms": 2350.45,
  "bottlenecks": [
    {"type": "Seq Scan", "table": "orders", "cost_pct": 89, "reason": "Missing index on status"}
  ],
  "recommendations": [
    {"type": "ADD_INDEX", "sql": "CREATE INDEX ..."}
  ]
}
```

---

## Guardrails
- **Beware of Stats:** Always check if row estimations wildly differ from actual rows. If so, recommend `ANALYZE table_name;` before blindly creating an index.
- **Context matters:** A Seq Scan is *supposed* to happen if the query requests 80% of the table. Don't recommend indexes for massive bulk exports.
- **Integration:** Forward complex index configurations to the `index-advisor` skill.
