# Çeviri hazırlama

`tools/plan_translation.py`, kalan metinlerden bir çeviri taslağı hazırlar. Kaynak olarak `tools/kaynaklar.json` içindeki committe temiz bir FU Git kopyası kullanılır.

## Taslak oluşturma

Komutları repo kökünde çalıştır:

```text
python tools/plan_translation.py --source fu_source --output planning_output/next
```

Belirli bir içerik ailesi için `--family` kullan:

```text
python tools/plan_translation.py --source fu_source --family dialog --output planning_output/dialog
python tools/plan_translation.py --source fu_source --family objects/crafting --output planning_output/crafting
```

Çıktıda `packet.json`, inceleme tablosu ve öncelik kuyruğu bulunur. Mevcut bir taslak klasörünün üzerine yazılmaz. Kaynak, katalog veya kurallar değiştiyse yeni klasöre taslak hazırla.

## Öncelikler

`tools/translation_priorities.json` görev ve uyarıları P0; diyalog, üretim ve diğer içerikleri ilgili önceliklerine ayırır. Bu kurallar karşılaşma sıklığı ölçümü değildir; oyundaki kullanıma göre kontrol edilir.

`confirmed` görünür olduğu doğrulanan adayları, `review` inceleme gereken alanları, `lua_review` Lua metni adaylarını içerir. Paket `confirmed` grubundan seçilir. Yüksek öncelikli diğer adayların görünürlüğünü de incele.

Dosyadaki görev, tarif, NPC ve betik bağlantıları kullanım yerini bulmaya yardımcı olur. Temel oyundaki dosyalar, koşullu yamalar ve diğer modlar gerektiğinde ayrıca kontrol edilir.

## Metinleri inceleme

1. `en`, `occurrences`, bağlam anahtarı, `tm_suggestions` ve `locked_terms` alanlarını oku.
2. Konuşanı, muhatabı, eşyayı veya ekranı kaynak dosyalarıyla eşleştir. Aynı İngilizce cümlenin farklı kullanımlarını ayrı değerlendir.
3. Türkçeyi `tr` alanına yaz. Mevcut çeviri önerisinin anlamını ve terimlerini kontrol et.
4. Bağlamı inceledikten sonra `context_reviewed=true` yap. Kullanım yerini `runtime_evidence` ve `runtime_review.evidence` içinde kaynak dosyası ve kısa açıklamayla kaydet.
5. Yanlış gruplama varsa kuralı düzelterek taslağı yeniden hazırla. Alan listesini veya girdi hashlerini elle değiştirme.

Taslakta yalnız `tr`, `context_reviewed`, `runtime_evidence`, `runtime_review` ve `measurements` düzenlenir. Ölçüm alanlarına ancak kaydedilmiş süre ve sonuçları yaz.

## Ön kontrol ve yayın

```text
python tools/plan_translation.py --source fu_source --check-packet planning_output/next/packet.json
```

Bu kontrol kaynak, kapsam ve biçimlendirmeyi yeniden doğrular. Boş çeviri, değişmiş girdi veya eksik bağlam incelemesi reddedilir. Kaynakla aynı kalabilen özel adların kuralları `locked_terms.json` içinde tutulur; bu izin açıklama cümlelerini İngilizce bırakmak için kullanılamaz.

Taslak kontrolü kataloğu değiştirmez. Türkçesi incelenen paket, sürüm listesi ve ilgili kaynak kontrolüyle birlikte eklenir. Ardından [test ve paketleme](QA_PIPELINE.md) adımları uygulanır.

[Paket kapsamı](TRANSLATION_BATCH_POLICY.md) · [Dil rehberi](STYLE_GUIDE.md)
