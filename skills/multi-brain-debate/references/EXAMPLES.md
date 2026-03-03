# Examples — Multi-Brain Debate

---

## Example: Monorepo vs Polyrepo

**Request:** "Should we use a monorepo or polyrepo for our microservices?"

```markdown
## 🧠 Debate — Round 1: Opening Positions

**Instance A — Creative:**
Use a hybrid: monorepo for shared libraries and contracts, polyrepo for
independently deployable services. Best of both worlds — shared types prevent
drift, independent repos allow team autonomy.

**Instance B — Pragmatic:**
Monorepo with Turborepo. Single source of truth, atomic cross-service changes,
unified CI. The tooling has matured enough that the old "monorepo doesn't scale"
argument no longer holds for teams under 50 engineers.

**Instance C — Comprehensive:**
Polyrepo with strict API contracts (OpenAPI/protobuf). Each team owns their
deployment pipeline entirely. Monorepos create CI bottlenecks as test suites
grow and force all teams onto the same build toolchain.

---

## ⚔️ Debate — Round 2: Challenges

**A challenges B:**
Monorepo with Turborepo still requires everyone to agree on Node.js tooling.
What about the Python ML service or the Go gateway?

**B challenges C:**
Polyrepo "strict contracts" sounds great in theory, but who enforces them?
Contract drift is the #1 cause of production incidents in polyrepo setups.

**C challenges A:**
The hybrid approach doubles the cognitive overhead — developers must understand
two different workflows. Simplicity has value.

**Rebuttals:**
- **A responds:** Fair point on complexity. Limit the mono portion to just types/contracts, keep it minimal.
- **B responds:** Use Nx instead of Turborepo for multi-language support. The polyglot concern is solvable.
- **C responds:** Contract testing (Pact) automates enforcement. Not a manual process.

---

## ⚖️ Verdict

**Winner:** Instance B (Monorepo) — core argument survived: atomic changes
and single source of truth outweigh the tooling constraints.
**Incorporated from others:** A's contract-first thinking (shared types package),
C's contract testing as a safety net.
**Eliminated:** A's hybrid (too complex), C's polyrepo (contract enforcement
is harder than claimed without dedicated investment).

---

## 📄 Report
[Full recommendation: monorepo with Nx, shared types package, contract testing,
migration plan from current setup]
```
