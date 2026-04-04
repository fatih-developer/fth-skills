# SQLite Performance Reference

## Table of Contents
1. [PRAGMA Tuning Guide](#pragma-tuning-guide)
2. [EXPLAIN QUERY PLAN](#explain-query-plan)
3. [Profiling Slow Queries](#profiling-slow-queries)
4. [Write Performance](#write-performance)
5. [Read Performance](#read-performance)
6. [WAL Mode Deep Dive](#wal-mode-deep-dive)
7. [Benchmarking Script](#benchmarking-script)

---

## PRAGMA Tuning Guide

### The Optimal Set (General Purpose)

```sql
-- Run immediately after connection open
PRAGMA journal_mode = WAL;           -- Enable WAL (persistent setting)
PRAGMA wal_autocheckpoint = 1000;    -- Checkpoint every 1000 pages (default)
PRAGMA synchronous = NORMAL;         -- Durable + fast (vs FULL = slow, OFF = risky)
PRAGMA foreign_keys = ON;            -- Enforce FK constraints (off by default!)
PRAGMA cache_size = -64000;          -- 64 MB in-process page cache (negative = KB)
PRAGMA page_size = 4096;             -- Default, good for most; set BEFORE first data
PRAGMA temp_store = MEMORY;          -- Sort/group temp tables in RAM, not disk
PRAGMA mmap_size = 268435456;        -- 256 MB memory-mapped I/O (faster reads)
PRAGMA busy_timeout = 5000;          -- Wait 5s before returning SQLITE_BUSY
PRAGMA optimize;                     -- Auto-analyze (SQLite 3.18+, run periodically)
```

### High-Throughput Writes (sacrifice some durability)

```sql
PRAGMA synchronous = OFF;            -- OS crash may corrupt DB, power loss won't
PRAGMA journal_mode = MEMORY;        -- Journal in RAM only (no WAL file)
PRAGMA locking_mode = EXCLUSIVE;     -- Single writer, maximum speed
```

> ⚠️ Use `synchronous = OFF` only for batch imports where you can re-run on failure.

### Read-Heavy Workload

```sql
PRAGMA cache_size = -256000;         -- 256 MB page cache
PRAGMA mmap_size = 1073741824;       -- 1 GB memory-mapped reads
PRAGMA query_only = ON;              -- Prevent accidental writes on read replicas
```

### PRAGMA Reference Table

| PRAGMA | Default | Recommended | Notes |
|---|---|---|---|
| `journal_mode` | DELETE | WAL | Concurrent reads |
| `synchronous` | FULL | NORMAL | Balanced safety |
| `cache_size` | -2000 (2 MB) | -64000 (64 MB) | More = faster |
| `temp_store` | DEFAULT | MEMORY | Faster sorts |
| `mmap_size` | 0 | 268435456 | Faster reads |
| `foreign_keys` | OFF | ON | Data integrity |
| `busy_timeout` | 0 | 5000 | Avoid SQLITE_BUSY |

---

## EXPLAIN QUERY PLAN

```sql
-- Basic usage
EXPLAIN QUERY PLAN
SELECT * FROM posts WHERE user_id = 42 ORDER BY created_at DESC;

-- Output columns: id, parent, notused, detail
-- Look for:
--   "SCAN" = full table scan (bad)
--   "SEARCH USING INDEX" = good
--   "USE TEMP B-TREE FOR ORDER BY" = missing covering index

-- Example output showing a bad plan:
-- SCAN TABLE posts   ← Full scan, no index used!

-- After adding index:
-- SEARCH TABLE posts USING INDEX idx_posts_user_created (user_id=?)
```

### Reading EQPLAN Output

```sql
-- Find all indexes on a table
PRAGMA index_list('posts');

-- Inspect an index
PRAGMA index_info('idx_posts_user_created');

-- See all stats
PRAGMA stats;
```

---

## Profiling Slow Queries

### Python Profiling

```python
import sqlite3
import time

conn = sqlite3.connect("app.db")
conn.set_trace_callback(print)  # Log every SQL statement

# Time a query
start = time.perf_counter()
conn.execute("SELECT COUNT(*) FROM posts WHERE status = 'published'").fetchone()
elapsed = time.perf_counter() - start
print(f"Query took {elapsed*1000:.1f}ms")
```

### Bun/Node Profiling

```typescript
import { Database } from 'bun:sqlite';

const db = new Database('app.db');

// Enable query logging
const start = performance.now();
const rows = db.query('SELECT COUNT(*) as n FROM posts').get();
const ms = performance.now() - start;
console.log(`Query: ${ms.toFixed(1)}ms`, rows);

// For Drizzle: enable logger
const db2 = drizzle(sqlite, { logger: true });
```

---

## Write Performance

### Batch Insert Benchmark

```typescript
// SLOW: 10k individual inserts (~10 seconds)
for (const item of items) {
  db.run('INSERT INTO logs (msg) VALUES (?)', [item]);
}

// FAST: same 10k in a single transaction (~50ms)
const insert = db.prepare('INSERT INTO logs (msg) VALUES (?)');
const batch = db.transaction((items: string[]) => {
  for (const msg of items) insert.run(msg);
});
batch(items);
```

### Prepared Statements

```typescript
// Prepare once, run many times
const stmt = db.prepare<{ id: number; email: string }, [number]>(
  'SELECT id, email FROM users WHERE id = ?'
);

// In a hot loop
const users = ids.map(id => stmt.get(id));
```

### Write Batching in Python

```python
import sqlite3

conn = sqlite3.connect("app.db")
conn.execute("PRAGMA journal_mode = WAL")

data = [(f"user{i}@x.com", f"User {i}") for i in range(10_000)]

# executemany in a transaction = fast
with conn:
    conn.executemany("INSERT INTO users (email, name) VALUES (?, ?)", data)

conn.close()
```

---

## Read Performance

### Covering Indexes

A covering index contains all columns needed by the query — SQLite never touches the table:

```sql
-- Query: SELECT email, name FROM users WHERE status = 'active' ORDER BY created_at
-- Covering index: includes all accessed columns
CREATE INDEX idx_users_covering
ON users(status, created_at, email, name);

-- EQPLAN shows:
-- SEARCH TABLE users USING COVERING INDEX idx_users_covering (status=?)
```

### Partial Indexes

```sql
-- Only index rows matching a condition (smaller index = faster)
CREATE INDEX idx_jobs_pending ON jobs(created_at)
WHERE status = 'pending';

-- Must use same WHERE clause in queries
SELECT * FROM jobs WHERE status = 'pending' ORDER BY created_at LIMIT 100;
```

### WITHOUT ROWID Tables

For tables where you always look up by PK and never need rowid:

```sql
CREATE TABLE kv_store (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
) WITHOUT ROWID;  -- 30-50% smaller, faster PK lookups
```

Good for: key-value stores, junction tables, session stores.

---

## WAL Mode Deep Dive

### How WAL Works

- Writers append to the WAL file; readers still see the original database
- Multiple readers can run concurrently with 1 writer (no blocking)
- Checkpoint = WAL content copied back to main database
- WAL file grows until checkpoint; auto-checkpoint at 1000 pages (~4 MB)

### WAL File Management

```sql
-- Manual checkpoint (useful after large batch writes)
PRAGMA wal_checkpoint;           -- Passive (doesn't block)
PRAGMA wal_checkpoint(TRUNCATE); -- Truncate WAL file after checkpoint
PRAGMA wal_checkpoint(RESTART);  -- Force all readers to restart

-- Check WAL status
PRAGMA wal_checkpoint(PASSIVE);
-- Returns: (busy, log, checkpointed) pages
```

### When WAL Doesn't Help

- Database on a network filesystem (NFS/SMB) — don't use SQLite here
- Only one connection ever — DELETE mode is fine
- Very write-heavy with no reads — consider `locking_mode = EXCLUSIVE`

---

## Benchmarking Script

```python
#!/usr/bin/env python3
"""Quick SQLite benchmark — run to check your PRAGMA settings."""
import sqlite3
import time
import tempfile
import os

def benchmark(journal_mode="WAL", synchronous="NORMAL", n=50_000):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    conn = sqlite3.connect(db_path)
    conn.execute(f"PRAGMA journal_mode = {journal_mode}")
    conn.execute(f"PRAGMA synchronous = {synchronous}")
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")

    data = [(f"value_{i}",) for i in range(n)]

    start = time.perf_counter()
    with conn:
        conn.executemany("INSERT INTO t (v) VALUES (?)", data)
    elapsed = time.perf_counter() - start

    conn.close()
    os.unlink(db_path)

    print(f"journal={journal_mode} sync={synchronous}: "
          f"{n} inserts in {elapsed:.3f}s "
          f"({n/elapsed:.0f}/sec)")

if __name__ == "__main__":
    benchmark("DELETE", "FULL")    # Worst case
    benchmark("WAL",    "NORMAL")  # Recommended
    benchmark("WAL",    "OFF")     # Maximum speed, some risk
    benchmark("MEMORY", "OFF")     # Pure RAM (no persistence)
```

Example output:
```
journal=DELETE sync=FULL:   50000 inserts in 48.2s  (1037/sec)
journal=WAL    sync=NORMAL: 50000 inserts in 0.31s  (161290/sec)
journal=WAL    sync=OFF:    50000 inserts in 0.09s  (555556/sec)
journal=MEMORY sync=OFF:    50000 inserts in 0.07s  (714286/sec)
```
