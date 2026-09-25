---
name: sdk-scaffolder
description: "Scaffold an idiomatic client SDK for Python, TypeScript, Go, or Kotlin from an OpenAPI spec, with retries, timeouts, pagination, and typed errors written the way a senior developer would. Use when the user needs a client library or typed SDK for an API."
---

# SDK Scaffolder Protocol

This skill focuses on Developer Experience (DX). Auto-generated clients (via standard Swagger/OpenAPI generators) are notoriously ugly, verbose, and lack domain-specific resilience. This skill generates *idiomatic* code tailored to a specific language's best practices.

**Core assumption:** If your SDK is hard to use, developers won't use your API. An SDK is a product in itself.

---

## 0. Context Intake

Before designing, make sure you have the inputs below. Read the previous workflow step's artifact first if it exists. Ask only for what is missing, in a single message, and state any assumption you make instead of blocking.

- The OpenAPI spec (file or `contract-designer-output.json`).
- Target language(s) and minimum runtime versions.
- Distribution (npm, PyPI, Go module, Maven) and authentication scheme the SDK must support.

## 1. Context & Language Analysis (Static)
Read the API OpenAPI specification and target language (e.g., Python `httpx` vs `requests`, or TypeScript `fetch` vs `axios`).

## 2. Idiomatic Design Enforcement
Generate an SDK structure that includes:
- **Resilient Core:** A base `HttpClient` that automatically handles retries (with exponential backoff) for `429` and `5xx` errors.
- **Timeouts:** A mandatory default timeout (e.g., 10s) to prevent hanging sockets.
- **Pagination Helpers:** Abstract away `limit/offset` or cursor logic into generator functions or async iterators.
- **Strong Typing:** Fully typed request/response models (e.g., Pydantic for Python, Zod for TypeScript).

## 3. Output Generation

**Outputs.** In *file mode* — the user wants artifacts, or this skill runs as a step of an ecosystem workflow — write both files below to `docs/api-report/`. In *inline mode* — a quick question — answer in the chat and end with the JSON below as a *Handoff* block instead of creating files.

1. **Human-Readable Markdown (`docs/api-report/sdk-scaffold-report.md`)**
````markdown
### 🧰 SDK Scaffolder: TypeScript/Node.js

**Architecture:** Fetch API + Native Types
**Features:** Auto-retry on 429, Typed Responses.

#### 📝 Usage Example
```typescript
import { MyApiClient } from '@myorg/api';

const client = new MyApiClient({ apiKey: 'sk_test...' });

// The iterator abstracts away pagination cursors!
for await (const order of client.orders.list()) {
  console.log(order.id);
}
```

#### 🏗️ Implementation Guidelines
1. Create a `BaseClient` that intercepts fetch calls to add the `Authorization` header and manage timeouts.
2. Group API endpoints logically into sub-classes (`client.orders.create()`, not `client.createOrder()`).
````

2. **Machine-Readable JSON (`docs/api-report/sdk-scaffold-output.json`)**
```json
{
  "skill": "sdk-scaffolder",
  "target_language": "TypeScript",
  "recommended_libraries": ["zod", "undici"],
  "features_included": ["pagination_iterators", "retry_backoff"],
  "structure_tree": ["src/", "src/index.ts", "src/client.ts", "src/resources/orders.ts"]
}
```

---

## When to Skip

- An official generator output is already maintained and the user only needs a usage example.

## Guardrails
- **No God Objects:** Do not generate a single 10,000-line `ApiClient` class containing 200 methods. Separate them by resource domains (e.g., `client.billing`, `client.users`).
- **Dependencies:** Keep third-party dependencies to an absolute minimum to reduce supply-chain risk for consumers. Prefer standard libraries (e.g., `fetch` in Node 18+).

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-api` — API Domain.

**Workflows:**
- **OpenAPI-First Design Flow** (`api-design`, step 4 of 4): last step → once it passes, complete the workflow and report the outcome.

**Handoff contract:** pass results to the next skill through `docs/api-report/sdk-scaffold-output.json` with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-api`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
