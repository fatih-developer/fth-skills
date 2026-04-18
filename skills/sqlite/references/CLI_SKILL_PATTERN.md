# System Skill Pattern: CLI + SQLite + SKILL.md

With this pattern, Claude can create **stateful** smart tools using a CLI tool + SQLite database + SKILL.md triad.

## Basic Concept

```
[User] → [Claude] → [CLI Binary] → [SQLite DB]
                 ↑              ↓
            SKILL.md      JSON/Table output
```

**Components:**
1. **CLI Binary** — Command line tool run by Claude
2. **SKILL.md** — The guide that teaches Claude how to use the system
3. **SQLite DB** — Persistent state store

---

## Why This Pattern?

- **Stateful**: Memory between conversations — Claude can query history in any session
- **Transparent**: Data is in SQLite, you can inspect it anytime with `sqlite3 cli`
- **Independent**: Single binary + single file = easy portability and backups
- **Extensible**: Claude can do things directly with SQL that the CLI doesn't natively do

---

## CLI Design Principles

### Mandatory

```bash
# Every CLI must have these:
./tool --help              # Comprehensive help output
./tool --version           # Version information
./tool --json              # Machine-readable JSON output mode

# Structured output Claude can read
./tool list --json
# → [{"id": 1, "task": "...", "status": "done"}]
```

### Command Structure

```bash
# Good CLI command design:
./tool <resource> <action> [options]

# Examples:
./tool task create --title "API integration" --priority high
./tool task list --status pending --limit 20
./tool task done 42
./tool task delete 42
./tool stats --period week
./tool export --format csv --output tasks.csv
```

### Decision Tree (for SKILL.md)

```markdown
## Quick Decision Tree

User request → Which command?
├─ New task → task create --title "..." [--priority high|med|low]
├─ List tasks → task list [--status pending|done] [--limit N]
├─ Complete task → task done <id>
├─ Statistics → stats [--period day|week|month]
├─ History → history [--days N]
└─ Analysis → Claude queries SQLite directly
```

---

## Creating a CLI with TypeScript/Bun

```typescript
// cli.ts — Compiled with Bun, becomes a zero-dependency binary
import { Database } from "bun:sqlite";
import { parseArgs } from "util";
import { join } from "path";

const DB_PATH = join(import.meta.dir, "data.db");

// DB setup
const db = new Database(DB_PATH);
db.run("PRAGMA journal_mode = WAL");
db.run("PRAGMA foreign_keys = ON");
db.run(`
  CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'pending',
    created_at INTEGER DEFAULT (unixepoch()),
    done_at INTEGER
  )
`);

// CLI parsing
const { values, positionals } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    json:     { type: "boolean", short: "j" },
    title:    { type: "string" },
    priority: { type: "string", default: "medium" },
    status:   { type: "string" },
    limit:    { type: "string", default: "20" },
    days:     { type: "string", default: "7" },
    help:     { type: "boolean", short: "h" },
  },
  allowPositionals: true,
});

const [resource, action] = positionals;
const asJson = values.json;

function out(data: unknown) {
  if (asJson) {
    console.log(JSON.stringify(data, null, 2));
  } else if (Array.isArray(data)) {
    console.table(data);
  } else {
    console.log(data);
  }
}

// Commands
if (resource === "task") {
  if (action === "create") {
    const task = db.query(`
      INSERT INTO tasks (title, priority) VALUES (?, ?) RETURNING *
    `).get(values.title!, values.priority) as any;
    out({ ok: true, task });

  } else if (action === "list") {
    const tasks = db.query(`
      SELECT * FROM tasks
      WHERE ($status IS NULL OR status = $status)
      ORDER BY created_at DESC LIMIT $limit
    `).all({
      $status: values.status ?? null,
      $limit: parseInt(values.limit ?? "20"),
    });
    out(tasks);

  } else if (action === "done") {
    const id = parseInt(positionals[2]);
    db.run(`UPDATE tasks SET status='done', done_at=unixepoch() WHERE id=?`, [id]);
    out({ ok: true, id });

  } else if (action === "delete") {
    const id = parseInt(positionals[2]);
    db.run("DELETE FROM tasks WHERE id = ?", [id]);
    out({ ok: true });
  }

} else if (resource === "stats") {
  const days = parseInt(values.days ?? "7");
  const stats = db.query(`
    SELECT
      COUNT(*) as total,
      SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) as done,
      SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
      ROUND(AVG(CASE WHEN done_at IS NOT NULL THEN done_at - created_at END), 0) as avg_duration_s
    FROM tasks
    WHERE created_at >= unixepoch() - ? * 86400
  `).get(days) as any;
  out(stats);

} else {
  console.log(`
Usage: tasks <resource> <action> [options]

Resources:
  task create --title "..." [--priority high|medium|low]
  task list   [--status pending|done] [--limit N]
  task done   <id>
  task delete <id>
  stats       [--days N]

Options:
  -j, --json    Output as JSON
  -h, --help    Show this help
`);
}
```

### Build

```bash
# Compile as a single binary with Bun (no dependencies)
bun build cli.ts --compile --outfile tasks

# Test
./tasks task create --title "Write SQLite skill" --priority high
./tasks task list --json
./tasks stats --days 7
```

---

## Python CLI Alternative

```python
#!/usr/bin/env python3
"""tasks CLI — Python stdlib only, no pip installs."""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "data.db"

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            created_at INTEGER DEFAULT (strftime('%s','now')),
            done_at INTEGER
        )
    """)
    conn.commit()
    return conn

def out(data, as_json=False):
    if as_json:
        print(json.dumps(data, indent=2))
    else:
        print(data)

parser = argparse.ArgumentParser(prog="tasks")
parser.add_argument("--json", "-j", action="store_true")
sub = parser.add_subparsers(dest="cmd")

# task subcommand
task_p = sub.add_parser("task")
task_sub = task_p.add_subparsers(dest="action")

create_p = task_sub.add_parser("create")
create_p.add_argument("--title", required=True)
create_p.add_argument("--priority", default="medium")

list_p = task_sub.add_parser("list")
list_p.add_argument("--status")
list_p.add_argument("--limit", type=int, default=20)

done_p = task_sub.add_parser("done")
done_p.add_argument("id", type=int)

stats_p = sub.add_parser("stats")
stats_p.add_argument("--days", type=int, default=7)

args = parser.parse_args()
db = get_db()

if args.cmd == "task":
    if args.action == "create":
        cur = db.execute(
            "INSERT INTO tasks (title, priority) VALUES (?, ?) RETURNING *",
            (args.title, args.priority)
        )
        task = dict(cur.fetchone())
        db.commit()
        out({"ok": True, "task": task}, args.json)

    elif args.action == "list":
        rows = db.execute(
            "SELECT * FROM tasks WHERE (? IS NULL OR status = ?) ORDER BY created_at DESC LIMIT ?",
            (args.status, args.status, args.limit)
        ).fetchall()
        out([dict(r) for r in rows], args.json)

    elif args.action == "done":
        db.execute("UPDATE tasks SET status='done', done_at=strftime('%s','now') WHERE id=?", (args.id,))
        db.commit()
        out({"ok": True}, args.json)

elif args.cmd == "stats":
    row = db.execute("""
        SELECT COUNT(*) total,
               SUM(status='done') done,
               SUM(status='pending') pending
        FROM tasks WHERE created_at >= strftime('%s','now') - ? * 86400
    """, (args.days,)).fetchone()
    out(dict(row), args.json)

db.close()
```

---

## SKILL.md Template (For System Skill)

```markdown
---
name: tasks
description: >
  Task tracking system. Use when the user wants to add, list, complete tasks or
  view statistics. Triggers: "add task", "todo",
  "task", "what did I do", "weekly summary", "statistics".
---

# Tasks System Skill

Manage the task tracking system. Works with a CLI binary and SQLite database.

## Setup

Skill directory: `~/.claude/skills/tasks/`
CLI: `./tasks`
DB: `./data.db`

## Quick Decision Tree

User request → Command
├─ New task → `./tasks task create --title "..." [--priority high]`
├─ View tasks → `./tasks task list [--status pending]`
├─ Complete → `./tasks task done <id>`
├─ Statistics → `./tasks stats [--days 7]`
└─ Analysis (No CLI) → Claude looks directly at SQLite

## Direct SQL (Advanced Analysis)

Claude can directly run queries not covered by the CLI:

```bash
sqlite3 data.db "SELECT priority, COUNT(*) FROM tasks GROUP BY priority"
```

## Important Notes

- Check status before every command invocation with `./tasks task list --json`
- Decide by parsing the JSON output (use the `--json` flag)
- Prefer direct SQL for large data analysis
```

---

## System Ideas

The following systems work perfectly with this pattern:

| System | CLI Commands | SQLite Tables |
|---|---|---|
| Pomodoro timer | start, stop, stats, history | sessions |
| Expense tracking | tx add, tx list, budget | transactions, categories |
| Reading list | book add, book done, stats | books, sessions |
| API key management | key add, key list, key rotate | api_keys, usage_logs |
| Project time tracking | log start, log stop, report | time_entries, projects |
| Agent log analysis | log ingest, log search, stats | agent_logs, sessions |
