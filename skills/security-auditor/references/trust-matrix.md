# Trust Matrix

Full breakdown of permissions granted per Trust Tier.

## Scoring Guide

| Score Range | Trust Tier | Color |
|-------------|------------|-------|
| 80 - 100 | TRUSTED | 🟢 |
| 60 - 79 | NORMAL | 🟡 |
| 40 - 59 | RESTRICTED | 🟠 |
| 0 - 39 | QUARANTINED | 🔴 |

## Permission Matrix

| Permission | TRUSTED (80-100) | NORMAL (60-79) | RESTRICTED (40-59) | QUARANTINED (0-39) |
|------------|:---:|:---:|:---:|:---:|
| Read files (scoped dir) | ✅ | ✅ | ✅ | ❌ |
| Read system files (/etc, ~/.ssh) | ❌ | ❌ | ❌ | ❌ |
| Write files (temp dir) | ✅ | ✅ | ❌ | ❌ |
| Write files (project dir) | ✅ | ⚠️ Checkpoint | ❌ | ❌ |
| Write system files | ❌ | ❌ | ❌ | ❌ |
| Execute whitelisted commands | ✅ | ✅ | ⚠️ Checkpoint | ❌ |
| Execute dynamic commands | ⚠️ Checkpoint | ⚠️ Checkpoint | ❌ | ❌ |
| Outbound HTTP (whitelisted) | ✅ | ✅ | ⚠️ Checkpoint | ❌ |
| Outbound HTTP (non-whitelisted) | ⚠️ Checkpoint | ❌ | ❌ | ❌ |
| Trigger other skills | ✅ | ⚠️ Checkpoint | ❌ | ❌ |
| Process PII | ✅ | ⚠️ Checkpoint | ❌ | ❌ |
| Access env variables | ✅ | ⚠️ Scoped only | ❌ | ❌ |
| Spawn subprocesses | ⚠️ Checkpoint | ❌ | ❌ | ❌ |
| Delete files | ⚠️ Checkpoint | ⚠️ Checkpoint | ❌ | ❌ |

**Legend:** ✅ = Allowed | ⚠️ = Checkpoint (human confirmation required) | ❌ = Denied

## Score Modifiers Reference

| Factor | Modifier |
|--------|----------|
| Audit PASSED (all categories clean) | +10 |
| Test coverage exists | +10 |
| Version history documented | +10 |
| Open source & verifiable | +5 |
| Verified ecosystem author | +5 |
| Minimal permissions only | +5 |
| Sandbox compatible | +5 |
| Audit FAILED (critical risk) | -10 |
| Uses eval/exec | -10 |
| Network + disk-write combined | -10 |
| Unknown / closed-source author | -5 |
| Broad filesystem access | -5 |
| Privilege-escalating chain | -5 |
| Zero test coverage | -5 |
| Contains blacklisted commands | -20 |
| Confirmed malicious command | -30 (floor: 0) |

---

## Extended Catalog

The detailed entries below were merged from the former `skill-security` skill. They use the same tiers as the summary above; when an entry appears in both, the stricter tier wins.

### Complete Authorization Map

Defines which operations are allowed, which require checkpoints, and which are forbidden for each confidence tier.

---

### TRUSTED (80-100)

```
FILESYSTEM
  ✓  Read          : free within defined scope
  ✓  Write         : free within defined scope
  ⚠️  Delete        : checkpoint (irreversible)
  ✓  Execute       : whitelisted commands only
  🚫 System dirs   : /etc /sys /proc — forbidden

NETWORK
  ✓  HTTPS GET     : whitelisted domains
  ✓  HTTPS POST    : whitelisted domains
  ✓  WebSocket     : whitelisted domains
  ⚠️  New domain    : approval on first use
  🚫 HTTP (clear)  : forbidden
  🚫 Raw socket    : forbidden

EXECUTION
  ✓  Bash (allowed): safe commands only
  ✓  Python/Node   : inside sandbox
  ⚠️  New process   : checkpoint
  🚫 eval/exec     : forbidden
  🚫 System service: forbidden

SKILL CHAIN
  ✓  Can trigger 60+ trust skills
  ⚠️  40-59 trust   : checkpoint
  🚫 0-39 trust    : cannot trigger

DATA
  ✓  Read user data
  ✓  Write to output
  ⚠️  Process PII   : masking mandatory
  🚫 3rd party PII : forbidden (no sharing)
```

---

### NORMAL (60-79)

```
FILESYSTEM
  ✓  Read          : working directory + tmp
  ⚠️  Write         : /tmp and project output dir only
  ⚠️  Delete        : checkpoint + rollback plan needed
  🚫 Execute       : strictly forbidden

NETWORK
  ✓  HTTPS GET     : safe domains only
  ⚠️  HTTPS POST    : checkpoint on payload logic
  🚫 WebSocket     : forbidden
  🚫 HTTP (clear)  : forbidden
  🚫 Raw socket    : forbidden

EXECUTION
  ✓  Python/Node   : strictly inside sandbox, no network
  🚫 Bash          : forbidden
  🚫 eval/exec     : forbidden

SKILL CHAIN
  ✓  Can trigger 80+ trust skills
  ⚠️  60-79 trust   : checkpoint
  🚫 0-59 trust    : cannot trigger

DATA
  ✓  Read non-sensitive data
  ⚠️  Write         : draft outputs only
  🚫 PII           : forbidden to read or touch
```

---

### SUSPICIOUS (0-59)

All operations are forbidden except requesting review from the user via the orchestrator.
