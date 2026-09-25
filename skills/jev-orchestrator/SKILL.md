---
name: jev-orchestrator
description: Orchestrate TypeSafe Jev as a first-class semantic decision runtime inside LLM and agent workflows. Use for bounded semantic judgments such as classification, routing, grading, filtering, triage, scoring, quality gates, RAG relevance, tool/model/agent selection, and confidence-based escalation. When Jev is appropriate, invoke the available Jev MCP/tool directly instead of merely recommending Jev or generating example integration code.
---

# JEV Orchestrator

Use Jev as a runtime decision primitive inside the current workflow.

Assume Jev authentication and its MCP/tool connection are already configured. Do not ask for API keys, tokens, endpoints, or MCP setup unless an actual invocation fails because the integration is unavailable.

The live TypeSafe documentation (https://docs.typesafe.ai/) is the source of truth for the current Jev API, models, limits, and SDK/tool behavior. Prefer it over this skill when they disagree.

## Core execution rule

Separate work into four owners:

1. **Deterministic code** — exact rules, arithmetic, counting, dates/times, permissions, thresholds, persistence, side effects, state transitions.
2. **Jev** — bounded semantic judgments: classification, routing, grading, filtering, triage, scoring, quality gates, relevance, escalation signals.
3. **Generative LLM** — writing, explanation, synthesis, brainstorming, open-ended reasoning.
4. **Human review** — consequential uncertainty when policy requires it.

If a task clearly fits Jev, invoke Jev directly. Do not stop at suggesting it.

## When to invoke Jev

Invoke Jev when all are true:

- semantic understanding is required;
- the answer space is bounded;
- deterministic code alone is insufficient;
- the judgment matters to the current execution path.

Common triggers:

- choose one known handler, model, tool, agent, skill, category, policy, workflow, theme, intent, or outcome;
- judge whether a semantic condition holds;
- grade an item on a defined ordered dimension;
- determine whether retrieved content is relevant;
- decide whether escalation, fallback, human review, stronger reasoning, or secondary processing is needed;
- evaluate generated content against explicit criteria;
- classify free-text tickets, documents, feedback, answers, records, or cases;
- replace an LLM prompt-and-parse step whose output is a small structured decision.

## When not to invoke Jev

Do not use Jev for:

- arithmetic, counting, weighted sums, or exact numeric aggregation;
- date/time calculation or comparison;
- deterministic validation already solved reliably in code;
- database lookups;
- exact string/enum checks;
- authentication or authorization enforcement;
- cryptographic validation;
- direct side effects;
- free-form content generation;
- genuinely open-ended output;
- security-critical enforcement as the sole control.

Prefer code when code is sufficient. Prefer the LLM when generation is required.

## Primitive selection

### Choice
Use when exactly one item should be selected from a known set.

Examples: intent, route, tool, model tier, workflow, card type, explanation type.

Add `other` or `no_match` when candidate coverage is not guaranteed.

### Noul
Use when deciding whether one semantic proposition holds.

Examples: needs human review, passage is relevant, answer mentions required concept, escalation required.

Use separate Noul judgments when multiple labels may independently be true. A probability near 0.5 means uncertainty, not medium severity.

### Score
Use for degree along an ordered, explicitly described semantic scale.

Examples: urgency, quality, completeness, impact, suitability.

Define every level concretely. Code applies business thresholds after the result.

See `references/primitive-selection.md`.

## Atomic judgments

Ask one coherent semantic question per judgment.

Bad:

```text
Is this request risky, urgent, fraudulent, and worth escalating?
```

Better:

```text
Noul: Does this request require fraud review?
Score: How urgent is the operational impact?
Noul: Does this request require human escalation?
```

## Speculative fan-out

When independent judgments share the same state, batch them in one Jev request when the connected tool supports it.

Example:

```text
Choice: intent
Noul: needs retrieval?
Noul: needs strong model?
Noul: needs human review?
Score: operational impact
```

Questions in the same batch must not depend on each other's answers.

Use a second Jev request only when an earlier answer is needed to fetch evidence, construct new state, or define the next candidates.

## Runtime behavior

When a Jev-suitable decision is found:

1. Build the minimum relevant state.
2. Select Choice, Noul, or Score.
3. Define explicit options or criteria.
4. Invoke the connected Jev MCP/tool immediately.
5. Read the returned decision and probability/confidence signals available from the tool.
6. Apply deterministic policy in code.
7. If uncertainty exceeds the application's accepted risk, use the configured fallback.
8. Continue the original task.

Do not merely say that Jev would be useful. Do not emit pseudo-code instead of invoking Jev when the tool can perform the decision.

## Confidence and fallback

Confidence is a routing signal, not proof of correctness.

Do not invent a universal threshold. Prefer thresholds calibrated on representative project data.

Fallback choices may include:

- stronger LLM;
- secondary evidence;
- another detector;
- safe default;
- manual review;
- human review.

For high-impact security/compliance/financial actions, Jev may contribute a signal but deterministic policy and/or human review must own the final action.

See `references/confidence-routing.md`.

## Keep execution in code

Jev supplies judgments. Code owns:

- thresholds and weighting;
- business rules;
- permissions;
- side effects;
- persistence;
- retries;
- state transitions;
- monetary calculations;
- schedules;
- final enforcement.

Do not ask Jev to calculate a final weighted numeric result when code can combine typed signals exactly.

## State discipline

Send only the information required for the judgment. Prefer named JSON fields when the context has several parts.

Avoid unrelated history, secrets, authentication tokens, full user profiles, or large irrelevant documents.

## Tool discovery

Exact Jev MCP/tool names may vary by host. If the operations are not already known:

1. inspect available connected tools;
2. identify the TypeSafe/Jev integration;
3. identify Choice, Noul, Score, or a generic typed-judgment operation;
4. invoke the matching operation.

Do not ask the user to configure Jev unless discovery or invocation actually shows the integration is unavailable.

See `references/tool-contract.md`.

## Existing code review

Actively look for LLM calls that:

- request JSON containing a small fixed set of labels;
- ask yes/no semantic questions;
- rank or grade against explicit criteria;
- select which tool/model/agent to call;
- decide whether to retry or escalate;
- filter RAG/search results;
- classify tickets/documents/feedback;
- semantically validate generated output.

Treat these as Jev migration candidates. Do not replace deterministic validators merely because they contain branches.

## Failure handling

If Jev invocation fails:

1. preserve deterministic state;
2. use the project's configured fallback;
3. otherwise use a generative model for semantic judgment when safe;
4. otherwise use human/manual review;
5. log the failure when observability exists.

A Jev outage must not corrupt application state.

## Evaluation

For repeated production decisions, record enough to evaluate:

- Jev result;
- probability/confidence signals;
- model/version when available;
- fallback route;
- final outcome;
- user/human override;
- latency and cost;
- false-positive/false-negative outcomes when labels exist.

See `references/evaluation.md`.

## Design principle

> Code decides rules. Jev decides bounded meaning. The LLM generates and explains. Humans resolve consequential uncertainty.

Read as needed:

- `references/decision-matrix.md`
- `references/primitive-selection.md`
- `references/confidence-routing.md`
- `references/anti-patterns.md`
- `references/tool-contract.md`
- `references/evaluation.md`
- `references/examples/classification.md`
- `references/examples/routing.md`
- `references/examples/grading.md`
- `references/examples/rag.md`

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated by scripts/build_ecosystems.py from skills/ecosystem-*/references/workflows.json — do not edit by hand) -->
**Ecosystem:** `@ecosystem-orchestration` — Agent Orchestration.

**Direct handoffs:**
- `@checkpoint-guardian` — A Jev decision would trigger an irreversible side effect.
- `@error-recovery` — Jev invocation fails and no project fallback exists.
- `@output-critic` — An open-ended critique is needed beyond a bounded quality gate.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (see `@ecosystem-orchestration` → `references/handoff-contract.md`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
