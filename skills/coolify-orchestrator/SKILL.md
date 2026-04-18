---
name: coolify-orchestrator
description: Expert Coolify management skill for self-hosted infrastructure. Deploy, manage, provision, and debug services, handle environment variables, and automate workflows with or without MCP.
---

# Coolify Orchestrator

Senin Coolify altyapını orchestrate eden, stack-aware, MCP-opsiyonel skill.

## Önce: Çalışma Modunu Belirle

Her oturumun başında hangi modda çalıştığını anla:

```
MCP_AVAILABLE = coolify-mcp MCP araçları çağrılabilir mi?
  Evet → MCP mod: araçları direkt kullan (references/api.md gereksiz)
  Hayır → API mod: curl/bash ile Coolify REST API'yi kullan (references/api.md oku)
```

MCP modunda bile bu SKILL.md'deki karar ağaçları ve playbook'lar geçerli — MCP sadece transport layer'dır.

**Çevre değişkenlerini bul veya sor:**
- `COOLIFY_BASE_URL` — örn. `https://coolify.example.com`
- `COOLIFY_ACCESS_TOKEN` — Coolify Settings → API Tokens

Eğer bunlar env'de yoksa, kullanıcıya sor. İkinci kez sorma — konuşma boyunca kaydet.

---

## Senaryo Tespiti → Playbook Yönlendirme

Kullanıcının isteğini şu ağaçla eşle:

```
"deploy" veya "build" söz konusu mu?
  + Turborepo / monorepo / paket hatası → [TURBO-DEPLOY]
  + Normal app deploy → [DEPLOY-VERIFY]

"down" / "sağlıklı değil" / "hata" söz konusu mu?
  + Container/dosya sorunu (htaccess, config, .env) → [CONTAINER-EXEC]
  + API/servis sorunu → [DEPLOY-VERIFY] (diagnose flow)

"yeni" / "provisioning" / "tenant" söz konusu mu?
  → [PROVISIONING]

"env var" / "environment" / "secret" söz konusu mu?
  → [MULTI-TENANT-ENV]

SSH / container terminal / exec isteniyor mu?
  → [CONTAINER-EXEC]
```

Her playbook için ilgili referans dosyasını oku.

---

## [TURBO-DEPLOY] Turborepo + Coolify Deploy Playbook

> Detay: `references/turborepo-deploy.md`

**Ne zaman tetikle:** Coolify'da Turborepo monorepo deploy ediliyor ve şu hatalar görülüyor:
- `Cannot find module '@myapp/shared'`
- `tsconfig.json` bulunamıyor
- Shared package build edilmemiş gibi davranıyor
- Docker build ortasında TypeScript hatası

**Hızlı teşhis:**

1. Dockerfile'da `COPY` sırasını kontrol et — shared packages önce build edilmeli
2. `turbo.json`'da dependency pipeline var mı?
3. Coolify'ın Docker build context doğru mu? (monorepo root mu, subdirectory mi?)

```bash
# API mod — build loglarını çek
curl -s -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/{uuid}/logs" | tail -100
```

MCP modunda: `application_logs(uuid)` → `deployment(action: list_for_app)` ile son deploy'u bul.

Sorunu tespit edince `references/turborepo-deploy.md`'yi oku — düzeltme pattern'leri orada.

---

## [DEPLOY-VERIFY] Deploy → Otomatik Verify Döngüsü

> Detay: `references/deploy-verify.md`

**Amaç:** Deploy tetikle, sağlıklı çalışıp çalışmadığını onayla, hata varsa diagnose et.

**Adımlar:**

```
1. Deploy tetikle
   MCP: deploy(uuid, force_rebuild?)
   API: POST /api/v1/applications/{uuid}/start

2. Deploy durumu izle (max 3 dakika, 10s aralıkla)
   MCP: deployment(action: get, uuid: deploy_uuid)
   API: GET /api/v1/deployments/{uuid}
   Beklenen: "finished" — "failed" ise logları çek

3. Uygulama health check
   MCP: diagnose_app(uuid veya domain)
   API: GET /api/v1/applications/{uuid} → status: "running:healthy"?

4. HTTP probe (Hono/Next.js için)
   curl -sf https://{domain}/health || curl -sf https://{domain}/api/health
   200 dönüyorsa başarılı.

5. Başarısız ise → logları analiz et ve temel nedeni bul
```

**Bun/Hono health check endpoint varsayımı:**
```
GET /health → { status: "ok", uptime: X }
GET /api/health → 200 OK
```
Bu endpoint yoksa kullanıcıya eklemesini öner.

**Deploy izleme döngüsü (bash):**
```bash
for i in $(seq 1 18); do
  STATUS=$(curl -s -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "$COOLIFY_BASE_URL/api/v1/deployments/$DEPLOY_UUID" | jq -r '.status')
  echo "[$i] $STATUS"
  [ "$STATUS" = "finished" ] && break
  [ "$STATUS" = "failed" ] && echo "HATA: Deploy başarısız" && break
  sleep 10
done
```

---

## [PROVISIONING] Yeni Servis Provisioning

> Detay: `references/provisioning.md`

**Amaç:** Sıfırdan bir tenant/proje için tüm servisleri ayarla.

**Standart sıra — kesinlikle bu sıraya uy:**

```
1. Proje oluştur (veya mevcut projeyi bul)
2. Environment oluştur (staging / production)
3. Database oluştur ve bağlantı bilgilerini al
4. Uygulama oluştur (kaynak: Docker image / GitHub repo)
5. Env var'ları set et (DB_URL dahil)
6. Deploy et
7. [DEPLOY-VERIFY] döngüsünü çalıştır
```

**Stack template seç** (kullanıcıya sor yoksa):

| Stack | Template |
|-------|----------|
| Bun + Hono + PostgreSQL | `references/provisioning.md#bun-hono-pg` |
| Next.js + PostgreSQL + Redis | `references/provisioning.md#nextjs-pg-redis` |
| Sadece PostgreSQL | `references/provisioning.md#db-only` |

**Provisioning öncesi kullanıcıdan al:**
- Proje/tenant adı
- Hedef environment (staging/production)
- Source (Docker image tag veya GitHub repo + branch)
- Domain (Traefik için)

---

## [MULTI-TENANT-ENV] Multi-Tenant Env Var Yönetimi

> Detay: `references/multi-tenant-env.md`

**Amaç:** Birden fazla uygulama/tenant için env var'ları güvenli ve izole şekilde yönet.

**Temel kurallar:**
1. Her tenant'ın env var'ları sadece kendi uygulamasına gitmeli — asla cross-contamination
2. Değişiklik sonrası mutlaka restart at
3. Secret'ları logda gösterme — maskeleme uygula

**Tek uygulama için env var güncelle:**
```bash
# Listele
curl -s -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs"

# Ekle/güncelle
curl -s -X POST -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key":"DATABASE_URL","value":"...","is_multiline":false}' \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/envs"
```

MCP modunda: `env_vars(resource: application, action: create|update, uuid, key, value)`

**Bulk update (birden fazla uygulama):**
MCP varsa: `bulk_env_update(app_uuids: [...], key, value)` — tek komutla tüm uygulamalara yaz.
API modunda: `references/multi-tenant-env.md#bulk-script` scriptini çalıştır.

**Verify: isolation check**
Her uygulamanın env var'larını listele, `DATABASE_URL` değerlerinin farklı olduğunu doğrula.

---

## [CONTAINER-EXEC] Container Exec / SSH Fallback

> Detay: `references/container-exec.md`

**Ne zaman kullan:**
- API yeterli olmadığında (dosya düzenleme, config patch, log dosyası okuma)
- `.env` / config dosyası container içinde düzenlenmesi gerektiğinde
- Container içi debug (node_modules, bun cache, vs.)

**Erişim stratejisi (sırayla dene):**

```
1. Coolify Dashboard → Servis → Terminal (web UI) — en kolay
2. SSH → sunucu → docker exec — shell erişimi varsa
3. Coolify API exec endpoint (varsa) — programmatic
```

**SSH + docker exec:**
```bash
# Sunucuya bağlan
ssh user@coolify-server

# Container adını bul
docker ps | grep <servis-adı>

# Container'a gir
docker exec -it <container-name> sh
# veya bash varsa:
docker exec -it <container-name> bash
```

**Coolify'da dosya yolu varsayımları:**

| Servis | Dosya yolu |
|--------|------------|
| Bun/Node app | `/app/` veya `/usr/src/app/` |
| Next.js | `/app/` |
| PostgreSQL data | `/var/lib/postgresql/data/` |

Container içi işlemler bittikten sonra **her zaman** servisi restart at:
```bash
# API mod
curl -X POST -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart"
```

---

## Genel İlkeler

**Token verimliliği:** Önce summary endpoint'leri kullan, detay gerekiyorsa tek kaynağa git.

**Hata durumunda sıra:**
1. Logları al (son 200 satır yeterli)
2. Status'u kontrol et
3. Bilinen hata pattern'leri için `references/` dosyalarına bak
4. Kullanıcıya netleştirici tek soru sor — birden fazla değil

**Güvenlik:**
- API token'ı asla logla veya çıktıda gösterme
- Env var değerlerini maskele: `DATABASE_URL=postgres://***`
- Destructive operasyonlar (stop_all, delete) öncesi kullanıcıdan onay al

**Coolify API base pattern:**
```bash
curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "$COOLIFY_BASE_URL/api/v1/{endpoint}"
```

---

## Referans Dosyaları

Şu durumlarda ilgili dosyayı oku:

| Dosya | Ne zaman |
|-------|----------|
| `references/turborepo-deploy.md` | Turborepo/monorepo build sorunları |
| `references/deploy-verify.md` | Deploy döngüsü detayları, Bun/Hono/Next.js health check pattern'leri |
| `references/provisioning.md` | Yeni servis provisioning template'leri |
| `references/multi-tenant-env.md` | Bulk env update, izolasyon verification |
| `references/container-exec.md` | SSH pattern'leri, dosya düzenleme, container debug |
| `references/api.md` | Tüm Coolify REST API endpoint'leri (MCP yoksa) |
