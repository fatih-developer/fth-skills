---
name: ecosystem-mobile
description: "Route mobile app work — pre-release audits, store submission, feature architecture, crash investigation — through the right fth-skills mobile skills in order. Use when the user wants to audit an app before launch, ship to the App Store or Play Store, build deep links, push, offline or onboarding features, fix crashes, or asks which mobile skills to use."
---

# 📱 Mobile Ecosystem

This skill is the entry point of its ecosystem. It chooses a workflow, checks which member skills are installed, runs them in order with explicit handoffs, and degrades gracefully when a member is missing. The workflow map lives in `references/workflows.json`; the handoff format lives in `references/handoff-contract.md`.

## Catalog

<!-- BEGIN GENERATED: ecosystem-catalog (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Domain:** Mobile App Domain — Architect, audit, release, and monitor iOS, Android, React Native, and Flutter apps.

**Philosophy:** Mobile apps live under store guidelines, limited battery and memory, and unreliable networks. Never ship a feature that regresses performance, security, or accessibility.

| Skill | Role | Handoff artifact |
|---|---|---|
| `@accessibility-enforcer` | Audits VoiceOver/TalkBack support and WCAG mobile criteria. | inline handoff block |
| `@mobile-perf-auditor` | Diagnoses cold start, frame drops, memory, battery, and bundle size. | inline handoff block |
| `@mobile-security-auditor` | Audits against OWASP Mobile Top 10: storage, network, runtime defenses. | inline handoff block |
| `@app-store-reviewer` | Checks App Store and Play Store guideline compliance and metadata. | inline handoff block |
| `@release-orchestrator` | Plans versioning, changelogs, beta tracks, and staged rollouts. | inline handoff block |
| `@deep-link-architect` | Designs Universal Links and App Links with fallbacks. | inline handoff block |
| `@push-notification-planner` | Designs APNs/FCM payloads, permission timing, and routing. | inline handoff block |
| `@offline-sync-designer` | Designs local-first storage, conflict resolution, and background sync. | inline handoff block |
| `@onboarding-designer` | Designs first-run experience, permission sequencing, and empty states. | inline handoff block |
| `@crash-analyst` | Symbolicates and analyzes crash reports to a root cause and fix. | inline handoff block |
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
### 1. Pre-Release Audit Flow (`mobile-pre-release-audit`)

**When:** “audit the app before launch”; “is the app ready”; “review mobile app quality”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@accessibility-enforcer` | Audit screen reader labels, touch targets, and contrast. | No critical accessibility issue remains open. | — | `audit` |
| 2 | `@mobile-perf-auditor` | Audit startup, rendering, memory, and bundle size. | Key metrics are within the stated budgets. | — | `audit` |
| 3 | `@mobile-security-auditor` | Audit storage, transport, secrets, and runtime defenses. | No critical OWASP Mobile finding remains open. | — | `audit` |

### 2. Production Release Flow (`mobile-release`)

**When:** “ship to the stores”; “prepare the release”; “submit to App Store or Play Store”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@app-store-reviewer` | Check guidelines, privacy disclosures, and store metadata. | No rejection-risk item remains open. | Run the Pre-Release Audit Flow first | — |
| 2 | `@release-orchestrator` | Bump versions, write notes, and plan beta and staged rollout. | Rollout stages, halt criteria, and notes are ready. | — | — |
| 3 | `@checkpoint-guardian` | Confirm before submitting to the stores or widening a rollout. | User explicitly approved the submission. | — | — |

### 3. Feature Architecture Flow (`mobile-feature-architecture`)

**When:** “build a mobile feature”; “add deep links”; “add push notifications”; “make the app work offline”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@deep-link-architect` *(optional)* | Design URL schema, association files, and in-app routing. | Links open the right screen on both platforms with a web fallback. | Feature needs deep links | `feature` |
| 2 | `@push-notification-planner` *(optional)* | Design payloads, permission timing, and tap routing. | Payload, permission, and analytics plan exist. | Feature needs push notifications | `feature` |
| 3 | `@offline-sync-designer` *(optional)* | Design local storage, optimistic UI, and conflict resolution. | Every entity has a sync and conflict policy. | Feature must work offline | `feature` |
| 4 | `@onboarding-designer` *(optional)* | Design first-run flow and permission sequencing. | Aha moment, permissions, and empty states are defined. | Feature changes first-run experience | `feature` |

### 4. Post-Launch Monitoring Flow (`mobile-post-launch`)

**When:** “fix crashes”; “investigate app issues”; “analyze crash reports”

| # | Skill | Does | Done when | Condition | Parallel group |
|---|---|---|---|---|---|
| 1 | `@crash-analyst` | Symbolicate, isolate the exception, and propose a fix. | Root cause and fix are identified. | — | — |
| 2 | `@mobile-perf-auditor` *(optional)* | Profile the regression when the root cause is performance (ANR, OOM, jank). | Performance fix is verified. | Root cause is performance-related | — |
| 3 | `@release-orchestrator` *(optional)* | Plan a hotfix release. | Hotfix version and rollout plan exist. | — | — |

### Direct handoffs

- `@push-notification-planner` → `@deep-link-architect`: Notification taps must open a specific screen.
- `@mobile-security-auditor` → `@auth-flow-designer`: Findings involve token storage or backend auth design.
- `@offline-sync-designer` → `@sqlite`: Local storage is SQLite-based.
<!-- END GENERATED: ecosystem-workflows -->
