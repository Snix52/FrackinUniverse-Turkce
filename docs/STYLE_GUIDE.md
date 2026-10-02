# Çeviri rehberi

Öncelik sırası: teknik bütünlük, doğru anlam, anlaşılabilirlik, terim tutarlılığı, doğal Türkçe, karakter tonu ve kaynak biçimi.

## Dil ve bağlam

- Kısa veya belirsiz bir metni tek başına çevirme. Dosyasını, komşu metinleri ve oyundaki kullanımını incele.
- İngilizce cümle düzenini kopyalama. Türkçede gereksiz kalan zamirleri ve dolambaçlı ifadeleri çıkar.
- Kaynakta olmayan bilgi, şaka veya küfür ekleme. Karakterin konuşma biçimini ve sertlik düzeyini koru.
- Floran'ın tıslamasını ve Glitch'in duygu öneklerini koru. Fenerox gibi kısa konuşan karakterlerin cümlelerini gereksiz yere uzatma.
- Yerleşik bilimsel karşılıkları kullan. Özel adları ve evrene özgü terimleri bağlamıyla değerlendir.
- Türkçe harfleri kullan. Font sorunu için çeviriyi ASCII'ye dönüştürme.

## Terimler

[Terim sözlüğünü](TERMINOLOGY.md) ve mevcut çevirileri kontrol et. `LOCKED` karşılıklar sabittir. Aynı kaynak metnin farklı anlamları varsa gerekçesini ilgili bağlamla birlikte kaydet.

Yeni, tekrar eden bir terimi `tools/locked_terms.json` içine ekle. Ad ve cümle içindeki kullanımlarını kontrol et; yanlış karşılıkların reddedildiğini test et. Genel sözcükleri bağlamlarını incelemeden tek karşılığa zorlama.

Oyuncuya görünen Türkçe adın yanına İngilizce karşılığını parantez içinde ekleme. Emin olmadığın bir karşılığı tahmin etmek yerine inceleme için işaretle.

## Görev ve arayüz

Görev hedefini kısa bir eylemle yaz: “Topla”, “Üret”, “Konuş”, “Teslim et”. Eşya ve makine adları envanterle aynı olmalı.

Düğmelerde kısa karşılıklar kullan: `Craft → Üret`, `Research → Araştır`, `Cancel → İptal`, `Apply → Uygula`, `Close → Kapat`. Dar bir alanda metni kısaltırken anlamını koru.

Eşya açıklamasında önce işlevi anlat; kaynak metnin mizahını ve atmosferini koru.

## Teknik alanlar

Yalnızca oyuncuya görünen metinleri çevir. JSON anahtarları, kimlikler, dosya yolları, betik/işlev adları ve değişkenler aynı kalır.

`%s`, `%d`, `{0}`, `{item}`, `$variable`, `\n`, `^red;`, `^reset;` gibi biçim ve değişken kodlarını koru. Kaynaktaki bir biçim hatasını düzeltmek gerekiyorsa ilgili alan ve gerekçeyi kontrol kurallarına ekle.

Çeviriyi kaydetmeden önce [otomatik kontrolleri](QA_RULES.md) çalıştır. Yeni ekran, uzun metin ve görev zincirlerini [oyunda kontrol et](LQA_CHECKLIST.md).
