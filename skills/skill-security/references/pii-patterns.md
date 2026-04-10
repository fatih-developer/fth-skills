# PII Tespit Kalıpları

## Kişisel Tanımlayıcı Bilgiler (PII)

Bir skill bu veri türlerini işliyorsa KVKK/GDPR kuralları geçerlidir.

---

## Türkiye'ye Özel PII

### TC Kimlik Numarası
```regex
\b[1-9][0-9]{10}\b
```
**Risk:** Kimlik hırsızlığı, dolandırıcılık
**Gereksinim:** Şifreli sakla, log'a yazma, 3. tarafa gönderme

### Vergi Numarası
```regex
\b[0-9]{10}\b   # şirket vergi no
```

### Türk Telefon Numarası
```regex
(\+90|0090|090)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}
\b05[0-9]{9}\b
```

---

## Evrensel PII

### E-posta Adresi
```regex
[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}
```
**Risk:** Spam, phishing, hesap ele geçirme

### IP Adresi
```regex
# IPv4
\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b
# IPv6
([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
```
**Not:** Kullanıcı IP'si PII sayılır (GDPR)

### Kredi Kartı Numarası
```regex
\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b
```
**Risk:** Finansal dolandırıcılık
**Zorunlu:** PCI-DSS uyumu, asla log'a yazma

### IBAN
```regex
TR[0-9]{2}[0-9]{5}[0-9]{17}
[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}
```

### Pasaport / Kimlik Numarası
```regex
[A-Z]{1,2}[0-9]{6,9}   # genel pasaport
```

---

## Teknik Gizli Veriler (Hassas ama PII değil)

### API Key Kalıpları
```regex
# Genel API key kalıbı
(?i)(api[_-]?key|apikey|api[_-]?secret)\s*[=:]\s*['"]?([a-zA-Z0-9\-_]{20,})
# Claude/Anthropic
sk-ant-[a-zA-Z0-9\-_]{40,}
# OpenAI
sk-[a-zA-Z0-9]{48}
# GitHub
ghp_[a-zA-Z0-9]{36}
# AWS
AKIA[0-9A-Z]{16}
# Stripe
(sk|pk)_(test|live)_[a-zA-Z0-9]{24,}
```

### JWT Token
```regex
eyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+
```
**Risk:** Oturum ele geçirme

### Private Key / Sertifika
```
-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
```

### Şifre Kalıpları
```regex
(?i)(password|passwd|pwd|secret|token)\s*[=:]\s*['"]?([^\s'"]{6,})
```

---

## Sızıntı Riski Değerlendirmesi

| Veri Türü | Sızarsa Risk | Önlem |
|-----------|-------------|-------|
| TC Kimlik | Kimlik hırsızlığı | Şifrele, log'a yazma |
| Kredi kartı | Finansal dolandırıcılık | PCI-DSS, asla saklama |
| E-posta | Spam, phishing | Minimum toplama |
| API Key | Servis ele geçirme | Vault kullan, rotate et |
| JWT | Oturum ele geçirme | Kısa TTL, revoke mekanizması |
| Şifre (hash) | Brute force | bcrypt/argon2, tuzlama |
| IP Adresi | Takip, profilleme | Anonim hale getir |
| Private Key | Tam sistem ele geçirme | KESİN YASAK — log'a yazma |

---

## Skill'de PII Kuralları

Bir skill PII işliyorsa şu kontroller zorunlu:

```
□ Minimum toplama: sadece gereken kadar veri al
□ Amaç sınırlaması: toplandığı amaç dışında kullanma
□ Şifreleme: transit ve depolama şifrelemesi
□ Log maskeleme: logda PII görünmemeli
  email: "fat***@gm***.com" formatında maskele
  telefon: "+90 5** *** **89" formatında maskele
  TC: "***********" göster
□ Silme hakkı: kullanıcı talep ederse sil
□ Veri saklama süresi: tanımla ve uygula
□ 3. taraf paylaşım: açık onay olmadan paylaşma
```

---

## Log Maskeleme Örnekleri

```python
# E-posta maskele
def mask_email(email):
    user, domain = email.split('@')
    return f"{user[:3]}***@{domain[:2]}***.{domain.split('.')[-1]}"

# Telefon maskele
def mask_phone(phone):
    return phone[:3] + "*** ***" + phone[-2:]

# Kart numarası maskele
def mask_card(card):
    return "**** **** **** " + card[-4:]

# API key maskele
def mask_key(key):
    return key[:8] + "..." + key[-4:]
```
