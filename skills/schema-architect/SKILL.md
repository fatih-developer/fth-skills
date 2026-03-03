---
name: schema-architect
description: Veri modelini (Database Schema) iş gereksinimlerinden türetir. Normalizasyon seviyesi (1NF→3NF→BCNF) seçer, ilişkileri (One-to-Many vb.) tasarlar, anti-pattern'ları işaretler ve platforma özel (PostgreSQL, MySQL vb.) DDL üretir. Tasarım kararlarının gerekçesini belgeler.
---

# Schema Architect Protocol

This skill transforms raw business requirements into a robust, normalized, and scalable database schema. It avoids common anti-patterns like "God Tables" or EAV (Entity-Attribute-Value) abuse.

**Core assumption:** A good schema must be extensible, maintainable, and explicitly document your design choices. 

---

## 1. Requirement Analysis & Normalization Phase
Before writing any SQL, analyze the request:
- **Identify Entities & Relationships:** What are the root domains? (e.g. Users, Orders, Products). What are the cardinalities?
- **Normalization Strategy (1NF → 3NF → BCNF):** 
  - Ensure data is logically divided. 
  - Stop at 3NF for most OLTP systems. Denormalize ONLY if there is a documented performance optimization justification.

## 2. Anti-Pattern Check
Scan your intended design against common pitfalls:
- ❌ **God Table:** Does one table have >30 columns handling multiple disconnected responsibilities (e.g., `Users` having billing, shipping, and auth info in one huge table)? → Split them!
- ❌ **EAV (Entity-Attribute-Value) Abuse:** Are you using EAV patterns instead of JSONB or proper typed tables? → Rework to standard models where possible!
- ❌ **Polymorphic Associations:** Using `entity_id` and `entity_type` without Foreign Key constraints? → Use standard associative tables or exclusive arcs!

## 3. Dialect Selection & Output Generation
Identify the target database (agnostic approach). Generate platform-specific SQL schema.

**Required Outputs (Must write BOTH to `docs/database-report/`):**

1. **Human-Readable Markdown (`docs/database-report/schema-architect-report.md`)**
```markdown
### 🏗️ Schema Generation Report
- **Target Dialect:** [PostgreSQL/MySQL/Snowflake]
- **Normalization Level:** [e.g., 3NF]
- **Trade-offs made:** [Fast Read vs. Fast Write considerations]

#### 📜 Generated DDL
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```
```

2. **Machine-Readable JSON (`docs/database-report/schema-architect-output.json`)**
```json
{
  "skill": "schema-architect",
  "dialect": "PostgreSQL",
  "entities": ["users"],
  "relations": [],
  "raw_ddl": "CREATE TABLE..."
}
```

## 4. Execution Context
- **Default (Static):** Analyze based on provided requirements or existing schema files (e.g., `schema.prisma` or `.sql` files).
- **Dynamic (On-Demand):** Only connect to a live database to introspect the current schema if the user explicitly requests it.

---

## Guardrails
- **No Vague Types:** Do not use `VARCHAR` without limits unless using PostgreSQL `TEXT`. Use proper types (`JSONB`, `NUMERIC(p,s)`, `TIMESTAMPTZ` vs `TIMESTAMP`).
- **Primary Keys:** Default to `UUIDv7` or `BIGSERIAL/BIGINT IDENTITY` for primary keys for distributed readiness.
- **Audit Columns:** `created_at` and `updated_at` must exist on almost all operational operational tables.

---

## 🔗 Next Steps & Handoffs
If you are executing the **New Schema Design Flow** as defined in the Database ECOSYSTEM guide, and the schema has been successfully generated, the next mandatory skill in the sequence is:
- `@access-policy-designer` (to design Row-Level Security constraints or app-level access controls for the new tables)
