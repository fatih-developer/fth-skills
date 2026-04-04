# SQLite Omni Skill References

Bu klasör, SQLite Omni skill için detaylı rehberler içerir. **İhtiyacınıza göre sadece ilgili dosyayı okuyun** — tüm referansları aynı anda yüklemeyin.

## Hızlı Karar Ağacı

```
Ne ihtiyacınız var?
├── TypeScript + Bun projesi?              → TYPESCRIPT_DRIZZLE.md
├── Python / FastAPI projesi?                → PYTHON.md
├── Performans, WAL, PRAGMA ayarı?          → PERFORMANCE.md
├── Full-text arama (FTS5)?                 → FTS5_VECTOR.md  §FTS5
├── AI vektör embeddings?                  → FTS5_VECTOR.md  §sqlite-vec
├── Cloud SQLite (Turso / D1)?               → CLOUD.md
├── CLI + SQLite stateful Skill mi yazıyorsunuz? → CLI_SKILL_PATTERN.md
└── Şema tasarımı ve normalizasyon?        → Ana SKILL.md  §Schema Design
```

## Referans Dosyaları

| Dosya | Konu | Kullanım Senaryosu |
|-------|------|-------------------|
| `TYPESCRIPT_DRIZZLE.md` | Bun + Drizzle ORM | TypeScript projelerinde type-safe SQLite, migrations, relations |
| `PYTHON.md` | Python sqlite3/asyncio | FastAPI, asyncio, connection pooling, raw SQL migrations |
| `PERFORMANCE.md` | PRAGMA tuning, profiling | Yavaş sorgular, WAL mode optimizasyonu, benchmark |
| `FTS5_VECTOR.md` | FTS5 + sqlite-vec | Full-text search, AI embeddings, vektör similarity search |
| `CLOUD.md` | Turso, Cloudflare D1 | Edge deployment, multi-region, serverless SQLite |
| `CLI_SKILL_PATTERN.md` | CLI Skill pattern | Stateful CLI araçları, System Skill geliştirme |

## Skill Kullanım Tetikleyicileri

Bu skill otomatik olarak şu anahtar kelimeler için çalışır:
- `sqlite`, `sqlite3`, `bun:sqlite`, `better-sqlite3`
- `aiosqlite`, `libsql`, `Turso`, `Cloudflare D1`
- `WAL mode`, `FTS5`, `sqlite-vec`
- Schema design, migrations, PRAGMA, backup/restore

> **Not:** PRAGMA ayarları ve driver-specific pattern'ler çok önemli — her zaman bu skill'i kullanın.
