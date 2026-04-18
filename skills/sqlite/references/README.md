# SQLite Omni Skill References

This folder contains detailed guides for the SQLite Omni skill. **Only read the relevant file according to your needs** — do not load all references at the same time.

## Quick Decision Tree

```
What do you need?
├── TypeScript + Bun project?              → TYPESCRIPT_DRIZZLE.md
├── Python / FastAPI project?                → PYTHON.md
├── Performance, WAL, PRAGMA tuning?          → PERFORMANCE.md
├── Full-text search (FTS5)?                 → FTS5_VECTOR.md  §FTS5
├── AI vector embeddings?                  → FTS5_VECTOR.md  §sqlite-vec
├── Cloud SQLite (Turso / D1)?               → CLOUD.md
├── Writing a CLI + SQLite stateful Skill? → CLI_SKILL_PATTERN.md
└── Schema design and normalization?        → Main SKILL.md  §Schema Design
```

## Reference Files

| File | Topic | Use Case |
|-------|------|-------------------|
| `TYPESCRIPT_DRIZZLE.md` | Bun + Drizzle ORM | Type-safe SQLite, migrations, relations for TypeScript projects |
| `PYTHON.md` | Python sqlite3/asyncio | FastAPI, asyncio, connection pooling, raw SQL migrations |
| `PERFORMANCE.md` | PRAGMA tuning, profiling | Slow queries, WAL mode optimization, benchmarking |
| `FTS5_VECTOR.md` | FTS5 + sqlite-vec | Full-text search, AI embeddings, vector similarity search |
| `CLOUD.md` | Turso, Cloudflare D1 | Edge deployment, multi-region, serverless SQLite |
| `CLI_SKILL_PATTERN.md` | CLI Skill pattern | Stateful CLI tools, System Skill development |

## Skill Use Triggers

This skill automatically triggers for these keywords:
- `sqlite`, `sqlite3`, `bun:sqlite`, `better-sqlite3`
- `aiosqlite`, `libsql`, `Turso`, `Cloudflare D1`
- `WAL mode`, `FTS5`, `sqlite-vec`
- Schema design, migrations, PRAGMA, backup/restore

> **Note:** PRAGMA settings and driver-specific patterns are very important — always use this skill.
