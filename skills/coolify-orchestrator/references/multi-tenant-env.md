# Multi-Tenant Env Var Management

## Isolation Principle

Each tenant's application must have a completely separate env var set.
Tenant A's `DATABASE_URL` should never go to tenant B.

## List Existing Env Vars

```bash
curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" \
  | jq '.[] | {key: .key, value: .value}' \
  | sed 's/"value": "[^"]*"/"value": "***"/'  # secret masking
```

## Single Application: CRUD

### Add
```bash
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key":"MY_KEY","value":"my_value","is_multiline":false}' \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs"
```

### Update
```bash
# First find the env var UUID
ENV_ID=$(curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" \
  | jq -r '.[] | select(.key=="MY_KEY") | .uuid')

# Then update
curl -s -X PATCH \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value":"new_value"}' \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs/$ENV_ID"
```

### Delete
```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs/$ENV_ID"
```

### Apply Change (Restart)
```bash
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart"
```

---

## Bulk Update Script {#bulk-script}

Write the same env var to multiple applications (if no MCP):

```bash
#!/usr/bin/env bash
# bulk_env_update.sh
# Usage: ./bulk_env_update.sh KEY VALUE app1-uuid app2-uuid app3-uuid

KEY=$1
VALUE=$2
shift 2
APP_UUIDS=("$@")

for APP_UUID in "${APP_UUIDS[@]}"; do
  echo "→ Setting $KEY for $APP_UUID..."
  
  # Check if exists
  EXISTING_ID=$(curl -s \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" \
    | jq -r --arg key "$KEY" '.[] | select(.key==$key) | .uuid')
  
  if [ -n "$EXISTING_ID" ]; then
    # Update
    curl -s -X PATCH \
      -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"value\":\"$VALUE\"}" \
      "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs/$EXISTING_ID" > /dev/null
    echo "  ✓ Updated"
  else
    # Add new
    curl -s -X POST \
      -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"key\":\"$KEY\",\"value\":\"$VALUE\",\"is_multiline\":false}" \
      "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" > /dev/null
    echo "  ✓ Added"
  fi
done

echo ""
echo "Is restart required? (y/n)"
read -r RESTART
if [ "$RESTART" = "y" ]; then
  for APP_UUID in "${APP_UUIDS[@]}"; do
    curl -s -X POST \
      -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
      "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart" > /dev/null
    echo "↻ $APP_UUID restarted"
  done
fi
```

In MCP mode, the same operation is a single line:
```
bulk_env_update(app_uuids: ["uuid1","uuid2"], key: "MY_KEY", value: "my_value")
```

---

## Isolation Verification

Verify that all tenant applications' `DATABASE_URL`s are different:

```bash
#!/usr/bin/env bash
# isolation_check.sh
TENANT_UUIDS=("uuid1" "uuid2" "uuid3")  # tenant app UUIDs

echo "=== DATABASE_URL Isolation Check ==="
declare -A seen_urls

for APP_UUID in "${TENANT_UUIDS[@]}"; do
  APP_NAME=$(curl -s \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID" | jq -r '.name')
  
  DB_URL=$(curl -s \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs" \
    | jq -r '.[] | select(.key=="DATABASE_URL") | .value')
  
  # Get only host/dbname part from URL (password masking)
  DB_HOST=$(echo $DB_URL | sed 's|postgres://[^@]*@||' | cut -d'/' -f1)
  DB_NAME=$(echo $DB_URL | sed 's|.*/||')
  
  if [ -n "${seen_urls[$DB_URL]}" ]; then
    echo "⚠️  CONFLICT: $APP_NAME → $DB_HOST/$DB_NAME (Same as ${seen_urls[$DB_URL]}!)"
  else
    seen_urls[$DB_URL]=$APP_NAME
    echo "✓ $APP_NAME → $DB_HOST/$DB_NAME"
  fi
done
```

---

## Multiline Values (PEM keys, JSON, etc.)

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

## Post-Change Verification for Env Vars

Verify that the env var reached the application after restart:

```bash
# After application starts (when health check passes)
# Use an endpoint like /debug/env if the application has it
# If not, search logs for lines like "Connected to database"

curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/logs" \
  | jq -r '.logs[-50:][]' \
  | grep -iE "(database|connected|env|config)"
```
