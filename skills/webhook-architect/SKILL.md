---
name: webhook-architect
description: Architects the provider side of the webhook infrastructure. Not only sends data but designs event schemas and robust delivery mechanisms.
---

# Webhook Architect Protocol

This skill focuses on building outbound webhooks that don't fail silently and don't overwhelm the consumer. An outbound webhook system must be treated as a mission-critical distributed system.

**Core assumption:** The consumer's server *will* go down. It *will* timeout. A good webhook architecture guarantees eventual delivery without blocking the main application flow.

---

## 1. Event Payload Design (Static)
Design the JSON structure of the event that will be sent.
- **Envelope Pattern:** Wrap the actual data in a standard envelope containing routing information.
  - `event_id` (UUID for tracing/idempotency).
  - `event_type` (e.g., `order.created`, `payment.failed`).
  - `created_at` (ISO 8601 Timestamp).
  - `data` (The actual payload, kept minimal or providing a full object).

## 2. Delivery & Reliability Strategy
Define how the system handles failure:
- **Timeouts & Retries:** Implement exponential backoff (e.g., retry instantly, then 1m, 1h, 6h, 24h).
- **Dead Letter Queue (DLQ):** Where do messages go after 5 failed retries? (e.g., A database table or queue for manual introspection).
- **Idempotency:** Force the consumer to implement an idempotency check by providing a unique `event_id`. Provide clear docs on how to do this.

## 3. Security Design
A webhook without validation is an open door.
- **HMAC Signatures:** Design a system where the payload is hashed with a shared secret (`v1=sha256=...`) sent in the `X-Webhook-Signature` header.
- **Replay Attack Prevention:** Add a timestamp header (`X-Webhook-Timestamp`) and enforce a 5-minute tolerance window.

## 4. Output Generation

**Required Outputs (Must write BOTH to `docs/api-report/`):**

1. **Human-Readable Markdown (`docs/api-report/webhook-architect-report.md`)**
```markdown
### 🎣 Webhook Architecture Plan
- **Event Scope:** `user.created`, `user.deleted`
- **Security:** HMAC-SHA256 Signature in `X-MyCompany-Signature`

#### 📦 Payload Envelope Design
```json
{
  "event_id": "evt_123456789",
  "event_type": "user.created",
  "created_at": "2024-03-24T12:00:00Z",
  "data": {
    "user_id": "usr_987",
    "email": "hello@example.com"
  }
}
```

#### 🔄 Retry Policy
- Initial Timeout: 5 seconds.
- Retry 1: +1 min.
- Retry 2: +1 hour.
- Retry 3: +24 hours -> move to DLQ.
```

2. **Machine-Readable JSON (`docs/api-report/webhook-architect-output.json`)**
```json
{
  "skill": "webhook-architect",
  "events": ["user.created", "user.deleted"],
  "signature_header": "X-MyCompany-Signature",
  "retry_policy": {"initial_timeout_sec": 5, "max_retries": 3, "dlq_enabled": true}
}
```

---

## Guardrails
- **Synchronous Delivery Ban:** NEVER send webhooks inline during an HTTP request cycle. They must be offloaded to a background worker (e.g., Redis Queue, BullMQ, Celery).
- **Fat vs. Thin Payloads:** Recommend "Thin Payloads" (just sending IDs) if data privacy is critical. Warn against sending PII in webhooks unless explicitly required.
