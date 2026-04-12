# Project Overview Report

**Repository:** `fth-skills` — Curated AI Agent Skill Library  
**Platform:** [skills.sh](https://skills.sh/fatih-developer/fth-skills)  
**Last Analyzed:** 2026-04-12  
**Analysis Type:** Standard (3 Report Variant)

---

## 1. Project Identity

| Attribute | Value |
|-----------|-------|
| **Type** | Curated AI Agent Skill Library (npm-compatible skill ecosystem) |
| **Purpose** | Reusable instruction packs for coding workflows, decision-making, and agentic task safety |
| **Platform** | skills.sh marketplace with CLI discovery (`npx skills add`) |
| **License** | MIT |
| **Repository Path** | `H:\Project\fth-skills` |

---

## 2. Repository Structure

The repository follows a **flat skill directory architecture** under `skills/`:

```
fth-skills/
├── skills/                   # 61 skill directories (flat, not domain-organized)
│   ├── <skill-name>/
│   │   ├── SKILL.md         # REQUIRED: frontmatter + instructions
│   │   ├── agents/
│   │   │   └── openai.yaml  # REQUIRED: skills.sh CLI discovery
│   │   ├── references/      # optional: docs, checklists, examples
│   │   ├── templates/       # optional
│   │   ├── scripts/         # optional
│   │   └── evals/          # optional: test cases
│   │
│   └── eachlabs-kling-generator/  # EXCLUDED from git but present in working dir
│
├── scripts/
│   ├── validate_curated_skills.py   # 200 lines: frontmatter & file validator
│   ├── generate_openai_yaml.py      # 97 lines: auto-generates openai.yaml
│   └── translate_skills.py          # 58 lines: translation utility
│
├── docs/analyze/             # This report directory
├── .agent/workflows/         # Agent workflow templates
├── .gitignore               # Excludes _workspace/ and eachlabs-kling-generator
├── README.md                 # 331 lines
└── AGENTS.md                 # 90 lines
```

**Key Observation:** The README claims skills are organized into domain folders (`mobile/`, `api/`, `database/`), but the actual structure is **completely flat** — all 61 skills reside directly under `skills/`. This is a documentation-reality mismatch.

---

## 3. Skill Inventory

### 3.1 Total Count

| Metric | Count | Evidence |
|--------|-------|----------|
| Total skill directories | 61 | `Get-ChildItem -Path skills -Directory | Measure-Object` returned 61 |
| SKILL.md files | 61 | One per skill directory |
| `agents/openai.yaml` files | 61 | All skills have it (except excluded ones) |
| ECOSYSTEM.md files | 0 | None found in `skills/` subtree |

### 3.2 Skill Domains (as categorized in README)

| Domain | Claimed Count | Actual Skills |
|--------|--------------|---------------|
| **Mobile** | 10 | `accessibility-enforcer`, `app-store-reviewer`, `crash-analyst`, `deep-link-architect`, `mobile-perf-auditor`, `mobile-security-auditor`, `offline-sync-designer`, `onboarding-designer`, `push-notification-planner`, `release-orchestrator` |
| **API** | 10 | `api-mock-designer`, `api-observability-planner`, `auth-flow-designer`, `breaking-change-detector`, `changelog-generator`, `contract-first-designer`, `protocol-selector`, `rate-limit-strategist`, `sdk-scaffolder`, `webhook-architect` |
| **Database** | 11 | `access-policy-designer`, `data-lineage-tracer`, `data-masker`, `index-advisor`, `migration-strategist`, `pgbouncer-architect`, `query-budget-enforcer`, `query-explainer`, `schema-architect`, `schema-diff-analyzer`, `seed-data-generator` |
| **Security Ecosystem** | 4 | `ecosystem-security`, `security-auditor`, `adaptive-guard`, `security-orchestrator` |
| **Ecosystem Orchestrators** | 4 | `ecosystem-api`, `ecosystem-database`, `ecosystem-mobile`, `ecosystem-orchestration` |
| **Core Agentic** | 14 | `task-decomposer`, `parallel-planner`, `tool-selector`, `checkpoint-guardian`, `error-recovery`, `context-compressor`, `memory-ledger`, `multi-brain`, `output-critic`, `assumption-checker`, `agent-reviewer`, `project-analyzer`, `proje-analizcisi`, `skill-comparator` |
| **Frameworks** | 1 | `react-flow` |
| **Experimental** | 3 | `multi-brain-experts`, `multi-brain-debate`, `multi-brain-score` |
| **Other** | ~3 | `sqlite` (flat, not domain), `claw-integration-design`, `pgbouncer-architect` |

### 3.3 README Badge vs Actual Count

| Source | Count |
|--------|-------|
| README badge | 58 |
| `ls skills/ | wc -l` | 61 (including `eachlabs-kling-generator.zip`) |
| Actual curated skills | ~59 (excluding excluded eachlabs) |

Discrepancy: README badge claims "58" but there are 61 directories under `skills/`.

---

## 4. Ecosystem Paradigm

### 4.1 The Handoff Pattern

Skills follow a **Hybrid Handoff Pattern** where:

1. **Skill-to-Skill Handoffs:** Individual SKILL.md files specify `🔗 Next Steps` sections that reference downstream skills. Examples found in:
   - `skills/schema-architect/SKILL.md:73` — hands off to `access-policy-designer` after schema design
   - `skills/contract-first-designer/SKILL.md:94` — hands off after OpenAPI contract generation
   - `skills/mobile-perf-auditor/SKILL.md:105` — hands off to `release-orchestrator` after audit passes
   - `skills/accessibility-enforcer/SKILL.md:111` — similar pre-release audit handoff

2. **ECOSYSTEM.md References:** README claims domain ECOSYSTEM.md files define multi-stage workflows, but **zero ECOSYSTEM.md files exist** in the repository. Instead, skills reference workflows inline.

3. **Orchestrator Awareness:** `task-decomposer/SKILL.md:32` instructs agents to read `skills/.curated/domains/<domain>/ECOSYSTEM.md` — but this path does not exist.

### 4.2 Security Ecosystem

A 4-skill security subsystem:
- `ecosystem-security` — entry point/overview
- `security-auditor` — static audit + trust scoring (renamed from `skill-security` at commit `fe9309d`)
- `adaptive-guard` — runtime 5-tier message filter
- `security-orchestrator` — 7-phase workflow coordinator

**Note:** A `skill-security` folder **still exists** at `skills/skill-security/` even though it was renamed to `security-auditor`. This is orphaned/dead code.

---

## 5. skills.sh Discovery Requirement

**Critical Rule (from AGENTS.md):** Every skill MUST have `agents/openai.yaml` or it is completely invisible on skills.sh.

The validator enforces this since commit `23d007a` which added the requirement.

**Template for `agents/openai.yaml`:**
```yaml
interface:
  display_name: "Human Readable Skill Name"
  short_description: "One sentence description for the skills.sh listing."
  default_prompt: "Use $<skill-name> to help with this task."

policy:
  allow_implicit_invocation: true
```

---

## 6. Scripts

| Script | Lines | Purpose |
|--------|-------|---------|
| `validate_curated_skills.py` | 200 | Validates frontmatter, openai.yaml presence, file references, double-quote warnings |
| `generate_openai_yaml.py` | 97 | Auto-generates `agents/openai.yaml` for skills missing it (uses hardcoded display names) |
| `translate_skills.py` | 58 | Updates skill descriptions from a hardcoded translation dictionary |

---

## 7. Git State

### 7.1 Recent Commits (last 5)

| Commit | Message |
|--------|---------|
| `1f495d0` | feat: implement skill-security module with audit, guard, and trust scoring protocols |
| `435be34` | sqlite-omni added |
| `91b3a00` | fix: sanitize security scanner triggers in skill-comparator to remove false positives |
| `b8260eb` | feat: add skill-comparator and interactive README |
| `71f6d60` | readme updated |

### 7.2 Files Changed (last 5 commits)

23 files changed, +3465 insertions, -5 deletions (from `git diff --stat HEAD~5`)

---

## 8. Excluded/Problematic Artifacts

| Path | Status | Issue |
|------|--------|-------|
| `_workspace/` | In .gitignore, does not exist | Local drafts placeholder |
| `skills/eachlabs-kling-generator/` | In .gitignore, still exists in working dir | Personal/local use, NOT committed |
| `skills/eachlabs-kling-generator.zip` | In .gitignore | ZIP of the excluded folder |
| `skills/skill-security/` | Orphaned folder, still exists | Renamed to `security-auditor` at commit `fe9309d` but old folder not removed |

---

## 9. Validation Status

**Command:** `python scripts/validate_curated_skills.py`

### Errors (2)

| Skill | Error |
|-------|-------|
| `sqlite` | Invalid frontmatter line: `description: >` multiline fold — folder name `sqlite` does NOT match frontmatter name `sqlite-omni`. Also has unexpected key `compatibility` |
| `eachlabs-kling-generator` | Missing agents/openai.yaml (excluded from git, intentionally not indexed) |

### Warnings (16)

All 16 skills have unquoted double-quotes in their `description` field that may break the skills.sh YAML parser:

`adaptive-guard`, `agent-reviewer`, `assumption-checker`, `context-compressor`, `ecosystem-api`, `ecosystem-database`, `ecosystem-mobile`, `ecosystem-orchestration`, `ecosystem-security`, `error-recovery`, `memory-ledger`, `output-critic`, `parallel-planner`, `security-orchestrator`, `task-decomposer`, `tool-selector`

---

## 10. Key Findings Summary

1. **58 claimed, 61 actual** — README badge mismatch with directory count
2. **Flat structure vs hierarchical claim** — README describes domain folders but all skills are flat
3. **ECOSYSTEM.md missing** — Referenced in docs and skill instructions but zero files exist
4. **2 validation errors** — `sqlite` (name mismatch + bad frontmatter), `eachlabs-kling-generator` (missing openai.yaml, intentionally excluded)
5. **16 description warnings** — Unquoted double-quotes across security/multi-brain ecosystem skills
6. **Orphaned `skill-security/` folder** — Renamed to `security-auditor` but old folder remains
7. **Hardcoded script data** — `generate_openai_yaml.py` has hardcoded skill display names dict, will break if new skills added without updating script
