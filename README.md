# Frackin' Universe Türkçe

Frackin' Universe için topluluk tabanlı, gayriresmî Türkçe yerelleştirme projesi.

**Durum: v0.14 Beta / Ana araştırma sistemleri + Delilik/Metafizik + Tutorial + Science + Outpost İçki + Arıcılık + Bilim Karakolu dükkânları + Kevin/Khe görevleri / statik QA tamamlandı, oyun içi LQA bekliyor.**

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
- Zırh ve Silahlar ağacının doğrudan yönlendirdiği Zırh Atölyesi, Örs yükseltmeleri ve Solunum EPP'si
- Zanaatkârlığın doğrudan referans verdiği koloni, mutfak, dikiş, biyokimya ve temel üretim istasyonları
- Güç Sistemlerinin doğrudan bağlı temel üretim, reaktör, pil, santrifüj ve atmosfer makineleri
- Başlangıç görevlerinin bir bölümü ve BYOS Yıldızlararası Yolculuk zinciri
- Başlangıç telsiz/öğretici mesajlarının mevcut dosyadaki 26/26 metni
- İmalat Tezgâhı yükseltme kademeleri ve seçili arayüz metinleri
- Tarım/genetik makineleri ve temel Tarım öğretici görevleri
- Kimya Laboratuvarı ve doğrudan bağlı temel kimya kaynakları
- Mühendislikteki temel çıkarma, araştırma, gemi ve çekirdek makineleri/kaynakları
- STL Motoru ve Küçük FTL Motoru oyuncu metinleri
- Araştırma ekranındaki seçili açıklamalar, fallback metinleri ve Lua içine gömülü sabit UI metinleri

Toplam **1.934 yapılandırılmış oyuncu metni alanı** ve **15 Lua UI metni**, yani **1.949 yerelleştirilmiş görünür metin birimi** bulunmaktadır. Bu, FU'nun tamamının Türkçe olduğu anlamına gelmez.

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

> **Paket notu:** Güncel beta paketi `dist/FU_Turkce_v0.14.0_Beta.zip` olarak GitHub Actions tarafından statik QA sonrasında otomatik üretilir.

## Sürüm uyumluluğu

```text
FU sürümü: 6.5.8
Kaynak commit: 329e714b3fe87571055c8ad7aa38135d199d3317
```

Güncel statik QA'da toplam yapılandırılmış kapsam **2.028 alan / 358 patch asset**tir. v0.14 Kevin/Khe paketindeki **94/94 yeni alan kaynak/provenans açısından doğrulandı**: 84 pinned FU ve 10 vanilla alan. Önceki Outpost paketlerinin provenans kontrolleri de korunuyor. Araştırma ekranının JSON Patch dışında kalan **1 Lua assetindeki 15 görünür metin** exact kaynak-fragment korumasıyla ayrıca doğrulanır.

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

Science cephesi v0.10 ile kapandı. Outpost'ta v0.11 İçki, v0.12 Arıcılık, v0.13 Bilim Karakolu dükkânları ve v0.14 Kevin/Khe görevleri işlendi; Arıcılıktaki `13mites` runtime'da bağlantısız olduğu için dağıtım dışı bırakıldı. Klasör-bazlı yol haritasında sırada **30 ham görev dosyası** bulunuyor: Battle 13, Other 13, BYOS 3 ve Exploration 1. Her kategori işlenirken yalnız klasör sayısına değil runtime quest-list/NPC bağlantılarına da bakılacak.

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
- [ ] Battle görev zincirleri
- [ ] Other görev zincirleri
- [ ] BYOS kalan görevleri
- [ ] Exploration görev zinciri
- [ ] Eşya ve makine açıklamalarının geniş kapsamlı çevirisi
- [ ] Görevlerin kalan bölümü
- [ ] Oyun içi tam LQA ve taşma kontrolleri

## Kaynak ve lisans

Orijinal çalışma: Frackin' Universe, sayter ve katkıda bulunanlar.

Frackin' Universe kaynak deposu CC BY 4.0 lisansı belirtmektedir. Ayrıntılar `docs/KAYNAK_VE_LISANS.txt` içindedir.

Bu proje Frackin' Universe ekibi, Chucklefish veya Starbound geliştiricileri tarafından hazırlanmış ya da onaylanmış resmî bir çeviri değildir.
