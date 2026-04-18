# Coolify REST API Referansı

MCP kurulu olmadığında doğrudan API kullanımı için.

Base URL: `$COOLIFY_BASE_URL/api/v1`
Auth: `Authorization: Bearer $COOLIFY_ACCESS_TOKEN`

## Hızlı Referans

### Genel

| İşlem | Method | Endpoint |
|-------|--------|----------|
| API version | GET | `/version` |
| Sağlık kontrolü | GET | `/healthcheck` |

### Sunucular

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/servers` |
| Detay | GET | `/servers/{uuid}` |
| Kaynaklar | GET | `/servers/{uuid}/resources` |
| Domainsler | GET | `/servers/{uuid}/domains` |
| Validate | POST | `/servers/{uuid}/validate` |

### Projeler

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/projects` |
| Detay | GET | `/projects/{uuid}` |
| Oluştur | POST | `/projects` |
| Güncelle | PATCH | `/projects/{uuid}` |
| Sil | DELETE | `/projects/{uuid}` |

### Environmentlar

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/projects/{uuid}/environments` |
| Detay | GET | `/projects/{uuid}/environments/{name}` |
| Oluştur | POST | `/environments` |
| Sil | DELETE | `/environments/{uuid}` |

### Uygulamalar

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/applications` |
| Detay | GET | `/applications/{uuid}` |
| Oluştur | POST | `/applications` |
| Güncelle | PATCH | `/applications/{uuid}` |
| Sil | DELETE | `/applications/{uuid}` |
| Loglar | GET | `/applications/{uuid}/logs` |
| Start | POST | `/applications/{uuid}/start` |
| Stop | POST | `/applications/{uuid}/stop` |
| Restart | POST | `/applications/{uuid}/restart` |
| Deploy | POST | `/applications/{uuid}/deploy` |

### Env Var'lar (Uygulama)

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/applications/{uuid}/envs` |
| Ekle | POST | `/applications/{uuid}/envs` |
| Güncelle | PATCH | `/applications/{uuid}/envs/{env_uuid}` |
| Sil | DELETE | `/applications/{uuid}/envs/{env_uuid}` |
| Toplu güncelle | PUT | `/applications/{uuid}/envs/bulk` |

### Database'ler

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/databases` |
| Detay | GET | `/databases/{uuid}` |
| Oluştur | POST | `/databases` |
| Sil | DELETE | `/databases/{uuid}` |
| Start | POST | `/databases/{uuid}/start` |
| Stop | POST | `/databases/{uuid}/stop` |
| Restart | POST | `/databases/{uuid}/restart` |

Database type değerleri: `standalone-postgresql`, `standalone-mysql`, `standalone-mariadb`,
`standalone-mongodb`, `standalone-redis`, `standalone-keydb`, `standalone-clickhouse`,
`standalone-dragonfly`

### Servisler

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/services` |
| Detay | GET | `/services/{uuid}` |
| Oluştur | POST | `/services` |
| Sil | DELETE | `/services/{uuid}` |
| Start | POST | `/services/{uuid}/start` |
| Stop | POST | `/services/{uuid}/stop` |
| Restart | POST | `/services/{uuid}/restart` |

### Deployment'lar

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/deployments` |
| Detay | GET | `/deployments/{uuid}` |
| Loglar | GET | `/deployments/{uuid}/logs` |
| İptal | POST | `/deployments/{uuid}/cancel` |
| Uygulama için listele | GET | `/applications/{uuid}/deployments` |

### Private Keys

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/security/keys` |
| Detay | GET | `/security/keys/{uuid}` |
| Oluştur | POST | `/security/keys` |
| Güncelle | PATCH | `/security/keys/{uuid}` |
| Sil | DELETE | `/security/keys/{uuid}` |

### Takımlar

| İşlem | Method | Endpoint |
|-------|--------|----------|
| Listele | GET | `/teams` |
| Detay | GET | `/teams/{id}` |
| Üyeler | GET | `/teams/{id}/members` |
| Mevcut takım | GET | `/teams/current` |

---

## Temel curl Wrapper

Tekrar yazmamak için shell fonksiyonu:

```bash
coolify() {
  local METHOD="${1:-GET}"
  local ENDPOINT="$2"
  local DATA="${3:-}"
  
  ARGS=(-s -X "$METHOD" \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    -H "Content-Type: application/json")
  
  [ -n "$DATA" ] && ARGS+=(-d "$DATA")
  
  curl "${ARGS[@]}" "$COOLIFY_BASE_URL/api/v1$ENDPOINT"
}

# Kullanım:
coolify GET /applications | jq '.[] | {uuid, name, status}'
coolify POST "/applications/$APP_UUID/restart"
coolify POST /projects '{"name":"my-project"}'
```

## Hata Kodları

| Kod | Anlam | Çözüm |
|-----|-------|-------|
| 401 | Token geçersiz | Token'ı kontrol et, yeniden üret |
| 403 | Yetersiz yetki | Token'ın yetki seviyesini kontrol et |
| 404 | Kaynak bulunamadı | UUID'yi doğrula |
| 422 | Validasyon hatası | Request body'yi kontrol et |
| 500 | Coolify server hatası | Coolify loglarını kontrol et |

## Faydalı jq Filtreleri

```bash
# Tüm uygulamaları listele (uuid + name + status)
curl ... /applications | jq '.[] | {uuid, name, status: .status}'

# Unhealthy uygulamaları bul
curl ... /applications | jq '.[] | select(.status | contains("unhealthy"))'

# Belirli isimli uygulamayı bul
curl ... /applications | jq '.[] | select(.name == "my-app")'

# DB bağlantı URL'sini al
curl ... /databases/$DB_UUID | jq '{internal: .internal_db_url, external: .external_db_url}'
```
