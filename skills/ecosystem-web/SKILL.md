---
name: ecosystem-web
description: "Route web product work — page design and build, design-system enforcement, SEO and AI-search visibility, and Coolify deploys — through the right fth-skills web skills in order. Use when the user wants to build or review a web page, enforce DESIGN.md tokens, improve search or ChatGPT visibility, or deploy and verify a service."
---

# 🧭 Web Ecosystem

This skill is the entry point of its ecosystem. It chooses a workflow, checks which member skills are installed, runs them in order with explicit handoffs, and degrades gracefully when a member is missing. The workflow map lives in `references/workflows.json`; the handoff format lives in `references/handoff-contract.md`.

## Catalog

<!-- BEGIN GENERATED: ecosystem-catalog (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Domain:** Web, Design & Delivery — Design product-grade web interfaces, keep design systems consistent, make sites visible to search and AI answer engines, and deploy them.

**Philosophy:** Start from the user journey, keep design tokens as the single source of visual truth, measure discoverability instead of guessing, and verify every deploy.

| Skill | Role | Handoff artifact |
|---|---|---|
| `@claude-style-coding` | Product-minded implementation: user journey, UX states, and visual quality first. | inline handoff block |
| `@design-intelligence` | Generates or reviews web pages with a 12-category rubric. | inline handoff block |
| `@design-md-enforcer` | Extracts and enforces DESIGN.md design-token specifications. | inline handoff block |
| `@react-flow` | Audits, repairs, migrates, and scaffolds @xyflow/react projects. | inline handoff block |
| `@geo-auditor` | Read-only SEO/GEO/AEO audit of public websites. | inline handoff block |
| `@geo-optimizer` | Implements and verifies SEO/GEO/AEO changes in a web codebase. | inline handoff block |
| `@coolify-orchestrator` | Deploys, provisions, and debugs services on self-hosted Coolify. | inline handoff block |
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
### 1. Product Page Build Flow (`web-build-page`)

**When:** “build a landing page”; “design a dashboard”; “create a new web screen”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@design-md-enforcer` *(optional)* | Load or create DESIGN.md tokens before styling. | Tokens exist for color, type, spacing, and components. | Project has or needs a design system | — |
| 2 | `@design-intelligence` | Plan sections and UX rules (GENERATE mode). | Page strategy and section architecture are approved. | — | — |
| 3 | `@claude-style-coding` | Implement the slice with every UX state handled. | Loading, empty, error, and success states work. | — | — |
| 4 | `@geo-optimizer` *(optional)* | Add metadata, structured data, and crawlable content. | Page passes the local SEO/GEO checks. | Page is public | — |

### 2. Search & AI Visibility Flow (`web-visibility`)

**When:** “audit our site for SEO”; “why doesn't ChatGPT cite us”; “improve AI search visibility”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@geo-auditor` | Audit the public site and set a visibility baseline. | Prioritized findings with evidence. | — | — |
| 2 | `@geo-optimizer` *(optional)* | Implement the prioritized fixes in the codebase. | Fixes verified locally and live when possible. | Repository access is available | — |

### 3. UI Review Flow (`web-review`)

**When:** “review my site”; “audit this page”; “check design consistency”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@design-intelligence` | Score the page on 12 categories (REVIEW mode). | Issues are classified by severity. | — | `review` |
| 2 | `@design-md-enforcer` *(optional)* | Lint the implementation against DESIGN.md tokens. | Token drift is listed with fixes. | — | `review` |

### 4. Deploy & Verify Flow (`web-deploy`)

**When:** “deploy to Coolify”; “the deploy failed”; “service is down”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@checkpoint-guardian` | Confirm production restarts, env changes, or deletions. | User approved each production-impacting action. | — | — |
| 2 | `@coolify-orchestrator` | Deploy, read logs, and verify health. | Service is healthy after deploy. | — | — |
| 3 | `@geo-auditor` *(optional)* | Re-check crawlability of the live site after a public release. | No new blocking crawl issue. | — | — |

### Direct handoffs

- `@react-flow` → `@claude-style-coding`: The flow editor needs product-level UX polish.
- `@claude-style-coding` → `@accessibility-enforcer`: The UI ships inside a mobile app.
<!-- END GENERATED: ecosystem-workflows -->
