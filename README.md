# Frackin' Universe Türkçe

Frackin' Universe için topluluk tabanlı, gayriresmî Türkçe yerelleştirme projesi.

**Durum: v0.27 Beta / Ana araştırma sistemleri + runtime'da erişilebilir görevler + üretim makineleri, seçili işlevsel dünya nesneleri, erişilebilir `items/generic/crafting` malzemeleri, Kademe 1-4 araştırma savaş ekipmanları ve Kademe 1-4 aktif zırh setleri / statik QA tamamlandı, oyun içi LQA bekliyor.**

## Mevcut kapsam

- Jeoloji araştırma ağacındaki aktif çevrilebilir metinler
- Tarım araştırma ağacının tamamı
- Kimya araştırma ağacının tamamı
- Mühendislik araştırma ağacının tamamı
- Güç Sistemleri araştırma ağacının tamamı
- Zanaatkârlık araştırma ağacının tamamı
- Zırh ve Silahlar araştırma ağacının tamamı
- Delilik / Metafizik araştırma ağacının 31 aktif düğümünün tamamı
- Delilik sisteminin temel psiyonik, ruh sağlığı ve madde işleme eşya/makineleri
- Tutorial görev ailesindeki bağlı görevlerin tamamı (41/41 görev dosyası)
- Tutorial görevlerinde doğrudan hedef gösterilen temel eşya ve makinelerin envanter adları
- Science bağlantılı erişilebilir görevlerin tamamı (37/37 benzersiz görev; 35 quest-list + 2 çapraz akış görevi)
- Science görevlerinde doğrudan hedef gösterilen temel eşya, malzeme ve makinelerin envanter adları
- Outpost Starbooze / İçki görev zincirinin tamamı (12/12 görev dosyası) ve doğrudan bağlı temel makineler/malzemeler
- Outpost Arıcılık zincirindeki erişilebilir görevlerin tamamı (13/13; `13mites` bağlantısız legacy olduğu için dağıtım dışı)
- Bilim Karakolu dükkânlarından doğrudan açılan 6/6 Outpost görevi ve ilgili görev artefaktları
- Arıcılık görevlerinde yönlendirilen temel arı türleri, çerçeveler, Arılık, mikroskop, bal işleme makinesi ve vanilla hedef eşyaların envanter adları
- Bilim Karakolundaki altı canlı dükkân görevi (6/6), hedef artefaktları ve dükkân nesneleri
- Battle klasöründeki 10/10 erişilebilir görev, Battle görev-listesi ve doğrudan hedeflenen 10 envanter asseti
- Other klasöründeki 8/8 erişilebilir görev ve doğrudan hedeflenen eşya/teslim nesneleri
- BYOS kalan kapsamındaki 2/2 erişilebilir görev ve BYOS görev-listesi metinleri
- Zırh ve Silahlar ağacının doğrudan yönlendirdiği Zırh Atölyesi, Örs yükseltmeleri ve Solunum EPP'si
- Zanaatkârlığın doğrudan referans verdiği koloni, mutfak, dikiş, biyokimya ve temel üretim istasyonları
- Güç Sistemlerinin doğrudan bağlı temel üretim, reaktör, pil, santrifüj ve atmosfer makineleri
- `objects/crafting` altındaki 84/84 etkin nesnede seçili oyuncuya görünür ad, açıklama, alt başlık, panel başlığı ve ırka özel inceleme metinleri
- `objects/power`, `objects/bees` ve `objects/scienceoutpost` altındaki v0.18 adaylarının runtime denetimi: 47 erişilebilir nesnede ad, açıklama, inceleme, panel ve sohbet metinleri; 10 ölü/bağlantısız nesne dağıtım dışı
- `items/generic/crafting` altındaki kalan 261 adayın runtime denetimi: 235 erişilebilir eşya/malzemede envanter adı ve açıklama; 26 ölü, deprecated veya bağlantısız asset dağıtım dışı
- Ana görev aileleri dışında kalan 97 `questtemplate` adayının runtime denetimi: 29 erişilebilir görevde 112 görünür alan; 68 erişilemez, devre dışı, geliştiriciye özel veya görünmez görev dağıtım dışı
- Aktif Zırh ve Silahlar ağacındaki Kemik, Demir, Telebrium ve Tungsten düğümlerinin açtığı 124/124 üretilebilir silah; 121 yeni assette ad ve açıklama, önceden çevrilen 3 asset korunarak tamamlandı
- Aktif Zırh ve Silahlar ağacındaki altı Kademe 3 düğümünün açtığı 158/158 üretilebilir savaş ekipmanı; 157 yeni assette ad ve açıklama, önceden çevrilen 1 silah korunarak tamamlandı
- Aktif Zırh ve Silahlar ağacındaki Gelişmiş Alaşım ve Durasteel Kademe 4 düğümlerinin açtığı 48/48 üretilebilir savaş ekipmanında envanter adı ve açıklama
- Aktif Zırh ve Silahlar ağacındaki Irradium, Trianglium, Prisilite, Quietus ve Biyosilah Kademe 4 düğümlerinin açtığı 148/148 üretilebilir savaş ekipmanında envanter adı ve açıklama
- Aktif Zırh ve Silahlar ağacındaki dokuz Kademe 1-2 kolunun açtığı, gerçek tarifle doğrulanan 114 zırh parçasında envanter adı ve set bonusu/açıklama metni
- Aktif Zırh ve Silahlar ağacındaki altı Kademe 3 kolunun açtığı, gerçek tarifle doğrulanan 76 zırh parçası; önceden çevrilmiş Mutavisk miğferi korunarak 75 yeni assette envanter adı ve set bonusu/açıklama metni
- Aktif Zırh ve Silahlar ağacındaki yedi Kademe 4 kolunun açtığı, gerçek tarifle doğrulanan 87 zırh parçasında envanter adı ve set bonusu/açıklama metni
- Usta Manipülatör görev-eşya zincirindeki kırık augment ve tamamlanmış aracın görünen ad/açıklamaları görev terminolojisiyle eşlendi
- Başlangıç görevlerinin bir bölümü ve BYOS Yıldızlararası Yolculuk zinciri
- Başlangıç telsiz/öğretici mesajlarının mevcut dosyadaki 26/26 metni
- İmalat Tezgâhı yükseltme kademeleri ve seçili arayüz metinleri
- Tarım/genetik makineleri ve temel Tarım öğretici görevleri
- Kimya Laboratuvarı ve doğrudan bağlı temel kimya kaynakları
- Mühendislikteki temel çıkarma, araştırma, gemi ve çekirdek makineleri/kaynakları
- STL Motoru ve Küçük FTL Motoru oyuncu metinleri
- Araştırma ekranındaki seçili açıklamalar, fallback metinleri ve Lua içine gömülü sabit UI metinleri

Toplam **4.876 yapılandırılmış oyuncu metni alanı** ve **15 Lua UI metni**, yani **4.891 yerelleştirilmiş görünür metin birimi** bulunmaktadır. Bu, FU'nun tamamının Türkçe olduğu anlamına gelmez.

## Anayasa ve terminoloji

- Ana standart: `docs/STYLE_GUIDE.md`
- Terminoloji: `docs/TERMINOLOGY.md`
- Karar kaydı: `docs/DECISIONS.md`
- QA kuralları: `docs/QA_RULES.md`

Oyuncuya gösterilen Türkçe adların yanına İngilizce karşılık parantez içinde eklenmez. Türkçe karakterler zorunludur; ASCII yedek sürüm üretilmez.

## Kurulum

1. Starbound ve Frackin' Universe kurulu olmalı.
2. Önce `storage` klasörünü yedekle.
3. `FU_Turkce` klasörünü Starbound'un `mods` klasörüne kopyala.
4. Son yol şu biçimde olmalı:

```text
Starbound/mods/FU_Turkce/_metadata
```

Ana Frackin' Universe `.pak` dosyasına veya Workshop klasörüne dokunma.

Ayrıntılı bilgi: `docs/KURULUM.txt`.

> **Paket notu:** Güncel beta paketi `dist/FU_Turkce_v0.27.0_Beta.zip` olarak GitHub Actions tarafından statik QA sonrasında otomatik üretilir.

## Sürüm uyumluluğu

```text
FU sürümü: 6.5.8
Kaynak commit: 329e714b3fe87571055c8ad7aa38135d199d3317
```

Güncel statik QA'da toplam yapılandırılmış kapsam **4.876 alan / 1.516 patch asset**tir. v0.27'de aktif Zırh ve Silahlar ağacındaki yedi Kademe 4 kolunun açtığı **87 tarif destekli zırh parçasının** yalnız ad ve açıklama alanlarından oluşan **174 alanı pinned FU 6.5.8 kaynağıyla exact doğrulandı**. Toplam provenans **4.788 pinned FU + 88 belgeli layered/external alan**, izlenmeyen alan **0**. Araştırma ekranının JSON Patch dışında kalan **1 Lua assetindeki 15 görünür metin** exact kaynak-fragment korumasıyla ayrıca doğrulanır.

`build_validate.py`, kaynak klasörü verilirse Lua override'ını doğrudan o kaynak script üzerinden üretir; beklenen kaynak metinlerinden biri değişmişse build durur.

## v0.6 Zanaatkârlık

Zanaatkârlık ağacındaki **76 gerçek araştırma düğümü** ve ağaç adı yerelleştirildi. Kaynakta bulunan ancak arayüz kodunda kullanılmayan `default` yardım/fallback çifti ile hiçbir düğüme bağlı olmayan `workbenchatechy` stringi oyuncuya görünmediği için yamaya alınmadı. Doğrudan yönlendirme yapılan temel istasyon adları envanter adlarıyla eşleştirildi.

v0.6 eklemesi: **284 aktif yapılandırılmış alan / 12 hedef asset**. Oyun içi LQA ve panel taşma kontrolleri hâlâ bekliyor.

## v0.7 Zırh ve Silahlar

Zırh ve Silahlar ağacındaki **47 gerçek araştırma düğümü** ve ağaç adı yerelleştirildi. Kaynaktaki `default` yardım/fallback çifti arayüz kodu tarafından kullanılmadığı için yamadan çıkarıldı. Araştırmanın doğrudan yönlendirdiği ana istasyonlar gerçek envanter adlarıyla eşleştirildi: **Zırh Atölyesi → Montaj Hattı → Cephanelik**, **Örs → Dövme Ocağı → Çoğaltıcı** ve **Solunum EPP'si**.

v0.7 eklemesi: **115 aktif yapılandırılmış alan / 4 hedef asset**. Oyun içi LQA ve panel taşma kontrolleri bekliyor.

## v0.8 Delilik / Metafizik

Delilik ağacındaki **31 aktif araştırma düğümü** ve ağaç adı yerelleştirildi. Kaynaktaki runtime'da kullanılmayan `default` yardım/fallback çifti yamaya alınmadı.

Aynı paket içinde oyuncunun sistemi İngilizce bilmeden takip edebilmesi için **Delilik**, **Karanlık Madde**, **Beyin Çıkarıcı**, **Psiyonik Tezgâhı**, **Psiyonik Yükselteç**, **Psi Enerjisi**, **Psiyonik Odak**, **Insta-Freud**, **Otopsi Masası**, **Madde Dönüştürücü**, Beyin Jeneratörü/Pili ve ilgili Psiyonik Tezgâhı UI metinleri de eşlendi.

v0.8 eklemesi: **103 aktif yapılandırılmış alan / 18 hedef asset**. Yeni alanların tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı. Oyun içi LQA ve panel taşma kontrolleri bekliyor.


## v0.9 Tutorial Görevleri

FU `fu_questlines/tutorial` altında kaynakta **42 questtemplate** bulunuyor. Bunlardan `start_basics1`, yarıda kesilmiş metni ve hiçbir yerden çağrılmayan yapısı nedeniyle kırık/bağlantısız kaynak olarak dağıtıma alınmadı. Oyuncunun ulaşabildiği tutorial ailesi böylece **41/41 görev dosyası** olarak Türkçeleştirildi.

v0.9'da daha önce çevrilmemiş **25 tutorial görev dosyasında 90 oyuncu metni** yerelleştirildi. Görev hedeflerinin envanterle birebir eşleşmesi için ayrıca **19 hedef eşya/makine assetinde 41 alan** çevrildi. Toplam v0.9 eklemesi **131 yapılandırılmış alan / 44 hedef asset**tir.

Kaynakta oyuncuyu yanlış yönlendiren eski tutorial metinleri gerçek quest koşullarına göre düzeltildi: Extractor IV/V'nin eski Tissue Culture / Genetic Material yönlendirmeleri, `create_silicon` içindeki 10 yerine gerçek 1 Silisyum koşulu, Wooden Centrifuge teslim hedefindeki yanlış Armorworks adı ve Rock Breaker metnindeki bozuk renk kapanışı.

Science v0.10, Outpost v0.14 ve Battle v0.15 ile erişilebilir kapsam düzeyinde kapandı. Arıcılıktaki `13mites` ile Battle altındaki `fuquest_gorgolith`, `fuquest_gorillaking` ve `fuquest_titan` runtime'da bağlantısız olduğu için dağıtım dışı bırakıldı. Klasör-bazlı yol haritasında sırada **17 ham görev dosyası** bulunuyor: Other 13, BYOS 3 ve Exploration 1. Her kategori işlenirken yalnız klasör sayısına değil runtime quest-list/NPC bağlantılarına da bakılacak.

## v0.10 Science Görevleri

Science klasöründe ham olarak **36 questtemplate** bulunmasına rağmen runtime akışı klasör yapısıyla birebir değildir. `fuquest_dna` ve `fuquest_mineral` hiçbir NPC, prerequisite zinciri veya quest-list tarafından çağrılmadığı için bağlantısız legacy görev olarak dağıtım dışı bırakıldı. Buna karşılık `deprecated` klasöründeki `fuquest_powerstation`, `fuquest_battery` ve `fuquest_prototyper` hâlâ Science quest-list tarafından başlatılıyor. Ayrıca `fuquest_biochem` Tutorial alt zincirinden, `create_blackglass` ise Bilim Karakolu NPC'sinden erişilebilir.

Bu nedenle oyuncunun ulaşabildiği benzersiz Science bağlantılı kapsam **37/37 görev** olarak yerelleştirildi: Chemistry 8, Electronics 8, Genetics 9, Mechanical 8 ve Physics 4.

v0.10 eklemesi **204 yapılandırılmış alan / 64 yeni patch asset**tir. Görevlerdeki eski veya hatalı üretim yönlendirmeleri gerçek tarif ve quest koşullarıyla karşılaştırıldı. Öne çıkan düzeltmeler arasında eski Bio Lab yönlendirmesi, Silisyum Devre Kartının eski Madde Birleştirici tarifi, Wiring Tool adı, Genetics laboratuvar kademe hataları, eski Fission Furnace adı ve Tritium görevindeki artık geçerli olmayan Fisyon Reaktörü hedefi bulunur.

Yeni alanların tamamı kaynak/provenans kontrolünden geçti: **193/193 pinned FU alanı + 11/11 bağımsız vanilla alanı**, toplam **204/204 PASS**. Patch pairing **204 test + 204 replace PASS**. Oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca yapılmalıdır.

## v0.11 Outpost İçki Görevleri

Outpost klasöründeki Starbooze / İçki alt zinciri **12/12 görev dosyası** olarak birlikte yerelleştirildi. Bu turda **44 görev alanı**, görev takibini envanterle eşlemek için **13 makine alanı** ve **32 malzeme/içki alanı** eklendi. Toplam v0.11 eklemesi **89 yapılandırılmış alan / 34 yeni patch asset**tir.

Terminoloji zinciri tekilleştirildi: **İçki Kiti**, **Mayşe**, **Mayşeleme Kazanı**, **Meyve Presi**, **Fermentör**, **Yağmur Varili**, **Damıtıcı**, **Maya Suyu**, **Şerbetçiotu** ve **Şıra**. Böylece görevde görülen ana adlar envanterdeki adlarla eşleşir.

Kaynak görevlerdeki adet sapmaları gerçek koşul ve tariflerle çaprazlandı. `2brew_a` kaynakta üç/dört Şişe dese de görev 1 ister; `3hops` kaynakta 2 Şerbetçiotu dese de görev 1 ister; `6beer` kaynakta 3 Bira dese de görev 1 ister ve tarif 2 üretir. `2brew_c` ise 1 Üzüm Mayşesiyle tamamlanmasına rağmen sonraki Wartweed Şarabı tarifi 2 ister; Türkçe metin bu geçişi açıklar.

Yeni alanların **89/89'u pinned FU 6.5.8 kaynağıyla exact doğrulandı**. Patch pairing **89 test + 89 replace PASS**. Outpost klasöründeki ham 45 görev dosyasının 12'si bu paketle işlendi; kalan dosyalar runtime/NPC bağlantı denetimiyle sonraki turlarda ele alınacak. Oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca yapılmalıdır.

## v0.12 Outpost Arıcılık

Outpost Arıcılık klasöründeki **14 ham questtemplate** runtime bağlantılarıyla denetlendi. Arıcı NPC, görev takip zinciri ve `fu_bees` quest-list birlikte incelendi; oyuncunun ulaşabildiği kapsam **13/13 görev** olarak yerelleştirildi. `13mites` hiçbir NPC, quest-list veya follow-up tarafından başlatılmadığı için bağlantısız legacy kabul edilerek dağıtım dışı bırakıldı ve build guard'a eklendi.

Görevlerde kullanılan Arılık, Büyük Arılık, Temel Çerçeve, Temel Mikroskop, Bal Ana/Erkek Arısı, Bombus ve Orkide arıları, Bal Peteği, Balmumu, Tungsten Çerçeve, Altın Odun ve Bal Kavanozlama Makinesi envanter adlarıyla eşlendi. Vanilla **Böcek Ağı, Kırmızı Çiçek ve Boş Şişe** ayrıca bağımsız Starbound kaynağından doğrulandı.

Kaynak `12breeding` metnindeki **Giant Apiary** gerçek bir envanter nesnesi değildir; aynı zincirdeki gerçek `normalalveary` nesnesinin adı **Large Apiary** olduğundan Türkçede **Büyük Arılık** kullanıldı. v0.12 eklemesi **78 yapılandırılmış alan / 31 yeni patch asset**tir: **72/72 pinned FU + 6/6 vanilla = 78/78 kaynak/provenans PASS**. Oyun içi LQA ayrıca yapılmalıdır.

## v0.13 Bilim Karakolu Dükkân Görevleri

Outpost kökündeki altı `scienceoutpost_*Shop` görevi, ilgili dükkân nesnelerinin `offeredQuests` ve `turnInQuests` alanlarıyla runtime'da doğrudan doğrulandı. Quest List'te yer almamalarına rağmen oyuncuya erişilebilir oldukları için **6/6 görev** yerelleştirildi.

Görev hedefi olan **Greenfinger Madalyası, Uğurlu Para, Kristal Kupa, Uzaylı Yayın Düğümü, X'i Kalıntısı ve Kadim Kumanda** envanter adlarıyla aynı pakette eşlendi. Altı dükkân nesnesinin görünen ad ve açıklamaları da Türkçeleştirildi. `Verdant Ruins`, `Ancient Temple` ve `Evernight Jungle` ise ilgili mission/harita zincirleri bütünüyle yerelleştirilene kadar özel yer adı olarak korunuyor.

v0.13 eklemesi **48 yapılandırılmış alan / 18 yeni patch asset**tir. Yeni alanların **48/48'i pinned FU 6.5.8 kaynağıyla exact doğrulandı**. Gölge dükkânının iki metnindeki `<...>` işaretleri teknik tag değil, karakterin konuşma biçimidir; dış açı parantezleri korunarak alan-bazlı QA istisnası belgelendi. Oyun içi görev işaretçisi, font ve dükkân etkileşim LQA'sı ayrıca yapılmalıdır.


## v0.13 Outpost Bilim Karakolu Dükkânları

Bilim Karakolundaki altı dükkân görevi, ilgili dükkân nesnelerinin `offeredQuests` / `turnInQuests` bağlantıları üzerinden runtime'da doğrulandı ve **6/6 canlı görev** olarak yerelleştirildi.

Görev metinlerindeki hedeflerin envanterle birebir eşleşmesi için **Greenfinger Madalyası, Uğurlu Para, Kristal Kupa, Uzaylı Yayın Düğümü, X'i Kalıntısı ve Kadim Kumanda** aynı pakette çevrildi. Altı dükkân nesnesinin görünür ad/açıklamaları da yerelleştirildi.

v0.13 eklemesi **48 yapılandırılmış alan / 18 yeni patch asset**tir. Yeni alanların tamamı pinned FU 6.5.8 kaynağıyla doğrulandı: **48/48 PASS**. `Verdant Ruins`, `Ancient Temple` ve `Evernight Jungle` gibi özel görev/konum adları, ilgili mission zincirleri bütünüyle yerelleştirilene kadar özgün bırakıldı.

Bu paketle Outpost tarafında geriye **13 ham görev dosyası** kaldı: Kevin 9 + Khe 4. Oyun içi görev işaretçisi, dükkân etkileşimi, font ve panel taşma LQA'sı ayrıca yapılmalıdır.


## v0.13.1 Geriye Dönük Türkçe QA

v0.1-v0.13 arasında yerelleştirilmiş **1.929 yapılandırılmış alan** ve **15 Lua UI metni** yeniden tarandı. Toplam **26 alanda** dilbilgisi, terminoloji, UI anlamı veya doğal Türkçe düzeltmesi yapıldı; teknik kapsam ve kaynak pointerları değişmedi.

Başlıca düzeltmeler: bozuk Bilim Karakolu teslim cümleleri, Arıcılıkta **Ana Arı** terminolojisi, Penumbrite yazım hatası, Glitch duygu etiketleri, monokl tarifleri ve v0.13 dükkân görevlerinin yönlendirme/akıcılık sorunları. Arı Barınağı düğmesi ilk turda **Sat** yapılmıştı; v0.13.2'de panelin hem arı teslimi hem rehber alımı yaptığı doğrulanınca nötr **Takas Et** olarak düzeltildi.

Statik QA sonucu: **0 duplicate, 0 boş çeviri, renk/kontrol/placeholder/sayı bütünlüğü PASS**. Oyun içi LQA, font ve panel taşma kontrolleri ayrıca bekliyor.


## v0.13.2 İkinci Geriye Dönük QA

v0.13.1 sonrasında bütün katalog tekrar tarandı. Kilitli **Mech** sistem adının eski içeriklerde 16 kez küçük harfle `mech` yazıldığı bulundu ve tamamı **Mech** olarak tekilleştirildi.

Arı Barınağı kaynak tarifleri yeniden incelendi. Panel yalnızca arıları para veya malzemeye çevirmiyor; aynı arayüzde 1 Piksel karşılığında arıcılık rehberleri de alınabiliyor. Bu nedenle tek yönlü **Sat** etiketi de eksik kaldığından eylem düğmesi her iki işlemi kapsayan **Takas Et** olarak düzeltildi.

Bu turda **17 yapılandırılmış alan** değişti. Alan/pointer sayısı, provenans ve patch asset kapsamı değişmedi: **1.929 structured + 15 Lua = 1.944 görünür birim / 322 patch asset**. Küçük harf `mech` ve Arı Barınağı eylemi için yeni build regresyon guardları eklendi.

## v0.13.3 Üçüncü Geriye Dönük QA

Bütün mevcut katalog üçüncü kez bağlam ve envanter takibi açısından tarandı. Crafting listelerinde runtime sırasında gerçek eşya adıyla değiştirilen üç `Replace Me` şablon alanı oyuncu metni olmadığı için kapsamdan çıkarıldı.

Sifter tutorialında İngilizce kalan **Loose Silt / Gravel** hedefleri gerçek envanter adlarıyla **Gevşek Mil / Çakıl** olarak eşlendi. Wooden Centrifuge tutorialında ise kaynak açıkça ayrı bir **Iron Centrifuge** nesnesine yönlendirdiği hâlde Türkçe metin yalnız “Santrifüj” diyordu. Gerçek `ironcentrifuge` nesnesi doğrulandı, **Demir Santrifüj** olarak LOCKED edildi ve envanterdeki açıklama/ad/alt başlık/kategori de çevrildi.

Ayrıca oyuncuya dönük iki `eldritch` sızıntısı **tekinsiz**, `vanilla` meta ifadesi **ana oyun** olarak düzeltildi. Net sonuç: **1.934 structured + 15 Lua = 1.949 görünür birim / 325 patch asset**. Oyun içi LQA hâlâ ayrı aşamadır.

## v0.14 Outpost Kevin ve Khe

Kevin'in **9/9**, Khe'nin **4/4** canlı görevi; Kevin'in NPC teklif/teslim zinciri, Khe'nin teslim NPC'si ve iki eşya-tetikli breadcrumb bağlantısı üzerinden doğrulandı. Görevlerde görünen hedef adları envanterle birebir eşlendi: **Booster Kısa Üstü, Biyoyakıt Kapsülü, Uzaylı Bileşiği, Çubukta Bebek Kafası, Portakal, Plazmik Kristal, Üstün Beyin, Nötronyum Çubuğu, Anti-Nötronyum Çubuğu, Nötron Bombası, Saf Erchius Kristali** ve **Hayalet Feneri**.

Kaynak görevdeki Sewing Wheel, gerçek üretim istasyonu olan **Sewing Machine / Dikiş Makinesi** ile; average quality Brains, gerçek brain envanter adı **Superior Brain / Üstün Beyin** ile açıklaştırıldı. Khe'nin kısa, kedimsi konuşma biçimi; Kevin'in kendini beğenmiş ve absürt tonu korunarak doğal Türkçeye aktarıldı.

v0.14 eklemesi **94 yapılandırılmış alan / 33 yeni patch asset**tir: 50 görev alanı, 3 görev-listesi alanı ve 41 bağlı envanter alanı. Kaynak/provenans sonucu **94/94 PASS** (84 pinned FU + 10 vanilla). Proje toplamı **2.028 structured + 15 Lua = 2.043 görünür birim / 358 patch asset** oldu. Oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca yapılmalıdır.

## v0.15 Battle Görevleri

Battle klasöründeki **13 ham questtemplate** görev listesi, NPC teklif/teslim alanları ve prerequisite/follow-up referanslarıyla denetlendi. `fu_gear` altındaki 6/6 ve `fu_monsters` altındaki 4/4 erişilebilir görev yerelleştirildi. **Gorgolith, Apex War-Born ve Wrexor Nar** görevleri yalnız kendi dosyalarında ve tamamlanma sonrası tüccar kilitlerinde geçiyor; hiçbir quest-list, NPC veya takip zinciri tarafından başlatılmadıkları için bağlantısız legacy kabul edilip dağıtım dışı bırakıldı.

Görev hedefleri gerçek envanter adlarıyla eşlendi: **Sıradan Şapka, Kol Topu, F4 Enerji Tüfeği, Lazer Tabancası, Çelik Savaş Kılıcı, Ferozium Satırı, Yadigâr Kalkanı, Anne Poptop Pençesi, Ağ Atıcı** ve **Hiper Hedefleme Çipi**. Kaynaktaki genel “Poptop Claw” yönlendirmesi, gerçek envanter adı **Mama Poptop Claw / Anne Poptop Pençesi** ile açıklaştırıldı.

v0.15 eklemesi **64 yapılandırılmış alan / 20 yeni patch asset**tir: 39 görev alanı, 4 görev-listesi alanı ve 21 bağlı envanter alanı. Kaynak/provenans sonucu **64/64 PASS** (tamamı pinned FU). Proje toplamı **2.092 structured + 15 Lua = 2.107 görünür birim / 378 patch asset** oldu. Oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca yapılmalıdır.

## v0.16 Kalan Görev Klasörleri

Other, BYOS ve Exploration klasörlerinde kalan **17 ham questtemplate** runtime tetikleyicileri, görev-listesi, NPC, pickup ve takip zinciri referanslarıyla denetlendi. Other içindeki **8**, BYOS içindeki **2** erişilebilir görev yerelleştirildi. Other içindeki 5 dosya kaynakta açıkça görünmez sinematik takipçi olarak tanımlandığı, BYOS'taki fu_byosshipcraftingtable ve Exploration'daki fuquest_explore1 ise hiçbir runtime tetikleyicisine bağlı olmadığı için dağıtım dışı bırakıldı.

Görev hedefleri gerçek envanter adlarıyla eşlendi: **Densinium Miğferi, Cthulhu Heykeli, Hidroponik Tepsi, Erimiş Çekirdek, Shoggoth Eti, Wagner'ın Kimlik Kartı, Yıpranmış Büyü Kitabı, Precursor Veri Anahtarı, Berbat Mürettebat Yatağı** ve **Mürettebat Tapusu**. create_densinium kaynak renk kapanışı düzeltildi; Precursor görevinin genel “data-disc” ifadesi gerçek hedef olan **Precursor Veri Anahtarı** ile açıklaştırıldı. Geriye dönük kontrolde Battle görevindeki **Cyber Sphere** kullanımı kilitli **Siberküre** terminolojisine birleştirildi.

v0.16 eklemesi **62 yapılandırılmış alan / 21 yeni patch asset**tir: 37 görev alanı, 3 görev-listesi alanı ve 22 bağlı hedef alanı. Kaynak/provenans sonucu **62/62 PASS** (60 pinned FU + 2 vanilla). Proje toplamı **2.154 structured + 15 Lua = 2.169 görünür birim / 399 patch asset** oldu. Planlanan görev klasörlerinin runtime erişilebilir kapsam taraması tamamlandı; oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca yapılmalıdır.

## v0.17 Üretim Makineleri

FU'nun `objects/crafting` ağacındaki **84 .object asseti** envanterlendi. Önceki sürümlerde kapsanan 30 nesne korunarak kalan **54 etkin üretim/makine nesnesinin 295 oyuncuya görünür alanı** yerelleştirildi. Kapsam; envanter adlarını, açıklamaları, alt başlıkları, makine panel başlıklarını ve mevcut ırka özel inceleme cümlelerini içerir.

Yeni 295 alanın tamamı pinned FU 6.5.8 bloblarıyla exact-source doğrulamasından geçti. Patch eşleşmesi **295 test + 295 replace PASS**; renk kodu, kontrol kodu, sayı, yinelenen pointer, boş çeviri ve küçük harfli `mech` kontrolleri temizdir. Pet Healing Station kaynağındaki yanlış **For broken robots** altyazısı, nesnenin gerçek işleviyle uyumlu **Yaralı evcil hayvanlar için** olarak belgeli biçimde düzeltildi.

Proje toplamı **2.449 structured + 15 Lua = 2.464 görünür birim / 453 patch asset** oldu. Bu klasörün seçili görünür kapsamı tamamlandı; diğer eşya/nesne klasörleri ve oyun içi font/panel taşma LQA'sı sonraki turlarda devam eder.

## v0.18 İşlevsel Power, Bees ve Science Outpost Nesneleri

`objects/power`, `objects/bees` ve `objects/scienceoutpost` altındaki daha önce çevrilmemiş **57 aday nesne**, yalnız dosya varlığına göre değil runtime bağlantılarıyla denetlendi. Tarifler, araştırma düğümleri, dükkânlar ve Tiled dungeon yerleşimleri sonucunda **47 erişilebilir nesne** dağıtıma alındı; yalnız tanım veya kullanılmayan tileset kaydı bulunan **10 ölü/bağlantısız nesne** dışarıda bırakıldı.

Yeni kapsam **340 yapılandırılmış alan / 47 patch asset**tir: Power 59, Arıcılık 142, Bilim Karakolu 139. Envanter adları ve açıklamaların yanında ırka özel incelemeler, makine panel başlıkları, güç sensörü/hava istasyonu runtime etiketleri ve Vinalisj, Danışma Noktası ile Starbucks sohbet havuzları da çevrildi. `%s` ve `%%` biçim belirteçleri için yeni regresyon kontrolü eklendi; ham satır sonu içeren geçerli Starbound assetleri de full-source doğrulamaya alındı.

Yeni alanların **340/340'ı pinned FU 6.5.8 kaynağıyla exact doğrulandı**. Proje toplamı **2.789 structured + 15 Lua = 2.804 görünür birim / 500 patch asset** oldu. Oyun içi font, panel taşması, etkileşim ve bağlam LQA'sı hâlâ bekliyor.

## v0.19 Üretim Malzemeleri

`items/generic/crafting` ağacındaki **313 item/consumable asseti** envanterlendi. Önceki sürümlerde kapsanan 52 asset korundu; kalan **261 aday** tarifler, aktif araştırma düğümleri, görev ödülleri, çıkarma/işleme tabloları ve ganimet havuzlarıyla runtime açısından denetlendi. Sonuçta **235 erişilebilir asset** dağıtıma alındı, **26 ölü, deprecated veya bağlantısız asset** dışarıda bırakıldı.

Her etkin assette yalnız oyuncuya görünen `/shortdescription` ve `/description` alanları yerelleştirildi. Kapsam; temel kimyasal ve cevherleri, alaşımları, izotopları, gen örneklerini, Precursor/Mythos bileşenlerini ve Starbooze ara ürünlerini içerir. Teknik `itemName`, kategori, etki, tarif, fiyat ve script alanları değiştirilmedi.

v0.19 eklemesi **470 yapılandırılmış alan / 235 yeni patch asset**tir. Yeni alanların **470/470'i pinned FU 6.5.8 kaynağıyla exact doğrulandı**; patch eşleşmesi **470 test + 470 replace PASS**. Proje toplamı **3.259 structured + 15 Lua = 3.274 görünür birim / 735 patch asset** oldu. Oyun içi envanter, tooltip, font ve bağlam LQA'sı ayrıca yapılmalıdır.

## v0.20 Aktif Özel Görevler

Ana `fu_questlines` kapsamı dışında kalan **97 questtemplate adayı** runtime bağlantılarıyla tek tek denetlendi. Görev başlangıcı, `pickupQuestTemplates`, NPC `offeredQuests`, SAIL görev tablosu, gerçek Tiled dungeon yerleşimi ve görev ödülü zinciri erişilebilirlik kanıtı sayıldı. Sonuçta **29 görev / 112 görünür alan** dağıtıma alındı.

Kapsam; 19 harita/özel bölge görevi, 4 Challenge Labs görevi, 2 Usta Manipülatör görevi ve gerçekten eşya kazanımıyla başlayan 4 Tech görevinden oluşur. Eski teknoloji görevlerinin 44'ü, başlangıcı yorum satırıyla kapatılmış 12 Optional Hardmode görevi, 3 eski Manipülatör görevi, 4 bağlantısız Protectorate alternatifi ve 5 görünmez/geliştirici/yanlış tetiklenmiş görev dağıtım dışı bırakıldı. Ayrıca yanlış `.questtemplat` uzantılı test dosyası canlı görev sayılmadı.

Özel görev yerleri SAIL ve mevcut görev zincirleriyle aynı kalacak biçimde `Brine Star`, `Ancient Temple`, `Evernight Jungle`, `Verdant Ruins` ve benzeri özgün adlarıyla korundu. v0.20 eklemesi **112 yapılandırılmış alan / 29 yeni patch asset**tir; **112 test + 112 replace PASS**. Proje toplamı **3.371 structured + 15 Lua = 3.386 görünür birim / 764 patch asset** oldu. Oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca yapılmalıdır.

## v0.21 Erken Oyun Silahları

`items/active/weapons` altındaki 1.201 gerçek silah dosyasına kör toplu çeviri uygulanmadı. Aktif Zırh ve Silahlar araştırma ağacında oyuncunun erken oyunda doğrudan açtığı `bonegear`, `irongear`, `telebriumgear` ve `tungstengear` düğümleri incelendi. Dört düğümün açtığı **124/124 silahın** gerçek üretim tarifi bulundu.

Önceden çevrilmiş 3 silah korundu; kalan **121 silahta** yalnız envanter adı ve açıklaması yerelleştirildi. Silah ID'leri, tarifler, hasar değerleri, yetenekler, scriptler ve diğer teknik alanlar değiştirilmedi. Broadsword -> **Büyük Kılıç**, Quarterstaff -> **Dövüş Asası**, Rapier -> **Meç**, Staff -> **Asa**, Wand -> **Değnek** olarak kilitlendi; model ve özel adlar korundu.

v0.21 eklemesi **242 yapılandırılmış alan / 121 yeni patch asset**tir; **242 test + 242 replace PASS**. Proje toplamı **3.613 structured + 15 Lua = 3.628 görünür birim / 885 patch asset** oldu. Oyun içi envanter, tooltip genişliği, font ve bağlam LQA'sı ayrıca yapılmalıdır.

## v0.22 Kademe 3 Savaş Ekipmanı ve Tutarlılık Düzeltmeleri

Aktif Zırh ve Silahlar araştırma ağacındaki `titaniumgear`, `carbonarmorgear`, `wastelandgear`, `protocitegear`, `penumbritegear` ve `zerchesiumgear` düğümleri denetlendi. Altı düğümün açtığı **158/158 savaş ekipmanının** etkin üretim tarifi bulundu. Önceden kapsanan F4 Enerji Tüfeği korundu; kalan **157 assette** yalnız envanter adı ve açıklaması yerelleştirildi.

Görev-envanter tutarlılığı için Khe zincirinden gelen kırık augment ile Nanoüreticide onarılan araç birlikte ele alındı. `Broken Master Manipulator`, augment görünen adı ve tamamlanmış araç artık görevlerdeki kilitli **Usta Manipülatör** terimiyle eşleşir. `combatmaneuvering1` içindeki iki belirsiz “Tuhaf eser yanına...” cümlesi de **“Tuhaf eserin yanına...”** olarak düzeltildi.

v0.22 eklemesi **319 yapılandırılmış alan / 159 yeni patch asset**tir: Kademe 3 savaş ekipmanında 314 alan, Usta Manipülatör zincirinde 5 alan. İki görev cümlesi mevcut alanlar içinde düzeltildi. **319 test + 319 replace PASS**; proje toplamı **3.932 structured + 15 Lua = 3.947 görünür birim / 1.044 patch asset** oldu. Oyun içi envanter, tooltip genişliği, font ve bağlam LQA'sı ayrıca yapılmalıdır.

## v0.23 Kademe 4 Çekirdek Savaş Ekipmanı

Aktif Zırh ve Silahlar araştırma ağacındaki `advancealloygear` ve `durasteelgear` düğümleri denetlendi. İki düğümün açtığı **48/48 savaş ekipmanının** etkin üretim tarifi bulundu. Bu sürümde yalnız bu çekirdek Kademe 4 kolları kapsandı; Irradium, Trianglium, Prisilite, Quietus ve biyosilah dalları sonraki paketlere bırakıldı.

48 assette yalnız `/shortdescription` ve `/description` alanları yerelleştirildi. `itemName`, tarifler, hasar, yetenek, mermi, kategori ve script alanları değiştirilmedi. Gauss, Breach ve Stynger gibi aile/model adları korunurken silah sınıfları ve işlev etiketleri Türkçeleştirildi.

v0.23 eklemesi **96 yapılandırılmış alan / 48 yeni patch asset**tir. **96 test + 96 replace PASS**; proje toplamı **4.028 structured + 15 Lua = 4.043 görünür birim / 1.092 patch asset** oldu. Oyun içi envanter, tooltip genişliği, font ve bağlam LQA'sı ayrıca yapılmalıdır.

## v0.24 Kademe 4 Kalan Savaş Ekipmanı

Aktif Zırh ve Silahlar araştırma ağacındaki `irradiumgear`, `triangliumgear`, `prisilitegear`, `quietusgear` ve `bioweaponsgear` düğümleri denetlendi. Beş düğümdeki 209 araştırma açılımından gerçek ve etkin üretim tarifi bulunan **148/148 savaş ekipmanı** yerelleştirildi. Düğümler arasında tekrar veya önceden kapsanmış asset bulunmadı.

148 assette yalnız `/shortdescription` ve `/description` alanları çevrildi. Teknik `itemName`, tarifler, hasar, yetenek, mermi, kategori ve script alanları korunurken renk kodları, sayılar ve satır sonları birebir doğrulandı. Irradium, Trianglium, Prisilite ve Quietus özel malzeme adları korundu; Prisilite silah ailesinde kaynakta kullanılan `Prismatic` sıfatı **Prizmatik**, `Fleshweave` ise **Et Örgüsü** olarak kilitlendi.

v0.24 eklemesi **296 yapılandırılmış alan / 148 yeni patch asset**tir. **296 test + 296 replace PASS**; proje toplamı **4.324 structured + 15 Lua = 4.339 görünür birim / 1.240 patch asset** oldu. Böylece aktif Zırh ve Silahlar ağacındaki seçili Kademe 1-4 üretilebilir savaş ekipmanı kapsamı tamamlandı. Oyun içi envanter, tooltip genişliği, font ve bağlam LQA'sı ayrıca yapılmalıdır.

## v0.25 Kademe 1-2 Aktif Zırh Setleri

Aktif Zırh ve Silahlar ağacındaki `bonegear`, `slimegear1`, `irongear`, `cottongear`, `telebriumgear`, `lunarigear`, `elduugear`, `skathgear` ve `tungstengear` düğümleri runtime kapsamı olarak seçildi. Araştırmanın açtığı zırh kimlikleri gerçek `.recipe` çıktılarıyla çaprazlandı; daha önce çevrilmiş parçalar korunarak kalan **114 zırh asseti** yerelleştirildi.

Bu sürümde yalnız `/shortdescription` ve `/description` alanları çevrildi. Set bonuslarındaki sayı, renk ve kontrol kodları korunurken **Set Bonusları, Kritik Şansı, Kritik Hasarı, Geri Tepme Direnci, Can Çalma, Enerji Yenilenmesi, Germe Hızı** ve **Atış Başına Enerji** ifadeleri tekilleştirildi. EPP araştırma düğümleri ayrı bir ekipman sistemi olduğu için bu zırh dilimine alınmadı.

v0.25 eklemesi **228 yapılandırılmış alan / 114 yeni patch asset**tir. Proje toplamı **4.552 structured + 15 Lua = 4.567 görünür birim / 1.354 patch asset** oldu. Oyun içi zırh tooltip genişliği, set bonusu satırları, font ve bağlam LQA'sı ayrıca bekliyor.

## v0.26 Kademe 3 Aktif Zırh Setleri

Aktif Zırh ve Silahlar ağacındaki `titaniumgear`, `carbonarmorgear`, `wastelandgear`, `protocitegear`, `penumbritegear` ve `zerchesiumgear` düğümleri denetlendi. Araştırmanın açtığı zırh kimlikleri gerçek `.recipe` çıktılarıyla çaprazlandı; **76 üretilebilir zırh parçası** doğrulandı. Science kapsamında daha önce çevrilmiş Mutavisk miğferi korundu, kalan **75 zırh asseti** yerelleştirildi.

Bu sürümde yalnız `/shortdescription` ve `/description` alanları çevrildi. Set bonuslarındaki sayı, renk ve kontrol kodları korundu; E.V.A., Nautilus, Hoplit, Hurdacı, Jandarma, Neishin, Spacepunk ve diğer araştırma zırhlarının envanter adları ile işlevsel tooltipleri Türkçeleştirildi. Kaynakta Kademe 3 araştırmasından açıldığı hâlde dosya yolu `tier4` altında bulunan Ödül Avcısı seti, runtime araştırma ve tarif zinciri esas alınarak kapsama dâhil edildi.

v0.26 eklemesi **150 yapılandırılmış alan / 75 yeni patch asset**tir. Proje toplamı **4.702 structured + 15 Lua = 4.717 görünür birim / 1.429 patch asset** oldu. Oyun içi zırh tooltip genişliği, set bonusu satırları, font ve bağlam LQA'sı ayrıca bekliyor.

## v0.27 Kademe 4 Aktif Zırh Setleri

Aktif Zırh ve Silahlar ağacındaki `advancealloygear`, `durasteelgear`, `irradiumgear`, `triangliumgear`, `prisilitegear`, `quietusgear` ve `bioweaponsgear` düğümleri denetlendi. Araştırma açılımları gerçek `.recipe` çıktılarıyla çaprazlanarak **87 üretilebilir zırh parçası** doğrulandı ve yerelleştirildi.

Bu sürümde yalnız `/shortdescription` ve `/description` alanları çevrildi. Sayı, renk ve kontrol kodları korunurken Korucu, Vahşi Ayı, Püstül, Hücresel, İnferno, Muhafız, İstilacı, Yıldız Katili, Grafen, Intersec, Irradium, Primus, Uzay Yolcusu Mk. 2 ve diğer Kademe 4 setlerinin işlevsel tooltipleri Türkçeleştirildi. Dosya yolu `tier5` altında bulunan Sevimli seti, Kademe 4 araştırma ve tarif zincirinden açıldığı için runtime zinciri esas alınarak kapsama dâhil edildi.

v0.27 eklemesi **174 yapılandırılmış alan / 87 yeni patch asset**tir. Proje toplamı **4.876 structured + 15 Lua = 4.891 görünür birim / 1.516 patch asset** oldu. Oyun içi zırh tooltip genişliği, set bonusu satırları, font ve bağlam LQA'sı ayrıca bekliyor.

## Yol haritası

- [x] Jeoloji araştırma ağacının ilk çevirisi
- [x] Başlangıç görevlerinin ilk paketi
- [x] Başlangıç telsiz ve öğretici mesajlarının ilk paketi
- [x] v0.1.1 Anayasa uyum düzeltmesi
- [x] Tarım araştırma ağacı
- [x] Kimya araştırma ağacı
- [x] Mühendislik araştırma ağacı
- [x] v0.4 geriye dönük statik QA ve eksik alan temizliği
- [x] v0.5 Güç Sistemleri ve bağlı temel makineler
- [x] Güç Sistemleri araştırma ağacı
- [x] Zanaatkârlık araştırma ağacı
- [x] Zırh ve Silahlar araştırma ağacı
- [x] v0.7 geriye dönük aktif-düğüm / ölü-string QA
- [x] Delilik araştırma ağacı
- [x] Tutorial görev ailesi
- [x] Science görev zincirleri
- [x] Outpost görev zincirleri (İçki 12/12 + Arıcılık 13/13 + Bilim Karakolu dükkânları 6/6 + Kevin 9/9 + Khe 4/4)
- [x] Battle görev zincirleri (10/10 erişilebilir; 3 bağlantısız legacy dağıtım dışı)
- [x] Other görev zincirleri (8 erişilebilir; 5 görünmez takipçi dağıtım dışı)
- [x] BYOS kalan görevleri (2 erişilebilir; 1 bağlantısız legacy dağıtım dışı)
- [x] Exploration görev zinciri (1 bağlantısız legacy runtime denetimiyle dağıtım dışı)
- [x] Ana görev aileleri dışındaki özel görevlerin runtime denetimi (29 erişilebilir görev; 68 erişilemez/görünmez dosya dağıtım dışı)
- [ ] Eşya ve makine açıklamalarının geniş kapsamlı çevirisi (`objects/crafting`: 84/84; v0.18 Power/Bees/Science Outpost: 47/47; v0.19 `items/generic/crafting`: 235/235; v0.21 erken oyun: 124/124; v0.22 Kademe 3: 158/158; v0.23-v0.24 Kademe 4: 196/196 üretilebilir savaş ekipmanı; v0.25-v0.27 Kademe 1-4 aktif zırhlar: 276 yeni asset tamamlandı; kalan zırh kademeleri ve diğer eşya/nesne klasörleri sürüyor)
- [x] Planlanan görev klasörlerinin runtime denetimi ve erişilebilir çevirileri
- [ ] Oyun içi tam LQA ve taşma kontrolleri

## Kaynak ve lisans

Orijinal çalışma: Frackin' Universe, sayter ve katkıda bulunanlar.

Frackin' Universe kaynak deposu CC BY 4.0 lisansı belirtmektedir. Ayrıntılar `docs/KAYNAK_VE_LISANS.txt` içindedir.

Bu proje Frackin' Universe ekibi, Chucklefish veya Starbound geliştiricileri tarafından hazırlanmış ya da onaylanmış resmî bir çeviri değildir.
