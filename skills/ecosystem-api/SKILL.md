---
name: ecosystem-api
description: Comprehensive map and workflows for the API domain. Triggers when users ask to "design an API", "secure the APIs", "update endpoints", "view the API ecosystem", or want to see all available API orchestration skills.
---

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

---

## 🚀 Installation & Orchestration Instructions

As an AI Agent reading this ecosystem file, you must **actively guide** the user to install the missing skills for the selected workflow.

If the user wants to execute the **OpenAPI-First Design Flow**, you must execute or instruct the user to execute the following terminal commands:

```bash
skills install contract-first-designer
skills install api-mock-designer
skills install sdk-scaffolder
```

**Execution Rule:**
Do not attempt to perform the tasks of these skills yourself. Your job is to install them and hand off the execution to the appropriate skill, or instruct the user to trigger the newly installed skills in order.
