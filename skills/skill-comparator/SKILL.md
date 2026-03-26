---
name: skill-comparator
description: 'Analyzes and compares existing skills from any source (skills.sh, GitHub, Claude marketplace, or local files) against a target skill or requirement. Fetches skill content, evaluates it across 10 dimensions, produces a structured comparison table, identifies gaps, and recommends whether to adopt, adapt, or build from scratch. Trigger when: analyze this skill, compare skills, is this skill good enough, what does this skill do, skill evaluation, should I use this skill, skill gap analysis, paste a skills.sh URL, GitHub skill URL, or upload a SKILL.md file for review.'
---

# Skill Comparator

Fetch the skill, read it deeply, evaluate it across 10 dimensions, compare
against requirements or an alternative, produce a structured report.

**Core principle:** Never summarize shallowly. Read the actual skill content.
Quote specific lines as evidence. Every score must have a justification.

---

## PHASE 1 — Skill Acquisition

### 1.1 Determine Source

```
Source types:
A) skills.sh URL      → https://skills.sh/author/skills/skillname
B) GitHub URL         → https://github.com/org/repo/blob/main/skill/SKILL.md
C) Raw GitHub URL     → https://raw.githubusercontent.com/...
D) Uploaded file      → User uploads SKILL.md directly
E) Local path         → /path/to/SKILL.md
F) Skill name only    → Search skills.sh first, then GitHub
```

### 1.2 Fetch Strategy

**For skills.sh URLs:**
```
1. Fetch the page with web_fetch
2. Extract SKILL.md content from the page
3. Also extract metadata:
   - Weekly installs
   - Security audit results (Gen Agent Trust Hub / Socket / Snyk)
   - First seen date
   - Supported platforms (claude-code, copilot, etc.)
   - Repository link
```

**For GitHub URLs:**
```
1. Convert to raw URL and attempt `web_fetch`.
2. If `web_fetch` fails (e.g., due to private repository authentication), do NOT give up immediately. Automatically attempt to use local Git tools (e.g., `git clone` to a temp directory, or GitHub CLI `gh api`).
3. Fetch raw SKILL.md content.
4. If all automated fetches fail or if instructed, ask the user to manually paste the SKILL.md content as a fallback.
```

**For uploaded files:**
```
Read content directly — no fetch needed
```

### 1.3 If Skill Cannot Be Fetched
```
Inform the user:
"Could not fetch the skill at [URL].
Options:
1. Paste the SKILL.md content directly into the chat
2. Upload the SKILL.md file
3. Provide a different URL"
```

---

## PHASE 2 — Deep Reading

Before scoring, read the entire skill carefully.
Extract and note:

```
□ Name and version
□ Language (English / Spanish / other)
□ Description / trigger conditions
□ Scope: what does it actually do?
□ Target project/context (general or specific to one project?)
□ Steps / phases / instructions
□ Config files or templates included
□ Hardcoded values (magic numbers, project-specific strings)
□ Security practices
□ Error handling
□ What it explicitly does NOT do
□ Dependencies mentioned
□ Output files / artifacts produced
□ Notes / warnings / caveats
```

**Red flags to note immediately:**
```
⚠️  Hardcoded passwords, API keys, project names
⚠️  Written in a language you don't understand
⚠️  "latest" image tags instead of pinned versions
⚠️  No error handling
⚠️  Scope too narrow (one project only)
⚠️  Last updated > 1 year ago
⚠️  Security audit failures (Snyk FAIL, etc.)
```

---

## PHASE 3 — 10-Dimension Scoring

Score each RELEVANT dimension 1-10. Every score requires a one-line justification with a direct quote or reference from the skill content.

**CRITICAL ADAPTIVE SCORING RULE:** If a dimension (e.g., ORM Compatibility, Monitoring) is completely irrelevant to the skill being analyzed (e.g., a frontend UI checker that has no database), mark the score as `N/A`. DO NOT penalize the skill for irrelevant dimensions. Subtract that dimension's maximum points (10) from the total available points, and calculate the final percentage scaled out of the remaining valid dimensions (e.g., 72/80 = 90%).

---

### DIMENSION 1 — Scope & Generality (weight: high)
```
1-3:  Written for a single specific project, hardcoded names/values
4-6:  Partially general but has project-specific assumptions
7-9:  General purpose, works across different projects
10:   Fully general, adapts to any context through discovery questions

Evidence: Quote any hardcoded project names, DB names, or fixed values
```

---

### DIMENSION 2 — Technical Depth (weight: high)
```
1-3:  Surface-level instructions, no formulas, no reasoning
4-6:  Some depth, covers common cases
7-9:  Deep coverage, explains WHY not just WHAT, handles edge cases
10:   Expert-level, includes formulas, calculations, trade-off analysis

Evidence: Note what's missing vs what's covered
```

---

### DIMENSION 3 — Decision Intelligence (weight: high)
```
1-3:  No decision making — just applies a fixed approach
4-6:  Some conditional logic ("if X then Y")
7-9:  Asks questions, analyzes context, selects best approach
10:   Full decision tree with justifications for each branch

Evidence: Quote any decision logic or lack thereof
```

---

### DIMENSION 4 — ORM / Framework Compatibility (weight: medium)
*Skip or reduce weight if skill is not database/backend related*
```
1-3:  Works with one specific ORM/framework only
4-6:  Covers 2-3 ORMs with basic notes
7-9:  Covers major ORMs with specific config for each
10:   Comprehensive matrix, edge cases, migration paths

Evidence: List which ORMs/frameworks are mentioned
```

---

### DIMENSION 5 — Security Practices (weight: high)
```
1-3:  Hardcoded secrets, no security considerations, Snyk FAIL
4-6:  Basic security (mentions env vars) but incomplete
7-9:  Proper secret handling, CVE awareness, security checklist
10:   Passes skill-security audit, no hardcoded values, CVE check included

Evidence: Quote any hardcoded values, auth_type, secret handling
```

---

### DIMENSION 6 — Output Quality (weight: medium)
```
1-3:  No structured output, ad-hoc
4-6:  Some output but incomplete or unstructured
7-9:  Clear output files defined, structured format
10:   Multiple output artifacts, each with defined purpose and format

Evidence: List what outputs are produced
```

---

### DIMENSION 7 — Error Handling (weight: medium)
```
1-3:  No error handling, assumes everything works
4-6:  Mentions some failure modes
7-9:  Clear fallback paths, skip conditions, fail-open/fail-closed
10:   Comprehensive error taxonomy, recovery procedures, user communication

Evidence: Quote any error handling or note its absence
```

---

### DIMENSION 8 — Monitoring & Observability (weight: low-medium)
*Skip if skill type doesn't involve running infrastructure*
```
1-3:  No monitoring guidance
4-6:  Mentions monitoring exists
7-9:  Specific metrics, queries, or dashboards provided
10:   Full observability setup: metrics, alerts, dashboards, interpretation

Evidence: Quote monitoring-related content
```

---

### DIMENSION 9 — Documentation Quality (weight: medium)
```
1-3:  Minimal explanation, hard to understand intent
4-6:  Reasonable documentation, some gaps
7-9:  Clear phases, explains trade-offs, good inline comments
10:   Exemplary documentation, teaches concepts not just steps

Evidence: Note structure quality, comment density, explanation depth
```

---

### DIMENSION 10 — Freshness & Maintenance (weight: medium)
```
1-3:  Outdated (>2 years), references deprecated tools/versions
4-6:  Somewhat current, minor outdated references
7-9:  Recent, pinned versions, CVE awareness
10:   Actively maintained, latest versions, security bulletins referenced

Evidence: Note version numbers, dates, any outdated references
```

---

## PHASE 4 — Comparison Table

Generate the structured comparison table.

### Format A — Single Skill Analysis (no alternative)
```markdown
## Skill Analysis: [skill name]

**Source:** [URL or file]
**Language:** [language]
**Security:** [Trust Hub: X | Socket: X | Snyk: X]

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | N/10 | "[quote or finding]" |
| Technical Depth | N/10 | "[quote or finding]" |
| Decision Intelligence | N/10 | "[quote or finding]" |
| ORM Compatibility | N/10 | "[quote or finding]" |
| Security Practices | N/10 | "[quote or finding]" |
| Output Quality | N/10 | "[quote or finding]" |
| Error Handling | N/10 | "[quote or finding]" |
| Monitoring | N/10 | "[quote or finding]" |
| Documentation | N/10 | "[quote or finding]" |
| Freshness | N/10 | "[quote or finding]" |
| **TOTAL** | **N/100** | |

**Verdict:** [ADOPT / ADAPT / REPLACE / BUILD FROM SCRATCH]
```

### Format B — Side-by-Side Comparison (two skills)
```markdown
## Skill Comparison

| Dimension | [Skill A] | [Skill B] | Winner |
|-----------|-----------|-----------|--------|
| Language | Spanish | English | Skill B |
| Scope | Single project | General purpose | Skill B |
| Pool mode selection | Fixed: transaction | Analyzes & selects | Skill B |
| Pool size calculation | Hardcoded (25, 500) | Formula-derived | Skill B |
| ORM compatibility | asyncpg only | Drizzle/Prisma/TypeORM/SQLAlchemy | Skill B |
| CVE check | None | CVE-2025-12819 included | Skill B |
| Capacity analysis | None | RAM/CPU/connection formula | Skill B |
| Security | Snyk: FAIL ❌ | passes skill-security ✅ | Skill B |
| Weekly installs | 7 | — | Skill A (existing users) |
| Config style | Static copy-paste | Dynamic, project-adaptive | Skill B |
| **Score** | **N/100** | **N/100** | |
```

### Format C — Ecosystem Gap Analysis (multiple skills)
```markdown
## Ecosystem Coverage Analysis

**Goal:** [what you want to achieve]

| Capability | Existing Skill | Coverage | Gap |
|------------|---------------|----------|-----|
| Schema design | schema-architect | ✅ Full | — |
| Index optimization | index-advisor | ✅ Full | — |
| Connection pooling | pgbouncer (skills.sh) | ⚠️ Partial | No mode selection, hardcoded values |
| Migration planning | — | ❌ None | Needs new skill |
| CDC pipeline | — | ❌ None | Needs new skill |
```

---

## PHASE 5 — Gap Analysis

If gaps found, produce `skill-gap-list.md`:

```markdown
# Skill Gap Analysis

## Critical Gaps (blocking — must fix)
1. **[Gap name]**
   - What's missing: [description]
   - Why it matters: [impact]
   - Suggested fix: [add section / rewrite / new skill]

## Important Gaps (should fix)
...

## Minor Gaps (nice to have)
...
```

---

## PHASE 6 — Build or Adopt Recommendation

Final recommendation with reasoning:

```markdown
# Recommendation: [ADOPT / ADAPT / BUILD FROM SCRATCH]

## ADOPT — Use as-is
*When: score >75/100, language matches, scope fits, security passes*
→ Install instructions: `npx skills add [URL]`
→ No changes needed

## ADAPT — Fork and modify
*When: score 50-75/100, good foundation but specific gaps*
→ Start with existing skill
→ Required changes: [specific list]
→ Estimated effort: [X hours]

## BUILD FROM SCRATCH
*When: score <50/100, wrong language, too narrow scope, security failures*
→ Existing skill is a reference at best
→ Use gap analysis as requirements
→ Estimated effort: [X hours]
→ Key sections to include: [list]
```

---

## PHASE 7 — Output Files

All output files MUST be written to the `docs/skill-report/` directory to keep the user's workspace clean and standardized.

### docs/skill-report/skill-analysis-report.md
Full report combining Phases 3-6:
- Skill metadata
- 10-dimension scoring table with evidence (with dynamically scaling max points)
- Comparison table (if comparing two skills)
- Summary of strengths and weaknesses

### docs/skill-report/skill-gap-list.md
*(Only if gaps found)*
- Structured gap list by priority
- Each gap with impact and fix suggestion

### docs/skill-report/build-or-adopt.md
- Clear recommendation (ADOPT / ADAPT / BUILD)
- Justification
- If ADAPT: specific changes needed
- If BUILD: requirements derived from gap analysis

---

## USAGE EXAMPLES

### Example 1 — Analyze a skills.sh skill
```
User: "Analyze https://skills.sh/davidcastagnetoa/skills/pgbouncer"

→ Fetch page
→ Extract SKILL.md content + security audit results
→ Score 10 dimensions
→ Note: Spanish, single project, hardcoded values, Snyk FAIL
→ Verdict: BUILD FROM SCRATCH
→ Gap list: mode selection, pool sizing formula, ORM matrix, CVE check
```

### Example 2 — Compare two skills
```
User: "Compare https://skills.sh/X/skills/Y with my skill [uploads SKILL.md]"

→ Fetch external skill
→ Read uploaded skill
→ Score both on all dimensions
→ Side-by-side table
→ Highlight winners per dimension
→ Overall recommendation
```

### Example 3 — Ecosystem gap analysis
```
User: "I need PostgreSQL skills. What exists and what's missing?"

→ Search skills.sh for PostgreSQL skills
→ Fetch top 5 results
→ Map to capability matrix
→ Identify gaps
→ Prioritized build list
```

### Example 4 — Quick verdict
```
User: "Is this skill good? [pastes SKILL.md]"

→ Read content
→ Rapid 10-dimension scan
→ Single verdict table + 2-sentence summary
→ One recommendation
```

---

## SCORING CALIBRATION

Use this to ensure consistent scoring:

```
9-10: Best-in-class. Hard to improve.
7-8:  Solid. Minor improvements possible.
5-6:  Adequate. Clear gaps but usable.
3-4:  Below average. Significant missing pieces.
1-2:  Poor. Fundamental problems.

Never give 10/10 unless it truly cannot be improved.
Never give 1/10 unless it's actively harmful.
Always justify with evidence from the skill content.
```

---

## SKIP CONDITIONS

- User just wants to install a skill without analysis → help install, skip analysis
- Skill is internal/private and cannot be fetched → ask user to paste content
- User says "just tell me if it's good" → Phase 3 only, quick table, skip full report
