# Çeviri paketi boyutu ve kapsam seçimi

Bu politika, yeni içerik paketlerinin kapsamını belirler. Teknik doğruluk, oyuncuya görünürlük ve terminoloji kuralları için [Çeviri standardı](STYLE_GUIDE.md), [QA kuralları](QA_RULES.md) ve kaynak kapıları geçerliliğini korur.

## Hedef boyut

- Varsayılan hedef, paket başına yaklaşık **500 alan** ve **250–400 benzersiz kaynak metindir**.
- Alan sayısı ile benzersiz kaynak metin sayısı ayrı izlenir. Tekrarlanan satırlar iş yükünü aynı ölçüde artırmadığı için paket seçimi yalnızca satır sayısına dayanmaz.
- Birbirine çok benzeyen metinlerin tekrarlandığı tutarlı bir ailede paket **800–1000 alana** çıkabilir; benzersiz metin sayısı ve inceleme yükü yine yönetilebilir tutulur.
- Tek ve doğal bir aile hedefin altında kalıyorsa sırf sayıyı doldurmak için ilgisiz metinler eklenmez. Küçük, tutarlı kapsam kabul edilir.

## Kapsam seçimi

1. Güncel main kataloğu ve pinned kaynak üzerinden kalan görünür adayları yeniden çıkar.
2. Önce tek bir oyuncu akışı, içerik ailesi veya yakın temalı grup seç; adayları sayı uğruna farklı konulardan karıştırma.
3. Alan ve benzersiz kaynak metin sayılarını birlikte hesapla. Hedefe ulaşmak için gerekiyorsa aynı temadaki komşu aileleri ekle.
4. Yeni kapsamda tekrar edecek özel ad ve terimleri, özellikle önceki sürümlerde yeniden düzeltilenleri, bağlamıyla denetle. Kesin karşılığı LOCKED olarak kaydet; ad ve cümle içindeki yanlış varyantı QA testiyle reddet. Belirsiz kararı REVIEW durumunda tut.
5. Exact-source manifesti, katalog allowlisti ve CI kaynak kapısını aynı kapsamı tarif edecek şekilde güncelle.
6. Çeviriyi çalışma sırasında küçük, bağlamı koruyan dilimlerde ele al; yayımlanabilir adayda tutarlı tema ve kaynak manifesti altında birleştir.
7. Sol doğrulama ve yayın sorumluluğunu sürdürür. Luna adayı kaynak pinini ve manifestini hazırlar; doğrulanmamış paketi yayımlanmış gibi işaretlemez.

## İstisnalar

Güvenli kaynak kapsamı, runtime bağı veya insan inceleme kapasitesi daha küçük bir dilim gerektiriyorsa kapsam dar tutulur. Gerekçe checkpoint'e yazılır. Hedefler kota değildir; konu bütünlüğü ve kaynak doğruluğu önceliklidir.
