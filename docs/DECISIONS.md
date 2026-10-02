# Çeviri kararları

Güncel karşılıklar [terim sözlüğünde](TERMINOLOGY.md), bağlama bağlı istisnalar `tools/translation_memory_exceptions.json` içindedir.

## Bağlama göre karşılıklar

| Kaynak | Karar |
| --- | --- |
| Research | Sistem ve kaynak adı “Araştırma”; eylem/düğme “Araştır”. |
| Buy | Dükkânda “Satın Al”; takasta “Takas Et”; işe alma ekranında “İşe Al”. |
| Incinerator, Field Generator, Oxygen | Nesne, silah, ekipman, malzeme ve tehlike bağlamları ayrı değerlendirilir. |
| Jungle | Genel kullanım “Tropik Orman”; görev/konum adındaki özel bölüm korunur. |
| `[Tile]` | Beş görünür durum etiketinde `[Zemin]`; teknik durum anahtarları aynı kalır. |
| Pulse Jump | “Enerji Sıçraması”; oyuncunun havadaki ikinci sıçramasını anlatır. |

## Özel adlar

`Precursor`, `Cthulhu`, `Erchius` ve `Lunari` gibi özel adlar korunur. Açıklayıcı görev ve yer adları Türkçeleştirilir: “Kadim Tapınak”, “Su Dağıtım Merkezi”, “Büyük Arena”. Karma adlarda özel kısım kalır: “Evernight Tropik Ormanı”, “Fae Ormanı”, “Gigant Dağı”.

`nightfort` teknik kimliği değişmez; görünen S.A.I.L. metni “Gece Hisarı'nı Ziyaret Et”tir. `Takeshi's Castle` dış referans olarak korunur. Marka ve kişi adları, dosya adına bakılarak çevrilmez.

## Metin ve kapsam

- Türkçe harfler korunur; ayrı ASCII sürümü hazırlanmaz.
- Görev metnindeki eşya adı envanter ve üretim menüsüyle eşleşir. Kaynakta hatalı hedef varsa gerçek görev koşulu kontrol edilir.
- Cümle içindeki sabit terimler Türkçe ek alabilir. Genel sözcüklerin farklı anlamları bağlamıyla kaydedilir.
- Kaynak sayı, renk veya biçim hataları için tam alana bağlı istisna gerekir.
- `biomes/` içindeki `friendlyName` ve `liquids/` içindeki `description` alanları görünür metin olarak doğrulanmadı. Sıvı eşya açıklamaları `.liqitem` dosyalarından çevrilir.
- NPC konuşmalarında konuşan ve muhatap tür ayrı incelenir. Floran tıslaması ve Glitch duygu önekleri korunur.

Sürüm bazındaki eklemeler [sürüm notlarında](../CHANGELOG.md), ayrıntılı diyalog düzeltmeleri [inceleme kayıtlarında](reviews/) bulunur.
