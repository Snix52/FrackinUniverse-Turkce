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
- Aday eşyalarda yalnız tanım dosyasının bulunması veya `/spawnitem` ile çağrılabilmesi erişilebilirlik kanıtı sayılmamalı; etkin tarif, araştırma, görev ödülü, çıkarma/işleme tablosu, ganimet ya da gerçek başlangıç/blueprint zinciri aranmalı.
- `.disabled` tarifler, yorum satırları, deprecated geri-kazanım girdileri ve üretim kaynağı olmayan filtre/blueprint kayıtları tek başına canlı içerik sayılmamalı.
- Görevlerde yalnız dosya, `id`, prerequisite veya aynı adlı eşya bulunması erişilebilirlik kanıtı sayılmamalı; gerçek başlangıç, `pickupQuestTemplates`, NPC `offeredQuests`, SAIL görevi ya da Tiled yerleşimi doğrulanmalı.
- `showInLog`, kabul/tamamlama/hata pencereleri kapalı takip ve uyumluluk görevlerinin metinleri oyuncuya görünür sayılmamalı.
- NPC `offeredQuests` içinde yorum satırına alınmış görev zincirleri ve yalnız geliştirici gemisi/hazine havuzuna bağlı görevler normal oyuncu kapsamına alınmamalı.
- `items/generic/crafting` kapsamındaki item/consumable dosyalarında bu sürüm için yalnız `/shortdescription` ve `/description` çevrilebilir; `itemName`, efekt, fiyat, kategori ve tooltip mekanikleri teknik alan olarak korunmalı.
- Silah kapsamına alınan `.activeitem` ve `.beamaxe` dosyalarında aktif araştırma düğümü ile gerçek `.recipe` çıktısı birlikte doğrulanmalı; yalnız araştırma listesi veya tanım dosyası yeterli sayılmamalı. v0.21 için exact allowlist'teki 121, v0.22 için exact allowlist'teki 157, v0.23 için `advancealloygear` + `durasteelgear` exact allowlist'indeki 48 ve v0.24 için kalan beş Kademe 4 düğümünün exact allowlist'indeki 148 yeni savaş ekipmanı assetinde yalnız `/shortdescription` ve `/description` çevrilebilir; hasar, yetenek, mermi, kategori ve script alanları korunmalı.
- Usta Manipülatör tutarlılık düzeltmesinde yalnız iki runtime-bağlı assetin görünür alanları kapsama alınmalı: kırık augment için `/shortdescription`, `/description`, `/augment/displayName`; tamamlanmış araç için `/shortdescription`, `/description`. `itemName`, pickup görevi, blueprint ve araç mekaniği alanları korunmalı.
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
