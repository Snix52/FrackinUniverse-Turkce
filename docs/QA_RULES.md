# FU TÜRKÇE QA Kuralları

Bu dosya `STYLE_GUIDE.md` içindeki Anayasa'nın otomatik ve pratik kontrol özetidir.

## Statik kapı
- JSON/JSON Patch geçerli olmalı.
- Yalnızca oyuncuya gösterilen alanlar değişmeli.
- Teknik key, ID, asset yolu ve script referansı değiştirilmemeli.
- Placeholder, printf biçim belirteçleri (`%s`, `%%` vb.) ve tuş kodları birebir korunmalı.
- Renk kodu değişikliği yalnızca açıkça kaydedilmiş kaynak hatası düzeltmesinde kabul edilir.
- Oyuncu metninde geçici İngilizce parantez glossu bırakılmamalı.
- Türkçe karaktersiz ASCII sürümü üretilmemeli.
- Terminoloji sözlüğündeki LOCKED kararlar ihlal edilmemeli.
- Exact FU kaynak commitindeki tüm pointer ve İngilizce kaynak değerleri doğrulanmalı.
- Aday nesnelerde salt dosya/tileset tanımı erişilebilirlik kanıtı sayılmamalı; tarif, araştırma, görev, dükkân veya gerçek Tiled yerleşimiyle runtime bağlantısı doğrulanmalı.
- Starbound'un ham satır sonu içeren JSON benzeri assetleri de kaynak simülasyonundan kaçmamalı.

## LQA kapısı
Statik QA geçse bile sürüm TAMAM sayılmaz. Oyunda:
- font ve Türkçe karakterler,
- metin taşmaları,
- görev zinciri,
- eşya/makine adları,
- renkler ve satır sonları,
- doğru NPC ve doğru bağlam,
- üretim menüsü ile görev hedefi eşleşmesi
kontrol edilmelidir.

LQA tamamlanmadan paket "tamamlanmış" veya "sorunsuz" diye etiketlenmez.
