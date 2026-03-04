---
name: data-masker
description: Masks production data for test and development environments (Data Masking). Detects PII (email, SSN, credit cards) and obfuscates them safely.
---

# Data Masker Protocol

This skill prevents sensitive production data (PII, PHI, financial records) from leaking into lower environments (staging, development, testing). It analyzes schemas and generates idempotent masking scripts.

**Core assumption:** Developers need realistic data to fix bugs, but giving them real user emails, passwords, or credit card numbers violates GDPR/KVKK and Zero Trust principles.

---

## 1. PII Detection (Static vs Dynamic)
- **Default (Static):** Analyze based on provided `.sql`, schema files, or DDL text.
- **Dynamic (On-Demand):** Only connect to a live database to sample data or infer column contents if explicitly requested by the user.
- When given a table structure, automatically flag high-risk columns:
  - 📛 **Direct Identifiers:** `email`, `ssn`, `tc_kimlik`, `phone`, `ip_address`, `mac_address`.
  - 💳 **Financial:** `credit_card`, `iban`, `balance`, `salary`.
  - 🩺 **Health/Personal:** `birth_date`, `blood_type`, `address`, `location_lat_lon`.

## 2. Masking Strategy Selection
Do not just overwrite everything with `'REDACTED'`. Choose the right mathematical mutation to keep the data realistic for QA testing:

### Strategy 1: Deterministic Substitution (Fake Data)
- **Best for:** Names, Emails.
- **Why:** To make the UI look normal. `john.doe@example.com` becomes `x8f9.mask@test.local`.

### Strategy 2: Partial Redaction
- **Best for:** Credit Cards, Phone Numbers.
- **Why:** `+1 (555) 123-4567` becomes `+1 (555) ***-**67`. Devs can still test formatting validations.

### Strategy 3: Variance / Shuffling (Jittering)
- **Best for:** Dates, Salaries.
- **Why:** `salary: 105,000` -> add +/- 20% random variance -> `91,200`. Keeps statistical distribution intact without revealing the exact amount.

### Strategy 4: Hashing / Nullification
- **Best for:** Passwords, API Tokens.
- **Why:** Replace all passwords with a known development hash (e.g., `password123`) so devs can log in as any test user without knowing the real user's password.

## 3. Output Generation

Provide an executable SQL script that can be run on a cloned staging database.

**Required Outputs (Must write BOTH to `docs/database-report/`):**

1. **Human-Readable Markdown (`docs/database-report/data-masking-report.md`)**
```markdown
### 🛡️ PII Discovery
- **Risk Level: HIGH** (Found emails, phones, and hashed passwords).

### 🛠️ Masking Execution Script (PostgreSQL)
```sql
-- Disable triggers temporarily to speed up the masking
ALTER TABLE users DISABLE TRIGGER ALL;

-- Masking `users` table
UPDATE users SET
  -- Strategy: Deterministic Substitution
  email = 'masked_' || id || '@sandbox.local',
  first_name = 'User_' || substring(md5(random()::text) from 1 for 6),
  last_name = 'Test',
  -- Strategy: Partial Redaction
  phone_number = concat(left(phone_number, 3), '***', right(phone_number, 2)),
  -- Strategy: Known Dev Value
  password_hash = '$2b$10$dev_password_hash_xyz';

-- Re-enable triggers
ALTER TABLE users ENABLE TRIGGER ALL;
```
```

2. **Machine-Readable JSON (`docs/database-report/data-masking-output.json`)**
```json
{
  "skill": "data-masker",
  "pii_found": ["email", "phone_number", "password_hash"],
  "masking_strategies_applied": {
    "email": "Deterministic Substitution",
    "phone_number": "Partial Redaction"
  },
  "sql_script_generated": "UPDATE users SET email = ..."
}
```

---

## Guardrails
- **Performance:** Bulk `UPDATE` on 10 million rows will overwhelm WAL logs. If the table is massive, suggest the `CREATE TABLE AS SELECT (CTAS)` strategy instead of `UPDATE`.
- **Referential Integrity:** If `email` is used as a Foreign Key (Anti-pattern, but it happens), masking it will break relationships. Detect FKs before masking.
- **Irreversibility:** Ensure the masking SQL uses one-way functions. Randomization seeds should not be deterministic.
