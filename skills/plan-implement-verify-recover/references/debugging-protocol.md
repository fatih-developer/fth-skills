# Debugging Protocol

## Establish Evidence

1. Capture the exact error, failing test, or incorrect output.
2. Determine whether the failure is reproducible.
3. Identify the smallest failing path.
4. Compare expected and observed behavior.
5. Trace the relevant data and control flow.

## Form a Hypothesis

State a testable causal hypothesis that identifies:

- The suspected faulty component.
- The mechanism producing the failure.
- Evidence expected if the hypothesis is correct.
- A check capable of disproving the hypothesis.

Do not change production code merely to see whether an unsupported guess works.

## Correct

1. Fix the cause at the narrowest appropriate boundary.
2. Avoid hiding the failure with default values, broad exception handling, or
   silent fallback.
3. Add a regression test when behavior is reproducible.
4. Re-run the original failing check.
5. Run checks for directly affected neighboring behavior.

## Stop Conditions

Stop and report a blocker when:

- The selected route's correction or replan budget is exhausted.
- The same failure persists after the same correction and no new testable
  hypothesis is available.
- Required access or credentials are unavailable.
- The failure depends on an unavailable external system.
- The required change expands product or architectural scope.
- A user-owned decision is required.
- Evidence contradicts the current plan and no bounded next hypothesis remains.
