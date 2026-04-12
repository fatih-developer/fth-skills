# Architecture and Code Quality Report

**Repository:** `fth-skills` — Curated AI Agent Skill Library  
**Analysis Date:** 2026-04-12  
**Analysis Type:** Architecture & Code Quality

---

## 1. Architecture Overview

### 1.1 Design Philosophy

The repository implements a **curated skill library** pattern for the skills.sh ecosystem. Skills are self-contained instruction packs that can be discovered and invoked by AI agents via the skills.sh CLI.

**Key Architectural Principles:**
1. **Flat Directory Structure** — All 61 skills live directly under `skills/` (no nested domain folders despite documentation)
2. **Mandatory File Contract** — Every skill MUST have `SKILL.md` + `agents/openai.yaml`
3. **Hybrid Handoff Pattern** — Skills reference each other via `🔗 Next Steps` sections rather than rigid automation
4. **Reference File Support** — Skills optionally include `references/`, `templates/`, `scripts/`, `evals/`

### 1.2 Skill Anatomy

```
skills/<skill-name>/
├── SKILL.md              # REQUIRED: YAML frontmatter + markdown instructions
├── agents/
│   └── openai.yaml       # REQUIRED: skills.sh CLI discovery manifest
├── references/           # OPTIONAL: supporting docs, checklists, examples
├── templates/            # OPTIONAL: templated files
├── scripts/              # OPTIONAL: helper scripts
└── evals/                # OPTIONAL: test cases (evals.json)
```

---

## 2. Frontmatter Validation Rules

### 2.1 Required Keys

From `scripts/validate_curated_skills.py:15`:
```python
REQUIRED_FRONTMATTER_KEYS = {"name", "description"}
```

**Rules:**
1. `name` — Must equal the folder name exactly (case-sensitive)
2. `description` — Must be non-empty, one-line recommended

### 2.2 Validation Checks

The validator (`validate_curated_skills.py`) performs:

| Check | Lines | Description |
|-------|-------|-------------|
| SKILL.md existence | 89-91 | Missing SKILL.md = FAIL |
| Frontmatter delimiter | 35-45 | Must start and end with `---` |
| Required keys | 99-101 | Missing `name` or `description` = FAIL |
| Extra keys | 103-105 | Keys outside `{"name", "description"}` = WARNING |
| Name-folder match | 107-114 | Frontmatter `name` must equal folder name = FAIL |
| Non-empty description | 116-117 | Empty description = FAIL |
| openai.yaml existence | 119-122 | Missing `agents/openai.yaml` = FAIL |
| Double-quote warning | 124-131 | Unquoted `"` in description = WARNING |
| File references | 133-135 | Referenced paths must exist = FAIL |

### 2.3 Frontmatter Parsing

The parser (`validate_curated_skills.py:31-70`) uses a simple custom implementation rather than a YAML library:

- Splits on first `:` to get key-value
- Strips quotes if value is `"quoted"` or `'quoted'`
- Does NOT handle multiline folded strings (`>` or `|`) correctly — this causes the `sqlite` validation error

**Evidence of parsing issue:** `skills/sqlite/SKILL.md` uses multiline description with `>` fold but validator fails with "Invalid frontmatter line".

---

## 3. Ecosystem Handoff Paradigm

### 3.1 Skill-to-Skill Handoffs

Found 7 skills with explicit `🔗 Next Steps` sections:

| Skill | File:Line | Handoff Target |
|-------|-----------|----------------|
| `schema-architect` | SKILL.md:73 | `access-policy-designer` (after schema design) |
| `contract-first-designer` | SKILL.md:94 | Subsequent API skills (OpenAPI-First Design Flow) |
| `mobile-perf-auditor` | SKILL.md:105 | `release-orchestrator` (after audit passes) |
| `accessibility-enforcer` | SKILL.md:111 | `release-orchestrator` (Pre-Release Audit Flow) |
| `release-orchestrator` | SKILL.md:109 | Final step of Mobile ECOSYSTEM guide |
| `ecosystem-mobile` | SKILL.md:48 | `mobile-perf-auditor` (on performance conclusion) |

### 3.2 ECOSYSTEM.md Maps (Claimed but Missing)

README claims:
> "Every domain folder (`mobile`, `api`, `database`) contains an `ECOSYSTEM.md` map. Orchestrator agents (like `task-decomposer` and `parallel-planner`) read these maps dynamically"

**Reality:** Zero ECOSYSTEM.md files exist in the repository. The path `skills/.curated/domains/<domain>/ECOSYSTEM.md` referenced in `task-decomposer/SKILL.md:32` does not exist.

### 3.3 Orchestrator Skills

4 ecosystem orchestrators exist as flat skills:
- `ecosystem-api` — with `scripts/install_all.py`
- `ecosystem-database` — with `scripts/install_all.py`
- `ecosystem-mobile` — with `scripts/install_all.py`
- `ecosystem-orchestration` — no install script

These appear to be meta-skills for bulk installation rather than true ECOSYSTEM.md guides.

---

## 4. skills.sh Discovery Mechanism

### 4.1 The openai.yaml Requirement

Every skill MUST have `agents/openai.yaml` for CLI discovery. The validator enforces this since commit `23d007a`.

**Template structure:**
```yaml
interface:
  display_name: "Human Readable Skill Name"
  short_description: "One sentence for skills.sh listing."
  default_prompt: "Use $<skill-name> to help with this task."

policy:
  allow_implicit_invocation: true
```

### 4.2 Auto-Generation Script

`scripts/generate_openai_yaml.py` can generate missing `openai.yaml` files. However:
- It only handles skills in its hardcoded `SKILL_DISPLAY_NAMES` dict (lines 9-41)
- Does NOT auto-detect new skills added to the repository
- Skills must be manually added to the dict before regeneration

**Evidence of brittleness:** 97 lines of hardcoded data that will silently skip any new skills not in the dict.

---

## 5. Code Quality Analysis

### 5.1 Validation Script (`validate_curated_skills.py`)

| Aspect | Assessment |
|--------|------------|
| **Size** | 200 lines — appropriately scoped |
| **Dependencies** | Only `pathlib` and `re` from stdlib — excellent |
| **Custom YAML parser** | Problematic — doesn't handle multiline folded strings (`>`) |
| **Error messages** | Clear, actionable — includes skill name and specific issue |
| **Path reference validation** | Uses regex to extract paths and validates existence — good |

**Issues:**
1. Custom YAML parser fails on multiline descriptions (`sqlite` bug)
2. Skips directories starting with `.` — intentional but not documented
3. No type hints (despite `from __future__ import annotations`)

### 5.2 Generate Script (`generate_openai_yaml.py`)

| Aspect | Assessment |
|--------|------------|
| **Size** | 97 lines |
| **Hardcoded display names** | Maintenance burden — must update dict for new skills |
| **Extract description** | Uses regex to parse frontmatter — fragile but functional |
| **Creates missing files** | Good — idempotent operation |

### 5.3 Translate Script (`translate_skills.py`)

| Aspect | Assessment |
|--------|------------|
| **Size** | 58 lines |
| **Purpose** | Bulk-update English descriptions for 27 skills |
| **Regex replacement** | Uses `re.sub` with multiline flag — could be fragile |
| **Deletes openai.yaml** | Intentionally removes before regeneration |

---

## 6. Security Architecture

### 6.1 Security Ecosystem Components

| Skill | Role | Lines in SKILL.md |
|-------|------|-------------------|
| `ecosystem-security` | Overview/map | Not measured |
| `security-auditor` | Static audit + trust scoring | 78 + references |
| `adaptive-guard` | Runtime 5-tier filter | ~80 + references |
| `security-orchestrator` | 7-phase coordinator | ~100 + references |

### 6.2 Reference Files for security-auditor

- `references/command-blacklist.md` — 177 lines
- `references/pii-patterns.md` — 158 lines
- `references/api-whitelist.md` — 33 lines
- `references/trust-matrix.md` — 176 lines

### 6.3 Reference Files for adaptive-guard

- `references/static-rules.md`
- `references/attack-taxonomy.md`
- `references/command-blacklist.md` (duplicate)
- `references/learning-examples.md`

---

## 7. Frontmatter Quality Issues

### 7.1 sqlite Malformed Frontmatter

**File:** `skills/sqlite/SKILL.md`

```yaml
---
name: sqlite-omni
description: >
  Expert SQLite guidance for modern full-stack and AI projects. Use this skill whenever the user
  mentions sqlite, sqlite3, bun:sqlite, better-sqlite3, aiosqlite, libsql, Turso, Cloudflare D1...
compatibility: "Bun 1.x+, Node 18+, Python 3.8+, Drizzle ORM, sqlite-vec, libsql/Turso"
---
```

**Issues:**
1. **Name mismatch:** Folder is `sqlite` but frontmatter declares `name: sqlite-omni` — validator FAIL
2. **Extra key:** `compatibility` is not in `REQUIRED_FRONTMATTER_KEYS` — validator WARNING
3. **Multiline description:** Parser likely fails on the `>` folded string

### 7.2 Unquoted Double-Quotes (16 Warnings)

The following skills have `"` characters in their description strings that are not single-quoted:

```
adaptive-guard, agent-reviewer, assumption-checker, context-compressor,
ecosystem-api, ecosystem-database, ecosystem-mobile, ecosystem-orchestration,
ecosystem-security, error-recovery, memory-ledger, output-critic,
parallel-planner, security-orchestrator, task-decomposer, tool-selector
```

**Risk:** YAML parser on skills.sh may break on these descriptions.

---

## 8. Dead/Orphaned Code

| Path | Issue | Evidence |
|------|-------|----------|
| `skills/skill-security/` | Renamed to `security-auditor` but folder still exists | Git history shows rename at commit `fe9309d` |
| `skills/eachlabs-kling-generator/` | Excluded from git but still in working directory | In .gitignore, folder exists with 4 files |
| `eachlabs-kling-generator.zip` | Excluded artifact | In .gitignore |

---

## 9. Documentation-Architecture Mismatch

| Documentation Claim | Reality | Impact |
|---------------------|---------|--------|
| "Domain folders (mobile/, api/, database/) contain skills" | Skills are flat under `skills/` | Misleading for contributors |
| "ECOSYSTEM.md maps define workflows" | Zero ECOSYSTEM.md files exist | Dead documentation |
| "58 curated skills" | 61 directories (including excluded) | Badge inaccuracy |
| "skill-security renamed to security-auditor" | Old folder `skill-security/` still exists | Orphaned code |

---

## 10. Git Integration Quality

### 10.1 Recent Change Velocity

Last 5 commits modified 23 files with +3465 insertions. Active development:
- Recent: skill-security module, sqlite-omni, skill-comparator
- Validator enhancements (openai.yaml requirement, double-quote warnings)

### 10.2 .gitignore Appropriateness

```gitignore
_workspace/                    # ✓ Local drafts — appropriate
skills/eachlabs-kling-generator/  # ✓ Personal use — appropriate
skills/eachlabs-kling-generator.zip
```

---

## 11. Summary

| Category | Rating | Notes |
|----------|--------|-------|
| **Architecture** | Good | Flat structure is simple, handoff pattern is sound |
| **Validation** | Needs Work | Multiline YAML parsing broken; extra key detection too strict |
| **Documentation** | Poor | Multiple claims don't match reality (domains, ECOSYSTEM.md, counts) |
| **Code Quality** | Acceptable | Small scripts, stdlib deps, but hardcoded data brittle |
| **Security** | Good | Comprehensive reference files, 4-skill security ecosystem |
| **Operational** | Needs Cleanup | Orphaned folders, validation errors, 16 warnings |
