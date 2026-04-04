# Bun + Drizzle ORM SQLite Reference

## Table of Contents
1. [Installation](#installation)
2. [Connection Setup](#connection-setup)
3. [Schema Definition](#schema-definition)
4. [Relations](#relations)
5. [Migrations](#migrations)
6. [CRUD Patterns](#crud-patterns)
7. [Advanced Queries](#advanced-queries)
8. [Drizzle Studio](#drizzle-studio)

---

## Installation

```bash
bun add drizzle-orm
bun add -D drizzle-kit
```

---

## Connection Setup

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/bun-sqlite';
import { Database } from 'bun:sqlite';
import * as schema from './schema';

const sqlite = new Database(process.env.DB_PATH ?? 'app.db');

// Always-on PRAGMAs
sqlite.run('PRAGMA journal_mode = WAL');
sqlite.run('PRAGMA synchronous = NORMAL');
sqlite.run('PRAGMA foreign_keys = ON');
sqlite.run('PRAGMA cache_size = -64000');
sqlite.run('PRAGMA temp_store = MEMORY');

export const db = drizzle(sqlite, { schema, logger: process.env.NODE_ENV === 'development' });

// Clean shutdown
process.on('exit', () => sqlite.close());
```

### drizzle.config.ts

```typescript
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'sqlite',
  dbCredentials: {
    url: process.env.DB_PATH ?? './app.db',
  },
  verbose: true,
  strict: true,
} satisfies Config;
```

---

## Schema Definition

### Core Column Types

```typescript
import {
  sqliteTable, text, integer, real, blob, index, uniqueIndex
} from 'drizzle-orm/sqlite-core';
import { sql, relations } from 'drizzle-orm';

// Users table
export const users = sqliteTable('users', {
  id:        integer('id').primaryKey({ autoIncrement: true }),
  ulid:      text('ulid').notNull().unique(),          // Application-level UUID
  email:     text('email').notNull().unique(),
  name:      text('name').notNull(),
  role:      text('role', { enum: ['admin', 'user', 'guest'] }).notNull().default('user'),
  meta:      text('meta', { mode: 'json' }).$type<Record<string, unknown>>(),
  isActive:  integer('is_active', { mode: 'boolean' }).notNull().default(true),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull().default(sql`(unixepoch())`),
  updatedAt: integer('updated_at', { mode: 'timestamp' }).notNull().default(sql`(unixepoch())`),
  deletedAt: integer('deleted_at', { mode: 'timestamp' }),
}, (t) => ({
  emailIdx:  index('idx_users_email').on(t.email),
  activeIdx: index('idx_users_active').on(t.isActive).where(sql`${t.deletedAt} IS NULL`),
}));

// Posts table
export const posts = sqliteTable('posts', {
  id:        integer('id').primaryKey({ autoIncrement: true }),
  title:     text('title').notNull(),
  slug:      text('slug').notNull().unique(),
  body:      text('body'),
  authorId:  integer('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  status:    text('status', { enum: ['draft', 'published', 'archived'] }).notNull().default('draft'),
  publishedAt: integer('published_at', { mode: 'timestamp' }),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull().default(sql`(unixepoch())`),
  updatedAt: integer('updated_at', { mode: 'timestamp' }).notNull().default(sql`(unixepoch())`),
}, (t) => ({
  authorIdx:  index('idx_posts_author').on(t.authorId),
  statusIdx:  index('idx_posts_status_created').on(t.status, t.createdAt),
  slugIdx:    uniqueIndex('idx_posts_slug').on(t.slug),
}));

// Type exports — very useful for TypeScript
export type User    = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
export type Post    = typeof posts.$inferSelect;
export type NewPost = typeof posts.$inferInsert;
```

---

## Relations

```typescript
// src/db/relations.ts
import { relations } from 'drizzle-orm';
import { users, posts } from './schema';

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

---

## Migrations

```bash
# Generate migration from schema changes
bunx drizzle-kit generate

# Apply migrations to the database
bunx drizzle-kit migrate

# Push schema directly (dev only — destructive!)
bunx drizzle-kit push

# Pull schema from existing DB
bunx drizzle-kit pull

# Check migration status
bunx drizzle-kit check
```

### Programmatic Migration (Production)

```typescript
// src/db/migrate.ts
import { migrate } from 'drizzle-orm/bun-sqlite/migrator';
import { db } from './index';

migrate(db, { migrationsFolder: './drizzle' });
console.log('Migrations applied');
```

### Custom Raw Migration

```sql
-- drizzle/0002_add_updated_at_trigger.sql
CREATE TRIGGER set_users_updated_at
AFTER UPDATE ON users
BEGIN
  UPDATE users SET updated_at = unixepoch() WHERE id = NEW.id;
END;
```

---

## CRUD Patterns

```typescript
import { db } from './db';
import { users, posts } from './db/schema';
import { eq, and, or, gt, lt, like, isNull, isNotNull, desc, asc, count, sql } from 'drizzle-orm';

// --- INSERT ---
const [newUser] = await db.insert(users).values({
  ulid: crypto.randomUUID(),
  email: 'fatih@example.com',
  name: 'Fatih',
}).returning();

// Bulk insert
await db.insert(users).values([
  { ulid: crypto.randomUUID(), email: 'a@x.com', name: 'A' },
  { ulid: crypto.randomUUID(), email: 'b@x.com', name: 'B' },
]);

// Upsert (on conflict)
await db.insert(users)
  .values({ ulid: id, email: 'x@x.com', name: 'X' })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: 'X Updated', updatedAt: sql`(unixepoch())` },
  });

// --- SELECT ---
// All
const allUsers = await db.select().from(users);

// With conditions
const activeUsers = await db.select()
  .from(users)
  .where(and(eq(users.isActive, true), isNull(users.deletedAt)))
  .orderBy(desc(users.createdAt))
  .limit(20)
  .offset(0);

// Specific columns
const emails = await db.select({ id: users.id, email: users.email }).from(users);

// With relations (requires relationsImported in drizzle())
const usersWithPosts = await db.query.users.findMany({
  where: isNull(users.deletedAt),
  with: { posts: { where: eq(posts.status, 'published') } },
  limit: 10,
});

// Single record
const user = await db.query.users.findFirst({
  where: eq(users.email, 'fatih@example.com'),
});

// Count
const [{ total }] = await db.select({ total: count() }).from(users);

// Raw SQL when needed
const result = await db.all(sql`SELECT * FROM users WHERE json_extract(meta, '$.plan') = 'pro'`);

// --- UPDATE ---
await db.update(users)
  .set({ name: 'New Name', updatedAt: sql`(unixepoch())` })
  .where(eq(users.id, 1));

// --- DELETE ---
await db.delete(users).where(eq(users.id, 1));

// Soft delete
await db.update(users)
  .set({ deletedAt: sql`(unixepoch())` })
  .where(eq(users.id, 1));
```

---

## Advanced Queries

### Joins

```typescript
const postsWithAuthors = await db
  .select({
    postId: posts.id,
    title: posts.title,
    authorName: users.name,
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id))
  .where(eq(posts.status, 'published'));
```

### Pagination with Cursor

```typescript
// Cursor-based pagination (better than OFFSET for large datasets)
const getPage = async (cursor?: number, limit = 20) => {
  return db.select().from(posts)
    .where(cursor ? gt(posts.id, cursor) : undefined)
    .orderBy(asc(posts.id))
    .limit(limit);
};
```

### Aggregation

```typescript
import { avg, sum, max, min } from 'drizzle-orm';

const stats = await db.select({
  total:   count(),
  avgAge:  avg(users.age),
  maxDate: max(users.createdAt),
}).from(users).groupBy(users.role);
```

### Transactions

```typescript
const result = await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values({ ... }).returning();
  await tx.insert(posts).values({ authorId: user.id, ... });
  return user;
});
```

---

## Drizzle Studio

```bash
# Open visual DB browser at localhost:4983
bunx drizzle-kit studio
```
