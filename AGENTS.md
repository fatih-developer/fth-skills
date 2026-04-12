# AGENTS.md — fth-skills Repository

## Repo Purpose

This is a **curated AI agent skill library** for the [skills.sh](https://skills.sh/fatih-developer/fth-skills) ecosystem. It ships ~58 reusable instruction packs for coding workflows, decision-making, and agentic task safety.

## Critical: skills.sh Discovery Requirement

**Every skill MUST have `agents/openai.yaml`** or it is completely invisible on skills.sh.

```
skills/<skill-name>/
├── SKILL.md              # required
└── agents/
    └── openai.yaml       # REQUIRED for skills.sh indexing
```

## SKILL.md Frontmatter Rules

Every `SKILL.md` must start with YAML frontmatter:

```yaml
---
name: <skill-name>          # must match folder name exactly
description: One line description of what triggers this skill.
---
```

- `name` and `description` are **required**
- `name` must equal the folder name (validation fails otherwise)
- Description with unquoted `"` may break the skills.sh YAML parser — use single quotes or remove them

## Validation

```bash
python scripts/validate_curated_skills.py                    # validate all skills
python scripts/validate_curated_skills.py --root skills      # same (default)
python scripts/validate_curated_skills.py --root skills/.experimental  # experimental skills
```

All errors must be resolved before committing.

## Key Skills by Purpose

| Purpose | Skills |
|---------|--------|
| Session continuity | `memory-ledger` (incremental), `session-transfer` (full handoff for long tasks) |
| Task orchestration | `task-decomposer`, `parallel-planner`, `checkpoint-guardian` |
| Security | `skill-security`, `adaptive-guard`, `security-orchestrator` |

`memory-ledger` and `session-transfer` work together — the former tracks incremental progress, the latter preserves full context for session switching. Both are optional and independently installable.

## Key Scripts

| Script | Purpose |
|--------|---------|
| `scripts/validate_curated_skills.py` | Validates frontmatter, openai.yaml presence, and file references |
| `scripts/generate_openai_yaml.py` | Auto-generates `agents/openai.yaml` for skills missing it |
| `scripts/translate_skills.py` | Translates skill content |

## What NOT to Commit

- `_workspace/` — local drafts/experiments, excluded via `.gitignore`
- `skills/eachlabs-kling-generator/` — personal/local use only

## Ecosystem Paradigm

Skills are **not isolated**. They follow a handoff pattern:
- Domain folders contain `ECOSYSTEM.md` maps defining multi-skill workflows
- Orchestrator skills (`task-decomposer`, `security-orchestrator`, etc.) read these maps dynamically
- Skill `SKILL.md` files specify `🔗 Next Steps` handoffs to downstream skills

## Skill Anatomy

```
skills/<skill-name>/
├── SKILL.md           # frontmatter + instructions
├── references/        # docs, checklists, examples (optional)
├── agents/
│   └── openai.yaml    # REQUIRED
├── templates/         # templated files (optional)
├── scripts/           # helper scripts (optional)
└── evals/             # test cases evals.json (optional)
```

## Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter
2. Create `skills/<skill-name>/agents/openai.yaml` (use `scripts/generate_openai_yaml.py` as reference)
3. Run `python scripts/validate_curated_skills.py`
4. Fix all errors, then commit

Skills.sh re-indexes automatically within ~1 hour of push.

## Quick Install (for users)

```bash
npx skills add fatih-developer/fth-skills --skill <skill-name>  # single skill
npx skills add fatih-developer/fth-skills                        # all skills
```
