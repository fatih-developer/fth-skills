# Examples

Three end-to-end examples demonstrating the multi-brain protocol in action.

---

## Example 1 — Report Output

**Request:** "Which cloud provider should I choose for my startup? AWS, GCP, or Azure? I need a detailed analysis."

**Flow:** 3 perspectives → Consensus → Detailed comparison report (Markdown, downloadable)

### Expected Output

```
## 🧠 Brainstorm

**Instance A — Creative:**
Consider a multi-cloud strategy from day one using Terraform abstractions.
You avoid vendor lock-in entirely and can exploit each provider's strengths.
The initial overhead pays off as you scale across regions.

**Instance B — Pragmatic:**
Start with GCP — $300k in startup credits, simpler pricing model, and
Firebase/Cloud Run reduce time-to-market. Migrate later only if needed.

**Instance C — Comprehensive:**
Evaluate total cost of ownership over 3 years including egress fees,
support tiers, and compliance certifications. AWS has the broadest
service catalog but highest complexity. Consider exit costs for each.

---

## ⚖️ Consensus
Start with GCP for speed and credits (B), but design cloud-agnostic
abstractions at the infrastructure layer (A). Use C's TCO framework
to plan a 12-month cost review checkpoint.

---

## 📄 Report
[Full comparison report: cost analysis, ecosystem, startup credits,
lock-in risks, recommendation with rationale, next steps]
```

---

## Example 2 — Code Output

**Request:** "Write a REST API rate limiter in Python. What approach should I use?"

**Flow:** 3 perspectives (token bucket vs. sliding window vs. fixed window) → Consensus → Working Python code

### Expected Output

```
## 🧠 Brainstorm

**Instance A — Creative:**
Use a sliding window with sorted sets for distributed rate limiting.
Sub-millisecond lookups and natural decay without timer resets.

**Instance B — Pragmatic:**
Token bucket with in-memory dict — simple, no external dependencies,
works for single-instance APIs. Add a distributed store later if you scale.

**Instance C — Comprehensive:**
Fixed window is easiest to reason about and monitor, but has burst-edge
issues. Combine with a short cooldown to prevent boundary attacks.

---

## ⚖️ Consensus
Token bucket (B) for the initial implementation — no dependencies, easy
to test. Structure the code so the storage backend can be swapped to
a distributed store (A) without changing the algorithm interface.

---

## 💻 Code
[Complete Python implementation: TokenBucket class, decorator for
Flask/FastAPI, unit tests, comments explaining design choices]
```

---

## Example 3 — Brief Summary Output

**Request:** "React Native or Flutter? Quick answer."

**Flow:** 3 perspectives (brief) → Consensus → Single paragraph

### Expected Output

```
## 🧠 Brainstorm

**Instance A — Creative:**
Flutter with Dart — hot reload is faster, Skia rendering gives pixel-perfect
control, and the widget system enables truly custom UIs.

**Instance B — Pragmatic:**
React Native if your team knows JavaScript. Hiring is easier, ecosystem is
larger, and Expo simplifies 80% of use cases.

**Instance C — Comprehensive:**
Consider long-term: Flutter has stronger momentum and Google backing, but
React Native's bridge-less architecture (New Architecture) closes the
performance gap. Evaluate based on team skills, not hype.

---

## ⚖️ Consensus
Team skills are the deciding factor (B + C).

---

## ✅ Answer
If your team already knows JavaScript/React, go with React Native — the
ecosystem is mature, hiring is straightforward, and the New Architecture
eliminates the old performance concerns. If starting fresh with no JS
background, Flutter offers a more cohesive developer experience. Pick
based on your existing talent, not framework benchmarks.
```
