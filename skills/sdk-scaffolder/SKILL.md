---
name: sdk-scaffolder
description: OpenAPI spec dosyasından Python, TypeScript, Go veya Kotlin için idiomatic SDK iskeleti üretir. Auto-generated makine kodundan ziyade, retry/timeout/pagination gibi built-in özelliklere sahip, gerçek bir geliştiricinin yazacağı kalitede istemci kodu tasarlar.
---

# SDK Scaffolder Protocol

This skill focuses on Developer Experience (DX). Auto-generated clients (via standard Swagger/OpenAPI generators) are notoriously ugly, verbose, and lack domain-specific resilience. This skill generates *idiomatic* code tailored to a specific language's best practices.

**Core assumption:** If your SDK is hard to use, developers won't use your API. An SDK is a product in itself.

---

## 1. Context & Language Analysis (Static)
Read the API OpenAPI specification and target language (e.g., Python `httpx` vs `requests`, or TypeScript `fetch` vs `axios`).

## 2. Idiomatic Design Enforcement
Generate an SDK structure that includes:
- **Resilient Core:** A base `HttpClient` that automatically handles retries (with exponential backoff) for `429` and `5xx` errors.
- **Timeouts:** A mandatory default timeout (e.g., 10s) to prevent hanging sockets.
- **Pagination Helpers:** Abstract away `limit/offset` or cursor logic into generator functions or async iterators.
- **Strong Typing:** Fully typed request/response models (e.g., Pydantic for Python, Zod for TypeScript).

## 3. Output Generation

**Required Outputs (Must write BOTH to `docs/api-report/`):**

1. **Human-Readable Markdown (`docs/api-report/sdk-scaffold-report.md`)**
```markdown
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
```

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

## Guardrails
- **No God Objects:** Do not generate a single 10,000-line `ApiClient` class containing 200 methods. Separate them by resource domains (e.g., `client.billing`, `client.users`).
- **Dependencies:** Keep third-party dependencies to an absolute minimum to reduce supply-chain risk for consumers. Prefer standard libraries (e.g., `fetch` in Node 18+).
