---
name: assumption-checker
description: Before starting a task or taking a critical step, surface and verify the assumptions the agent is making. Checks 4 types - technical (libraries, APIs), data (files, formats), business logic (rules, scope), and user intent (what the user actually wants). Triggers on ambiguous requests, multi-step tasks, or whenever 'are you sure', 'check first', 'don't assume' appears.
---

# Assumption Checker Protocol

Before acting, stop and surface the assumptions you are making. Verify what you can, ask about what you cannot. Goal: catch wrong assumptions before building on them.

**Core principle:** Catching a wrong assumption now is far cheaper than discovering it 10 minutes later.

---

## When to Activate

### At Task Start
Run an assumption scan on every new task. Especially when:
- Task is ambiguous or missing information
- Phrasing is open to interpretation ("update", "fix", "clean up")
- Task involves irreversible actions
- External dependencies exist (API, files, database)

### Before Critical Steps
Re-scan during execution when:
- Previous step output was unexpected
- A new dependency emerged
- User changed direction

---

## 4 Assumption Types

### Technical Assumptions
Beliefs about environment, tools, and infrastructure.
- "Is this library installed?" → verifiable, check it
- "Is this API accessible?" → verifiable, test it
- "Does this work on this OS?" → platform-dependent

### Data Assumptions
Beliefs about files, formats, and data structures.
- "Does this file exist?" → verifiable, check it
- "Does this CSV have headers?" → verifiable, inspect it
- "All rows are in the same format" → verify with sample

### Business Logic Assumptions
Beliefs about rules, scope, and requirements.
- "Delete means soft delete" → ambiguous, ask
- "All users are affected" → scope unclear, ask
- "Date format is DD/MM/YYYY" → needs confirmation

### User Intent Assumptions
Beliefs about what the user actually wants.
- "Refactor = don't change behavior" → ask
- "Quick = not production quality" → ask
- "Update = keep existing, add new" → ask
- "Clean up = delete? archive? organize?" → ambiguous, ask

---

## Confidence Levels

Assign a confidence level to each assumption:

| Level | Meaning | Action |
|-------|---------|--------|
| VERIFIED | Checked and confirmed | Proceed |
| VERIFIABLE | Can be checked with a tool/command | Check now |
| UNCERTAIN | Cannot be verified, open to interpretation | Ask the user |
| RISKY | If wrong, causes significant damage | Must ask |

---

## Output Format

### Task Start Scan

```
ASSUMPTION CHECK — Task Start
Assumptions found: N
Verified: N | Checking: N | Need to ask: N

## Technical
| Assumption | Confidence | Action |
|------------|------------|--------|
| [assumption] | VERIFIED/VERIFIABLE/UNCERTAIN/RISKY | [action] |

## Data
| Assumption | Confidence | Action |
|------------|------------|--------|
| [assumption] | ... | [action] |

## Business Logic
| Assumption | Confidence | Action |
|------------|------------|--------|
| [assumption] | ... | [action] |

## User Intent
| Assumption | Confidence | Action |
|------------|------------|--------|
| [assumption] | ... | [action] |

[Verifiable assumptions being checked now...]
[Questions for uncertain/risky assumptions:]

? [Question 1]
? [Question 2]
```

### Pre-Step Scan (lighter format)

```
ASSUMPTION CHECK — Before [step name]
New assumptions: N found

| Assumption | Type | Confidence | Action |
|------------|------|------------|--------|
| [assumption] | Technical/Data/Logic/Intent | ... | ... |

[Questions or "All assumptions verified, proceeding."]
```

---

## Verification Protocol

Check verifiable assumptions with tools before asking the user:
- File exists? → check filesystem
- Library installed? → check import
- JSON field present? → inspect data
- API reachable? → test endpoint

Update the assumption table: VERIFIABLE → VERIFIED or RISKY

---

## Question Rules

- **Ask at most 3 questions at a time** — don't overwhelm the user
- **Ask riskiest first** — RISKY > UNCERTAIN
- **Use yes/no or multiple choice** — not open-ended
- Do not start the related step until answers arrive

---

## When to Skip

- Task is single-step, clear, and easily reversible
- User said "just do it, make your own assumptions"
- All assumptions were already verified in previous steps
- Repeated task — same structure worked before

---

## Guardrails

- Never skip assumption checking for irreversible actions, regardless of task simplicity.
- Keep scans concise — table format, not paragraphs.
- Verify before asking — don't ask the user things you can check yourself.
- Cross-skill: works with `checkpoint-guardian` (risk gates) and `task-decomposer` (plan validation).

## Coexistence with Other Gates

Clarification gates follow one precedence (see `@ecosystem-reasoning`): 1. `@project-focus-first` → 2. `@ask-first-act-later` → 3. `@assumption-checker` → 4. `@plan-hardener`. Run at most one gate per request — the first whose condition holds — and skip any gate whose questions were already answered in this conversation. `@checkpoint-guardian` is separate: it always applies before irreversible actions.

You are gate 3. If gate 1 or 2 already ran for this request, do not ask new questions: list the remaining assumptions with their confidence and ask at most one question, only for a high-risk unverified assumption.

## References

- `references/EXAMPLES.md` — worked assumption scans for ambiguous requests such as "clean up the database". Read it when the expected output format or level of detail is unclear.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-reasoning` — Reasoning, Planning Gates & Prompting.

**Workflows:**
- **Clarification Gate Flow** (`reason-clarify`, step 3 of 3): last step → summarize the workflow outcome.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-reasoning`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
