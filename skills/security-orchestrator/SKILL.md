---
name: security-orchestrator
description: Orchestrates the Security Ecosystem by running skill-security and adaptive-guard in the correct order. Manages audit phases, trust scoring, guard activation, incident response, and calibration. Trigger on "security orchestrator", "run security", "audit and guard", or "security workflow".
---

# Security Ecosystem Orchestrator

Execute the two skills of the Security Ecosystem in the correct order, with the correct context.
Detect the user's security needs, and decide which skill will be activated and when.

**Core rule:** Security is always enabled. `adaptive-guard` can never be fully disabled — only its sensitivity can be adjusted.

---

## Orchestrator Decision Tree

```text
What is the trigger?
│
├── "I wrote a new skill / is it safe?"
│   └── PHASE 1 → PHASE 2 → PHASE 3
│
├── "Scan the Ecosystem"
│   └── PHASE 1 (all skills) → PHASE 2 → PHASE 3
│
├── "The skill will run in production"
│   └── PHASE 1 → PHASE 2 → PHASE 3 → PHASE 4 (activate guard)
│
├── Attack detection (from adaptive-guard)
│   └── PHASE 5 (incident response)
│
├── "Guard is too slow / blocks too often"
│   └── PHASE 6 (guard calibration)
│
└── Periodic check
    └── PHASE 7 (health report)
```

---

## PHASE 1 — Discovery (First Step in Every Scenario)

### Step 1.1 — Scope Detection

```text
Ask (or extract from context):
□ Is it a single skill or the ecosystem being scanned?
□ Goal: audit / trust / guard setup / all?
□ Environment: dev / staging / production?
□ Is there an active attack? (is it urgent?)
```

### Step 1.2 — Urgency Check

```text
ACTIVE ATTACK?     → Skip to PHASE 5 (urgent response)
PROD DEPLOYMENT?   → Full flow (PHASES 1-4)
GENERAL CHECK?     → Fast flow (PHASES 1-3)
```

---

## PHASE 2 — Run skill-security

### Step 2.1 — Audit

**skill-security MODE 1 (Audit):**
```text
For the target skill(s):
1. Load SKILL.md
2. Scan the 7 threat categories
3. Extract concrete findings for each category
4. Generate security-report.md
```

**Expected time:** 2-5 minutes / skill

**Evaluate results:**
```text
🔴 CRITICAL FINDING EXISTS →
  "This skill cannot be deployed. Pending fixes."
  Send the user the list of necessary fixes
  Do not move to PHASE 3 — fix first

🟡 MODERATE RISK EXISTS →
  "Appropriate for limited use. Suggested fixes."
  Proceed to PHASE 3

🟢 CLEAN →
  Proceed to PHASE 3
```

### Step 2.2 — Trust Scoring

**skill-security MODE 3 (Trust):**
```text
1. Fetch Audit results
2. Calculate Trust score (0-100)
3. Set trust level
4. Build permission map
5. Generate trust-score.md
```

**Pass Trust result to adaptive-guard:**
```python
trust_context = {
    "skill_name": "...",
    "trust_score": N,
    "trust_level": "TRUSTED|NORMAL|RESTRICTED|QUARANTINED",
    "permitted_actions": [...],
    "denied_actions": [...],
    "requires_checkpoint": [...]
}
```

---

## PHASE 3 — Generate Guard Rules

**skill-security MODE 2 (Guard):**

Construct the guard rule profile based on the Trust score:
```text
RESTRICTED or QUARANTINED (0-59):
  → K4 Human approval mandatory for every execution
  → K1 threshold lowered (tighter scanning)
  → All external API calls blocked

NORMAL (60-79):
  → K3 LLM judge active for suspicious cases
  → Whitelisted APIs permitted
  → File write requires checkpoint

TRUSTED (80-100):
  → Standard K0-K2 sufficient
  → K3 only on anomalies
  → Human approval only for critical actions
```

---

## PHASE 4 — Activate adaptive-guard

**Production environments only:**

### Step 4.1 — Guard Configuration

```python
adaptive_guard_config = {
    "skill": skill_name,
    "trust_score": N,
    "fail_policy": "fail-open|fail-closed",  # Pick based on trust
    "k2_active": true|false,              # Does ML infra exist?
    "k4_timeout": 1800,                   # 30 minutes
    "learning_active": true,
    "cache_ttl": 86400,                   # 24 hours
    "anomaly_multiplier": 5
}
```

### Step 4.2 — Establish Baseline

On initial production deployment:
```text
"Normal interaction baseline being established for adaptive-guard
on this skill. Monitoring mode active for the first 48 hours
(logging without blocking). Full protection follows thereafter."
```

### Step 4.3 — Activation Confirmation

```text
📋 Guard Activation Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Skill         : [name]
Trust Score   : [N]/100 → [level]
Fail Policy   : [fail-open|fail-closed]
K2 ML Filter  : [active|disabled]
Learning Mode : active
Monitoring    : 48 hours (then full protection)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Proceed with activation?
```

---

## PHASE 5 — Incident Response (Urgent)

**Trigger:** Active attack detected or adaptive-guard critical violation report.

```text
STEP 1 — Isolate immediately
  → Suspend attacker's session
  → Temporarily disable the associated skill

STEP 2 — Analyze
  skill-security → Re-audit the impacted skill
  adaptive-guard → Extract incident-report.md details

STEP 3 — Rule update
  → Detect attack class
  → Manually trigger learning engine
  → Append new rule (automatic if confidence >0.60)

STEP 4 — Report
  To the user:
  ┌─────────────────────────────────────────┐
  │ 🚨 Security Incident Detected          │
  │                                         │
  │ Type     : [attack class]               │
  │ Time     : [timestamp]                  │
  │ Skill    : [impacted skill]             │
  │ Action   : [what occurred]              │
  │ New Rule : [learned rule pattern]       │
  └─────────────────────────────────────────┘

STEP 5 — De-isolate / Re-open
  If patched → reactivate skill
  If unpatched → keep quarantined
```

---

## PHASE 6 — Guard Calibration

**Trigger:** "Too many false alarms" or "Running too slow"

### High False Alarms (False Positive >1%)

```text
1. Inspect the last 100 blocks
2. Identify unjustified blocks
3. Loosen or drop the exact K1 rule responsible
4. Add to Whitelist (if necessary)
5. Monitor for 24 hours, recalculate rates
```

### High Latency (>100ms average)

```text
K0 cache hit rate < 60% → Increase Cache TTL
K2 traffic > 20%        → Strengthen K1 rules (send fewer to K2)
K3 traffic > 5%         → Fine-tune the K2 model
```

---

## PHASE 7 — Periodic Health Report

**Trigger:** Weekly automated snapshot or "give me a security report"

```markdown
# Weekly Security Ecosystem Report

## Ecosystem Health: 🟢 / 🟡 / 🔴

### skill-security
Last Audit      : [date]
Scanned         : N skills
Critical finding: N
Pending fixes   : N

### adaptive-guard
Total messages  : N
Blocked         : N (X%)
False positive  : N (X%)
Rules learned   : N
Average latency : Xms

### Highlight of the Week
- [key event 1]
- [key event 2]

### Recommended Actions
1. [high priority step]
2. [...]
```

---

## Orchestrator Rules of Operation

```text
1. adaptive-guard is never fully turned off
   → Only sensitivities (K1/K2/K3) can be manually bypassed

2. If skill-security audit FAILED
   → Skill cannot go to production
   → Enforced strictly by Orchestrator

3. If Trust score < 40
   → Orchestrator clearly alerts the user
   → Asks: "This skill is quarantined, still want to use it?"

4. The Guard displays every learned rule
   → Principle: "No implicit rule is applied without notification"

5. Incident sequence: isolate → analyze → learn → report → re-open
   → Steps cannot be skipped

6. Every orchestrator decision is logged
   → Appended to security-audit-trail.log
   → Traceability of exactly who/what made the decision
```
