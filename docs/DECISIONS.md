# FU TÜRKÇE Karar Kaydı

## 2026-09-19 - Anayasa uyum düzeltmesi v0.1.1

- Oyuncuya gösterilen Türkçe adların yanındaki İngilizce parantez açıklamaları kaldırıldı.
- ASCII / Türkçe karaktersiz dağıtım iptal edildi. Font sorunu olursa Türkçeyi bozmak yerine font/LQA sorunu olarak ele alınacak.
- Research için bağlama göre iki kilitli kullanım tanımlandı: sistem adı **Araştırma**, eylem/buton **Araştır**.
- **Precursor** FU kaynaklarında species/özel ad olarak geçtiği için çevrilmeden korunacak.
- **Homestead I** geçici olarak **Yerleşim I** yapıldı; görev serisinin I-V bölümleri tamamlandığında karar yeniden değerlendirilecek (REVIEW).
- Kaynak Greenhouse görevindeki tekrar açılan `^orange;` biçimlendirmesi Türkçe yamada bilinçli olarak `^reset;` ile kapatıldı. Bu tek kaynak-format düzeltmesi QA istisnası olarak kaydedildi.
- Oyuncuya gösterilen sabit ondalıklar Türkçe biçimde virgülle yazılabilir: 2,5 / %17,3.

## 2026-09-19 - v0.2 Tarım

- Tarım araştırma ağacının 50 araştırma düğümü bütün olarak yerelleştirildi.
- Tarım ağacının doğrudan yönlendirdiği FU makineleri aynı sürümde çevrildi.
- Sprouting Table -> **Filizlendirme Tezgâhı**, Growing Tray -> **Yetiştirme Tepsisi**, Heatlamp Tray -> **Isı Lambalı Tepsi**, Hydro Tray -> **Hidroponik Tepsi** LOCKED.
- Xeno özel ad olarak korunur: **Xeno Araştırma Laboratuvarı**.
- Quantum Fluid -> **Kuantum Sıvısı**, Alien Compound -> **Uzaylı Bileşiği**, Caliginous Gas -> **Caliginous Gazı**.
- `create_growingtray` kaynak metnindeki `^oraange;` renk yazım hatası düzeltildi.
- Aynı görevin yanlış Armorworks teslim hedefi, gerçek koşul olan `fu_growingtray` ile uyumlu biçimde **Yetiştirme Tepsisi** yapıldı.

## 2026-09-19 - v0.3 Kimya

- Kimya araştırma ağacındaki 71 oyuncu metni bütün olarak yerelleştirildi.
- Araştırma ağacının doğrudan referans verdiği 9 makine/kaynak assetindeki 32 oyuncu metni aynı pakete alındı.
- Toplam v0.3 eklemesi: **10 asset / 103 oyuncu metni**.
- Chemistry Lab -> **Kimya Laboratuvarı**, Bio-Chem Lab -> **Biyokimya Laboratuvarı**, Advanced Plastic -> **Gelişmiş Plastik** LOCKED.
- Cell Material -> **Hücre Materyali**, Spliced Cell -> **Birleştirilmiş Hücre**, Unstable Particles -> **Kararsız Parçacıklar** LOCKED.
- Metallic Hydrogen -> **Metalik Hidrojen**, Quietus Ore -> **Quietus Cevheri**, Ammonium Sulfate -> **Amonyum Sülfat**, Hand Mill -> **El Değirmeni** LOCKED.
- Quietus özel FU terimi olarak korunur; yalnızca nesne türü olan “Ore” Türkçeleştirilir.
- Yeni 103 alan, FU 6.5.8 kaynak commit'i `329e714b3fe87571055c8ad7aa38135d199d3317` üzerinden pointer bazında **103/103 PASS** doğrulandı.
- Renk/kontrol kodu ve sayı bütünlüğü yeni alanlarda **PASS**. Oyun içi LQA henüz yapılmadı.

## 2026-09-20 - v0.4 Mühendislik

- Mühendislik araştırma ağacının 69 düğümündeki 139 oyuncu metni bütün olarak yerelleştirildi.
- Doğrudan bağlı 15 temel makine/kaynak assetindeki 52 oyuncu metni aynı pakete alındı.
- v0.4 yeni içerik toplamı: **16 asset / 191 oyuncu metni**.
- Engineering -> **Mühendislik** mevcut LOCKED kararı korundu.
- Mech, Tech, EPP, FTL sistem/kısaltma adları çevrilmeden korunacak şekilde LOCKED yapıldı.
- STL Drive -> **STL Motoru**, Extraction Lab -> **Çıkarma Laboratuvarı**, Ship Component Assembler -> **Gemi Bileşeni Birleştirici**, Quantum Manipulator -> **Kuantum Manipülatörü** LOCKED.
- Focusing Array -> **Odaklama Dizisi**, Power Core -> **Güç Çekirdeği**, Nuclear Core -> **Nükleer Çekirdek**, Particle Core -> **Parçacık Çekirdeği** LOCKED.
- Araştırma seviye sıfatları standardize edildi: Improved -> **Geliştirilmiş**, Advanced -> **Gelişmiş**, Superior -> **Üstün**, Peerless -> **Eşsiz**.
- Bu karar nedeniyle Kimya ağacındaki üç eski Peerless başlığı **Eşsiz** karşılığına geçirildi.
- Kaynak Mühendislik metninde “Ship Crafting Table” denmesine rağmen gerçek FU nesnesi fu_shipcraftingtable oyuncuya **Ship Component Assembler** adıyla gösterildiği için Türkçede gerçek nesne adı **Gemi Bileşeni Birleştirici** kullanıldı. Bu, oyuncu takip bütünlüğü için bilinçli kaynak-ad uyarlamasıdır.
- Yeni 191 alan, FU 6.5.8 kaynak commit'i `329e714b3fe87571055c8ad7aa38135d199d3317` üzerinden pointer bazında **191/191 PASS** doğrulandı.
- Oyun içi LQA henüz yapılmadı.
## 2026-09-20 - Geriye dönük QA düzeltmeleri

- v0.4 tabanındaki **654 yapılandırılmış oyuncu metni** yeniden denetlendi; eksik görünür alan taramasıyla kapsam **689 JSON/JSONC alanına** çıkarıldı.
- Araştırma ekranındaki JSON Patch ile değiştirilemeyen **15 Lua sabit UI metni** ayrıca kaynak-kilitli ham override olarak yerelleştirildi. Toplam yerelleştirilmiş görünür metin birimi **704** oldu.
- Yapılandırılmış kapsam **64 patch asset**, Lua kapsamı **1 ham override asset** olmak üzere toplam **65 hedef asset** içeriyor.
- FU kaynağı sabit referans olarak 6.5.8 / `329e714b3fe87571055c8ad7aa38135d199d3317` commit'inde tutuluyor.

### Düzeltilen çeviri ve terminoloji hataları

- Jeoloji metninde kalan `(Inventor’s Table)` İngilizce parantez açıklaması kaldırıldı.
- `Extraction Lab` kullanımı **Çıkarma Laboratuvarı**, `Advanced Beekeeping` **Gelişmiş Arıcılık** ile eşleştirildi.
- Terraforming ailesi tekleştirildi: **Gezegen Biçimlendirme**, **Mikro Biçimlendirici**, **Gezegen Biçimlendirici** LOCKED.
- `Tech Upgrades` -> **Tech Yükseltmeleri** yapılarak Starbound sistem adı olan **Tech** korundu.
- `Complex Plastics` yanlışlıkla `Advanced` ile aynılaştırılmıştı; **Karmaşık Plastikler** yapıldı. `Complex` -> **Karmaşık** LOCKED.
- Gelişmiş Xeno Laboratuvarı açıklamasında “Quantum Xeno Lab” nesne adı gibi kullanılmıyor; nesne adı **Gelişmiş Xeno Laboratuvarı**, kuantum bilgisi açıklama niteliğinde tutuluyor.
- Mühendislikte Mech Parçası Üretim Tezgâhına gönderme yapan belirsiz “bir tane araştırabilir” ifadesi, araştırılan nesneyi açıkça belirtecek şekilde düzeltildi.
- Görev yönlendirmelerindeki “alanını araştır” gibi İngilizce söz dizimi temizlenerek oyuncunun menüde ne açacağı açıklaştırıldı.

### Eksik metin ve kaynak-hata düzeltmeleri

- **Filizlendirme Tezgâhı** için kaynakta bulunan ancak yamada eksik kalan Apex, Avian, Floran, Glitch, Human ve Hylotl inceleme cümleleri eklendi.
- **Arı Barınağı** arayüzünde eksik kalan `Buy`, `Cancel`, `Search` ve `Replace Me` metinleri çevrildi.
- `radiomessages/fu_quests.radiomessages` dosyasındaki 26 oyuncu mesajının tamamı karşılaştırıldı; eksik kalan 4 BYOS/FTL mesajı eklendi.
- Bu mesajların bağlı olduğu `fu_byosftldrive` görevi bütünüyle yerelleştirildi: başlık, ana metin, tamamlanma metni ve 3 hedef.
- Görev zincirinin açtığı gerçek `fu_ftldrivesmall` nesnesi **Küçük FTL Motoru** olarak çevrildi; açıklama ve 7 ırka özel inceleme metni de eklendi.
- `create_electronics`, `create_greenhouse` ve `create_tinkertable` kaynaklarında teslim metni yanlışlıkla **Armorworks** diyor. Türkçe metinler kaynak koşullarındaki gerçek `itemName` değerleri esas alınarak sırasıyla **Elektronik Merkezi**, **Sera** ve **İnce İşçilik Tezgâhı** yapıldı.
- Daha önce belgelenen `create_growingtray` Armorworks hatasında da aynı ilke korunuyor: gerçek koşul `fu_growingtray` olduğu için **Yetiştirme Tepsisi** kullanılıyor.
- Tarım `farming3` açıklaması kaynakta “Growing Tray” dese de düğümün gerçek açtığı nesne `isn_hydroponicstray` / **Hidroponik Tepsi** olduğu için oyuncu takip bütünlüğü adına gerçek nesne adı korunuyor.
- **Garp Berry** ve **Blister Bush**, FU eşya/bitki adlarıyla eşleşen özel adlar olarak LOCKED; İngilizce kaçak sayılmıyor.

### Araştırma ekranı Lua güvenliği

- `researchTree.lua` içinde config dışında kalan 15 sabit oyuncu metni Türkçeleştirildi: araştırma ağacı seçimi, arama yönlendirmesi, kaynak/eşya tüketim uyarıları, boş-ağaç uyarıları, salt-okunur metni, Piksel/Öz etiketleri ve hata/fallback metinleri.
- Script mantığı elle yeniden yazılmadı. `tools/raw_text_translations.json` yalnızca beklenen kaynak kod parçalarını ve Türkçe karşılıklarını tutuyor.
- `build_validate.py`, açılmış FU kaynağı verilirse her ham metnin exact-match sayısını doğrulayıp o kaynak script üzerinden override üretir; eşleşme bozulursa build hata verir.
- Kaynak klasörü verilmeden build alındığında 6.5.8 için doğrulanmış `tools/raw_overrides/zb/researchTree/researchTree.lua` şablonu kullanılır.

### QA sonucu

- Yapılandırılmış **689 alanda** yinelenen asset/pointer: **0**.
- Boş Türkçe değer: **0**.
- Belgeli kaynak renk-kodu düzeltmeleri dışında placeholder / kontrol kodu / renk kodu / sayı bütünlüğü: **PASS**.
- Eski hatalı karşılıklar (`Özütleme Laboratuvarı`, `İleri Arıcılık`, `Gezegen Dönüşümü`, `Mikro Dönüştürücü`, `Gezegen Dönüştürücü`, `Teknoloji Yükseltmeleri`, `Kuantum Xeno Laboratuvarı`, `Gelişmiş Plastikler`) repository ledger'ında kalmadı.
- Aynı kaynak stringin farklı Türkçeye çevrildiği iki durum bilinçlidir: **Research -> Araştırma/Araştır** bağlam ayrımı ve FU'nun hatalı Armorworks teslim metinlerinin gerçek görev koşuluna göre düzeltilmesi.
- Önceki 654/654 exact-source doğrulaması korunuyor; eklenen 35 yapılandırılmış alan kaynak ve patch değerleriyle doğrulandı. Bugün değiştirilen yüksek etkili 8 asset ayrıca **432/432**, eksik yakalanan 10 asset ise **77/77** kaynak/ledger/patch eşleşmesiyle yeniden kontrol edildi.
- Oyun içi LQA, font ve panel taşma testi bu statik denetimin parçası değildir ve hâlâ yapılmalıdır.

## 2026-09-20 - v0.5 Güç Sistemleri

- `fu_power` araştırma ağacındaki 39 düğümün 81 oyuncu metni bütün olarak yerelleştirildi.
- Doğrudan bağlı 32 güç/işleme/atmosfer makinesi assetindeki 139 oyuncu metni aynı sürüme alındı.
- v0.5 yeni içerik toplamı: **33 asset / 220 yapılandırılmış alan**.
- Proje toplamı **909 yapılandırılmış alan + 15 Lua UI metni = 924 görünür metin birimi** oldu.
- Kaynak `fu_power` ağaç başlığı **Electronics**, fakat FU içi çapraz referanslar bu ağacı **Power Systems** diye adlandırıyor. Oyuncunun yönlendirmeleri takip edebilmesi için ağaç adı Türkçede **Güç Sistemleri** olarak LOCKED yapıldı; ağacın içindeki Electronics düğümü **Elektronik** olarak ayrıştırıldı.
- Steam Power kaynak açıklamasındaki “hydraulic piston” ifadesi, araştırmanın gerçekten açtığı `hydraulicdynamo` nesnesinin oyuncu adıyla eşleştirilerek **Hidrolik Dinamo** olarak kullanıldı.
- Combustion kaynak metnindeki **Combustion Engine**, gerçek açılan nesnenin `shortdescription` değeri **Combustion Generator** olduğu için Türkçede **Yanmalı Jeneratör** olarak standardize edildi.
- Silicon -> **Silisyum**, Blast Furnace -> **Yüksek Fırın**, Arc Smelter -> **Ark Ergitici**, Fission Reactor -> **Fisyon Reaktörü**, Quantum Nucleonics -> **Kuantum Nükleoniği** LOCKED.
- Güneş üretim zinciri **Güneş Paneli -> Güneş Dizisi -> Güneş Kulesi** olarak standardize edildi.
- Santrifüj zinciri **Endüstriyel Santrifüj -> Laboratuvar Santrifüjü -> Gaz Santrifüjü** olarak standardize edildi.
- Yeni 220 alan FU 6.5.8 kaynak commit'i `329e714b3fe87571055c8ad7aa38135d199d3317` üzerinden pointer bazında **220/220 PASS** doğrulandı.
- Renk kodu, kontrol kodu, sayı ve yinelenen pointer kontrolleri v0.5 yeni içerikte **PASS**.
- Oyun içi LQA, panel taşması ve üretim/yakıt zinciri testi henüz yapılmadı.

## 2026-09-20 - v0.6 Zanaatkârlık

- Çalışma `work/v0.6-craftsmanship` dalında başlatıldı; mevcut v0.5 beta paketi değiştirilmedi.
- `fu_craftsmanship` araştırma ağacındaki 76 gerçek araştırma düğümünün başlık ve açıklamaları bütün olarak yerelleştirildi.
- Ağaç adı, görünür `default` yardım/fallback çifti ve 76 düğüm metniyle **155 yapılandırılmış oyuncu metni alanı** eklendi. Kaynakta olup hiçbir düğüme bağlı olmayan `workbenchatechy/0-1` oyuncuya görünmediği için dağıtımdan çıkarıldı.
- Craftsmanship -> **Zanaatkârlık** LOCKED.
- Improved / Advanced / Superior / Peerless için mevcut kilitli sıfatlar korunarak Geliştirilmiş / Gelişmiş / Üstün / Eşsiz kullanıldı.
- Bilim Karakolu, Mucit Tezgâhı, Grafen, Penumbrite, Nocxium, Trianglium ve Durasteel gibi daha önce kilitlenmiş adlar aynen korundu.
- Ağaç metninde geçen Mutfak Tezgâhı, Koloni İstasyonu, Koloni Çekirdeği, Dikiş Makinesi, Kar Yazıcısı ve Biyokimyacı Tezgâhı gibi doğrudan oyuncu referansları bağlı asset geçişinde kaynak adlarıyla doğrulanacak; bu çalışma tamamlanmadan v0.6 sürümü bitmiş sayılmayacak.

### v0.6 bağlı makine ilk geçişi

- İlk bağlı paket 6 FU-owned asset / 50 oyuncu metni olarak eklendi.
- Colony Station -> **Koloni İstasyonu**, Colony Core -> **Koloni Çekirdeği**, Colony Deed Mark II -> **Koloni Tapusu Mark II**, Snowprinter -> **Kar Yazıcısı**, The Lamporium -> **Lamporium** LOCKED.
- Zanaatkârlık araştırma metni kaynakta `Mk2 Tenant Deeds` derken gerçek eşya `shortdescription` değeri **Colony Deed Mark II**. Oyuncunun araştırma ekranından envantere aynı adı takip edebilmesi için Türkçede **Koloni Tapusu Mark II** kullanıldı.
- Aynı nedenle Koloni Çekirdeği açıklamasındaki kaynak `MK2 deeds` ifadesi de gerçek eşya adına eşlendi. Bu iki alan sayı-token QA istisnası olarak açıkça kayıt altına alındı.
- v0.6 nihai beta kapsamı **286/286** kaynak/provenans doğrulaması, 0 yinelenen pointer, 0 boş çeviri ve sağlam renk/kontrol kodlarıyla PASS.
- Vanilla nesneleri FU `.patch` katmanıyla değiştiren Mutfak Tezgâhı, dikiş istasyonu ve benzeri bağlı istasyonlar doğrudan FU-owned nesneler gibi ele alınmayacak; güvenli birleşik patch yöntemi doğrulanmadan ana dala alınmayacak.

### v0.6 katmanlı vanilla asset stratejisi

- FU bazı vanilla Starbound nesnelerini tam nesne olarak değil `.object.patch` ile değiştiriyor. Bunlar FU-owned `.object` assetleriyle aynı şekilde kaynak doğrulanamaz.
- İlk güvenli örnek `woodencookingtable`: FU patchi `/upgradeStages` dizisini tamamen oluşturduğu için Mutfak Tezgâhı ve Şef Mutfağı metinleri doğrudan bu FU patchinden exact kaynak değeriyle alınır. Türkçe mod, FU'dan sonra aynı hedef assete test/replace patch uygular.
- Kitchen Counter -> **Mutfak Tezgâhı**, Chef's Kitchen -> **Şef Mutfağı** LOCKED.
- `slimecentrifuge` FU-owned tam nesne olduğu için standart exact-source yöntemiyle çevrildi. Biochemist Table -> **Biyokimyacı Tezgâhı**, Biochemist Centrifuge -> **Biyokimyacı Santrifüjü**, Biochemist Microseparator -> **Biyokimyacı Mikroayırıcısı** LOCKED.
- Dikiş Makinesi / `craftingwheel` FU patchi yalnızca vanilla nesnenin bazı kademelerini değiştiriyor. İlk kademe gerçek envanter adı vanilla kaynak doğrulanmadan kilitlenmeyecek; araştırma metnindeki ad tek başına kaynak kabul edilmeyecek.

### v0.6 craftingwheel doğrulaması

- `craftingwheel` vanilla tabanlı, FU tarafından kısmen patchlenen üç kademeli bir istasyondur.
- Vanilla adları bağımsız Starbound Patch Project test değerleriyle doğrulandı: **Spinning Wheel** (ana/1. kademe) ve **Sewing Machine** (2. kademe). FU bu iki kısa adı değiştirmiyor.
- FU pinned kaynak patchi 3. kademe olarak **Clothing Fabricator** ekliyor.
- Türkçe aile: **Çıkrık -> Dikiş Makinesi -> Giysi Üreticisi**. Üçü LOCKED.
- Vanilla kısa adlarındaki hatalı/eski `^white;` kapanışı Türkçe yamada `^reset;` ile kapatılır; bu bilinçli renk-kodu QA düzeltmesidir.
- Zanaatkârlık `canvas` araştırmasındaki Sewing Machine referansı gerçek 2. kademe envanter adıyla doğrulandı.

### v0.6 vanilla tezgâh adları

- Zanaatkârlık ağacının doğrudan yönlendirdiği vanilla tezgâh adları, kaynak değerlerini test eden bağımsız Starbound Patch Project kayıtlarıyla doğrulandı.
- **Wooden Workbench -> Ahşap Tezgâh**, **Industrial Workbench -> Endüstriyel Tezgâh** LOCKED.
- **Inventor's Table -> Mucit Tezgâhı**, **Engineer's Table -> Mühendis Tezgâhı**, **Architect's Table -> Mimar Tezgâhı** LOCKED.
- FU bu iki vanilla nesneye kendi kaynak ağacında ek `.object.patch` uygulamıyor. Bu yüzden yalnızca exact doğrulanmış kısa adlar çevrildi; açıklamalar tahmin edilmedi.
- Vanilla kısa adlarındaki `^white;` kapanışı Türkçe patchte `^reset;` olarak düzeltilir ve belgeli renk-kodu istisnası sayılır.

### v0.6 beta kapsam kapanışı

- Zanaatkârlık beta kapsamı **155 ağaç/fallback alanı + 131 bağlı makine/tezgâh alanı = 286 yeni yapılandırılmış alan** olarak kapatıldı.
- Proje toplamı **1195 yapılandırılmış alan + 15 Lua UI metni = 1210 görünür metin birimi** oldu.
- 243 v0.6 alanı pinned FU-owned kaynaklardan, 33 alan pinned FU `.patch` katmanlarından, 10 vanilla kısa ad alanı bağımsız test değerlerinden doğrulandı.
- `workbenchatechy` string çifti kaynakta mevcut olsa da `researchTree.fu_craftsmanship` içinde karşılık gelen düğüm bulunmadığından oyuncuya görünür kapsam sayılmadı ve yamadan çıkarıldı.
- Oyun içi LQA, font ve panel taşma testleri tamamlanmadığı için sürüm Beta olarak kalır.

## 2026-09-20 - v0.7 Zırh ve Silahlar

- Çalışma `work/v0.7-warcraft` dalında başlatıldı; main dalındaki v0.6 beta korunuyor.
- `fu_warcraft` ağacında **47 gerçek araştırma düğümü** var. `default` yardım/fallback çifti ve ağaç adıyla ilk geçiş **97 görünür alan** içeriyor; ölü/bağlantısız string bulunmadı.
- Armor and Weapons -> **Zırh ve Silahlar** mevcut LOCKED kararı korunuyor.
- Kaynakta araştırmanın açtığı gerçek FU `armory` nesnesi aynı pakete bağlandı: **Zırh Atölyesi -> Montaj Hattı -> Cephanelik**.
- Eski vanilla silah istasyonu zinciri harici vanilla test değerleriyle doğrulandı: **Örs -> Dövme Ocağı -> Çoğaltıcı**.
- Tungsten araştırmasının açtığı `breathprotectionback` gerçek kısa adı **Breathing EPP** olarak vanilla kaynaktan doğrulandı; Türkçesi **Solunum EPP'si** LOCKED.
- `depleted uranium` bilimsel olarak **tüketilmiş uranyum** karşılığıyla standardize edildi; önceki geçici `seyreltilmiş uranyum` kullanılmayacak.
- `Wastelander Equipment` özel ad olmadığı ve açıklama doğrudan kıyamet sonrası hurda ekipmanını anlattığı için **Kıyamet Sonrası Ekipman** olarak çevrildi.
- İlk v0.7 bağlı paketle mevcut kapsam **117 yeni alan** oldu. Oyun içi LQA henüz yapılmadı.

### v0.7 beta kapsam kapanışı

- Zırh ve Silahlar beta kapsamı **97 ağaç/fallback alanı + 20 bağlı istasyon/EPP alanı = 117 yeni yapılandırılmış alan** olarak kapatıldı.
- Proje toplamı **1312 yapılandırılmış alan + 15 Lua UI metni = 1327 görünür metin birimi** oldu.
- 111 v0.7 alanı pinned FU kaynağından, 4 Örs zinciri alanı bağımsız vanilla test değerlerinden, 2 Solunum EPP alanı vanilla Starbound asset kaynağından doğrulandı.
- Zırh Atölyesi yükseltme ailesi **Zırh Atölyesi -> Montaj Hattı -> Cephanelik**; vanilla silah istasyonu ailesi **Örs -> Dövme Ocağı -> Çoğaltıcı** olarak LOCKED.
- Oyun içi LQA, font ve panel taşma testleri tamamlanmadığı için sürüm Beta olarak kalır.

## 2026-09-20 - v0.7 geriye dönük aktif-düğüm ve anlam QA

- Pinned FU 6.5.8 araştırma ağaçları ile `researchTree.lua` birlikte yeniden incelendi.
- `strings.research.default` çiftlerinin arayüz kodu tarafından okunmadığı; boş seçimde gerçek fallback'in `data.strings.info` üzerinden geldiği doğrulandı.
- Aktif `researchTree` düğümleri ile ledger pointer'ları çaprazlandı. Toplam **36 runtime-inaktif araştırma alanı** yamadan çıkarıldı: Jeoloji 20, Tarım 2, Kimya 4, Mühendislik 2, Güç Sistemleri 4, Zanaatkârlık 2, Zırh ve Silahlar 2.
- Jeolojide eski/bağlantısız `metals_tier7`, `metals_morphite`, `metals_nocxium`, `metals_plasmiccrystal`, `metals_diamond`, `metals_alloy5`, `metals_alloy6`, `isotopes6`, `terraforming1-3`; Kimyada `elduucrystals`; Güç Sistemlerinde `ansible` araştırma metinleri aktif düğüm olmadığı için dağıtımdan çıkarıldı.
- Önceki **1312 yapılandırılmış / 1327 toplam görünür birim** sayımı bu ölü alanları içeriyordu. Güncel aktif kapsam **1276 yapılandırılmış alan + 15 Lua UI metni = 1291 yerelleştirilmiş görünür birim** olarak düzeltildi.
- Kilitli terim hatası düzeltildi: `Arc Smelter` referansındaki **Ark Eritici** -> **Ark Ergitici**.
- Bilimsel/terminoloji hatası düzeltildi: `organic silicon` içindeki **organik silikon** -> **organik silisyum**; `Silicon -> Silisyum` LOCKED kararıyla eşlendi.
- Başlangıç görevindeki üç hedefte kalan “alanında araştırma yap” yapısı kaldırıldı; oyuncuya ilgili araştırma ağacında hangi nesne araştırmasını açıp üretmesi gerektiği açıkça yazıldı.
- Başlangıç telsizinde Karanlık Mağara enerji kaynağı cümlesi ve Tarım araştırma yönlendirmesi daha açık, takip edilebilir Türkçeye çevrildi.
- `build_validate.py` artık pinned 6.5.8 kaynağında aktif düğüme bağlı olmadığı bilinen araştırma stringleri ledger'a yeniden eklenirse build'i durdurur.
- Bu tur statik/kaynak QA'dır. Oyun içi LQA, font ve panel taşma testleri hâlâ ayrı olarak bekliyor.

## 2026-09-20 - v0.8 Delilik / Metafizik

- `zb/researchTree/madness.config` içinde **31 aktif araştırma düğümü** doğrulandı.
- Kaynaktaki `strings.research.default` yardım çifti `researchTree.lua` tarafından kullanılmadığı için v0.8 kapsamına alınmadı.
- Ağaç adı **Metafizik [ Delilik ]** olarak yerelleştirildi.
- Aktif ağaç kapsamı: **31 düğüm x 2 alan + ağaç adı = 63 alan**.
- Delilik sisteminin takip edilebilirliği için 17 bağlı assette **40 oyuncu metni** aynı sürüme alındı.
- v0.8 toplam ekleme: **103 yapılandırılmış alan / 18 hedef asset**.
- Madness -> **Delilik**, Metaphysics -> **Metafizik**, Psionics -> **Psiyonik**, Psionic Energy -> **Psiyonik Enerji**, Psionic Focus -> **Psiyonik Odak** LOCKED.
- Brain Extractor -> **Beyin Çıkarıcı**, Psionics Table -> **Psiyonik Tezgâhı**, Psionic Amplifier -> **Psiyonik Yükselteç**, Matter Converter -> **Madde Dönüştürücü**, Autopsy Table -> **Otopsi Masası** LOCKED.
- Insta-Freud özel ürün/cihaz adı olarak korunur.
- Astral Projection -> **Astral Projeksiyon**, Dimensional Phasing -> **Boyutsal Faz Geçişi** LOCKED.
- Psi enerji zinciri **Psi-1 Enerjisi -> Psi-2 Enerjisi -> Psi-3 Enerjisi -> Psi-4 Enerjisi** olarak standardize edildi.
- Eski çalışma dalındaki geçici **Psionik**, **Astral Yansıtma**, **Psionik Kanallama**, **Ortaya Çıkan Teknoloji** ve **Karanlık Madde Teçhizatı** karşılıkları ana sürüme taşınmadı.
- Delilik ağacı ve bağlı 18 assetteki **103/103 kaynak değer** pinned FU 6.5.8 commitinden exact doğrulandı.
- Oyun içi LQA, panel taşması ve Delilik ilerleme zincirinin oyun içi testi hâlâ bekliyor.

## 2026-09-20 - v0.9 Tutorial görev ailesi

- FU `quests/fu_questlines/tutorial` kapsamı envanterlendi: kaynakta 42 questtemplate var.
- `start_basics1` yalnızca kendi dosyasında geçen, metni `Try making` ile yarıda kesilmiş, başlığı Armament iken koşulu tekrar 5 patates isteyen kırık/bağlantısız bir kaynak. Oyuncuya ulaşan zincire bağlı olmadığı için dağıtıma alınmadı ve build guard ile yeniden eklenmesi engellendi.
- Daha önce çevrilmiş 16 tutorial görevine ek olarak kalan **25 çalışan tutorial dosyasında 90 oyuncu metni** çevrildi. Böylece bağlı tutorial görevi kapsamı **41/41** oldu.
- Görev ile envanter adı tutarlılığı için **19 hedef eşya/makine assetinde 41 alan** aynı sürüme bağlandı. v0.9 toplam ekleme: **131 yapılandırılmış alan / 44 hedef asset**.
- Kaynak `extractor4` Plant Fibre -> Tissue Culture, `extractor5` Meat -> Genetic Material anlatıyor; pinned extraction tariflerinde bu dönüşümler yok ve gerçek quest koşulu her ikisinde de 5 `fuscienceresource`. Türkçe görev metinleri gerçek koşul olan **5 Araştırma** üzerinden yazıldı.
- `create_silicon` teslim metni 10 Silicon derken gerçek `gatherItem` koşulu 1 `ff_silicon`. Türkçede **1 Silisyum** yazıldı.
- `create_woodencentrifuge` teslim metni yanlışlıkla Armorworks derken gerçek koşul `woodencentrifuge`. Türkçede **Ahşap Santrifüj** kullanıldı.
- `create_rockbreaker` içindeki bozuk `^;` kapanışı Türkçede `^reset;` ile düzeltildi.
- Kaynak hedef metninde adet yazmayan fakat quest koşulunda adet bulunan Yağ, Gümüş Külçesi, Araştırma ve Hidrojen hedeflerinde Türkçe hedef gerçek sayıyı açıkça gösterir.
- Rock Breaker -> **Kaya Parçalayıcı**, Rock Crusher -> **Kaya Kırıcı** ayrımı LOCKED; iki farklı makine aynı adla çevrilmeyecek.
- Tutorial hedefleri için Fener Çubuğu, Madencilik Lazeri, Metanol, Hidrojen, Silisyum, İlkel Mızrak, Elek, Ahşap Santrifüj, Kaya Parçalayıcı, Standart/Geliştirilmiş Mech Bacakları, Mech Tableti, Tech Tableti, Tamirci Anahtarı, Depolama Köprüsü ve Tech Konsolu adları envanterle eşlendi.
- Vanilla Kağıt, Gümüş Külçesi, Yağ ve Tech Konsolu adları bağımsız Starbound kaynak commitinden exact doğrulandı.
- Tutorial dışındaki bağlı FU görevlerinde 111 dosya hâlâ bekliyor.
- Oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca yapılmalıdır.

## 2026-09-20 - v0.10 Science görev envanteri ve Chemistry ilk geçiş

- `quests/fu_questlines/science` altında ham olarak **36 questtemplate** bulunuyor.
- `fuquest_dna` ve `fuquest_mineral` yalnızca kendi dosyalarında geçiyor; NPC, prerequisite zinciri veya `zb/questList/data.config` tarafından çağrılmıyor. İkisi de runtime-bağlantısız kabul edilerek dağıtım dışı bırakıldı ve build guard'a eklendi.
- Science klasöründeki erişilebilir görev sayısı bu nedenle **34**.
- Oyundaki `fu_sciences` quest-list'i **35 görev** başlatabiliyor. Bu liste Science klasörü dışındaki üç `deprecated` asseti hâlâ aktif kullanıyor: `fuquest_powerstation`, `fuquest_battery`, `fuquest_prototyper`.
- `create_blackglass` Science quest-list'inde görünmese de Bilim Karakolu NPC'si tarafından veriliyor ve `create_arcsmelter` zincirine bağlı; aktiftir.
- `fuquest_biochem` Science quest-list'inde değil, `fu_tutorial > fu_vinj` alt zincirinde `player.startQuest()` üzerinden erişilebilir; v0.9 klasör-tabanlı Tutorial kapsamının dışında kaldığı için v0.10 Chemistry geçişinde ayrıca ele alındı.
- Böylece oyuncuya ulaşabilen Science bağlantılı benzersiz görev havuzu **37 görev** olarak belirlendi: Science quest-list 35 + `create_blackglass` + `fuquest_biochem`.
- İlk Chemistry paketi: Science quest-list UI'sındaki 7 görünür alan + 8 erişilebilir Chemistry görevinin 31 metni + 8 hedef eşya/malzemenin 16 alanı = **54 yeni yapılandırılmış alan**.
- Caliche Stone -> **Kaliş Taşı**, Iodine -> **İyot**, Methyl Iodide -> **Metil İyodür**, Contaminated Water -> **Kirlenmiş Su**, Mulch -> **Malç**, Fertilizer -> **Gübre**, Bonemeal -> **Kemik Unu**, Ice Crystal -> **Buz Kristali** LOCKED.
- `create_plastic` kaynak metni güncel üretim zinciriyle uyuşmuyor: metin `Bio Lab` diyor, pinned FU 6.5.8 tarifleri `ff_plastic` üretimini `chemlab2` altında yapıyor. Türkçe yönlendirme gerçek makine adı olan **Kimya Laboratuvarı** üzerinden düzeltildi; Kemik Ununun santrifüjde Yağ verebildiği kaynak tarifle ayrıca doğrulandı.
- Buz Kristali vanilla Starbound kaynağı olduğu için `FerreiraJGB/Starbound @ 3b370d25c27923155badb38c414a664e1ee2abfc` üzerinden exact kaynak doğrulamasına bağlandı.
- Bu tur statik kaynak/terminoloji çalışmasıdır; oyun içi LQA ayrıca yapılacaktır.
