# Risk Classification Matrix

Complete risk classification for common agent actions.

---

## Default Risk Levels

| Action Type | Default Risk | Escalation Condition |
|---|---|---|
| File deletion | HIGH | — |
| File overwrite | MEDIUM | Production file → HIGH |
| New file creation | LOW | — |
| DB INSERT | MEDIUM | Bulk (50+) → HIGH |
| DB UPDATE / DELETE | HIGH | — |
| GET request | LOW | — |
| POST / PUT / DELETE API | MEDIUM | Payment / auth endpoint → HIGH |
| Payment / transfer | HIGH | — |
| Test/staging deploy | MEDIUM | — |
| Production deploy | HIGH | — |
| Secret / credential usage | HIGH | — |
| Git push (non-main) | LOW | — |
| Git push (main/prod) | MEDIUM | Force push → HIGH |
| Git tag / release | MEDIUM | Production release → HIGH |
| Environment variable change | MEDIUM | Production env → HIGH |
| Package install / update | LOW | Major version bump → MEDIUM |
| Schema migration | HIGH | — |

---

## Escalation Triggers

When any of these conditions apply, bump the risk level **one step up**:

| Trigger | Example |
|---------|---------|
| **Bulk operation** | Affecting 50+ records, files, or resources |
| **Production environment** | Target tagged `prod`, `production`, `live`, `main` |
| **No rollback path** | No backup exists, no soft-delete, no transaction log |
| **Sensitive data** | PII, payment info, credentials, API keys |
| **Chain reaction** | Action triggers downstream critical operations |
| **Cross-service impact** | Affects multiple services or systems simultaneously |
| **Time-sensitive** | Action cannot be undone after a short window (DNS, certificates) |

---

## Risk Decision Flowchart

```
Is the action destructive or irreversible?
├── Yes → HIGH RISK
└── No
    ├── Does it modify existing state?
    │   ├── Yes → MEDIUM RISK
    │   │   └── Any escalation trigger? → HIGH RISK
    │   └── No → LOW RISK
    └── Is it read-only?
        └── Yes → LOW RISK
```
