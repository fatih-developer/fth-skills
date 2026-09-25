---
description: How to create a new skill in the fth-skills repository
---

# Creating a New Skill in fth-skills

## Required File Structure

Every skill MUST have this minimum structure:

```
skills/<skill-name>/
├── SKILL.md              ← required: frontmatter + instructions
└── agents/
    └── openai.yaml       ← REQUIRED for skills.sh indexing
```

> ⚠️ **CRITICAL RULE: Always create `agents/openai.yaml`**
> skills.sh (https://skills.sh/fatih-developer/fth-skills) ONLY indexes skills
> that have this file. Without it, the skill is completely invisible on the platform.

## Step 1: Create SKILL.md

```markdown
---
name: <skill-name>
description: "What it does. Use when <concrete trigger phrases>."
---

# Skill Title

...instructions...
```

## Step 2: Create agents/openai.yaml (MANDATORY)

```yaml
interface:
  display_name: "Human Readable Skill Name"
  short_description: "One sentence description for the skills.sh listing."
  default_prompt: "Use $<skill-name> to help with this task."

policy:
  allow_implicit_invocation: true
```

## Step 3: Add Optional Supporting Files

```
references/    ← Docs, examples, checklists
assets/        ← Templates, JSON files
evals/         ← Test cases (evals.json)
  └── evals.json
```

## Step 4: Add the Skill to an Ecosystem

Add the skill as a member of exactly one ecosystem in `skills/ecosystem-<domain>/references/workflows.json`, and into workflow steps or direct handoffs where it belongs. Then regenerate the derived files (hub blocks, the skill's `🔗 Next Steps & Handoffs` section, `skills.sh.json`, README catalog):

```bash
python scripts/build_ecosystems.py
```

## Step 5: Validate

```bash
python scripts/validate_curated_skills.py
python -m unittest discover -s scripts/tests
```

Fix every error, then commit the skill together with the regenerated files. CI runs the same checks.
