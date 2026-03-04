# Examples

## Example 1 — Domain-Specific Resource Creation (E-Commerce)

### Scenario

> An OpenClaw agent needs to create a B2B order in an E-commerce application. The Discovery phase identified `orders` as a core resource.

### tools.json Manifest (relevant snippet)

```json
{
  "name": "create_order",
  "method": "POST",
  "path": "/orders",
  "description": "Creates a new B2B order in the system. Requires write:orders scope.",
  "input_schema": {
    "type": "object",
    "required": ["tenant_id", "customer_id", "items"],
    "properties": {
      "tenant_id": { "type": "string" },
      "customer_id": { "type": "string" },
      "items": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "product_id": { "type": "string" },
            "quantity": { "type": "integer" }
          }
        }
      }
    }
  }
}
```

### Request (Agent → API)

```http
POST /v1/orders
Authorization: Bearer sk_...
Idempotency-Key: uuid-123
X-Agent-Name: openclaw

{ "tenant_id": "org_1", "customer_id": "cust_89", "items": [{"product_id": "p_44", "quantity": 10}], "source": "agent" }
```

### Response

```json
{ "id": "ord_99", "status": "draft", "total": 290.0 }
```

---

---

## Example 2 — Cross-Domain Search (OpenAI Tool-Calling)

### Request (Agent → API)

```http
GET /v1/search?tenant_id=org_3&q=urgent+delay&types=invoice,ticket&limit=10
Authorization: Bearer sk_...
```

### Response

```json
{
  "results": [
    {
      "id": "inv_1",
      "type": "invoice",
      "title": "Unpaid invoice #1042 causing delay",
      "score": 0.91
    },
    {
      "id": "tic_2",
      "type": "ticket",
      "title": "Shipping delay on order 991",
      "score": 0.78
    }
  ]
}
```
