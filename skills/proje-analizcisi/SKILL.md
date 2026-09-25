---
name: proje-analizcisi
description: "Kullanımdan kaldırılmış Türkçe takma ad: project-analyzer skill'ine yönlendirir. Kullanıcı açıkça $proje-analizcisi çağırdığında kullan; yeni kurulumlar için project-analyzer tercih edilmeli (Türkçe raporları o üretir)."
---

# Proje Analizcisi (Takma Ad)

Bu skill `project-analyzer` ile birleştirildi. İki kopyanın ayrı ayrı bakımı hatalara yol açtığı için içerik tek kaynakta tutuluyor. `project-analyzer`, kullanıcı Türkçe yazdığında raporları Türkçe dosya adlarıyla (`01-proje-genel-bakis.md` vb.) üretir.

## Ne yapmalı

1. `project-analyzer` skill'i kuruluysa onu çağır ve talimatlarını eksiksiz uygula. Raporları Türkçe yaz.
2. Kurulu değilse kullanıcıya şu komutu öner ve onay almadan çalıştırma:

   ```bash
   npx skills add fatih-developer/fth-skills --skill project-analyzer
   ```

3. Kullanıcı kurmak istemezse analizi yine yap: proje yapısını, bağımlılıkları, mimariyi, kod kalitesini, güvenliği, performansı ve testleri gerçek dosyalara bakarak incele. Bulguları `docs/analyze/` altına şu dosyalarla yaz: `01-proje-genel-bakis.md`, `02-mimari-ve-kod-kalitesi.md`, `03-riskler-ve-oneriler.md` ve API varsa `04-api-endpoint-listesi.md`.

## 🔗 Next Steps & Handoffs

- Asıl skill: `@project-analyzer`
