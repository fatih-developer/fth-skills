---
name: b2b-founder-roadmap
description: 'Orchestrate a B2B founder from market uncertainty to validated demand, first paying customers, repeatable revenue, retention, and growth. Use when a user wants to validate, position, market, sell, price, retain, or grow a B2B SaaS/product; when they ask what to do next in go-to-market; or when continuing an existing B2B marketing roadmap. Diagnose the current stage, find the single biggest bottleneck, execute the work tools permit, produce stage artifacts, validate evidence, and only then advance.'
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

# Stage 0 — Business Context

## Objective

Establish enough business context to choose the correct validation, funnel,
metrics, and sales model.

## Determine

- Product / idea
- B2B status
- Target customer / ICP
- Company size: SMB / Mid-market / Enterprise
- Buyer, user, and economic buyer if different
- Current workflow and alternative
- Expected price / ACV range
- Sales cycle estimate if known
- Product state: idea / prototype / MVP / live
- Existing customers
- Existing users / waitlist / traffic
- Existing revenue / MRR / ARR if any
- GTM motion:
  - Product-led
  - Founder-led
  - Sales-led
  - Hybrid
- Main acquisition channels already tested
- Current strongest evidence
- Current biggest uncertainty

## Deliverable

`marketing/00-business-context.md`

## Definition of Done

Enough context exists to avoid using the wrong B2B playbook.

If the GTM motion is unclear, infer the most likely motion from ACV, buyer,
complexity, onboarding requirements, and current stage; mark the inference as
an assumption.

---

# Stage 1 — Problem Discovery & Value

## Objective

Understand the business problem in outcome terms before discussing product
features.

## Work

Answer:

1. Who is the customer?
2. What is their biggest problem?
3. How do they solve it today?
4. What is wrong with the current solution?
5. How much time, money, risk, or opportunity does the problem cost?
6. What is the economic value of fixing it?
7. Why should the buyer trust this product or founder?
8. What happens if they do nothing?

Translate:

`Feature → Benefit → Business Outcome`

Classify pain:

- Low
- Medium
- High

Prioritize medium/high pain with urgency.

## Deliverable

`marketing/01-value-prop.md`

Include:

- 8-question value proposition
- Feature → Benefit → Outcome table
- Pain score
- Urgency
- Initial ROI/value estimate
- Assumptions needing validation

## Definition of Done

The founder can explain the value without referring to the technology stack.

---

# Stage 2 — Customer Research

## Objective

Understand actual customer behavior and workflow using observed complaints,
past behavior, competitor evidence, and interviews.

## Research sources

Use relevant sources such as:

- Reddit
- LinkedIn
- Industry forums
- Discord / Slack communities
- YouTube comments
- GitHub issues
- App marketplace reviews
- G2 / Capterra / industry directories
- Competitor reviews
- Customer interviews

Do not treat source counts as universal laws. Use enough evidence to identify
clear recurring patterns.

## Methods

- ICP definition
- Workflow mapping
- Frustration-point mapping
- Five Whys
- Complaint clustering
- Competitor review mining
- Mom Test style questions
- Past-behavior evidence

Never ask interviewees only:
“Would you buy this?”

Prefer questions such as:

- When did this last happen?
- What did you do?
- What did it cost?
- What tool did you use?
- Have you paid to solve it?
- Who approved that purchase?
- What happened when you did nothing?

## Deliverable

`marketing/02-customer-research.md`

Include:

- ICP
- Workflow map
- Repeated complaints
- Competitor evidence
- Interview evidence
- Ranked pains
- Evidence strength
- Unresolved hypotheses

## Definition of Done

The customer, top pain, current alternative, and at least several independent
pieces of evidence are clear enough to design a validation test.

---

# Stage 3 — Validation

## Objective

Prove meaningful buying intent before committing excessive development effort.

## Evidence ladder

Treat evidence approximately as:

1. Problem acknowledged
2. Problem occurs repeatedly
3. Buyer actively searches for a solution
4. Buyer already spends money/time/resources on the problem
5. Buyer requests a demo/pilot
6. Buyer commits internal resources
7. LOI / pre-order / paid pilot
8. Payment

Higher levels outweigh large volumes of weak signals.

## Adaptive validation

Do not use one fixed gate for every B2B product.

### Example: low-ACV / self-service

Possible signals:

- Relevant traffic
- Waitlist / signup conversion
- Activation intent
- Trial starts
- Pre-orders
- Payments

### Example: high-ACV / enterprise

Possible signals:

- Qualified interviews
- Confirmed budget/problem owner
- Serious pilot discussions
- Internal champion
- LOI
- Paid pilot
- Procurement movement

## Validation methods

Choose the smallest credible test:

- Fake door landing page
- Waitlist
- Smoke test
- Pre-order
- Paid early access
- Concierge MVP
- Wizard of Oz MVP
- Discovery calls
- Pilot
- LOI

## Deliverable

`marketing/03-validation-report.md`

Include:

- Hypothesis
- Test
- Audience
- Evidence collected
- Quantitative results
- Qualitative results
- Evidence level
- Decision:
  - continue
  - iterate
  - pivot
  - kill

## Definition of Done

There is sufficient buying evidence for the product's ACV, market, and GTM
motion to justify the next investment.

Do not mark `PASS` merely because people say the idea is good.

---

# Stage 4 — Positioning

## Objective

Explain why this buyer should choose this product over alternatives, including
doing nothing.

## Formula

For [customer], who struggles with [problem],
our product helps them achieve [result],
unlike [alternative].

## Work

- Current alternatives
- Feature → Result → Desired outcome
- Known category / category anchor
- Transformation vs incremental improvement
- 5-second clarity test
- Three positioning variants

## Deliverable

`marketing/04-positioning.md`

Include:

- One-sentence positioning
- Homepage headline
- Category line
- Alternatives
- Feature → Benefit → Outcome table
- 5-second test criteria

## Definition of Done

A relevant stranger can quickly identify:

- what this is,
- who it is for,
- what outcome it creates,
- why it is preferable to the current alternative.

---

# Stage 5 — Offer & Copy

## Objective

Create an offer and message that moves the right buyer toward the next action.

## Copy principles

- Clarity beats cleverness.
- Outcome before technology.
- Design for scanning.
- Use concrete CTAs.
- Handle objections before they are voiced.

## Structure

- Headline
- Subheadline
- Primary CTA
- Key benefits
- How it works
- Proof
- Objections / FAQ
- Final CTA

Use frameworks when helpful:

- Hook → Agitate → Solution → Proof → CTA
- AIDA

## Deliverable

`marketing/05-landing-copy.md`

## Definition of Done

The page communicates the buyer, outcome, credibility, and next action without
requiring a long explanation.

---

# Stage 6 — Distribution

## Objective

Find one or two acquisition channels that consistently reach the target buyer.

## Channel families

### Owned
- Website
- SEO
- Newsletter
- YouTube
- LinkedIn content
- Tools/templates

### Earned
- Communities
- Referrals
- Reviews
- Podcasts
- Partnerships
- Integrations
- Guest content

### Paid
- Google Ads
- LinkedIn Ads
- Meta Ads
- Reddit Ads
- Sponsorships

## Bullseye scoring

Score candidate channels on:

- Audience presence
- Intent
- Cost
- Speed to signal
- Scale

Start with 1–2 channels.

Do not test many channels at once.

## Deliverable

`marketing/06-distribution-plan.md`

Include:

- Channel inventory
- Scoring
- Primary channel
- Secondary channel
- Experiment hypothesis
- Duration
- Success metric
- Kill / keep criteria

## Definition of Done

At least one channel shows measurable progress toward qualified conversations,
signups, trials, pilots, or revenue appropriate to the GTM motion.

---

# Stage 7 — Founder-led / B2B Sales

## Objective

Convert qualified demand into paying customers through discovery, diagnosis,
ROI, demo, proposal, and follow-up.

## Sales principles

- First conversation is usually discovery, not demo.
- Understand before explaining.
- Start demo from the buyer's pain.
- Sell outcomes, not stack.
- Make ROI visible.
- Treat objections as information.
- Follow up with useful context.

## Framework

Use SPIN when appropriate:

- Situation
- Problem
- Implication
- Need-Payoff

## Deliverable

`marketing/07-sales-playbook.md`

Include:

- Discovery questions
- SPIN question set
- 30-second outcome pitch
- ROI template
- Objection responses
- Demo flow
- Follow-up cadence
- Qualification criteria

## Definition of Done

At least one unrelated buyer has completed a meaningful buying step. For an
early-stage founder, the strongest gate is generally a real paying customer,
paid pilot, or equivalent commercial commitment.

---

# Stage 8 — Activation & Metrics

## Objective

Measure the funnel that matches the product's actual GTM motion.

## Do not assume one universal funnel.

### Product-led example

Traffic
→ Signup
→ Activation
→ Trial
→ Paid
→ Retained
→ Referral

### Sales-led example

Lead
→ Qualified
→ Discovery
→ Demo
→ Pilot
→ Proposal
→ Contract
→ Renewal / Expansion

### Hybrid

Combine only the stages that actually exist.

## Metrics

Select only relevant metrics:

- Visitors
- Qualified leads
- Signup conversion
- Activation
- Trial → paid
- Demo → proposal
- Proposal → close
- Sales cycle
- MRR / ARR
- Churn
- Retention
- Expansion
- CAC
- Payback
- LTV
- NRR
- Referrals

## Warning

Early-stage LTV estimates may be unreliable when churn history is too short.
Mark such numbers as immature estimates.

Treat benchmark ratios such as LTV:CAC >= 3 as guidelines, not universal laws.

## Deliverable

`marketing/08-metrics.md`

Include:

- GTM funnel
- North Star / core value metric
- Metric definitions
- Current baseline
- Current bottleneck
- Next experiment

## Definition of Done

The founder knows which funnel exists, where prospects are dropping, and which
single metric or stage is the current constraint.

---

# Stage 9 — Pricing & Unit Economics

## Objective

Capture a defensible share of customer value while preserving healthy
economics.

## Principles

- Do not price only from server/API cost.
- Compare competitor pricing but do not copy it blindly.
- Estimate buyer value.
- Match pricing model to GTM motion.
- Avoid unnecessary tier complexity.
- Separate price objection from value misunderstanding and poor fit.

## Consider

- Value-based pricing
- Competitor range
- Free trial
- Freemium
- Soft paywall
- Hard paywall
- Usage-based
- Seat-based
- Contract / annual
- Paid pilot
- Enterprise pricing

## Deliverable

`marketing/09-pricing.md`

Include:

- Competitor price comparison
- Value estimate
- Pricing model
- Tiers or contract structure
- Monthly/annual logic if relevant
- Unit economics assumptions
- Pricing experiment

## Definition of Done

Pricing is tied to buyer value, market reality, and GTM motion rather than only
development cost.

---

# Stage 10 — Retention & Expansion

## Objective

Help customers repeatedly reach value and create reasons to renew, expand, and
refer.

## Work

- Define the Aha! moment
- Minimize Time to Value
- Outcome-focused onboarding
- Customer journey
- Churn reason log
- Support feedback loop
- Expansion path
- Referral path
- Cohort retention

## Deliverable

`marketing/10-retention-plan.md`

## Definition of Done

Retention is measurable, churn reasons are captured, and at least one explicit
renewal/expansion mechanism exists.

Do not impose a universal churn target without considering contract length,
market, ACV, and customer count.

---

# Stage 11 — Growth Machine

## Objective

Turn acquisition, conversion, retention, expansion, and referral into a
repeatable system.

## Growth loop

Traffic
→ Landing / Conversation
→ Activation / Qualified Opportunity
→ Paid
→ Retention
→ Expansion / Referral
→ More Traffic

Adapt the loop to the actual GTM motion.

## Work

- Map the complete growth system
- Identify the current bottleneck
- Design one product-native or customer-native loop
- Run one-variable experiments
- Build durable marketing assets
- Reduce dangerous channel concentration
- Establish weekly review
- Establish quarterly constraint review
- Document repeatable processes

## Deliverable

`marketing/11-growth-machine.md`

## Definition of Done

Growth no longer depends only on ad hoc founder effort. The business has a
measurable acquisition and retention system, documented experiments, and a
repeatable operating cadence.

---

# State management

Use:

`marketing/ROADMAP_STATE.md`

Update it after every meaningful run.

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
