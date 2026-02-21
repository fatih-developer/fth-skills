# Examples

Worked examples across all risk levels.

---

## Example 1 — File Deletion (HIGH)

```
CHECKPOINT [HIGH RISK]
================================
Action      : Delete /data/users.csv
Target      : /data/users.csv (2.3 MB, 15,420 rows)
Impact      : All user data permanently removed
Reversible? : No (no backup exists)
Alternative : Move to /archive/users_backup.csv instead
================================
Type "yes" to proceed, "no" to cancel.
```

---

## Example 2 — Production Deploy (HIGH)

```
CHECKPOINT [HIGH RISK]
================================
Action      : Deploy v2.4.1 to production
Target      : api.example.com (production)
Impact      : All users switch to new version, rollback takes ~5 minutes
Reversible? : Partially (rollback possible but risks downtime)
Alternative : Deploy to staging first and run smoke tests
================================
Type "yes" to proceed, "no" to cancel.
```

---

## Example 3 — Bulk DB Update (HIGH, escalated)

```
CHECKPOINT [HIGH RISK] -- Escalated from MEDIUM (bulk operation)
================================
Action      : UPDATE orders SET status = 'archived'
Target      : orders table — WHERE created_at < '2024-01-01'
Impact      : 12,847 records will be updated
Reversible? : No (no transaction log)
Alternative : Run SELECT first to review affected records
================================
Type "yes" to proceed, "no" to cancel.
```

---

## Example 4 — File Overwrite (MEDIUM)

```
CHECKPOINT [MEDIUM RISK]
Action : Overwrite config.json
Target : ./config.json
Impact : Current configuration will be replaced
Proceed? (yes/no)
```

---

## Example 5 — Test Deploy (MEDIUM)

```
CHECKPOINT [MEDIUM RISK]
Action : Deploy to staging environment
Target : staging.example.com
Impact : Current staging build will be replaced
Proceed? (yes/no)
```

---

## Example 6 — End-of-Task Audit Trail

```
CHECKPOINT AUDIT TRAIL
========================
Step 1  : Read project files          | LOW    | Passed silently
Step 3  : Overwrite config.json       | MEDIUM | Approved
Step 5  : Create backup.sql           | LOW    | Passed silently
Step 7  : Update 12,847 DB records    | HIGH   | Approved
Step 9  : Deploy to production        | HIGH   | Rejected → deployed to staging instead
========================
Total checkpoints: 5 (2 LOW, 1 MEDIUM, 2 HIGH)
High-risk actions: 1 approved, 1 rejected
```
