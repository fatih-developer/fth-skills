---
name: mastermind-logger
description: Compiles and extracts session knowledge into a living, interconnected LLM-Wiki. Instead of writing isolated logs, it identifies key entities, updates cross-referenced topic files in docs/knowledgelib/, and maintains an index and chronological log. Use this to ensure persistent, compounding project knowledge.
---

# Mastermind Logger Skill (LLM-Wiki Pattern)

This skill acts as an intelligent knowledge base maintainer, inspired by the "LLM-Wiki" pattern. It does NOT just leave "dump" files. When invoked, it compiles crucial technical discoveries, architectural decisions, and constraints from the active session and integrates them into a structured, interconnected wiki.

The core philosophy: **Knowledge should be compounding, constantly updated, and heavily cross-referenced, not just appended as isolated time-stamped files.**

## 🛠 Operation Protocol

Whenever the user triggers `mastermind-logger`, you MUST perform the following steps autonomously in the `[workspace-root]/docs/knowledgelib/` directory:

### 1. Ingest & Analyze (Context Extraction)
Scan the recent conversation history and current file context. Determine what new information was produced:
- Technical rulings, constraints, or environment variables.
- Architectural design choices.
- Fixed bugs and their root causes.
- New concepts or API integrations explored.

### 2. Update/Create Entity Files (The Wiki Nodes)
Do **NOT** write all findings into a single date-stamped file. Instead, target specific "Entity/Topic" files.
- E.g., if the session involved Cloudflare and PayTR, you should modify (or create if missing) `cloudflare-config.md` and `paytr-integration.md`.
- Read the existing content of those domain files first.
- Inject the new findings seamlessly, updating outdated claims if necessary.
- **Cross-Reference:** You must use Obsidian-style markdown links (e.g., `[[cloudflare-config.md]]`) to connect concepts across different files.

### 3. Maintain the Central Index (`index.md`)
`docs/knowledgelib/index.md` acts as the map of the knowledge base.
- If you created a new entity file, add its link and a one-line summary to `index.md`.
- Group them logically (e.g., `## Infrastructure`, `## Third-Party Services`, `## Database`).

### 4. Provide the Chronological Trail (`log.md`)
`docs/knowledgelib/log.md` is an append-only timeline file. Add a new entry detailing what you updated in this session:
```markdown
## [YYYY-MM-DD HH:MM] ingest | [Short Descriptive Title]
- Discovered X, updated `[[entity-file-x.md]]`.
- Replaced outdated authentication pattern in `[[auth-module.md]]`.
- Linked Database rules to `[[cloudflare-config.md]]`.
```

## ⚠️ Important Guidelines
- **Be a Disciplined Maintainer:** You own the `docs/knowledgelib/` folder. Your text should be extremely concise.
- **Link Heavy:** The magic is in the cross-references. Connect new learnings to existing files.
- **No Permissions Needed:** Do not ask for permission to execute file reads and writes. Perform the operations using your filesystem tools directly.
- **Report Back:** When finished, give the user a short summary of which files were modified and what the current graph topology looks like.
