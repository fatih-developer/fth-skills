# Skip Conditions

Decision matrix for when to bypass task decomposition.

---

## Skip — Execute Directly

| Condition | Example |
|-----------|---------|
| Single-step task | "Fix this typo", "rename this variable" |
| User already has a plan | "I have 3 steps, just do them" |
| Under 3 minutes of work | "Add this import statement" |
| Bug fix with obvious cause | "This null check is missing" |
| Simple file operation | "Create a .gitignore file" |
| Direct question | "What does this function do?" |

## Decompose

| Condition | Example |
|-----------|---------|
| Task has multiple phases | "Build an auth system" |
| Unclear starting point | "Where do I begin?" |
| Dependencies between steps | "Set up DB then write API" |
| Multiple output files | "Create full documentation" |
| Research + implementation | "Analyze options then implement" |
| Refactoring across files | "Restructure this module" |
| Task takes > 30 minutes | Anything large enough to lose track |

## Edge Cases

- **"Just do it"** — Check if the task has hidden complexity. If it does, offer a quick plan: "This has 4 steps, want me to list them or just go?"
- **User gives partial steps** — Fill in the gaps, present the complete plan, then execute.
- **Mid-task scope change** — Stop, update the plan, get re-approval, continue.
