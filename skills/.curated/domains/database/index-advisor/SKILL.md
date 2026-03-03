---
name: index-advisor
description: Mevcut sorguları (queries) ve şemayı analiz eder. Eksik indexleri tespit eder, composite (bileşik) index sıralamasını optimize eder ve gereksiz/çakışan indexleri bulup kaldırır. Query execution plan (EXPLAIN) okuyarak somut CREATE/DROP INDEX önerileri üretir.
---

# Index Advisor Protocol

This skill focuses on making database reads remarkably fast while minimizing write amplification and storage bloat. It recommends standard, composite, partial, and covering indexes based on actual or predicted query workload.

**Core principle:** Indexes are not free. Every index accelerates reads but slows down writes, inserts, and consumes disk space.

---

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

**Required Outputs (Must write BOTH to `docs/database-report/`):**

1. **Human-Readable Markdown (`docs/database-report/index-advisor-report.md`)**
```markdown
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
```

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

## Guardrails
- **Don't Over-Index:** Warn the user if a single table acquires more than 5-7 indexes or if indexes combined overlap the table size.
- **Zero-Downtime:** ALWAYS recommend `CREATE INDEX CONCURRENTLY` in PostgreSQL to avoid locking the table taking down production operations.
- **High Cardinality Check:** Only index where selectivity is high; indexing a boolean col `(is_active)` without a partial clause is an anti-pattern.
