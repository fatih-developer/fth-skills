---
name: ecosystem-product
description: "Route product and growth work — B2B go-to-market, naming, launch assets, and UGC creative — through the right fth-skills product skills in order. Use when the user wants to take a product to market, validate B2B demand, name or rebrand a product, or produce UGC-style campaign content."
---

# 🚀 Product Ecosystem

This skill is the entry point of its ecosystem. It chooses a workflow, checks which member skills are installed, runs them in order with explicit handoffs, and degrades gracefully when a member is missing. The workflow map lives in `references/workflows.json`; the handoff format lives in `references/handoff-contract.md`.

## Catalog

<!-- BEGIN GENERATED: ecosystem-catalog (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Domain:** Product & Growth — Take a product from focus to market: B2B go-to-market, naming, creative content, and discoverability.

**Philosophy:** Evidence before scale. Validate demand before building more, name and position only after the problem is clear, and measure every channel.

| Skill | Role | Handoff artifact |
|---|---|---|
| `@b2b-founder-roadmap` | Stage-gated B2B go-to-market from validation to repeatable revenue. | inline handoff block |
| `@brand-name-lab` | Generates, screens, and selects brand and product names. | inline handoff block |
| `@ugc-crafter` | Writes prompts for authentic UGC-style image and video content. | inline handoff block |
<!-- END GENERATED: ecosystem-catalog -->

## Router Protocol

<!-- BEGIN GENERATED: ecosystem-router (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
Follow this protocol whenever this ecosystem is invoked.

1. **Match.** Compare the request with each workflow's *When* phrases. Pick one workflow, or route straight to a single member skill when the request is narrow. If two workflows fit equally, ask one question to choose. If the request belongs to another domain, use the ecosystem index in `@ecosystem-orchestration`.
2. **Preflight.** Find out which step skills are installed: check the skills your host lists, or run `python <skill-dir>/scripts/install_all.py --status --workflow <id>` (`<skill-dir>` is the folder containing this `SKILL.md`). Show a short plan: step, skill, installed or missing, condition, expected artifact.
3. **Missing skills never block.** Offer once: (a) install them — `install_all.py --workflow <id>` prints the commands and only runs them with `--execute` after the user agrees; or (b) continue in fallback mode — perform the step yourself using its *Does* and *Done when* columns and label that output `fallback`.
4. **Conditions.** Skip optional steps whose condition does not hold, and say which steps you skipped and why.
5. **Execute.** Run steps in order. Steps that share a parallel group are independent and may run concurrently (`@parallel-planner`). Pass artifacts as described in `references/handoff-contract.md`. Check each step's *Done when* before moving on.
6. **Gates.** Before any destructive, irreversible, or production-impacting action, stop at `@checkpoint-guardian`, or ask for explicit confirmation when it is not installed.
7. **Failures.** When a step misses its *Done when*, hand off to `@error-recovery`. Without it, retry once with a changed approach, then report the blocker with evidence instead of guessing.
8. **State.** Keep a run log (workflow id, step, status, artifact). Record it with `@memory-ledger` when installed, and write a `@session-transfer` handoff if the run will continue in another session.
9. **Finish.** Summarize artifacts, skipped steps, open risks, and the most relevant next workflow.

**Skip this protocol** when the user names one specific skill (invoke it directly) or asks a quick factual question that needs no workflow.
<!-- END GENERATED: ecosystem-router -->

## Workflows

<!-- BEGIN GENERATED: ecosystem-workflows (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
### 1. Product Launch Flow (`product-launch`)

**When:** “launch a new product”; “take this idea to market”; “go-to-market plan”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@project-focus-first` *(optional)* | Fix the primary focus before planning. | User chose one primary focus. | No focus stated yet | — |
| 2 | `@b2b-founder-roadmap` | Diagnose the stage and run the current stage's work. | Stage deliverable meets its definition of done. | B2B product | — |
| 3 | `@brand-name-lab` *(optional)* | Create and screen names once positioning is clear. | One name selected with domain and trademark notes. | Product needs a name | — |
| 4 | `@geo-auditor` *(optional)* | Baseline search and AI visibility of the launch site. | Visibility baseline recorded. | — | `launch-assets` |
| 5 | `@ugc-crafter` *(optional)* | Produce UGC-style creative prompts for launch campaigns. | Prompt set covers each target platform. | — | `launch-assets` |

### 2. Naming & Positioning Flow (`product-naming`)

**When:** “name our product”; “rebrand”; “check this name”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@brand-name-lab` | Run the naming playbook through screening and selection. | Shortlist scored; one name locked. | — | — |
| 2 | `@multi-brain-debate` *(optional)* | Stress-test the final two names. | Verdict addresses every rebuttal. | — | — |

### 3. Creative Content Flow (`product-content`)

**When:** “UGC ad creatives”; “influencer-style product video”; “testimonial video prompts”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@ugc-crafter` | Build archetypes, identity locks, and scene prompts. | Prompts pass the UGC evaluation checklist. | — | — |
| 2 | `@prompt-crafter` *(optional)* | Evaluate or optimize prompts for a specific model. | Prompt meets the output contract. | — | — |

### Direct handoffs

- `@b2b-founder-roadmap` → `@geo-auditor`: Inbound discovery is the current bottleneck.
- `@b2b-founder-roadmap` → `@design-intelligence`: A landing page is needed for validation.
<!-- END GENERATED: ecosystem-workflows -->
