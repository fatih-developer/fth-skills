# Primitive Selection

## Choice

Use when exactly one known candidate should win.

Examples:

```text
Which support route best matches the request?
- billing
- technical
- security
- general
- no_match
```

Guidelines:
- include `no_match`/`other` when coverage is incomplete;
- do not use Choice when several labels may independently be true;
- use returned distribution/confidence for fallback policy.

## Noul

Use for one semantic proposition.

Examples:

```text
Does this passage directly help answer the query?
```

```text
Does this answer mention transaction isolation?
```

```text
Does this case require human review because evidence conflicts?
```

Guidelines:
- one proposition per judgment;
- use multiple Noul questions for overlapping labels;
- probability near 0.5 means uncertainty, not medium intensity.

## Score

Use for degree along an ordered semantic dimension.

Example:

```text
How severe is the operational impact?
1 = negligible; no user-visible effect
2 = minor; isolated inconvenience
3 = material; multiple users blocked
4 = critical; core service unavailable
```

Guidelines:
- define every level concretely;
- ensure levels are genuinely ordered;
- code applies thresholds after the Score result.

## Fan-out

If independent judgments share the same state, batch them:

```text
Choice: owning team
Score: urgency
Noul: human review
Noul: credential exposure
```

Do not batch judgments that require another judgment's answer to build their state.
