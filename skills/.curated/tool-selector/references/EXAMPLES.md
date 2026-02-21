# Examples

## Example 1 — "Research competitors and produce an Excel report"

```
TOOL SELECTOR
Task    : Competitor analysis + Excel report
Selected: 3 tools | Total calls: 5 | Blocked: 2

## Tool Plan
| Step | Tool | Purpose | Depends On | Cached? |
|------|------|---------|------------|---------|
| 1 | Web search x3 | One search per competitor | — | Yes |
| 2 | Code execution | Structure data + compare | #1 | No |
| 3 | File write | Save Excel output | #2 | No |

## Blocked Calls
| Blocked | Reason | Alternative |
|---------|--------|-------------|
| 4th web search (general market) | #1 searches already cover this | Extract from #1 cache |
| Intermediate file save | Unnecessary, keep in memory | Only save final Excel |

## Optimization Notes
- 3 competitor searches can run in parallel
- Web search results cached for step #2
```

---

## Example 2 — "Fetch users from DB, process, send to API"

```
TOOL SELECTOR
Task    : DB -> Process -> API sync
Selected: 3 tools | Total calls: 4 | Blocked: 3

## Tool Plan
| Step | Tool | Purpose | Depends On | Cached? |
|------|------|---------|------------|---------|
| 1 | Memory | Connection config + endpoints | — | Yes |
| 2 | DB query | Fetch users (single SELECT) | #1 | Yes |
| 3 | Code execution | Transform + prepare batch | #2 | No |
| 4 | API call | Send batch (single call) | #3 | No |

## Blocked Calls
| Blocked | Reason | Alternative |
|---------|--------|-------------|
| Per-user API calls | Rate limit + slow | Use batch endpoint |
| Schema check SELECT | Already in cache | Read from #1 memory |
| Post-sync verification SELECT | API response is sufficient | Validate API response |
```
