# Examples

## Example 1 — TimeoutError (Transient)

```
[ERROR LOG]
Step     : Fetch user data from API
Error    : requests.exceptions.Timeout: 30s exceeded
Category : Transient

Attempt 1: Immediate retry -> Timeout (35s)
Attempt 2: Wait 2s, retry -> Timeout (30s)
Attempt 3: Wait 4s, retry -> Success (2.3s)
Result   : Recovered
```

## Example 2 — ImportError (Configuration)

```
[ERROR LOG]
Step     : Process CSV with pandas
Error    : ModuleNotFoundError: No module named 'pandas'
Category : Configuration

Attempt 1: Install missing dependency -> Success
Result   : Recovered
```

## Example 3 — 403 Forbidden (Permanent)

```
[ERROR LOG]
Step     : Call premium API endpoint
Error    : 403 Forbidden: Subscription required
Category : Permanent

ERROR ESCALATION
================================
Failed step : Premium API call
Error       : 403 Forbidden — Subscription required
Category    : Permanent / External
Tried       : Direct request (1 attempt)
================================
Options:
  A) Use free endpoint (less data)
  B) Try web scraping alternative
  C) Skip this step, produce report with available data
  D) Stop the task
```
