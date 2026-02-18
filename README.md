# fth-skills

Agent skills for coding workflows, packaged for the `skills.sh` ecosystem.

This repository uses `skills.sh` skill format (`SKILL.md` instruction packs), not Mycroft/OVOS runtime Python skills.

## Install

Install all skills from this repository:

```bash
npx skills add <github-owner>/fth-skills
```

Install only one skill:

```bash
npx skills add https://github.com/<github-owner>/fth-skills --skill react-flow
```

## Structure

```text
fth-skills/
|- skills/
|  |- .curated/
|  |  |- react-flow/
|  |     |- SKILL.md
|  |     |- references/
|  |     |- templates/
|  |     `- agents/
|  `- .experimental/
|- README.md
`- LICENSE
```

## Available Skills

| Skill | Channel | Description |
|---|---|---|
| `react-flow` | `.curated` | Analyze, repair, migrate, and scaffold `@xyflow/react` projects with typed patterns and safe auto-fix workflow. |

Migration capabilities are bundled inside `react-flow` (no separate migration skill is required).

## Add a New Skill

1. Create a folder under `skills/.curated/<skill-name>/` or `skills/.experimental/<skill-name>/`.
2. Add a `SKILL.md` file with required YAML frontmatter:

```yaml
---
name: skill-name
description: Explain what the skill does and exactly when it should trigger.
---
```

3. Add only needed optional folders: `references/`, `templates/`, `scripts/`, `assets/`, `agents/`.
4. Keep the name in lowercase kebab-case and match folder name with `name`.
5. Update this README table after adding the skill.

## Release Checklist

1. Ensure each skill has `SKILL.md` with valid `name` and `description` frontmatter.
2. Run repository quality gate (all curated skills in one command):

```bash
python scripts/validate_curated_skills.py
```

3. (Optional) Run upstream per-skill validator:

```bash
python C:/Users/fatih/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/.curated/<skill-name>
```

4. Verify referenced files exist (`references/`, `templates/`, `agents/openai.yaml` when used).
5. Smoke-test install commands with your repo path:

```bash
npx skills add <github-owner>/fth-skills
npx skills add https://github.com/<github-owner>/fth-skills --skill <skill-name>
```

6. Commit and push to a public GitHub repository.
7. After publish, run one real task per skill and refine weak instructions.

## First Release Flow

Use this sequence after validation:

```bash
git add README.md LICENSE scripts/validate_curated_skills.py
git commit -m "chore: migrate repository to skills.sh format and add quality gate"
git add skills/.curated/react-flow
git commit -m "feat(skill): add unified react-flow curated skill"
git tag -a v0.1.0 -m "fth-skills initial curated release"
git push origin main --tags
```

Suggested next tags:
- `v0.1.1` for docs/checklist updates only.
- `v0.2.0` when adding a new curated skill.
- `v1.0.0` when skill contracts stabilize and install docs are final.

## License

MIT
