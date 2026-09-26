# S.A.I.L. gemi konuşmaları: Slimeperson ve Shadow

Oyuncunun üç ekran görüntüsündeki İngilizce replikler pinli FU 6.5.8
`objects/ship/slimepersontechstation/slimepersontechstation.object` dosyasının
`/dialog/wakeUp` dizisinden geliyor. Kurulu oyun günlüğü de bu üç metnin
oyuncuya gösterildiğini doğruladı.

Önceki gemi S.A.I.L. çevirisi 17 istasyonun 182 diyalog alanını kapsıyordu.
Kaynakta aynı betikleri ve S.A.I.L. arayüzünü kullanan Slimeperson ve Shadow
istasyonları dışında kalmıştı. Bu iki istasyonun 23 alanı (23 farklı kaynak
metni; 32 cümle) v0.65.2 kataloğuna eklendi. Portre yolları, satır sırası,
gemi davranışı ve FU kaynak pini değiştirilmedi.

Slimeperson S.A.I.L.'ın canlı/alaycı sesi korundu: “Yaşıyorum!”, “Çok iyi
arkadaş olacağız, eminim.”, “Tabii önce ölmezsen.” Shadow S.A.I.L.'ın mekanik
sesi korundu; oyuncuya seslenişi olan `Fragment` özel unvanı yalnız bu alanların
kaynak kapısında sabitlendi. S.A.I.L.'ın uzun tanımında ve bir yeniden başlatma
repliğinde daha önce onaylanan aynı Türkçe karşılıklar kullanıldı.

`tools/check_ship_sail_dialog_20260926.py` pinli FU ağacındaki **19 gemi
techstation nesnesinin 205 açılış/yeniden başlatma alanını** katalogla
karşılaştırır. Yeni bir istasyon, ek replik, kaynak değeri değişikliği veya
çevirisiz alan geldiğinde CI durur. Yeni 23 alanın manifest ve katalog
eşleşmesi ayrıca doğrulanır. Birim regresyonu çevrilmemiş ve değişmiş kaynak
satırlarını reddeder. Kaynak listesinde iki özgün FU dosyasının blob hashleri
tutulur.

Oyun içi tekrar testi: **NOT TESTED**. Ekran görüntüleri v0.65.1'deki
İngilizceyi kanıtlar; yeni Türkçe paket için görsel doğrulama ayrıca yapılır.
