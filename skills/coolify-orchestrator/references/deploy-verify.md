# Deploy → Verify Loop

## Full Flow

```
trigger_deploy()
  → poll_deployment_status(max=3min, interval=10s)
    → [failed]  → fetch_logs() → analyze() → report_root_cause()
    → [success] → probe_health_endpoint()
                    → [unhealthy] → fetch_app_status() → report()
                    → [healthy]   → ✓ Done
```

## Triggering Deploy

### MCP Mode
```
deploy(uuid: "app-uuid", force_rebuild: false)
# force_rebuild: true → Clears Docker layer cache
```

### API Mode
```bash
# Normal deploy
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/deploy"

# Force rebuild
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"force":true}' \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/deploy"

# Fetch Deploy UUID from response
DEPLOY_UUID=$(curl ... | jq -r '.deployment_uuid')
```

## Monitoring Deployment Status

### Poll Loop (bash)
```bash
DEPLOY_UUID="..."
MAX_WAIT=180  # 3 minutes
INTERVAL=10
elapsed=0

while [ $elapsed -lt $MAX_WAIT ]; do
  RESPONSE=$(curl -s \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/deployments/$DEPLOY_UUID")
  
  STATUS=$(echo $RESPONSE | jq -r '.status')
  echo "[${elapsed}s] Status: $STATUS"
  
  case $STATUS in
    "finished") echo "✓ Deploy successful"; break ;;
    "failed")   echo "✗ Deploy failed"; exit 1 ;;
    "cancelled") echo "! Deploy cancelled"; exit 1 ;;
  esac
  
  sleep $INTERVAL
  elapsed=$((elapsed + INTERVAL))
done
```

### Deployment Log Analysis (On Error)
```bash
# Last 200 lines — usually sufficient
curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/deployments/$DEPLOY_UUID/logs" \
  | jq -r '.logs[-200:][]'
```

## Health Check Probe

### Endpoint by Stack

| Stack | Primary | Fallback |
|-------|---------|----------|
| Hono.js | `GET /health` | `GET /` |
| Next.js | `GET /api/health` | `GET /` |
| Express/Bun | `GET /health` | `GET /ping` |
| FastAPI | `GET /health` | `GET /docs` |

### Health Check Script
```bash
DOMAIN="https://myapp.example.com"
HEALTH_PATH="/health"

# Wait briefly for Coolify to start the container
sleep 5

for attempt in 1 2 3; do
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    --connect-timeout 5 --max-time 10 \
    "$DOMAIN$HEALTH_PATH")
  
  if [ "$HTTP_STATUS" -ge 200 ] && [ "$HTTP_STATUS" -lt 400 ]; then
    echo "✓ Health check successful (HTTP $HTTP_STATUS)"
    break
  else
    echo "Attempt $attempt: HTTP $HTTP_STATUS — waiting 5s..."
    sleep 5
  fi
done
```

### Hono.js Health Endpoint Template
```typescript
// src/routes/health.ts
import { Hono } from 'hono'

const health = new Hono()

health.get('/', (c) => {
  return c.json({
    status: 'ok',
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
    version: process.env.APP_VERSION ?? 'unknown',
  })
})

export default health
```

### Next.js Health Endpoint
```typescript
// app/api/health/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    uptime: process.uptime(),
  })
}
```

## Common Deploy Errors and Diagnosis

### "Port already in use"
```bash
# In-container check
docker exec -it <container> ss -tlnp | grep <port>
# Solution: Force restart from Coolify
```

### "OOMKilled" — Insufficient Memory
Regex search in log for: `OOMKilled` or `Killed`
```bash
# Check container memory limit
docker inspect <container> | jq '.[0].HostConfig.Memory'
# Increase Memory Limit via Coolify → Application → Resources
```

### "Health check failing" — Container is running but unhealthy
Check Coolify's own health check settings:
- Application → Health Checks → Path, Interval, Retries
- If path `/health` doesn't exist, enter `/` or the actual endpoint

### Database connection error on initial deploy
During initial provisioning, the DB takes time to start:
```bash
# Wait for DB during provision
for i in $(seq 1 12); do
  DB_STATUS=$(curl -s -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/databases/$DB_UUID" | jq -r '.status')
  [ "$DB_STATUS" = "running" ] && break
  echo "Waiting for DB: $DB_STATUS ($i/12)"
  sleep 10
done
```
