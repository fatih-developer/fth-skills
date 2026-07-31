---
name: plan-implement-verify-recover
description: Execute repository code changes through risk-adaptive planning, targeted context reading, scoped implementation, verification, and a bounded evidence-driven correction loop. Use when Codex is asked to modify an existing codebase, fix a bug, implement a feature, refactor code, integrate an API, change a database, perform a migration, or make architectural or security-sensitive changes. Do not use for read-only explanations, analysis without changes, research, content writing, prompt creation, document summarization, or standalone examples that will not be applied to a repository.
---

# Plan, Implement, Verify, Recover

Apply the smallest workflow that safely completes the requested code change.

Do not expose private reasoning. Communicate only decisions, plans, risks,
blockers, verification evidence, and concise progress useful to the user.

## Inspect Project Instructions

Before editing:

1. Read applicable `AGENTS.md` and repository instructions.
2. Inspect repository status and preserve unrelated user changes.
3. Locate relevant entrypoints, implementation files, nearby patterns,
   configuration, callers, and tests.
4. Use targeted discovery; do not read the entire repository when a smaller
   context is sufficient.
5. Do not modify files during initial discovery.

Use repository-provided build, test, lint, formatting, and validation commands.
Do not invent project commands when existing instructions are available.

## Define the Change

Establish:

- A one-sentence goal.
- In-scope and out-of-scope behavior.
- Observable completion criteria.
- Primary risks and affected boundaries.

Keep this internal for small, clear changes. Present it when ambiguity, risk,
or scope makes user confirmation materially useful.

## Select One Route

### Fast

Use for clear, low-risk, localized, easily reversible changes that do not
affect public contracts, data models, authentication, authorization, security,
payments, or infrastructure.

1. Read the directly relevant implementation and nearby test or example.
2. Make the smallest correct change.
3. Run the fastest relevant validation.
4. Review the diff.
5. Report evidence.

Do not create a written plan artifact.

### Standard

Use for normal multi-file features, bug fixes, and refactoring where the
architecture remains stable.

1. Create a concise implementation plan.
2. Identify files, sequence, risks, and verification.
3. Read relevant implementation, callers, and tests.
4. Implement the plan in scoped increments.
5. Run targeted checks, then broader checks when justified.
6. Review the complete diff.
7. Report evidence and remaining limitations.

Do not add a plan file to the repository unless repository instructions, the
user, or the task explicitly requires one.

### Deep

Use for architecture, security, authentication, authorization, payments,
personal data, migrations, public API changes, difficult rollback, large
refactors, major dependencies, or high ambiguity.

1. Perform targeted architectural discovery.
2. Prepare a written plan with alternatives, tradeoffs, affected boundaries,
   rollback considerations, and a verification strategy.
3. Resolve product decisions or missing authority before implementation.
4. Implement in reviewable checkpoints.
5. Run verification appropriate to every affected risk domain.
6. Perform a fresh semantic review of the complete diff.
7. Use an independent review only when explicitly requested or when applicable
   project instructions require and permit it.
8. Report evidence, residual risks, and proof gaps.

## Run the Bounded Execution Loop

Track these internal state values:

- `route`: `fast`, `standard`, or `deep`.
- `state`: `discover`, `plan`, `implement`, `verify`, `review`, `recover`,
  `complete`, or `blocked`.
- `correction_cycles`: completed Recovery-to-Verification cycles.
- `replans`: plan replacements caused by new evidence.
- `last_failure`: latest distinct failure.
- `last_hypothesis`: latest tested causal hypothesis.
- `evidence`: compact list of checks and results.

Apply these route budgets:

| Route | Maximum correction cycles | Maximum replans |
|---|---:|---:|
| Fast | 1 | 0 |
| Standard | 3 | 1 |
| Deep | 5 | 2 |

Run this state loop:

1. `discover`: Gather only enough relevant context to act safely.
2. `plan`: Produce only the plan detail required by the selected route.
3. `implement`: Apply the smallest planned increment.
4. `verify`: Run the fastest relevant check before broader checks.
5. Move from `verify` to `review` when checks pass.
6. Move from `verify` or `review` to `recover` when evidence shows a defect.
7. In `recover`, form and test a new causal hypothesis, correct the cause,
   increment `correction_cycles`, and return to `verify`.
8. Return to `plan` and increment `replans` only when evidence invalidates the
   current plan.
9. Move from `review` to `complete` when the diff is clean and completion
   criteria have evidence.
10. Move to `blocked` when a stop condition applies.

Do not repeat an unchanged command, action, hypothesis, or fix. Treat the same
failure after the same attempted correction as no progress. Change the
hypothesis or stop.

Do not reload unchanged files unless new evidence requires it. Maintain a
compact state summary instead of restating the full history each cycle.

Stop the loop when:

- Completion criteria have sufficient evidence.
- The selected route budget is exhausted.
- No new testable hypothesis remains.
- Required access, credentials, or external availability is missing.
- New authority or a user-owned product decision is required.
- Scope materially expands or an external contract changes unexpectedly.
- Continuing could overwrite unrelated user work or make recovery unsafe.

## Apply Implementation Principles

1. Prefer the smallest safe solution.
2. Apply KISS and YAGNI before introducing abstractions.
3. Reuse established project patterns when they fit.
4. Avoid speculative code for possible future requirements.
5. Stay within the accepted user-visible and architectural scope.
6. Match nearby naming, structure, comments, and idioms.
7. Preserve backward compatibility unless the request requires otherwise.
8. Do not hide failures with silent fallbacks.
9. Make necessary fallbacks observable, bounded, and justified.
10. Do not hardcode credentials, environment values, URLs, mutable policies,
    domain limits, or repeated unexplained literals.
11. Do not create configuration or abstraction for local, stable,
    self-explanatory literals.
12. Do not overwrite or discard unrelated user changes.

Allow technical implementation details to evolve within the accepted scope.
Stop for direction when work requires new authority, expands product scope,
changes an external contract, unexpectedly changes the data model, or
introduces a material architectural decision.

## Verify

Select checks by change type and risk. Read
`references/verification-matrix.md` when the right checks are unclear or the
change affects multiple domains.

Prefer this order:

1. Syntax or formatting check.
2. Targeted test for changed behavior.
3. Module-level typecheck, lint, or test.
4. Build or broader integration checks when justified.
5. Semantic diff review.

Treat `git diff --stat` as scope evidence, not functional verification.

Never claim completion without relevant evidence. When a check cannot run,
report the exact unverified behavior, why it could not be verified, available
evidence, and the next check required.

When verification succeeds, continue to `review`. When it fails, preserve the
failure evidence and enter `recover`.

## Recover from Failure

Enter Recovery when implementation or verification produces an unexpected
failure. Read `references/debugging-protocol.md`, then:

1. Reproduce or isolate the failure.
2. Record expected and observed behavior.
3. Form a testable root-cause hypothesis.
4. Gather evidence before applying a fix.
5. Apply the smallest causal correction.
6. Add or update a regression test when appropriate.
7. Increment `correction_cycles` and return to `verify`.

Do not apply unrelated speculative fixes.

Obey the correction and replan budgets for the selected route. Stop earlier
when the loop makes no progress or any global stop condition applies.

## Report Completion

Report:

- What changed.
- Why it was the smallest suitable solution.
- Files or components affected.
- Checks executed and their results.
- Checks not executed and why.
- Remaining risks, limitations, or proof gaps.

Keep the report proportional to the change.
