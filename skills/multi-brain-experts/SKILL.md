---
name: multi-brain-experts
description: "Replace generic perspectives with three domain experts selected per request from a role pool (security, performance, UX, cost, DX, architecture, and more), then build consensus. Use when a decision needs specialist trade-offs, or the user asks for expert opinions or a panel review."
---

# Multi-Brain Experts Protocol

Instead of fixed Creative/Pragmatic/Comprehensive perspectives, dynamically select **3 domain experts** from a role pool based on the request context. Each expert evaluates the request through their specialized lens.

---

## Workflow

```
1. Understand the request
2. Select 3 experts from the role pool
3. Each expert provides their perspective (2-3 sentences)
4. Synthesize consensus
5. Produce full output with all perspectives visible
```

---

## Step 1: Understand the Request

Identify the domain, constraints, and key decision factors. This determines which experts to activate.

---

## Step 2: Expert Selection

Choose the **3 most relevant experts** from the role pool. Selection criteria:

- **Relevance**: How directly does this role address the core problem?
- **Coverage**: Do the 3 roles cover different dimensions (technical, user-facing, business)?
- **Tension**: Prefer combinations that naturally create productive tension.

See `references/EXPERT_ROLES.md` for the full role pool and selection heuristics.

### Selection Output

Always declare the selected experts before their perspectives:

```markdown
**Selected Experts:** [Role A], [Role B], [Role C]
**Why these 3:** [One sentence explaining the selection logic]
```

---

## Step 3: Expert Perspectives

Each expert provides their analysis independently:

```markdown
## 🧠 Expert Panel

**Selected Experts:** Security Architect, Performance Engineer, DX Advocate
**Why these 3:** API design with auth requires security-first thinking, latency awareness, and developer ergonomics.

**🔒 Security Architect:**
[2-3 sentences from security perspective]

**⚡ Performance Engineer:**
[2-3 sentences from performance perspective]

**🛠️ DX Advocate:**
[2-3 sentences from developer experience perspective]
```

---

## Step 4: Consensus

Synthesize expert opinions:
- **Agreement points**: Where experts align
- **Complementary insights**: Unique contributions from each expert
- **Conflicts**: Which expert's concern takes priority and why

---

## Step 5: Full Output

**Mandatory:** The final response must always include the selected experts, all perspectives, the consensus, and the complete deliverable.

---

## Guardrails

- **Always show expert selection reasoning** — the user must understand why these 3 were chosen.
- Each expert must reason **within their domain** — no generic advice.
- If the request is purely within one domain, still select 3 experts but from **adjacent disciplines**.
- Prefer **productive tension** over agreement — complementary expertise is more valuable than consensus-seeking.
- Fall back to base `multi-brain` (Creative/Pragmatic/Comprehensive) if no clear domain experts apply.

---

## References

- See `references/EXPERT_ROLES.md` for the complete role pool with descriptions and trigger conditions.
- See `references/EXAMPLES.md` for worked examples.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-reasoning` — Reasoning, Planning Gates & Prompting.

**Workflows:**
- **Decision Quality Flow** (`reason-decision`, step 2 of 5): next → `@multi-brain-debate` *(optional)*.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-reasoning`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
