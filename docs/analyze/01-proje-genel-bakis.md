# Proje Genel Bakış

> Analiz tarihi: 2026-08-07  
> Analiz eden: Proje Analizcisi Skill v1.0  
> Kapsam: `skills/` klasörü ve bu klasörü yayınlayan repo metadata/scripts katmanı

## Özet Kartı

| Özellik | Değer |
|---------|-------|
| Proje adı | fth-skills |
| Proje tipi | Curated skill library / metadata monorepo |
| Ana dil | Markdown, YAML, Python, Bash |
| Framework | Uygulama framework'ü yok; skills.sh uyumlu dosya sözleşmesi kullanılıyor |
| Paket yöneticisi | Node/Python paket yöneticisi yok; kullanıcı kurulumu `npx skills add ...` üzerinden |
| Toplam skill dizini | 77 |
| Toplam dosya | 298 |
| Metin/config/kod satırı | 20.209 |
| Test kapsamı | Kısmi: 4 `evals/` dizini, 3 `evals.json`; klasik unit test yok |
| API tipi | Yok |
| Son commit | `8a91e68`, 2026-08-06 22:42:55 +0300 |
| Son 3 ay commit | 10 |
| Aktif geliştirici | 3 yazar |
| Doğrulama | `python scripts/validate_curated_skills.py` geçti: 77 skill |

## Proje Amacı

Bu repo, AI agent'lar için yeniden kullanılabilir skill paketleri yayımlıyor. Ana ürün yüzeyi `skills/<skill-name>/SKILL.md` ve `skills/<skill-name>/agents/openai.yaml` sözleşmesi. `README.md` kurulumu `npx skills add fatih-developer/fth-skills` ile tarif ediyor; `skills.sh.json` ise public katalog gruplamalarını tanımlıyor.

## Klasör Yapısı

```text
skills/
  <skill-name>/
    SKILL.md              # Zorunlu ana yönerge dosyası
    agents/openai.yaml    # skills.sh/OpenAI görünürlüğü için zorunlu metadata
    references/           # Detaylı rehberler, örnekler, kontrol listeleri
    scripts/              # Yardımcı komutlar veya analiz araçları
    templates/            # Üretilecek doküman/kod şablonları
    evals/                # Skill davranışı için örnek/eval dosyaları
scripts/
  validate_curated_skills.py  # Frontmatter, openai.yaml ve referans doğrulaması
  generate_openai_yaml.py     # Eksik openai.yaml üretimi için yardımcı script
  translate_skills.py         # Skill içeriği çeviri yardımcı script'i
docs/analyze/
  01/02/03 raporları          # Bu analiz çıktıları
```

## Teknoloji ve İçerik Dağılımı

| Dosya tipi | Adet | Yorum |
|------------|------|-------|
| `.md` | 175 | Skill içerikleri ve referanslar ana gövdeyi oluşturuyor |
| `.yaml` | 79 | 77 zorunlu `openai.yaml` + 1 ekstra nested dosya + diğer YAML |
| `.tmpl` | 12 | `checkpoint-guardian`, `multi-brain`, `task-decomposer`, `react-flow`, `design-md-enforcer` şablonları |
| `.py` | 10 | Doğrulama, yayın/çeviri ve bazı skill yardımcı script'leri |
| `.json` | 7 | `skills.sh.json`, eval ve örnek veri dosyaları |
| `.sh` | 4 | `project-analyzer` ve `proje-analizcisi` keşif/analiz script'leri |
| Binary/local | 2 | `eachlabs-kling-generator.zip` ve `.png`, ikisi de local/ignore kapsamına giriyor |

## Skill Kapsamı

Repo 77 skill dizini içeriyor. Bunların 41'inde `references/`, 11'inde `scripts/`, 5'inde `templates/`, 4'ünde `evals/` var. Bu dağılım, çoğu skill'in tek dosyalı hızlı yönerge paketleri olduğunu; daha karmaşık skill'lerin ise referans ve şablonlarla genişletildiğini gösteriyor.

Öne çıkan geniş skill'ler:

| Skill | Satır | Gözlem |
|-------|-------|--------|
| `sqlite` | 1.769 | Çok kapsamlı referans seti var; TypeScript, Python, performans, FTS/vector ve cloud konuları ayrılmış |
| `coolify-orchestrator` | 1.096 | Operasyonel Coolify iş akışları için detaylı referanslar içeriyor |
| `ugc-crafter` | 1.060 | Platform kalibrasyonu, kimlik tutarlılığı ve eval dosyasıyla olgun bir paket |
| `design-intelligence` | 1.031 | Web kuralları ve review rubric referansları güçlü |
| `prompt-crafter` | 887 | Çok sayıda prompt pattern referansı ve eval dosyaları var |

## Geliştirme Süreci Göstergeleri

| Gösterge | Değer | Yorum |
|----------|-------|-------|
| Doğrulama sonucu | 77/77 geçti | Temel dağıtım sözleşmesi güçlü |
| `agents/openai.yaml` zorunluluğu | Tüm skill dizinlerinde var | skills.sh görünürlüğü için kritik gereksinim karşılanmış |
| `skills.sh.json` public liste | 69 unique skill | 77 dizinle bilinçli veya güncel olmayan fark var |
| Ungrouped skill sayısı | 8 | `brand-name-lab`, `geo-auditor`, `geo-optimizer`, `plan-implement-verify-recover`, `project-focus-first`, `turkish-prompt-compiler`, `ugc-crafter`, `eachlabs-kling-generator` |
| Evals yaygınlığı | 4/77 dizin | Skill kalitesi için düşük otomasyon seviyesi |
| README sayısı | 69 Public | `skills/` gerçek dizin sayısı 77; dokümantasyon güncelleme ihtiyacı var |

## Güçlü Yönler

- `scripts/validate_curated_skills.py`, frontmatter alanlarını, `name` ve klasör adı eşleşmesini, `agents/openai.yaml` varlığını ve `SKILL.md` içindeki `references/`, `templates/`, `scripts/`, `assets/`, `agents/` referanslarının dosya olarak varlığını kontrol ediyor. Bu, skills.sh görünmezlik hatasını erken yakalayan iyi bir kalite kapısı.
- Skill anatomy tutarlı: her geçerli skill dizininde `SKILL.md` ve `agents/openai.yaml` var. Doğrulama çıktısı 77 skill için temiz.
- Karmaşık skill'lerde progressive disclosure'a uygun ayrım var: `sqlite`, `prompt-crafter`, `coolify-orchestrator`, `design-intelligence`, `session-transfer` gibi paketler ana `SKILL.md` dosyasını referanslarla destekliyor.
- Güvenlik ve orkestrasyon alanları birbirini tamamlıyor: `skill-security`, `security-auditor`, `adaptive-guard`, `security-orchestrator`, `checkpoint-guardian`, `task-decomposer`, `parallel-planner` ayrı görev sınırlarına sahip.

## Zayıf Yönler

- `README.md` ve `skills.sh.json` 69 public skill gösterirken `skills/` altında 77 dizin var. Bu fark public katalog için bilinçli değilse keşfedilebilirlik kaybı yaratır.
- `README.md`, domain klasörlerinde `ECOSYSTEM.md` bulunduğunu söylüyor; `rg "ECOSYSTEM.md"` sonucunda gerçek `ECOSYSTEM.md` dosyası bulunmadı. Bunun yerine `ecosystem-api`, `ecosystem-database`, `ecosystem-mobile` gibi skill dizinleri var. Dokümantasyon ile repo yapısı ayrışmış.
- `skills/agent-reviewer/agents/agents/openai.yaml` içinde `Task Decomposer` metadata'sı duruyor. Zorunlu `skills/agent-reviewer/agents/openai.yaml` doğru olduğu için doğrulama geçiyor, fakat ekstra dosya kopyalama/üretim hatası izlenimi veriyor.
- `skills/eachlabs-kling-generator/` ve `skills/eachlabs-kling-generator.zip` `.gitignore` altında, fakat `validate_curated_skills.py` ignored dizinleri dışlamadığı için lokal/personal skill de 77 sayısına dahil ediliyor. Bu CI veya lokal doğrulama sonuçlarını ortama bağlı hale getirebilir.
- Evals kapsamı zayıf: yalnızca `claw-integration-design`, `prompt-crafter`, `project-focus-first`, `ugc-crafter` altında eval dizini/dosyası var; 73 skill için davranış regresyonlarını yakalayan test/eval yok.
