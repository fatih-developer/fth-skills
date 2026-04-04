# Python SQLite Reference

## Table of Contents
1. [Sync: sqlite3 (stdlib)](#sync-sqlite3-stdlib)
2. [Async: aiosqlite](#async-aiosqlite)
3. [FastAPI Integration](#fastapi-integration)
4. [Connection Pooling Pattern](#connection-pooling-pattern)
5. [Data Classes & Type Safety](#data-classes--type-safety)
6. [Migration with raw SQL](#migration-with-raw-sql)

---

## Sync: sqlite3 (stdlib)

```python
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path("app.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Access columns by name: row["email"]
    _apply_pragmas(conn)
    return conn

def _apply_pragmas(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = NORMAL;
        PRAGMA foreign_keys = ON;
        PRAGMA cache_size = -64000;
        PRAGMA temp_store = MEMORY;
        PRAGMA mmap_size = 268435456;
    """)

@contextmanager
def db_conn():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# Usage
with db_conn() as conn:
    rows = conn.execute("SELECT * FROM users WHERE is_active = 1").fetchall()
    for row in rows:
        print(row["email"])
```

### Bulk Insert (Executemany)

```python
users = [("ali@x.com", "Ali"), ("veli@x.com", "Veli")]
with db_conn() as conn:
    conn.executemany(
        "INSERT INTO users (email, name) VALUES (?, ?)",
        users
    )
```

### Named Parameters

```python
with db_conn() as conn:
    conn.execute(
        "UPDATE users SET name = :name WHERE id = :id",
        {"name": "Fatih", "id": 42}
    )
```

---

## Async: aiosqlite

```bash
pip install aiosqlite
```

```python
import aiosqlite
from pathlib import Path

DB_PATH = Path("app.db")

async def get_db() -> aiosqlite.Connection:
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    await db.executescript("""
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = NORMAL;
        PRAGMA foreign_keys = ON;
        PRAGMA cache_size = -64000;
        PRAGMA temp_store = MEMORY;
    """)
    return db

# Context manager pattern
from contextlib import asynccontextmanager

@asynccontextmanager
async def db_context():
    db = await get_db()
    try:
        yield db
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()

# Usage
async def get_users():
    async with db_context() as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
    return [dict(row) for row in rows]
```

---

## FastAPI Integration

### Dependency Injection Pattern

```python
# app/db.py
import aiosqlite
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import AsyncGenerator

DB_PATH = "app.db"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: run migrations
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
            PRAGMA journal_mode = WAL;
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                created_at INTEGER NOT NULL DEFAULT (unixepoch())
            );
        """)
        await db.commit()
    yield
    # Shutdown: nothing needed for SQLite

app = FastAPI(lifespan=lifespan)

async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("PRAGMA foreign_keys = ON")
        await db.execute("PRAGMA journal_mode = WAL")
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise

# Router
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    name: str

@router.get("/users")
async def list_users(db: aiosqlite.Connection = Depends(get_db)):
    async with db.execute("SELECT id, email, name FROM users") as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]

@router.post("/users", status_code=201)
async def create_user(payload: UserCreate, db: aiosqlite.Connection = Depends(get_db)):
    async with db.execute(
        "INSERT INTO users (email, name) VALUES (?, ?) RETURNING id",
        (payload.email, payload.name)
    ) as cur:
        row = await cur.fetchone()
    return {"id": row[0], **payload.model_dump()}

app.include_router(router, prefix="/api")
```

---

## Connection Pooling Pattern

SQLite doesn't need a real pool (one writer, many readers). A simple singleton works:

```python
import sqlite3
import threading

_local = threading.local()

def get_thread_conn() -> sqlite3.Connection:
    """One connection per thread — safe for multi-threaded servers."""
    if not hasattr(_local, "conn"):
        _local.conn = sqlite3.connect("app.db", check_same_thread=False)
        _local.conn.row_factory = sqlite3.Row
        _local.conn.execute("PRAGMA journal_mode = WAL")
        _local.conn.execute("PRAGMA foreign_keys = ON")
    return _local.conn
```

For asyncio, use a single shared aiosqlite connection (it serializes internally):

```python
import aiosqlite
import asyncio

_db: aiosqlite.Connection | None = None
_lock = asyncio.Lock()

async def get_shared_db() -> aiosqlite.Connection:
    global _db
    async with _lock:
        if _db is None:
            _db = await aiosqlite.connect("app.db")
            _db.row_factory = aiosqlite.Row
            await _db.execute("PRAGMA journal_mode = WAL")
            await _db.execute("PRAGMA foreign_keys = ON")
    return _db
```

---

## Data Classes & Type Safety

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: int  # unix timestamp

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "User":
        return cls(**dict(row))

    @property
    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created_at)

# Usage
with db_conn() as conn:
    row = conn.execute("SELECT * FROM users WHERE id = ?", (1,)).fetchone()
    user = User.from_row(row)
    print(user.created_datetime)
```

---

## Migration with raw SQL

```python
# app/migrations.py
import sqlite3
from pathlib import Path

MIGRATIONS_DIR = Path("migrations")

def run_migrations(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            applied_at INTEGER NOT NULL DEFAULT (unixepoch())
        )
    """)
    conn.commit()

    applied = {row[0] for row in conn.execute("SELECT name FROM _migrations")}
    pending = sorted(
        f for f in MIGRATIONS_DIR.glob("*.sql")
        if f.name not in applied
    )

    for migration_file in pending:
        print(f"Applying {migration_file.name}...")
        conn.executescript(migration_file.read_text())
        conn.execute("INSERT INTO _migrations (name) VALUES (?)", (migration_file.name,))
        conn.commit()
        print(f"  ✓ {migration_file.name}")

# Run at startup
if __name__ == "__main__":
    conn = get_connection()
    run_migrations(conn)
    conn.close()
```
