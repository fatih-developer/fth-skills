# Pooling Modes — Deep Dive

## Session Mode

**How it works:**
A client gets one PostgreSQL server connection for the entire duration of its
session. The connection is returned to the pool only when the client disconnects.

**Use when:**
- Your app uses prepared statements that persist across transactions
- Your app uses LISTEN / NOTIFY
- Your app uses advisory locks held across transactions
- Your app uses SET / RESET for session-level configuration
- Your app uses temporary tables
- You're migrating an existing app and can't refactor immediately

**Performance profile:**
```
Connections saved: minimal
Client:Server ratio ≈ 1:1 (no real pooling benefit)
Best for: apps that need full PostgreSQL feature set
Worst for: high-concurrency, many idle connections
```

**When session mode still helps:**
Even in 1:1 mode, PgBouncer provides value:
- Single point of connection management
- Automatic reconnection on PostgreSQL restart
- Connection queueing (clients wait instead of getting "too many connections")
- Easier SSL termination management

---

## Transaction Mode

**How it works:**
A client gets a PostgreSQL connection only for the duration of a transaction.
Once `COMMIT` or `ROLLBACK` is issued, the connection returns to the pool
immediately — even if the client stays connected to PgBouncer.

**Use when:**
- Web applications with short-lived transactions
- REST APIs, GraphQL servers
- Any stateless request/response pattern
- Drizzle, Prisma, TypeORM (with config changes)

**Performance profile:**
```
Connections saved: significant
Client:Server ratio ≈ 5:1 to 100:1 depending on transaction duration
Best for: high-concurrency web apps
Worst for: apps with session-level state
```

**What BREAKS in transaction mode:**

| Feature | Why it breaks |
|---------|--------------|
| Persistent prepared statements | Connection changes after each transaction |
| LISTEN / NOTIFY | Session ends, subscription lost |
| Advisory locks (session-level) | Released when connection returns to pool |
| `SET` session variables | Lost when connection returns |
| Temporary tables | Dropped when connection returns |
| `WITH HOLD` cursors | Cursor is on the connection, not the session |
| `SAVEPOINT` outside transaction | No transaction to save to |

**Workarounds:**

```sql
-- Prepared statements: use query strings instead
-- BEFORE (breaks in transaction mode):
PREPARE my_stmt AS SELECT * FROM users WHERE id = $1;
EXECUTE my_stmt(1);

-- AFTER (works in transaction mode):
SELECT * FROM users WHERE id = $1;  -- just send the query directly
```

```sql
-- Advisory locks: use transaction-level instead of session-level
-- BEFORE (breaks):
SELECT pg_advisory_lock(1234);
-- ... do work across multiple transactions ...
SELECT pg_advisory_unlock(1234);

-- AFTER (works):
BEGIN;
SELECT pg_advisory_xact_lock(1234);  -- released automatically at COMMIT
-- ... do work within single transaction ...
COMMIT;
```

---

## Statement Mode

**How it works:**
A client gets a PostgreSQL connection for a single SQL statement only.
Connection is returned immediately after each statement completes.

**Use when:**
- Extremely high concurrency, very short queries
- Simple SELECT/INSERT/UPDATE with no transactions
- You know exactly what you're doing

**Performance profile:**
```
Connections saved: maximum
Client:Server ratio: potentially 1000:1
Dangerous: most applications will break
```

**What BREAKS in statement mode:**

Everything that breaks in transaction mode, PLUS:
- Multi-statement transactions (`BEGIN` ... `COMMIT`)
- Any transaction at all (each statement is its own implicit transaction)
- `RETURNING` clause (technically works but beware)
- Sequential operations that depend on each other

**Recommendation:** Avoid unless you have a very specific, well-understood use case.
The pgBouncer documentation itself calls this mode "not recommended for general use."

---

## Mode Comparison Table

| Aspect | Session | Transaction | Statement |
|--------|---------|-------------|-----------|
| Connection efficiency | ❌ Low | ✅ High | ✅ Highest |
| PostgreSQL feature support | ✅ Full | ⚠️ Partial | ❌ Minimal |
| Prepared statements | ✅ | ❌ | ❌ |
| LISTEN/NOTIFY | ✅ | ❌ | ❌ |
| Advisory locks (session) | ✅ | ❌ | ❌ |
| Multi-statement transactions | ✅ | ✅ | ❌ |
| SET session config | ✅ | ❌ | ❌ |
| Temp tables | ✅ | ❌ | ❌ |
| ORM compatibility | ✅ All | ⚠️ With config | ❌ Rare |
| Recommended for web apps | ⚠️ Only if needed | ✅ Default choice | ❌ Avoid |

---

## Switching Modes in Production

**Session → Transaction (safe migration path):**

```
Step 1: Audit your codebase for session-level features
        grep -r "pg_advisory_lock\|LISTEN\|NOTIFY\|CREATE TEMP\|SET " src/

Step 2: Refactor found usages
        - Prepared statements → inline queries
        - Session advisory locks → transaction advisory locks
        - LISTEN/NOTIFY → separate persistent connection (not through PgBouncer)

Step 3: Test with transaction mode in staging
        Set pool_mode = transaction in pgbouncer.ini
        Run full test suite

Step 4: Deploy with monitoring
        Watch for: unexpected errors, broken features
        Have rollback plan (revert to session mode)
```

**LISTEN/NOTIFY pattern (when you need it alongside transaction mode):**
```
Separate the LISTEN/NOTIFY connection from the regular pool:
- Regular queries → PgBouncer (transaction mode)
- LISTEN/NOTIFY → Direct PostgreSQL connection (bypass PgBouncer)

In Node.js:
const poolClient = new Pool({ host: 'pgbouncer', port: 6432 });  // transaction mode
const listenClient = new Client({ host: 'postgres', port: 5432 }); // direct
await listenClient.connect();
await listenClient.query('LISTEN my_channel');
```
