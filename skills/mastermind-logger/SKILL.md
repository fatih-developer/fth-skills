---
name: mastermind-logger
description: "Maintain a cross-referenced project knowledge wiki in docs/knowledgelib/: update topic files with durable decisions, constraints, and learnings from the session, and keep index.md and log.md current. Use when the user asks to save what was learned, update the project wiki or knowledge base, or invokes $mastermind-logger."
---

# Mastermind Logger Skill (LLM-Wiki Pattern)

This skill acts as an intelligent knowledge base maintainer, inspired by the "LLM-Wiki" pattern. It does NOT just leave "dump" files. When invoked, it compiles crucial technical discoveries, architectural decisions, and constraints from the active session and integrates them into a structured, interconnected wiki.

The core philosophy: **Knowledge should be compounding, constantly updated, and heavily cross-referenced, not just appended as isolated time-stamped files.**

## 🛠 Operation Protocol

Whenever the user triggers `mastermind-logger`, you MUST perform the following steps in the `[workspace-root]/docs/knowledgelib/` directory:

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
- **Scoped Writes:** Read and write only inside `docs/knowledgelib/`; never touch other files. If the folder does not exist yet, ask once before creating it. After that, update the wiki without further prompts, because the user invoked this skill to do exactly that.
- **Report Back:** When finished, give the user a short summary of which files were modified and what the current graph topology looks like.

## How This Differs from Related Skills

- `@memory-ledger` tracks the state of the **current task** (decisions, status, failed approaches) and is closed when the task ends.
- `@session-transfer` writes an **immutable handoff** so another session or agent can resume unfinished work.
- **This skill** keeps **durable project knowledge** (how things work and why) that stays true after the task is done. Promote only lasting facts from a ledger or handoff into the wiki; do not copy task status here.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-orchestration` — Agent Orchestration.

**Workflows:**
- **Knowledge Capture Flow** (`orch-knowledge`, step 2 of 2): last step → summarize the workflow outcome.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-orchestration`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
