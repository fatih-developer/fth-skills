# Examples — Multi-Brain Score

---

## Example: State Management Choice for React App

**Request:** "Which state management should I use for a complex React dashboard?"

```markdown
## 🧠 Brainstorm (Scored)

**Instance A — Creative:** (Confidence: 5/10)
Use Jotai with derived atoms — atomic state eliminates re-render cascading and
the mental model maps naturally to a dashboard's independent widget panels.
_Confidence rationale: Jotai is excellent for this pattern but the team has
no experience with atomic state. Adoption risk is real._

**Instance B — Pragmatic:** (Confidence: 9/10)
Zustand with slices pattern. Minimal boilerplate, great TypeScript support,
and the team already knows it. Devtools integration makes debugging trivial.
_Confidence rationale: Battle-tested choice, team has shipped 2 projects with
Zustand. Low risk, high predictability._

**Instance C — Comprehensive:** (Confidence: 7/10)
TanStack Query for server state + Zustand for client state. Most dashboard
state is actually server data — treat it differently. Separate concerns prevent
the "everything in one store" anti-pattern.
_Confidence rationale: Architecturally sound but adds two libraries to learn
and maintain. Worth it if server state dominates._

---

## 📊 Confidence Analysis

| Instance | Score | Strength | Weakness |
|----------|-------|----------|----------|
| A — Creative | 5/10 | Elegant mental model | Team unfamiliarity |
| B — Pragmatic | 9/10 | Proven, team knows it | Might miss server state separation |
| C — Comprehensive | 7/10 | Clean architecture | Extra learning curve |

**Average Confidence:** 7.0/10
**Spread:** 4 points (notable disagreement)
**Highest Confidence:** Instance B

---

## ⚖️ Weighted Consensus

**Primary direction:** Zustand as the core state manager (B, 9/10).
**Modified by:** Add TanStack Query for API/server state to avoid putting
everything in Zustand (C, 7/10).
**Flagged for research:** If the team has bandwidth, evaluate Jotai for the
widget panel specifically — its atomic model could be a better fit for
independent panels (A, 5/10).

**Overall Decision Confidence:** 8/10

---

## 💻 Code
[Zustand store setup with slices, TanStack Query integration, example
dashboard widget using both, TypeScript types]
```
