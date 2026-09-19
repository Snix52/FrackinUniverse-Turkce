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
