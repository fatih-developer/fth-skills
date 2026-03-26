# Pool Sizing Formulas — Extended

## Single App, Single Database (Standard)

```
pgbouncer_reserved = max_connections - superuser_reserved(3) - admin(3)
default_pool_size  = pgbouncer_reserved
max_client_conn    = max(pool_size × 4, workers × conn_per_worker × 1.5)
reserve_pool_size  = ceil(pool_size × 0.1)
```

## Multi-App, Single Database

```
# Each app gets a share of the pool
pool_per_app = floor(pgbouncer_reserved / number_of_apps)

# In pgbouncer.ini — configure per database-user pair:
[databases]
mydb = host=postgres port=5432 dbname=mydb pool_size=30  ; app1
mydb = host=postgres port=5432 dbname=mydb pool_size=30  ; app2
mydb = host=postgres port=5432 dbname=mydb pool_size=34  ; app3 (gets remainder)
```

## Multi-Tenant SaaS

```
# Tenant isolation: each tenant gets a separate pool user
# Pool size per tenant depends on tier

[databases]
; Enterprise tenants: larger pool
enterprise_db = host=postgres dbname=saas_db user=enterprise_pool pool_size=20

; Standard tenants: smaller pool
standard_db = host=postgres dbname=saas_db user=standard_pool pool_size=5

; Free tier: minimal
free_db = host=postgres dbname=saas_db user=free_pool pool_size=2
```

## Kubernetes / Horizontal Scaling

```
# When app scales horizontally, total connections = pods × connections_per_pod
# PgBouncer absorbs this burst

# Per pod: connect to PgBouncer with pool_size=1
# PgBouncer: maintains fixed pool to PostgreSQL

# Example: 50 pods × 1 connection each = 50 client connections to PgBouncer
# PgBouncer maintains 20 connections to PostgreSQL
# Savings: 30 connections (60%)

# Formula:
pgbouncer_pool_size = ceil(peak_pod_count × avg_concurrent_queries_per_pod × 1.2)
```

## Read Replica Configuration

```ini
[databases]
; Write database → primary
mydb = host=primary-postgres port=5432 dbname=mydb

; Read-only replica → replica
mydb_ro = host=replica-postgres port=5432 dbname=mydb

; In your app:
; - Use DATABASE_URL for writes
; - Use DATABASE_URL_READONLY for reads
```

## Sizing for Different Workload Types

### OLTP (Online Transaction Processing)
```
# Many short transactions, high concurrency
# Optimal: transaction mode, small pool, many client connections

default_pool_size = 20-50
max_client_conn   = 1000-5000
pool_mode         = transaction
query_wait_timeout = 10  # fail fast
```

### OLAP (Analytics / Reporting)
```
# Few long-running queries, low concurrency
# Optimal: session mode or transaction mode, larger pool

default_pool_size = 5-10   # fewer but longer connections
max_client_conn   = 50-100
pool_mode         = session  # long queries often use session features
server_lifetime   = 7200     # keep connections alive longer
query_wait_timeout = 300     # wait longer for available connection
```

### Mixed (OLTP + Reporting)
```
# Use separate PgBouncer instances or named pools:

[databases]
mydb_oltp = host=postgres dbname=mydb pool_mode=transaction pool_size=40
mydb_olap = host=postgres dbname=mydb pool_mode=session pool_size=5

; OLTP app connects to :6432/mydb_oltp
; Reporting app connects to :6432/mydb_olap
```

## When PostgreSQL max_connections is Fixed (Cloud/Managed)

```
# Supabase free tier: max 60 connections
# Supabase Pro: max 200
# Neon: max 112 (varies by plan)
# RDS db.t3.micro: max 170 (depends on RAM)

# Formula for managed DB:
pgbouncer_reserved = max_connections × 0.9  # leave 10% for direct access
default_pool_size  = pgbouncer_reserved
min_pool_size      = ceil(pool_size × 0.1)

# For Supabase + PgBouncer:
# Supabase already has its own PgBouncer (port 6543)
# Using external PgBouncer + Supabase's PgBouncer = double pooling
# → Connect external PgBouncer directly to PostgreSQL port (5432), not 6543
```

## Detecting Pool Exhaustion

```sql
-- Connect to PgBouncer admin: psql -p 6432 pgbouncer

-- Check for waiting clients (cl_waiting > 0 = pool too small)
SHOW POOLS;

-- Check max wait time (maxwait > 100ms = investigate)
SELECT pool_name, cl_waiting, maxwait, maxwait_us
FROM pgbouncer.pools
WHERE cl_waiting > 0;

-- PostgreSQL side: check active connections vs max
SELECT count(*), state
FROM pg_stat_activity
GROUP BY state;

-- Connection headroom
SELECT max_conn, used, res_for_super,
       max_conn - used - res_for_super AS available
FROM (
  SELECT count(*) AS used FROM pg_stat_activity
) u,
(SELECT setting::int AS max_conn FROM pg_settings WHERE name = 'max_connections') m,
(SELECT setting::int AS res_for_super FROM pg_settings WHERE name = 'superuser_reserved_connections') r;
```

## Pgbench Validation

After configuration, validate with pgbench:

```bash
# Initialize test data
pgbench -i -s 10 -h pgbouncer -p 6432 -U app_user mydb

# Run benchmark: 10 clients, 5 threads, 60 seconds
pgbench -c 10 -j 5 -T 60 -h pgbouncer -p 6432 -U app_user mydb

# High concurrency test: 100 clients
pgbench -c 100 -j 10 -T 60 -h pgbouncer -p 6432 -U app_user mydb

# Watch PgBouncer during test:
watch -n 1 'psql -p 6432 -U pgbouncer_admin pgbouncer -c "SHOW POOLS;"'

# Expected healthy output:
# cl_active ≈ default_pool_size
# cl_waiting = 0  (or minimal)
# maxwait < 100ms
```
