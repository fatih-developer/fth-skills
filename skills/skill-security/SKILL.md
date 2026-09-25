---
name: skill-security
description: "Deprecated alias that routes to security-auditor. Use only when the user explicitly invokes $skill-security; for skill audits, trust scores, or runtime guard rules prefer security-auditor, which now holds the merged command blacklist, PII patterns, trust matrix, and API whitelist."
---

# Skill Security (Alias)

This skill has been merged into `security-auditor`. Both skills defined the same three modes (Audit, Guard, Trust) with diverging reference files, which produced inconsistent verdicts. The references now live in one place: `security-auditor/references/`.

## What to do

1. If `security-auditor` is installed, invoke it and follow its instructions. Mode mapping is one-to-one:

   | skill-security mode | security-auditor mode |
   |---|---|
   | Audit (static analysis) | MODE 1 — AUDIT |
   | Guard (runtime protection) | MODE 2 — GUARD |
   | Trust Scorer (0-100) | MODE 3 — TRUST |

2. If it is not installed, suggest the install command and do not run it without the user's approval:

   ```bash
   npx skills add fatih-developer/fth-skills --skill security-auditor
   ```

3. If the user declines, perform a minimal audit yourself: flag destructive shell commands (`rm -rf /`, `mkfs`, `dd` to devices, `curl … | bash`, reverse shells, `sudo` escalation), unsanitized user input passed to `eval`/`exec`/`subprocess`, secrets or PII written to logs, plain-HTTP or non-allowlisted network calls, and any write outside the skill's declared scope. Report PASS / CONDITIONAL / FAIL with the evidence line for each finding.

## Guardrails

- Never execute a newly created or modified skill before an audit.
- Any Tier 1 — STRICT REJECT command drops the trust score to 0 and stops execution.

## 🔗 Next Steps & Handoffs

- Canonical skill: `@security-auditor`
- Full lifecycle (audit → guard → incident response): `@security-orchestrator`
