# Frackin' Universe Türkçe

Frackin' Universe için topluluk tabanlı, gayriresmî Türkçe yerelleştirme projesi.

**Durum: v0.1.1 Beta / Anayasa statik QA geçti / oyun içi LQA bekliyor.**

## Mevcut kapsam

- Jeoloji araştırma ağacındaki seçili metinler
- Başlangıç görevlerinin bir bölümü
- Başlangıç telsiz ve öğretici mesajları
- İmalat Tezgâhı yükseltme kademeleri ve seçili arayüz metinleri
- Araştırma ekranındaki seçili açıklamalar

Toplam **185 oyuncu metni alanı** çevrilmiştir. Bu, FU'nun tamamının Türkçe olduğu anlamına gelmez.

## Anayasa ve terminoloji

- Ana standart: `docs/STYLE_GUIDE.md`
- Terminoloji: `docs/TERMINOLOGY.md`
- Karar kaydı: `docs/DECISIONS.md`
- QA kuralları: `docs/QA_RULES.md`

Oyuncuya gösterilen Türkçe adların yanına İngilizce karşılık parantez içinde eklenmez. Türkçe karakterler zorunludur; ASCII yedek sürüm üretilmez.

## Kurulum

1. Starbound ve Frackin' Universe kurulu olmalı.
2. Önce `storage` klasörünü yedekle.
3. `FU_Turkce` klasörünü Starbound'un `mods` klasörüne kopyala.
4. Son yol şu biçimde olmalı:

```text
Starbound/mods/FU_Turkce/_metadata
```

Ana Frackin' Universe `.pak` dosyasına veya Workshop klasörüne dokunma.

Ayrıntılı bilgi: `docs/KURULUM.txt`.

## Sürüm uyumluluğu

```text
FU sürümü: 6.5.8
Kaynak commit: 329e714b3fe87571055c8ad7aa38135d199d3317
```

v0.1.1 hazırlanırken **14/14 hedef kaynak dosya ve 185/185 kaynak alanı exact commit üzerinden pointer bazında doğrulandı**.

## Yol haritası

- [x] Jeoloji araştırma ağacının ilk çevirisi
- [x] Başlangıç görevlerinin ilk paketi
- [x] Başlangıç telsiz ve öğretici mesajlarının ilk paketi
- [x] v0.1.1 Anayasa uyum düzeltmesi
- [ ] Tarım araştırma ağacı
- [ ] Kimya araştırma ağacı
- [ ] Mühendislik araştırma ağacı
- [ ] Enerji araştırma ağacı
- [ ] Zanaatkârlık araştırma ağacı
- [ ] Savaş araştırma ağacı
- [ ] Delilik araştırma ağacı
- [ ] Eşya ve makine açıklamalarının geniş kapsamlı çevirisi
- [ ] Görevlerin kalan bölümü
- [ ] Oyun içi tam LQA ve taşma kontrolleri

## Kaynak ve lisans

Orijinal çalışma: Frackin' Universe, sayter ve katkıda bulunanlar.

Frackin' Universe kaynak deposu CC BY 4.0 lisansı belirtmektedir. Ayrıntılar `docs/KAYNAK_VE_LISANS.txt` içindedir.

Bu proje Frackin' Universe ekibi, Chucklefish veya Starbound geliştiricileri tarafından hazırlanmış ya da onaylanmış resmî bir çeviri değildir.
