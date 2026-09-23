# Frackin' Universe Türkçe

Frackin' Universe için hazırlanan gayriresmî Türkçe yerelleştirme projesi.

Amaç yalnızca İngilizce metinleri Türkçeye çevirmek değil; görevleri, araştırmayı, üretim zincirlerini, makineleri, eşyaları ve arayüzleri İngilizce bilmeden takip edilebilen, tutarlı bir Türkçe deneyim hâline getirmek.

**Güncel sürüm:** v0.52.0 Beta
**Hedef FU sürümü:** 6.5.8  
**Durum:** Statik QA ve sabitlenmiş FU kaynak doğrulaması başarılı. Oyun içi LQA henüz tamamlanmadı.

## Güncel durum

v0.52.0 Beta itibarıyla:

- **9.655** yapılandırılmış oyuncu metni
- **57** görünür Lua/script metni
- **9.712** toplam yerelleştirilmiş görünür birim
- **2.829** patch asset
- **7** raw override asset
- **2.836** toplam hedef asset
- Statik QA: **PASS**
- Pinned FU source validation: **PASS**
- ZIP bütünlüğü ve kurulum ağacı eşleşmesi: **PASS**
- Oyun içi LQA: **NOT TESTED**

Güncel doğrulanmış paket:

`dist/FU_Turkce_v0.52.0_Beta.zip`

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

Bir dosyanın FU kaynak ağacında bulunması tek başına çeviri gerekçesi sayılmıyor. Oyuncuya gerçekten görünen içerik mümkün olduğunca görev, tarif, araştırma, nesne, NPC, script veya runtime bağlantıları üzerinden doğrulanıyor.

## Tamamlanan audit kategorileri

Otomatik doğrulanan kalan kapsam açısından:

- **Arayüz:** 0 confirmed alan
- **Görevler:** 0 confirmed alan

Bu, oyunda artık hiçbir İngilizce arayüz veya görev metni kalmadığı anlamına gelmez. Review havuzu, Lua literal incelemeleri ve oyun içi LQA ayrı iş sınıflarıdır. Otomatik auditin kesin olarak doğruladığı borç bu iki kategoride kapatılmıştır.

## v0.45.1 bakım paketi

Lua görünür string güvenliği, LOCKED karma-varyant kontrolü, alan-bağlı kontrol kodu istisnaları, beş zemin etiketi, iki Mech yakıt uyarısı ve görev dili düzeltildi. PR QA salt okunur; generated çıktı değişiklikleri kaynak güncellemesi yerine kabul edilmez. Ayrıntılar: [bakım raporu](docs/QA_HARDENING_20260922.md).

## Son tamamlanan çalışma

v0.46 Irklar ve SAIL/AI confirmed kapsamı kapatıldı.

- 53 canlı asset
- 129 oyuncuya gösterilen alan
- 89 SAIL/AI alanı
- 20 oynanabilir ırkta 40 species alanı
- Irklar ve SAIL/AI confirmed borcu: 0

v0.46.1-v0.46.3 bakımında Jungle ve görev/konum görünen adları geriye dönük denetlendi. **v0.47.0** ile 66 bitki assetindeki **170** oyuncu-yüzü ad, açıklama ve Floran/Glitch inceleme metni Türkçeleştirildi. `.biome/friendlyName` ve `.liquid/description` gibi runtime görünürlüğü doğrulanmayan metadata alanları çeviri borcundan çıkarıldı.

**v0.48.0** ile koyu, açık renkli ve süslü ahşap ailelerindeki 32 assetin **151** adı, açıklaması ve ırka özgü inceleme metni Türkçeleştirildi. **v0.49.0** ile Aen, oyuncak ev, Dynast, ham ahşap ve yıpranmış ahşap ailelerindeki 44 assetin **227** alanı çevrildi. Taş ve diğer karo aileleri ayrı kapsam olarak tutulur.

**v0.50.0** ile 207 arıcılık assetindeki **537** görünür alan çevrildi. Arı türleri ve koloni rolleri, petekler, çerçeveler ve arıcılık arayüzü aynı terim düzeniyle ele alındı.

**v0.51.0** ile 33 platform assetindeki **99** görünür alan çevrildi; Floran, Glitch ve Novakid inceleme metinleri bu kapsama dahildir.

**v0.52.0** ile 126 taş, toprak ve yapı bloğu assetindeki **318** görünür alan çevrildi. Sabitlenmiş FU kaynak sürümü korunur.

## Kurulum

1. Starbound'u kapat.
2. Mümkünse `storage` klasörünü yedekle.
3. [Güncel beta paketini](dist/FU_Turkce_v0.52.0_Beta.zip) indirip çıkar.
4. Eski `FU_Turkce` kurulumunu `mods` dışına yedekle; yeni paketteki `FU_Turkce` klasörünü `mods` içine temiz kurulum olarak kopyala. Klasörleri birleştirmek kaldırılan eski yamaları oyunda bırakabilir.
5. Son yol şu şekilde görünmeli:

```text
Starbound/mods/FU_Turkce/_metadata
```

Ana Frackin' Universe `.pak` dosyasını veya Workshop klasörünü değiştirme.

Repository içindeki `FU_Turkce/` kurulum ağacı ile `dist/FU_Turkce_v0.52.0_Beta.zip` aynı doğrulanmış build sürecinden üretilir. Çeviri kataloğu değiştiğinde CI, `tools/kaynaklar.json` içindeki sabitlenmiş FU commitini kaynak olarak kullanarak doğrulama yapar.

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

Güncel çalışma checkpoint'i: [FU_SESSION_CHECKPOINT.md](FU_SESSION_CHECKPOINT.md)

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
