# New Service Provisioning

Guide to creating a tenant/project from scratch in Coolify.

## Mandatory Sequence

The sequence is important — do not skip:

```
1. Project → 2. Environment → 3. Database → 4. Application → 5. Env Vars → 6. Deploy → 7. Verify
```

The database connection URL must be known before the app is created because it will be provided as an env var.

---

## Step 1: Create Project

### MCP
```
projects(action: create, name: "tenant-acme", description: "Acme tenant")
```

### API
```bash
PROJECT=$(curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"tenant-acme","description":"Acme tenant"}' \
  "$COOLIFY_BASE_URL/api/v1/projects")

PROJECT_UUID=$(echo $PROJECT | jq -r '.uuid')
echo "Project UUID: $PROJECT_UUID"
```

## Step 2: Create Environment

```bash
ENV=$(curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"project_uuid\":\"$PROJECT_UUID\",\"name\":\"production\"}" \
  "$COOLIFY_BASE_URL/api/v1/environments")

ENV_UUID=$(echo $ENV | jq -r '.uuid')
```

## Step 3: Create Database

### PostgreSQL (most common)
```bash
# Find Server UUID
SERVER_UUID=$(curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/servers" | jq -r '.[0].uuid')

DB=$(curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"standalone-postgresql\",
    \"name\": \"acme-db\",
    \"environment_uuid\": \"$ENV_UUID\",
    \"server_uuid\": \"$SERVER_UUID\",
    \"postgres_db\": \"acme\",
    \"postgres_user\": \"acme_user\",
    \"postgres_password\": \"$(openssl rand -base64 32 | tr -d /=+ | cut -c1-32)\"
  }" \
  "$COOLIFY_BASE_URL/api/v1/databases")

DB_UUID=$(echo $DB | jq -r '.uuid')
DB_INTERNAL_URL=$(echo $DB | jq -r '.internal_db_url')
# internal_db_url = connection within the same server (faster)
# external_db_url = external connection
```

### Redis (for cache/session)
```bash
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"standalone-redis\",
    \"name\": \"acme-redis\",
    \"environment_uuid\": \"$ENV_UUID\",
    \"server_uuid\": \"$SERVER_UUID\"
  }" \
  "$COOLIFY_BASE_URL/api/v1/databases"
```

## Step 4: Create Application

### From Docker Image
```bash
APP=$(curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"dockerfile\",
    \"name\": \"acme-api\",
    \"environment_uuid\": \"$ENV_UUID\",
    \"server_uuid\": \"$SERVER_UUID\",
    \"docker_registry_image_name\": \"myregistry.com/acme/api\",
    \"docker_registry_image_tag\": \"latest\",
    \"fqdn\": \"https://api.acme.example.com\",
    \"ports_exposes\": \"3000\"
  }" \
  "$COOLIFY_BASE_URL/api/v1/applications")

APP_UUID=$(echo $APP | jq -r '.uuid')
```

### From GitHub Repo
```bash
# First find GitHub App UUID
GITHUB_APP_UUID=$(curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/security/github-apps" | jq -r '.[0].uuid')

APP=$(curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"github-apps\",
    \"name\": \"acme-api\",
    \"environment_uuid\": \"$ENV_UUID\",
    \"server_uuid\": \"$SERVER_UUID\",
    \"github_app_uuid\": \"$GITHUB_APP_UUID\",
    \"git_repository\": \"myorg/acme-api\",
    \"git_branch\": \"main\",
    \"base_directory\": \"/\",
    \"dockerfile_location\": \"/apps/api/Dockerfile\",
    \"fqdn\": \"https://api.acme.example.com\",
    \"ports_exposes\": \"3000\"
  }" \
  "$COOLIFY_BASE_URL/api/v1/applications")
```

## Step 5: Set Env Vars

```bash
# Set all env vars at once
set_env() {
  local KEY=$1
  local VALUE=$2
  curl -s -X POST \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"key\":\"$KEY\",\"value\":\"$VALUE\",\"is_multiline\":false}" \
    "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" > /dev/null
  echo "Set: $KEY"
}

set_env "DATABASE_URL" "$DB_INTERNAL_URL"
set_env "NODE_ENV" "production"
set_env "PORT" "3000"
set_env "APP_VERSION" "1.0.0"
# Tenant-specific:
set_env "TENANT_ID" "acme"
set_env "TENANT_NAME" "Acme Corp"
```

## Step 6-7: Deploy + Verify

Run the [DEPLOY-VERIFY] flow from SKILL.md.

---

## Stack Templates

### Bun + Hono + PostgreSQL {#bun-hono-pg}

Minimum env var set:
```
DATABASE_URL=postgres://user:pass@host:5432/dbname
PORT=3000
NODE_ENV=production
LOG_LEVEL=info
```

Health check path: `/health`
Port: `3000`

### Next.js + PostgreSQL + Redis {#nextjs-pg-redis}

```
DATABASE_URL=postgres://...
REDIS_URL=redis://...
NEXTAUTH_SECRET=<random-32-char>
NEXTAUTH_URL=https://app.example.com
NEXT_PUBLIC_API_URL=https://api.example.com
NODE_ENV=production
```

Health check path: `/api/health`
Port: `3000`

### PostgreSQL only {#db-only}

Skip Step 4. After creating DB, provide the connection string to the user.

---

## Provisioning Checklist

- [ ] Project UUID obtained
- [ ] Environment UUID obtained  
- [ ] Database created and in `running` state
- [ ] App created and UUID obtained
- [ ] `DATABASE_URL` env var set with internal URL
- [ ] Other env vars set
- [ ] Domain/FQDN correctly configured
- [ ] Deploy triggered
- [ ] Deploy reached `finished` state
- [ ] Health endpoint returned `200 OK`
