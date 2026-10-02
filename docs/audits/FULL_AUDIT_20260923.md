# Teknik inceleme — 23 Eylül 2026

İncelenen kaynak `3f54a6900de2ffa75e24f5cc2ec9306e6172d033`, FU 6.5.8 commit'i `329e714b3fe87571055c8ad7aa38135d199d3317` idi.

| Sorun | Düzeltme |
| --- | --- |
| Katmanlı alanlarda eksik temel dosya kaynak kontrolünü atlatabiliyordu. | FU yamasına bağlı 120 alan doğrudan yama değerinden doğrulandı. |
| Eski build raporu kural/araç değişikliğinden sonra kullanılabiliyordu. | Bütün Python/JSON/Lua girdileri ve terimler hash kontrolüne bağlandı; gerçek commit kaydedildi. |
| Renk/sayı izinleri ilgisiz hataları da geçirebiliyordu. | 18 renk ve 20 sayı düzeltmesi tam alana, iki dildeki metne ve gerekçeye bağlandı. |
| Sürüm listeleri katalogla tam eşleşmeyebiliyordu. | Kaynak/alan/çeviri eşitliği ve tekillik zorunlu tutuldu. |
| Ek FU dosyaları taramaya sızabiliyordu. | Temiz Git kökü ve ek dosya kontrolü eklendi. |
| Tarayıcı yama test değerlerini metin sayabiliyor, Lua Unicode'unu bozabiliyordu. | Son yama değerleri ve gerçek Lua metinleri kullanıldı. |
| Windows kod sayfası, Lua kitaplığı ve satır sonları testleri bozuyordu. | UTF-8/LF üretimi, Lua 5.4 alternatifi ve Windows testleri eklendi. |
| Eski kurulum bağlantısı ve klasör birleştirme adımı hatalıydı. | Güncel paket bağlantısı ve temiz yükseltme adımı yazıldı. |
| Kapsam taraması bazı yardımcı modül değişikliklerinde çalışmıyordu. | Eksik workflow tetikleyicileri eklendi. |

180 test ve tam FU kaynak derlemesi geçti. Bu bakım çeviri metinlerini veya paket sürümünü değiştirmedi. Sonraki oyun denemeleri [test notlarında](../LQA_CHECKLIST.md), güncel paket sonucu [paket raporunda](../../dist/build-evidence.json) bulunur.
