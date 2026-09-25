# Confidence Routing

Confidence guides routing; it does not prove correctness.

## Rules

1. Do not use one universal threshold across projects.
2. Calibrate thresholds on representative data.
3. Consider consequence, reversibility, and fallback cost.
4. Ignore uncertainty on unused speculative branches.
5. Several acceptable Choice alternatives can naturally spread probability.
6. Noul probability near 0.5 means yes/no uncertainty, not medium severity.

## Consequence-aware policy

### Low consequence / reversible
Examples: theme suggestion, UI route, content category.

Use a reasonable calibrated Jev decision and continue.

### Medium consequence
Examples: support escalation, model routing, content rejection.

If uncertain, use stronger reasoning or a second signal.

### High consequence
Examples: security enforcement, compliance action, account blocking, financial action.

Jev is a signal only. Deterministic policy, verified evidence, and/or human review owns the final action.

## Log

Record when possible:

```text
judgment
probabilities/confidence
selected route
fallback used
final outcome
override
```
