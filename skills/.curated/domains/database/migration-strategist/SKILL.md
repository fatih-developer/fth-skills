---
name: migration-strategist
description: Sıfırdan migration değil — büyük şema değişikliklerini zero-downtime ile yönetir. Expand-contract pattern, backward-compatible geçiş, feature flag ile kademeli rollout, ve rollback planı oluşturur. Production durmadan tablo/kolon yapılandırma stratejileri sunar.
---

# Migration Strategist Protocol

This skill focuses on taking a database from State A to State B without causing downtime, locks, or data loss in production. Direct `ALTER TABLE` operations on large tables are dangerous and often require a multi-step rollout.

**Core assumption:** You cannot lock the table. You cannot break the old version of the application while the new version is deploying.

---

## 1. The Zero-Downtime Pipeline
When asked "How do I rename this column?" or "How do I split this table?", standard `ALTER TABLE RENAME` breaks the app. 
Always enforce a backward-compatible migration strategy:

### The Expand & Contract Pattern (4 Steps)
For breaking changes (e.g., renaming a column `name` to `full_name`):

1. **Add (Expand):** Add the new column `full_name` (nullable initially).
2. **Dual Write:** Deploy application code that writes to BOTH `name` and `full_name`, but reads from `name`.
3. **Backfill:** Write a script or background job to populate `full_name` using `name` for old rows.
4. **Switch & Drop (Contract):** Change the app to read/write ONLY `full_name`. After successful deployment, run a final migration to drop `name`.

## 2. Output Format (The Plan)

Provide a numbered timeline mapping Application Code states vs Database changes.

**Required Outputs (Must write BOTH to `docs/database-report/`):**

1. **Human-Readable Markdown (`docs/database-report/migration-strategist-report.md`)**
```markdown
### 🕰️ Step 1: Database Expand (Migration 1)
- Add `full_name` column.
- SQL: `ALTER TABLE users ADD COLUMN full_name VARCHAR(255);`

### 💻 Step 2: Application Release (v1.1)
- Code updates to write to BOTH `name` and `full_name`.
- Read from `name`.

### 🔄 Step 3: Data Backfill Script
- SQL: `UPDATE users SET full_name = name WHERE full_name IS NULL;`
- Action: Run this out-of-band in batches of 10,000 to avoid long locks.

### 💻 Step 4: Application Release (v1.2)
- Code updates to read/write ONLY to `full_name`.

### ✂️ Step 5: Database Contract (Migration 2)
- SQL: `ALTER TABLE users DROP COLUMN name;`
- Action: Execute only when v1.1 is fully retired from traffic.
```

2. **Machine-Readable JSON (`docs/database-report/migration-strategist-output.json`)**
```json
{
  "skill": "migration-strategist",
  "steps": [
    {"phase": "expand", "target_table": "users", "action": "add_column", "details": "full_name"},
    {"phase": "app_release_1", "action": "dual_write"},
    {"phase": "backfill", "query": "UPDATE users SET full_name = name"},
    {"phase": "app_release_2", "action": "read_write_new_only"},
    {"phase": "contract", "target_table": "users", "action": "drop_column", "details": "name"}
  ]
}
```

## 3. Rollback Strategy
Every Migration plan must include a clear rollback path if Step 2 or Step 4 fails. How do we reverse it?
- "If v1.2 fails, rollback to v1.1. Data is still dual-written to `name`, so reverting the code is safe."

---

## Guardrails
- **No `DEFAULT` on new columns for large tables:** In some older SQL versions, adding a column with a default value locks and rewrites the entire table. Use nullable + background backfill.
- **Data Type Casting:** Be explicitly careful about data truncation passing from State A to State B.
- **Constraints Last:** Add `NOT NULL`, `UNIQUE`, or Foreign Keys only at the very end of the backfill process.
