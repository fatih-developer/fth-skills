# Mimari ve Kod Kalitesi Analizi

## Mimari Değerlendirme

Bu repo klasik uygulama mimarisi değil; bir paket/katalog mimarisi kullanıyor. Ana sınır `skills/<skill-name>/` dizinleri. Her skill bağımsız dağıtılabilir bir doküman paketi gibi tasarlanmış, repo seviyesinde ise `scripts/validate_curated_skills.py`, `scripts/generate_openai_yaml.py`, `skills.sh.json` ve `README.md` yayın/keşif katmanını oluşturuyor.

### Katman Yapısı

| Katman | Dosyalar | Değerlendirme |
|--------|----------|----------------|
| Skill runtime yönergeleri | `skills/*/SKILL.md` | Ana davranış sözleşmesi burada. 77/77 dizinde mevcut. |
| Connector/skills.sh metadata | `skills/*/agents/openai.yaml` | Görünürlük için kritik. 77 skill'de doğru yerde var. |
| Derin referanslar | `skills/*/references/` | 41 skill'de var; karmaşık görevlerde iyi ayrıştırılmış. |
| Yardımcı script'ler | `skills/*/scripts/`, `scripts/` | 11 skill script içeriyor; repo doğrulama script'i net ve okunabilir. |
| Katalog manifesti | `skills.sh.json`, `README.md` | Kamuya sunulan listeyi yönetiyor, ancak mevcut dizin sayısıyla ayrışmış. |

### Bağımlılık Yönetimi

Kod bağımlılığı sınırlı. `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml` gibi merkezi bağımlılık dosyası yok. Python script'ler standart kütüphane ağırlıklı çalışıyor. Bu, kurulum yükünü azaltıyor; ancak eval/test çalıştırma standardı da oluşmamış.

`scripts/validate_curated_skills.py` içinde bağımlılık mantığı tek dosyada ve anlaşılır:

- `parse_frontmatter()` frontmatter'ı basit ama yeterli bir parser ile okuyor.
- `extract_referenced_paths()` skill içindeki `references/`, `templates/`, `scripts/`, `assets/`, `agents/` referanslarını regex ile çıkarıyor.
- `list_skill_dirs()` `root.rglob("SKILL.md")` kullandığı için nested veya ignored skill'leri de yakalıyor.

Bu yaklaşım küçük repo için pragmatik; ancak ignored/personal dizinleri kapsam dışı bırakma desteği olmadığı için lokal ortam farkı yaratabiliyor.

### Modülerlik Skoru

`8/10`

Gerekçe: Skill paketleri bağımsız, zorunlu dosya sözleşmesi net, referanslar iyi ayrılmış. Skoru düşüren noktalar public manifest ile gerçek dizinlerin ayrışması, `ECOSYSTEM.md` dokümantasyon uyuşmazlığı ve nested `agents/agents/openai.yaml` kalıntısı.

## Kod Kalitesi Metrikleri

| Metrik | Değer | Durum |
|--------|-------|-------|
| Toplam skill | 77 | İyi |
| Doğrulama | 77/77 geçti | İyi |
| Toplam dosya | 298 | Beklenen düzey |
| Metin/config/kod satırı | 20.209 | Orta ölçekli doküman repo |
| En büyük metin dosyası | `skills/pgbouncer-architect/SKILL.md`: 437 satır | Dikkat |
| En büyük binary/local dosya | `skills/eachlabs-kling-generator/outputs/kling_v3_1774716312.png`: 4.665.257 byte | Risk |
| Ekstra `openai.yaml` | 1: `skills/agent-reviewer/agents/agents/openai.yaml` | Dikkat |
| Evals dizini | 4/77 | Zayıf |
| Klasik test dosyası | 0 | Zayıf |
| TODO/FIXME | Çoğunlukla şablon/script placeholder'ları | Düşük risk |

## Dikkat Gerektiren Dosyalar

### `skills/agent-reviewer/agents/agents/openai.yaml`

Neden dikkat: Bu dosya `agent-reviewer` altında nested `agents/agents` yolunda duruyor ama içeriği `Task Decomposer` metadata'sı:

```yaml
interface:
  display_name: "Task Decomposer"
```

Öneri: Dosya gerçekten kullanılmıyorsa kaldırılmalı. Doğrulayıcıya `agents/agents/` gibi beklenmeyen nested metadata yollarını warning olarak raporlayan bir kontrol eklenmeli.

### `README.md`

Neden dikkat: Başlık ve skill listesi "69 Public" diyor. `skills/` altında 77 dizin, `skills.sh.json` içinde 69 unique skill var. Ayrıca README, domain folder'larda `ECOSYSTEM.md` olduğunu söylüyor ama repo içinde bu dosyalar yok.

Öneri: README iki seviyeyi açık ayırmalı: "77 local skill dizini, 69 public manifest skill'i" gibi. `ECOSYSTEM.md` iddiası ya gerçek dosyalar eklenerek karşılanmalı ya da `ecosystem-*` skill'lerine göre düzeltilmeli.

### `skills.sh.json`

Neden dikkat: Public gruplamalarda 8 skill yok:

```text
brand-name-lab
eachlabs-kling-generator
geo-auditor
geo-optimizer
plan-implement-verify-recover
project-focus-first
turkish-prompt-compiler
ugc-crafter
```

`eachlabs-kling-generator` lokal/personal olduğu için dışarıda kalması doğru görünüyor. Diğer 7 skill bilinçli dışarıda değilse public keşfedilebilirlik kaybı var.

Öneri: Public/experimental/private sınıflandırması repo içinde makine-okunur hale getirilmeli. Örneğin `skills.sh.json` eksikleri için CI warning üretilebilir.

### `skills/eachlabs-kling-generator/`

Neden dikkat: AGENTS talimatı bu dizinin commit edilmemesi gerektiğini söylüyor ve `.gitignore` bunu kapsıyor. Ancak doğrulayıcı ignored dizinleri hariç tutmuyor. Lokal dizin içinde `.env`, `.zip`, `.png` var.

Öneri: `validate_curated_skills.py` default olarak git ignored path'leri hariç tutmalı ya da `--include-ignored` opsiyonu eklenmeli. Böylece CI/lokal doğrulama sayıları birbirinden sapmaz.

### `skills/proje-analizcisi/SKILL.md` ve `skills/project-analyzer/SKILL.md`

Neden dikkat: Her iki skill de analiz script'lerini `bash ~/.gemini/antigravity/skills/...` yolundan çalıştırmayı söylüyor. Repo içinde script'ler `skills/<skill>/scripts/` altında mevcut. Bu path, farklı agent ortamlarında kırılgan.

Öneri: Yönergeler relative path veya skill dizinine göre çözümleme kuralı kullanmalı. Örneğin `bash skills/proje-analizcisi/scripts/phase1_discovery.sh` repo içi kullanım için daha taşınabilir.

## Tekrar Eden Kod ve İçerik

Belirgin bir kod tekrarından çok, bilinçli ikiz skill tasarımı var:

- `project-analyzer` ve `proje-analizcisi` aynı araç setinin İngilizce/Türkçe varyantları gibi duruyor.
- `security-auditor` ve `skill-security` aynı referans dosya setlerinden bazılarını taşıyor.
- `ecosystem-api`, `ecosystem-database`, `ecosystem-mobile`, `ecosystem-orchestration` benzer `scripts/install_all.py` yapısına sahip.

Bu tekrar kabul edilebilir; ancak ortak script/şablon değişirse senkronizasyon riski oluşur. Özellikle `project-analyzer` ve `proje-analizcisi` script'leri için diff tabanlı bir kontrol faydalı olur.

## Error Handling Kalitesi

`scripts/validate_curated_skills.py` hata yönetimi iyi seviyede:

- Eksik `SKILL.md` erken dönüyor.
- Frontmatter parse hataları `ValueError` ile issue'a çevriliyor.
- Uyarılar ve hatalar ayrı listeleniyor.
- Exit code 1/0 CI için uygun.

Zayıf nokta, frontmatter parser'ın YAML'ın tamamını desteklememesi. Bu bilinçli sadeleştirme gibi duruyor, fakat çok satırlı description veya karmaşık quoting ihtiyaçlarında yanlış sonuç verebilir. Repo kuralı tek satır description olduğu için şu an kabul edilebilir.

## Tip Güvenliği

TypeScript uygulama kodu yok. Python tarafında type hint kullanımı iyi:

- `from __future__ import annotations`
- `dataclass`
- `Path`, `Sequence`, `tuple[list[...]]` tipleri

`scripts/generate_openai_yaml.py` daha basit ve az tipli; üretim kalite kapısı değil, yardımcı script olduğu için risk düşük.

## Genel Kod Kalitesi Skoru

```text
Mimari          : 8 / 10
Okunabilirlik   : 8 / 10
Sürdürülebilirlik: 7 / 10
Test/Eval Kapsamı: 3 / 10
Dokümantasyon   : 7 / 10
─────────────────────────
Genel           : 6.6 / 10
```

Skoru düşüren ana etken kod kalitesi değil; katalog gerçekliği, dokümantasyon tutarlılığı ve eval eksikliği.

## En İyi Yazılmış Bölümler

- `scripts/validate_curated_skills.py`: Repo için en kritik sözleşmeyi otomatik kontrol ediyor. Frontmatter, `agents/openai.yaml`, path referansları ve exit code davranışı net.
- `skills/sqlite/`: Ana skill ile referanslar iyi bölünmüş. `TYPESCRIPT_DRIZZLE.md`, `PYTHON.md`, `PERFORMANCE.md`, `FTS5_VECTOR.md`, `CLOUD.md` gibi dosyalar progressive disclosure için uygun.
- `skills/session-transfer/`: Script, template ve resume checklist kombinasyonu gerçek iş akışını destekliyor; sadece prompt metni değil, yardımcı araç da sunuyor.
- `skills/prompt-crafter/`: Çok sayıda referans ve eval dosyasıyla kalite standardı yüksek skill örneği.

## En Çok İyileştirme Gereken Bölümler

| Öncelik | Alan | Öneri | Tahmini efor |
|---------|------|-------|--------------|
| Yüksek | Manifest/README tutarlılığı | `skills.sh.json`, README ve gerçek skill dizinlerini karşılaştıran CI kontrolü ekle | 2-4 saat |
| Yüksek | Ignored lokal skill kapsamı | `validate_curated_skills.py` içine ignored/private dizinleri hariç tutma modu ekle | 2-3 saat |
| Orta | Nested metadata kalıntısı | `agents/agents/openai.yaml` gibi beklenmeyen yolları tespit et | 1 saat |
| Orta | Ecosystem dokümantasyonu | README'deki `ECOSYSTEM.md` iddiasını gerçek yapıyla hizala | 1-2 saat |
| Orta | Eval kapsamı | En kritik 15 skill için minimum trigger eval dosyası ekle | 1-2 gün |
