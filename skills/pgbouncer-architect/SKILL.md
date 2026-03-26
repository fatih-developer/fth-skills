---
name: pgbouncer-architect
description: 'Designs and configures PgBouncer connection pooling for PostgreSQL based on actual workload analysis. Calculates optimal pool sizes using server capacity formulas, selects the correct pooling mode (session/transaction/statement) based on ORM compatibility, generates production-ready pgbouncer.ini and docker-compose.yml, audits active CVEs, and validates ORM-specific constraints. Trigger when: pgbouncer setup, connection pooling, too many connections, max_connections exceeded, connection pool sizing, pgbouncer config, database connections scaling, pool mode selection, or any mention of PgBouncer in a PostgreSQL context. Part of database-ecosystem.'
---

# PgBouncer Architect

Analyze the workload, calculate the right numbers, select the right mode,
generate production-ready config. Never hardcode values — always derive them
from actual system parameters.

**Core principle:** Wrong pool mode = silent bugs. Wrong pool size = either
wasted resources or connection starvation. Always ask before generating.

---

## PHASE 1 — Discovery

Before writing a single config line, collect these inputs.
Ask the user or derive from context:

### 1.1 Server Capacity
```
□ PostgreSQL max_connections  (default: 100)
□ Server RAM available to PostgreSQL
□ Number of CPU cores
□ Current active connections (if existing system):
    SELECT count(*) FROM pg_stat_activity;
```

### 1.2 Application Profile
```
□ Application framework / language
    (Node.js, Python/FastAPI, Go, .NET, ...)
□ ORM / driver:
    Drizzle · Prisma · TypeORM · SQLAlchemy · asyncpg · pg · pgx · Npgsql
□ Number of application instances / workers
□ Expected concurrent users (peak)
□ Average transaction duration (ms)
□ Do you use any of these? (critical for mode selection)
    - Prepared statements (persisted across transactions)
    - LISTEN / NOTIFY
    - Advisory locks
    - SET / RESET session variables
    - Temporary tables
    - WITH HOLD cursors
```

### 1.3 Deployment Context
```
□ Deployment: Docker Compose · Kubernetes · bare metal · managed cloud
□ Is PgBouncer alongside PostgreSQL or on a separate host?
□ TLS required between app ↔ PgBouncer ↔ PostgreSQL?
□ High availability required? (multiple PgBouncer instances)
□ Monitoring stack: Prometheus · Grafana · Datadog · none
```

### 1.4 Discovery Summary (show before proceeding)
```
📋 System Profile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PostgreSQL max_connections : N
Application workers        : N
ORM / driver               : X
Session features used      : yes/no
Peak concurrent users      : N
Deployment                 : X
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Proceed with these values?
```

---

## PHASE 2 — Pool Mode Selection

**This is the most critical decision.** Wrong mode breaks features silently.

### Decision Matrix

| Feature Used | Session | Transaction | Statement |
|-------------|---------|-------------|-----------|
| Prepared statements (persistent) | ✅ | ❌ | ❌ |
| LISTEN / NOTIFY | ✅ | ❌ | ❌ |
| Advisory locks | ✅ | ❌ | ❌ |
| SET session variables | ✅ | ❌ | ❌ |
| Temporary tables | ✅ | ❌ | ❌ |
| WITH HOLD cursors | ✅ | ❌ | ❌ |
| Connection efficiency | 🔴 Low | 🟢 High | 🟢 Highest |
| Scalability | 🔴 Low | 🟢 High | 🟢 Highest |

### Mode Selection Logic

```
IF any session-level feature is used:
    → SESSION mode
    → Warn: connection efficiency is low, consider refactoring

ELSE IF ORM is Prisma or Drizzle:
    → TRANSACTION mode
    → Note: disable prepared statement cache (see ORM section)

ELSE IF ORM is SQLAlchemy + asyncpg:
    → TRANSACTION mode
    → Note: set statement_cache_size=0

ELSE IF all queries are simple, stateless:
    → TRANSACTION mode (default recommendation)

NEVER recommend STATEMENT mode unless:
    → User explicitly requests it
    → AND workload is confirmed single-statement only
```

### Mode announcement
```
🔧 Selected Mode: TRANSACTION
Reason: Drizzle ORM detected, no session-level features reported.
Trade-off: Prepared statements will not persist across transactions.
Action required: See ORM compatibility section.
```

---

## PHASE 3 — Pool Size Calculation

Never use arbitrary numbers. Derive from system parameters.

### 3.1 Core Formula

```
# PostgreSQL connections reserved for PgBouncer
pgbouncer_reserved = max_connections - superuser_reserved - admin_connections
# superuser_reserved default: 3
# admin_connections: 2-5 (for maintenance, monitoring)

pgbouncer_reserved = max_connections - 3 - 3  # conservative

# default_pool_size per database-user pair
default_pool_size = floor(pgbouncer_reserved / number_of_pools)

# For single app, single DB (most common case):
default_pool_size = pgbouncer_reserved  # e.g. 94 for max_connections=100
```

### 3.2 max_client_conn Formula

```
# Rule of thumb: 3-5x the number of actual server connections
max_client_conn = default_pool_size * 4

# But also consider:
max_client_conn >= app_workers * connections_per_worker * 1.5  # headroom

# Take the larger of the two:
max_client_conn = max(default_pool_size * 4, app_workers * conn_per_worker * 1.5)
```

### 3.3 Reserve Pool

```
reserve_pool_size = ceil(default_pool_size * 0.1)  # 10% of pool
reserve_pool_timeout = 3  # seconds before using reserve
```

### 3.4 Example Calculation

```
Given:
  max_connections = 100
  app_workers     = 8
  pools           = 1 (single app, single DB)

Calculation:
  pgbouncer_reserved = 100 - 3 - 3 = 94
  default_pool_size  = 94
  reserve_pool_size  = ceil(94 * 0.1) = 10
  max_client_conn    = max(94 * 4, 8 * 10 * 1.5) = max(376, 120) = 376

Result:
  default_pool_size  = 94
  reserve_pool_size  = 10
  max_client_conn    = 376
```

### 3.5 Timeout Parameters

```
# How long an unused server connection stays open
server_lifetime = 3600        # 1 hour (reduce for cloud DBs with idle limits)

# How long an idle server connection stays before disconnect
server_idle_timeout = 600     # 10 minutes

# How long a client can sit idle
client_idle_timeout = 300     # 5 minutes

# How long to wait for a server connection before error
query_wait_timeout = 30       # 30 seconds

# For cloud databases (RDS, Supabase, Neon) — reduce:
server_lifetime = 300         # 5 min (avoid cloud idle disconnects)
server_idle_timeout = 120     # 2 min
```

---

## PHASE 4 — ORM Compatibility

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

---

## PHASE 5 — Generate Configuration Files

### 5.1 pgbouncer.ini

```ini
[databases]
; Database alias = actual PostgreSQL connection
; Use * to allow any database name to pass through
{DB_NAME} = host={PG_HOST} port={PG_PORT} dbname={PG_DBNAME}

; Read replica (optional)
; {DB_NAME}_readonly = host={REPLICA_HOST} port=5432 dbname={PG_DBNAME}

[pgbouncer]
;; Network
listen_addr = 0.0.0.0
listen_port = 6432

;; Auth — NEVER use trust or plain in production
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt

;; Pooling
pool_mode = {CALCULATED_MODE}       ; session | transaction | statement
max_client_conn = {CALCULATED}      ; derived from formula
default_pool_size = {CALCULATED}    ; derived from formula
min_pool_size = {CEIL(POOL*0.1)}    ; warm pool — avoid cold start
reserve_pool_size = {CALCULATED}    ; 10% of default_pool_size
reserve_pool_timeout = 3

;; Timeouts
server_lifetime = {CALCULATED}      ; 3600 standard / 300 cloud
server_idle_timeout = {CALCULATED}  ; 600 standard / 120 cloud
client_idle_timeout = 300
query_wait_timeout = 30
client_login_timeout = 10

;; TLS (enable in production)
; server_tls_sslmode = require
; server_tls_ca_file = /etc/ssl/certs/ca-certificates.crt
; client_tls_sslmode = require
; client_tls_cert_file = /etc/pgbouncer/pgbouncer.crt
; client_tls_key_file = /etc/pgbouncer/pgbouncer.key

;; Logging
log_connections = 0     ; set to 1 only for debugging (high volume)
log_disconnections = 0
log_pooler_errors = 1
stats_period = 60

;; Admin console — for monitoring queries
admin_users = pgbouncer_admin
stats_users = pgbouncer_stats

;; Ignore startup params sent by ORMs
; Required for some ORMs that send extra connection params
ignore_startup_parameters = extra_float_digits,options
```

### 5.2 userlist.txt

```
; Generate hashes with:
; psql -c "SELECT concat('\"', usename, '\" \"', passwd, '\"') FROM pg_shadow WHERE usename = '{YOUR_USER}';"
;
; NEVER put plaintext passwords here.
; Format: "username" "SCRAM-SHA-256$<iterations>:<salt>$<stored_key>:<server_key>"

"{APP_USER}" "SCRAM-SHA-256$4096:{HASH_FROM_PSQL}"
"pgbouncer_admin" "SCRAM-SHA-256$4096:{HASH_FROM_PSQL}"
```

### 5.3 docker-compose-pgbouncer.yml

```yaml
services:
  pgbouncer:
    image: bitnami/pgbouncer:latest    # actively maintained, rootless
    # Alternative: edoburu/pgbouncer (also good)
    restart: unless-stopped
    ports:
      - "6432:6432"
    environment:
      # Bitnami image env vars
      POSTGRESQL_HOST: ${POSTGRESQL_HOST:-postgres}
      POSTGRESQL_PORT: ${POSTGRESQL_PORT:-5432}
      POSTGRESQL_DATABASE: ${POSTGRESQL_DATABASE}
      POSTGRESQL_USERNAME: ${POSTGRESQL_USERNAME}
      POSTGRESQL_PASSWORD: ${POSTGRESQL_PASSWORD}
      PGBOUNCER_POOL_MODE: ${PGBOUNCER_POOL_MODE:-transaction}
      PGBOUNCER_MAX_CLIENT_CONN: ${PGBOUNCER_MAX_CLIENT_CONN:-400}
      PGBOUNCER_DEFAULT_POOL_SIZE: ${PGBOUNCER_DEFAULT_POOL_SIZE:-94}
      PGBOUNCER_MIN_POOL_SIZE: ${PGBOUNCER_MIN_POOL_SIZE:-10}
      PGBOUNCER_RESERVE_POOL_SIZE: ${PGBOUNCER_RESERVE_POOL_SIZE:-10}
      PGBOUNCER_IGNORE_STARTUP_PARAMETERS: extra_float_digits,options
      PGBOUNCER_AUTH_TYPE: scram-sha-256
    volumes:
      - ./pgbouncer.ini:/bitnami/pgbouncer/conf/pgbouncer.ini:ro
      - ./userlist.txt:/bitnami/pgbouncer/conf/userlist.txt:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -h 127.0.0.1 -p 6432 -U ${POSTGRESQL_USERNAME}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - db_network

networks:
  db_network:
    driver: bridge
```

---

## PHASE 6 — Monitoring Queries

Provide these as a ready-to-use reference:

```sql
-- Connect to PgBouncer admin console:
-- psql -h 127.0.0.1 -p 6432 -U pgbouncer_admin pgbouncer

-- Pool status: active vs idle vs waiting
SHOW POOLS;
-- Key columns: cl_active, cl_waiting, sv_active, sv_idle, sv_used, maxwait

-- If maxwait > 0: clients are waiting → pool may be undersized

-- Aggregate stats (requests/sec, avg query time)
SHOW STATS;

-- Current client connections
SHOW CLIENTS;

-- Current server (PostgreSQL) connections
SHOW SERVERS;

-- Global config
SHOW CONFIG;

-- Live update pool size without restart:
SET default_pool_size=120;
RELOAD;

-- Prometheus metrics (if pgbouncer_exporter is deployed):
-- Scrape: http://pgbouncer-exporter:9127/metrics
-- Key metrics:
--   pgbouncer_pools_cl_waiting    → should be 0
--   pgbouncer_pools_sv_active     → vs pool_size
--   pgbouncer_stats_avg_wait_time → should be <5ms
```

---

## PHASE 7 — CVE & Security Audit

Always check before finalizing config.

### Known Active CVEs (as of early 2026)

```
CVE-2025-12819 (PgBouncer < 1.25.0) — CRITICAL
  Affected: auth_user + track_extra_parameters + auth_query combination
  Risk: Unauthenticated SQL execution
  Fix: Upgrade to >= 1.25.1

CVE-2024-XXXX — Check https://www.pgbouncer.org/changelog.html for latest
```

**Always pin to a specific version:**
```yaml
# BAD — gets whatever latest is, may be vulnerable
image: edoburu/pgbouncer:latest

# GOOD — pinned, predictable
image: bitnami/pgbouncer:1.25.1
```

### Security Checklist
```
□ auth_type = scram-sha-256  (never md5, never trust in production)
□ No plaintext passwords in userlist.txt
□ admin_users locked down (not exposed to app)
□ TLS enabled between app ↔ PgBouncer AND PgBouncer ↔ PostgreSQL
□ PgBouncer admin port (6432/pgbouncer db) not exposed publicly
□ Image pinned to specific version
□ userlist.txt mounted read-only (:ro)
□ No DATABASE_URL containing passwords in docker-compose env (use secrets)
```

---

## PHASE 8 — Report

Generate `pgbouncer-report.md` summarizing all decisions:

```markdown
# PgBouncer Architecture Report

**Generated:** {date}
**Version:** pgbouncer-architect v1.0.0

## System Profile
| Parameter | Value |
|-----------|-------|
| PostgreSQL max_connections | N |
| App workers | N |
| ORM | X |
| Session features | yes/no |

## Decisions

### Pool Mode: {MODE}
**Reason:** {why this mode}
**Trade-offs:** {what this mode cannot do}

### Pool Sizing
| Parameter | Value | Formula |
|-----------|-------|---------|
| default_pool_size | N | max_connections - 6 |
| max_client_conn | N | pool_size × 4 |
| reserve_pool_size | N | pool_size × 10% |

## ORM Configuration Required
{ORM-specific changes the developer must make}

## Security
{CVE status, checklist results}

## Monitoring
{Where to look, what to watch}

## Files Generated
- pgbouncer.ini
- docker-compose-pgbouncer.yml
- userlist.txt (template — fill hashes manually)
```

---

## SKIP CONDITIONS

- Project uses managed connection pooling already (Supabase built-in, AWS RDS Proxy, Neon)
  → Check if PgBouncer is still needed or redundant
- Serverless / edge functions (each invocation = new connection)
  → PgBouncer alone insufficient → recommend connection pooler at platform level
- SQLite / embedded DB
  → Not applicable

---

## REFERENCE FILES

- `references/pooling-modes.md` — Deep dive: session vs transaction vs statement
- `references/sizing-formulas.md` — Extended formulas for complex multi-tenant setups
