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
description: What it does and when to trigger. Be specific and "pushy".
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

## Step 4: Validate

```powershell
python scripts/validate_curated_skills.py
```

All issues must be resolved before committing.

## Step 5: Commit & Push

```powershell
git add skills/<skill-name>/
git commit -m "feat: add <skill-name> skill"
git push origin main
```

skills.sh will re-index within ~1 hour of the push.
