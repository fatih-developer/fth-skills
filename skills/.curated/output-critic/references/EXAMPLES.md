# Examples

## Example 1 — Code Review

```
OUTPUT CRITIC
Type     : Code (Python)
Decision : CONDITIONAL
Score    : 6.8/10

## Criterion Scores
| Criterion | Score | Note |
|-----------|-------|------|
| Correctness | 8/10 | Core scenarios work, edge case missing |
| Readability | 7/10 | Good names, no comments |
| Security | 5/10 | Hardcoded API key at line 12 |
| Performance | 7/10 | Acceptable |
| Testability | 6/10 | Functions independent but no tests |
| **Overall** | **6.8/10** | |

## Strengths
- Meaningful, consistent function names
- Basic error handling present

## Weaknesses
- API key hardcoded in source (line 12)
- IndexError on empty list input

## Improvement Suggestions
1. Read API key from os.environ, remove from code
2. Add guard clause for empty list (before line 8)
3. Write at least 3 unit tests

## Next Step
Security issue (hardcoded key) is critical — fix that first.
```

## Example 2 — Plan Review

```
OUTPUT CRITIC
Type     : Plan / Task List
Decision : REJECT
Score    : 4.5/10

## Criterion Scores
| Criterion | Score | Note |
|-----------|-------|------|
| Completeness | 4/10 | Test and deploy steps missing |
| Atomicity | 5/10 | "Write backend" is too broad |
| Dependency accuracy | 6/10 | General order is logical |
| Verifiability | 3/10 | No "done" criteria on any step |
| Realism | 5/10 | 8 steps in 1 day is unrealistic |
| **Overall** | **4.5/10** | |

## Improvement Suggestions
1. Split "Write backend" into at least 4 substeps
2. Add "done" criteria to every step
3. Add test and deployment steps
4. Revise time estimates

## Next Step
Re-process the plan with task-decomposer, then resubmit.
```
