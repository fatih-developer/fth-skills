---
name: access-policy-designer
description: Row-level security (RLS), column-level masking ve role bazlı erişim politikalarını (RBAC/ABAC) tasarlar ve uygular. "Muhasebe sadece kendi departmanının verilerini görebilmeli" gibi iş kurallarını PostgreSQL RLS, MySQL view veya Snowflake politikalarına dönüştürür.
---

# Access Policy Designer Protocol

This skill enforces Zero Trust at the database layer. Instead of relying purely on the application backend to filter `WHERE tenant_id = ?`, it pushes security down to the database engine to prevent data leaks.

**Core assumption:** Application code has bugs. Database security policies (RLS/Views) are the final, unbreakable safety net against SQL Injection or logic flaws.

---

## 1. Requirement Translation
Convert business rules into technical access models.
*Business Rule:* "Doctors can only see their own patients' records."
*Translation:* We need Row-Level Security (RLS) on the `patients` table where `primary_doctor_id = current_user_id()`.

## 2. Policy Paradigms

### Row-Level Security (RLS) - PostgreSQL / Supabase
- Define policies for `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
- Distinguish between **Who you are** (Current Role/User) and **What you belong to** (Tenant/Organization ID).

### Column-Level Security (CLS)
- Restricting `SELECT` on specific columns.
- E.g., The `Customer Support` role can see the `users` table but cannot `SELECT ssn` or `salary`.

## 3. Output Generation

Generate platform-specific DDL for security policies.

**Required Outputs (Must write BOTH to `docs/database-report/`):**

1. **Human-Readable Markdown (`docs/database-report/access-policy-report.md`)**
```markdown
### 🔒 Security Design: Patient Records

**Business Rule:** Doctors only access their assigned patients.

**SQL Implementation (PostgreSQL RLS):**

```sql
-- 1. Enable RLS on the table
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;

-- 2. Create the SELECT policy
CREATE POLICY doctor_select_own_patients 
ON patients FOR SELECT 
TO qualified_doctors
USING (primary_doctor_id = current_setting('app.current_user_id')::uuid);

-- 3. Create the UPDATE policy (Must belong to them and remain assigned to them)
CREATE POLICY doctor_update_own_patients 
ON patients FOR UPDATE 
TO qualified_doctors
USING (primary_doctor_id = current_setting('app.current_user_id')::uuid)
WITH CHECK (primary_doctor_id = current_setting('app.current_user_id')::uuid);
```

### ⚠️ Security Checklist (Audit)
- [x] Does the policy account for "Superadmins" who need to see everything?
- [x] Is the `app.current_user_id` setting securely injected by the backend connection?
```

2. **Machine-Readable JSON (`docs/database-report/access-policy-output.json`)**
```json
{
  "skill": "access-policy-designer",
  "target_table": "patients",
  "dialect": "PostgreSQL",
  "policies": [
    {"name": "doctor_select_own_patients", "action": "SELECT", "role": "qualified_doctors"},
    {"name": "doctor_update_own_patients", "action": "UPDATE", "role": "qualified_doctors"}
  ],
  "rls_enabled": true
}
```

---

## Guardrails
- **Infinite Recursion:** If a policy on `users` queries the `users` table to check a role, it will infinite-loop. Restrict policy lookups or use a separate `user_roles` mapping table.
- **Performance Tax:** Complex RLS policies (e.g., `USING (EXISTS (SELECT 1 FROM ...))`) execute on *every row read*. Warn the user if a policy will cause a sequential scan.
- **Bypass Clauses:** Ensure the policy explicitly handles `BypassRLS` roles (like system migrations or background workers).
