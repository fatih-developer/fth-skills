---
name: query-budget-enforcer
description: Sorguların kaynak limitlerini belirler ve denetler. Hangi sorgular çok fazla satır tarıyor, memory şişiriyor veya kilit tutuyor tespit eder. Maliyet tahmini yapar (Snowflake kredisi, BigQuery byte'ı vb.) ve limiti aşanlar için uyarı/alternatif üretir.
---

# Query Budget Enforcer Protocol

This skill acts as the financial and operational conscience of the database. It reviews queries not just for speed, but for computational cost, lock duration, and hardware limits.

**Core assumption:** In cloud data warehouses (Snowflake, BigQuery), bad queries cost actual money. In OLTP (PostgreSQL), bad queries crash the server.

---

## 1. Budget Categories (Static vs Dynamic)
- **Default (Static):** Analyze queries textually based on known engine constraints (e.g. flagging `SELECT *` without `WHERE` for BigQuery or lack of `LIMIT`).
- **Dynamic (On-Demand):** Connect to the database or metrics API (e.g. pg_stat_statements) to read historical query execution costs or dry-run estimates only if requested.
- When evaluating a query, enforce limits based on the context:

### A. Data Warehouse Constraints (BigQuery / Snowflake)
- **Terabytes Scanned:** Did they use a `SELECT *` without partition filters (`WHERE date = ...`)? 
- **Cost Estimation:** "This query scans 4TB. At $5/TB, this single run costs $20."

### B. OLTP Constraints (PostgreSQL / MySQL)
- **Rows Examined vs Returned:** If a query examines 100,000 rows (`Rows Removed by Filter: 99990`) to return 10 rows, it violates the efficiency budget.
- **Locking Time:** Does the query hold an `Access Exclusive Lock` or lengthy `SELECT ... FOR UPDATE` that blocks concurrent transactions?
- **Memory Spillage:** Does the sort operation exceed `work_mem` and spill to temporary disk?

## 2. Enforcing Limits (The Output)

Review the query and provide a Pass/Fail budget assessment.

**Required Outputs (Must write BOTH to `docs/database-report/`):**

1. **Human-Readable Markdown (`docs/database-report/query-budget-report.md`)**
```markdown
### 💳 Query Budget Assessment: FAILED ❌

**Query Analyzed:**
`SELECT * FROM events WHERE event_type = 'click';`

**Violations Detected:**
1. **[BigQuery] Partition Ignored:** The table is partitioned by `event_date`, but no date filter was provided. This will scan the entire 50TB table.
2. **[OLTP] Over-fetching:** `SELECT *` pulls down 140 columns when the application likely only needs 3.

### 💡 Remediation (How to get under budget)
Rewrite the query to respect system limits:

```sql
-- ✅ Budget-friendly rewrite
-- Added mandatory partition filter limit and explicit columns
SELECT user_id, event_payload, created_at 
FROM events 
WHERE event_type = 'click' 
  AND event_date >= CURRENT_DATE - INTERVAL '7 days';
```
```

2. **Machine-Readable JSON (`docs/database-report/query-budget-output.json`)**
```json
{
  "skill": "query-budget-enforcer",
  "assessment": "FAILED",
  "violations": [
    {"type": "Partition Ignored", "engine": "BigQuery", "severity": "High"},
    {"type": "Over-fetching", "engine": "OLTP", "severity": "Medium"}
  ],
  "suggested_sql": "SELECT user_id, event_payload..."
}
```

---

## Guardrails
- **Engine Awareness:** BigQuery hates `SELECT *` but loves denormalization. PostgreSQL hates denormalization but `SELECT *` is less deadly if properly indexed. Adjust budgets based on the target engine.
- **Hard Limits:** Recommend configuring server-side limits like `statement_timeout` (PostgreSQL) or Maximum Bytes Billed (BigQuery) to definitively enforce budgets at the infrastructure layer.
