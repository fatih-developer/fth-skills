---
name: output-critic
description: Evaluate every produced output (code, report, plan, data, API response) against type-specific quality criteria, score 1-10, make accept/reject decisions, and provide actionable improvement suggestions. Triggers on 'evaluate', 'check', 'review', 'quality control', 'is this good enough', 'score it', or before passing output to the next step in an agentic workflow.
---

# Output Critic Protocol

Evaluate the output by type, score each criterion, make an accept/reject decision, and suggest concrete improvements. Goal: prevent weak output from reaching the next step.

---

## Workflow

```
1. Detect output type
2. Apply type-specific criteria
3. Score each criterion
4. Calculate overall score
5. Make accept / conditional / reject decision
6. Suggest improvements
```

---

## Acceptance Threshold

| Overall Score | Decision | Action |
|---|---|---|
| 8-10 | ACCEPT | Proceed |
| 6-7 | CONDITIONAL | Apply minor fixes, then proceed |
| 0-5 | REJECT | Apply improvements, re-evaluate |

---

## Type-Specific Criteria

### Code

| Criterion | Weight | Question |
|-----------|--------|----------|
| Correctness | 30% | Produces expected output? Handles edge cases? |
| Readability | 20% | Meaningful names? Clean indentation? |
| Security | 20% | SQL injection? Hardcoded secrets? Unsafe input? |
| Performance | 15% | Unnecessary loops? N+1 queries? Memory leaks? |
| Testability | 15% | Functions independently testable? |

### Report / Written Content

| Criterion | Weight | Question |
|-----------|--------|----------|
| Accuracy | 30% | Claims supported? Misleading statements? |
| Coverage | 25% | All requested topics addressed? Missing sections? |
| Clarity | 20% | Target audience can understand? Jargon explained? |
| Structure | 15% | Logical flow? Consistent headings? |
| Actionability | 10% | Reader knows what to do next? |

### Plan / Task List

| Criterion | Weight | Question |
|-----------|--------|----------|
| Completeness | 30% | All necessary steps present? Critical step missing? |
| Atomicity | 25% | Each step does one thing? Overly broad steps? |
| Dependency accuracy | 20% | Order makes sense? Circular dependencies? |
| Verifiability | 15% | Each step has clear "done" criteria? |
| Realism | 10% | Steps are achievable? Overly optimistic estimates? |

### Data / Table

| Criterion | Weight | Question |
|-----------|--------|----------|
| Accuracy | 35% | Numbers consistent? Calculations correct? |
| Completeness | 25% | Missing rows/columns? Nulls explained? |
| Format consistency | 20% | Units, date formats, currency consistent? |
| Readability | 20% | Meaningful headers? Proper sorting? |

---

## Output Format

```
OUTPUT CRITIC
Type     : [output type]
Decision : ACCEPT / CONDITIONAL / REJECT
Score    : [X/10]

## Criterion Scores

| Criterion | Score | Note |
|-----------|-------|------|
| [Criterion 1] | X/10 | [short note] |
| [Criterion 2] | X/10 | [short note] |
| **Overall** | **X/10** | |

## Strengths
- [What was done well — specific]

## Weaknesses
- [What is missing / wrong — specific]

## Improvement Suggestions
1. [Concrete action — what to do, where]
2. [Concrete action]

## Next Step
[Accept -> proceed | Conditional -> fix X | Reject -> apply suggestions, resubmit]
```

---

## Re-Evaluation

When improved output is resubmitted:

```
RE-EVALUATION
Previous score: X/10
New score     : Y/10
Change        : +N points
Improved      : [which criteria]
Still open    : [remaining issues if any]
```

---

## When to Skip

- User said "quick and dirty, doesn't need to be perfect"
- Prototype / draft stage (user explicitly stated)
- Single-line simple output

---

## Guardrails

- **Never accept security issues** — hardcoded secrets = automatic REJECT regardless of other scores.
- **Be specific in suggestions** — "improve code" is useless; "move API key to env var at line 12" is actionable.
- **Cross-skill**: works with `task-decomposer` (validates plan quality), `output-critic` is the quality gate before task completion.

## References

- `references/EXAMPLES.md` — scored critiques of code, reports, plans, and data outputs. Read it when the expected output format or level of detail is unclear.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-orchestration` — Agent Orchestration.

**Workflows:**
- **Complex Task Execution Flow** (`orch-complex-task`, step 5 of 6): next → `@agent-reviewer` *(optional)*.
- **Decision Quality Flow** (`reason-decision`, step 5 of 5, via `@ecosystem-reasoning`): last step → summarize the workflow outcome.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-orchestration`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
