# Çeviri dosyalarının kontrolü

## Metin ve dosya yapısı

- JSON ve JSON Patch geçerli olmalı.
- Yalnızca oyuncuya görünen alanlar değişmeli; kimlik, yol, betik ve oyun parametreleri korunmalı.
- Kaynak İngilizce metin, dosya yolu ve alan konumu kullanılan FU commit'iyle eşleşmeli.
- Ana katalog ve sürüm listelerinde aynı alanın İngilizce/Türkçe değerleri eşit olmalı. Eksik veya yinelenen kayıt kabul edilmez.
- Sabit terimler ve bağlama bağlı karşılıklar `tools/locked_terms.json` ile `tools/translation_memory_exceptions.json` üzerinden kontrol edilir.

## Biçimlendirme

Değişkenler, `%s` ve `%%` gibi biçim belirteçleri, tuş kodları, simgeler, renkler, sayılar, işaretler, sekmeler ve satır sonları kaynakla eşleşmeli. Türkçe harfler korunmalı; boş veya geçici açıklamalı çeviri eklenmemeli.

Kaynaktaki hata için istisna gerekiyorsa tam dosya/alan, kaynak metin, çeviri ve gerekçe kaydedilir. `allow_tab_fix`, `allow_color_fix` veya `allow_number_fix` bayrağı tek başına yeterli değildir.

## Lua ve oyun içeriği

Lua çevirilerinde yalnızca kaydedilmiş görünür metinler değişir. Kod, yorumlar ve diğer dizgeler aynı kalır. Kaynak şablonları FU dosyalarıyla karşılaştırılır.

Eşya ve ekipmanın oyundaki kullanımını tarif, araştırma, görev veya nesne bağlantısından kontrol et. Hasar, mermi, yetenek, istatistik, tarif, efekt ve betik alanları çeviri kapsamına girmez.

## Paket

Tam test sırası [QA_PIPELINE.md](QA_PIPELINE.md) içinde. Paket, `tools/kaynaklar.json` içindeki FU commit'inden hazırlanır. ZIP ve `FU_Turkce/` aynı dosyaları içermeli; kaynak ve paket bilgileri `dist/build-evidence.json` dosyasına yazılır.

## Oyun kontrolü

Yeni metinlerde Türkçe harfleri, taşmaları, görevdeki eşya adlarını, konuşan karakteri, renkleri ve düğmeleri kontrol et. Oynanış denemeleri [test notlarında](LQA_CHECKLIST.md) tutulur.
