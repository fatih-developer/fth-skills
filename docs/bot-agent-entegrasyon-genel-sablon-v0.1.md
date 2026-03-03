# Bot/Agent Entegrasyon Dokümanı (Genel Şablon) — v0.1

Bu doküman, herhangi bir web uygulamasını (SaaS / internal tool / ürün) dış botlar ve agent sistemleriyle (OpenAI tool-calling, LangChain, OpenClaw benzeri, custom agents vb.) entegre edebilmek için **genel bir API ve güvenlik şablonu** sunar.

Amaç: Uygulaman “bot”a dönüşmeden, botların uygulamana **güvenli şekilde bağlanıp** veri okuyup yazabilmesi.

---

## 0) Hedef Kullanım Senaryoları

Aşağıdaki senaryoların bir veya birkaçını desteklemek için tasarlanmıştır:

1) **Güvenli varsayılan:** Bot, uygulamada bir “Inbox/Capture” alanına ham girdi bırakır.  
2) **Doğrudan aksiyon:** Bot, kullanıcı adına kayıt oluşturur/günceller (task/note/ticket vb.).  
3) **Arama ve bağlama:** Bot, mevcut kayıtları arar; benzerleri bulur; ilişkilendirir.  
4) **Rutinler:** Bot, günlük/haftalık özet çıkarır; backlog temizliği önerir (opsiyonel).

---

## 1) Temel Kavramlar

### 1.1 Tenant / Workspace / Organization
Çok kiracılı (multi-tenant) yapılarda istekler bir “kapsam” içinde çalışır:
- `tenant_id` / `org_id` / `workspace_id` (hangi kavram kullanılıyorsa)

> Tüm write/read işlemleri mutlaka bu kapsam ile sınırlandırılmalıdır.

### 1.2 Kaynak (Resource) modeli
Uygulamanızın alanına göre farklı kaynaklar olabilir. Genel bir yaklaşım:
- `items` (type ile ayrışır) veya ayrı uçlar (`/tasks`, `/notes`, `/projects`, ...)

Örnek `type` enum:
- `task` | `note` | `project` | `issue` | `idea` | `prompt` | `ticket` | `doc` | ...

### 1.3 “Capture/Inbox” modeli (önerilen güvenli varsayılan)
Botların en güvenli şekilde yazabilmesi için bir “gelen kutusu” önerilir:
- Bot “ham metin” bırakır
- Uygulama kullanıcıya sunar (onay/convert)
- Böylece yanlış/zararlı yazımlar minimize olur

---

## 2) Kimlik Doğrulama ve Yetkilendirme

### 2.1 MVP: API Key (kolay başlangıç)
Header:
- `Authorization: Bearer <API_KEY>`

API key, bir kullanıcıya veya servise bağlanabilir.

### 2.2 Prod: OAuth2 (önerilen)
Üçüncü parti bot/agent sağlayıcıları ile entegrasyonda standart:
- Authorization Code + PKCE
- Access token (kısa ömür) + refresh token (opsiyonel)

### 2.3 Scope / Permission modeli (çok önemli)
API anahtarı veya token şu permission’lar ile sınırlandırılmalıdır:

Örnek scope seti:
- `read:items`
- `write:captures`
- `write:items`
- `write:links`
- `admin:audit`

> “Silme” ve “toplu değişiklik” gibi riskli işlemler ayrı scope ile ayrılmalıdır:
- `write:items:delete`
- `write:items:bulk`

---

## 3) Standart HTTP Kuralları

- Base URL: `https://<your-domain>`
- API Base path: `/v1` (öneri)
- Content-Type: `application/json`
- Timeout önerisi: 10–30s
- Rate limit önerisi: 60 req/min (token/key başına)
- Idempotency (create uçlarında): `Idempotency-Key: <uuid>`

Önerilen ek header’lar:
- `X-Tenant-Id: ...` (alternatif: query/body)
- `X-Agent-Name: openclaw|langchain|custom`
- `X-Trace-Id: ...` (log korelasyonu)
- `Idempotency-Key: ...`

---

## 4) Endpoint Şablonları (Önerilen Minimum Set)

Aşağıdaki uçlar “botların bağlanması” için çoğu projede yeterlidir.

### 4.1 Health / Meta

**GET `/v1/health`**  
200:
```json
{ "status": "ok", "version": "0.1.0" }
```

**GET `/v1/openapi.json`**  
OpenAPI spesifikasyonu (botların otomatik tool üretmesi için).

---

### 4.2 Captures (Inbox’a ham girdi bırakma)

**POST `/v1/captures`**  
Scope: `write:captures`

Request:
```json
{
  "tenant_id": "tn_123",
  "text": "Yarın 15:00 müşteri görüşmesi, notları ekle.",
  "suggested_type": "task",
  "source": "agent",
  "metadata": {
    "agent_name": "openclaw-agent",
    "trace_id": "tr_abc123",
    "confidence": 0.78
  }
}
```

201:
```json
{
  "id": "cap_789",
  "tenant_id": "tn_123",
  "text": "Yarın 15:00 müşteri görüşmesi, notları ekle.",
  "status": "inbox",
  "created_at": "2026-03-03T10:12:00Z"
}
```

**GET `/v1/captures?tenant_id=...&status=inbox&limit=50`**  
Scope: `read:items` veya `read:captures` (tercihe bağlı)

---

### 4.3 Items (Genel kaynak uçları)

**GET `/v1/items`**  
Scope: `read:items`

Örnek:
- `/v1/items?tenant_id=tn_123&type=task&status=open&limit=50`

200:
```json
{
  "items": [
    {
      "id": "itm_1",
      "type": "task",
      "title": "Teklif revizyonu",
      "content": "Müşteri geri bildirimi eklenecek",
      "status": "open",
      "priority": "medium",
      "due_at": "2026-03-04T12:00:00Z",
      "tags": ["client", "sales"],
      "created_at": "2026-03-03T10:12:00Z",
      "updated_at": "2026-03-03T10:12:00Z"
    }
  ],
  "next_cursor": null
}
```

**GET `/v1/items/{id}`**  
Scope: `read:items`

**POST `/v1/items`**  
Scope: `write:items`  
Idempotency: önerilir

Request:
```json
{
  "tenant_id": "tn_123",
  "type": "task",
  "title": "Teklif revizyonu",
  "content": "Müşteri toplantısı notlarına göre revize et",
  "status": "open",
  "priority": "high",
  "due_at": "2026-03-05T12:00:00Z",
  "tags": ["client", "urgent"],
  "source": "agent",
  "metadata": { "agent_name": "openclaw-agent", "trace_id": "tr_abc123" }
}
```

201:
```json
{ "id": "itm_99", "type": "task", "title": "Teklif revizyonu", "status": "open" }
```

**PATCH `/v1/items/{id}`**  
Scope: `write:items`

Request:
```json
{
  "tenant_id": "tn_123",
  "patch": {
    "status": "done",
    "tags": ["client", "completed"]
  }
}
```

200:
```json
{ "id": "itm_99", "status": "done", "updated_at": "2026-03-03T11:00:00Z" }
```

**DELETE `/v1/items/{id}`** (opsiyonel)  
Öneri: agent’lara default kapalı; ayrı scope ile açın.

---

### 4.4 Search (Bot entegrasyonunun “altın ucu”)

**GET `/v1/search`**  
Scope: `read:items`

Örnek:
- `/v1/search?tenant_id=tn_123&q=teklif%20revizyon&types=task,note&limit=10`

200:
```json
{
  "results": [
    { "id": "itm_99", "type": "task", "title": "Teklif revizyonu", "score": 0.84 },
    { "id": "itm_12", "type": "note", "title": "Müşteri notları", "score": 0.72 }
  ]
}
```

> MVP: SQL full-text.  
> V2: embedding/semantic search: `POST /v1/semantic-search { text, types, limit }`

---

### 4.5 Links (İlişkilendirme)

**POST `/v1/links`**  
Scope: `write:links`

Request:
```json
{
  "tenant_id": "tn_123",
  "from_id": "itm_99",
  "to_id": "itm_10",
  "relation": "belongs_to"
}
```

201:
```json
{ "id": "lnk_1", "from_id": "itm_99", "to_id": "itm_10", "relation": "belongs_to" }
```

---

### 4.6 Audit Logs (Önerilir)

**GET `/v1/audit`**  
Scope: `admin:audit`

200:
```json
{
  "events": [
    {
      "id": "aud_1",
      "at": "2026-03-03T10:12:01Z",
      "actor_type": "agent",
      "actor": "openclaw-agent",
      "action": "create_item",
      "target_id": "itm_99",
      "trace_id": "tr_abc123",
      "status": "success"
    }
  ]
}
```

---

## 5) Hata Formatı (Standartlaştırın)

Tüm hatalar aynı formatta dönsün:

```json
{
  "error": {
    "code": "insufficient_scope",
    "message": "write:items scope required",
    "details": { "required": ["write:items"] }
  }
}
```

Örnek `code` değerleri:
- `unauthorized`
- `insufficient_scope`
- `not_found`
- `validation_error`
- `rate_limited`
- `conflict`
- `internal_error`

---

## 6) Botlar için Tool Manifest (tools.json) — Şablon

Bot framework’leri için sade bir manifest örneği:

```json
{
  "name": "app-tools",
  "base_url": "https://<your-domain>/v1",
  "auth": { "type": "bearer" },
  "tools": [
    {
      "name": "create_capture",
      "method": "POST",
      "path": "/captures",
      "description": "Inbox'a ham metin bırakır (güvenli varsayılan).",
      "input_schema": {
        "type": "object",
        "required": ["tenant_id", "text"],
        "properties": {
          "tenant_id": { "type": "string" },
          "text": { "type": "string" },
          "suggested_type": { "type": "string" },
          "metadata": { "type": "object" }
        }
      }
    },
    {
      "name": "search_items",
      "method": "GET",
      "path": "/search",
      "description": "Kayıtlar içinde arama yapar.",
      "input_schema": {
        "type": "object",
        "required": ["tenant_id", "q"],
        "properties": {
          "tenant_id": { "type": "string" },
          "q": { "type": "string" },
          "types": { "type": "array", "items": { "type": "string" } },
          "limit": { "type": "integer", "default": 10 }
        }
      }
    },
    {
      "name": "create_item",
      "method": "POST",
      "path": "/items",
      "description": "Yeni kayıt oluşturur (task/note/ticket vb.).",
      "input_schema": {
        "type": "object",
        "required": ["tenant_id", "type", "title"],
        "properties": {
          "tenant_id": { "type": "string" },
          "type": { "type": "string" },
          "title": { "type": "string" },
          "content": { "type": "string" },
          "status": { "type": "string" },
          "priority": { "type": "string" },
          "due_at": { "type": "string" },
          "tags": { "type": "array", "items": { "type": "string" } },
          "metadata": { "type": "object" }
        }
      }
    },
    {
      "name": "update_item",
      "method": "PATCH",
      "path": "/items/{id}",
      "description": "Var olan kaydı günceller.",
      "input_schema": {
        "type": "object",
        "required": ["tenant_id", "id", "patch"],
        "properties": {
          "tenant_id": { "type": "string" },
          "id": { "type": "string" },
          "patch": { "type": "object" }
        }
      }
    }
  ]
}
```

---

## 7) Güvenlik ve Operasyon Checklist

Minimum öneriler:
- [ ] Auth (API key veya OAuth2) var
- [ ] Scope/permission kontrolü var
- [ ] Rate limiting var
- [ ] Idempotency (create uçlarında) var
- [ ] Audit log var
- [ ] “Delete / bulk update” ayrı scope ile korumalı
- [ ] Tool whitelist yaklaşımı (bot sadece tanımlı uçları çağırır)
- [ ] PII / hassas veri için maskeleme veya alan bazlı erişim (gerekiyorsa)

---

## 8) Uygulama İçinde Agent Kaynak Alanları (önerilen)
Her kayıt/capture için:
- `source`: `human | agent`
- `agent_name`: string
- `trace_id`: string
- `metadata`: json (opsiyonel)
- audit event referansı (opsiyonel)

---

## 9) Sonraki Adım (Opsiyonel)
Bu şablonu projenize uyarlamak için şu kararlar netleştirilir:
- Tenant alanı adı: `workspace_id` mi `tenant_id` mi?
- Kaynak modeli: tek `/items` mi, yoksa `/tasks` `/notes` ayrı mı?
- Auth: API key mi OAuth2 mi?
- Search: SQL FTS mi, embedding mi?

