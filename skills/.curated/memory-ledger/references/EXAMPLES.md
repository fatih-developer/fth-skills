# Examples

## Example — Live Ledger for a Python Project

```
MEMORY LEDGER
Task        : Python REST API Rate Limiter
Started     : Step 1
Last updated: Step 4

## Goal
Build a sliding window rate limiter with FastAPI middleware and standalone
decorator support. Success criteria: 9 test scenarios pass.

## User Preferences & Constraints
- No external dependencies (pure Python)
- Must be thread-safe
- FastAPI middleware support required

## Decisions Made
| # | Decision | Rationale | Step |
|---|----------|-----------|------|
| 1 | Sliding window chosen | More predictable than token bucket | 1 |
| 2 | Per-key isolation | Users should not affect each other | 2 |
| 3 | deque used | O(1) popleft, thread-safe with lock | 2 |

## Current Status
Completed  : Algorithm choice, core class, decorator, middleware
In progress: Writing tests
Pending    : Documentation

## Failed Approaches
| Approach | Why It Failed | Step |
|----------|---------------|------|
| list usage | O(n) cleanup on every call — too slow | 2 |
| Global lock | Different keys blocking each other | 3 |

## Bugs & Fixes
| Bug | Fix | Status |
|-----|-----|--------|
| Race condition (concurrent test) | Added per-key threading.Lock | Fixed |

## Next Step
Write test_rate_limiter.py and run all 9 scenarios
```
