# 🌐 API Domain Ecosystem

Welcome to the `api` domain ecosystem. This directory contains specialized agentic skills for designing, scaling, securing, and evolving Application Programming Interfaces (REST, GraphQL, gRPC).

> **For Orchestrator Agents (`task-decomposer`, `parallel-planner`):**
> When asked to plan an API-related task, you **MUST** consult the workflows below. Do not hallucinate steps; map your plan strictly to these available skills in the order defined.

---

## 🔄 Standard Workflows & Handoffs

### 1. OpenAPI-First Design Flow
When the user asks to "design a new API", "create endpoints", or "build an API from scratch", execute these skills sequentially:

1. `@contract-first-designer` -> Designs the OpenAPI/Swagger specification or GraphQL schema.
2. `@api-mock-designer` -> Generates mock servers and fake data responses based on the contract.
3. `@sdk-scaffolder` -> Generates client SDKs or typed interfaces (e.g., TypeScript interfaces) from the contract.

### 2. API Security & Scale Flow
When the user asks to "secure the API" or "prepare the API for high traffic":

1. `@protocol-selector` -> Evaluates REST vs. GraphQL vs. gRPC needs if not yet decided.
2. `@auth-flow-designer` -> Designs OAuth2, JWT, or Session-based authentication and authorization mechanisms.
3. `@rate-limit-strategist` -> Prevents abuse by designing throttling, rate-limiting, and quota rules.

### 3. API Evolution Flow
When the user asks to "update the API", "release v2", or "change endpoints":

1. `@breaking-change-detector` -> Analyzes the new contract against the old one to flag backward-incompatible changes.
2. `@changelog-generator` -> Compiles developer-friendly release notes mapping the API changes.

### 4. Production Readiness Flow
When the user asks to "make the API production-ready" or "add webhooks":

- If webhooks/event-driven architecture is needed: use `@webhook-architect`
- If monitoring is needed: use `@api-observability-planner` to define logging, tracing, and metric alerts.

---

## 🧠 Core Philosophy
API development is contract-driven and security-first. Every skill in this domain is programmed to defend against breaking changes for API consumers and ensure robust security boundaries. Never prioritize speed over backward compatibility in a public API environment.
