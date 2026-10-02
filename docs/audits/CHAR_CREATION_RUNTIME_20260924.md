# Karakter oluşturma ekranı oyun içi kontrolü — 24 Eylül 2026

## v0.63'te görülen sorun

- `FU_Turkce/interface/windowconfig/charcreation.config.patch` bütün 19 metni tek koşullu işlem listesinde tutuyordu. FU'nun `interface/windowconfig/charcreation.config.patch` dosyası zorlu mod açıklamasını sonradan değiştirdiği için tek test başarısız oldu ve ekranın bütün Türkçe metinleri sessizce atlandı.
- FU'nun Steam `contents.pak` dosyasındaki çok satırlı tür açıklamaları CRLF içeriyor; pinli Git blobları LF içeriyor. Eski tür yaması yalnız LF değerini test ettiği için Avian dahil 10 türün Türkçe açıklaması Steam kurulumunda uygulanmadı. Bu iki kaynak biçimi aynı FU 6.5.8 metnini taşıyor.
- Kurulu iki genel Starbound Türkçe modundan biri karakter ekranında başarısız bir patch için günlük hatası veriyor (`2854928268`); bu hata FU Türkçe paketine ait değil.

## v0.63.1 düzeltmesi

- Karakter ekranındaki 19 alan ayrı koşullu gruplara ayrıldı. FU'nun sonradan değiştirdiği zorlu mod açıklaması doğru kaynak değeriyle kilitlendi ve kısa, anlamı koruyan Türkçe karşılıkla yenilendi.
- Tür açıklamalarında LF ve CRLF kaynak biçimleri ayrı koşullu gruplarla kabul edildi. Başka kaynak metni olursa ilgili grup çalışmıyor; tür adına ya da oyun parametrelerine dokunulmuyor.
- Pinli FU commit'i `bb58383c0d16c1152e3439e606b39ff82288b586` ve ilan edilen 6.5.8 sürümü değişmedi.
- Geçici kurulu pakette oyun içi denemede `IRK` etiketleri ile Avian, Fenerox ve Thelusian açıklamaları Türkçe göründü. Zorlu mod açıklaması kısaltıldı ve son paketle 800×630 oyun penceresinde metin alanına sığdığı görüldü.
- CI paket kanıtı doğrulayıcısı da koşullu grup biçimini ve yalnız LF/CRLF kaynak varyantını sayacak şekilde güncellendi; yanlış kaynak varyantı hâlâ reddediliyor.

## Ayrı kalan görünür alanlar

- `CHARACTER CREATION` metni FU'nun `interface/title/charactercreation.png` görseline işlenmiş. Görseli yeniden üretme denemesi özgün piksel düzenini korumadığı için pakete alınmadı.
- `Feather colour`, `Beak`, `Plumage` gibi türe özgü özelleştirme etiketleri `/species/*.species` içindeki `charGenTextLabels` alanından geliyor. Bunlar v0.40/v0.46 katalog kapsamına hiç alınmamış. Türlerin tamamı için kaynak ve oyun içi görünürlük denetimiyle ayrı çeviri turu gerekiyor.
- Bu nedenle v0.63.1 yaması karakter oluşturma ekranının bütün İngilizce parçalarını kapattığını iddia etmez.
