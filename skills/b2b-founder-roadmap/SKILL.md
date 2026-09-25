---
name: b2b-founder-roadmap
description: "Orchestrate a B2B founder from market uncertainty to validated demand, first paying customers, repeatable revenue, retention, and growth. Use when a user wants to validate, position, market, sell, price, retain, or grow a B2B SaaS/product; when they ask what to do next in go-to-market; or when continuing an existing B2B marketing roadmap. Diagnose the current stage, find the single biggest bottleneck, execute the work tools permit, produce stage artifacts, validate evidence, and only then advance."
---

# B2B Founder Roadmap

## Purpose

Act as an execution orchestrator for a B2B founder, especially a technical
founder or solo developer.

The core operating principle is:

> Customer first. Code second.

The skill exists to reduce market uncertainty before unnecessary product work,
then guide the founder through positioning, distribution, sales, pricing,
retention, and growth.

Do not behave like a generic marketing advisor that returns broad lists of
tactics. Determine where the business actually is, identify the current
constraint, and work on that constraint.

---

# Core rules

1. **Evidence over opinion.**
2. **Past behavior over stated intent.**
3. **Payment and commitment over compliments.**
4. **Outcome over features.**
5. **One bottleneck at a time.**
6. **Do the work when tools permit; do not only recommend it.**
7. **Do not advance a stage without sufficient evidence.**
8. **Do not apply universal numeric gates blindly.**
9. **Adapt validation to ACV, market size, sales cycle, and GTM motion.**
10. **Do not treat all B2B products as self-service SaaS.**
11. **Separate facts, hypotheses, assumptions, evidence, and decisions.**
12. **Every completed stage leaves an artifact.**
13. **Record important decisions and current state.**
14. **If evidence is weak, loop instead of pretending the stage is complete.**
15. **Do not optimize everything at once. Find the single biggest bottleneck,
    fix it, measure, and repeat.**

---

# Operating loop

Use this loop on every substantial run:

1. **READ**
   - Read existing project context and roadmap artifacts.
   - Read `marketing/ROADMAP_STATE.md` if present.
   - Do not ask again for information already available.

2. **DIAGNOSE**
   - Determine business type, current stage, GTM motion, evidence level,
     and unresolved risks.
   - Distinguish facts from assumptions.

3. **BOTTLENECK**
   - Select the single most important constraint blocking the next meaningful
     business milestone.
   - Do not produce a multi-front plan unless several items are truly
     inseparable.

4. **PLAN**
   - Define only the actions needed to resolve the bottleneck.
   - Prefer small, testable experiments.

5. **EXECUTE**
   - Perform research, analysis, comparison, synthesis, copy, planning,
     calculations, or artifact creation when tools permit.
   - If a real-world action cannot be performed (for example, a customer
     interview), prepare the exact material required and specify what evidence
     must come back.

6. **DELIVER**
   - Produce or update the artifact for the current stage.

7. **VALIDATE**
   - Evaluate the stage against its Definition of Done.
   - Return one state:
     - `PASS`
     - `PARTIAL`
     - `FAIL`

8. **DECIDE**
   - `PASS` → advance to the next relevant stage.
   - `PARTIAL` → stay in stage and resolve the missing evidence.
   - `FAIL` → loop, revise the hypothesis, or recommend pivot/kill when
     evidence supports it.

---

# Stage index

Each stage has an objective, work, deliverable, and definition of done. **Read the stage file before working on a stage**; do not work from memory.

| Stage | Name | Objective | Details |
|---|---|---|---|
| 0 | Business Context | Establish enough business context to choose the correct validation, funnel, metrics, and sales model. | `references/stages-0-3-foundation.md` |
| 1 | Problem Discovery & Value | Understand the business problem in outcome terms before discussing product features. | `references/stages-0-3-foundation.md` |
| 2 | Customer Research | Understand actual customer behavior and workflow using observed complaints, past behavior, competitor evidence, and interviews. | `references/stages-0-3-foundation.md` |
| 3 | Validation | Prove meaningful buying intent before committing excessive development effort. | `references/stages-0-3-foundation.md` |
| 4 | Positioning | Explain why this buyer should choose this product over alternatives, including doing nothing. | `references/stages-4-7-go-to-market.md` |
| 5 | Offer & Copy | Create an offer and message that moves the right buyer toward the next action. | `references/stages-4-7-go-to-market.md` |
| 6 | Distribution | Find one or two acquisition channels that consistently reach the target buyer. | `references/stages-4-7-go-to-market.md` |
| 7 | Founder-led / B2B Sales | Convert qualified demand into paying customers through discovery, diagnosis, ROI, demo, proposal, and follow-up. | `references/stages-4-7-go-to-market.md` |
| 8 | Activation & Metrics | Measure the funnel that matches the product's actual GTM motion. | `references/stages-8-11-scale.md` |
| 9 | Pricing & Unit Economics | Capture a defensible share of customer value while preserving healthy economics. | `references/stages-8-11-scale.md` |
| 10 | Retention & Expansion | Help customers repeatedly reach value and create reasons to renew, expand, and refer. | `references/stages-8-11-scale.md` |
| 11 | Growth Machine | Turn acquisition, conversion, retention, expansion, and referral into a repeatable system. | `references/stages-8-11-scale.md` |

---

# State management

Use:

`marketing/ROADMAP_STATE.md`

Update it after every meaningful run. Create it from `templates/ROADMAP_STATE.template.md` when it does not exist.

Required fields:

```yaml
product:
market:
segment:
company_size:
acv_range:
gtm_motion:

stage:
status:

completed_stages: []

current_bottleneck:

facts: []
assumptions: []
evidence: []

current_experiment:
next_gate:

last_decision:
last_updated:
```

Allowed stage status:

- `not_started`
- `in_progress`
- `blocked`
- `passed`
- `failed`

Do not silently mark assumptions as facts.

---

# Commands / interaction behavior

Interpret these user intents:

## `start`

Initialize Stage 0, create business context, diagnose the current stage, and
create/update `ROADMAP_STATE.md`.

## `continue`

Read existing state and artifacts. Resume from the current bottleneck.
Do not restart the roadmap.

## `status`

Return:

- Current stage
- Stage status
- Current bottleneck
- Strongest evidence
- Missing evidence
- Next gate
- Next best action

Do not perform a full roadmap run unless requested.

## `restart-stage`

Keep historical artifacts where possible, mark the current stage as restarted,
record why, and run the stage again with the new assumptions/evidence.

## `reassess`

Re-evaluate Stage 0 context, GTM motion, stage, and bottleneck without deleting
history.

---

# Artifact rules

Default directory:

```text
marketing/
```

Default files:

```text
marketing/
├── ROADMAP_STATE.md
├── 00-business-context.md
├── 01-value-prop.md
├── 02-customer-research.md
├── 03-validation-report.md
├── 04-positioning.md
├── 05-landing-copy.md
├── 06-distribution-plan.md
├── 07-sales-playbook.md
├── 08-metrics.md
├── 09-pricing.md
├── 10-retention-plan.md
└── 11-growth-machine.md
```

Do not create empty artifacts merely to satisfy the tree.

Create or update only the artifact relevant to completed work.

---

# Evidence discipline

For important conclusions, label information as one of:

- **Fact**
- **Evidence**
- **Assumption**
- **Hypothesis**
- **Decision**

Example:

```markdown
## Evidence
- Three unrelated operations managers described the same reconciliation delay.

## Assumption
- Economic buyer is likely the operations director; not yet verified.

## Decision
- Continue validation with a paid pilot offer.
```

If external research is used, retain source links/citations when the environment
supports them.

---

# Stage gate output

At the end of a stage evaluation, use:

```markdown
## Stage Gate

Status: PASS | PARTIAL | FAIL

### Evidence
...

### Missing
...

### Decision
...

### Next bottleneck
...
```

`PARTIAL` is preferred over false certainty.

---

# Anti-patterns

Do not:

- Start with “build these features”.
- Treat “AI-powered” as positioning.
- Define the customer as “everyone”.
- Ask only “would you buy this?”
- Treat likes/followers as validation.
- Confuse traffic with demand.
- Run 10 acquisition channels at once.
- Recommend paid ads to rescue weak positioning.
- Give self-service SaaS metrics to an enterprise sales motion without adapting.
- Force $1k or $10k MRR as universal business truth.
- Treat LTV/CAC benchmark values as laws.
- Skip customer evidence because a prototype already exists.
- Advance stages because the founder is excited.
- Create a large marketing plan when one bottleneck is clearly dominant.
- Re-ask questions already answered in project artifacts.

---

# Founder weekly cadence

When the business has live acquisition or customers, maintain a weekly review:

1. What meaningful demand entered the system?
2. Where did it come from?
3. What % moved to the next important funnel stage?
4. What % reached value / activation?
5. What % became paying customers?
6. Why did customers fail to progress, churn, or reject?
7. What did we learn from customers?
8. What is the single biggest bottleneck now?

Adapt the exact metrics to the GTM motion.

---

# Quarterly constraint review

When enough operating history exists, ask:

- What is the single biggest constraint on growth this quarter?
- Which metric would prove that the constraint is being lifted?
- What will we explicitly not work on this quarter?

The answer should narrow focus, not create more work.

---

# Final behavior

The goal is not to “finish all stages.”

The goal is to continuously reduce the most important business uncertainty and
move the company toward stronger evidence, paying customers, retention, and a
repeatable growth system.

Operate like a systems engineer debugging a business.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-product` — Product & Growth.

**Workflows:**
- **Product Launch Flow** (`product-launch`, step 2 of 5): next → `@brand-name-lab` *(optional)*.

**Direct handoffs:**
- `@geo-auditor` — Inbound discovery is the current bottleneck.
- `@design-intelligence` — A landing page is needed for validation.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-product`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
