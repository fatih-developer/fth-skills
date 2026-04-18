# Deploy → Verify Döngüsü

## Tam Akış

```
trigger_deploy()
  → poll_deployment_status(max=3min, interval=10s)
    → [failed]  → fetch_logs() → analyze() → report_root_cause()
    → [success] → probe_health_endpoint()
                    → [unhealthy] → fetch_app_status() → report()
                    → [healthy]   → ✓ Done
```

## Deploy Tetikleme

### MCP Mod
```
deploy(uuid: "app-uuid", force_rebuild: false)
# force_rebuild: true → Docker layer cache'i temizle
```

### API Mod
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

# Deploy UUID'yi response'dan al
DEPLOY_UUID=$(curl ... | jq -r '.deployment_uuid')
```

## Deployment Status İzleme

### Poll Döngüsü (bash)
```bash
DEPLOY_UUID="..."
MAX_WAIT=180  # 3 dakika
INTERVAL=10
elapsed=0

while [ $elapsed -lt $MAX_WAIT ]; do
  RESPONSE=$(curl -s \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/deployments/$DEPLOY_UUID")
  
  STATUS=$(echo $RESPONSE | jq -r '.status')
  echo "[${elapsed}s] Status: $STATUS"
  
  case $STATUS in
    "finished") echo "✓ Deploy başarılı"; break ;;
    "failed")   echo "✗ Deploy başarısız"; exit 1 ;;
    "cancelled") echo "! Deploy iptal edildi"; exit 1 ;;
  esac
  
  sleep $INTERVAL
  elapsed=$((elapsed + INTERVAL))
done
```

### Deployment Log Analizi (Hata Durumunda)
```bash
# Son 200 satır — genellikle yeterli
curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/deployments/$DEPLOY_UUID/logs" \
  | jq -r '.logs[-200:][]'
```

## Health Check Probe

### Stack'e Göre Endpoint

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

# Coolify'ın container'ı başlatması için kısa bekle
sleep 5

for attempt in 1 2 3; do
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    --connect-timeout 5 --max-time 10 \
    "$DOMAIN$HEALTH_PATH")
  
  if [ "$HTTP_STATUS" -ge 200 ] && [ "$HTTP_STATUS" -lt 400 ]; then
    echo "✓ Health check başarılı (HTTP $HTTP_STATUS)"
    break
  else
    echo "Deneme $attempt: HTTP $HTTP_STATUS — 5s bekliyor..."
    sleep 5
  fi
done
```

### Hono.js Health Endpoint Şablonu
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

## Yaygın Deploy Hataları ve Teşhis

### "Port already in use"
```bash
# Container içi kontrol
docker exec -it <container> ss -tlnp | grep <port>
# Çözüm: Coolify'dan force restart
```

### "OOMKilled" — Memory yetersiz
Log'da arama: `OOMKilled` veya `Killed`
```bash
# Container memory limitini kontrol et
docker inspect <container> | jq '.[0].HostConfig.Memory'
# Coolify → Application → Resources → Memory Limit'i artır
```

### "Health check failing" — Container çalışıyor ama unhealthy
Coolify'ın kendi health check ayarlarını kontrol et:
- Application → Health Checks → Path, Interval, Retries
- Path `/health` yoksa `/` veya gerçek endpoint'i gir

### Database bağlantı hatası ilk deploy'da
İlk provisioning'de DB çalışmaya başlaması zaman alır:
```bash
# Provision sırasında DB'yi bekle
for i in $(seq 1 12); do
  DB_STATUS=$(curl -s -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/databases/$DB_UUID" | jq -r '.status')
  [ "$DB_STATUS" = "running" ] && break
  echo "DB bekliyor: $DB_STATUS ($i/12)"
  sleep 10
done
```
