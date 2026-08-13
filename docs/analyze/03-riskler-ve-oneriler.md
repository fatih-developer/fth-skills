# Riskler ve Öneriler

## Risk Matrisi

| Risk | Kategori | Etki | Olasılık | Öncelik |
|------|----------|------|----------|---------|
| Public manifest ile gerçek skill dizinleri farklı | Operasyon / Keşfedilebilirlik | Orta | Yüksek | Yüksek |
| README'de `ECOSYSTEM.md` var denip dosyaların olmaması | Dokümantasyon / Mimari | Orta | Yüksek | Yüksek |
| Lokal ignored skill'in doğrulama kapsamına girmesi | Operasyon / CI tutarlılığı | Orta | Orta | Yüksek |
| Nested yanlış `openai.yaml` kalıntısı | Metadata hijyeni | Düşük | Yüksek | Orta |
| Evals kapsamının 4/77 ile sınırlı olması | Kalite / Regresyon | Orta | Yüksek | Orta |
| `project-analyzer` ve `proje-analizcisi` script path'lerinin ortam bağımlı olması | Taşınabilirlik | Orta | Orta | Orta |
| Binary/local dosyaların `skills/` altında durması | Repo hijyeni / Gizlilik | Orta | Düşük-Orta | Orta |

## Kritik Riskler

Bu analizde production güvenlik açığı veya çalışan API riski bulunmadı. Ancak yayınlanan skill kataloğu açısından aşağıdaki iki konu kritik seviyeye yakın operasyonel risktir.

### Manifest ve README Gerçek Skill Sayısıyla Uyuşmuyor

**Kategori:** Operasyon / Keşfedilebilirlik  
**Nerede:** `README.md`, `skills.sh.json`, `skills/`  
**Sorun:** `skills/` altında 77 dizin var. `skills.sh.json` 69 unique skill listeliyor. README de "69 Public" diyor. 8 dizin public manifest dışında kalmış. `eachlabs-kling-generator` bilinçli private görünüyor; diğer 7 skill için niyet belirsiz.

**Kanıt:**

```text
skills dirs: 77
grouped unique: 69
ungrouped:
brand-name-lab, eachlabs-kling-generator, geo-auditor, geo-optimizer,
plan-implement-verify-recover, project-focus-first,
turkish-prompt-compiler, ugc-crafter
```

**Düzeltme:**

1. Her ungrouped skill için karar ver: public, experimental, private.
2. Public olanları `skills.sh.json` gruplarına ekle.
3. Private olanları doğrulama dışında tut veya `skills/.private/` gibi net bir alana taşı.
4. README'deki "69 Public" sayısını otomatik üreten bir script veya CI check ekle.

**Tahmini efor:** 2-4 saat.

### README'deki Ecosystem Yapısı Dosya Sistemiyle Uyuşmuyor

**Kategori:** Dokümantasyon / Mimari  
**Nerede:** `README.md`, `skills/task-decomposer/SKILL.md`, `skills/ecosystem-*`  
**Sorun:** README, domain folder'larda `ECOSYSTEM.md` bulunduğunu söylüyor. Tarama sonucunda gerçek `ECOSYSTEM.md` dosyası bulunmadı. `task-decomposer` da `skills/.curated/domains/<domain>/ECOSYSTEM.md` gibi mevcut olmayan bir path'ten bahsediyor.

**Kanıt:**

```text
rg "ECOSYSTEM.md" skills README.md
README.md: Every domain folder (...) contains an ECOSYSTEM.md map
skills/task-decomposer/SKILL.md: read skills/.curated/domains/<domain>/ECOSYSTEM.md
```

Gerçek dosya yok; buna karşılık `skills/ecosystem-api`, `skills/ecosystem-database`, `skills/ecosystem-mobile`, `skills/ecosystem-orchestration`, `skills/ecosystem-security` dizinleri var.

**Düzeltme:**

1. Tercih edilen modeli seç: ayrı `ECOSYSTEM.md` dosyaları mı, yoksa `ecosystem-*` skill'leri mi?
2. README ve `task-decomposer` yönergelerini aynı modele göre düzelt.
3. Doğrulayıcıya `ECOSYSTEM.md` referanslarının gerçekten varlığını kontrol eden özel bir kural ekle.

**Tahmini efor:** 2-3 saat.

## Önemli Riskler

### Ignored Local Skill Doğrulama Kapsamına Giriyor

**Kategori:** Operasyon / CI tutarlılığı  
**Nerede:** `skills/eachlabs-kling-generator/`, `.gitignore`, `scripts/validate_curated_skills.py`  
**Sorun:** `.gitignore` bu dizini ve zip dosyasını hariç tutuyor, AGENTS de commit edilmemesini söylüyor. Ancak doğrulayıcı `root.rglob("SKILL.md")` ile tüm dizinleri taradığı için lokal ignored skill de validasyon sayısına dahil oluyor.

**Kanıt:**

```text
.gitignore:
skills/eachlabs-kling-generator/
skills/eachlabs-kling-generator.zip

Validation PASSED for 77 skill(s)
```

**Düzeltme:** Doğrulayıcıya `git check-ignore` tabanlı hariç tutma veya explicit denylist ekle. Alternatif olarak private skill'i `skills/` dışına taşı.

**Tahmini efor:** 2-3 saat.

### Yanlış Nested `openai.yaml`

**Kategori:** Metadata hijyeni  
**Nerede:** `skills/agent-reviewer/agents/agents/openai.yaml`  
**Sorun:** Dosya `agent-reviewer` altında ama `Task Decomposer` display name'i ve prompt'u içeriyor. Zorunlu doğru dosya ayrıca bulunduğu için mevcut doğrulama bunu yakalamıyor.

**Düzeltme:** Dosyayı kaldır ve doğrulayıcıya `agents/openai.yaml` dışında `openai.yaml` bulunursa warning veren kontrol ekle.

**Tahmini efor:** 30-60 dakika.

### Evals Kapsamı Çok Düşük

**Kategori:** Kalite / Regresyon  
**Nerede:** `skills/*/evals/`  
**Sorun:** 77 skill içinde yalnızca 4 dizinde eval klasörü var. `evals.json` dosyası bulunanlar 3: `claw-integration-design`, `prompt-crafter`, `ugc-crafter`. `project-focus-first` altında `evals.md` var. Skill trigger ve davranış regresyonları çoğunlukla otomatik yakalanmıyor.

**Düzeltme:** Önce public ve yüksek etkili skill'leri kapsa: `skill-security`, `adaptive-guard`, `checkpoint-guardian`, `task-decomposer`, `session-transfer`, `project-analyzer`, `proje-analizcisi`, `sqlite`, `design-intelligence`, `coolify-orchestrator`.

**Tahmini efor:** İlk 10 skill için 1-2 gün.

### Analiz Skill'lerinde Ortam Bağımlı Script Path

**Kategori:** Taşınabilirlik  
**Nerede:** `skills/proje-analizcisi/SKILL.md`, `skills/project-analyzer/SKILL.md`  
**Sorun:** Skill yönergeleri script'leri `~/.gemini/antigravity/...` altından çalıştırmayı söylüyor. Repo içinde script'ler mevcut olduğu halde başka agent ortamında bu path kırılabilir.

**Düzeltme:** Skill içindeki komutları repo-relative hale getir veya "skill dizinine göre resolve et" kuralını açık yaz.

**Tahmini efor:** 30-60 dakika.

## Güvenlik Analizi

### Pozitif Bulgular

- `skill-security`, `security-auditor`, `adaptive-guard`, `security-orchestrator` gibi güvenlik odaklı skill'ler ayrı ve kapsamlı.
- `session-transfer/scripts/validate_handoff.py`, handoff dosyalarında secret pattern ve TODO placeholder kontrolü yapıyor.
- `.gitignore`, `skills/eachlabs-kling-generator/` ve zip dosyasını hariç tutuyor.
- `git ls-files skills` çıktısında `eachlabs` dosyası görünmüyor; yani local ignored dosyalar şu an tracked değil.

### Endişe Verici Bulgular

- `skills/eachlabs-kling-generator/.env` lokal olarak mevcut. Tracked değil, ancak sensitive dosyaların `skills/` altında durması yanlış komut veya arşivleme akışlarında risk yaratır.
- `skills/eachlabs-kling-generator.zip` ve output PNG büyük local artifact'ler. Bunlar ignored olsa da validasyon/tarama sürelerini ve rapor metriklerini bozuyor.
- Doğrulayıcı secret taraması yapmıyor. Bu repo bir skill kütüphanesi olduğu için `SKILL.md`, `references/` ve `agents/openai.yaml` içinde yanlışlıkla credential örneği veya gerçek token kalması ayrı kontrol edilmeli.

## Performans Analizi

Bu repo runtime uygulama üretmiyor; performans riski CI ve tarama süreleriyle sınırlı.

Darboğaz adayları:

- `validate_curated_skills.py`, ignored ve binary-heavy lokal dizinleri hariç tutmadığı için workspace'e bağlı olarak fazla dosya tarayabilir.
- `rg` ile görülen `.zip`, `.png`, `.env` gibi local dosyalar `skills/` altında olduğu için geniş taramalar gereksiz gürültü üretiyor.
- README/manifest tutarsızlığı büyüdükçe release öncesi manuel kontrol maliyeti artar.

## Teknik Borç Envanteri

| Borç | Dosya/Modül | Tahmini Efor | Öncelik |
|------|-------------|--------------|---------|
| Public/private skill ayrımı makine-okunur değil | `skills.sh.json`, `.gitignore`, validator | 0.5 gün | Yüksek |
| README skill sayısı elle tutuluyor | `README.md` | 1-2 saat | Orta |
| `ECOSYSTEM.md` referansları gerçek dosya yapısıyla uyumsuz | `README.md`, `task-decomposer` | 2-3 saat | Yüksek |
| Nested yanlış metadata dosyası | `skills/agent-reviewer/agents/agents/openai.yaml` | 30 dakika | Orta |
| Evals kapsamı düşük | `skills/*/evals/` | 1-2 gün ilk faz | Orta |
| Analiz script path'leri taşınabilir değil | `project-analyzer`, `proje-analizcisi` | 1 saat | Orta |

## Önerilen Eylem Planı

### Bu Hafta

1. `skills/agent-reviewer/agents/agents/openai.yaml` kalıntısını kaldır.
2. `skills.sh.json` ile `skills/` dizinleri arasındaki farkı kontrol eden script veya validator kuralı ekle.
3. `eachlabs-kling-generator` için doğrulama kapsamı kararını netleştir: ignored path'leri hariç tut veya private dizini `skills/` dışına taşı.
4. README'deki "69 Public" ve `ECOSYSTEM.md` bölümlerini gerçek yapıyla hizala.

### Bu Ay

1. En kritik 10 skill için trigger/eval dosyaları ekle.
2. `validate_curated_skills.py` kapsamını genişlet:
   - beklenmeyen nested `openai.yaml`
   - manifest dışı public adayları
   - ignored path kapsamı
   - büyük binary/local artifact uyarısı
3. `project-analyzer` ve `proje-analizcisi` script path'lerini taşınabilir hale getir.

### Uzun Vade

1. Public/experimental/private lifecycle'ı tek manifestte tanımla.
2. README skill listelerini manifestten otomatik üret.
3. Güvenlik skill'leri için fixture tabanlı eval suite kur.
4. Domain ekosistemi için ya gerçek `ECOSYSTEM.md` dosyaları oluştur ya da `ecosystem-*` skill'lerini resmi mimari model olarak dokümante et.

## Genel Sağlık Skoru

```text
Güvenlik          : 7 / 10
Operasyon         : 6 / 10
Sürdürülebilirlik : 7 / 10
Test/Eval Kapsamı : 3 / 10
Dokümantasyon     : 6 / 10
─────────────────────────────
Proje Sağlığı     : 5.8 / 10
```

Genel durum kötü değil: temel skills.sh görünürlük sözleşmesi güçlü ve doğrulama geçiyor. Asıl risk çalışan koddan değil, katalog gerçekliği ve kalite kapılarının eksikliğinden geliyor.
