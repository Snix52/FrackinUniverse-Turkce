# Metin kontrolleri — 22 Eylül 2026

v0.45.1 bakımında şu düzeltmeler yapıldı:

- Lua replacements için gerçek görünür metin konumları belirlendi; kod, yorum ve diğer dizgeler korunur.
- Doğru terimin aynı cümledeki yanlış varyantı gizlemesi önlendi.
- Beş görünür `[Tile]` etiketi `[Zemin]` yapıldı; teknik anahtarlar değişmedi.
- Mech'in dolu depo ve farklı yakıt türü uyarıları çevrildi. Yakıt tüketimi ve normal doldurma yolları test edildi.
- Üç görev ifadesi ve bir nokta sonrası boşluk düzeltildi.
- Kaynak değişikliğiyle üretilen paket dosyalarının ayrımı ve yayın sırası kontrolü eklendi.
- Lua 5.4 ile yazı animasyonu ve yakıt davranışı testleri eklendi.

8.024 katalog alanının dokuz Türkçe hedef metni değişti. Mevcut 506 sabit terim korundu. KheAA Router, statWindow ve Mech şablonları kaynaklarıyla eşleştirildi; istisnalar tam dosya/alan ve metne bağlandı.

152 test yöntemi, 14 yazı animasyonu ve 8 yakıt senaryosu bu bakımın kontrol kapsamındaydı. Güncel test akışı [QA_PIPELINE.md](../QA_PIPELINE.md), oyun denemeleri [test notları](../LQA_CHECKLIST.md) içinde.
