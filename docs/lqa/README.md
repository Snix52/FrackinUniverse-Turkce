# Ekran ve diyalog notları

Bu belgeler belirli sürümlerde değişen metinleri ve hedefli kontrolleri listeler. Güncel genel oynanış denemesi [oyun testi belgesinde](../LQA_CHECKLIST.md).

- [Arayüz düzeltmeleri](LQA_UI_20260925.md)
- [Slimeperson ve Shadow S.A.I.L. konuşmaları](LQA_SHIP_SAIL_20260926.md)
- [v0.66: yetiştirme ve yer imi](LQA_V066_20261001.md)
- [v0.67: ilk NPC diyalog dilimi](LQA_V067_20261001.md)
- [v0.68: ikinci NPC diyalog dilimi](LQA_V068_20261001.md)
- [v0.69: üçüncü NPC diyalog dilimi](LQA_V069_20261001.md)
- [v0.70: dördüncü NPC diyalog dilimi](LQA_V070_20261001.md)

## NPC kaynakları

Temel oyunun `dialog/converse.config` dosyası FU kaynak kopyasında bulunmaz; ilgili çeviriler FU'nun `converse.config.patch` değerlerinden doğrulanır. ElDuukhar köylüsü kendi `elduuconverse.config` dosyasını kullanır; temel dosyaya bağlantısı `breakObject` içindir.

Bir NPC'nin dosyada konuşma havuzuna bağlanması, bütün konuşmacı/muhatap dallarının oyunda seçildiğini göstermez. Yeni replikleri ilgili karakterlerle kontrol et. Ayrıntılı önce/sonra kayıtları [reviews/](../reviews/) altında tutulur.
