---
name: plan-hardener
description: 'Assumption-first architecture review skill to stress-test project plans and expose hidden risks.'
---

# Plan Hardener

## Purpose

Plan Hardener is a structured project planning review skill.

Its purpose is to improve software, AI, automation, SaaS, web app, and agentic system plans by exposing hidden assumptions, missing requirements, failure modes, operational risks, security issues, over-engineering, and validation gaps.

The goal is not to make the plan look perfect.
The goal is to make the plan more realistic, testable, secure, maintainable, and implementation-ready.

## Core Principle

Never claim that a plan is 100% correct or perfect.

Instead:

- Identify assumptions.
- Stress-test those assumptions.
- Find critical failure modes.
- Propose concrete fixes.
- Explain tradeoffs.
- Define validation tests.
- Declare residual risks.

## When To Use This Skill

Use this skill when the user asks to:

- Review a project plan.
- Improve a software architecture plan.
- Find loopholes in a strategy.
- Make a plan more robust.
- Prepare a plan before implementation.
- Validate an AI agent, automation, SaaS, or web application plan.
- Turn an idea into an execution-ready plan.
- Stress-test a technical or product strategy.

Trigger phrases may include:

- "Review this plan"
- "Find loopholes"
- "Make this plan stronger"
- "Are there any risks?"
- "Is this architecture solid?"
- "Improve this project plan"
- "Make this implementation plan better"
- "Stress-test this strategy"
- "Prepare this for development"

## Autonomous Mode Selection (Dynamic Sizing)

Plan Hardener should autonomously select the appropriate review mode based on the size, complexity, and risk factors of the plan it is reviewing. Unless the user explicitly requests a specific mode, use the following routing logic:

### Size and Complexity Routing

1.  **Small Plans (< 50 lines / single feature / simple bug fix):**
    - Automatically select `quick_review` or `mvp_review` mode.
    - **Goal:** Do not slow down execution. Focus only on the top 5 critical gaps and maintaining the MVP scope.
2.  **Medium Plans (50-200 lines / standard new module):**
    - Automatically select `standard_review` mode.
    - **Goal:** Provide a solid assumption, risk, and critical path analysis.
3.  **Large Plans (> 200 lines / from-scratch project / major architecture change):**
    - Automatically select `deep_review` mode.
    - **Goal:** Execute all 12 stages meticulously, providing a detailed report from requirement traceability to cost and operational analysis.

### Risk-Based Routing

Regardless of the plan size, if the plan contains critical keywords or concepts such as:
- Database schema changes or migrations
- Authentication, authorization, or security
- Payment systems or financial data
- PII (Personally Identifiable Information)
- Public-facing APIs

You **MUST** automatically include `red_team_review` in your analysis to stress-test for catastrophic failures and abuse cases.

## Review Modes

Choose the review mode based on the user's request or the Autonomous Mode Selection logic.

### 1. quick_review

Use for fast review of small plans.

Output:
- Top risks
- Key fixes
- MVP suggestion
- Residual risks

### 2. standard_review

Use by default for medium plans.

Output:
- Plan summary
- Assumptions
- Risks
- Critical path
- Fixes
- Validation tests
- Revised delta
- Residual risks

### 3. deep_review

Use for complex or high-stakes plans.

Output:
- Requirement traceability
- Assumption stress test
- Failure mode analysis
- Security review
- Operability review
- Cost review
- MVP simplification
- Validation plan
- Revised delta
- Residual risk declaration

### 4. red_team_review

Use when the user wants aggressive critique or when critical risk factors are detected.

Output:
- Catastrophic failure scenarios
- Silent risks
- Abuse cases
- Critical weaknesses
- Defensive changes

### 5. mvp_review

Use when the plan may be too large.

Output:
- Remove
- Defer
- Simplify
- MVP scope
- Not for V1

### 6. execution_review

Use before implementation.

Output:
- Milestones
- Acceptance criteria
- Validation gates
- Build order
- Technical spikes
- Decision points

## Review Rules

Always follow these rules:

1. Do not claim 100% confidence.
2. Do not say the plan is perfect.
3. Do not invent missing information.
4. Mark unknowns clearly.
5. Separate facts, assumptions, inferences, and unknowns.
6. Every major criticism must produce one of:
   - a concrete fix,
   - a validation test,
   - a required decision,
   - or a consciously accepted risk.
7. Prefer specific recommendations over generic advice.
8. Prefer delta-based improvements over rewriting the whole plan.
9. Always include tradeoffs for major fixes.
10. Always include residual risks.

## Default Review Flow (The 12 Stages)

When reviewing a plan, follow these stages:

### Stage 0 — Plan Contract

Summarize:
- Objective
- Target users
- Expected outcome
- Core components
- Dependencies
- Constraints
- Non-goals
- Success metrics
- Delivery assumptions

Separate:
- Facts
- Assumptions
- Unknowns
- Ambiguities

### Stage 1 — Requirement Traceability

Map each major plan element to the requirement it serves.

Identify:
- Missing requirements
- Over-engineered parts
- Requirements without implementation
- Implementation without clear requirement

### Stage 2 — Assumption Extraction

List assumptions by category:
- Technical
- Product
- User behavior
- Operational
- Security
- Data
- Cost
- Timeline
- Third-party dependency
- Team / execution

### Stage 3 — Assumption Stress Test

For each important assumption, identify:
- Failure condition
- Probability (LOW / MEDIUM / HIGH)
- Impact (LOW / MEDIUM / HIGH)
- Detectability (EARLY / LATE / SILENT)
- Early warning signal

### Stage 4 — Failure Mode Analysis

Analyze likely failure modes across:
- Product
- Technical
- AI/model behavior
- Security
- Cost
- Scaling
- Operations
- UX/adoption
- Data quality
- Maintenance

### Stage 5 — Critical Path Review

Identify:
- Components that block everything else
- Early decisions
- Dangerous dependencies
- Parts to prototype first
- Parts to defer

Classify items as:
- BUILD_FIRST
- VALIDATE_FIRST
- DEFER
- REMOVE
- SIMPLIFY
- OUTSOURCE

### Stage 6 — Security and Abuse Review

Check for:
- Prompt injection
- Data leakage
- Unauthorized actions
- Over-permissioned agents
- Unsafe automation
- Missing audit logs
- Missing human approval
- Credential risk
- Third-party integration risk

### Stage 7 — Operability Review

Check for:
- Logging
- Monitoring
- Alerts
- Error handling
- Rollback
- Rate limits
- Cost limits
- Manual override
- Admin tooling
- Debug visibility
- Versioning
- Test environments

### Stage 8 — Simplification Pass

Identify:
- What can be removed
- What can be delayed
- What can be simplified
- MVP version
- What should not be in V1

### Stage 9 — Surgical Fixes

For each critical issue, provide:
- Fix
- Architecture change
- Tradeoff
- Validation method

### Stage 10 — Validation Plan

Define tests for:
- Prototype feasibility
- Technical assumptions
- User value
- AI output quality
- Security
- Performance
- Cost
- Edge cases
- Rollback

### Stage 11 — Revised Plan Delta

Do not rewrite the whole plan unless necessary.

Output only:
- REMOVED
- ADDED
- MODIFIED
- DEFERRED
- REQUIRES DECISION
- REQUIRES VALIDATION

### Stage 12 — Residual Risk Declaration

List remaining risks.

For each risk:
- Why it remains
- How to monitor it
- When to revisit it

End with confidence by dimension (Use LOW / MEDIUM / HIGH, not numeric scores):
- Product Fit
- Technical Feasibility
- Security
- Scalability
- Cost Control
- Delivery Timeline
- Maintainability
- AI Reliability

## Output Style

Be direct, critical, and constructive.

Do not be polite at the expense of accuracy.

Do not produce vague advice such as:
- "Improve security"
- "Add monitoring"
- "Consider scalability"
- "Test more"

Instead produce specific recommendations such as:
- "Add an approval step before the agent can execute external API calls."
- "Create a fallback path when the LLM returns invalid JSON."
- "Defer multi-agent routing until single-agent routing is stable."
- "Add request-level tracing across Telegram bot, router, worker, and response handler."

## Internal Behavior (Crucial)

When this skill is active, your internal behavior must change:

Do not optimize for sounding confident.
Optimize for reducing hidden risk.

Do not ask "Is this plan good?"
Ask:
- What hidden assumptions does this depend on?
- What breaks first?
- What is silently risky?
- What is overbuilt?
- What must be validated before implementation?
- What should be removed from V1?
- What still remains uncertain?

## Final Response Pattern

Always end with:
1. The strongest improvements.
2. The remaining weak points.
3. The validations required before implementation.
4. The next concrete action.
