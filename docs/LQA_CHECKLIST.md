# FU Türkçe — oyun içi LQA

**Durum: NOT TESTED.** Statik QA veya başarılı paketleme bu durumu PASS yapmaz.

Her test kaydına oyun/FU sürümü, kullanılan `source_commit`, ZIP SHA256, ekran çözünürlüğü, UI ölçeği, diğer dil/font modları, test eden kişi ve tarih yazılmalıdır. Sonuç ekran görüntüsü ve gerekiyorsa `starbound.log` ile desteklenmelidir.

| Kontrol | Uygulama | Sonuç |
|---|---|---|
| Türkçe font | ı/İ/ğ/Ğ/ş/Ş/ö/Ö/ü/Ü/ç/Ç içeren envanter, görev, diyalog ve butonları aç. | NOT TESTED |
| Tooltip ve glyph | U+E024 içeren zırh/silah açıklamalarını aç; ikon, renk, satır ve signed bonusları karşılaştır. | NOT TESTED |
| Arayüz taşması | Araştırma, üretim, dükkân, görev günlüğü, uzun ad ve butonları farklı UI ölçeklerinde incele. | NOT TESTED |
| Research bağlamı | Araştırma para birimi ile Araştır butonunun isim/fiil ayrımını kontrol et. | NOT TESTED |
| Görev → üretim → teslim | İstenen eşyayı doğru araştırma ve tezgâhtan üret, envanter adını ve teslimi doğrula; Master Manipulator zincirini dahil et. | NOT TESTED |
| Makine/hedef kaynak düzeltmeleri | Armorworks adı yanlış tekrarlanan görevlerde istenen gerçek hedefi; pet healing alt başlığını doğrula. | NOT TESTED |
| NPC bağlamı | Konuşan kişi, hitap, bağlam, cümle kesilmesi ve seçeneklerin doğru eyleme bağlanmasını kontrol et. | NOT TESTED |
| TAB istisnaları | Plebiancap görev metni ve Nightar kısa kılıç açıklamasında normal boşlukla okunurluğu doğrula. | NOT TESTED |
| Ayrı anlamlar | Incinerator nesnesi/silahı, Field Generator nesnesi/EPP'si, Oxygen malzemesi/tehlikesi ayrımını incele. | NOT TESTED |

Tek bir ekranın geçmesi bütün oyun içi LQA'nın geçtiğini göstermez. Test edilmemiş satırlar NOT TESTED kalır. Hatalar ayrı issue'da gerçek asset/pointer, beklenen/görülen sonuç ve kanıtla kaydedilir.

## v0.45.1 hedefli oyun içi kontrol (NOT TESTED)
- Tricorder: Cangıl, Çamur, Buz, Sulu Kar ve Kar `[Zemin]` etiketlerini aç; satır taşması ve stat gösterimini kontrol et.
- Mech yakıtı: dolu depoyu doldurmayı dene; başka yakıt türünü eklemeyi dene. Türkçe uyarı ve tüketim olmamasını kontrol et. Sonra uyumlu yakıtla normal doldurmayı dene.
- SAIL ve istasyon: Türkçe karakterleri yazı animasyonunda, atlamada ve renkli metinlerde kontrol et.
- Gate/ship repair görevleri: düzeltilen Türkçe ifadeleri ve renk sınırlarını kontrol et.
