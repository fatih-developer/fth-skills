---
name: claw-integration-design
description: Design and implement secure APIs and integration points for external AI bots and agents (OpenAI tool-calling, LangChain, OpenClaw). Use this skill whenever the user mentions agent integrations, tool manifests, bot API access, capture/inbox models, OAuth2 scopes for bots, webhook integrations, or designing endpoints for agentic workflows — even if they don't use the exact terms "OpenClaw" or "tool manifest". Also trigger when users ask about giving bots access to their app, securing bot writes, or designing APIs for AI-powered automation.
---

# Bot/Agent Integration Design (Claw)

This skill provides guidelines and patterns for integrating web applications (SaaS/internal tools/products) with external bots and agent systems (e.g., OpenAI tool-calling, LangChain, OpenClaw). The goal is to allow agents to securely connect, read, and write data without turning the application itself into a bot.

## Phase 1: Pre-Integration Discovery (MANDATORY)

Before designing any API endpoints or tool manifests, you **MUST** scan the host application to understand its specific domain model. Do not assume the app uses "tasks", "notes", or generic "items".

1. **Scan the Database / API:** Look at `schema.prisma`, `models/`, OpenAPI specs, or route definitions.
2. **Identify Core Entities:** What are the central resources? (e.g., in e-commerce: `orders`, `products`; in CRM: `leads`, `customers`).
3. **Select Exposure Targets:** Decide which specific entities the agent _actually needs_ access to. Do not expose the entire database.

## Core Architectural Concepts

When building agent integrations based on your discovery, implement these foundational concepts:

### 1. Multi-Tenant Context

All read/write operations MUST be scoped to a specific tenant/workspace:

- **Rule:** Always require `tenant_id`, `org_id`, or `workspace_id` in requests (via header, path, or body).

### 2. Domain-Specific Resource Model

Design endpoints that match the discovered entities exactly:

- **Do NOT** use a generic `/items` endpoint unless the application itself is a generic CMS.
- **Do:** Use specific, pluralized endpoints based on the domain (e.g., `/v1/invoices`, `/v1/leads`, `/v1/candidates`).

### 3. "Capture/Inbox" Model (Safe Default)

For the safest interaction, implementations SHOULD provide an Inbox/Capture model:

- The bot leaves raw text/JSON input in a generic "capture" area (e.g., `/v1/captures` or `/v1/drafts`).
- The human user reviews, approves, or converts this input within the application UI.
- This minimizes the risk of incorrect or harmful writes by the agent directly into production tables.

## Authentication and Authorization

### Authentication Methods

- **MVP Validation:** Use API Keys passed via the `Authorization: Bearer <API_KEY>` header.
- **Production Standard:** Use OAuth2 (Authorization Code + PKCE) for integrations with third-party agent providers.

### Scope / Permission Model (CRITICAL)

You MUST enforce a granular scope model based on the discovered resources using the `{action}:{resource}` pattern. Do not give agents root access.

**Standard Scopes (Generic Examples):**

- `read:{resource}`: Read access to a specific resource (e.g., `read:invoices`).
- `write:captures`: Access to drop draft items into the inbox.
- `write:{resource}`: Access to create/update resources (e.g., `write:leads`).
- `admin:audit`: Access to read audit logs.

**High-Risk Scopes:**

- **Rule:** Isolate riskier operations behind specific scopes, default off.
- `write:{resource}:delete`: Permission to delete items (e.g., `write:invoices:delete`).
- `write:{resource}:bulk`: Permission for bulk modifications.

## Standard HTTP Guidelines

Enforce these standards on all agent-facing endpoints:

- **Base Path:** `/v1` (e.g., `https://<domain>/v1`)
- **Content-Type:** `application/json`
- **Rate Limiting:** Implement rate limits (e.g., 60 req/min per key/token).
- **Idempotency:** Require an `Idempotency-Key` header (UUID) for all `POST` (create) endpoints.
- **Agent Traceability:** Suggest headers like `X-Agent-Name` (e.g., `openclaw`, `langchain`) and `X-Trace-Id` for log correlation.

## Standard API Endpoints

When setting up the API, implement these minimal required endpoints dynamically based on Phase 1 discovery.

### 1. Health and Meta

- `GET /v1/health`: Returns `{ "status": "ok", "version": "0.1.0" }`.
- `GET /v1/openapi.json`: Serve the OpenAPI spec so agents can auto-generate tools.

### 2. Captures (Inbox Drop)

- **Endpoint:** `POST /v1/captures` (or `/drafts`)
- **Scope:** `write:captures`
- **Payload:** Needs `tenant_id`, `text`, `suggested_type` (e.g., "lead", "invoice"), `source: "agent"`, and `metadata` (agent_name, trace_id, confidence).

### 3. Exposed Resources (CRUD)

For every entity you decided to expose in Phase 1 (e.g., `invoices`):

- **List:** `GET /v1/{resource}?tenant_id=...&status=open` (Scope: `read:{resource}`)
- **Read:** `GET /v1/{resource}/{id}` (Scope: `read:{resource}`)
- **Create:** `POST /v1/{resource}` (Scope: `write:{resource}`, require `Idempotency-Key`)
- **Update:** `PATCH /v1/{resource}/{id}` (Scope: `write:{resource}`)
- **Delete:** `DELETE /v1/{resource}/{id}` (Requires specialized scope `write:{resource}:delete`)

### 4. Search (Crucial for Agents)

- **Endpoint:** `GET /v1/search?tenant_id=...&q=...&types={resource1},{resource2}`
- **MVP:** SQL Full-Text Search (PostgreSQL `tsvector`, SQLite FTS5).
- **V2 — Semantic Search:** Use embedding models (e.g., `text-embedding-3-small` from OpenAI, or `nomic-embed-text` locally) to generate vectors, stored in a vector DB:
  - **Managed:** Pinecone, Weaviate, Qdrant Cloud
  - **Self-hosted / Postgres-native:** `pgvector` extension (lowest ops overhead for most projects)
  - **Endpoint:** `POST /v1/semantic-search { text, types, limit, threshold }`
  - **When to use V2:** When keyword search fails for paraphrased queries or conceptually similar content.

> See `references/oauth2-flow.md` for auth setup and `assets/tools-manifest-template.json` for a ready-to-use manifest.

### 5. Links (Relationships)

If the domain model is highly relational (e.g., an invoice belongs to a customer):

- **Endpoint:** `POST /v1/links`
- **Scope:** `write:links`
- **Payload:** `tenant_id`, `from_id`, `to_id`, `relation` (e.g., `belongs_to`).

### 6. Audit Logging

- **Endpoint:** `GET /v1/audit`
- **Scope:** `admin:audit`
- Keep a detailed log of actor (`agent_name`), action (e.g., `create_invoice`), target, and `trace_id`.

## Standard Error Formatting

Always return errors in this consistent format for predictability:

```json
{
  "error": {
    "code": "insufficient_scope",
    "message": "write:invoices scope required",
    "details": { "required": ["write:invoices"] }
  }
}
```

**Common codes:** `unauthorized`, `insufficient_scope`, `not_found`, `validation_error`, `rate_limited`, `conflict`, `internal_error`.

## Agent Manifest (tools.json)

When requested to build a tool manifest for an agent framework, use the ready-to-use template at:

> **`assets/tools-manifest-template.json`**

The template includes definitions for `create_capture`, `search_items`, `create_item`, `update_item`, and `create_link`. Replace `<your-domain>` with the actual API base URL.

Key manifest conventions:

- Use `"type": "bearer"` for auth
- Always include `tenant_id` as a required field in every tool's `input_schema`
- Keep `description` fields agent-friendly — they guide LLM tool selection

## Internal Data Tracking

Every record/capture created by an agent MUST trace back to its origin. Add these fields to database schemas:

- `source`: Should indicate `agent` (vs `human`).
- `agent_name`: Identifying name of the bot.
- `trace_id`: For request correlation.
- `metadata`: Flexible JSON column for arbitrary agent state/data.
