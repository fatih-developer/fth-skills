# Security Auditor — Report Templates

> Loaded on demand by `security-auditor`. Use the template for the mode you are running.

## Audit Report

```markdown
# Security Auditor Audit Report

**Skill:** [name]
**Version:** [version]
**Date:** [date]
**Auditor:** security-auditor v1.0

## Overall Assessment

| Status | Description |
|--------|-------------|
| 🟢 PASSED | All critical checks are clean |
| 🟡 CONDITIONAL | Medium/Low risks spotted, fix before PROD |
| 🔴 FAILED | Critical vulnerability detected, DO NOT DEPLOY |

**Result: [STATUS]**

## Threat Scorecard

| Category | Score | Status | Summary |
|----------|-------|--------|---------|
| Prompt Injection| [+/-N] | [🟢/🟡/🔴] | [summary] |
| Over Privileged| [+/-N] | [🟢/🟡/🔴] | [summary] |
| Sensitive Data| [+/-N] | [🟢/🟡/🔴] | [summary] |
| Malicious Cmd | [+/-N] | [🟢/🟡/🔴] | [summary] |
| Chain Security| [+/-N] | [🟢/🟡/🔴] | [summary] |
| API Audit     | [+/-N] | [🟢/🟡/🔴] | [summary] |
| Data Rules    | [+/-N] | [🟢/🟡/🔴] | [summary] |
| **TOTAL**     | [N/14] | | |

> Thresholds: 10+ → Pass | 6-9 → Conditional | <5 → Fail

## Critical Findings 🔴

### [Finding Title]
- **Threat:** [category]
- **Location:** SKILL.md, Line [N]
- **Evidence:** `[snippet]`
- **Risk:** [concrete exploit scenario]
- **Remediation:** [step-by-step fix]

## Moderate Findings 🟡
[Same format]

## Minor Findings 🟢
[Same format]

## Verified Secure Practices ✅
[What was done right]

## Remediation Priority Queue
1. [Most critical — mandatory]
2. [...]
```

## Guard Protocols

```markdown
# [skill-name] Guard Protocols

## Permitted (Whitelist)
- Read: [defined scopes]
- Write: [defined scopes]
- Network: [allowed domains]
- Commands: [whitelisted binaries]

## Denied (Blacklist)
- Read denied: /etc, /sys, /proc, ~/.ssh
- Write denied: system routes, .env
- Banned commands: [command-blacklist.md]
- Banned domains: [non-whitelisted zones]

## Checkpoints (Human-in-the-loop)
- File deletion: mandatory approval
- Ext API: first-use approval
- Spawning subprocesses: approval
- High data egress (>10MB): approval

## Violation Policy
- Warn: [low risk] → continue, log
- Halt: [high risk] → interrupt, notify user
- Abort: [critical] → freeze environment, trigger incident response
```

## Runtime Violations Ledger

```markdown
# Runtime Violations Ledger

**Skill:** [name]
**Session:** [timestamp]

## Violations

| Time | Threat | Command/Action | Decision | Result |
|------|--------|----------------|----------|--------|
| [T] | Malicious Cmd | `rm -rf /tmp/x` | 🔴 ABORTED | User Notified |
| [T] | Sensitive Data| Dumped API_KEY  | 🟡 MASKED  | Returned as `***` |

## Halt Explanations
[Detailed rationale for every interrupted event]
```

## Trust Score Report

```markdown
# Skill Trust Score Report

**Skill:** [name]
**Trust Score:** [N]/100
**Level:** [TRUSTED / NORMAL / RESTRICTED / QUARANTINED]
**Date:** [date]

## Calculation Breakdown

| Parameter | Points | Note |
|-----------|--------|------|
| Audit result    | [+/-N] | [pass/fail] |
| Test coverage   | [+/-N] | [exists/missing] |
| Permission scope| [+/-N] | [minimal/broad] |
| Author trusted  | [+/-N] | [known/unknown] |
| ... | | |
| **TOTAL** | **[N]/100** | |

## Granted Authorities

✅ Permitted:
- [permissions]

❌ Denied:
- [permissions]

⚠️ Checkpoints:
- [checkpoints]

## Trust Improvement Path
To boost the trust score:
1. [concrete step — +N points]
2. [...]
```

## Ecosystem Security Summary

```markdown
# Ecosystem Security Summary

| Skill | Audit | Trust | Tier | Critical Risks |
|-------|-------|-------|------|----------------|
| schema-architect | 🟢 | 85 | TRUSTED | — |
| data-masker | 🟢 | 78 | NORMAL  | — |
| query-budget-enforcer| 🟡 | 62 | NORMAL  | Missing timeouts |
| ... | | | | |

## Global Ecosystem Health: [N]/100

## Top 3 Riskiest Skills
1. [skill] — [reason]
2. ...

## Chain Security Topology
[Mapping of execution paths and bottleneck risks]

## Recommended Actions
[Top-down remediation priorities]
```
