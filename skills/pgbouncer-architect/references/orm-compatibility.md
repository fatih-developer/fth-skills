# PgBouncer — ORM Compatibility

> Loaded on demand by `pgbouncer-architect` in PHASE 4.

Each ORM has specific requirements. Apply automatically based on Phase 1 detection.

### Drizzle ORM
```typescript
// In transaction mode: disable prepared statement caching
// drizzle config:
const db = drizzle(pool, {
  // Drizzle uses node-postgres (pg) under the hood
  // pg handles prepared statements per connection
  // In transaction mode, connections change per transaction
  // → Use query strings, not prepared statement names
});

// Connection string: point to PgBouncer port
const pool = new Pool({
  connectionString: process.env.DATABASE_URL, // pgbouncer:6432
  // Do NOT set statement_timeout here — set in pgbouncer.ini
});
```
⚠️ **Warning:** Drizzle's `db.transaction()` works fine in transaction mode.
Advisory locks inside transactions do NOT work — use session mode if needed.

---

### Prisma
```
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")  // pgbouncer:6432
  // Add pgbouncer=true to connection string:
  // postgresql://user:pass@pgbouncer:6432/db?pgbouncer=true
}
```
```
// .env
DATABASE_URL="postgresql://user:pass@pgbouncer:6432/db?pgbouncer=true&connection_limit=1"
//                                                         ↑ disables Prisma's own pool
//                                                                          ↑ 1 conn per instance
```
⚠️ **Warning:** `pgbouncer=true` disables Prisma's prepared statements. This is required.

---

### TypeORM
```typescript
const dataSource = new DataSource({
  type: "postgres",
  host: "pgbouncer",       // ← PgBouncer host
  port: 6432,              // ← PgBouncer port
  poolSize: 1,             // ← Let PgBouncer handle pooling
  extra: {
    statement_timeout: 30000,
    // Disable TypeORM's prepared statements in transaction mode:
    prepare: false,
  }
});
```

---

### SQLAlchemy + asyncpg (Python)
```python
engine = create_async_engine(
    DATABASE_URL,  # postgresql+asyncpg://user:pass@pgbouncer:6432/db
    pool_size=1,          # Let PgBouncer pool
    max_overflow=0,
    connect_args={
        "statement_cache_size": 0,    # ← REQUIRED for transaction mode
        "prepared_statement_cache_size": 0,
    }
)
```

---

### node-postgres (pg)
```javascript
const pool = new Pool({
  connectionString: process.env.DATABASE_URL, // pgbouncer:6432
  max: 1,  // Let PgBouncer pool
  // No special config needed for transaction mode
  // But: cannot use pool.connect() + persistent prepared statements
});
```
