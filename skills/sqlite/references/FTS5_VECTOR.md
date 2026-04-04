# FTS5 Full-Text Search & sqlite-vec (AI Embeddings)

## Table of Contents
1. [FTS5 Full-Text Search](#fts5-full-text-search)
2. [sqlite-vec Vector Search](#sqlite-vec-vector-search)

---

# FTS5 Full-Text Search

FTS5 is SQLite's built-in full-text search extension. No extra dependencies needed.

## Basic Setup

```sql
-- Create an FTS5 virtual table
CREATE VIRTUAL TABLE posts_fts USING fts5(
  title,
  body,
  content=posts,      -- External content table (keeps data in posts, FTS is index only)
  content_rowid=id    -- Rowid column in the content table
);

-- Populate from existing data
INSERT INTO posts_fts(rowid, title, body)
SELECT id, title, body FROM posts;

-- Keep FTS in sync with triggers
CREATE TRIGGER posts_ai AFTER INSERT ON posts BEGIN
  INSERT INTO posts_fts(rowid, title, body) VALUES (NEW.id, NEW.title, NEW.body);
END;

CREATE TRIGGER posts_ad AFTER DELETE ON posts BEGIN
  INSERT INTO posts_fts(posts_fts, rowid, title, body)
  VALUES ('delete', OLD.id, OLD.title, OLD.body);
END;

CREATE TRIGGER posts_au AFTER UPDATE ON posts BEGIN
  INSERT INTO posts_fts(posts_fts, rowid, title, body)
  VALUES ('delete', OLD.id, OLD.title, OLD.body);
  INSERT INTO posts_fts(rowid, title, body) VALUES (NEW.id, NEW.title, NEW.body);
END;
```

## Searching

```sql
-- Basic search (matches any column)
SELECT rowid, title FROM posts_fts WHERE posts_fts MATCH 'sqlite performance';

-- Column-specific search
SELECT rowid FROM posts_fts WHERE posts_fts MATCH 'title:sqlite';

-- Phrase search
SELECT rowid FROM posts_fts WHERE posts_fts MATCH '"full text search"';

-- Prefix search
SELECT rowid FROM posts_fts WHERE posts_fts MATCH 'perf*';

-- Boolean operators
SELECT rowid FROM posts_fts WHERE posts_fts MATCH 'sqlite AND NOT nosql';
SELECT rowid FROM posts_fts WHERE posts_fts MATCH 'sqlite OR postgres';

-- BM25 relevance ranking (lower = more relevant)
SELECT rowid, rank FROM posts_fts WHERE posts_fts MATCH 'sqlite' ORDER BY rank;

-- Join with content table for full data
SELECT p.id, p.title, p.body, fts.rank
FROM posts_fts fts
JOIN posts p ON p.id = fts.rowid
WHERE posts_fts MATCH 'sqlite performance'
ORDER BY fts.rank
LIMIT 10;
```

## Snippets & Highlights

```sql
-- Snippet: surrounding text with highlighted match
SELECT snippet(posts_fts, 1, '<b>', '</b>', '...', 10) AS excerpt
FROM posts_fts
WHERE posts_fts MATCH 'sqlite';

-- Highlight: mark matches in a column
SELECT highlight(posts_fts, 0, '<mark>', '</mark>') AS title_hl
FROM posts_fts
WHERE posts_fts MATCH 'performance';
```

## Tokenizers

```sql
-- Default: unicode61 (handles Unicode, case-insensitive)
-- ASCII tokenizer (faster, ASCII only)
CREATE VIRTUAL TABLE docs_fts USING fts5(content, tokenize='ascii');

-- Porter stemmer (dog/dogs/dogged all match "dog")
CREATE VIRTUAL TABLE docs_fts USING fts5(content, tokenize='porter ascii');
```

## Standalone FTS (No Content Table)

```sql
-- Simpler: store data directly in FTS (no external content table)
CREATE VIRTUAL TABLE notes_fts USING fts5(title, body);
INSERT INTO notes_fts VALUES ('SQLite Tips', 'WAL mode improves concurrency');
SELECT * FROM notes_fts WHERE notes_fts MATCH 'concurrency';
```

## TypeScript Integration (Bun)

```typescript
import { Database } from 'bun:sqlite';

const db = new Database('app.db');

// Setup FTS
db.run(`CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(title, body)`);

// Insert
const insertFts = db.prepare('INSERT INTO docs_fts(rowid, title, body) VALUES (?, ?, ?)');

// Search with BM25 ranking
const search = db.prepare<{ rowid: number; title: string; rank: number }, [string]>(`
  SELECT rowid, title, rank
  FROM docs_fts
  WHERE docs_fts MATCH ?
  ORDER BY rank
  LIMIT 20
`);

const results = search.all('sqlite performance');
```

## Python Integration

```python
import sqlite3

conn = sqlite3.connect("app.db")
conn.row_factory = sqlite3.Row

# FTS5 is built into Python's sqlite3 module
conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(title, body)")

# Search
query = "sqlite performance"
rows = conn.execute(
    "SELECT rowid, title, rank FROM docs WHERE docs MATCH ? ORDER BY rank LIMIT 10",
    (query,)
).fetchall()

for row in rows:
    print(dict(row))
```

---

# sqlite-vec Vector Search

[sqlite-vec](https://github.com/asg017/sqlite-vec) is a lightweight SQLite extension for
vector similarity search. A drop-in alternative to pgvector for local/edge deployments.

## Installation

```bash
# Python
pip install sqlite-vec

# Node.js
npm install sqlite-vec

# Bun
bun add sqlite-vec
```

## Python Setup

```python
import sqlite3
import sqlite_vec
import struct
import numpy as np

conn = sqlite3.connect("vectors.db")
conn.enable_load_extension(True)
sqlite_vec.load(conn)
conn.enable_load_extension(False)

# Check version
print(conn.execute("SELECT vec_version()").fetchone()[0])

# Helper: convert list to sqlite-vec binary format
def serialize_vector(v: list[float]) -> bytes:
    return struct.pack(f"{len(v)}f", *v)

# Create vector table (1536 dims = OpenAI text-embedding-3-small)
conn.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS embeddings USING vec0(
        item_id INTEGER PRIMARY KEY,
        embedding FLOAT[1536]
    )
""")

# Insert vectors
vectors = [
    (1, [0.1, 0.2, ...]),  # (id, embedding)
    (2, [0.3, 0.1, ...]),
]
conn.executemany(
    "INSERT INTO embeddings VALUES (?, ?)",
    [(id_, serialize_vector(v)) for id_, v in vectors]
)
conn.commit()

# KNN search (k-nearest neighbors)
query_vector = serialize_vector([0.15, 0.25, ...])
rows = conn.execute("""
    SELECT item_id, distance
    FROM embeddings
    WHERE embedding MATCH ?
    ORDER BY distance
    LIMIT 5
""", (query_vector,)).fetchall()

for item_id, distance in rows:
    print(f"id={item_id}  distance={distance:.4f}")
```

## TypeScript/Bun Setup

```typescript
import { Database } from 'bun:sqlite';
import * as sqliteVec from 'sqlite-vec';

const db = new Database('vectors.db');
sqliteVec.load(db);

// Create vector table (384 dims = all-MiniLM-L6-v2)
db.run(`
  CREATE VIRTUAL TABLE IF NOT EXISTS embeddings USING vec0(
    id INTEGER PRIMARY KEY,
    embedding FLOAT[384]
  )
`);

// Helper
function toFloat32Array(v: number[]): Float32Array {
  return new Float32Array(v);
}

// Insert
const insert = db.prepare('INSERT INTO embeddings VALUES (?, ?)');
insert.run(1, toFloat32Array([0.1, 0.2, ...]));

// Search
const search = db.prepare<{ id: number; distance: number }, [Float32Array, number]>(`
  SELECT id, distance
  FROM embeddings
  WHERE embedding MATCH ?
  ORDER BY distance
  LIMIT ?
`);

const results = search.all(toFloat32Array(queryVector), 5);
```

## Full Pipeline: Embed + Store + Search

```python
import sqlite3
import sqlite_vec
import struct
import openai

openai_client = openai.OpenAI()

def embed(text: str) -> list[float]:
    resp = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return resp.data[0].embedding

def serialize(v: list[float]) -> bytes:
    return struct.pack(f"{len(v)}f", *v)

# Setup
conn = sqlite3.connect("knowledge.db")
conn.enable_load_extension(True)
sqlite_vec.load(conn)
conn.enable_load_extension(False)

conn.executescript("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        source TEXT,
        created_at INTEGER DEFAULT (unixepoch())
    );

    CREATE VIRTUAL TABLE IF NOT EXISTS doc_embeddings USING vec0(
        id INTEGER PRIMARY KEY,
        embedding FLOAT[1536]
    );
""")
conn.commit()

# Index a document
def index_document(content: str, source: str = "") -> int:
    vector = embed(content)
    cursor = conn.execute(
        "INSERT INTO documents (content, source) VALUES (?, ?) RETURNING id",
        (content, source)
    )
    doc_id = cursor.fetchone()[0]
    conn.execute(
        "INSERT INTO doc_embeddings VALUES (?, ?)",
        (doc_id, serialize(vector))
    )
    conn.commit()
    return doc_id

# Semantic search
def search(query: str, top_k: int = 5) -> list[dict]:
    q_vec = serialize(embed(query))
    rows = conn.execute("""
        SELECT d.id, d.content, d.source, e.distance
        FROM doc_embeddings e
        JOIN documents d ON d.id = e.id
        WHERE e.embedding MATCH ?
        ORDER BY e.distance
        LIMIT ?
    """, (q_vec, top_k)).fetchall()
    return [{"id": r[0], "content": r[1], "source": r[2], "score": r[3]} for r in rows]

# Example
index_document("SQLite WAL mode improves concurrency", "docs/sqlite.md")
results = search("how to improve database performance")
```

## Hybrid Search (FTS5 + sqlite-vec)

Combine keyword + semantic search for best results:

```python
def hybrid_search(query: str, top_k: int = 10) -> list[dict]:
    # 1. Semantic search
    semantic_hits = {
        r[0]: {"semantic_rank": i, "distance": r[1]}
        for i, r in enumerate(semantic_search(query, top_k * 2))
    }

    # 2. Keyword search (FTS5)
    keyword_hits = {
        r[0]: {"keyword_rank": i}
        for i, r in enumerate(conn.execute(
            "SELECT rowid, rank FROM docs_fts WHERE docs_fts MATCH ? ORDER BY rank LIMIT ?",
            (query, top_k * 2)
        ).fetchall())
    }

    # 3. Reciprocal Rank Fusion (RRF)
    k = 60  # RRF constant
    all_ids = set(semantic_hits) | set(keyword_hits)
    scores = {}
    for doc_id in all_ids:
        s = semantic_hits.get(doc_id, {}).get("semantic_rank")
        kw = keyword_hits.get(doc_id, {}).get("keyword_rank")
        scores[doc_id] = (
            (1 / (k + s) if s is not None else 0) +
            (1 / (k + kw) if kw is not None else 0)
        )

    top_ids = sorted(scores, key=lambda x: scores[x], reverse=True)[:top_k]
    # Fetch and return documents...
```

## Embedding Model Quick Reference

| Model | Dims | Quality | Cost |
|---|---|---|---|
| `text-embedding-3-small` (OpenAI) | 1536 | Good | Low |
| `text-embedding-3-large` (OpenAI) | 3072 | Best | Medium |
| `all-MiniLM-L6-v2` (local) | 384 | OK | Free |
| `nomic-embed-text` (Ollama) | 768 | Good | Free |
| Gemini `embedding-001` | 768 | Good | Low |
