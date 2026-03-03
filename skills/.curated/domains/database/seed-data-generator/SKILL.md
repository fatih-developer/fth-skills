---
name: seed-data-generator
description: Gerçekçi, ilişkisel bütünlüğü (Referential Integrity) koruyan test verisi üretir. Şemayı okur, foreign key zincirlerini çözer, doğru insert sırasını bulur ve sütun adına göre Faker pattern'larını otomatik uygular (email kolonu → fake email).
---

# Seed Data Generator Protocol

This skill helps developers populate empty local or staging databases with massive amounts of realistic data for load testing and UI development.

**Core assumption:** Simple random strings (`asdfgh`) are useless for UI testing. Seed data must look real and respect Foreign Key constraints to successfully insert.

---

## 1. Schema Analysis & Topological Sort
Before generating data, read the schema and understand the relationships:
- If `orders` depends on `users` and `products`.
- If `order_items` depends on `orders` and `products`.
- **Topological Sort (Insert Order):** `users` -> `products` -> `orders` -> `order_items`.

*(Never try to insert an order item before the order exists).*

## 2. Smart Field Generation (Faking)
Map column names and data types to specific Faker generators:
- `email` -> Faker.Internet.Email()
- `first_name`, `last_name`, `full_name` -> Faker.Person.FullName()
- `status` (VARCHAR) -> Random pick from `('active', 'pending', 'cancelled')`.
- `description`, `bio` -> Faker.Lorem.Paragraph()
- `created_at` -> Random Timestamp between `NOW() - 1 year` and `NOW()`.

## 3. Output Generation

Provide an executable seeder script (TypeScript/Prisma, Python, or raw SQL depending on the user's stack). Raw SQL is the default.

**Required Outputs (Must write BOTH to `docs/database-report/`):**

1. **Human-Readable Markdown (`docs/database-report/seed-data-report.md`)**
```markdown
### 🔗 Dependency Graph Resolution
Insert Order:
1. `companies`
2. `users` (Depends on `companies`)
3. `posts` (Depends on `users`)

### 🛠️ Seed Script (Raw SQL)
```sql
-- Disable triggers temporarily for fast bulk inserts
SET session_replication_role = 'replica';

-- 1. Insert Companies
INSERT INTO companies (id, name, created_at) VALUES 
('c1', 'Acme Corp', '2023-01-15 10:00:00'),
('c2', 'Globex', '2023-02-20 11:30:00');

-- 2. Insert Users
INSERT INTO users (id, company_id, email, first_name) VALUES 
('u1', 'c1', 'john.acme@example.com', 'John'),
('u2', 'c2', 'sarah.globex@example.com', 'Sarah');

-- Re-enable triggers
SET session_replication_role = 'origin';
```
```

2. **Machine-Readable JSON (`docs/database-report/seed-data-output.json`)**
```json
{
  "skill": "seed-data-generator",
  "insertion_order": ["companies", "users", "posts"],
  "faker_mappings": {
    "users.email": "Faker.Internet.Email()",
    "companies.name": "Faker.Company.CompanyName()"
  },
  "rows_generated": {
    "companies": 2,
    "users": 2
  }
}
```

---

## Guardrails
- **Performance:** For requesting >10,000 rows, do not output literal SQL `INSERT` statements. Instead, output a Python/Node script using `faker` and fast bulk `COPY` commands.
- **Unique Constraints:** Be extremely careful with random generators hitting duplicate values on `UNIQUE` columns. Append `id` or sequence numbers to emails/usernames if necessary.
- **Environment:** Warn the user to NEVER run seed scripts in production.
