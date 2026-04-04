# System Skill Pattern: CLI + SQLite + SKILL.md

Bu pattern ile Claude, bir CLI aracı + SQLite veritabanı + SKILL.md üçlüsünü kullanarak
**kalıcı durum tutan** akıllı araçlar oluşturabilir.

## Temel Konsept

```
[Kullanıcı] → [Claude] → [CLI Binary] → [SQLite DB]
                 ↑              ↓
            SKILL.md      JSON/Table output
```

**Bileşenler:**
1. **CLI Binary** — Claude'un çalıştırdığı komut satırı aracı
2. **SKILL.md** — Claude'a sistemin nasıl kullanılacağını öğreten kılavuz
3. **SQLite DB** — Kalıcı durum deposu

---

## Neden Bu Pattern?

- **Stateful**: Konuşmalar arası hafıza — Claude her oturumda geçmişi sorgulayabilir
- **Şeffaf**: Veriler SQLite'ta, dilediğinde `sqlite3 cli` ile inceleyebilirsin
- **Bağımsız**: Tek binary + tek dosya = taşıma, yedekleme kolaylığı
- **Genişletilebilir**: Claude, CLI'ın yapmadığı şeyleri doğrudan SQL ile yapabilir

---

## CLI Tasarım İlkeleri

### Zorunlular

```bash
# Her CLI şunlara sahip olmalı:
./arac --help              # Kapsamlı yardım çıktısı
./arac --version           # Versiyon bilgisi
./arac --json              # Makine-okunur JSON çıktı modu

# Claude'un okuyabileceği yapılandırılmış çıktı
./arac list --json
# → [{"id": 1, "task": "...", "status": "done"}]
```

### Komut Yapısı

```bash
# İyi CLI komut tasarımı:
./arac <kaynak> <eylem> [seçenekler]

# Örnekler:
./arac task create --title "API entegrasyonu" --priority high
./arac task list --status pending --limit 20
./arac task done 42
./arac task delete 42
./arac stats --period week
./arac export --format csv --output tasks.csv
```

### Karar Ağacı (SKILL.md için)

```markdown
## Quick Decision Tree

Kullanıcı isteği → Hangi komut?
├─ Yeni görev → task create --title "..." [--priority high|med|low]
├─ Görevleri listele → task list [--status pending|done] [--limit N]
├─ Görevi tamamla → task done <id>
├─ İstatistik → stats [--period day|week|month]
├─ Geçmiş → history [--days N]
└─ Analiz → Claude doğrudan SQLite'ı sorgular
```

---

## TypeScript/Bun ile CLI Oluşturma

```typescript
// cli.ts — Bun ile derlenir, zero-dependency binary olur
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

### Derleme

```bash
# Bun ile tek binary olarak derle (dependency yok)
bun build cli.ts --compile --outfile tasks

# Test et
./tasks task create --title "SQLite skill yaz" --priority high
./tasks task list --json
./tasks stats --days 7
```

---

## Python CLI Alternatifi

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

## SKILL.md Şablonu (System Skill için)

```markdown
---
name: tasks
description: >
  Görev takip sistemi. Kullanıcı görev eklemek, listelemek, tamamlamak veya
  istatistik görmek istediğinde kullan. Triggers: "görev ekle", "yapılacaklar",
  "task", "ne yaptım", "haftalık özet", "istatistik".
---

# Tasks System Skill

Görev takip sistemini yönet. CLI binary ve SQLite veritabanı ile çalışır.

## Kurulum

Skill dizini: `~/.claude/skills/tasks/`
CLI: `./tasks`
DB: `./data.db`

## Quick Decision Tree

Kullanıcı isteği → Komut
├─ Yeni görev → `./tasks task create --title "..." [--priority high]`
├─ Görevleri gör → `./tasks task list [--status pending]`
├─ Tamamla → `./tasks task done <id>`
├─ İstatistik → `./tasks stats [--days 7]`
└─ Analiz (CLI yok) → Claude doğrudan SQLite'a bak

## Doğrudan SQL (Gelişmiş Analiz)

Claude, CLI'ın karşılamadığı sorguları doğrudan çalıştırabilir:

```bash
sqlite3 data.db "SELECT priority, COUNT(*) FROM tasks GROUP BY priority"
```

## Önemli Notlar

- Her komut çağrısından önce `./tasks task list --json` ile durumu kontrol et
- JSON çıktısını parse ederek karar ver (`--json` flag'i kullan)
- Büyük veri analizlerinde doğrudan SQL tercih et
```

---

## Sistem Fikirleri

Aşağıdaki sistemler bu pattern ile mükemmel çalışır:

| Sistem | CLI Komutları | SQLite Tabloları |
|---|---|---|
| Pomodoro timer | start, stop, stats, history | sessions |
| Harcama takibi | tx add, tx list, budget | transactions, categories |
| Okuma listesi | book add, book done, stats | books, sessions |
| API key yönetimi | key add, key list, key rotate | api_keys, usage_logs |
| Proje zaman takibi | log start, log stop, report | time_entries, projects |
| Agent log analizi | log ingest, log search, stats | agent_logs, sessions |
