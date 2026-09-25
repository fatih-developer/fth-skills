# Skill Denetimi — Güncelleme ve Düzeltme Listesi

**Tarih:** 2026-09-25
**Kapsam:** `skills/` altındaki 78 skill (`SKILL.md`, `agents/openai.yaml`, `references/`, `templates/`, `scripts/`, `evals/`), `skills.sh.json`, `README.md`
**Yöntem:** Katı YAML ayrıştırma, yol ve skill referansı kontrolü, Markdown code fence analizi, script sözdizimi ve test çalıştırma (`session-transfer`: 10/10 test geçti), ardından skill'lerin elle okunması.

> `scripts/validate_curated_skills.py` şu anda 78 skill için **PASSED** veriyor. Aşağıdaki P0 maddelerinin çoğunu yakalayamıyor, çünkü frontmatter'ı gerçek YAML olarak ayrıştırmıyor ve `openai.yaml` içeriğine bakmıyor.

---

## Öncelik özeti

| Öncelik | Anlamı | Madde sayısı |
|---|---|---|
| **P0** | Bozuk: skill yanlış çalışıyor, keşfedilemiyor ya da var olmayan bir şeye yönlendiriyor | 7 |
| **P1** | Yanlış veya riskli davranış, keşif ve tetikleme sorunları, çakışan skill'ler | 7 |
| **P2** | Kalite ve tutarlılık | 12 |
| **P3** | Uzun vadeli iyileştirme | 4 |

---

## Uygulama durumu (2026-09-25)

Bu denetimdeki maddeler `claude/relaxed-volta-xh8ycc` branch'inde uygulandı. `python scripts/validate_curated_skills.py` artık 81 skill için geçiyor (78 + 3 yeni ecosystem hub'ı); ayrıca 14 araç testi ve 10 `session-transfer` testi geçiyor. CI (`.github/workflows/validate.yml`) aynı kontrolleri her push ve PR'da çalıştırıyor.

| Madde | Durum | Nasıl çözüldü |
|---|---|---|
| P0-1 | ✅ | Frontmatter geçerli YAML; doğrulayıcı artık `yaml.safe_load` kullanıyor, bu hata test ile korunuyor |
| P0-2 | ✅ | Ecosystem `default_prompt` alanları doğru `$ecosystem-*` adıyla ve görev odaklı yeniden yazıldı |
| P0-3 | ✅ | Script'ler `<skill-dir>/scripts/...` ile çağrılıyor; script çalışamazsa elle yapılacak adımlar tanımlandı |
| P0-4 | ✅ | Ortak, varsayılan olarak deneme modunda çalışan kurulum script'i (`--status`, `--workflow`, `--missing-only`, `--execute`); kurulum kullanıcı onayına bağlı |
| P0-5 | ✅ | `task-decomposer` ve `parallel-planner` otomatik üretilen ecosystem indeksini kullanıyor; README ve AGENTS.md güncellendi |
| P0-6 | ✅ | `skill-security`, `security-auditor`'a birleştirildi; katman adları eşitlendi |
| P0-7 | ✅ | `.pyc` kaldırıldı, `.gitignore` güncellendi, doğrulayıcı commit edilmiş bytecode'u engelliyor |
| P1-1 | ✅ | `skills.sh.json` gruplamaları ve README kataloğu `workflows.json` dosyalarından üretiliyor; her skill tam bir ecosystem'e ait |
| P1-2 | ✅ | 40 açıklama "Use when…" ile yeniden yazıldı; doğrulayıcı tetik ifadesini zorunlu tutuyor |
| P1-3 | ✅ | İki alias (`skill-security`, `proje-analizcisi`); hafıza üçlüsü ve tasarım üçlüsü için kapsam bölümleri; kapılar için öncelik sırası (`@ecosystem-reasoning`) |
| P1-4 | ✅ | `ask-first-act-later`, `project-focus-first`, `mastermind-logger` ve iki alias için `allow_implicit_invocation: false`. `claude-style-coding` açık bırakıldı; açıklaması "user-facing work" ile daraltıldı |
| P1-5 | ✅ | Coolify'da canlı restart, toplu env değişikliği ve silme işlemleri onaya bağlandı; `mastermind-logger` yalnızca `docs/knowledgelib/` altına yazıyor |
| P1-6 | ✅ | Kırık referanslar düzeltildi; doğrulayıcı `@skill` referanslarını kontrol ediyor |
| P1-7 | ✅ | `design-md-enforcer` yolları göreli; `plan-implement-verify-recover` açıklaması runtime'dan bağımsız |
| P2-1 | ✅ | 17 skill'de dış kod bloğu 4 backtick'e çevrildi; doğrulayıcı iç içe fence'i engelliyor |
| P2-2 | ✅ | 36 `short_description` tam cümle halinde; `generate_openai_yaml.py` artık metni kesmiyor |
| P2-3 | ✅ | Her üye skill'de handoff bölümü otomatik üretiliyor |
| P2-4 | ✅ | Bütün bağlantısız dosyalar SKILL.md'den bağlandı; doğrulayıcı orphan dosyaları engelliyor |
| P2-5 | ✅ | 20 API/DB skill'ine bağlam toplama adımı, dosya/sohbet çıktı modu ve "When to Skip" eklendi |
| P2-6 | ✅ | 4 büyük skill `references/` klasörüne bölündü (en büyüğü 1017 satırdan 367'ye indi); 500 satır sınırı zorunlu |
| P2-7 | ✅ | `pgbouncer-architect` CVE listesi canlı changelog/NVD kontrolüne bağlandı |
| P2-8 | ✅ | Coolify açıklaması tetik ifadeleriyle yeniden yazıldı |
| P2-9 | ✅ | `evals.md`, `evals.json` (15 senaryo) ve `trigger-evals.json` dosyalarına dönüştürüldü |
| P2-10 | ✅ | Webhook retry metni, `mastermind-logger` kısa açıklaması ve K0–K4 açıklaması düzeltildi |
| P2-11 | ✅ | Token sayacının yalnızca OpenAI encoding'lerini bildiği ve diğer modeller için yaklaşık kaldığı belirtildi |
| P2-12 | ✅ | "Experimental" bölümü kaldırıldı; multi-brain varyantları `ecosystem-reasoning`'e taşındı |
| P3-1 | ◐ | Eval'i olan skill sayısı 5'ten 19'a çıktı (8 hub, kapı skill'leri, planlama ve giriş skill'leri). Kalan skill'lere eval eklemek sürüyor |
| P3-2 | ✅ | Doğrulayıcı yeniden yazıldı; hepsi hata seviyesinde 15'ten fazla kontrol yapıyor |
| P3-3 | ✅ | GitHub Actions: build `--check`, doğrulayıcı, testler, script sözdizimi, kurulum script'lerinin çalışması |
| P3-4 | ✅ | AGENTS.md ve `.agent/workflows/create-skill.md` yeniden yazıldı; `docs/analyze/*` tarihli anlık görüntü olarak işaretlendi |

Aşağıdaki skill bazında kontrol tablosu **denetim anındaki** durumu gösteriyor.

---

## P0 — Kritik

- [x] **P0-1 · Geçersiz YAML frontmatter:** `project-analyzer`, `proje-analizcisi`
  `description: '... phrases like 'analyze the project', ...'`: Tek tırnaklı değerin içinde kaçırılmamış tek tırnaklar var ve `yaml.safe_load` hata veriyor. skills.sh açıklamayı okuyamaz, dolayısıyla skill tetiklenmez.
  **Düzeltme:** Değeri çift tırnakla sarmak ya da içteki tırnakları `''` ile kaçırmak.

- [x] **P0-2 · Yanlış skill adına işaret eden `default_prompt`:** `ecosystem-api`, `ecosystem-database`, `ecosystem-mobile`, `ecosystem-orchestration`
  `agents/openai.yaml` dosyalarında `$api-ecosystem`, `$database-ecosystem`, `$mobile-ecosystem`, `$orchestration-ecosystem` yazıyor. Doğru adlar `$ecosystem-api` vb.
  **Düzeltme:** Adları düzeltmek. Ayrıca `default_prompt` şu an çok genel ("help with this task"); iş akışını anlatan bir ifadeye çevrilmeli.

- [x] **P0-3 · Script'ler runtime'a özgü sabit bir yoldan çağrılıyor:** `project-analyzer`, `proje-analizcisi`
  `bash ~/.gemini/antigravity/skills/<ad>/scripts/phase1_discovery.sh`. Bu yol Claude Code, Codex, Cursor ve skills.sh kurulumlarında yok.
  **Düzeltme:** Skill dizinine göreli yol kullanmak (`scripts/phase1_discovery.sh`).

- [x] **P0-4 · `install_all.py` çalışmıyor ve riskli talimat içeriyor:** 4 `ecosystem-*` skill'i
  - `skills install <skill>` diye var olmayan bir CLI komutu çağrılıyor. Belgelenen komut: `npx skills add fatih-developer/fth-skills --skill <skill>`.
  - `python skills/ecosystem-*/scripts/install_all.py` yolu repo köküne bağlı; kurulumdan sonra bu yol geçersiz oluyor.
  - "Do not attempt to perform the tasks of these skills yourself. Your job is to install them" talimatı, ajanı kullanıcıya sormadan paket kurmaya yönlendiriyor.
  **Düzeltme:** Komutu düzeltmek, yolu göreli yapmak, kurulumu kullanıcı onayına bağlamak ve skill yüklü değilse iş akışının bilgi olarak yine de kullanılabilmesini sağlamak.

- [x] **P0-5 · Var olmayan bir dosyanın zorunlu okunması:** `task-decomposer`
  `skills/.curated/domains/<domain>/ECOSYSTEM.md` okunmasını **MUST** olarak istiyor. Repoda hiç `ECOSYSTEM.md` yok; bu içerik artık `ecosystem-*` skill'lerinde. README ve AGENTS.md de aynı eski yapıyı anlatıyor.
  **Düzeltme:** İlgili `ecosystem-<domain>` skill'ine yönlendirmek; README'deki "Ecosystem Paradigm" bölümünü ve AGENTS.md'yi güncellemek.

- [x] **P0-6 · Kırık referans:** `skill-security`
  Guardrail'de geçen "KESİN RED" katmanı `references/command-blacklist.md` dosyasında artık yok; başlık `ABSOLUTE DECLINE` olarak değiştirilmiş.
  **Düzeltme:** Terimi eşitlemek (bkz. P1-3; skill'in tamamen birleştirilmesi daha iyi bir çözüm).

- [x] **P0-7 · Commit edilmiş derleme çıktısı:** `session-transfer`
  `scripts/__pycache__/session_transfer_lib.cpython-313.pyc` repoda duruyor ve skill'le birlikte dağıtılıyor. `.gitignore` dosyasında `__pycache__/` ve `*.pyc` kuralı yok.
  **Düzeltme:** Dosyayı `git rm --cached` ile kaldırmak ve `.gitignore`'a kuralları eklemek.

---

## P1 — Yüksek

- [x] **P1-1 · Kayıt eksikleri (keşif)**
  - `skills.sh.json` içinde olmayan 8 skill var: `b2b-founder-roadmap`, `brand-name-lab`, `geo-auditor`, `geo-optimizer`, `plan-implement-verify-recover`, `project-focus-first`, `turkish-prompt-compiler`, `ugc-crafter`. Bunlar hiçbir grupta görünmüyor.
  - README tablolarında olmayan 24 skill var (aşağıdaki tabloda `M` kodu). Bunların arasında `session-transfer`, `skill-security`, `sqlite`, `prompt-crafter`, `plan-hardener`, `coolify-orchestrator` ve 4 `ecosystem-*` skill'i bulunuyor.
  - Sayılar birbirini tutmuyor: AGENTS.md "~58", README "70 Public", gerçek klasör sayısı 78.

- [x] **P1-2 · Tetikleme ifadesi olmayan açıklamalar:** 47 skill (tabloda `T` kodu)
  Bu açıklamalar skill'in ne yaptığını söylüyor ama *ne zaman* kullanılacağını söylemiyor ("Use when…", "Trigger on…" yok). Ağırlıklı olarak API (9/10), DB (9/10) ve Mobile skill'leri etkileniyor. Sayıya, frontmatter'ı ayrıştırılamayan 2 analyzer skill'i de dahil. Örtük tetiklemede ajanın hangi skill'i seçeceğine bu açıklama karar veriyor.
  **Düzeltme:** Her açıklamaya 3–6 somut tetik ifadesi eklemek. Model olarak `adaptive-guard`, `error-recovery` ve `output-critic` açıklamaları kullanılabilir.

- [x] **P1-3 · Birbirini kopyalayan veya çakışan skill'ler**
  | Grup | Sorun | Öneri |
  |---|---|---|
  | `skill-security` ↔ `security-auditor` | Aynı üç mod (Audit/Guard/Trust) ve aynı 4 referans dosya adı; ancak içerikleri ayrışmış (blacklist 177 satıra karşı 47 satır). `ecosystem-security` ve `security-orchestrator`, `skill-security`'yi hiç tanımıyor. | Tek skill'de birleştirmek (`security-auditor` kalsın, zengin referanslar ona taşınsın). `skill-security` ya kaldırılsın ya da yönlendirme yapan ince bir skill'e dönüşsün. |
  | `project-analyzer` ↔ `proje-analizcisi` | 380'er satırlık birebir çeviriler; her düzeltme iki kez yapılıyor. P0-1 ve P0-3 ikisinde de var. | Tek skill + "raporları kullanıcının dilinde yaz" kuralı. Türkçe şablonlar `references/` altına alınabilir. |
  | `memory-ledger` ↔ `session-transfer` ↔ `mastermind-logger` | Üçü de oturum bilgisini kalıcı hale getiriyor; sınırları tanımlı değil (`mastermind-logger` diğer ikisine hiç değinmiyor). | Her birinin açıklamasına "ne zaman diğeri" bölümü eklemek: ledger görev içinde, transfer oturumlar arasında, logger proje bilgi tabanı için. |
  | `ask-first-act-later` ↔ `project-focus-first` ↔ `assumption-checker` ↔ `plan-hardener` | Dördü de "dur ve sor" kapısı; aynı istekte birden fazlası tetiklenebilir ve kullanıcıya art arda soru dizisi gelir. | Öncelik sırası belirlemek ve her birine "diğeri aktifse atla" kuralı eklemek. |
  | `design-intelligence` ↔ `design-md-enforcer` ↔ `claude-style-coding` | UI/UX tetikleyicileri çakışıyor. | Açıklamalarda kapsamı ayırmak (sayfa üretimi/denetimi, tasarım token'ı, ürün zihniyeti). |

- [x] **P1-4 · Davranışı tümden değiştiren skill'ler örtük tetiklemeye açık**
  78 skill'in hepsinde `allow_implicit_invocation: true` var. `ask-first-act-later` ("halt any implementation") ve `project-focus-first` ("hard gate"; *herhangi* bir yeni proje, iş ya da iş akışında tetikleniyor) otomatik devreye girerse normal işleri durdurur.
  **Düzeltme:** Bu iki skill için `allow_implicit_invocation: false`. `claude-style-coding` ("Forces…") ve `mastermind-logger` için de değerlendirilmeli.

- [x] **P1-5 · İzinsiz yazma ve yıkıcı işlemler**
  - `mastermind-logger`: "No Permissions Needed: Do not ask for permission" diyerek `docs/knowledgelib/` altında dosya oluşturup değiştiriyor.
  - `coolify-orchestrator`: Değişikliklerden sonra "**always** restart the service" diyor. Canlı servisleri onaysız yeniden başlatıyor; onay yalnızca `stop_all/delete` için isteniyor. Çoklu tenant env var değişiklikleri de onaysız.
  **Düzeltme:** Canlı ortam restart'ı ve çoklu tenant değişiklikleri için `@checkpoint-guardian` handoff'u ya da açık onay adımı eklemek.

- [x] **P1-6 · Kırık skill referansları**
  - `ecosystem-orchestration` → `claw-integration` (doğrusu `claw-integration-design`)
  - `geo-auditor` → `ai-geo-optimizer` (doğrusu `geo-optimizer`)

- [x] **P1-7 · Taşınabilir olmayan yollar ve runtime'a özgü ifadeler**
  - `design-md-enforcer`: `skills/design-md-enforcer/templates/` ve `.../examples/` repo köküne bağlı. Kurulumdan sonra bulunamıyor; sonuç olarak 9 şablon ve örnek dosyası fiilen kullanılamıyor. Doğrusu `templates/` ve `examples/`.
  - `plan-implement-verify-recover`: Açıklama "Use when **Codex** is asked…" diyor. Skill Claude Code, Cursor vb. için de yayınlanıyor; ifade "the agent" olmalı. `openai.yaml` içinde `display_name` Türkçe, diğer skill'lerde İngilizce.

---

## P2 — Orta

- [x] **P2-1 · İç içe code fence render hatası:** 17 skill (`F`)
  ```` ```markdown ```` bloğunun içinde ```` ```sql ```` / ```` ```json ```` açılıyor; içteki ilk kapanış dış bloğu da kapatıyor ve kalan içerik bozuk görünüyor. 5 skill'de (`crash-analyst`, `deep-link-architect`, `mobile-perf-auditor`, `mobile-security-auditor`, `push-notification-planner`) fence dosya sonuna kadar kapanmıyor.
  **Düzeltme:** Dış blokta dört backtick (````` ```` `````) ya da `~~~` kullanmak.

- [x] **P2-2 · Cümle ortasında kesilmiş `short_description`:** 29 skill (`S`)
  `generate_openai_yaml.py` açıklamayı 117 karakterde kesip `...` ekliyor ("…and role-based access control policies..."). skills.sh kartlarında yarım cümle görünüyor.
  **Düzeltme:** Her birine elle yazılmış tam bir kısa açıklama. Script de kesmek yerine uyarı verecek şekilde değiştirilmeli.

- [x] **P2-3 · Handoff bölümü olmayan skill'ler:** 59 skill (`H`)
  AGENTS.md ve README "🔗 Next Steps" desenini temel mimari olarak anlatıyor, ama skill'lerin çoğunda bu bölüm yok. Öncelik API ve DB zincirlerinde olmalı (ör. `contract-first-designer` → `api-mock-designer` → `sdk-scaffolder`; `schema-architect` → `access-policy-designer` → `seed-data-generator`).

- [x] **P2-4 · Bağlantısız (orphan) referans dosyaları:** 12 skill (`O`)
  Dosya var ama `SKILL.md` ona hiç atıf yapmıyor, dolayısıyla ajan dosyayı hiç yüklemiyor:
  - `references/EXAMPLES.md`: `agent-reviewer`, `assumption-checker`, `claw-integration-design`, `context-compressor`, `error-recovery`, `memory-ledger`, `output-critic`, `parallel-planner`, `tool-selector`
  - `b2b-founder-roadmap/templates/ROADMAP_STATE.template.md`, `sqlite/references/README.md`, `design-md-enforcer` şablonları (bkz. P1-7)

- [x] **P2-5 · İnce API/DB skill'leri:** 20 skill (API 10 + DB 10; `pgbouncer-architect` ve `sqlite` hariç)
  65–85 satırlık, aynı şablondan türemiş dosyalar. Eksikler:
  - girdi toplama adımı (hangi DB veya dil, mevcut şema var mı?)
  - "When to Skip" bölümü
  - referans dosyası
  - handoff bölümü

  Ayrıca hepsi her çalışmada `docs/api-report/` veya `docs/database-report/` altına **zorunlu olarak** iki dosya yazıyor. Kullanıcı yalnızca bir soru sorduğunda da dosya oluşuyor.
  **Düzeltme:** Mobile skill'lerinin yapısını (Workflow / When to Skip / References / Next Steps) şablon almak; dosya yazımını isteğe bağlı yapmak.

- [x] **P2-6 · Aşırı uzun SKILL.md:** `b2b-founder-roadmap` (1001), `project-focus-first` (615), `security-auditor` (565), `pgbouncer-architect` (555)
  Her tetiklenmede bağlamın tamamı yükleniyor. Aşama ve mod detayları `references/` klasörüne taşınmalı; `SKILL.md` 300–400 satırın altında kalmalı.

- [x] **P2-7 · Eskiyen statik içerik:** `pgbouncer-architect`, `skill-comparator`
  "Known Active CVEs (as of early 2026)" altında statik bir liste ve `CVE-2024-XXXX` yer tutucusu var.
  **Düzeltme:** Listeyi örnek olarak işaretlemek ve ajana pgbouncer.org changelog'unu canlı kontrol ettiren bir adım eklemek.

- [x] **P2-8 · `coolify-orchestrator` açıklaması zayıf**
  Tetik ifadesi yok. Aynı skill'in harici yayınlanmış sürümünde "my deploy failed", "service is down", "add a new tenant" gibi zengin tetikleyiciler var; repo sürümü geride kalmış.

- [x] **P2-9 · `project-focus-first` eval formatı**
  `evals/evals.md` Markdown biçiminde; diğer skill'lerdeki `evals.json` / `trigger-evals.json` formatına çevrilmeli.

- [x] **P2-10 · Tutarsızlıklar**
  - `webhook-architect`: Metin "5 failed retries" diyor, örnek politika 3 retry kullanıyor.
  - `mastermind-logger`: `short_description` "appends them to a knowledge base" diyor, gövde ise "append etme, entity dosyalarını güncelle" diyor.
  - `ecosystem-security`: Harita `K0-K4` kısaltmasını açıklamadan kullanıyor (adaptive-guard'daki karşılığı "Layer").

- [x] **P2-11 · `turkish-prompt-compiler` token sayımı**
  `count_tokens.cjs` yalnızca `tiktoken` (OpenAI) encoding'lerini destekliyor. Claude veya Gemini hedeflendiğinde sayım yaklaşık kalıyor. SKILL.md bunu açıkça belirtmeli ya da sağlayıcının token sayma API'sini önermeli.

- [x] **P2-12 · README'deki "Experimental" bölümü**
  `multi-brain-debate/-experts/-score` README'de "Experimental (Preview)" olarak geçiyor, ama `skills.sh.json` içinde normal yayında ve ayrı bir `.experimental` klasörü yok. Durum netleştirilmeli.

---

## P3 — İyileştirme

- [~] **P3-1 · Eval kapsamı:** 78 skill'in yalnızca 5'inde `evals/` var (`E`). Önce en çok tetiklenen ve kapı işlevi gören skill'ler için `trigger-evals.json` eklenmeli: `task-decomposer`, `checkpoint-guardian`, `ask-first-act-later`, `project-focus-first`, API/DB giriş skill'leri.
- [x] **P3-2 · Doğrulayıcıyı güçlendirmek** (`scripts/validate_curated_skills.py`):
  - frontmatter'ı `yaml.safe_load` ile gerçekten ayrıştırmak
  - `openai.yaml` içinde `$<skill-name>` kontrolü
  - `...` ile biten `short_description` uyarısı
  - `skills.sh.json` ve README kaydı kontrolü
  - `@skill` referanslarının var olduğunu doğrulamak
  - orphan dosya ve iç içe fence uyarısı
  - `__pycache__` / `.pyc` yasağı
- [x] **P3-3 · CI:** Doğrulayıcıyı her push ve PR'da çalıştıran bir GitHub Actions iş akışı. Şu an repoda `.github/` klasörü yok.
- [x] **P3-4 · Eskimiş dokümanlar:** `docs/analyze/*` (2026-04, 61 skill, Windows yolu) ve AGENTS.md'deki skill sayısı ile ECOSYSTEM.md anlatımı güncellenmeli.

---

## Skill bazında kontrol tablosu

**Kodlar:**
- `F` iç içe fence
- `T` tetikleme ifadesi yok
- `H` handoff bölümü yok
- `R` `skills.sh.json` kaydı yok
- `M` README'de yok
- `O` bağlantısız dosya
- `S` kesik `short_description`
- `E` eval yok

| Skill | Kodlar | Ek not |
|---|---|---|
| `access-policy-designer` | F T H S E |  |
| `accessibility-enforcer` | F T S E |  |
| `adaptive-guard` | H E |  |
| `agent-reviewer` | T H O E |  |
| `api-mock-designer` | T H S E |  |
| `api-observability-planner` | T H S E |  |
| `app-store-reviewer` | T S E |  |
| `ask-first-act-later` | T H M E | örtük tetikleme kapatılmalı; kapı skill'leriyle çakışma |
| `assumption-checker` | T H O E |  |
| `auth-flow-designer` | H S E |  |
| `b2b-founder-roadmap` | H R M O S E | 1001 satır; ROADMAP_STATE şablonu bağlantısız |
| `brand-name-lab` | H R M E |  |
| `breaking-change-detector` | T H E |  |
| `changelog-generator` | T H E |  |
| `checkpoint-guardian` | T H E |  |
| `claude-style-coding` | T H M E | kapı/tasarım skill'leriyle çakışma |
| `claw-integration-design` | H M O |  |
| `context-compressor` | O E |  |
| `contract-first-designer` | F T S E |  |
| `coolify-orchestrator` | T H M E | onaysız otomatik restart; zayıf tetik ifadeleri; `ssh user@coolify-server` |
| `crash-analyst` | F T H S E |  |
| `data-lineage-tracer` | T H S E |  |
| `data-masker` | F T H S E |  |
| `deep-link-architect` | F T S E |  |
| `design-intelligence` | T H M E |  |
| `design-md-enforcer` | T H M O E | repo köküne bağlı `skills/design-md-enforcer/...` yolları |
| `ecosystem-api` | M E | P0: default_prompt `$api-ecosystem`; install_all.py yanlış CLI |
| `ecosystem-database` | M E | P0: default_prompt `$database-ecosystem`; install_all.py yanlış CLI |
| `ecosystem-mobile` | M E | P0: default_prompt `$mobile-ecosystem`; install_all.py yanlış CLI |
| `ecosystem-orchestration` | M E | P0: default_prompt `$orchestration-ecosystem`; install_all.py yanlış CLI; `claw-integration` referansı |
| `ecosystem-security` | H E | skill-security'yi kapsamıyor |
| `error-recovery` | H O E |  |
| `geo-auditor` | R M E | `ai-geo-optimizer` → `geo-optimizer` |
| `geo-optimizer` | H R M E |  |
| `index-advisor` | F T H S E |  |
| `jev-orchestrator` | — |  |
| `mastermind-logger` | H M E | izinsiz dosya yazımı; short_description ile gövde çelişkili |
| `memory-ledger` | O E |  |
| `migration-strategist` | T H S E |  |
| `mobile-perf-auditor` | F T S E |  |
| `mobile-security-auditor` | F T H S E |  |
| `multi-brain` | E |  |
| `multi-brain-debate` | T H E |  |
| `multi-brain-experts` | T H E |  |
| `multi-brain-score` | T H E |  |
| `offline-sync-designer` | T H S E |  |
| `onboarding-designer` | T H S E |  |
| `output-critic` | T H O E |  |
| `parallel-planner` | T H O E |  |
| `pgbouncer-architect` | H E | statik CVE listesi, `CVE-2024-XXXX` yer tutucusu; 555 satır |
| `plan-hardener` | T H M E |  |
| `plan-implement-verify-recover` | H R M E | açıklama "Use when Codex…" (runtime’a özgü) |
| `proje-analizcisi` | T H E | P0: geçersiz YAML frontmatter; `~/.gemini/antigravity` yolu; project-analyzer ile ikiz |
| `project-analyzer` | T H E | P0: geçersiz YAML frontmatter; `~/.gemini/antigravity` yolu |
| `project-focus-first` | H R M | örtük tetikleme kapatılmalı; evals.md JSON değil; 615 satır |
| `prompt-crafter` | H M |  |
| `protocol-selector` | T H S E |  |
| `push-notification-planner` | F T H S E |  |
| `query-budget-enforcer` | F T H S E |  |
| `query-explainer` | H S E |  |
| `rate-limit-strategist` | F T H S E |  |
| `react-flow` | H E |  |
| `release-orchestrator` | T S E |  |
| `schema-architect` | F T S E |  |
| `schema-diff-analyzer` | F T S E |  |
| `sdk-scaffolder` | F T H S E |  |
| `security-auditor` | H E | skill-security ile çakışma; 565 satır |
| `security-orchestrator` | H E |  |
| `seed-data-generator` | F T E |  |
| `session-transfer` | T M E | P0: commit edilmiş `.pyc` |
| `skill-comparator` | H E |  |
| `skill-security` | T H M E | P0: olmayan "KESİN RED" katmanı; security-auditor ile çakışma |
| `sqlite` | H M O E |  |
| `task-decomposer` | T H S E | P0: var olmayan `.curated/.../ECOSYSTEM.md` zorunlu okuma |
| `tool-selector` | H O E |  |
| `turkish-prompt-compiler` | H R M E | yalnızca tiktoken (OpenAI) sayacı |
| `ugc-crafter` | H R M |  |
| `webhook-architect` | F T H S E | DLQ 5 retry ↔ örnek 3 retry tutarsız |

---

## Önerilen uygulama sırası

1. **Tek commit'lik hızlı düzeltmeler (P0 tamamı + P1-6):** YAML, `default_prompt`, göreli yollar, KESİN RED, `.pyc` / `.gitignore`, kırık referanslar.
2. **Keşif:** P1-1 (kayıtlar), P1-2 (tetik ifadeleri), P2-2 (`short_description`).
3. **Davranış güvenliği:** P1-4 (örtük tetikleme), P1-5 (onay adımları).
4. **Birleştirmeler:** P1-3 (`skill-security` → `security-auditor`, analyzer ikizleri).
5. **Doğrulayıcı ve CI (P3-2, P3-3):** Böylece aynı hatalar geri gelmez.
6. **Kalite:** P2-1, P2-3, P2-4, P2-5, P2-6 ve eval'ler.
