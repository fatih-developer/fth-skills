# Trust Matrix — Yetki × Güven Seviyesi

## Tam Yetki Haritası

Her güven seviyesi için hangi işlemlere izin var, hangisi checkpoint gerektirir, hangisi yasak.

---

## GÜVENİLİR (80-100)

```
DOSYA SİSTEMİ
  ✅ Okuma         : tanımlanan scope içinde serbest
  ✅ Yazma         : tanımlanan scope içinde serbest
  ✅ Silme         : checkpoint (geri alınamaz)
  ✅ Çalıştırma    : whitelist'teki komutlar
  ❌ Sistem dizini : /etc /sys /proc — yasak

AĞ
  ✅ HTTPS GET     : whitelist domain'ler
  ✅ HTTPS POST    : whitelist domain'ler
  ✅ WebSocket     : whitelist domain'ler
  ⚠️ Yeni domain  : ilk kullanımda onay
  ❌ HTTP (şifresiz): yasak
  ❌ Raw socket    : yasak

EXECUTION
  ✅ Bash (whitelist): güvenli komutlar
  ✅ Python/Node  : sandbox içinde
  ⚠️ Yeni process: checkpoint
  ❌ eval/exec    : yasak
  ❌ Sistem servis: yasak

SKILL ZİNCİRİ
  ✅ 60+ trust skill tetikleyebilir
  ⚠️ 40-59 trust : checkpoint
  ❌ 0-39 trust  : tetikleyemez

VERİ
  ✅ Kullanıcı verisi okuma
  ✅ Çıktıya yazma
  ⚠️ PII işleme  : maskeleme zorunlu
  ❌ 3. taraf PII paylaşımı: yasak
```

---

## NORMAL (60-79)

```
DOSYA SİSTEMİ
  ✅ Okuma         : çalışma dizini + temp
  ⚠️ Yazma         : sadece /tmp ve proje çıktı dizini
  ⚠️ Silme         : checkpoint + geri alma planı
  ❌ Sistem dizini : yasak
  ❌ Home dizin    : yasak (~/ dışında çalışma dizini)

AĞ
  ✅ HTTPS GET     : whitelist domain'ler
  ⚠️ HTTPS POST    : checkpoint (veri gönderiyor)
  ❌ HTTP          : yasak
  ❌ WebSocket     : yasak (uzun süreli bağlantı riski)

EXECUTION
  ✅ Bash (dar whitelist): ls, cat, grep, wc, find (temp)
  ⚠️ Python/Node  : salt okunur çıktı üretenler
  ❌ Shell script çalıştırma: yasak
  ❌ eval/exec    : yasak

SKILL ZİNCİRİ
  ✅ 70+ trust skill tetikleyebilir
  ❌ Daha düşük trust tetikleyemez

VERİ
  ✅ Kullanıcı verisi okuma (PII hariç)
  ⚠️ PII: özel onay gerektirir
  ❌ PII yazma    : yasak
```

---

## KISITLI (40-59)

```
DOSYA SİSTEMİ
  ✅ Okuma         : sadece proje dizini, okuma
  ❌ Yazma         : yasak
  ❌ Silme         : yasak

AĞ
  ⚠️ HTTPS GET     : sınırlı whitelist, checkpoint
  ❌ POST          : yasak
  ❌ Diğer         : yasak

EXECUTION
  ⚠️ Bash          : sadece ls, cat, grep — her çalıştırmada onay
  ❌ Script        : yasak
  ❌ eval/exec     : yasak

SKILL ZİNCİRİ
  ❌ Başka skill tetikleyemez

VERİ
  ✅ Anonim veri okuma
  ❌ PII           : yasak
  ❌ Yazma         : yasak
```

---

## KARANTİNA (0-39)

```
DOSYA SİSTEMİ   : TAMAMEN YASAK
AĞ              : TAMAMEN YASAK
EXECUTION       : TAMAMEN YASAK
SKILL ZİNCİRİ   : TAMAMEN YASAK
VERİ            : TAMAMEN YASAK

→ Manuel inceleme gerekli
→ Üretimde kullanılamaz
→ Sadece sandbox'ta izleme altında test
```

---

## Zincir Güvenliği Kuralları

### İzin Verilen Zincirler
```
GÜVENİLİR → GÜVENİLİR     ✅ serbest
GÜVENİLİR → NORMAL        ✅ serbest
GÜVENİLİR → KISITLI       ⚠️ checkpoint
NORMAL    → NORMAL         ✅ serbest
NORMAL    → KISITLI        ⚠️ checkpoint
KISITLI   → herhangi      ❌ yasak
```

### Privilege Escalation Kuralı
Düşük güven skorlu skill, yüksek güven skorlu skill'i tetikleyemez:
```
KISITLI (45) → GÜVENİLİR (85)   ❌ YASAK
NORMAL (65)  → GÜVENİLİR (85)   ⚠️ checkpoint + log
```

### Maksimum Zincir Derinliği
```
1-2 seviye  : serbest
3 seviye    : uyarı ver, logla
4 seviye    : checkpoint
5+ seviye   : yasak (sadece manuel onay ile)
```

---

## Özel Durumlar

### Ecosystem Skill'leri (Dahili, Bilinen Yazar)
Ecosystem'e dahil skill'ler başlangıç skoru +10 alır:
```
Temel skor: 50 + 10 (ecosystem) = 60
→ NORMAL seviyeden başlar
```

### Production-Onaylı Skill'ler
Manuel review geçmiş skill'ler +15 alır:
```
→ Audit + Trust + Manuel onay = +25 bonus
```

### Deneysel / Yeni Skill'ler
İlk 7 gün içinde yazılmış skill'ler -10 alır:
```
→ KISITLI modda izleme altında çalışır
→ 7 gün sorunsuz geçerse normal skora döner
```
