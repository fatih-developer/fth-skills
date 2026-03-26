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
