---
name: contract-first-designer
description: "Write the OpenAPI or AsyncAPI contract before any code: resources, schemas, error format, pagination, and versioning, plus contract tests. Use when the user starts a new API, adds endpoints, needs a spec for frontend and backend to agree on, or wants to move from code-first to contract-first."
---

# Contract-First Designer Protocol

This skill enforces API design before implementation. It breaks the habit of writing controller code and auto-generating the spec from it. By designing the OpenAPI/AsyncAPI contract first, backend and frontend teams can work in parallel.

**Core assumption:** Code is cheap, contracts are expensive to change. A well-designed API contract prevents endless integration meetings.

---

## 0. Context Intake

Before designing, make sure you have the inputs below. Read the previous workflow step's artifact first if it exists. Ask only for what is missing, in a single message, and state any assumption you make instead of blocking.

- Resources and main use cases, or the feature being built.
- Protocol (from `protocol-selection-output.json` if it exists) and style conventions (naming, pagination, error format).
- Existing specs or endpoints the new contract must stay compatible with.

## 1. Specification Generation (Static)

Analyze the business requirements to output a standard API documentation format.

### REST APIs (OpenAPI 3.x)
- Define all endpoints, methods (`GET`, `POST`, etc.).
- Explicitly define standard HTTP status codes (`200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `404 Not Found`, `500 Internal Server Error`).
- Define strict Request/Response JSON schemas using `$ref` components.
- Include pagination parameters (`limit`, `cursor`/`offset`) for all collection endpoints.

### Event-Driven / WebSockets (AsyncAPI)
- Define Channels and Messages.
- Specify headers, payload shape, and correlation IDs.

## 2. Contract Testing (Pact / Schema Validation)

Instead of relying only on E2E tests, generate the scenarios required to prove the provider (backend) and consumer (frontend) honor the contract.
- Describe the expected state.
- Define what the mock provider should return.

## 3. Output Generation

**Outputs.** In *file mode* — the user wants artifacts, or this skill runs as a step of an ecosystem workflow — write both files below to `docs/api-report/`. In *inline mode* — a quick question — answer in the chat and end with the JSON below as a *Handoff* block instead of creating files.

1. **Human-Readable Markdown (`docs/api-report/contract-designer-report.md`)**
````markdown
### 📝 Contract-First Design
- **Protocol:** HTTP REST
- **Specification:** OpenAPI 3.1
- **Focus Area:** User Orders

#### 📑 OpenAPI Specification (Snippet)
```yaml
openapi: 3.1.0
info:
  title: Order API
  version: 1.0.0
paths:
  /orders:
    post:
      summary: Create a new order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderCreatePayload'
      responses:
        '201':
          description: Order created
# ...
```

#### 🛡️ Contract Testing Scenarios (Pact)
- **State:** "User is authenticated and has $50 balance"
- **Request:** `POST /orders` with valid payload.
- **Expected Response:** `201 Created` with `order_id` string.
````

2. **Machine-Readable JSON (`docs/api-report/contract-designer-output.json`)**
```json
{
  "skill": "contract-first-designer",
  "protocol": "REST",
  "endpoints": [
    {"method": "POST", "path": "/orders", "request_schema": "OrderCreatePayload", "responses": [201, 400, 401]}
  ],
  "pact_states": ["User is authenticated and has $50 balance"]
}
```

---

## When to Skip

- The user asks about a single existing endpoint's behavior, or the API is a private function call with no network boundary.

## Guardrails
- **No Ambiguous Types:** Avoid `Any` or `Object` types in definitions. Require strict typing (e.g., `string` with `format: uuid`).
- **Standardized Errors:** Use RFC 7807 Problem Details for HTTP APIs instead of custom random error schemas.
- **Security Definitions:** Ensure Authorization headers/schemes (`Bearer`, `ApiKey`) are explicitly defined in the spec components.

---

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-api` — API Domain.

**Workflows:**
- **OpenAPI-First Design Flow** (`api-design`, step 2 of 4): next → `@api-mock-designer`, `@sdk-scaffolder` *(optional)* (can run in parallel).

**Direct handoffs:**
- `@breaking-change-detector` — A previous contract version exists.

**Handoff contract:** pass results to the next skill through `docs/api-report/contract-designer-output.json` with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-api`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
