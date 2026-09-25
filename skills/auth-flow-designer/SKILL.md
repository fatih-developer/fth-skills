---
name: auth-flow-designer
description: "Choose and design API authentication and authorization: API keys, JWT, OAuth2/OIDC, or mTLS, with token lifetimes, refresh and revocation strategy, and scope design. Use when the user asks how to authenticate an API, design login or token flows, add OAuth2 scopes, or secure machine-to-machine access."
---

# Auth Flow Designer Protocol

This skill designs the authentication and authorization strategy for an API. It prevents developers from defaulting to "Just use JWTs for everything," ensuring the right security model is applied based on the consumers and the data sensitivity.

**Core assumption:** A leaked token is inevitable. The architecture must minimize the damage through short lifespans, refresh flows, and tight scopes.

---

## 0. Context Intake

Before designing, make sure you have the inputs below. Read the previous workflow step's artifact first if it exists. Ask only for what is missing, in a single message, and state any assumption you make instead of blocking.

- Client types: browser SPA, mobile app, server-to-server, third-party integrators, AI agents.
- Identity provider in use or allowed (Auth0, Cognito, Keycloak, Supabase, custom).
- Compliance or security requirements (SOC 2, PCI, HIPAA, token revocation needs).

## 1. Flow Selection (Static)

Analyze the consumer type to pick the right strategy:
- **Server-to-Server (Internal):** `mTLS` (Mutual TLS) or service-specific short-lived `JWT` signed by an internal KMS.
- **Server-to-Server (B2B/External):** `API Keys` with IP whitelisting, or `OAuth2 Client Credentials` flow.
- **Single Page App (SPA) / Frontend:** `HttpOnly Cookies` holding the session ID or a short-lived `JWT`. NEVER store JWTs in `localStorage`.
- **Mobile App:** `OAuth2 Authorization Code Flow with PKCE`. Use a refresh token rotation strategy.

## 2. Token Lifecycle & Strategy
Define the rules of engagement:
- **Access Token:** Very short lifespan (e.g., 5-15 minutes). Contains minimal claims (`user_id`, `role`).
- **Refresh Token:** Longer lifespan (e.g., 7-30 days). Opacity is preferred (random string in DB, not a JWT).
- **Rotation:** Every time a refresh token is used, it is invalidated and a new one is issued (Refresh Token Rotation).

## 3. Scope Design (RBAC vs ABAC)
Define how permissions are enforced:
- **RBAC (Role-Based):** Standard roles (`admin`, `user`).
- **Scopes (Capability-Based):** `read:orders`, `write:profile`. Ensure scopes are attached to the token payload so the API Gateway can reject requests before they hit the microservice.

## 4. Output Generation

**Outputs.** In *file mode* — the user wants artifacts, or this skill runs as a step of an ecosystem workflow — write both files below to `docs/api-report/`. In *inline mode* — a quick question — answer in the chat and end with the JSON below as a *Handoff* block instead of creating files.

1. **Human-Readable Markdown (`docs/api-report/auth-flow-report.md`)**
```markdown
### 🔐 Authentication Architecture Plan
- **Primary Consumer:** React Native Mobile App
- **Selected Flow:** OAuth2 Authorization Code Flow (PKCE)
- **Token Strategy:** JWT Access Token + Opaque Refresh Token (Rotated)

#### 🚦 Token Configurations
- **Access Token (JWT):** Lifespan: 15 minutes. Claims: `sub` (UUID), `roles` (Array).
- **Refresh Token (Opaque):** Lifespan: 30 days. Action: Rotated on every use. Stored securely on the device encrypted enclave.

#### 🛡️ API Gateway Enforcement
The API Gateway must validate the JWT Signature and ensure `Scope: read:orders` exists before forwarding to the upstream service.
```

2. **Machine-Readable JSON (`docs/api-report/auth-flow-output.json`)**
```json
{
  "skill": "auth-flow-designer",
  "flow": "oauth2_pkce",
  "client_type": "mobile",
  "access_token": {"type": "JWT", "lifespan_min": 15},
  "refresh_token": {"type": "Opaque", "lifespan_days": 30, "rotation": true},
  "required_scopes": ["read:orders", "write:profile"]
}
```

---

## When to Skip

- The user only asks how to call an already-designed auth endpoint, or authentication is fully delegated to a managed gateway with no design choices left.

## Guardrails
- **JWT in LocalStorage:** Strictly forbid and flag this practice. Push towards `HttpOnly` cookies for web clients.
- **Revocation:** Point out that stateless JWTs cannot be instantly revoked without a blocklist check. If instant revocation is required, suggest opaque Session IDs or a Redis-backed blocklist.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-api` — API Domain.

**Workflows:**
- **Agent Connectivity Flow** (`orch-agent-connectivity`, step 2 of 3, via `@ecosystem-orchestration`): next → `@security-auditor`.
- **API Security & Scale Flow** (`api-security-scale`, step 1 of 3): next → `@rate-limit-strategist`.

**Direct handoffs:**
- `@access-policy-designer` — Authorization must also be enforced in the database (RLS).

**Handoff contract:** pass results to the next skill through `docs/api-report/auth-flow-output.json` with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-api`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
