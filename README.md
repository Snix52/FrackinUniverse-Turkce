# Frackin' Universe Türkçe

Starbound için Frackin' Universe moduna hazırlanan gayriresmî Türkçe yama ve yerelleştirme projesi.

**Steam Workshop:** [Frackin' Universe Türkçe [TR] - Snix](https://steamcommunity.com/sharedfiles/filedetails/?id=3805257011)

Amaç yalnızca İngilizce metinleri Türkçeye çevirmek değil; görevleri, araştırmayı, üretim zincirlerini, makineleri, eşyaları ve arayüzleri İngilizce bilmeden takip edilebilen, tutarlı bir Türkçe deneyim hâline getirmek.

**Güncel GitHub paket sürümü:** v0.70.0 Beta
**Hedef FU sürümü:** 6.5.8  
**Durum:** Statik QA ve sabitlenmiş FU kaynak doğrulaması başarılı. Oyun içi LQA henüz tamamlanmadı.

## Güncel durum

v0.70.0 Beta itibarıyla:

- **16.147** yapılandırılmış çeviri alanı
- **126** Lua/script metin gösterimi
- **16.273** toplam yerelleştirilmiş birim
- **4.923** patch asset
- **10** raw override asset
- **14** ek oyun asseti
- **4.947** toplam hedef asset
- Statik QA: **PASS**
- Pinned FU source validation: **PASS**
- ZIP bütünlüğü ve kurulum ağacı eşleşmesi: **PASS**
- Oyun içi LQA: **NOT TESTED**

Güncel doğrulanmış paket:

`dist/FU_Turkce_v0.70.0_Beta.zip`

24 Eylül 2026’da sabitlenen FU 6.5.8 kaynak commitine geçiş ve yeni çeviri kapsamı karşılaştırması: [FU upstream kontrolü](docs/audits/FU_UPSTREAM_20260924.md).

Paket ve güncel build kanıtı `main` yayın workflow'u tarafından üretilir. Paket SHA-256 değeri, kaynak commit kimliği, workflow run numarası ve doğrulama durumu yalnız [dist/build-evidence.json](dist/build-evidence.json) içinde tutulur; README’ye kopyalanmaz.

## Neler Türkçe?

Projenin tamamlanan ana kapsamları arasında şunlar bulunuyor:

- Ana araştırma sistemleri ve araştırma arayüzleri
- Tutorial ve Science görev zincirleri
- Outpost görevleri ve bağlı görev içerikleri
- Battle, Other, BYOS ve erişilebilir diğer görev aileleri
- Görevlerde kullanılan eşya, malzeme ve makine adları
- Üretim makineleri, tezgâhlar ve işlevsel dünya nesneleri
- Tarım, kimya, mühendislik ve güç sistemlerinin önemli bölümleri
- Geniş silah ve zırh kapsamı
- Başlangıç telsiz mesajları
- SAIL, görev terminali, üretim ve araştırma arayüzlerinin önemli bölümleri
- Windowconfig tabanlı canlı üretim, dükkân ve yardımcı paneller
- Pet House ve bağlı görünür arayüz metinleri
- MetaGUI tema metinleri ve doğrulanmış stat ekranı etiketleri
- Koyu, açık renkli ve süslü ahşap yapı malzemeleri
- Aen, oyuncak ev, Dynast, ham ahşap ve yıpranmış ahşap yapı malzemeleri
- Arı türleri ve kolonileri, bal petekleri, kovan çerçeveleri ve arıcılık arayüzü
- Platformlar ve merdivenler ile bunların ırklara özgü inceleme metinleri
- Taş, toprak ve yapı blokları ile bunların ırklara özgü inceleme metinleri
- Peglaci yapı, kablo ve Pykrete malzemeleri
- Bal peteği, altın odun, cam ve balmumu yapı malzemeleri
- FU kodeks belgeleri ve oyun içi rehberleri
- NPC konuşmalarının ilk dört diyalog dilimi

Bir dosyanın FU kaynak ağacında bulunması tek başına çeviri gerekçesi sayılmıyor. Oyuncuya gerçekten görünen içerik mümkün olduğunca görev, tarif, araştırma, nesne, NPC, script veya runtime bağlantıları üzerinden doğrulanıyor.

## Tamamlanan audit kategorileri

Otomatik doğrulanan kalan kapsam açısından:

- **Arayüz:** 0 confirmed alan
- **Görevler:** 0 confirmed alan

Bu, oyunda artık hiçbir İngilizce arayüz veya görev metni kalmadığı anlamına gelmez. Review havuzu, Lua literal incelemeleri ve oyun içi LQA ayrı iş sınıflarıdır. Otomatik auditin kesin olarak doğruladığı borç bu iki kategoride kapatılmıştır.

## Son tamamlanan çalışma

**v0.70.0** ile 375 NPC diyalog alanı eklendi; 350 konuşmacı/muhatap bağlamı incelendi. Hylotl, Pharitu, Mantizi, Nightar, Novakid, Shadow ve Skath sohbetleri yerelleştirildi. Katalog toplamı 16.147 alan, terim sözlüğü 637 LOCKED kayıttır. Önce/sonra düzeltmeler [inceleme raporunda](docs/reviews/dialogue4-20261001.json), kaynak ve oyun içi kontrol sınırları [LQA kaydında](docs/lqa/LQA_V070_20261001.md) bulunur.

**v0.69.0** üçüncü NPC diyalog diliminde 399, **v0.68.0** ikinci dilimde 380, **v0.67.0** ilk dilimde 376 alan ekledi. **v0.66.0** Bilim Karakolu yer imi ve ilk yetiştirme diliminde 454 alan ekledi. Diyalog önceliği sürer. Teknik doğrulama, her repliğin canlı oyunda denenmiş olduğu anlamına gelmez.

Önceki çalışmalar: [sürüm notları](docs/history/RELEASE_NOTES.md) ve [tarihsel denetimler](docs/audits/).

## Kurulum

### Steam Workshop

Atölye yayını GitHub paketinden ayrı güncellenir.

[Steam Workshop sayfasından](https://steamcommunity.com/sharedfiles/filedetails/?id=3805257011) yamaya abone olabilirsin.

### Manuel kurulum

1. Starbound'u kapat.
2. Mümkünse `storage` klasörünü yedekle.
3. [Güncel beta paketini](dist/FU_Turkce_v0.70.0_Beta.zip) indirip çıkar.
4. Eski `FU_Turkce` kurulumunu `mods` dışına yedekle; yeni paketteki `FU_Turkce` klasörünü `mods` içine temiz kurulum olarak kopyala. Klasörleri birleştirmek kaldırılan eski yamaları oyunda bırakabilir.
5. Son yol şu şekilde görünmeli:

```text
Starbound/mods/FU_Turkce/_metadata
```

Ana Frackin' Universe `.pak` dosyasını veya Workshop klasörünü değiştirme.

Repository içindeki `FU_Turkce/` kurulum ağacı ile `dist/FU_Turkce_v0.70.0_Beta.zip` aynı doğrulanmış build sürecinden üretilir. Çeviri kataloğu değiştiğinde CI, `tools/kaynaklar.json` içindeki sabitlenmiş FU commitini kaynak olarak kullanarak doğrulama yapar.

Ayrıntılı kurulum notu: [docs/KURULUM.txt](docs/KURULUM.txt)

## Çeviri yaklaşımı

Projenin temel hedefi oyuncuya "birileri modu çevirmiş" hissi vermek değil, "bu modun Türkçe desteği varmış" hissi vermektir.

Bu nedenle:

- Aynı eşya, makine ve sistem adı her yerde aynı tutulur.
- Görevdeki ad ile envanter ve üretim menüsündeki ad eşleştirilir.
- JSON key'leri, ID'ler, asset yolları ve teknik referanslar çevrilmez.
- Placeholder'lar, renk kodları ve biçimlendirme yapıları korunur.
- UI metinleri kısa ve işlevsel tutulur.
- Görev hedefleri doğrudan ve takip edilebilir yazılır.
- Diyaloglarda karakter tonu korunur.
- Bilimsel kavramlarda doğru Türkçe terminoloji tercih edilir.
- Bağlamı belirsiz FU terimleri tahmin edilmez.
- Gereksiz dosya yeniden biçimlendirmesi yapılmaz; minimum diff korunur.

Projenin dil ve teknik kuralları:

- [Çeviri standardı](docs/STYLE_GUIDE.md)
- [Çeviri paketi boyutu ve kapsam seçimi](docs/TRANSLATION_BATCH_POLICY.md)
- [Terminoloji](docs/TERMINOLOGY.md)
- [Karar kaydı](docs/DECISIONS.md)
- [QA kuralları](docs/QA_RULES.md)
- [Otomatik doğrulama ve paket kanıtı](docs/QA_PIPELINE.md)
- [Manuel oyun içi LQA](docs/LQA_CHECKLIST.md)

## QA yaklaşımı

Statik QA; diğer kontrollerin yanında şunları denetler:

- Kaynak metin ve provenance eşleşmeleri
- JSON/Patch yapısı
- Placeholder bütünlüğü
- Renk ve kontrol kodları
- Teknik alanların korunması
- Terminoloji kuralları
- Boş veya yinelenen çeviri alanları
- Paket bütünlüğü
- Kurulum ağacı ile ZIP eşleşmesi

Ancak dosyada doğru görünen bir metin otomatik olarak oyun içinde doğru kabul edilmez.

Manuel LQA aşamasında özellikle şunlar kontrol edilmelidir:

- Türkçe karakter ve font görünümü
- Metin taşmaları ve kesilmeler
- Görev akışları
- Görev, eşya, makine ve üretim adı eşleşmeleri
- NPC ve ekran bağlamları
- Renkler ve satır sonları
- Buton ve panel boyutları
- İngilizce bilmeden görev ve üretim zincirinin takip edilip edilemediği

Bu nedenle proje hâlâ **Beta** durumundadır.

## Geliştirme

Proje tek kişi tarafından yürütülüyor. Otomasyon ve yapay zekâ araçları büyük kapsamı yönetmek, kaynak bağlarını doğrulamak ve QA kontrollerini çalıştırmak için yardımcı olarak kullanılıyor.

Üretilen metinler yalnızca gramer düzgünlüğüne göre kabul edilmiyor. Terminoloji, runtime bağlamı, teknik güvenlik ve oyuncunun sistemi takip edip edemediği ayrıca değerlendiriliyor.

[Belge dizini](docs/README.md) · [Katkı ve bakım rehberi](CONTRIBUTING.md) · [Araç dizini](tools/README.md)

Güncel çalışma checkpoint'i: [FU_SESSION_CHECKPOINT.md](docs/history/FU_SESSION_CHECKPOINT_20261001.md)

## Kaynak ve lisans

Frackin' Universe, sayter ve katkıda bulunanların çalışmasıdır. Bu proje FU ekibi, Chucklefish veya Starbound geliştiricileri tarafından hazırlanmış ya da onaylanmış resmî bir Türkçe sürüm değildir.

Kaynak, lisans ve atıf bilgileri: [docs/KAYNAK_VE_LISANS.txt](docs/KAYNAK_VE_LISANS.txt)

## Hata bildirimi

Bir hata bulursan mümkünse şunları birlikte paylaş:

- Sorunun ekran görüntüsü
- Hangi görev, eşya, makine veya ekranda olduğu
- `Starbound/storage/starbound.log`
- Kullandığın FU Türkçe sürümü

Özellikle şu sorunlar yüksek önceliklidir:

- Aynı eşyanın veya makinenin farklı adlarla çevrilmesi
- İngilizce kalmış görünür oyuncu metinleri
- Görevde istenen şeyin Türkçe adıyla oyunda bulunamaması
- Yanlış yönlendiren görev metinleri
- Bozuk placeholder, renk kodu veya biçimlendirme
- UI taşması, kesilmesi veya okunamayan Türkçe karakterler
