# FU TÜRKÇE ÇEVİRİ ANAYASASI - Repository Çalışma Özeti

Bu belge, FU TÜRKÇE projesinin ana Anayasasının repository içinde uygulanacak çalışma özetidir. Çelişki durumunda proje içindeki tam **FU TÜRKÇE ÇEVİRİ ANAYASASI v1.0** esas alınır.

## Öncelik sırası

1. Teknik bütünlük
2. Anlam doğruluğu
3. Oyuncunun anlayabilmesi
4. Terminoloji tutarlılığı
5. Doğal Türkçe
6. Karakter ve oyun tonu
7. Kaynak metne biçimsel sadakat

Kelime kelime çeviri hedef değildir. Oyuncu İngilizce bilmeden oyunu takip edebilmelidir.

## Teknik güvenlik

Aşağıdakiler çevrilmez veya değiştirilmez:

- JSON key'leri
- item / object / quest / recipe / status ID'leri
- script ve function isimleri
- asset ve dosya yolları
- değişkenler ve teknik tanımlayıcılar

Yalnızca oyuncuya gösterilen metin alanları çevrilir. Dosya yapısı ve teknik alanlar gereksiz yere yeniden formatlanmaz.

## Placeholder ve biçimlendirme

`%s`, `%d`, `{0}`, `{item}`, `$variable`, `\n`, `^red;`, `^green;`, `^orange;`, `^reset;` gibi teknik yapılar korunur.

Kaynakta gerçek bir biçimlendirme hatası varsa düzeltme yalnızca açık QA notuyla yapılır.

## Terminoloji

`docs/TERMINOLOGY.md` merkezi sözlüktür.

- LOCKED terim başka karşılıkla çevrilmez.
- Belirsiz terim rastgele çevrilmez.
- Önce sözlük, diğer kullanım örnekleri ve oyun bağlamı kontrol edilir.
- Emin olunmayan terim REVIEW durumuna alınır.
- Bir terim değişirse repository genelindeki eski kullanımlar temizlenir.
- Yeni pakette tekrar eden özel adlar, tür/fraksiyon, malzeme ve sistem adları ile önceki sürümlerde yeniden düzeltilen terimler bağlamları doğrulandıktan sonra `tools/locked_terms.json` içinde LOCKED karara bağlanır. Doğru karşılık ve bilinen yanlış varyantlar birlikte kaydedilir.
- Terim bir adın veya cümlenin içinde de geçiyorsa QA bu kullanımı denetlemelidir; tek sözcüklü özel adlarda gerektiğinde `enforce_in_text` kullanılır. Yanlış varyantı reddeden regresyon testi eklenir. Genel sözcüklerin farklı bağlamları gerekçesiz küresel yasakla kapatılmaz.

Oyuncuya gösterilen Türkçe adın yanına geçici kolaylık amacıyla bile İngilizce ad parantez içinde eklenmez.

## Görevler

Görev hedefleri kısa, net ve eylem odaklıdır.

Tercih edilen yapı:

**Eylem + hedef + gerekiyorsa konum**

Örnek fiiller: Bul, Topla, Üret, İnşa et, Konuş, Araştır, Etkinleştir, İncele, Götür, Teslim et, Yok et.

Görevde geçen eşya ve makine adı, envanter ve üretim menüsündeki adla aynı olmalıdır.

## UI

UI ve buton metinleri kısa ve işlevsel tutulur.

Örnek:
- Craft -> Üret
- Research -> Araştır
- Cancel -> İptal
- Apply -> Uygula
- Close -> Kapat

Alan darsa anlamı koruyan en kısa doğal Türkçe kullanılır.

## Tooltip ve eşya açıklamaları

Önce oyuncunun ihtiyacı olan işlevsel bilgi verilir. Atmosfer ve mizah korunabilir ancak bilgiyi gömmemelidir.

## NPC ve diyalog

Karakterin kaynak sesi korunur. Kaba, bilimsel, ciddi, komik veya gündelik bir karakter Türkçede de aynı etkiyi vermelidir.

Kaynakta olmayan şaka, küfür, lore veya bilgi eklenmez. Sertlik seviyesi gereksiz yere artırılmaz veya azaltılmaz.

## Bilimsel terimler

Gerçek dünyada yerleşik Türkçe bilimsel karşılığı bulunan kavramlarda doğru Türkçe terim kullanılır. Sırf daha bilimsel görünsün diye uydurma veya gereksiz ağır karşılık kullanılmaz.

## Özel isimler

Karakter, ırk, fraksiyon, marka ve evrene özgü özel adlar otomatik çevrilmez. Her biri bağlamıyla değerlendirilir.

İşlev açıklayan genel adlar oyuncuya anlam sağladığı için genellikle Türkçeleştirilir.

## Türkçe karakterler

Her zaman gerçek Türkçe karakterler kullanılır:

**ç, Ç, ğ, Ğ, ı, İ, ö, Ö, ş, Ş, ü, Ü**

ASCII yedek sürüm yoktur. Font sorunu varsa Türkçeyi bozmak yerine font sorunu çözülür.

## Doğal Türkçe

İngilizce söz dizimi Türkçeye taşınmaz. Gereksiz zamirler, edilgen yapılar ve dolambaçlı cümleler azaltılır.

Son soru:

**"Bu metin ilk kez Türkçe yazılmış olsaydı gerçekten böyle mi yazılırdı?"**

## Bağlam

Kısa veya belirsiz string tek başına çevrilmez. Dosya adı, key, komşu stringler, nesne ID'si ve kullanım yeri incelenir.

Emin olunmuyorsa tahmin etmek yerine REVIEW kararı verilir.

## Toplu çeviri

Binlerce string kör şekilde çevrilmez. Sistemler ayrı ayrı ele alınır:

- UI
- Görevler
- Araştırma
- Üretim
- Makineler
- Kaynaklar
- Eşyalar
- Tooltipler
- NPC diyalogları
- Lore / Codex

Aynı sistemde yarı Türkçe yarı İngilizce yapı mümkün olduğunca bırakılmaz.

## Otomatik QA

Mümkün olan her değişiklikte:

- JSON/patch geçerliliği
- placeholder eşitliği
- renk ve escape kodları
- değiştirilmiş teknik ID/path tespiti
- İngilizce kalmış oyuncu metni
- terminoloji ihlali
- boş/bozuk çeviri
- kaynak commit/pointer eşleşmesi

kontrol edilir.

## Oyun içi LQA

Statik QA yeterli değildir. Oyunda ayrıca:

- metin taşıması
- Türkçe font
- doğru NPC / doğru ekran
- görev hedefi
- görevdeki eşya ile envanter adı
- tooltip
- renkler
- satır sonları
- buton kesilmesi
- görev -> eşya -> üretim -> makine -> teslim zinciri

test edilir.

Oyun içi LQA tamamlanmadan bir sürüm **TAMAM** veya **sorunsuz** sayılmaz.

## Nihai test

Oyuncu İngilizce bilmeden:

- görevleri anlayabiliyor,
- eşyaları bulabiliyor,
- üretim zincirini takip edebiliyor,
- araştırma sistemini öğrenebiliyor,
- makineleri ayırt edebiliyor,
- açıklamalardan gerekli bilgiyi çıkarabiliyorsa

yerelleştirme görevini yerine getiriyor demektir.

Hedef:

**"Birileri bu modu çevirmiş." değil, "Bu mod Türkçe destekliyormuş." hissi.**
