---
name: changelog-generator
description: Commit geçmişini, PR açıklamalarını ve spec değişikliklerini analiz ederek otomatik (fakat developer-friendly) API changelog üretir. Breaking change'leri vurgular, migration örneği ekler ve yeni özellikler için net release notları yazar.
---

# Changelog Generator Protocol

This skill bridges the gap between raw git history and consumer-facing API updates. Consumers don't care about "Refactored user service;" they care about "The `/users` endpoint now returns a `profile_pic` URL."

**Core assumption:** A changelog is a communication tool, not a git dump. It must focus on the API interface, not internal implementation tweaks.

---

## 1. Input Analysis (Static)
Parse the provided text (Git commits, PR bodies, or OpenAPI diffs) and filter out internal noise.
- **Keep:** Added fields, new endpoints, deprecated endpoints, bug fixes that changed API behavior.
- **Discard:** Dependency updates, CI/CD tweaks, internal refactoring (unless it drastically improved performance).

## 2. Categorization & Formatting
Organize the update into established categories:
- **🚀 Features:** New capabilities for the consumer.
- **🛠️ Fixes:** Resolved behavior issues.
- **⚠️ Deprecations:** Warnings about endpoints/fields being sunset.
- **🚨 BREAKING CHANGES:** Red-alert items requiring consumer code updates. (Cross-reference findings with `breaking-change-detector`).

## 3. Output Generation

**Required Outputs (Must write BOTH to `docs/api-report/`):**

1. **Human-Readable Markdown (`docs/api-report/api-changelog.md`)**
```markdown
# 🌍 API Changelog

## [v1.4.0] - 2024-03-24

### 🚀 Features
- **[Orders]** Added new `POST /v1/orders/{id}/cancel` endpoint. You can now cancel orders within 30 minutes of creation.
- **[Users]** The `GET /v1/users/me` endpoint now includes a `last_login_at` timestamp.

### 🛠️ Fixes
- **[Payments]** Fixed an issue where `GET /v1/payments` would return a 500 error if the user had no payment methods. It now correctly returns an empty array `[]`.

### ⚠️ Deprecations
- **[Products]** The `category_id` field in the `/products` response is deprecated. Please use the new `categories` array instead. `category_id` will be removed in v2.0.0.
```

2. **Machine-Readable JSON (`docs/api-report/api-changelog-output.json`)**
```json
{
  "skill": "changelog-generator",
  "version": "1.4.0",
  "date": "2024-03-24",
  "changes": {
    "features": ["POST /v1/orders/{id}/cancel added", "last_login_at added to GET /v1/users/me"],
    "fixes": ["GET /v1/payments empty state fix"],
    "deprecations": ["category_id in /products response"]
  },
  "breaking_changes": []
}
```

---

## Guardrails
- **Migration Context:** If there is a breaking change or a deprecation, *always* include a 1-2 sentence instruction on what the developer should use instead.
- **Tone:** Keep it professional, concise, and focused purely on the API consumer's perspective.
