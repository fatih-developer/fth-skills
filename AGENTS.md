# AGENTS.md — fth-skills Repository

## Repo Purpose

A **curated AI agent skill library** for the [skills.sh](https://skills.sh/fatih-developer/fth-skills) ecosystem: reusable instruction packs for coding workflows, decision-making, and agentic task safety, organized into **ecosystems** with routed workflows and explicit handoffs. The public skill count is shown in the README badge (generated).

## Critical: skills.sh Discovery Requirement

**Every skill MUST have `agents/openai.yaml`** or it is invisible on skills.sh.

```
skills/<skill-name>/
├── SKILL.md              # required
└── agents/
    └── openai.yaml       # REQUIRED for skills.sh indexing
```

`openai.yaml` needs `interface.display_name`, a complete `interface.short_description` (≤150 characters, never ending in `...`), an `interface.default_prompt` that mentions `$<skill-name>`, and `policy.allow_implicit_invocation` (true/false).

## SKILL.md Frontmatter Rules

```yaml
---
name: <skill-name>          # must match folder name exactly
description: "What the skill does. Use when ..."
---
```

- Only `name` and `description` are allowed.
- The description must say **when** to use the skill (`Use when…`, `Trigger on…`).
- Frontmatter must be valid YAML. Prefer double quotes; never put unescaped `'` inside a single-quoted value.
- Keep `SKILL.md` under 500 lines; move detail into `references/` and link it.

## Ecosystems (source of truth)

Every skill belongs to exactly one ecosystem. Each ecosystem hub `skills/ecosystem-<domain>/` holds:

| File | Role |
|---|---|
| `references/workflows.json` | **Source of truth**: members, workflows (steps with *do*, *done_when*, conditions, parallel groups), direct handoffs, gate precedence |
| `SKILL.md` | Hand-written intro + generated catalog, router protocol, and workflow blocks |
| `references/handoff-contract.md` | Generated from `scripts/templates/ecosystem/` |
| `scripts/install_all.py` | Generated dry-run installer (`--status`, `--workflow`, `--missing-only`, `--execute`) |

Hubs: `ecosystem-orchestration` (hub of hubs), `ecosystem-reasoning`, `ecosystem-api`, `ecosystem-database`, `ecosystem-mobile`, `ecosystem-web`, `ecosystem-product`, `ecosystem-security`.

`scripts/build_ecosystems.py` renders from the maps: hub blocks, each member's `🔗 Next Steps & Handoffs` block, the ecosystem index in `task-decomposer` and `parallel-planner`, `skills.sh.json` groupings, and the README catalog. **Never edit generated blocks by hand** — edit `workflows.json` and rebuild.

## Validation (run before every commit; CI runs the same)

```bash
python scripts/build_ecosystems.py            # regenerate derived files
python scripts/validate_curated_skills.py     # structural validation
python -m unittest discover -s scripts/tests  # tooling tests
```

The validator checks YAML frontmatter, trigger wording, file size, nested code fences, `openai.yaml` content, referenced paths and `@skill` references, orphan supporting files, JSON evals, ecosystem membership, `skills.sh.json` and README coverage, committed bytecode, and that generated files are current.

## Key Scripts

| Script | Purpose |
|---|---|
| `scripts/build_ecosystems.py` | Renders every ecosystem-derived artifact; `--check` for CI |
| `scripts/validate_curated_skills.py` | Validates all skills and repo-level registration |
| `scripts/generate_openai_yaml.py` | Creates a starter `agents/openai.yaml` for new skills |
| `scripts/publish_clawhub.py` | Publishes skills listed in `skills.sh.json` to ClawHub |
| `scripts/tests/` | Tests for the tooling above |

## Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter.
2. Run `python scripts/generate_openai_yaml.py <skill-name>` and edit the result.
3. Add the skill as a member of one ecosystem in `skills/ecosystem-<domain>/references/workflows.json` (and to workflows or handoffs where it belongs).
4. Run `python scripts/build_ecosystems.py` then `python scripts/validate_curated_skills.py`.
5. Commit the skill together with the regenerated files.

Skills.sh re-indexes automatically within ~1 hour of push.

## Deprecated Aliases

`proje-analizcisi` → `project-analyzer` and `skill-security` → `security-auditor`. Aliases stay installable, route to the canonical skill, and set `allow_implicit_invocation: false`. Declare them under `deprecated` in the owning `workflows.json`.

## Safety Conventions

- Irreversible or production-impacting actions (deploys, restarts, migrations on shared databases, deletions, bulk sends) go through `checkpoint-guardian` or explicit user confirmation.
- Clarification gates follow one precedence (`project-focus-first` → `ask-first-act-later` → `assumption-checker` → `plan-hardener`); at most one runs per request.
- Skills that halt normal work or write files autonomously are not implicitly invoked.

## What NOT to Commit

- `_workspace/` — local drafts/experiments
- `skills/eachlabs-kling-generator/` — personal/local use only
- `__pycache__/`, `*.pyc`

## Quick Install (for users)

```bash
npx skills add fatih-developer/fth-skills --skill <skill-name>  # single skill
npx skills add fatih-developer/fth-skills                        # all skills
```
