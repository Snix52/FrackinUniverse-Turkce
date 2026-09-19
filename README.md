# Frackin' Universe Türkçe

Frackin' Universe için topluluk tabanlı, gayriresmî Türkçe yerelleştirme projesi.

Bu depo şu anda **v0.1.0 Beta** durumundadır. Çeviri tamamlanmış değildir ve oyun içinde kapsamlı test beklemektedir.

## Mevcut kapsam

- Jeoloji araştırma ağacındaki seçili metinler
- Başlangıç görevlerinin bir bölümü
- Başlangıç telsiz ve öğretici mesajları
- Machining Table yükseltme kademeleri ve seçili arayüz metinleri
- Araştırma ekranındaki seçili açıklamalar

İlk paket toplam **185 metin alanı** için Türkçe karşılık içerir.

## Kurulum

1. Starbound ve Frackin' Universe kurulu olmalı.
2. Önce `storage` klasörünü yedekle.
3. `FU_Turkce` klasörünü Starbound'un `mods` klasörüne kopyala.
4. Son yol şu biçimde olmalı:

```text
Starbound/mods/FU_Turkce/_metadata
```

Ana Frackin' Universe `.pak` dosyasına veya Workshop klasörüne dokunma.

Ayrıntılı bilgi için `docs/KURULUM.txt` dosyasını oku.

## Sürüm uyumluluğu

İlk çeviri, Frackin' Universe deposundaki aşağıdaki kaynak anlık görüntüsüne göre hazırlanmıştır:

```text
FU sürümü: 6.5.8
Kaynak commit: 329e714b3fe87571055c8ad7aa38135d199d3317
```

Kaynak metin değişirse ilgili yama bilinçli olarak uygulanmayabilir. Bu davranış, eski çevirinin yeni FU sürümünün üstüne körlemesine yazılmasını önlemek içindir.

## Depo yapısı

```text
FU_Turkce/     Oyuna kurulacak mod klasörü
tools/         Çeviri defteri, kaynak kaydı ve doğrulama araçları
docs/          Kurulum, kontrol ve lisans notları
dist/          Hazır beta paketleri
```

## Yol haritası

- [x] Jeoloji araştırma ağacının ilk çevirisi
- [x] Başlangıç görevlerinin ilk paketi
- [x] Başlangıç telsiz ve öğretici mesajlarının ilk paketi
- [ ] Agriculture araştırma ağacı
- [ ] Chemistry araştırma ağacı
- [ ] Engineering araştırma ağacı
- [ ] Power araştırma ağacı
- [ ] Craftsmanship araştırma ağacı
- [ ] Warfare araştırma ağacı
- [ ] Madness araştırma ağacı
- [ ] Eşya ve makine açıklamalarının geniş kapsamlı çevirisi
- [ ] Görevlerin kalan bölümü
- [ ] Oyun içi tam test ve taşma kontrolleri

## Çeviri yaklaşımı

Kod, kimlikler, tarifler, maliyetler ve oyun mantığı değiştirilmez. Yalnızca oyuncunun gördüğü metin alanları hedeflenir. Renk kodları, tuş gösterimleri ve Starbound biçimlendirme etiketleri korunur.

Terimler mümkün olduğunca tutarlı tutulur. Özel evren terimlerinde anlam kaybı yaratacak zoraki Türkçeleştirmeden kaçınılır.

## Kaynak ve lisans

Orijinal çalışma: Frackin' Universe, sayter ve katkıda bulunanlar.

Kaynak: https://github.com/sayterdarkwynd/FrackinUniverse

Frackin' Universe kaynak deposu CC BY 4.0 lisansı belirtmektedir. Ayrıntılı attribution ve proje notları `docs/KAYNAK_VE_LISANS.txt` içindedir.

Bu proje Frackin' Universe ekibi, Chucklefish veya Starbound geliştiricileri tarafından hazırlanmış ya da onaylanmış resmî bir çeviri değildir.
