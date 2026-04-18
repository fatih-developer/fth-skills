# Container Exec / SSH Fallback

## Ne Zaman Kullan

Coolify API'nin yetersiz kaldığı durumlar:
- Container içindeki bir dosyayı düzenlemek (config, .env, cert)
- Uygulama loglarını dosya olarak okumak (stdout değil disk logu)
- Bun/node_modules cache temizliği
- Database migration'ı manuel çalıştırmak
- Container içi process debug

## Erişim Stratejisi (Sırayla Dene)

### Strateji 1: Coolify Web Terminal (MCP'siz, en kolay)

Coolify Dashboard → Application/Service → "Terminal" sekmesi → container seç → komut gir.

Bu yeterli değilse veya otomasyona ihtiyaç varsa Strateji 2'ye geç.

### Strateji 2: SSH + Docker Exec

```bash
# 1. Sunucuya bağlan
ssh -i ~/.ssh/coolify_key user@coolify-server-ip

# 2. Çalışan container'ları listele
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 3. İlgili container'ı bul (servis adına göre)
docker ps | grep <servis-adı>

# 4. Container'a gir
docker exec -it <container-name> sh
# Bash varsa:
docker exec -it <container-name> bash
# Bun container'ı için:
docker exec -it <container-name> /bin/sh
```

### Container adı nasıl bulunur?

Coolify, container adlarını genellikle şöyle üretir:
- `<proje-adı>-<servis-adı>-1`
- `coolify-<uuid>-<servis>-1`

```bash
# UUID ile ara
docker ps | grep <coolify-app-uuid>

# Servis adıyla ara
docker ps | grep -i "acme-api"
```

---

## Yaygın Container İçi İşlemler

### Dosya Görüntüleme ve Düzenleme

```bash
# Config dosyasını oku
docker exec <container> cat /app/.env

# Dosyayı düzenle (vi ile)
docker exec -it <container> vi /app/config.json

# Sed ile satır değiştir (interaktif session gerektirmez)
docker exec <container> \
  sed -i 's/OLD_VALUE/NEW_VALUE/g' /app/config.json
```

### Bun Cache Temizliği

```bash
docker exec <container> bun pm cache rm

# node_modules'ü sil ve yeniden yükle
docker exec <container> sh -c "rm -rf node_modules && bun install"
```

### Database Migration

```bash
# Drizzle migration
docker exec <container> bunx drizzle-kit push

# Veya migration scripti
docker exec <container> bun run db:migrate
```

### Log Dosyası Okuma

```bash
# Container log (stdout/stderr)
docker logs <container> --tail 200 -f

# Disk üzerindeki log dosyası
docker exec <container> tail -f /var/log/app/error.log
```

### Process ve Kaynak Kontrolü

```bash
# CPU/Memory kullanımı
docker stats <container> --no-stream

# Container içi process'ler
docker exec <container> ps aux

# Port dinleme kontrolü
docker exec <container> ss -tlnp
```

---

## Coolify Bun/Node Uygulaması: Dosya Yolları

| İçerik | Yol |
|--------|-----|
| Uygulama kodu | `/app/` |
| node_modules | `/app/node_modules/` |
| .env dosyası | `/app/.env` (varsa) |
| Bun binary | `/usr/local/bin/bun` |
| Build output | `/app/dist/` |

## Coolify Next.js: Dosya Yolları

| İçerik | Yol |
|--------|-----|
| Uygulama | `/app/` |
| .next build | `/app/.next/` |
| Static dosyalar | `/app/public/` |

---

## Container Dışından Dosya Kopyalama

```bash
# Container'dan sunucuya kopyala
docker cp <container>:/app/config.json /tmp/config.json

# Düzenle
nano /tmp/config.json

# Geri kopyala
docker cp /tmp/config.json <container>:/app/config.json

# Restart gerekli değilse uygulama reload yapabilir
# Gerekirse:
docker restart <container>
# veya Coolify API üzerinden:
curl -X POST -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart"
```

---

## Sunucuya SSH Erişimi Yoksa

Coolify'ın API'si üzerinden bazı işlemler yapılabilir:

```bash
# Uygulama logları (stdout)
curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/logs?lines=500"

# Servis restart
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart"
```

Dosya düzenleme için SSH şart. SSH erişimi yoksa:
1. Kullanıcıya Coolify web terminal'ini kullanmasını söyle
2. Veya env var üzerinden config geç (dosya yerine environment-based config)

---

## İşlem Sonrası

Container içi değişiklikten sonra kontrol listesi:

```
[ ] Değişiklik doğru uygulandı (cat ile verify et)
[ ] Servis restart edildi (gerekiyorsa)
[ ] Health check geçti
[ ] Log'da hata yok
```

Eğer restart gerektirmeden reload yapılabiliyorsa (örn. Hono reload signal):
```bash
docker exec <container> kill -HUP 1  # SIGHUP ile graceful reload
```
