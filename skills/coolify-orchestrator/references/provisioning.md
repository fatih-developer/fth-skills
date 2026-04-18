# Yeni Servis Provisioning

Coolify'da sıfırdan tenant/proje oluşturma rehberi.

## Zorunlu Sıra

Sıra önemlidir — atlamayın:

```
1. Proje → 2. Environment → 3. Database → 4. Uygulama → 5. Env Vars → 6. Deploy → 7. Verify
```

Database bağlantı URL'si app oluşturulmadan önce bilinmeli çünkü env var olarak verilecek.

---

## Adım 1: Proje Oluştur

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

## Adım 2: Environment Oluştur

```bash
ENV=$(curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"project_uuid\":\"$PROJECT_UUID\",\"name\":\"production\"}" \
  "$COOLIFY_BASE_URL/api/v1/environments")

ENV_UUID=$(echo $ENV | jq -r '.uuid')
```

## Adım 3: Database Oluştur

### PostgreSQL (en yaygın)
```bash
# Server UUID'yi bul
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
# internal_db_url = aynı server içi bağlantı (daha hızlı)
# external_db_url = dışarıdan bağlantı
```

### Redis (cache/session için)
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

## Adım 4: Uygulama Oluştur

### Docker Image'dan
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

### GitHub Repo'dan
```bash
# Önce GitHub App UUID'ni bul
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

## Adım 5: Env Var'ları Set Et

```bash
# Tüm env var'ları tek seferde set et
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

## Adım 6-7: Deploy + Verify

SKILL.md'deki [DEPLOY-VERIFY] akışını çalıştır.

---

## Stack Template'leri

### Bun + Hono + PostgreSQL {#bun-hono-pg}

Minimum env var seti:
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

### Sadece PostgreSQL {#db-only}

Adım 4'ü atla. DB oluşturduktan sonra connection string'i kullanıcıya ver.

---

## Provisioning Checklist

- [ ] Proje UUID alındı
- [ ] Environment UUID alındı  
- [ ] Database oluşturuldu ve `running` durumda
- [ ] App oluşturuldu ve UUID alındı
- [ ] `DATABASE_URL` env var'ı iç URL ile set edildi
- [ ] Diğer env var'lar set edildi
- [ ] Domain/FQDN doğru ayarlandı
- [ ] Deploy tetiklendi
- [ ] Deploy `finished` durumuna geldi
- [ ] Health endpoint `200 OK` döndü
