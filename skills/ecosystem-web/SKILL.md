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
| `@design-system` | Researches and proposes palette and typography directions, writes DESIGN.md and tokens, designs pages, and reviews UI against them. | inline handoff block |
| `@design-intelligence` | Deprecated alias — use `@design-system`. | inline handoff block |
| `@design-md-enforcer` | Deprecated alias — use `@design-system`. | inline handoff block |
| `@anti-ai-slop-design` | Removes generic AI aesthetics and restores product-specific hierarchy in designs, reviews, and image briefs. | inline handoff block |
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
### 1. Palette & Typography Flow (`web-foundations`)

**When:** “choose colors and fonts for our product”; “create a design system”; “renk paleti ve tipografi öner”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@design-system` | FOUNDATIONS: scan competitors and type in use, find fonts beyond defaults, build 2-3 flat-color directions, and render the specimen. | specimen.html shows 2-3 directions with no FAIL checks and a written rationale. | — | — |
| 2 | `@anti-ai-slop-design` *(optional)* | Check each direction for generic AI aesthetics before the user chooses. | No direction relies on template colors, glow, or default fonts without a reason. | — | — |
| 3 | `@design-system` | SPEC: export the chosen direction to DESIGN.md, tokens.css, and the Tailwind theme. | DESIGN.md and tokens exist for the chosen direction. | — | — |
| 4 | `@claude-style-coding` *(optional)* | Apply the tokens to the codebase. | Components use tokens only; no hardcoded colors or gradients. | The user asked for code changes | — |

### 2. Product Page Build Flow (`web-build-page`)

**When:** “build a landing page”; “design a dashboard”; “create a new web screen”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@design-system` *(optional)* | FOUNDATIONS + SPEC: research, propose 2-3 palette and type directions, and export the chosen one as DESIGN.md and tokens. | An approved DESIGN.md with tokens exists. | No approved DESIGN.md yet | — |
| 2 | `@design-system` | PAGE: page strategy, section architecture, and rule check on top of DESIGN.md. | Page strategy and section architecture are approved. | — | — |
| 3 | `@anti-ai-slop-design` *(optional)* | Check the page direction for generic AI/SaaS patterns and replace them with product-specific choices. | No unjustified glow, gradient, fake proof, or uniform card grid remains in the plan. | Draft leans on generic AI visuals, or the user asked for a less generic look | — |
| 4 | `@claude-style-coding` | Implement the slice with every UX state handled. | Loading, empty, error, and success states work. | — | — |
| 5 | `@geo-optimizer` *(optional)* | Add metadata, structured data, and crawlable content. | Page passes the local SEO/GEO checks. | Page is public | — |

### 3. Search & AI Visibility Flow (`web-visibility`)

**When:** “audit our site for SEO”; “why doesn't ChatGPT cite us”; “improve AI search visibility”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@geo-auditor` | Audit the public site and set a visibility baseline. | Prioritized findings with evidence. | — | — |
| 2 | `@geo-optimizer` *(optional)* | Implement the prioritized fixes in the codebase. | Fixes verified locally and live when possible. | Repository access is available | — |

### 4. UI Review Flow (`web-review`)

**When:** “review my site”; “audit this page”; “check design consistency”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@design-system` | REVIEW: score 12 categories and lint the code against DESIGN.md tokens. | Issues are classified by severity and token drift is listed. | — | `review` |
| 2 | `@anti-ai-slop-design` *(optional)* | Flag generic AI patterns that weaken hierarchy, meaning, or credibility. | The few highest-impact patterns are listed with concrete fixes. | — | `review` |

### 5. Remove the AI Look Flow (`web-de-slop`)

**When:** “remove the AI look”; “make this less generic”; “too shiny, neon, or futuristic”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@anti-ai-slop-design` | Audit the design, pick one coherent correction, and apply it within the requested scope. | All seven acceptance checks pass and product identity is preserved. | — | — |
| 2 | `@design-system` *(optional)* | SPEC: record the corrected palette, type, and component rules as tokens. | DESIGN.md reflects the corrected choices. | The project has or needs a design system | — |
| 3 | `@claude-style-coding` *(optional)* | Implement the corrected design with every UX state handled. | Desktop and mobile renders match the correction. | The user asked for code changes | — |

### 6. Deploy & Verify Flow (`web-deploy`)

**When:** “deploy to Coolify”; “the deploy failed”; “service is down”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@checkpoint-guardian` | Confirm production restarts, env changes, or deletions. | User approved each production-impacting action. | — | — |
| 2 | `@coolify-orchestrator` | Deploy, read logs, and verify health. | Service is healthy after deploy. | — | — |
| 3 | `@geo-auditor` *(optional)* | Re-check crawlability of the live site after a public release. | No new blocking crawl issue. | — | — |

### Direct handoffs

- `@react-flow` → `@claude-style-coding`: The flow editor needs product-level UX polish.
- `@claude-style-coding` → `@accessibility-enforcer`: The UI ships inside a mobile app.
- `@anti-ai-slop-design` → `@ugc-crafter`: Imagery needs authentic, smartphone-style people or product shots.
- `@anti-ai-slop-design` → `@accessibility-enforcer`: The design is a mobile app screen.
- `@design-system` → `@anti-ai-slop-design`: A direction or page relies on generic AI/SaaS visuals.
- `@design-system` → `@accessibility-enforcer`: The system will be used in a mobile app.
<!-- END GENERATED: ecosystem-workflows -->
