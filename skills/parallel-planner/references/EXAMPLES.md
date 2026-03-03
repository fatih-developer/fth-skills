# Examples

## Example 1 — Competitor Analysis Report

**Steps:** Research 3 competitors → Compare → Write report → Save PDF

```
PARALLEL PLANNER
Total steps: 6 | Parallel groups: 2 | Sequential steps: 2
Estimated speedup: ~60% faster

## Dependency Graph
[#1 Competitor A] || [#2 Competitor B] || [#3 Competitor C]
        |                  |                  |
              [#4 Compare]
                    |
              [#5 Write report]
                    |
              [#6 Save PDF]

## Execution Plan

### Group 1 — Parallel (3 steps)
- [ ] #1: Competitor A web research
- [ ] #2: Competitor B web research
- [ ] #3: Competitor C web research
-> All complete, then proceed to Group 2

### Group 2 — Sequential
- [ ] #4: Comparison analysis  (requires: #1, #2, #3)
- [ ] #5: Write report         (requires: #4)
- [ ] #6: Save PDF             (requires: #5)
```

---

## Example 2 — Microservice Project Setup

```
PARALLEL PLANNER
Total steps: 7 | Parallel groups: 2 | Sequential steps: 3
Estimated speedup: ~55% faster

## Execution Plan

### Group 1 — Parallel (3 steps)
- [ ] #1: auth-service/ + code
- [ ] #2: user-service/ + code
- [ ] #3: product-service/ + code
-> All complete, then proceed

### Group 2 — Sequential
- [ ] #4: API Gateway config  (requires: #1, #2, #3)

### Group 3 — Parallel (2 steps)
- [ ] #5: Dockerfiles          (requires: #4)
- [ ] #6: docker-compose.yml   (requires: #4)
-> All complete, then proceed

### Group 4 — Sequential
- [ ] #7: Integration tests    (requires: #5, #6)

## Conflict Warnings
- #5 and #6 may conflict if using same docker network name
```
