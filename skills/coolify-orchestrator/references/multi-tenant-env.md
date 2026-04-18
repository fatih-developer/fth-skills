# Multi-Tenant Env Var Yönetimi

## İzolasyon Prensibi

Her tenant'ın uygulaması tamamen ayrı env var setine sahip olmalı.
Hiçbir zaman tenant A'nın `DATABASE_URL`'si tenant B'ye gitmemeli.

## Mevcut Env Var'ları Listele

```bash
curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" \
  | jq '.[] | {key: .key, value: .value}' \
  | sed 's/"value": "[^"]*"/"value": "***"/'  # secret maskeleme
```

## Tek Uygulama: CRUD

### Ekle
```bash
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key":"MY_KEY","value":"my_value","is_multiline":false}' \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs"
```

### Güncelle
```bash
# Önce env var UUID'sini bul
ENV_ID=$(curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" \
  | jq -r '.[] | select(.key=="MY_KEY") | .uuid')

# Sonra güncelle
curl -s -X PATCH \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value":"new_value"}' \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs/$ENV_ID"
```

### Sil
```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs/$ENV_ID"
```

### Değişikliği Uygula (Restart)
```bash
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart"
```

---

## Bulk Update Script {#bulk-script}

Birden fazla uygulamaya aynı env var'ı yaz (MCP yoksa):

```bash
#!/usr/bin/env bash
# bulk_env_update.sh
# Kullanım: ./bulk_env_update.sh KEY VALUE app1-uuid app2-uuid app3-uuid

KEY=$1
VALUE=$2
shift 2
APP_UUIDS=("$@")

for APP_UUID in "${APP_UUIDS[@]}"; do
  echo "→ $APP_UUID için $KEY ayarlanıyor..."
  
  # Mevcut var mı kontrol et
  EXISTING_ID=$(curl -s \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" \
    | jq -r --arg key "$KEY" '.[] | select(.key==$key) | .uuid')
  
  if [ -n "$EXISTING_ID" ]; then
    # Güncelle
    curl -s -X PATCH \
      -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"value\":\"$VALUE\"}" \
      "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs/$EXISTING_ID" > /dev/null
    echo "  ✓ Güncellendi"
  else
    # Yeni ekle
    curl -s -X POST \
      -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"key\":\"$KEY\",\"value\":\"$VALUE\",\"is_multiline\":false}" \
      "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" > /dev/null
    echo "  ✓ Eklendi"
  fi
done

echo ""
echo "Restart gerekli mi? (e/h)"
read -r RESTART
if [ "$RESTART" = "e" ]; then
  for APP_UUID in "${APP_UUIDS[@]}"; do
    curl -s -X POST \
      -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
      "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart" > /dev/null
    echo "↻ $APP_UUID restart edildi"
  done
fi
```

MCP modunda aynı işlem tek satır:
```
bulk_env_update(app_uuids: ["uuid1","uuid2"], key: "MY_KEY", value: "my_value")
```

---

## İzolasyon Verification

Tüm tenant uygulamalarının `DATABASE_URL`'lerinin farklı olduğunu doğrula:

```bash
#!/usr/bin/env bash
# isolation_check.sh
TENANT_UUIDS=("uuid1" "uuid2" "uuid3")  # tenant app UUID'leri

echo "=== DATABASE_URL İzolasyon Kontrolü ==="
declare -A seen_urls

for APP_UUID in "${TENANT_UUIDS[@]}"; do
  APP_NAME=$(curl -s \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID" | jq -r '.name')
  
  DB_URL=$(curl -s \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" \
    | jq -r '.[] | select(.key=="DATABASE_URL") | .value')
  
  # URL'den sadece host/dbname kısmını al (password maskeleme)
  DB_HOST=$(echo $DB_URL | sed 's|postgres://[^@]*@||' | cut -d'/' -f1)
  DB_NAME=$(echo $DB_URL | sed 's|.*/||')
  
  if [ -n "${seen_urls[$DB_URL]}" ]; then
    echo "⚠️  ÇAKIŞMA: $APP_NAME → $DB_HOST/$DB_NAME (${seen_urls[$DB_URL]} ile aynı!)"
  else
    seen_urls[$DB_URL]=$APP_NAME
    echo "✓ $APP_NAME → $DB_HOST/$DB_NAME"
  fi
done
```

---

## Multiline Değerler (PEM keys, JSON, vs.)

```bash
# Multiline: is_multiline: true
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"key\": \"PRIVATE_KEY\",
    \"value\": $(cat private.pem | jq -Rs .),
    \"is_multiline\": true
  }" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs"
```

## Env Var Değişikliği Sonrası Doğrulama

Restart sonrası env var'ın uygulamaya ulaştığını doğrula:

```bash
# Uygulama başladıktan sonra (health check geçince)
# Uygulamanın /debug/env gibi bir endpoint'i varsa kullan
# Yoksa, log'larda "Connected to database" gibi satırları ara

curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/logs" \
  | jq -r '.logs[-50:][]' \
  | grep -iE "(database|connected|env|config)"
```
