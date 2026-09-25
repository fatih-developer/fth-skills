---
name: multi-brain-debate
description: "Two-round debate protocol: independent opening positions, then challenges and rebuttals, then a verdict that answers every rebuttal. Use when two strong options clash, for high-stakes or hard-to-reverse decisions, or when the user asks to debate, steelman, or stress-test a choice."
---

# Multi-Brain Debate Protocol

Extend the multi-brain consensus with a **two-round adversarial debate**. Perspectives don't just state their case — they challenge each other. The result is a stress-tested decision where weak arguments have been exposed and strong ones reinforced.

---

## Workflow

```
1. Understand the request
2. Round 1: Independent positions (3 perspectives)
3. Round 2: Counter-arguments and rebuttals
4. Judge's verdict (consensus)
5. Produce full output with debate trail visible
```

---

## Step 1: Understand the Request

Same as base multi-brain. Ask **one** clarifying question if needed, otherwise proceed.

---

## Step 2: Round 1 — Opening Positions

Each instance presents their approach independently (same as base multi-brain):

```markdown
## 🧠 Debate — Round 1: Opening Positions

**Instance A — Creative:**
[2-3 sentences: position + rationale]

**Instance B — Pragmatic:**
[2-3 sentences: position + rationale]

**Instance C — Comprehensive:**
[2-3 sentences: position + rationale]
```

---

## Step 3: Round 2 — Challenges & Rebuttals

Each instance can now see the others' positions and must:
1. **Challenge** the weakest point of another instance's argument
2. **Defend** their own position against potential objections

```markdown
## ⚔️ Debate — Round 2: Challenges

**A challenges B:**
[1-2 sentences: specific weakness identified]

**B challenges C:**
[1-2 sentences: specific weakness identified]

**C challenges A:**
[1-2 sentences: specific weakness identified]

**Rebuttals:**
- **A responds:** [1 sentence defense or concession]
- **B responds:** [1 sentence defense or concession]
- **C responds:** [1 sentence defense or concession]
```

---

## Step 4: Judge's Verdict

After the debate, synthesize the **strongest surviving arguments**:

```markdown
## ⚖️ Verdict

**Winner:** [Which perspective's core argument survived the debate]
**Incorporated from others:** [Elements from losing arguments that strengthen the decision]
**Eliminated:** [Arguments that were successfully challenged and dropped]
```

---

## Step 5: Full Output

**Mandatory:** The final response must include both debate rounds, the verdict, and the complete deliverable. The user must see the full reasoning trail.

---

## When to Use Debate vs Base Multi-Brain

| Situation | Use |
|-----------|-----|
| High-stakes architecture decision | **Debate** |
| Choosing between competing technologies | **Debate** |
| Quick implementation question | Base multi-brain |
| Strategy with long-term consequences | **Debate** |
| Simple feature decision | Base multi-brain |
| Security-sensitive design | **Debate** |

---

## Guardrails

- **Always show both rounds** — the debate trail is the value, not just the verdict.
- Challenges must be **specific and substantive** — not generic "this might not scale."
- Rebuttals can include **concessions** — "You're right, I'll adjust my position to X."
- The verdict must explain **what was eliminated and why** — not just what won.
- Keep the total debate concise: Round 1 (2-3 sentences each), Round 2 (1-2 sentences each), Rebuttals (1 sentence each).
- **Do not force disagreement** — if all 3 genuinely align, acknowledge it and skip Round 2.

---

## References

- See `references/EXAMPLES.md` for worked debate examples.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-reasoning` — Reasoning, Planning Gates & Prompting.

**Workflows:**
- **Decision Quality Flow** (`reason-decision`, step 3 of 5): next → `@multi-brain-score` *(optional)*.
- **Naming & Positioning Flow** (`product-naming`, step 2 of 2, via `@ecosystem-product`): last step → once it passes, complete the workflow and report the outcome.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-reasoning`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
