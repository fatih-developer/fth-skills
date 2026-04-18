---
name: coolify-orchestrator
description: Expert Coolify management skill for self-hosted infrastructure. Deploy, manage, provision, and debug services, handle environment variables, and automate workflows with or without MCP.
---

# Coolify Orchestrator

A stack-aware, MCP-optional skill that orchestrates your Coolify infrastructure.

## First: Determine Operating Mode

Understand which mode you are operating in at the beginning of each session:

```
MCP_AVAILABLE = Can coolify-mcp MCP tools be called?
  Yes → MCP mode: use tools directly (references/api.md is unnecessary)
  No → API mode: use Coolify REST API via curl/bash (read references/api.md)
```

Even in MCP mode, the decision trees and playbooks in this SKILL.md are valid — MCP is just the transport layer.

**Find or ask for environment variables:**
- `COOLIFY_BASE_URL` — e.g. `https://coolify.example.com`
- `COOLIFY_ACCESS_TOKEN` — Coolify Settings → API Tokens

If these aren't in the env, ask the user. Do not ask for the second time — save it for the duration of the conversation.

---

## Scenario Detection → Playbook Routing

Match the user's request with this tree:

```
Is it about "deploy" or "build"?
  + Turborepo / monorepo / package error → [TURBO-DEPLOY]
  + Normal app deploy → [DEPLOY-VERIFY]

Is it about "down" / "unhealthy" / "error"?
  + Container/file issue (htaccess, config, .env) → [CONTAINER-EXEC]
  + API/service issue → [DEPLOY-VERIFY] (diagnose flow)

Is it about "new" / "provisioning" / "tenant"?
  → [PROVISIONING]

Is it about "env var" / "environment" / "secret"?
  → [MULTI-TENANT-ENV]

Is SSH / container terminal / exec requested?
  → [CONTAINER-EXEC]
```

Read the relevant reference file for each playbook.

---

## [TURBO-DEPLOY] Turborepo + Coolify Deploy Playbook

> Detail: `references/turborepo-deploy.md`

**When to trigger:** When a Turborepo monorepo is deployed on Coolify and the following errors are seen:
- `Cannot find module '@myapp/shared'`
- `tsconfig.json` cannot be found
- Shared package acts as if it hasn't been built
- TypeScript error in the middle of Docker build

**Quick diagnosis:**

1. Check the `COPY` order in the Dockerfile — shared packages must be built first
2. Is there a dependency pipeline in `turbo.json`?
3. Is Coolify's Docker build context correct? (monorepo root or subdirectory?)

```bash
# API mode — fetch build logs
curl -s -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/{uuid}/logs" | tail -100
```

In MCP mode: Use `application_logs(uuid)` → `deployment(action: list_for_app)` to find the last deploy.

When you identify the problem, read `references/turborepo-deploy.md` — fix patterns are there.

---

## [DEPLOY-VERIFY] Deploy → Automatically Verify Loop

> Detail: `references/deploy-verify.md`

**Objective:** Trigger deploy, verify healthy operation, diagnose if there is an error.

**Steps:**

```
1. Trigger deploy
   MCP: deploy(uuid, force_rebuild?)
   API: POST /api/v1/applications/{uuid}/start

2. Monitor deploy status (max 3 minutes, 10s intervals)
   MCP: deployment(action: get, uuid: deploy_uuid)
   API: GET /api/v1/deployments/{uuid}
   Expected: "finished" — if "failed", fetch logs

3. Application health check
   MCP: diagnose_app(uuid or domain)
   API: GET /api/v1/applications/{uuid} → status: "running:healthy"?

4. HTTP probe (For Hono/Next.js)
   curl -sf https://{domain}/health || curl -sf https://{domain}/api/health
   Successful if it returns 200.

5. If failed → analyze logs and find the root cause
```

**Bun/Hono health check endpoint assumption:**
```
GET /health → { status: "ok", uptime: X }
GET /api/health → 200 OK
```
If this endpoint does not exist, ask the user to add it.

**Deploy monitoring loop (bash):**
```bash
for i in $(seq 1 18); do
  STATUS=$(curl -s -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/deployments/$DEPLOY_UUID" | jq -r '.status')
  echo "[$i] $STATUS"
  [ "$STATUS" = "finished" ] && break
  [ "$STATUS" = "failed" ] && echo "ERROR: Deploy failed" && break
  sleep 10
done
```

---

## [PROVISIONING] New Service Provisioning

> Detail: `references/provisioning.md`

**Objective:** Set up all services from scratch for a tenant/project.

**Standard order — strictly follow this order:**

```
1. Create project (or find existing project)
2. Create environment (staging / production)
3. Create database and obtain connection credentials
4. Create application (source: Docker image / GitHub repo)
5. Set env vars (including DB_URL)
6. Deploy
7. Run [DEPLOY-VERIFY] loop
```

**Select stack template** (ask user if not specified):

| Stack | Template |
|-------|----------|
| Bun + Hono + PostgreSQL | `references/provisioning.md#bun-hono-pg` |
| Next.js + PostgreSQL + Redis | `references/provisioning.md#nextjs-pg-redis` |
| PostgreSQL only | `references/provisioning.md#db-only` |

**Pre-provisioning data collection from user:**
- Project/tenant name
- Target environment (staging/production)
- Source (Docker image tag or GitHub repo + branch)
- Domain (for Traefik)

---

## [MULTI-TENANT-ENV] Multi-Tenant Env Var Management

> Detail: `references/multi-tenant-env.md`

**Objective:** Manage env vars securely and isolatedly for multiple apps/tenants.

**Basic rules:**
1. Each tenant's env vars should go only to their app — strictly no cross-contamination
2. You must always restart after changes
3. Do not show secrets in the log — apply masking

**Update env var for single application:**
```bash
# List
curl -s -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs"

# Add/update
curl -s -X POST -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key":"DATABASE_URL","value":"...","is_multiline":false}' \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs"
```

In MCP mode: `env_vars(resource: application, action: create|update, uuid, key, value)`

**Bulk update (multiple applications):**
If MCP is present: `bulk_env_update(app_uuids: [...], key, value)` — write to all apps with a single command.
In API mode: run the `references/multi-tenant-env.md#bulk-script` script.

**Verify: isolation check**
List the env vars of each app, ensure that `DATABASE_URL` values are different.

---

## [CONTAINER-EXEC] Container Exec / SSH Fallback

> Detail: `references/container-exec.md`

**When to use:**
- When API is insufficient (file editing, config patch, log file reading)
- When `.env` / config file needs to be edited inside the container
- In-container debug (node_modules, bun cache, etc.)

**Access strategy (try in order):**

```
1. Coolify Dashboard → Service → Terminal (web UI) — easiest
2. SSH → server → docker exec — if shell access is available
3. Coolify API exec endpoint (if available) — programmatic
```

**SSH + docker exec:**
```bash
# Connect to server
ssh user@coolify-server

# Find container name
docker ps | grep <service-name>

# Enter container
docker exec -it <container-name> sh
# or if bash exists:
docker exec -it <container-name> bash
```

**File path assumptions in Coolify:**

| Service | File path |
|--------|------------|
| Bun/Node app | `/app/` or `/usr/src/app/` |
| Next.js | `/app/` |
| PostgreSQL data | `/var/lib/postgresql/data/` |

After in-container operations are completed, **always** restart the service:
```bash
# API mode
curl -X POST -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart"
```

---

## General Principles

**Token efficiency:** First use summary endpoints, if detail is needed go to single source.

**Order in case of error:**
1. Fetch logs (last 200 lines is enough)
2. Check status
3. Look at `references/` files for known error patterns
4. Ask user one clarifying question — not multiple

**Security:**
- Never show API token in log or output
- Mask env var values: `DATABASE_URL=postgres://***`
- Obtain user approval prior to destructive operations (stop_all, delete)

**Coolify API base pattern:**
```bash
curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "$COOLIFY_BASE_URL/api/v1/{endpoint}"
```

---

## Reference Files

Read the relevant file in the following cases:

| File | When |
|-------|----------|
| `references/turborepo-deploy.md` | Turborepo/monorepo build issues |
| `references/deploy-verify.md` | Deploy loop details, Bun/Hono/Next.js health check patterns |
| `references/provisioning.md` | New service provisioning templates |
| `references/multi-tenant-env.md` | Bulk env update, isolation verification |
| `references/container-exec.md` | SSH patterns, file editing, container debug |
| `references/api.md` | All Coolify REST API endpoints (if MCP unavailable) |
