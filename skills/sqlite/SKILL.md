---
name: sqlite-omni
description: >
  Expert SQLite guidance for modern full-stack and AI projects. Use this skill whenever the user
  mentions sqlite, sqlite3, bun:sqlite, better-sqlite3, aiosqlite, libsql, Turso, Cloudflare D1,
  WAL mode, FTS5, sqlite-vec, or asks about local/embedded databases. Also triggers for schema
  design, SQLite migrations with Drizzle or raw SQL, performance tuning, backup/restore, and
  building stateful CLI + SQLite System Skills. Works across TypeScript (Bun, Node), Python
  (FastAPI, asyncio), and CLI contexts. Always use this skill when SQLite is involved — even
  indirectly — because correct PRAGMA, WAL, and driver-specific patterns matter a lot.
compatibility: "Bun 1.x+, Node 18+, Python 3.8+, Drizzle ORM, sqlite-vec, libsql/Turso"
---

# SQLite Expert Skill

SQLite is a self-contained, serverless, zero-configuration SQL database engine. It's the right
choice for local tools, CLI apps, AI agents, edge deployments (Cloudflare D1, Turso), and
embedded databases in SaaS products.

## Quick Decision Tree

```
What do you need?
├── TypeScript + Bun project?          → references/TYPESCRIPT_DRIZZLE.md
├── Python / FastAPI project?          → references/PYTHON.md
├── Performance, WAL, PRAGMA tuning?  → references/PERFORMANCE.md
├── Full-text search (FTS5)?          → references/FTS5_VECTOR.md  §FTS5
├── AI vector embeddings?             → references/FTS5_VECTOR.md  §sqlite-vec
├── Cloud SQLite (Turso / D1)?        → references/CLOUD.md
├── Building a stateful CLI Skill?    → references/CLI_SKILL_PATTERN.md
├── Schema design & normalization?    → This file §Schema Design
└── Backup, vacuum, integrity?        → This file §Maintenance
```

Read the referenced file ONLY when relevant. Don't load all references at once.

---

## Core Concepts

### Driver Selection

| Runtime | Recommended Driver | Notes |
|---|---|---|
| Bun | `bun:sqlite` (built-in) | Zero-dep, fastest |
| Bun + ORM | `drizzle-orm/bun-sqlite` | Type-safe, migrations |
| Node.js | `better-sqlite3` | Sync, very fast |
| Node.js async | `@libsql/client` | For Turso/libsql |
| Python sync | `sqlite3` (stdlib) | Zero-dep |
| Python async | `aiosqlite` | asyncio-native |
| Edge / CF | Cloudflare D1 binding | Workers only |

### Always-On PRAGMAs

Run these immediately after opening any connection:

```sql
PRAGMA journal_mode = WAL;       -- Concurrent readers + writer
PRAGMA synchronous = NORMAL;     -- Safe + fast (vs FULL)
PRAGMA foreign_keys = ON;        -- Enforce FK constraints
PRAGMA cache_size = -64000;      -- 64 MB page cache
PRAGMA temp_store = MEMORY;      -- Temp tables in RAM
PRAGMA mmap_size = 268435456;    -- 256 MB memory-mapped I/O
```

> ⚠️ `WAL` is a file-level setting — it persists across connections. Set once, check after.

---

## Schema Design

### Naming Conventions

```sql
-- Tables: snake_case, plural
CREATE TABLE user_sessions (...);

-- Columns: snake_case
created_at, updated_at, deleted_at

-- PKs: always integer with AUTOINCREMENT or WITHOUT ROWID
id INTEGER PRIMARY KEY AUTOINCREMENT

-- FKs: <table_singular>_id
user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
```

### Type Affinity Rules

SQLite has flexible typing — use these mappings:

| Concept | SQLite Type | Notes |
|---|---|---|
| Auto-increment PK | `INTEGER PRIMARY KEY` | Also the rowid alias |
| String | `TEXT` | UTF-8 by default |
| Boolean | `INTEGER` (0/1) | No native bool |
| Float | `REAL` | 8-byte IEEE 754 |
| Timestamps | `INTEGER` (unix) or `TEXT` (ISO8601) | Pick one, be consistent |
| JSON | `TEXT` | Use `json_extract()` / `->` operator |
| Binary | `BLOB` | Images, embeddings |
| UUID | `TEXT` (36 chars) or `BLOB` (16 bytes) | BLOB is 60% smaller |

### Timestamp Pattern (Recommended)

```sql
created_at INTEGER NOT NULL DEFAULT (unixepoch()),
updated_at INTEGER NOT NULL DEFAULT (unixepoch())
```

Use triggers for `updated_at`:

```sql
CREATE TRIGGER set_updated_at
AFTER UPDATE ON my_table
BEGIN
  UPDATE my_table SET updated_at = unixepoch() WHERE id = NEW.id;
END;
```

### JSON Columns

SQLite 3.38+ supports the `->` and `->>` operators:

```sql
-- Store
INSERT INTO events (payload) VALUES ('{"type":"click","x":100}');

-- Extract (returns JSON)
SELECT payload -> '$.type' FROM events;

-- Extract as text (no quotes)
SELECT payload ->> '$.type' FROM events;

-- Index a JSON field
CREATE INDEX idx_events_type ON events(payload ->> '$.type');
```

### Soft Delete Pattern

```sql
deleted_at INTEGER DEFAULT NULL  -- NULL = alive, unix timestamp = deleted

-- Query living rows
SELECT * FROM users WHERE deleted_at IS NULL;

-- Partial index for performance
CREATE INDEX idx_users_active ON users(email) WHERE deleted_at IS NULL;
```

---

## Indexing Strategy

```sql
-- Single column
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Composite — order matters: equality first, range last
CREATE INDEX idx_sessions_user_created ON sessions(user_id, created_at);

-- Partial index — only index relevant rows
CREATE INDEX idx_jobs_pending ON jobs(created_at) WHERE status = 'pending';

-- Covering index — avoids table lookup entirely
CREATE INDEX idx_users_email_name ON users(email, name);

-- Inspect query plan
EXPLAIN QUERY PLAN SELECT * FROM posts WHERE user_id = 1 ORDER BY created_at DESC;
```

**Index anti-patterns:**
- Don't index every column — writes get slower
- Avoid indexing low-cardinality columns (boolean, enum with few values)
- Composite index column order matters: `(a, b)` helps `WHERE a=? AND b=?` and `WHERE a=?`, but NOT `WHERE b=?`

---

## Transactions

```sql
-- Explicit transaction (fastest for bulk inserts)
BEGIN;
INSERT INTO logs VALUES (...);
INSERT INTO logs VALUES (...);
COMMIT;

-- Savepoints (nested transactions)
SAVEPOINT sp1;
-- ... operations ...
ROLLBACK TO sp1;  -- or RELEASE sp1 to commit

-- Immediate write lock (prevents SQLITE_BUSY in WAL mode)
BEGIN IMMEDIATE;
```

**Bulk insert pattern (10-100x faster than individual inserts):**

```typescript
// Bun / better-sqlite3
const insert = db.prepare('INSERT INTO items (name, value) VALUES (?, ?)');
const insertMany = db.transaction((items) => {
  for (const item of items) insert.run(item.name, item.value);
});
insertMany(myArray);  // Single transaction
```

---

## Maintenance

### Vacuum & Analyze

```sql
-- Reclaim space after large deletes (creates new file, takes time)
VACUUM;

-- Incremental vacuum (WAL mode, run periodically)
PRAGMA incremental_vacuum(100);  -- Free 100 pages

-- Update query planner statistics
ANALYZE;

-- Integrity check
PRAGMA integrity_check;

-- Quick check (faster, less thorough)
PRAGMA quick_check;
```

### Backup

```bash
# CLI backup (safe while DB is in use)
sqlite3 app.db ".backup backup_$(date +%Y%m%d).db"

# Hot backup via SQLite Online Backup API
sqlite3 app.db "VACUUM INTO 'backup.db';"
```

```python
# Python: safe online backup
import sqlite3
src = sqlite3.connect('app.db')
dst = sqlite3.connect('backup.db')
src.backup(dst, pages=100)  # 100 pages at a time = non-blocking
dst.close(); src.close()
```

### File Size Check

```sql
SELECT
  page_count * page_size AS total_bytes,
  freelist_count * page_size AS free_bytes,
  ROUND(freelist_count * 100.0 / page_count, 1) AS fragmentation_pct
FROM pragma_page_count(), pragma_page_size(), pragma_freelist_count();
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| `SQLITE_BUSY` errors | Enable WAL mode; use `BEGIN IMMEDIATE` for writes |
| Slow bulk inserts | Wrap in explicit `BEGIN/COMMIT` transaction |
| No FK enforcement | Run `PRAGMA foreign_keys = ON` on every connection |
| Boolean confusion | Store as `INTEGER` 0/1; never `'true'`/`'false'` |
| Timestamp inconsistency | Pick unix (INTEGER) or ISO8601 (TEXT), never mix |
| File locking on network drives | Never use SQLite on NFS/SMB — copy locally first |
| WAL file growing | Run `PRAGMA wal_checkpoint(TRUNCATE)` periodically |

---

## Reference Files

| File | When to Read |
|---|---|
| `references/TYPESCRIPT_DRIZZLE.md` | TypeScript + Bun + Drizzle ORM setup, migrations, relations |
| `references/PYTHON.md` | Python sqlite3, aiosqlite, FastAPI integration |
| `references/PERFORMANCE.md` | Deep PRAGMA tuning, profiling, EXPLAIN QUERY PLAN |
| `references/FTS5_VECTOR.md` | FTS5 full-text search + sqlite-vec AI embeddings |
| `references/CLOUD.md` | Turso (libsql), Cloudflare D1, multi-region |
| `references/CLI_SKILL_PATTERN.md` | CLI + SQLite stateful Skill pattern |
