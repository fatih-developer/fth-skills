# Examples

## Example 1 — Ticket Creation (OpenClaw Agent)

### Scenario

> An OpenClaw agent needs to create a support ticket in a Next.js SaaS application.

### tools.json Manifest (relevant snippet)

```json
{
  "name": "create_ticket",
  "method": "POST",
  "path": "/items",
  "description": "Creates a new support ticket.",
  "input_schema": {
    "type": "object",
    "required": ["tenant_id", "type", "title"],
    "properties": {
      "tenant_id": { "type": "string" },
      "type": { "type": "string", "enum": ["ticket"] },
      "title": { "type": "string" },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "critical"]
      }
    }
  }
}
```

### Request (Agent → API)

```http
POST /v1/items
Authorization: Bearer sk_...
Idempotency-Key: uuid-123
X-Agent-Name: openclaw

{ "tenant_id": "org_1", "type": "ticket", "title": "Login broken", "priority": "high", "source": "agent" }
```

### Response

```json
{ "id": "itm_99", "type": "ticket", "title": "Login broken", "status": "open" }
```

---

## Example 2 — Safe Inbox Drop (LangChain Agent)

### Scenario

> A LangChain agent doesn't have `write:items` scope. It uses the safer Inbox/Capture API instead.

### Request (Agent → API)

```http
POST /v1/captures
Authorization: Bearer sk_...
Idempotency-Key: uuid-456

{
  "tenant_id": "org_2",
  "text": "Customer says the proposal needs revision by Friday 3 PM.",
  "suggested_type": "task",
  "source": "agent",
  "metadata": { "agent_name": "langchain-assistant", "confidence": 0.85 }
}
```

### Response

```json
{ "id": "cap_77", "status": "inbox", "created_at": "2026-03-03T10:00:00Z" }
```

### Human Review

The capture appears in the UI Inbox. A human clicks "Convert to Task" to create the real resource.

---

## Example 3 — Search (OpenAI Tool-Calling)

### Request (Agent → API)

```http
GET /v1/search?tenant_id=org_3&q=API+error&types=ticket,log&limit=10
Authorization: Bearer sk_...
```

### Response

```json
{
  "results": [
    {
      "id": "itm_1",
      "type": "ticket",
      "title": "500 error in payment service",
      "score": 0.91
    },
    {
      "id": "log_2",
      "type": "log",
      "title": "API timeout at /checkout",
      "score": 0.78
    }
  ]
}
```
