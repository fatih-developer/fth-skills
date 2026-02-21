# Examples

Worked examples demonstrating the task decomposer protocol.

---

## Example 1 — Software Project

**Request:** "Build a rate limiter in Python."

### Plan

```markdown
## Task Plan: Python Rate Limiter

**Goal:** Build a thread-safe sliding window rate limiter with decorator support.
**Total subtasks:** 5
**Execution order:** #1 -> #2 -> #3 || #4 -> #5

| # | Task | Depends On | Output | Priority |
|---|------|------------|--------|----------|
| 1 | Design the rate limiting algorithm | — | Algorithm choice + interface | Required |
| 2 | Implement SlidingWindowRateLimiter class | #1 | `rate_limiter.py` | Required |
| 3 | Add decorator wrapper | #2 | `rate_limit()` decorator | Required |
| 4 | Add custom exception | #2 | `RateLimitExceeded` class | Required |
| 5 | Write tests | #3, #4 | `test_rate_limiter.py` | Required |
```

### Execution Result

**#1 — Algorithm choice:** Sliding window with deque — O(1) amortized, thread-safe with lock.

**#2 — Implementation:**
```python
class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._store: dict[str, deque] = {}
        self._lock = threading.Lock()

    def is_allowed(self, key: str) -> tuple[bool, dict]:
        now = time.time()
        window_start = now - self.window_seconds
        with self._lock:
            q = self._store.setdefault(key, deque())
            while q and q[0] < window_start:
                q.popleft()
            if len(q) >= self.max_requests:
                return False, {"remaining": 0, "reset_in": round(q[0] - window_start, 2)}
            q.append(now)
            return True, {"remaining": self.max_requests - len(q), "reset_in": self.window_seconds}
```

**#5 — Test results:** 5/5 passed (basic limit, key isolation, window sliding, decorator, per-key decorator).

### Summary

```
Task Completed

| Subtask | Status | Output |
|---------|--------|--------|
| #1 Algorithm design | Done | Sliding window chosen |
| #2 Core class | Done | rate_limiter.py |
| #3 Decorator | Done | rate_limit() function |
| #4 Exception | Done | RateLimitExceeded class |
| #5 Tests | Done | test_rate_limiter.py (5/5) |

Files produced: rate_limiter.py, test_rate_limiter.py
```

---

## Example 2 — Research & Analysis

**Request:** "Analyze the e-commerce market and write a report."

### Plan

```markdown
## Task Plan: E-Commerce Market Analysis

**Goal:** Produce a comprehensive market analysis report.
**Total subtasks:** 5
**Execution order:** #1 || #2 || #3 -> #4 -> #5

| # | Task | Depends On | Output | Priority |
|---|------|------------|--------|----------|
| 1 | Gather market size & growth data | — | Data notes | Required |
| 2 | Research major players | — | Competitor list | Required |
| 3 | Research consumer behavior trends | — | Trend notes | Required |
| 4 | Perform SWOT analysis | #1, #2, #3 | SWOT table | Required |
| 5 | Write the full report | #4 | report.md | Required |
```

---

## Example 3 — Documentation

**Request:** "Create API documentation for my team."

### Plan

```markdown
## Task Plan: API Documentation

**Goal:** Produce complete, team-ready API docs.
**Total subtasks:** 5
**Execution order:** #1 -> #2 || #3, #4 (parallel) -> #5

| # | Task | Depends On | Output | Priority |
|---|------|------------|--------|----------|
| 1 | List all existing endpoints | — | Endpoint inventory | Required |
| 2 | Write example request/response per endpoint | #1 | Examples | Required |
| 3 | Document error codes | #1 | Error table | Required |
| 4 | Write getting started section | — | getting-started.md | Required |
| 5 | Merge everything | #2, #3, #4 | api-docs.md | Required |
```
