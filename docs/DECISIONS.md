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
