# Frackin' Universe Türkçe

Frackin' Universe'ü Türkçe oynamak isteyenler için hazırlanan gayriresmî yerelleştirme projesi.

**Güncel sürüm:** v0.30 Beta  
**Hedef FU sürümü:** 6.5.8  
**Durum:** Statik kontroller tamamlandı. Oyun içi LQA, font ve taşma kontrolleri devam ediyor.

Bu çalışma henüz FU'nun tamamını çevirmiyor. Şu an **6.016 yapılandırılmış oyuncu metni** ve **15 Lua arayüz metni** olmak üzere toplam **6.031 görünür metin birimi** Türkçeleştirilmiş durumda.

## Neler Türkçe?

Şu anki kapsamın ana parçaları:

- Ana araştırma ağaçları ve ilgili arayüz metinleri
- Tutorial, Science, Outpost, Battle, Other ve BYOS tarafındaki erişilebilir görev zincirleri
- Görevlerde doğrudan kullanılan eşya ve makine adları
- Üretim makineleri ve seçili işlevsel dünya nesneleri
- Erişilebilir `items/generic/crafting` malzemeleri
- Zırh ve Silahlar araştırma ağacına bağlı geniş silah ve zırh kapsamı
- Başlangıç mesajları ve seçili UI metinleri

Kapsam genişlemeye devam ediyor. Bir dosyanın kaynakta bulunması tek başına yeterli sayılmıyor; oyuncunun gerçekten erişebildiği içerik mümkün olduğunca görev, tarif, araştırma, NPC veya dünya bağlantıları üzerinden doğrulanıyor.

## Kurulum

1. Starbound'u kapat.
2. Mümkünse `storage` klasörünü yedekle.
3. Güncel beta paketini çıkar.
4. İçindeki `FU_Turkce` klasörünü Starbound'un `mods` klasörüne kopyala.
5. Son yol şu şekilde görünmeli:

```text
Starbound/mods/FU_Turkce/_metadata
```

Ana Frackin' Universe `.pak` dosyasını veya Workshop klasörünü değiştirme.

Ayrıntılı kurulum notu: [docs/KURULUM.txt](docs/KURULUM.txt)

## Çeviri yaklaşımı

Amaç İngilizce cümleleri tek tek Türkçeye çevirmek değil, oyunun sistemlerini Türkçe olarak takip edilebilir hâle getirmek.

Bu yüzden özellikle şunlara dikkat ediliyor:

- Aynı eşya, makine ve sistem adı her yerde aynı kalmalı.
- Görevde yazan ad, envanter ve üretim menüsündeki adla uyuşmalı.
- JSON key'leri, ID'ler, asset yolları, placeholder'lar ve biçimlendirme kodları korunmalı.
- UI kısa ve anlaşılır, görev hedefleri doğrudan, diyaloglar ise karakterin tonuna uygun olmalı.
- Bağlamı belirsiz terimler tahmin edilmek yerine ayrıca kontrol edilmeli.

Projenin dil ve teknik kuralları:
- [Çeviri standardı](docs/STYLE_GUIDE.md)
- [Terminoloji](docs/TERMINOLOGY.md)
- [Karar kaydı](docs/DECISIONS.md)
- [QA kuralları](docs/QA_RULES.md)

## Geliştirme notu

Bu proje tek kişi tarafından yürütülüyor. Otomasyon ve yapay zekâ araçları büyük iş yükünü yönetmek için yardımcı araç olarak kullanılıyor; terminoloji, bağlam, patch yapısı ve QA sonuçları proje kurallarına göre ayrıca kontrol ediliyor.

Kısacası amaç otomatik çeviri yığını çıkarmak değil, İngilizce bilmeden oynanabilecek tutarlı bir Türkçe FU deneyimi oluşturmak.

## Test durumu

Statik QA; kaynak eşleşmeleri, patch yapısı, placeholder'lar, biçimlendirme kodları, teknik alanlar ve terminoloji gibi kontrolleri kapsıyor.

Buna rağmen statik kontrol tek başına yeterli değil. Oyun içinde özellikle şu noktaların denenmesi gerekiyor:

- Türkçe karakter ve font görünümü
- Metin taşmaları
- Görev akışı
- Görev, eşya ve üretim adı eşleşmeleri
- NPC ve ekran bağlamları
- Renkler, satır sonları ve buton metinleri

Bu yüzden proje hâlâ **Beta** olarak işaretleniyor.

## Kaynak ve lisans

Frackin' Universe, sayter ve katkıda bulunanların çalışmasıdır. Bu proje FU ekibi, Chucklefish veya Starbound geliştiricileri tarafından hazırlanmış ya da onaylanmış resmî bir Türkçe sürüm değildir.

Kaynak, lisans ve atıf bilgileri: [docs/KAYNAK_VE_LISANS.txt](docs/KAYNAK_VE_LISANS.txt)

## Hata bildirimi

Bir hata bulursan mümkünse şunları birlikte paylaş:

- Sorunun ekran görüntüsü
- Hangi görev, eşya, makine veya ekranda olduğu
- `Starbound/storage/starbound.log`
- Kullandığın FU Türkçe sürümü

Özellikle farklı çevrilmiş aynı eşya adları, İngilizce kalmış görünür metinler ve görevde söylenen şeyin oyunda bulunamaması en yüksek öncelikli hatalar arasında.
