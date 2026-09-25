---
name: breaking-change-detector
description: "Compare two versions of an OpenAPI, AsyncAPI, or GraphQL contract, classify every change as MAJOR, MINOR, or PATCH, and propose migration and versioning steps. Use when the user changes endpoints or schemas, plans a v2 release, or asks whether an API change will break clients."
---

# Breaking Change Detector Protocol

This skill acts as the API gatekeeper. It prevents accidental deployment of changes that would break existing mobile apps, web clients, or 3rd-party integrations by comparing API contracts offline.

**Core assumption:** Once an API is published, you no longer control the clients. Removing a field or changing its type will cause production crashes.

---

## 0. Context Intake

Before designing, make sure you have the inputs below. Read the previous workflow step's artifact first if it exists. Ask only for what is missing, in a single message, and state any assumption you make instead of blocking.

- Both contract versions (old and new), or the old one plus the proposed change.
- Who consumes the API (public, partners, internal only) and the versioning policy.
- Supported deprecation window, if any.

## 1. Specification Diff Analysis (Static)

Compare Version A (Current) with Version B (Proposed) and categorize changes based on backward compatibility logic:

### 🔴 MAJOR: Breaking Changes (Requires v2 or /v2/ route)
- Removing an endpoint or method.
- Removing a property from a response payload.
- Changing a property data type (e.g., `id` from `integer` to `uuid string`).
- Adding a *new required* field to a request payload.
- Changing authentication requirements (e.g., enforcing scopes that weren't there).

### 🟡 MINOR: Non-Breaking Additions
- Adding a *new optional* field to a request payload.
- Adding a *new property* to a response payload (properly written clients ignore unknown fields).
- Adding a new endpoint.

### 🟢 PATCH: Fixes
- Fixing typos in documentation/descriptions.
- Changing examples.

## 2. Migration Guidance
If a breaking change is detected, immediately propose an alternative backward-compatible method or generate a migration guide for the clients.

## 3. Output Generation

**Outputs.** In *file mode* — the user wants artifacts, or this skill runs as a step of an ecosystem workflow — write both files below to `docs/api-report/`. In *inline mode* — a quick question — answer in the chat and end with the JSON below as a *Handoff* block instead of creating files.

1. **Human-Readable Markdown (`docs/api-report/breaking-change-report.md`)**
```markdown
### 🚨 API Version Diff Assessment
- **Status:** FAILED / BREAKING DETECTED
- **Recommended SemVer:** MAJOR BUMP (`v1.4.0` -> `v2.0.0`)

#### 🔴 Breaking Changes
1. **Endpoint `GET /users/{id}`:** Response type of `status` changed from `boolean` to `string (enum)`. This will crash strongly-typed clients (like Swift/Kotlin).
2. **Endpoint `POST /orders`:** Added new **required** field `shipping_address`. Existing clients will start receiving `400 Bad Request`.

#### 💡 Migration / Remediation Strategy
- **Fix for POST /orders:** Make `shipping_address` optional in the database, or provide a default fallback on the server.
- **Fix for GET /users:** Create a new field `status_text` and leave `status` as a boolean, marked as *deprecated*.
```

2. **Machine-Readable JSON (`docs/api-report/breaking-change-output.json`)**
```json
{
  "skill": "breaking-change-detector",
  "has_breaking_changes": true,
  "recommended_bump": "MAJOR",
  "breaking_changes": [
    {"type": "response_type_change", "path": "/users/{id}", "field": "status", "old": "boolean", "new": "string"},
    {"type": "required_field_added", "path": "/orders", "field": "shipping_address"}
  ]
}
```

---

## When to Skip

- There is no previous version (first release) or the change is internal to a service with no external consumers.

## Guardrails
- **Ignore Order:** The order of keys in JSON or OpenAPI specs does not constitute a breaking change.
- **Query Params:** Adding a required query parameter is breaking. Adding an optional one is not.
- **Semantic Versioning Strictness:** An API bump only follows SemVer rules for the public interface, not backend logic.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-api` — API Domain.

**Workflows:**
- **API Evolution Flow** (`api-evolution`, step 1 of 2): next → `@changelog-generator`.

**Handoff contract:** pass results to the next skill through `docs/api-report/breaking-change-output.json` with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-api`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
