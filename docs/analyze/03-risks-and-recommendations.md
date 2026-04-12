# Risks and Recommendations Report

**Repository:** `fth-skills` — Curated AI Agent Skill Library  
**Analysis Date:** 2026-04-12  
**Analysis Type:** Risks & Recommendations

---

## 1. Critical Risks

### 1.1 Frontmatter Validation Errors (2 skills)

#### Risk: `sqlite` SKILL.md Broken

| Attribute | Value |
|-----------|-------|
| **File** | `skills/sqlite/SKILL.md` |
| **Error** | "Invalid frontmatter line" — multiline YAML fold fails parsing |
| **Root Cause** | Custom YAML parser in validator doesn't handle `>` folded strings |
| **Secondary Issues** | Folder name `sqlite` ≠ frontmatter `name: sqlite-omni` (validation FAIL) <br> Extra key `compatibility` not in required set (validation WARNING) |
| **Impact** | `sqlite` skill cannot be validated; likely invisible or broken on skills.sh |
| **Severity** | **HIGH** — Active skill with 284 lines of content and 7 reference files |

#### Risk: `eachlabs-kling-generator` Missing openai.yaml

| Attribute | Value |
|-----------|-------|
| **File** | `skills/eachlabs-kling-generator/` |
| **Error** | Missing `agents/openai.yaml` |
| **Intentional?** | YES — in `.gitignore` as "personal/local use only" |
| **Impact** | Cannot be discovered via skills.sh; intentionally excluded |
| **Severity** | **LOW** — By design, but folder shouldn't exist in working directory if truly excluded |

---

### 1.2 Documentation-Architecture Mismatch

| Claim (README/AGENTS.md) | Reality | Risk |
|--------------------------|---------|------|
| "Domain folders organize skills" | All 61 skills are flat under `skills/` | Contributor confusion |
| "ECOSYSTEM.md maps define workflows" | **Zero** ECOSYSTEM.md files exist | Dead documentation; handoff pattern unsupported |
| "task-decomposer reads ECOSYSTEM.md" | Path `skills/.curated/domains/<domain>/ECOSYSTEM.md` does not exist | Broken feature |
| "58 curated skills" | 61 directories (or ~59 excluding excluded) | Badge inaccuracy |
| "skill-security → security-auditor" | Old `skill-security/` folder still exists | Orphaned code confusion |

**Severity: MEDIUM** — Contributors may create skills in wrong structure expecting domain folders that don't exist.

---

### 1.3 Orphaned/Dead Code

| Path | Issue | Action Needed |
|------|-------|---------------|
| `skills/skill-security/` | Renamed to `security-auditor` at commit `fe9309d` but folder remains | Delete or migrate |
| `skills/eachlabs-kling-generator/` | In .gitignore but present in working directory | Remove from filesystem OR commit |
| `eachlabs-kling-generator.zip` | In .gitignore | Already excluded |

**Severity: MEDIUM** — Dead code causes confusion and maintenance burden.

---

## 2. High-Priority Warnings (16 skills)

### 2.1 Unquoted Double-Quotes in Descriptions

All 16 warnings share the same pattern: Description contains literal `"` characters that may break YAML parsing on skills.sh.

| Skill | Description Contains |
|-------|---------------------|
| `adaptive-guard` | Likely: `5-tier` or similar |
| `agent-reviewer` | 6 dimensions |
| `assumption-checker` | Likely text with quotes |
| `context-compressor` | 70% |
| `ecosystem-api` | Multi-stage |
| `ecosystem-database` | Multi-stage |
| `ecosystem-mobile` | Multi-stage |
| `ecosystem-orchestration` | Multi-stage |
| `ecosystem-security` | 3-layer |
| `error-recovery` | Transient/config/logic/permanent |
| `memory-ledger` | Likely text with quotes |
| `output-critic` | Likely text with quotes |
| `parallel-planner` | Likely text with quotes |
| `security-orchestrator` | 7-phase |
| `task-decomposer` | Likely text with quotes |
| `tool-selector` | Likely text with quotes |

**Fix:** Wrap description values in single quotes instead of double quotes.

**Example:**
```yaml
# BAD
description: Analyzes "stuff" and does things.

# GOOD
description: 'Analyzes "stuff" and does things.'
```

**Severity: MEDIUM** — May cause silent failures on skills.sh platform.

---

## 3. Architecture Risks

### 3.1 Broken ECOSYSTEM.md Handoff Pattern

**Problem:** Skills reference ECOSYSTEM.md files that don't exist:
- `task-decomposer/SKILL.md:32` instructs reading `skills/.curated/domains/<domain>/ECOSYSTEM.md`
- Skills with `🔗 Next Steps` sections claim to follow "ECOSYSTEM guide" workflows

**Reality:** 
- No `ECOSYSTEM.md` files anywhere in repository
- No `.curated/domains/` directory structure
- The handoff pattern is **documented but unimplemented**

**Risk:** Skills declare adherence to workflows that cannot be verified or enforced.

**Recommendation:** Either:
1. Create actual ECOSYSTEM.md files (proper implementation), OR
2. Remove ECOSYSTEM.md references from skill instructions (documentation cleanup)

---

### 3.2 Hardcoded Script Data

**`generate_openai_yaml.py`** (97 lines) contains hardcoded `SKILL_DISPLAY_NAMES` dict (lines 9-41) with 27 skills.

**Problem:** When adding new skills:
1. Must remember to add to this dict
2. `generate_openai_yaml.py` will silently skip unknown skills
3. Easy to add a skill and forget to update the script

**Evidence:**
```python
SKILL_DISPLAY_NAMES = {
    "access-policy-designer": "Access Policy Designer",
    "accessibility-enforcer": "Accessibility Enforcer",
    # ... 25 more ...
}
```

**Recommendation:** Generate display names from `agents/openai.yaml` if it exists, or extract from `SKILL.md` frontmatter.

---

### 3.3 Custom YAML Parser Limitations

**`validate_curated_skills.py`** implements a custom YAML parser rather than using `PyYAML`.

**Problems:**
1. **Multiline folded strings fail** — `sqlite/SKILL.md` description uses `>` but parser fails
2. **No error recovery** — First malformed line aborts entire parse
3. **Limited quote handling** — Only handles simple `"x"` or `'x'` patterns

**Evidence of failure:**
```
[FAIL] [sqlite] Invalid frontmatter line: '  Expert SQLite guidance for modern full-stack and AI projects. Use this skill whenever the user'.
```

**Recommendation:** Replace custom parser with `PyYAML` library:
```python
import yaml
frontmatter = yaml.safe_load(content_between_dashes)
```

---

## 4. Validation Gaps

### 4.1 Extra Frontmatter Keys Not Enforced as Errors

**Current behavior:** Extra keys like `compatibility` in `sqlite/SKILL.md` generate only a WARNING.

**AGENTS.md rule:** "All errors must be resolved before committing"

**Problem:** A WARNING doesn't fail validation in the current script (only ERRORS fail).

**Evidence:** `sqlite` has `compatibility` key as WARNING but script returns exit code 1 only for ERRORS (line 185-190).

**Recommendation:** Make extra frontmatter keys an ERROR, not just a WARNING, per AGENTS.md policy.

---

### 4.2 Orphan openai.yaml Detection

**Issue:** Nested `agents/agents/` directory found in `agent-reviewer`:
```
skills/agent-reviewer/agents/agents/openai.yaml
```

**Risk:** Extra nested directory that is never validated or used.

**Recommendation:** Add validation to detect and report nested agent directories.

---

## 5. Operational Risks

### 5.1 skills.sh Re-indexing Delay

**Claim (AGENTS.md):** "Skills.sh re-indexes automatically within ~1 hour of push"

**Risk:** Developers may push broken skills and not discover issues until an hour later.

**Mitigation:** Local validation with `python scripts/validate_curated_skills.py` catches errors before push.

---

### 5.2 No CI/CD Validation

**Current state:** No automated checks run on push.

**Risk:** Commits with validation errors could reach main branch.

**Recommendation:** Add GitHub Actions workflow:
```yaml
- name: Validate Skills
  run: python scripts/validate_curated_skills.py
```

---

### 5.3 No Backup of eachlabs-kling-generator

The `eachlabs-kling-generator/` folder is:
- In `.gitignore` (not committed)
- Contains `.env` file (likely secrets)
- Present in working directory

**Risk:** Accidental `git clean -fd` or fresh clone loses this folder.

**Recommendation:** Either:
1. Commit the skill (with secrets removed), OR
2. Document the exclusion clearly in a `CONTRIBUTING.md`

---

## 6. Security Observations

### 6.1 Security Ecosystem Quality

The 4-skill security subsystem appears well-designed:
- `security-auditor` has comprehensive threat analysis (7 categories)
- `adaptive-guard` has 5-tier protection with learning capability
- `security-orchestrator` has 7-phase lifecycle

**Positive:** 544 lines of reference documents (command-blacklist, pii-patterns, trust-matrix, etc.)

### 6.2 Skill Chain Trust Scoring

`security-auditor` assigns 0-100 trust scores:
- Below 40: quarantined
- Above 80: default automation

**Note:** This is internal to the skill library and doesn't affect skills.sh discovery.

---

## 7. Maintenance Risks

### 7.1 Display Name Drift

**Issue:** `generate_openai_yaml.py` has hardcoded display names that could drift from actual skill content.

**Example:**
```python
"sqlite": "SQLite Omni",  # But frontmatter name is "sqlite-omni"
```

**Risk:** openai.yaml display names may not match skill content.

---

### 7.2 No Version Tagging

**Problem:** Repository has no version tags; users get latest via `npx skills add`

**Risk:** Breaking changes pushed to main affect all users immediately.

**Recommendation:** Use GitHub releases and version branches, or document that users should pin to specific commits.

---

## 8. Summary Risk Matrix

| Risk | Severity | Likelihood | Priority |
|------|----------|------------|----------|
| `sqlite` frontmatter broken | HIGH | Certain | P0 — Fix immediately |
| 16 unquoted double-quote warnings | MEDIUM | Certain | P1 — Fix all |
| ECOSYSTEM.md pattern unimplemented | MEDIUM | Certain | P2 — Implement or remove |
| Orphaned `skill-security/` folder | MEDIUM | Certain | P2 — Delete |
| Custom YAML parser limitations | MEDIUM | Possible | P2 — Replace with PyYAML |
| eachlabs-kling-generator not committed | LOW | Possible | P3 — Decide and document |
| Hardcoded script data | LOW | Possible | P3 — Make dynamic |
| No CI/CD validation | MEDIUM | Possible | P2 — Add GitHub Actions |
| Extra key is only WARNING | LOW | Certain | P3 — Make ERROR per policy |
| Nested agents/agents/ directory | LOW | Possible | P4 — Clean up |

---

## 9. Recommended Action Items

### Immediate (P0)

1. **Fix `sqlite` SKILL.md frontmatter:**
   - Rename folder `sqlite` → `sqlite-omni`, OR
   - Change frontmatter `name: sqlite-omni` → `name: sqlite`
   - Remove or move `compatibility` key to a reference file
   - Test multiline description parsing

### Short-term (P1-P2)

2. **Fix all 16 unquoted double-quote warnings** — wrap descriptions in single quotes
3. **Delete orphaned `skills/skill-security/` folder** — it was renamed
4. **Implement or remove ECOSYSTEM.md references**:
   - Option A: Create actual ECOSYSTEM.md files in domain folders
   - Option B: Remove ECOSYSTEM.md references from all skill SKILL.md files
5. **Add GitHub Actions CI/CD** — run validator on every push
6. **Replace custom YAML parser with PyYAML** — fix multiline parsing bug

### Long-term (P3-P4)

7. **Make `generate_openai_yaml.py` dynamic** — extract names from existing files
8. **Document eachlabs-kling-generator exclusion** in CONTRIBUTING.md
9. **Clean up nested `agents/agents/` directory** in agent-reviewer
10. **Add version tagging** for user pin capability
