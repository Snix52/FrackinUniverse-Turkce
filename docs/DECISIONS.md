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

### v0.10 Electronics geçişi

- `fu_electronics` quest-listindeki **8/8 görev** yerelleştirildi; `fuquest_powerstation` ve `fuquest_battery` dosya olarak `deprecated` altında olsa da quest-list tarafından `player.startQuest()` ile hâlâ aktiftir.
- Electronics görevleri **30 görünür görev alanı** içeriyor. Yapay Zekâ Çipi, Silisyum Devre Kartı ve Gözcü hedef assetlerindeki 6 alanla paket toplamı **36 yeni yapılandırılmış alan / 11 yeni patch asset** oldu.
- AI Chip / A.I. Chip -> **Yapay Zekâ Çipi**, Silicon Board -> **Silisyum Devre Kartı**, Watcher -> **Gözcü** LOCKED.
- `create_circuitboard` kaynak metni güncel tarifle uyuşmuyor: eski metin Silisyum + Bakır Kabloyu Madde Birleştiricide birleştirmeyi söylüyor. Vanilla pinned tarif `siliconboard` için `craftingfurnace3` grubunu, yani **Atomik Fırını**, ve Kum + Kömür girdilerini kullanıyor. FU Madde Birleştirici yalnız `prototyper1/2/3` filtrelerini gösteriyor. Türkçe görev gerçek üretim zincirine göre düzeltildi.
- `fuquest_battery` kaynak metni eski **Wiring Tool** adını kullanıyor. FU'daki ilgili araç `wiretoolfu` ve gerçek kısa adı **Mechanic's Wrench**; projede **Tamirci Anahtarı** olarak zaten LOCKED/çevrilmiş olduğundan görev buna eşlendi.
- `create_centrifuge` tamamlanma metnindeki generic `advanced centrifuge`, gerçek sonraki envanter adı olan **Gaz Santrifüjü** ile açıklaştırıldı.
- Silisyum Devre Kartı vanilla asset olduğu için `FerreiraJGB/Starbound @ 3b370d25c27923155badb38c414a664e1ee2abfc` üzerinden exact doğrulandı.
- Electronics yeni alanları pinned/vanilla kaynakta **36/36 PASS**; renk, kontrol kodu ve sayı bütünlüğü **PASS**; üretilen patchlerde **36 test + 36 replace PASS**.

### v0.10 Genetics geçişi

- `fu_genetics` quest-listindeki **9/9 görev** yerelleştirildi.
- Genetics görevleri **32 görünür görev alanı**; doğrudan hedef 9 assette **19 görünür alan** olmak üzere toplam **51 yeni yapılandırılmış alan / 18 yeni patch asset** içeriyor.
- Mucize Otu Tohumu, Bracken Ağacı Tohumu, Mutavisk Tohumu, Oonforta Tohumu, Klonlama Laboratuvarı, Ignus Biberi Tohumu, Mutavisk Miğferi, Radyasyon Yaprağı ve Thornitox Tohumu LOCKED.
- Pinned tarifler `designlab1 = Sera`, `designlab2 = Botanik Laboratuvarı`, `designlab3 = Gen Tasarım Laboratuvarı` kademeleriyle çaprazlandı. Kaynak görevlerdeki eski/yanlış istasyon yönlendirmeleri buna göre düzeltildi.
- `create_miraclegrass`: kaynak gereksiz yere Gen Tasarım Laboratuvarı isterken gerçek tarif `designlab1`; Türkçe görev **Sera** üzerinden düzeltildi.
- `fuquest_bracken` ve `fuquest_oonforta`: kaynak Sera ile üretim yapılabileceğini ima ediyor, ancak gerçek tarifler `designlab2`; Türkçe görevler **Botanik Laboratuvarı** gereksinimini açıkça söylüyor.
- `fuquest_mutavisk` ve `create_ignuschili`: belirsiz/gereksiz yüksek laboratuvar yönlendirmeleri gerçek `designlab2` tarifine göre **Botanik Laboratuvarı** olarak açıklaştırıldı.
- Kaynak metinde adet yazmayan ancak quest koşulu 3 olan Bracken, Mutavisk, Oonforta, Ignus Biberi ve Radyasyon Yaprağı hedeflerinde gerçek adet oyuncuya açıkça gösterildi.
- `fuquest_cloning` kaynak metni hedefi açık söylemek yerine cihaz kullanımını iki kez tekrar ediyor; Türkçe başlangıç metni doğrudan **Klonlama Laboratuvarı üret** hedefini anlatacak şekilde düzenlendi.
- Genetics yeni alanları **51/51 kaynak PASS**, renk/kontrol/sayı QA **PASS**, patch pairing **51 test + 51 replace PASS**.

### v0.10 Mechanical geçişi

- `fu_mechanical` quest-listindeki 7 görev + Bilim Karakolu NPC'sinin verdiği `create_blackglass` olmak üzere **8/8 erişilebilir Mechanical görevi** yerelleştirildi.
- Mechanical görevleri **31 görünür görev alanı**; Elektromıknatıs, Asit Kalkanı ve Siyah Cam hedeflerinde **10 görünür alan** olmak üzere toplam **41 yeni yapılandırılmış alan / 11 yeni patch asset** içeriyor.
- Acid Shield -> **Asit Kalkanı**, Black Glass -> **Siyah Cam** LOCKED; Elektromıknatıs mevcut LOCKED kararına göre envanterde de çevrildi.
- `create_atmosregulator` teslim metnindeki eski `Atmosphere Regulator`, gerçek eşya adı `Atmospheric Regulator` ile eşlenerek **Atmosfer Düzenleyici** kullanıldı.
- `create_blackglass` başlangıç metni gerçek quest koşulundaki hedefi açık söylemiyordu; Türkçede Yüksek Fırında Obsidiyen eritip **Siyah Cam** elde etme hedefi açıklaştırıldı.
- Siyah Cam vanilla Starbound itemi olduğu için `FerreiraJGB/Starbound @ 3b370d25c27923155badb38c414a664e1ee2abfc` üzerinden exact doğrulandı; ırk inceleme metinleri de aynı assette yerelleştirildi.
- Mechanical yeni alanları **41/41 kaynak PASS**, renk/kontrol/sayı QA **PASS**, patch pairing **41 test + 41 replace PASS**.

### v0.10 Physics geçişi

- `fu_physics` quest-listindeki **4/4 görev** yerelleştirildi.
- Physics görevleri **16 görünür görev alanı**; Protocite Külçesi, Trityum Çubuğu ve Işınlayıcı Çekirdeği hedeflerinde **6 görünür alan** olmak üzere toplam **22 yeni yapılandırılmış alan / 7 yeni patch asset** içeriyor.
- Industrial Furnace -> **Endüstriyel Fırın**, Protocite Bar -> **Protocite Külçesi**, Tritium Rod -> **Trityum Çubuğu** LOCKED; Işınlayıcı Çekirdeği mevcut LOCKED kararına göre vanilla envanter assetinde de çevrildi.
- `create_protocite` kaynak metnindeki **Fission Furnace** güncel değildir. Pinned `protocitebar` tarifi `craftingfurnace2` grubundadır; vanilla gerçek kademe adı **Industrial Furnace / Endüstriyel Fırın** olduğundan Türkçe görev gerçek üretim zincirine göre düzeltildi.
- `create_tritium` kaynak metni Fisyon Reaktörü üretmeyi söylese de gerçek quest koşulu yalnız 1 `tritium` ister. Pinned Tritium tarifi `craftingfurnace3`, yani **Atomik Fırın** grubundadır. Türkçe görev gerçek hedefe göre düzeltildi.
- Kaynak teslim metinlerinde adet yazmayan Protocite ve Trityum hedeflerinde gerçek quest koşulları olan **2** ve **1** açıkça gösterildi.
- Işınlayıcı Çekirdeği vanilla Starbound itemi olduğu için `FerreiraJGB/Starbound @ 3b370d25c27923155badb38c414a664e1ee2abfc` üzerinden exact doğrulandı.
- Physics yeni alanları **22/22 kaynak PASS**, renk/kontrol/sayı QA **PASS**, patch pairing **22 test + 22 replace PASS**.

## 2026-09-20 - v0.11 Outpost / İçki zinciri

- Outpost içindeki Starbooze görev ailesi tek zincir olarak ele alındı: 12/12 görev dosyası birlikte yerelleştirildi.
- `Mash` ailesi için **Mayşe**, `Wort` için **Şıra**, `Hops` için **Şerbetçiotu**, `Mashing Tun` için **Mayşeleme Kazanı**, `Fermenter` için **Fermentör** ve `Distillery / Still` için **Damıtıcı** kilitlendi.
- `2brew_a` kaynak metni üç, sonra dört şişe isterken gerçek `gatherItem` koşulu 1 `bottle` istiyor. Türkçe görev metni gerçek koşula göre 1 Şişe ister.
- `3hops` kaynak metni en az 2 Hops derken gerçek koşul 1 `hops` istiyor. Türkçe metinde yanlış adet verilmedi; görev koşuluyla çelişmeyecek şekilde “yetiştirip topla” denildi.
- `2brew_c` görevi 1 Grape Mash ile tamamlanıyor ancak bir sonraki Wart Wine tarifi 2 Grape Mash istiyor. Türkçe metin bu farkı açıkça anlatır.
- `6beer` kaynak metni 3 Beer üret derken gerçek görev koşulu 1 `beer` istiyor; tarif tek üretimde 2 verir. Türkçe görev gerçek koşula göre yazıldı ve envanter adı **Buğday Birası** ile eşleştirildi.
- İçki görevlerinde geçen FU makineleri ve ana ara ürünlerin envanter adları aynı pakette çevrildi; görev zinciri İngilizce eşya adını bilmeyi gerektirmeyecek şekilde bağlandı.
- Oyun içi LQA, görev akışı ve crafting panel taşma testi hâlâ ayrı aşamadır.


## 2026-09-20 - v0.12 Outpost Arıcılık

- `quests/fu_questlines/outpost/bees` altında **14 ham görev dosyası** bulunuyor.
- Runtime bağlantıları Arıcı NPC + `fu_bees` quest-list + follow-up zinciri üzerinden çaprazlandı. Oyuncuya erişilebilir benzersiz Arıcılık görevi **13/13**.
- `13mites` yalnız kendi dosyasında prerequisite olarak `12breeding` yazmasına rağmen hiçbir NPC, quest-list veya follow-up tarafından başlatılmıyor. Bu nedenle bağlantısız legacy kabul edildi; dağıtım dışı bırakıldı ve build guard'a eklendi.
- Arıcılık görevlerinde **39 görünür görev alanı**, bağlı/yönlendirilen **18 hedef assette 39 alan** olmak üzere v0.12 toplamı **78 yeni yapılandırılmış alan / 31 yeni patch asset**.
- Apiary -> **Arılık**, Large Apiary -> **Büyük Arılık**, Queen -> **Ana Arı**, Drone -> **Erkek Arı**, Honeycomb -> **Bal Peteği**, Beeswax -> **Balmumu**, Honey Jarring Machine -> **Bal Kavanozlama Makinesi** ve ilgili arı/çerçeve adları LOCKED.
- `12breeding` kaynak metnindeki **Giant Apiary** gerçek bir item/object adı değil. Görev zincirinde kullanılan `normalalveary` nesnesinin gerçek kısa adı **Large Apiary** olduğundan Türkçede **Büyük Arılık** kullanıldı.
- Vanilla Böcek Ağı, Kırmızı Çiçek ve Boş Şişe ad/açıklamaları `FerreiraJGB/Starbound @ 3b370d25c27923155badb38c414a664e1ee2abfc` üzerinden exact doğrulandı.
- Yeni alan kaynak/provenansı: **72/72 pinned FU + 6/6 vanilla = 78/78 PASS**. Patch pairing: **78 test + 78 replace PASS**.
- v0.11 Outpost İçki kapsamı aynen korunarak proje toplamı **1881 yapılandırılmış alan + 15 Lua = 1896 yerelleştirilmiş görünür birim**; toplam patch asset **304** oldu.
- Oyun içi Arıcılık görev akışı, eşya adları, font ve panel taşma LQA'sı ayrıca yapılmalıdır.
## 2026-09-20 - v0.13 Outpost Bilim Karakolu dükkânları

- Altı `scienceoutpost_*Shop` görevi ilgili dükkân nesnelerinin `offeredQuests` / `turnInQuests` alanlarıyla runtime'da doğrudan doğrulandı; quest-listte görünmemeleri bağlantısız oldukları anlamına gelmiyor.
- Görev hedefi olan altı artefaktın envanter adları aynı pakette kilitlendi: **Greenfinger Madalyası, Uğurlu Para, Kristal Kupa, Uzaylı Yayın Düğümü, X'i Kalıntısı, Kadim Kumanda**.
- `Verdant Ruins`, `Ancient Temple` ve `Evernight Jungle` şu aşamada özel görev/konum adları olarak korunur. Bu adlar, ilgili görev/mission/harita zinciri bütünüyle yerelleştirilmeden tek bir Outpost metninde Türkçeleştirilmez.
- `Shards` Eld'uukhar söyleminde büyük harfle kullanılan lore özel adı olarak geçici biçimde özgün bırakılır; Eld'uukhar lore paketi ele alındığında yeniden değerlendirilecek.
- Turn-in metinlerinde kaynakta geçen generic dükkân tarifleri doğal Türkçeyle aktarıldı; hedef artefakt adları envanterle birebir eşleştirildi.
- Oyun içi LQA, görev işaretçisi ve dükkân etkileşim testi ayrıca yapılacaktır.

## 2026-09-20 - v0.13.1 geriye dönük Türkçe QA

- v0.1-v0.13 arasındaki **1929 yapılandırılmış alan + 15 Lua UI metni** yeniden tarandı.
- Altı eski tutorial teslim metnindeki bozuk **"Bilim Karakolundaki bana getir"** kalıbı **"Bilim Karakolunda bana getir"** olarak düzeltildi.
- v0.13 dükkân teslim metinleri iki ayrı hedef varmış gibi okunan yapıdan çıkarılarak **"Bilim Karakolundaki X Dükkânına götür"** biçiminde netleştirildi.
- Arıcılıkta eski **kraliçe arı** kullanımı, kilitli gerçek arıcılık terimi **Ana Arı** ile eşlendi.
- Arı Barınağı tariflerinin arıyı tüketip para verdiği kaynak tariflerden doğrulandı; oyuncu eylemi satın alma değil satış olduğundan UI düğmesi **Satın Al -> Sat** düzeltildi.
- Penumbrite açıklamasındaki **keskinlığını -> keskinliğini** yazım hatası ve cümlenin yapay devamı düzeltildi.
- Glitch ton etiketlerinde **Interested -> Meraklı**, **Inspired -> İlhamlanmış** kullanıldı; "İlgili" ve "İlhamlı" anlam/akıcılık hataları temizlendi.
- monocled görev tariflerinde yapay **monokllü** yerine **monokl takan** kullanıldı; Human Scientist ifadesi doğal **insan bilimci** yapısına çekildi.
- v0.13 Kirhos/Radien/Shadow metinlerindeki yapay Türkçe ifadeler ve **Kristal Kusursuzluk** başlığı doğal Türkçeyle düzeltildi.
- **Homestead -> Yerleşim** kararı, I-V zinciri tamamlandığı için REVIEW'dan LOCKED durumuna geçirildi.
- Alan/pointer sayısı değişmedi. Bu tur kaynak anlamı veya teknik ID değiştirmeyen dil/terminoloji düzeltmesidir.
- Oyun içi LQA, font ve panel taşma kontrolleri ayrıca bekliyor.

## 2026-09-20 - v0.13.2 ikinci geriye dönük QA

- Terminoloji sözlüğünde **Mech** LOCKED olmasına rağmen eski içeriklerde 16 oyuncu metninde küçük harf `mech` kalmıştı. Tamamı **Mech** biçimine getirildi ve lowercase regresyon guard eklendi.
- Arı Barınağı yeniden kaynak tarifleriyle denetlendi. Panelde arı -> para/malzeme dönüşümleri yanında `money -> bees1-codex / bees2-codex` rehber tarifleri de bulunuyor.
- Bu nedenle v0.13.1'deki tek yönlü **Sat** etiketi de eksik kabul edildi. Her iki kullanım biçimini doğru kapsayan kısa UI eylemi **Takas Et** olarak kilitlendi.
- 15 Lua UI metni yeniden gözden geçirildi; değişiklik gerektirmedi.
- Teknik alan/pointer/provenans değişmedi; tur yalnız Türkçe hedef metin ve regresyon güvenliği düzeltmesidir.
- Oyun içi LQA, font ve panel taşma kontrolleri ayrıca bekliyor.

## 2026-09-20 - v0.13.3 üçüncü geriye dönük QA

- `Replace Me` değeri crafting listelerindeki runtime `listTemplate` dummy etiketidir; gerçek eşya adı çalışma anında bu alanın yerine yazılır. Oyuncuya ait içerik olmadığı için Arı Barınağı, Gemi Bileşeni Birleştirici ve Psiyonik Tezgâhı kataloglarından **3 alan çıkarıldı** ve yeniden eklenmesini engelleyen build guard eklendi.
- Oyuncuya dönük metindeki **vanilla** ifadesi **ana oyun** olarak yerelleştirildi. İngilizce bilmeden anlam takibi ilkesi gereği meta terim LOCKED.
- Generic **eldritch** sıfatı mevcut Tarım kullanımındaki **tekinsiz** ile birleştirildi; iki İngilizce sızıntı temizlendi.
- Sifter tutorialında `silt` İngilizce kalmış, `Gravel` ise görevde **Çakıl** olmasına rağmen envanterde İngilizceydi. Vanilla envanter adları bağımsız Starbound kaynağından doğrulandı ve **Loose Silt -> Gevşek Mil**, **Gravel -> Çakıl** olarak eşlendi.
- **Silt -> Mil** kararı Türkçe jeoloji/zemin terminolojisindeki yerleşik kullanıma göre alındı. Görev metni envanter adıyla birebir takip edilebilmesi için **Gevşek Mil** kullanır.
- `sand.matitem` final açıklaması FU'nun `items/materials/sand.matitem.patch` katmanından; kısa adı vanilla `sand.matitem` tabanından exact doğrulandı. `gravel.matitem` açıklama ve kısa adı vanilla kaynaktan exact doğrulandı.
- Eski `create_alchemy`, `create_electronics`, `create_greenhouse`, `create_tinkertable` teslim metinlerinde daha önce doğru yapılmış kaynak/ID düzeltmelerine eksik QA provenans notları eklendi.
- Oyun içi LQA, font ve panel taşma kontrolleri ayrıca bekliyor.
- Tutorial `create_woodencentrifuge` tamamlanma metni gerçek bir sonraki yükseltme olan `ironcentrifuge` nesnesini **Iron Centrifuge** adıyla yönlendiriyor. Eski Türkçe yalnız **Santrifüj** diyerek envanter adını kaybediyordu; **Iron Centrifuge -> Demir Santrifüj** LOCKED edildi ve nesnenin görünür envanter alanları aynı pakette çevrildi.

## 2026-09-20 - v0.14 Outpost Kevin ve Khe

- Kevin'in fuoutposthylotlscientist üzerinden açılan **9/9** görevi ve Khe'nin teslim NPC'si/eşya pickup zincirleriyle açılan **4/4** görevi runtime'da doğrulandı.
- Kaynak Sewing Wheel yönlendirmesi, boosterchest üretiminin gerçek 2. kademe istasyonu **Sewing Machine / Dikiş Makinesi** ile eşlendi.
- create_clothingfabricator3e teslim metnindeki generic average quality Brains, gerçek brain kısa adı **Superior Brain / Üstün Beyin** ile düzeltildi.
- Nötronyum hedefleri generic madde adları yerine gerçek envanter adları **Nötronyum Çubuğu** ve **Anti-Nötronyum Çubuğu** olarak kullanıldı.
- Khe kumaş görevinin genel malzeme adları gerçek koşullarla eşlenerek **Altın Külçe, Elmas, Kristal, Çekirdek Parçası, Saf Erchius Kristali** biçiminde açıklaştırıldı.
- Kevin/Khe görevlerinin doğrudan andığı FU ve vanilla hedeflerin görünen envanter alanları aynı pakette çevrildi; İngilizce eşya adını bilme zorunluluğu kaldırıldı.
- Yeni kapsam: **94 structured alan / 33 yeni patch asset**; kaynak/provenans **94/94 PASS** (84 pinned FU + 10 vanilla). Proje toplamı **2028 structured + 15 Lua / 358 patch asset**.
- Oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.15 Battle görevleri

- Battle klasöründeki 13 ham görev, `zb/questList/data.config`, NPC `offeredQuests` / `turnInQuests` alanları ve takip referanslarıyla denetlendi.
- `fu_gear` 6/6 ve `fu_monsters` 4/4 olmak üzere **10 erişilebilir görev** dağıtıma alındı.
- `fuquest_gorgolith`, `fuquest_gorillaking` ve `fuquest_titan` hiçbir quest-list, NPC veya follow-up tarafından başlatılmıyor. Tüccar havuzundaki `prerequisiteQuest` kullanımları görev başlatmadığı için bu üç dosya bağlantısız legacy kabul edildi ve build guard'a eklendi.
- **Battle -> Savaş**, **Gear -> Ekipman**, **Monsters and Villains -> Canavarlar ve Düşmanlar**, **[BOSS] -> [PATRON]** olarak kilitlendi.
- Görev hedefleri gerçek kısa adlarla eşlendi: **Sıradan Şapka, Kol Topu, F4 Enerji Tüfeği, Lazer Tabancası, Çelik Savaş Kılıcı, Ferozium Satırı, Yadigâr Kalkanı, Anne Poptop Pençesi, Ağ Atıcı, Hiper Hedefleme Çipi**.
- Mama Poptop görevinin generic **Poptop Claw** teslim metni, gerçek envanter adı **Mama Poptop Claw / Anne Poptop Pençesi** ile düzeltildi.
- `plebiancap.questtemplate` kaynak metnindeki literal sekme standart JSON'a aykırı olduğundan üç görünür alan exact ham-kaynak guard ile doğrulanır.
- Yeni kapsam: **64 structured alan / 20 yeni patch asset**; kaynak/provenans **64/64 pinned FU PASS**. Proje toplamı **2092 structured + 15 Lua / 378 patch asset**.
- Oyun içi görev akışı, font ve panel taşma kontrolleri ayrıca bekliyor.

## 2026-09-20 - v0.16 Kalan görev klasörleri

- Other, BYOS ve Exploration altındaki kalan 17 ham görev dosyası runtime referansları üzerinden tek tek denetlendi.
- Other'da 8, BYOS'ta 2 erişilebilir görev yerelleştirildi. Kaynakta oyuncuya görünmemesi açıkça belirtilen 5 sinematik takipçi dağıtım dışı tutuldu.
- fu_byosshipcraftingtable ve fuquest_explore1 için görev-listesi, NPC, pickup, prerequisite veya follow-up tetikleyicisi bulunamadı; bağlantısız legacy olarak build guard'a alındı.
- Görevde geçen hedef adları gerçek envanter adlarıyla eşlendi. Densinium Helm -> **Densinium Miğferi**, Cthulhu Statue -> **Cthulhu Heykeli**, Shoggoth Flesh -> **Shoggoth Eti**, Tattered Grimoire -> **Yıpranmış Büyü Kitabı**, Precursor Data-Key -> **Precursor Veri Anahtarı**, Crew Deed -> **Mürettebat Tapusu** LOCKED.
- Vanilla Molten Core -> **Erimiş Çekirdek** adı bağımsız pinned vanilla kaynak üzerinden doğrulandı.
- create_densinium kaynak metnindeki hatalı kapanış ^orange; Türkçe yamada ^reset; olarak düzeltildi.
- Precursor görevinin genel data-disc yönlendirmesi gerçek hedef envanter adı **Precursor Veri Anahtarı** ile açıklaştırıldı.
- Battle kapsamındaki tekil Cyber Sphere kullanımı, mevcut kilitli çoğul **Siberküreler** terimiyle uyumlu **Siberküre** olarak düzeltildi.
- Yeni kapsam 62 yapılandırılmış alan / 21 yeni patch assettir; 60 pinned FU ve 2 vanilla alanın tamamı exact-source/provenans kontrolünden geçti.

## 2026-09-20 - v0.17 Üretim makineleri

- `objects/crafting` ağacındaki 84 .object asseti envanterlendi; 30'u önceki sürümlerde kapsanmıştı, kalan 54 etkin asset bu sürümde yerelleştirildi.
- Yeni kapsam **295 yapılandırılmış oyuncu alanı / 54 yeni patch asset**tir. Ad, açıklama, alt başlık, panel başlığı ve mevcut ırka özel inceleme metinleri birlikte ele alındı.
- Armorworks -> **Zırh Atölyesi**, Assembly Line -> **Montaj Hattı**, Armory -> **Cephanelik**, Fuel Refinery -> **Yakıt Rafinerisi**, Fission Furnace -> **Fisyon Fırını**, Gene Sequencer -> **Gen Dizileyici**, Nanofabricator -> **Nanoüretici**, Cosmic Crucible -> **Kozmik Pota** LOCKED.
- Racialiser/Racializer aynı oyuncu kavramı olarak **Irk Dönüştürücü** biçiminde tekilleştirildi; Precursor ve X'ian özel adları çevrilmeden korundu, Mech büyük harf kilidi sürdürüldü.
- `objects/crafting/pethealingstation/pethealingstationauto.object` kaynağındaki **For broken robots** altyazısı nesnenin adı ve açıklamasıyla çeliştiği için **Yaralı evcil hayvanlar için** olarak düzeltildi ve regresyon guard'ına bağlandı.
- Yeni alanların **295/295'i pinned FU 6.5.8 kaynağıyla exact doğrulandı**; proje toplamı 2449 structured + 15 Lua / 453 patch asset oldu.
- Bu sonuç FU'nun bütün eşya ve nesne klasörlerinin tamamlandığı anlamına gelmez; oyun içi LQA ve diğer klasörlerin kapsam taraması sürer.

## 2026-09-20 - v0.18 İşlevsel Power, Bees ve Science Outpost nesneleri

- Daha önce çevrilmemiş 57 aday `.object` dosyası yalnız klasör varlığına göre değil; tarif, araştırma, dükkân, görev ve Tiled dungeon yerleşimleri üzerinden runtime'da denetlendi.
- Erişilebilir kapsam **47 asset / 340 görünür alan** olarak belirlendi: Power 15 asset/59 alan, Bees 17 asset/142 alan, Science Outpost 15 asset/139 alan.
- Aşağıdaki 10 asset için gerçek kullanım bağlantısı bulunmadı ve dağıtıma alınmadı: `fu_solararrayscienceoutpost`, `fu_upgrade`, `makeshiftreactor2`, `scentedalveary`, `scentedapiary`, `deeponegame`, `moonlitcomet2`, `scienceoutpostbanner2`, `scienceoutpostbanner3`, `scienceoutpostbanner4`.
- `fu_upgrade` yalnız kullanılmayan bir tileset tanımı ve kaynakta açıkça kırık/geliştirme artığı olduğunu belirten metinler içerir. `scentedalveary` yalnız yorum satırındaki blueprint kaydında, `scentedapiary` ile bazı bannerlar ise kullanılmayan tileset tanımlarında geçer. Bu tür tanımlar erişilebilirlik kanıtı sayılmadı.
- Standart ad/açıklama/ırk incelemesi alanlarına ek olarak `fu_rechargesensor` ve `fu_weatherbeacon` runtime etiketleri ile Vinalisj, Danışma Noktası ve Starbucks `chatOptions` havuzları oyuncuya görünür kabul edildi.
- Kaynaktaki boş `gnomefactory/subtitle` teknik olarak görünür bir değer üretmediği için yamaya eklenmedi. Özel ürün/kişi adları Burger Fool, SuperPet, Vinalisj, Infinity Express ve Starbucks korunurken açıklamaları Türkçeleştirildi.
- Power Relay -> **Güç Rölesi**, Field Generator -> **Alan Jeneratörü**, Nocturn Array -> **Gece Dizisi**, Weather Beacon -> **Hava İstasyonu**, Gnome Workshop -> **Gnom Atölyesi**, Honey Extractor -> **Bal Özütleyici**, Info Booth -> **Danışma Noktası** olarak kilitlendi.
- Derleyiciye `%s`, `%%` ve diğer printf biçim belirteçlerinin birebir korunması için yeni kontrol eklendi. Starbound'un alıntılı metin içindeki ham satır sonlarını kabul eden assetleri `strict=False` ile parse edilerek artık full-source simülasyona giriyor.
- Geriye dönük full-source taramasında FU'nun `orange.consumable` açıklamasının vanilla tabandan farklı olduğu saptandı. Kaynak kilidi gerçek FU değeri olan `It's an orange. ^green;Type: Plant^reset;` ile düzeltildi; iki alan pinned FU provenansına taşındı.
- Yeni alanların **340/340'ı pinned FU 6.5.8 kaynağıyla exact doğrulandı**. Proje toplamı **2789 structured + 15 Lua / 500 patch asset**; provenans **2701 pinned FU + 88 layered/external**, izlenmeyen alan **0**.
- Oyun içi font, panel taşması, etkileşim ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.19 Üretim malzemeleri

- `items/generic/crafting` altında 290 `.item` ve 23 `.consumable`, toplam **313 asset** envanterlendi. Önceden kapsanan 52 asset çıkarılınca kalan **261 aday** runtime bağlantılarıyla denetlendi.
- Tarif girdisi/çıktısı, araştırma açılımı, görev ödülü, çıkarma veya işleme tablosu, ganimet havuzu ve etkin tür blueprint zinciri erişilebilirlik kanıtı sayıldı. Yalnız dosyanın var olması, yorum satırı, `.disabled` tarif veya üretim tarifi olmayan blueprint kaydı yeterli sayılmadı.
- **235 erişilebilir assette** yalnız `/shortdescription` ve `/description` alanları yerelleştirildi. `itemName`, kategori, fiyat, efekt, tooltip türü, script, tarif ve diğer teknik alanlar değiştirilmedi.
- **19 assetin** kendi tanımı dışında hiçbir exact item-ID referansı bulunmadı. **7 ek asset** yalnız yorum satırı, `.disabled` tarif, deprecated geri-kazanım girdisi, ürün kaynağı olmayan kargo kabul listesi veya karşılığı bulunmayan tür blueprint kaydında geçti. Toplam **26 asset** dağıtım dışı bırakılıp build deny-guard'a alındı.
- Deprecated `kheWarpedAIChip`, yalnız eski kayıtların kaynaklarını geri kazanmasına yarayan çıkarma girdisi olarak korunur; yeni oyun akışında üretilemediği ve kendi açıklaması da açıkça deprecated dediği için yerelleştirme kapsamına alınmadı.
- `fufleshalien`, aynı otopsi/embalming tablosunda hem `cadaveralien` çıktısı hem de işlenebilir girdi olduğundan erişilebilir kabul edildi. `sciencebrochure`, etkin `fu_start_MA` görevinin ödülü olduğundan kapsama alındı.
- İzotoplar için yerleşik Türkçe element adları kullanıldı: **Döteryum, Neptünyum, Plütonyum, Toryum, Uranyum**. `Precursor`, `X'ian`, `Aether`, `Lunari` ve FU malzeme özel adları korunurken işlevsel son ekler Türkçeleştirildi.
- Yeni kapsam **470 yapılandırılmış alan / 235 patch asset**tir. Tamamı pinned FU 6.5.8 kaynak değerleri ve blob SHA'larıyla doğrulandı; 470 `test` + 470 `replace` eşleşmesi PASS.
- Proje toplamı **3259 structured + 15 Lua / 735 patch asset** oldu. Oyun içi envanter, tooltip, font, satır sonu ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.20 Aktif özel görevler

- Daha önce çevrilmemiş **97 `.questtemplate` adayı** ile yanlış `.questtemplat` uzantılı 1 test dosyası runtime açısından denetlendi.
- Erişilebilir kapsam **29 görev / 112 görünür alan** olarak belirlendi: 19 harita ve özel bölge görevi, 4 Challenge Labs görevi, 2 Usta Manipülatör görevi ve eşya/artefakt kazanımıyla gerçekten başlayan 4 Tech görevi.
- 49 teknoloji görevinden yalnız `combatmaneuvering1`, `fudistortionsphere`, `microsphereprecursor` ve `longjump0` gerçek pickup/artefakt zincirine bağlıdır. 44 eski teknoloji görevi ile yalnız geliştirici gemisindeki `fudevtech` normal oyuncu kapsamına alınmadı.
- Optional Hardmode'un 12 görevlik zinciri kaynakta bulunuyor ancak başlangıç görevi Khe'nin `offeredQuests` listesinde açıkça yorum satırına alınmış. Zincir normal oyunda başlayamadığı için tamamı dağıtım dışı ve deny-guard altındadır.
- `mmgravgun`, `mmgravgun2` ve `mmgravgun3` görev şablonlarını başlatan bir tetikleyici bulunmadı. Buna karşılık `mastermanipulator2` Khe tarafından sunuluyor; ödül olarak verilen `humanartifactaugment` da `mastermanipulator` görevini başlatıyor.
- `fu_asraNoxSailFix`, `madnessquestdata` ve `fuelDataQuest` runtime'da çalışan fakat bütün görev pencereleri kapalı uyumluluk/takip görevleridir. Oyuncuya görünür metin üretmedikleri için yamaya alınmadı. `ancientpowerconduit` ise aynı adlı eşya ve radyo mesajına sahip olsa da görevi başlatan bir bağlantı taşımıyor.
- Challenge Labs teslim kristalleri gerçek dungeon Tiled katmanlarında ayrı ayrı yerleştirilmiş olduğundan 4 görev de erişilebilir kabul edildi. 19 harita/özel bölge görevi SAIL, görev haritası, teslim nesnesi veya gerçek Tiled yerleşimiyle doğrulandı.
- `Brine Star`, `Ancient Temple`, `Hydro Center`, `Evernight Jungle`, `Forest of Fae`, `Grand Arena`, `Mount Gigant`, `Castle Takeshi`, `Techno City`, `Sky Boulevard`, `Snow Crash`, `Sunset Riders`, `Tower Invincible` ve `Verdant Ruins` SAIL/harita zinciriyle eşleşen özel görev adları olarak özgün bırakıldı.
- `combatmaneuvering1` tamamlanma metnindeki köşeli parantezler oyuncuya gösterilen açıklama cümlesidir; kontrol etiketi değildir. Yalnız bu alan için field-specific `allow_control_fix` kullanıldı, renk kodları ve parantez düzeni korundu.
- Yeni kapsamın **112/112 alanı** pinned FU 6.5.8 kaynağıyla exact doğrulandı; patch pairing **112 test + 112 replace PASS**. Proje toplamı **3371 structured + 15 Lua / 764 patch asset** oldu. Oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.21 Erken oyun silahları

- `items/active/weapons` altında **1201 `.activeitem`** bulundu. Bütün klasörü kör biçimde çevirmek yerine oyuncunun erken oyunda aktif Zırh ve Silahlar araştırma ağacından açtığı `bonegear`, `irongear`, `telebriumgear` ve `tungstengear` düğümleri seçildi.
- Dört düğüm toplam **124 gerçek silah asseti** açıyor. Bu silahların **124/124'ü** etkin `.recipe` çıktısıyla doğrulandı; yalnız dosya varlığı erişilebilirlik kanıtı sayılmadı.
- Daha önce görev/makine zincirleri kapsamında çevrilmiş `hardenedsteelblade`, `laspistol` ve `armcannon` korundu. Kalan **121 silahta** yalnız `/shortdescription` ve `/description` alanları yerelleştirildi; `itemName`, yetenek, hasar, kategori, script ve teknik parametrelere dokunulmadı.
- Silah türleri oyuncuya kısa ve ayırt edilebilir adlarla kilitlendi: Broadsword -> **Büyük Kılıç**, Quarterstaff -> **Dövüş Asası**, Rapier -> **Meç**, Staff -> **Asa**, Wand -> **Değnek**. `Stynger`, `Cestus`, `Protectorate`, `Telebrium`, `Bushmaster`, `Fellshot` ve `Hellion` özel/model adları korundu.
- Kaynaktaki mizahi veya yetişkin ton temizlenmedi; örneğin Telebrium Uzun Kılıç açıklamasındaki ima, Türkçede doğal fakat kaynakla aynı şiddette bırakıldı. Kaynakta olmayan küfür veya yeni şaka eklenmedi.
- Yeni kapsam **242 yapılandırılmış alan / 121 patch asset**tir. Tamamı pinned FU 6.5.8 kaynağı ve blob SHA'larıyla exact doğrulandı; patch pairing **242 test + 242 replace PASS**. Proje toplamı **3613 structured + 15 Lua / 885 patch asset** oldu. Oyun içi envanter adı, tooltip genişliği, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.22 Kademe 3 savaş ekipmanı ve tutarlılık düzeltmeleri

- Aktif Zırh ve Silahlar ağacındaki `titaniumgear`, `carbonarmorgear`, `wastelandgear`, `protocitegear`, `penumbritegear` ve `zerchesiumgear` düğümleri seçildi. Bu düğümlerin açtığı **158/158 savaş ekipmanı** etkin `.recipe` çıktısıyla doğrulandı.
- Daha önce Battle görevi kapsamında çevrilen `energyassault` korundu. Kalan **157 assette** yalnız `/shortdescription` ve `/description` yerelleştirildi; teknik `itemName`, hasar, yetenek, mermi, kategori ve script alanları değiştirilmedi.
- Araştırma düğümlerinin açtığı beş kalkan da üretilebilir savaş ekipmanı olduğundan aynı kapsamda tutuldu. Salt dosya varlığı veya yalnız araştırma listesi yeterli sayılmadı.
- `mastermanipulator2` görevi ödül olarak `humanartifactaugment` verir; bu augment `mastermanipulator` görevini başlatır ve Nanoüretici tarifiyle `fumastermanipulator` aracına dönüşür. Bu nedenle kırık augmentin 3 görünür alanı ile tamamlanmış aracın 2 görünür alanı birlikte **Usta Manipülatör** terminolojisine eşlendi.
- `combatmaneuvering1` içindeki iki “Tuhaf eser yanına yaklaştığında...” çevirisi özneyi belirsizleştirdiği için “Tuhaf eserin yanına yaklaştığında...” olarak düzeltildi. Kaynak değer, renk ve köşeli parantez QA istisnası değişmedi.
- Yeni kapsam **319 yapılandırılmış alan / 159 patch asset**tir. Tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı; patch pairing **319 test + 319 replace PASS**. Proje toplamı **3932 structured + 15 Lua / 1044 patch asset** oldu. Oyun içi envanter adı, tooltip genişliği, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.23 Kademe 4 çekirdek savaş ekipmanı

- Kademe 4'ün tamamına kör toplu çeviri yapılmadı. Aktif Zırh ve Silahlar ağacındaki çekirdek `advancealloygear` ve `durasteelgear` düğümleri seçildi; Irradium, Trianglium, Prisilite, Quietus ve biyosilah dalları ayrı sürümlere bırakıldı.
- İki düğümün açtığı **48/48 savaş ekipmanı**, gerçek ve etkin `.recipe` çıktısıyla doğrulandı. Salt research listesi, asset varlığı veya `/spawnitem` erişimi yeterli kanıt sayılmadı.
- 48 assette yalnız `/shortdescription` ve `/description` alanları çevrildi. Bir adet Matter Manipulator sınıfı `.beamaxe` de araştırma + tarif zinciriyle açıldığı için savaş ekipmanı kapsamındaki aynı görünür alan kuralıyla işlendi.
- `Gauss`, `Breach` ve `Stynger` aile/model adları korundu. `Railgun` -> **Raylı Tüfek**, `Sonic Cannon` -> **Sonik Top**, `Gravity Wand` -> **Yerçekimi Değneği**, `Orbital Strike` -> **Yörünge Saldırısı** olarak kilitlendi.
- Yeni kapsam **96 yapılandırılmış alan / 48 patch asset**tir. Tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı; patch pairing **96 test + 96 replace PASS**. Proje toplamı **4028 structured + 15 Lua / 1092 patch asset** oldu. Oyun içi envanter adı, tooltip genişliği, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.24 Kademe 4 kalan savaş ekipmanı

- Aktif Zırh ve Silahlar ağacındaki `irradiumgear`, `triangliumgear`, `prisilitegear`, `quietusgear` ve `bioweaponsgear` düğümleri seçildi. Beş düğümdeki 209 araştırma açılımından **148 benzersiz savaş ekipmanı**, gerçek ve etkin `.recipe` çıktısıyla doğrulandı.
- Düğümler arasında tekrar veya önceden kapsanmış asset bulunmadı. 148 assette yalnız `/shortdescription` ve `/description` yerelleştirildi; teknik `itemName`, hasar, yetenek, mermi, kategori, tarif ve script alanları değiştirilmedi.
- Irradium, Trianglium, Prisilite ve Quietus FU malzeme adları korundu. Prisilite silahlarındaki `Prismatic` sıfatı **Prizmatik**, Atropus biyosilah ailesindeki `Fleshweave` adı **Et Örgüsü**, `Plague Bearing` etkisi **Veba taşır** olarak kilitlendi.
- `Breach`, `Gishinanki`, `Justicar`, `Manstopper`, `Ocu`, `Quellhound` ve `Lasher` model/özel adları korundu. Silah sınıfları önceki kararlarla eşlendi: **Büyük Kılıç, Dövüş Asası, Meç, Makineli Tabanca, Taarruz Tüfeği, Roketatar**.
- Yeni kapsam **296 yapılandırılmış alan / 148 patch asset**tir. Tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı; patch pairing **296 test + 296 replace PASS**. Proje toplamı **4324 structured + 15 Lua / 1240 patch asset** oldu. Oyun içi envanter adı, tooltip genişliği, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.25 Kademe 1-2 aktif zırh setleri

- Aktif Zırh ve Silahlar ağacındaki `bonegear`, `slimegear1`, `irongear`, `cottongear`, `telebriumgear`, `lunarigear`, `elduugear`, `skathgear` ve `tungstengear` düğümleri seçildi. Bütün `items/armors` klasörünü kör çevirmek yerine araştırma açılımı ile gerçek `.recipe` çıktısı birlikte erişilebilirlik kanıtı sayıldı.
- Dokuz düğümde daha önce çevrilmemiş ve tarif destekli **114 zırh parçası** bulundu. Her assette yalnız `/shortdescription` ile `/description` alanı yerelleştirildi; `itemName`, stat hesapları, efektler, tooltip türü, tarif ve script alanları korunur.
- `epps1`-`epps4` düğümleri sırt ekipmanı/EPP sistemi olarak ayrı tutuldu. Bunlar zırh seti dilimine karıştırılmayacak ve kendi işlev zincirleriyle ayrıca denetlenecek.
- Zırh istatistiklerinde **Set Bonusları, Kritik Şansı, Kritik Hasarı, Geri Tepme Direnci, Kalkan Canı ve Yenilenmesi, İyileştirme Gücü, Can Çalma, Germe Hızı, Atış Başına Enerji** terminolojisi kilitlendi.
- `Oxygen` bağışıklık etiketi bu bağlamda element değil, oksijensiz ortam tehlikesidir; oyuncuya etkisini doğru anlatmak için **Oksijensizlik** kullanıldı. `Bio-Ooze`, `Slush`, `Chill` ve `Quicksand` sırasıyla **Biyo-Balçık, Sulu Kar, Üşüme** ve **Batak Kum** olarak kilitlendi.
- `Dracon` ve `Warscorned`, anlamı oyun içinde açıklanmayan Skath model adları olduğundan özel ad olarak korundu. İşlevsel parça adları ve tooltip metinleri Türkçeleştirildi.
- Yeni kapsam **228 yapılandırılmış alan / 114 patch asset**tir. Tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı; proje toplamı **4552 structured + 15 Lua / 1354 patch asset** oldu. Oyun içi zırh tooltip genişliği, set bonusu satırları, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.26 Kademe 3 aktif zırh setleri

- Aktif Zırh ve Silahlar ağacındaki `titaniumgear`, `carbonarmorgear`, `wastelandgear`, `protocitegear`, `penumbritegear` ve `zerchesiumgear` düğümleri seçildi. Araştırma açılımı ile gerçek `.recipe` çıktısı birlikte erişilebilirlik kanıtı sayıldı.
- Altı düğümde **76 üretilebilir zırh parçası** doğrulandı. Science kapsamında daha önce yerelleştirilmiş Mutavisk miğferi korundu; kalan **75 assette** yalnız `/shortdescription` ve `/description` alanları çevrildi.
- Kaynak klasör kademesi yerine runtime araştırma zinciri esas alındı. Bu nedenle dosya yolu `items/armors/tier4` altında bulunan ancak Kademe 3 araştırma düğümlerinden açılan üç Ödül Avcısı parçası kapsama dâhil edildi.
- Tooltip terimleri **Kalkan Yenilenmesi, Nefes Yenilenmesi, Proto-Zehir, Enerji Yenilenme Gecikmesi, Bomba Teknolojisi Hasarı, Savunma Teknolojisi Verimliliği** ve **Araştırma Bonusu** biçiminde kilitlendi.
- `Spacepunk`, `Neishin`, `Nightar` ve `Tenebrhae` özel/model adları korundu. `Battleborn` kısa set adı olarak **Savaşdoğan**, `Spacefarer` ise **Uzay Yolcusu** biçiminde yerelleştirildi.
- Yeni kapsam **150 yapılandırılmış alan / 75 patch asset**tir. Tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı; proje toplamı **4702 structured + 15 Lua / 1429 patch asset** oldu. Oyun içi zırh tooltip genişliği, set bonusu satırları, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.27 Kademe 4 aktif zırh setleri

- Aktif Zırh ve Silahlar ağacındaki `advancealloygear`, `durasteelgear`, `irradiumgear`, `triangliumgear`, `prisilitegear`, `quietusgear` ve `bioweaponsgear` düğümleri seçildi. Araştırma açılımı ile gerçek `.recipe` çıktısı birlikte erişilebilirlik kanıtı sayıldı.
- Yedi düğümde daha önce yerelleştirilmemiş **87 üretilebilir zırh asseti** doğrulandı. Her assette yalnız `/shortdescription` ve `/description` çevrildi; teknik `itemName`, stat hesapları, efekt listeleri, tooltip türü, tarif ve script alanları korundu.
- Kaynak klasör kademesi yerine runtime araştırma zinciri esas alındı. Bu nedenle dosya yolu `items/armors/tier5/cute` altında bulunan ancak Kademe 4 araştırma düğümlerinden açılan Sevimli seti kapsama dâhil edildi.
- Tooltip terimleri **Kalkan Dayanıklılığı, Kalkan Darbesi, Zihinsel Direnç, Parıltı, Yavaş Düşüş, Yerçekimi Normalleştirmesi, Açlık Tüketim Hızı, Buzda Kayma, Karda Yavaşlama, Gölge Lekesi** ve **Ateş Novası** biçiminde kilitlendi.
- `Maverick`, `Intersec` ve `Primus` model/özel adları korundu. `Cellular`, `Pustule`, `Star-Killer` ve `Graphene` sırasıyla **Hücresel, Püstül, Yıldız Katili** ve **Grafen** olarak yerelleştirildi.
- Yeni kapsam **174 yapılandırılmış alan / 87 patch asset**tir. Tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı; proje toplamı **4876 structured + 15 Lua / 1516 patch asset** oldu. Oyun içi zırh tooltip genişliği, set bonusu satırları, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.28 Kademe 5 savaş ekipmanı

- Aktif Zırh ve Silahlar ağacındaki `tritaniumgear`, `enrichedgear`, `violiumgear`, `feroziumgear`, `aegisaltgear`, `densealloygear` ve `effigiumgear` düğümleri seçildi. Yedi düğümdeki açılımlar gerçek ve etkin `.recipe` çıktılarıyla çaprazlandı.
- **97 tarif destekli savaş ekipmanı** doğrulandı. Battle görevi kapsamında daha önce çevrilmiş `warcleaver` / **Ferozium Satırı** korundu; kalan **96 assette** yalnız `/shortdescription` ve `/description` yerelleştirildi.
- `itemName`, hasar, yetenek, mermi, kategori, tarif ve script alanları değiştirilmedi. Beş kalkan da araştırma + tarif zincirinden açılan savaş ekipmanı olduğu için aynı görünür alan kuralıyla kapsama alındı.
- Tritanium, Effigium, Aegisalt, Ferozium ve Violium özel malzeme adları korundu. **Phantasm → Hayalet, Shadow Reaper → Gölge Biçici, Veilbreaker → Perdekıran, Minigun → Döner Makineli Tüfek** kararları kilitlendi; `FarSight`, `Helios`, `Imperius` ve `Fissure` model/özel ad olarak korundu.
- Yeni kapsam **192 yapılandırılmış alan / 96 patch asset**tir. Tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı; proje toplamı **5068 structured + 15 Lua / 1612 patch asset** oldu. Oyun içi silah adı, tooltip genişliği, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.29 Kademe 5 aktif zırh setleri

- Aktif Zırh ve Silahlar ağacındaki `tritaniumgear`, `enrichedgear`, `violiumgear`, `feroziumgear`, `aegisaltgear`, `densealloygear` ve `effigiumgear` düğümleri zırh çıktıları için seçildi. Araştırma açılımı ile gerçek `.recipe` çıktısı birlikte erişilebilirlik kanıtı sayıldı.
- Yedi düğümde daha önce yerelleştirilmemiş **61 üretilebilir zırh asseti** doğrulandı. Her assette yalnız `/shortdescription` ve `/description` çevrildi; teknik `itemName`, stat hesapları, efekt listeleri, tooltip türü, kategori, tarif ve script alanları korundu.
- Kaynak klasör kademesi yerine runtime araştırma zinciri esas alındı. Bu nedenle dosya yolu `tier4` altında olan Kral Katili ile `tier6` altında olan Şampiyon, Güneş Gezgini, Morphite Mk. 2 ve Replikant setleri Kademe 5 kapsamında yerelleştirildi.
- **Beastmaster → Canavar Ustası, Skill Quiver → Beceri Sadağı, Peerless Quiver → Eşsiz Sadak, Kingslayer → Kral Katili, Sentry → Nöbetçi, Champion → Şampiyon, Sunwalker → Güneş Gezgini, Replicant → Replikant** kararları kilitlendi. `Capturenaut`, `Gishinanki`, `Decker`, `Legionii`, `Millenion`, `Morphite`, `Rifter`, `Valkyrie` ve `Warframe` model/özel ad olarak korundu.
- Tooltip terimleri **Havada Hasar, Germe Hızı, Atış Başına Enerji, Katana Ustalığı, Yerçekimi Yağmuru, Ağır Giysi, Tek Kılıç** ve **Çift Kılıçlar** biçiminde kilitlendi.
- Yeni kapsam **122 yapılandırılmış alan / 61 patch asset**tir. Tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı; proje toplamı **5190 structured + 15 Lua / 1673 patch asset** oldu. Oyun içi zırh tooltip genişliği, set bonusu satırları, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-20 - v0.30 aktif araştırma ekipmanı kapanışı

- Aktif `fu_warcraft` ağacı tam olarak yeniden denetlendi. Kapsama alınmak için araştırma düğümü açılımı, gerçek `.recipe` çıktısı ve görünür bir ekipman asseti birlikte zorunlu tutuldu; yalnız dosya varlığı veya `/spawnitem` erişimi yeterli sayılmadı.
- Daha önce yerelleştirilmemiş **413 tarif destekli asset** bulundu: 6 erken kalkan, 126 erken yan dal ekipmanı, 85 Kirhos/Lunari/Elduu/Skath/Vel'uuish silahı, 28 EPP/sırt ekipmanı, 130 Kademe 6 ve 38 Kademe 7 ekipmanı. Sınıf dağılımı **288 silah/kalkan + 125 zırh/EPP** olarak doğrulandı.
- Her assette yalnız `/shortdescription` ve `/description` çevrildi. Teknik `itemName`, tarifler, stat hesapları, efekt listeleri, yetenekler, mermiler, kategori ve script alanları değiştirilmedi.
- Sayıların değeri ve sırası, renk kodları, tooltip simgeleri, satır sonları ve sekmeler kaynakla birebir kilitlendi. 826 yeni alanın tamamı pinned FU 6.5.8 kaynağına karşı exact test/replace korumasına alındı.
- `EPP`, `Aether`, `Stynger`, `Magnorb`, `Xithricite`, `Isogen`, `Pyreite`, `Solarium`, `Densinium`, `Oceanite`, `Thanatite` ve `Nhydri` özel yazımları korundu. **Minor Vulnerability → Hafif Savunmasızlık, Alt-Fire → Alternatif Atış, Spawns Minions → Minyon Çağırır, Electrified → Elektriklenme, Frost Burn → Ayaz Yanığı** kararları kilitlendi.
- EPP enerji paketlerindeki `E. Block`, mevcut `Energy Regen Block` kararıyla aynı mekanik kabul edilerek **Enerji Yenilenme Gecikmesi** olarak çevrildi. `Heating EPP` ve `Cooling EPP` işlev yönünü açıkça korumak için **Isıtma EPP'si** ve **Soğutma EPP'si** oldu.
- Yeni kapsam **826 yapılandırılmış alan / 413 patch asset**tir. Proje toplamı **6016 structured + 15 Lua / 2086 patch asset** oldu. Böylece aktif Zırh ve Silahlar araştırma ağacındaki tarif destekli ekipman kapsamı kapandı; oyun içi tooltip, font ve bağlam LQA'sı ayrıca bekliyor.

## 2026-09-21 - CI kaynak doğrulama ve dağıtım ağacı sıkılaştırması

- Ana paket workflow'u artık FU kaynağını `tools/kaynaklar.json` içindeki pinned committen checkout eder ve `build_validate.py --source-dir fu_source` çalıştırır. Böylece JSON Patch `test` değerleri yalnız katalog içi fixture'a karşı değil, gerçek FU 6.5.8 kaynağına karşı da her ana buildde doğrulanır.
- Repository'deki `FU_Turkce/` kurulum ağacı ile `dist/FU_Turkce_v0.30.0_Beta.zip` aynı `build_output` ağacından üretilir. Generated commit yalnız bu iki yolu değiştirdiğinde workflow tekrar tetiklenmez.
- Structured metinler için `{0}`, `{item}`, `$variable` ve `${variable}` placeholder eşitliği ile satır sonu sayısı yeni statik guardlara alındı.
- Dil QA sırasında üç yapay/ham ifade düzeltildi: Vel'uuish tüfek açıklaması, Uzay Giysisi Hava Tankı açıklaması ve Yerçekimi Silahı açıklaması. Aynı ifadelerin geri dönmesini önlemek için regresyon guardları eklendi.


## 2026-09-21 - Ekipman terminolojisi düzeltmeleri

- `Greaves` için mevcut LOCKED **Baldırlık** kararı bütün envanter adlarına uygulandı; çoğul **Baldırlıkları** ve eksik tamlama eki kullanılan eski adlar tekil eşya adı biçiminde temizlendi.
- `Skill Quiver` yazımındaki eski **Beceri Sadakı** biçimi Türkçe tamlama hatası olduğu için **Beceri Sadağı** olarak düzeltildi ve ilgili terminoloji kayıtları güncellendi.
- `Teleporter` için LOCKED **Işınlayıcı** kararı korundu. Radyasyon silahı `Irradiator`, oyuncu tarafındaki ad çakışmasını önlemek için **Radyasyon Yayıcı** olarak kilitlendi.
