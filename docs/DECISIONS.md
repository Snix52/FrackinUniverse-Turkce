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

- Mevcut 654 oyuncu metni; boş çeviri, yinelenen pointer, placeholder/renk/escape bütünlüğü, aynı kaynak string tutarlılığı, kilitli terminoloji ve İngilizce parantez kalıntıları açısından yeniden tarandı.
- Jeoloji metninde kalan `(Inventor’s Table)` İngilizce parantez açıklaması kaldırıldı.
- Tarım ağacındaki `Extraction Lab` kullanımı **Çıkarma Laboratuvarı** ile, `Advanced Beekeeping` başlığı **Gelişmiş Arıcılık** ile yeniden eşleştirildi.
- Jeoloji ve Mühendislik arasında farklı çevrilen Terraforming ailesi tekleştirildi: **Gezegen Biçimlendirme**, **Mikro Biçimlendirici**, **Gezegen Biçimlendirici** LOCKED.
- Başlangıç telsiz mesajındaki Starbound sistem adı `Tech Upgrades`, kilitli **Tech** terminolojisine uygun olarak **Tech Yükseltmeleri** yapıldı.
- Mühendislikte Mech Parçası Üretim Tezgâhına gönderme yapan belirsiz “bir tane araştırabilir” ifadesi, araştırılan nesnenin tezgâh olduğunu açıkça belirtecek şekilde düzeltildi.
- Gelişmiş Xeno Laboratuvarının açıklaması, aynı nesnenin kilitli görünen adıyla eşleştirildi; “Quantum Xeno Lab” ifadesi nesne adı gibi kullanılmayıp kuantum teknolojisi bilgisi açıklamada korundu.
- Teknik ID, JSON path, placeholder, biçimlendirme kodu veya kaynak pointer değiştirilmedi. Çevrilen alan sayısı **654** olarak kaldı.

