---
name: mastermind-logger
description: Automatically extracts key decisions, constraints, and learnings from the current session and appends them to a mastermind knowledge base under the docs/knowledgelib directory. Use this when you want to preserve session insights for future agents or project continuity.
---

# Mastermind Logger Skill

This skill acts as a memory crystallization tool. When invoked, it compiles crucial technical discoveries, architectural decisions, solved issues, or user preferences from the active session into a structured markdown document.

## 🛠 Operation Protocol

Whenever the user triggers `mastermind-logger`, you MUST perform the following steps autonomously:

### 1. Context Analysis
Scan the recent conversation history and current file context. Extract:
- **Key Constraints & Rulings**: Any rules or constraints newly established.
- **Architectural Decisions**: "Why" a specific approach was chosen.
- **Troubleshooting Insights**: A specific bug that was fixed and the root cause.
- **Next Steps / Open Questions**: What should the next agent know?

### 2. File Creation
Determine the current project's workspace directory (where you are executing).
- Create the target folder if it does not exist: `[workspace-root]/docs/knowledgelib/`
- Using the current system time, generate a timestamped filename: 
  `YYYY-MM-DD-HH-MM-[agent-name]-insights.md`
  *(e.g., `2026-04-18-22-35-mastermind-logger-insights.md`)*

### 3. File Execution
Write the extracted content using the exact template below.

## 📝 Document Template

```markdown
# Session Insights: [Short Descriptive Title]

**Date:** YYYY-MM-DD
**Time:** HH:MM
**Agent/Skill:** [Who recorded this]

## 🧠 Context & Goal
Briefly explain what the session or task was about. What was the core problem?

## 💡 Key Decisions & Constraints
- Decision 1 (Why it was made)
- Constraint 1 (Environment or API limits discovered)

## 🐛 Bugs & Fixes (If Applicable)
- **Symptom:** What went wrong?
- **Root Cause:** Why did it happen?
- **Resolution:** How was it fixed?

## 🔗 Actionable Takeaways
What should future agents or developers know when working on this module next?
```

## ⚠️ Important Guidelines
- **Do not ask for permission** to create the file if the skill is triggered. Just create it and tell the user it is done.
- Include concrete code snippets or commands in the **Bugs & Fixes** section if they are critical to the learning.
- Keep the language concise. A future agent will read this, so clarity over verbosity is paramount.
