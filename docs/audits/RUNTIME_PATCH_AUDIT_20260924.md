# FU Türkçe runtime yama denetimi — 24 Eylül 2026

## Bulgular

Pinli FU 6.5.8 kaynağı (`bb58383c0d16c1152e3439e606b39ff82288b586`) ve kurulu Steam FU paketi, katalogdaki 812 doğrudan kaynak alanında metin içi LF/CRLF farkı taşıyor. Önceki build, Python `read_text()` ile satır sonlarını normalleştirdiği için bunu kaçırdı. Bu alanların 802'si tek test listesindeki yamalarda bulunuyordu; bu 802 asset içindeki 1.606 alan birlikte atlanabiliyordu. Tür açıklamalarının 10'u v0.63.1'de korunmuştu. FU kaynak yamasından gelen bir SAIL satırı da CRLF nedeniyle atlanıyordu. Üç alan hem LF hem CRLF içeren karışık metin taşıyor.

FU'nun kendi `.patch` dosyaları altı açıklamayı değiştirmişti: yağ, Tech Konsolu, Böcek Ağı, çakıl, portakal ve Erimiş Çekirdek. Katalog eski İngilizce değeri test ettiği için bu altı açıklama ile aynı assetlerdeki altı kısa adın çevirisi uygulanmıyordu. Altı açıklamanın katalog kaynağı FU sonrası değerle eşleştirildi; Türkçe açıklamaları bu metne göre güncellendi. Pinli vanilla ve FU yama koşulları kurulu oyun dosyalarında ayrıca incelendi. Grafen yaması aynı kaynak değerini yazdığı için uyuşmazlık yaratmıyor.

Kalan 49 vanilla kaynaklı katalog alanı kurulu Starbound `packed.pak` içindeki değerlerle eşleşiyor; hedef alanlarını FU yamaları değiştirmiyor. Bu denetim mevcut base → FU → FU Türkçe yükleme sırası için statiktir. Başka modlar etkinleşirse onların yama sırası ayrıca denetlenmelidir.

## Kalıcı build kapısı

- Her çeviri alanı bağımsız koşullu `test`/`replace` grubu olarak üretilir. Bir kaynaktaki fark diğer alanları düşüremez. Paket doğrulayıcısı çok alanlı düz yamayı reddeder.
- LF ve CRLF kaynak değerleri aynı incelenmiş metnin koşullu seçenekleridir. Üç karışık satır sonlu alanın tam düzeni katalogda sabitlenir; farklı metin varyantı kabul edilmez.
- Pinli FU kaynak dosyaları satır sonları korunarak okunur. Build, ürettiği Türkçe yamaları bu ham değerlere uygulayıp her doğrudan alanın gerçekten çevrildiğini doğrular.
- FU'nun iç içe `.patch` grupları da taranır. FU sonrası kaynak değeri katalogla farklıysa açık kaynak yaması dayanağı olmadan build başarısız olur. FU yamalı alanlar ham yama değeriyle ayrıca simüle edilir.
- Kaynak FU pini, sürüm 6.5.8 ve toplam katalog alanı korunmuştur. Bu düzeltmede altı Türkçe açıklama alanı değişti.
