---
name: security-auditor
description: Audits skills or the entire ecosystem for security vulnerabilities, enforces runtime guard rules, and assigns trust scores. Three modes: Audit (static analysis), Guard (runtime protection), Trust (permission mapping). Trigger on "skill security", "audit skill", "is this skill safe", "skill trust score", or "ecosystem security scan".
---


# Skill Security — Meta-Skill

The foundational security layer of the Skill ecosystem. It operates across three independent but interlocking modes. Decide which mode to run based on the context—or adhere to the user's explicit instructions.

**Execution Decision Matrix:**
- "I wrote a new skill, is it safe?" → Audit + Trust
- "This skill will be deployed to production" → Audit + Trust + Synthesize Guard rules
- "Scan the Ecosystem" → Audit + Trust on all skills
- Suspicious runtime behavior → Guard mode intervention

---

## MODE 1 — AUDIT (Static Analysis)

Diagnose security flaws by deeply parsing a `SKILL.md` file. Assess risks exclusively through the skill's instructions without executing code.

### Audit Steps

**Step A1 — Read the Skill**
```text
- Load the entire SKILL.md content
- Extract Frontmatter: name, description, outputs, requires
- Body: analyze count of bash/code lines, tool usage
- Detect targets: external URLs, APIs, file system nodes
```

**Step A2 — Scan the 7 Threat Categories**

Sequentially evaluate each category and quote the evidence if findings exist.

---

#### THREAT 1 — Prompt Injection
Does the skill indiscriminately append user input directly into an LLM prompt?

**Risky patterns:**
```python
# Direct injection of user input
"Analyze this: {user_input}"        ← High Risk
"The user said: {message}"          ← High Risk

# Dynamic system prompts
system_prompt = f"Act like {user_role}"  ← Medium Risk

# Secure patterns
"Analyze the following data:" + sanitized_data  ← Low Risk
```

**Detection Questions:**
- Does the skill pass raw user input to an LLM without isolation delimiters?
- Is there protection against instructions like "forget everything above"?

**Scoring:** No risk +2, minor risk -1, critical risk -3

---

#### THREAT 2 — Excessive Privileges (Least Privilege Violation)
Is the skill requesting permissions broader than absolutely necessary for its functional scope?

**Checklist:**
```text
□ Demanding write access when only read is needed?
□ Accessing the entire file system instead of a scoped directory?
□ Requesting full API keys for a single endpoint?
□ Employing persistent storage for highly ephemeral data?
□ Requesting permissions without an immediate user scenario?
□ Attempting to execute outside the designated Sandbox?
```

**Red Flags (DEFINITE REJECTION):**
```bash
# Excessive privilege examples
rm -rf /                     # STRICT REJECT
find / -type f               # Entire system scan — REJECT
curl ... | bash              # Remote Code Execution (RCE) — STRICT REJECT
chmod 777                    # Open to all — REJECT
sudo ...                     # Privilege escalation — STRICT REJECT
cat /etc/passwd              # System file access — REJECT
env | grep -i key            # Full environment dump — REJECT
```

**Scoring:** Clean +2, excessive privilege -2, critical privilege escalation -5

---

#### THREAT 3 — Sensitive Data Leakage
Does the skill handle API keys, passwords, tokens, or PII insecurely?

**Detection:**
```bash
# Potential leakage patterns
echo $API_KEY                      # Console dump — REJECT
log("User token: " + token)        # Log dump — REJECT
COPY .env /app/.env                # Embedding in container — REJECT
git add .env                       # Hardcoded commit — STRICT REJECT
curl ... -H "Key: hardcoded_key"   # Hardcoded secret — REJECT

# Secure handling
process.env.API_KEY                # Read from env — OK
vault.get("api_key")               # Secret manager — OK
os.getenv("SECRET")                # Env variable — OK
```

**PII Detection:**
- Does the skill process usernames, emails, phones, or IP addresses?
- Is the data encrypted at rest?
- Do GDPR/KVKK compliance procedures apply?
- Is the data transmitted to untrusted 3rd parties?

**Scoring:** Clean +2, processes PII securely 0, generic leakage risk -3, confirmed leakage -5

---

#### THREAT 4 — Malicious Commands
Does the skill contain highly destructive or easily exploitable commands?

**Blacklist (STRICT REJECT):**
```bash
rm -rf          # Mass deletion
dd if=/dev/zero # Disk wipe
:(){ :|:& };:   # Fork bomb payload
mkfs            # Disk format
> /dev/sda      # Disk overwrite
wget|curl ... | bash  # Untrusted RCE
nc -e /bin/sh   # Reverse shell
chmod 777 /     # System-wide permission mod
chown -R root   # Ownership hijack
iptables -F     # Firewall flush
```

**High Risk:**
```bash
kill -9 -1         # Kill all processes
find / -delete     # Unbounded deletion
truncate -s 0      # Unbounded truncation
mv /* /dev/null    # Unbounded move
```

**Dynamic Command Risks:**
```python
# User inputs merged directly into execution
cmd = f"ls {user_input}"    # REJECT — ls; rm -rf /
os.system(user_path)        # REJECT
eval(user_code)             # STRICT REJECT
exec(user_input)            # STRICT REJECT
```

**Scoring:** Clean +2, dynamic command risk -2, blacklisted command -5, STRICT REJECT → Instant Audit Fail

---

#### THREAT 5 — Skill Chain Security
If a skill forms an invocation chain, is the entire sequence secure?

**Analyze:**
```text
□ Which skills are invoked? (requires, calls, triggers)
□ Are invoked skills trusted? (do they have a trust score?)
□ Is there privilege escalation within the chain? (Low-privilege → High-privilege)
□ Is there an infinite loop risk? (A→B→C→A)
□ Depth of the chain? (>3 depth = warning, >5 depth = reject)
□ Is a skill's output blindly piped into a system command?
```

**Chain Security Matrix:**
```text
Chain Depth      Risk
1-2 levels     → Low
3 levels       → Medium (Monitor)
4 levels       → High (Audit thoroughly)
5+ levels      → Critical (Manual approval only)

Privilege Flow   Risk
Horizontal     → Low
Downward       → Low
Upward         → High (Warning + Checkpoint)
```

**Scoring:** No chain or secure chain +1, medium risk 0, privilege escalation -3, looping -4

---

#### THREAT 6 — External API Call Audit
If the skill accesses remote servers, are these connections verified?

**Checklist:**
```text
□ Endpoint URLs (Is there a whitelist?)
□ Is HTTPS enforced over HTTP?
□ Is SSL cert validation strictly enabled?
□ Are Timeouts defined? (No timeout → DoS risk)
□ Are Rate limits applied?
□ Is the API response schema-validated before processing?
□ Does a failed call dump sensitive request headers?
□ Is the 3rd party host trusted?
```

**Red Flags:**
```python
# SSL verification disabled — REJECT
requests.get(url, verify=False)

# Timeout omitted — RISKY
requests.get(url)  # missing timeout flag

# HTTP usage (unencrypted) — REJECT
curl http://...

# Response piped to eval — STRICT REJECT
eval(response.text)
```

**Scoring:** Clean HTTPS+timeout+validation +2, generic HTTP -2, SSL off -3, eval response -5

---

#### THREAT 7 — User Data Processing Rules
Are robust data handling rules enforced when intaking user data?

**Checklist:**
```text
□ Input validation? (type, length, format)
□ Input sanitization?
□ Adherence to Data Minimization principles?
□ Data retention lifecycle defined?
□ Data purge / export mechanisms provided?
□ Encryption at rest active?
□ Cross-user data bleed risks? (multi-tenant environments)
```

**Scoring:** Clean +2, missing validation -1, unprotected PII -3, cross-user risk -5

---

### Audit Report Artifact → `security-report.md`

```markdown
# Skill Security Audit Report

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

---

## MODE 2 — GUARD (Runtime Shield)

Applying security strictures at real-time execution. Acts across two paradigms:

### Use Case A — Generate Guard Protocols
Synthesize constraint parameters before an execution even starts:

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

### Use Case B — Real-Time Interception
Intercept execution immediately preceding an instruction trigger:

```text
Pre-Execution Checks:
1. Is it on the blacklist? → STRICT REJECT, block
2. Does it contain dynamic input? → Sanitize or reject
3. Is it within permitted scopes? → Proceed
4. Does it hit a checkpoint? → Await human prompt

Post-Execution Checks:
1. Does output contain secrets (API keys)? → Mask
2. Unexpected side-effects? → Trace and log
3. Resource exhaustion? → Issue warning
```

### Violation Log Artifact → `runtime-violations.md`

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

---

## MODE 3 — TRUST SCORER

Calculate an empirical Trust score (0-100) per skill. This dictates authorization limits system-wide.

### Trust Score Calculation

```text
BASE SCORE: 50

MULTIPLIERS (+):
  +10  Audit PASSED cleanly
  +10  Test coverage exists
  +10  Transparent version history
  +5   Open-source (traceable)
  +5   Verified core ecosystem actor
  +5   Least Privilege architecture
  +5   Full Sandbox compatibility

DETRACTORS (-):
  -10  Audit FAILED (critical risks)
  -10  Executes unverified code blocks (eval/exec)
  -10  Couples network + disk-write permissions
  -5   Closed-source / unknown author
  -5   Broad filesystem access
  -5   Privilege-escalating invocation chains
  -5   Zero test coverage
  -20  Contains blacklisted baseline targets
  -30  Malicious payload confirmed → Score plummets to 0.
```

### Trust Tiers & Authorization Map

```text
SCORE 80-100 → TRUSTED
  ✅ All execution types
  ✅ Advanced disk read/write
  ✅ Advanced networking
  ✅ Chain invocations allowed
  ✅ Approved for PII

SCORE 60-79 → NORMAL
  ✅ Disk read
  ✅ Restrictive disk write (temp zones only)
  ✅ Whitelisted APIs only
  ⚠️ Checkpoints triggered on critical boundaries
  ❌ Zero system-folder access

SCORE 40-59 → RESTRICTED
  ✅ Read-only execution
  ✅ Extreme API whitelisting
  ❌ No disk writes
  ❌ Prohibited from triggering chains
  ⚠️ K4 Human Approval mandated per execution

SCORE 0-39 → QUARANTINED
  ❌ No executions
  ❌ Network disabled
  ❌ Disk disconnected
  ⚠️ Under manual triage
  🔴 Banned from production
```

### Trust Report Artifact → `trust-score.md`

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

---

## ECOSYSTEM SCAN MODE

Macro-audit across the entire application ecosystem:

```bash
# Locate all recognized skills
find . -name "SKILL.md" -not -path "*/node_modules/*"
```

For every located SKILL.md:
1. Fire Audit mode
2. Calculate Trust Score
3. Map Chain Dependencies

### Ecosystem Health Summary Artifact

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

---

## DECISION TREE — Selecting Modes

```text
User Intent Analysis:
│
├── "I just authored this skill" / "Is it safe?"
│   → Run Audit + Trust
│
├── "Moving this skill into Production"
│   → Run Audit + Trust + Synthesize Guard Protocols
│
├── "Scan the entire Ecosystem"
│   → Run Ecosystem Scan Mode
│
├── Suspicious execution/runtime anomaly detected
│   → Run Guard Mode (Real-time intercept)
│
└── Inquiry: "What's the trust score?"
    → Run Trust Scorer exclusively
```

---

## RULES OF OPERATION

```text
1. Never execute a skill prior to a static Audit
2. If Trust Score < 40, explicitly ask the user "Do you wish to abort?"
3. If blacklisted command detected → FREEZE, report anomaly immediately
4. When uncertain → Default to restriction ("fail-closed")
5. Deliver unvarnished reports — Do not mitigate or be "polite" about bad security
6. Make all decisions traceable and append them to an un-erasable log
```

---

## WHEN TO BYPASS

- The skill is purely conversational text generation, zero file handling, zero execution → Audit is enough, Guard/Trust can be skipped.
- The user declares "bypass security checks" → Issue a warning, attain affirmative consent, and log.
- Local Sandbox / Test environment → Use abbreviated/lightweight Audit.

---

## REFERENCE FILES

For granular guidelines, consult:
- `references/command-blacklist.md` — Exhaustive execution blacklist
- `references/pii-patterns.md` — Pattern matchers for sensitive data
- `references/api-whitelist.md` — Allowed domain/endpoint scopes
- `references/trust-matrix.md` — Detailed breakdown of Trust vs Permissions
