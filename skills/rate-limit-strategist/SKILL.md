---
name: rate-limit-strategist
description: Sliding window, token bucket veya leaky bucket stratejilerinden en uygun olanını seçer. Per-user, per-IP, per-endpoint limitleri kurgular. 429 yanıt formatı (Retry-After header dahil) tasarlayarak API'nin DDoS veya abuse ataklarından çökmesini engeller.
---

# Rate Limit Strategist Protocol

This skill designs the throttling and quota mechanisms that protect an API from noisy neighbors, accidental infinite loops in client code, and malicious abuse. It shifts the focus from "how to code it" to "what the limits should actually be."

**Core assumption:** Without rate limits, your API will eventually be DDOSed by your own front-end bug.

---

## 1. Algorithm Selection (Static)
Select the right rate-limiting algorithm based on traffic characteristics:
- **Token Bucket / Leaky Bucket:** Best for general APIs. Allows small bursts of traffic (e.g., a burst of 10 requests) but smooths out average flow.
- **Fixed Window:** Simple to implement (e.g., reset at the top of the minute), but vulnerable to edge spikes (submitting 100 requests at 00:59 and 100 at 01:00).
- **Sliding Window Log/Counter:** More accurate, prevents edge spikes. Best for strict, paid-tier APIs.

## 2. Granularity & Dimensions
Rate limits should rarely be global. Define multiple layers:
- **Layer 1: Global/IP (Infrastructure):** Prevent DDOS (e.g., 500 req/sec per IP at Cloudflare/WAF).
- **Layer 2: User Level (Application):** Prevent noisy neighbors (e.g., 100 req/min for User A, 1000 req/min for Enterprise User B).
- **Layer 3: Endpoint Level (Business Logic):** Highly restrictive on expensive endpoints (e.g., `/export-pdf` limited to 1 req/min).

## 3. Response Standardization
When a limit is hit, the application must respond gracefully, not just fail. Define standard headers to inform the client.

## 4. Output Generation

**Required Outputs (Must write BOTH to `docs/api-report/`):**

1. **Human-Readable Markdown (`docs/api-report/rate-limit-report.md`)**
```markdown
### 🛑 Rate Limiting Strategy
- **Selected Algorithm:** Token Bucket
- **Implementation Layer:** Redis-backed API Gateway Plugin.

#### ⚖️ Configured Quotas
1. **Global (IP-Based):** 300 requests per minute.
2. **Standard User (Token-Based):** 60 requests per minute.
3. **Expensive Route (`POST /generate-report`):** 5 requests per hour per User.

#### 📬 Consumer Response Design
When limits are exceeded, return `429 Too Many Requests`.
**Headers Included:**
- `X-RateLimit-Limit: 60` (Total quota)
- `X-RateLimit-Remaining: 0` (Used up)
- `X-RateLimit-Reset: 1711281600` (Unix timestamp of reset)
- `Retry-After: 45` (Seconds to wait)

**Body:**
```json
{
  "error": "quota_exceeded",
  "message": "You have exceeded your plan limit of 60 req/min. Please try again in 45 seconds.",
  "upgrade_url": "https://dashboard.com/billing"
}
```
```

2. **Machine-Readable JSON (`docs/api-report/rate-limit-output.json`)**
```json
{
  "skill": "rate-limit-strategist",
  "algorithm": "token_bucket",
  "tiers": [
    {"type": "IP", "limit": 300, "window": "1m"},
    {"type": "User", "limit": 60, "window": "1m"},
    {"type": "Endpoint", "path": "/generate-report", "limit": 5, "window": "1h"}
  ],
  "enforced_headers": ["Retry-After", "X-RateLimit-Remaining"]
}
```

---

## Guardrails
- **Header Standardization:** Remind the user that different gateways use different headers (e.g., `X-RateLimit` vs standard IETF `RateLimit`). Pick one and be consistent.
- **Distributed State:** Point out that local in-memory rate limiting fails in horizontally scaled environments. Redis, Memcached, or native Gateway limits are required.
