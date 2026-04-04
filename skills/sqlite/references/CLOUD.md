# Cloud SQLite Reference

## Table of Contents
1. [Turso (libsql)](#turso-libsql)
2. [Cloudflare D1](#cloudflare-d1)
3. [Migration Strategy: Local → Cloud](#migration-strategy-local--cloud)

---

# Turso (libsql)

Turso is a managed cloud SQLite built on [libsql](https://github.com/tursodatabase/libsql)
(an open-source SQLite fork). Multi-region replicas, edge-close reads, HTTP + WebSocket API.

## Setup

```bash
# Install Turso CLI
curl -sSfL https://get.tur.so/install.sh | bash

# Auth
turso auth login

# Create database
turso db create myapp

# Get connection URL + token
turso db show myapp --url     # libsql://myapp-<org>.turso.io
turso db tokens create myapp  # eyJhbGci...
```

## TypeScript + Drizzle + Turso

```bash
bun add @libsql/client drizzle-orm
bun add -D drizzle-kit
```

```typescript
// src/db/index.ts
import { createClient } from '@libsql/client';
import { drizzle } from 'drizzle-orm/libsql';
import * as schema from './schema';

const client = createClient({
  url: process.env.TURSO_URL!,      // libsql://myapp-org.turso.io
  authToken: process.env.TURSO_TOKEN!,
});

export const db = drizzle(client, { schema });
```

```typescript
// drizzle.config.ts — Turso variant
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'turso',
  dbCredentials: {
    url: process.env.TURSO_URL!,
    authToken: process.env.TURSO_TOKEN!,
  },
} satisfies Config;
```

## Embedded Replicas (Offline-First + Edge)

```typescript
// Local replica that syncs from Turso — zero latency reads
import { createClient } from '@libsql/client';
import { drizzle } from 'drizzle-orm/libsql';

const client = createClient({
  url: 'file:local.db',                   // Local SQLite file
  syncUrl: process.env.TURSO_URL!,        // Sync from Turso
  authToken: process.env.TURSO_TOKEN!,
  syncInterval: 60,                       // Sync every 60 seconds
});

// Manual sync when needed
await client.sync();

export const db = drizzle(client, { schema });
```

## Python + Turso

```bash
pip install libsql-client
```

```python
import libsql_client
import asyncio

async def main():
    async with libsql_client.create_client(
        url=os.environ["TURSO_URL"],
        auth_token=os.environ["TURSO_TOKEN"],
    ) as client:
        result = await client.execute("SELECT * FROM users LIMIT 10")
        for row in result.rows:
            print(dict(zip(result.columns, row)))

asyncio.run(main())
```

## Turso CLI Cheatsheet

```bash
turso db list                          # List databases
turso db show myapp                    # DB info + size
turso db shell myapp                   # Interactive SQL shell
turso db shell myapp < schema.sql      # Run SQL file
turso db locations                     # Available regions
turso db replicate myapp ams           # Add replica in Amsterdam
turso db destroy myapp                 # Delete database
turso db tokens create myapp --expiry 7d  # Expiring token
```

---

# Cloudflare D1

D1 is Cloudflare's SQLite-compatible database for Workers. Runs at the edge globally.

## Setup

```bash
npm install -g wrangler
wrangler login

# Create D1 database
wrangler d1 create myapp-db
```

## wrangler.jsonc

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "d1_databases": [
    {
      "binding": "DB",             // Access as env.DB in Worker
      "database_name": "myapp-db",
      "database_id": "your-uuid",
      "preview_database_id": "local",
      "migrations_dir": "./drizzle"
    }
  ]
}
```

## TypeScript + Drizzle + D1

```bash
npm install drizzle-orm
npm install -D drizzle-kit @cloudflare/workers-types
```

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/d1';
import type { D1Database } from '@cloudflare/workers-types';
import * as schema from './schema';

export function getDb(d1: D1Database) {
  return drizzle(d1, { schema });
}

// Worker handler
export default {
  async fetch(request: Request, env: { DB: D1Database }) {
    const db = getDb(env.DB);
    const users = await db.select().from(schema.users).limit(10);
    return Response.json(users);
  },
};
```

```typescript
// drizzle.config.ts — D1 variant
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'sqlite',
  driver: 'd1-http',
  dbCredentials: {
    accountId: process.env.CLOUDFLARE_ACCOUNT_ID!,
    databaseId: process.env.CLOUDFLARE_DATABASE_ID!,
    token: process.env.CLOUDFLARE_D1_TOKEN!,
  },
} satisfies Config;
```

## D1 CLI Commands

```bash
# Local dev
wrangler d1 execute myapp-db --local --file=schema.sql
wrangler d1 execute myapp-db --local --command="SELECT * FROM users"

# Production
wrangler d1 execute myapp-db --file=schema.sql
wrangler d1 execute myapp-db --command="PRAGMA table_info(users)"

# Migrations with Drizzle
bunx drizzle-kit generate
wrangler d1 migrations apply myapp-db
wrangler d1 migrations apply myapp-db --local  # Local only

# Backup
wrangler d1 export myapp-db --output=backup.sql
```

## D1 Limitations vs Regular SQLite

| Feature | D1 | Regular SQLite |
|---|---|---|
| Max DB size | 10 GB | No limit |
| Max row size | 2 MB | No limit |
| Max columns | 100 | 2000 |
| `ATTACH DATABASE` | ❌ | ✅ |
| Custom extensions | ❌ | ✅ |
| WAL mode control | ❌ (managed) | ✅ |
| `sqlite-vec` | ❌ | ✅ |
| FTS5 | ✅ | ✅ |

---

# Migration Strategy: Local → Cloud

## Local SQLite → Turso

```bash
# 1. Export local DB to SQL
sqlite3 app.db ".dump" > dump.sql

# 2. Create Turso DB
turso db create myapp

# 3. Import (for small DBs)
turso db shell myapp < dump.sql

# 4. For large DBs, use the upload API
turso db upload myapp app.db
```

## Local SQLite → D1

```bash
# 1. Export schema
sqlite3 app.db ".schema" > schema.sql

# 2. Export data as INSERT statements
sqlite3 app.db ".mode insert" ".output data.sql" ".dump" > /dev/null

# 3. Apply to D1
wrangler d1 execute myapp-db --file=schema.sql
wrangler d1 execute myapp-db --file=data.sql
```

## Choosing Between Turso and D1

| Need | Turso | D1 |
|---|---|---|
| Cloudflare Workers | ✅ (via HTTP) | ✅ (native binding) |
| Edge-close reads | ✅ Multi-region replicas | ✅ Global |
| Embedded replica | ✅ Offline-first | ❌ |
| Custom extensions | ✅ libsql | ❌ |
| Open source self-host | ✅ sqld | ❌ |
| Free tier | 500 DBs, 9 GB | 10 GB, 5M rows/day |
| Python SDK | ✅ libsql-client | ❌ (HTTP only) |
