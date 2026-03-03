# Examples

## Example 1 — "Clean up the database"

```
ASSUMPTION CHECK — Task Start
Assumptions found: 5
Verified: 1 | Checking: 2 | Need to ask: 2

## Technical
| Assumption | Confidence | Action |
|------------|------------|--------|
| DB connection is active | VERIFIABLE | Testing connection now |

## Data
| Assumption | Confidence | Action |
|------------|------------|--------|
| Backup exists | VERIFIABLE | Checking backup table |
| Target table is "logs" | UNCERTAIN | Ask |

## Business Logic
| Assumption | Confidence | Action |
|------------|------------|--------|
| "Clean" = hard delete (not soft) | RISKY | Must ask |
| "Old" = older than 30 days | UNCERTAIN | Ask |

[Verification results...]
VERIFIED: DB connection is active
RISKY: No backup found!

? [RISKY] Does "clean up" mean permanent deletion, or archiving?
? [RISKY] No backup found — proceed without backup?
? [UNCERTAIN] Which table should I clean — "logs"?
```

---

## Example 2 — "Process this CSV and generate a report"

```
ASSUMPTION CHECK — Task Start
Assumptions found: 4
Verified: 3 | Checking: 0 | Need to ask: 1

## Data
| Assumption | Confidence | Action |
|------------|------------|--------|
| data.csv exists | VERIFIED | Checked |
| Has header row | VERIFIED | First row inspected |
| UTF-8 encoding | VERIFIED | Confirmed |
| Date format is DD/MM/YYYY | UNCERTAIN | Ask |

? [UNCERTAIN] What format are dates in the CSV — DD/MM/YYYY or YYYY-MM-DD?
```
