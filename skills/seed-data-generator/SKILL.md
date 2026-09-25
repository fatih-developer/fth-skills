---
name: seed-data-generator
description: "Generate realistic seed and test data that respects foreign keys and constraints, inserted in topological order, as SQL or ORM scripts. Use when the user needs development or test data, demo fixtures, or to populate a new schema."
---

# Seed Data Generator Protocol

This skill helps developers populate empty local or staging databases with massive amounts of realistic data for load testing and UI development.

**Core assumption:** Simple random strings (`asdfgh`) are useless for UI testing. Seed data must look real and respect Foreign Key constraints to successfully insert.

---

## 0. Context Intake

Before designing, make sure you have the inputs below. Read the previous workflow step's artifact first if it exists. Ask only for what is missing, in a single message, and state any assumption you make instead of blocking.

- Schema or `schema-architect-output.json` with foreign keys and constraints.
- Row counts per table and any realistic distributions needed.
- Output format (SQL, ORM seed script, CSV) and locale for fake data.

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

**Outputs.** In *file mode* — the user wants artifacts, or this skill runs as a step of an ecosystem workflow — write both files below to `docs/database-report/`. In *inline mode* — a quick question — answer in the chat and end with the JSON below as a *Handoff* block instead of creating files.

1. **Human-Readable Markdown (`docs/database-report/seed-data-report.md`)**
````markdown
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
````

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

## When to Skip

- The user needs one or two literal rows for a quick test; write them directly.

## Guardrails
- **Performance:** For requesting >10,000 rows, do not output literal SQL `INSERT` statements. Instead, output a Python/Node script using `faker` and fast bulk `COPY` commands.
- **Unique Constraints:** Be extremely careful with random generators hitting duplicate values on `UNIQUE` columns. Append `id` or sequence numbers to emails/usernames if necessary.
- **Environment:** Warn the user to NEVER run seed scripts in production.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-database` — Database Domain.

**Workflows:**
- **New Schema Design Flow** (`db-new-schema`, step 4 of 4): last step → once it passes, complete the workflow and report the outcome.

**Handoff contract:** pass results to the next skill through `docs/database-report/seed-data-output.json` with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-database`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
