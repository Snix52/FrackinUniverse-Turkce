# Frackin' Universe Türkçe

Frackin' Universe için topluluk tabanlı, gayriresmî Türkçe yerelleştirme projesi.

**Durum: v0.10.0 Beta / Ana araştırma sistemleri + Delilik/Metafizik + Tutorial + Science görevleri / statik QA tamamlandı, oyun içi LQA bekliyor.**

## Mevcut kapsam

- Jeoloji araştırma ağacındaki aktif çevrilebilir metinler
- Tarım araştırma ağacının tamamı
- Kimya araştırma ağacının tamamı
- Mühendislik araştırma ağacının tamamı
- Güç Sistemleri araştırma ağacının tamamı
- Zanaatkârlık araştırma ağacının tamamı
- Zırh ve Silahlar araştırma ağacının tamamı
- Delilik / Metafizik araştırma ağacının 31 aktif düğümünün tamamı
- Delilik sisteminin temel psiyonik, ruh sağlığı ve madde işleme eşya/makineleri
- Tutorial görev ailesindeki bağlı görevlerin tamamı (41/41 görev dosyası)
- Tutorial görevlerinde doğrudan hedef gösterilen temel eşya ve makinelerin envanter adları
- Science bağlantılı erişilebilir görevlerin tamamı (37/37 benzersiz görev; 35 quest-list + 2 çapraz akış görevi)
- Science görevlerinde doğrudan hedef gösterilen temel eşya, malzeme ve makinelerin envanter adları
- Zırh ve Silahlar ağacının doğrudan yönlendirdiği Zırh Atölyesi, Örs yükseltmeleri ve Solunum EPP'si
- Zanaatkârlığın doğrudan referans verdiği koloni, mutfak, dikiş, biyokimya ve temel üretim istasyonları
- Güç Sistemlerinin doğrudan bağlı temel üretim, reaktör, pil, santrifüj ve atmosfer makineleri
- Başlangıç görevlerinin bir bölümü ve BYOS Yıldızlararası Yolculuk zinciri
- Başlangıç telsiz/öğretici mesajlarının mevcut dosyadaki 26/26 metni
- İmalat Tezgâhı yükseltme kademeleri ve seçili arayüz metinleri
- Tarım/genetik makineleri ve temel Tarım öğretici görevleri
- Kimya Laboratuvarı ve doğrudan bağlı temel kimya kaynakları
- Mühendislikteki temel çıkarma, araştırma, gemi ve çekirdek makineleri/kaynakları
- STL Motoru ve Küçük FTL Motoru oyuncu metinleri
- Araştırma ekranındaki seçili açıklamalar, fallback metinleri ve Lua içine gömülü sabit UI metinleri

Toplam **1.714 yapılandırılmış oyuncu metni alanı** ve **15 Lua UI metni**, yani **1.729 yerelleştirilmiş görünür metin birimi** bulunmaktadır. Bu, FU'nun tamamının Türkçe olduğu anlamına gelmez.

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

> **Paket notu:** Güncel beta paketi `dist/FU_Turkce_v0.10.0_Beta.zip` olarak GitHub Actions tarafından statik QA sonrasında otomatik üretilir.

## Sürüm uyumluluğu

```text
FU sürümü: 6.5.8
Kaynak commit: 329e714b3fe87571055c8ad7aa38135d199d3317
```

Güncel statik QA'da toplam yapılandırılmış kapsam **1.714 alan / 239 patch asset**tir. v0.10 Science eklemesindeki **204 yeni alanın 193'ü pinned FU 6.5.8 kaynağından**, **11'i bağımsız vanilla kaynağından** exact doğrulandı. Araştırma ekranının JSON Patch dışında kalan **1 Lua assetindeki 15 görünür metin** exact kaynak-fragment korumasıyla ayrıca doğrulanır.

`build_validate.py`, kaynak klasörü verilirse Lua override'ını doğrudan o kaynak script üzerinden üretir; beklenen kaynak metinlerinden biri değişmişse build durur.

## v0.6 Zanaatkârlık

Zanaatkârlık ağacındaki **76 gerçek araştırma düğümü** ve ağaç adı yerelleştirildi. Kaynakta bulunan ancak arayüz kodunda kullanılmayan `default` yardım/fallback çifti ile hiçbir düğüme bağlı olmayan `workbenchatechy` stringi oyuncuya görünmediği için yamaya alınmadı. Doğrudan yönlendirme yapılan temel istasyon adları envanter adlarıyla eşleştirildi.

v0.6 eklemesi: **284 aktif yapılandırılmış alan / 12 hedef asset**. Oyun içi LQA ve panel taşma kontrolleri hâlâ bekliyor.

## v0.7 Zırh ve Silahlar

Zırh ve Silahlar ağacındaki **47 gerçek araştırma düğümü** ve ağaç adı yerelleştirildi. Kaynaktaki `default` yardım/fallback çifti arayüz kodu tarafından kullanılmadığı için yamadan çıkarıldı. Araştırmanın doğrudan yönlendirdiği ana istasyonlar gerçek envanter adlarıyla eşleştirildi: **Zırh Atölyesi → Montaj Hattı → Cephanelik**, **Örs → Dövme Ocağı → Çoğaltıcı** ve **Solunum EPP'si**.

v0.7 eklemesi: **115 aktif yapılandırılmış alan / 4 hedef asset**. Oyun içi LQA ve panel taşma kontrolleri bekliyor.

## v0.8 Delilik / Metafizik

Delilik ağacındaki **31 aktif araştırma düğümü** ve ağaç adı yerelleştirildi. Kaynaktaki runtime'da kullanılmayan `default` yardım/fallback çifti yamaya alınmadı.

Aynı paket içinde oyuncunun sistemi İngilizce bilmeden takip edebilmesi için **Delilik**, **Karanlık Madde**, **Beyin Çıkarıcı**, **Psiyonik Tezgâhı**, **Psiyonik Yükselteç**, **Psi Enerjisi**, **Psiyonik Odak**, **Insta-Freud**, **Otopsi Masası**, **Madde Dönüştürücü**, Beyin Jeneratörü/Pili ve ilgili Psiyonik Tezgâhı UI metinleri de eşlendi.

v0.8 eklemesi: **103 aktif yapılandırılmış alan / 18 hedef asset**. Yeni alanların tamamı pinned FU 6.5.8 kaynağıyla exact doğrulandı. Oyun içi LQA ve panel taşma kontrolleri bekliyor.


## v0.9 Tutorial Görevleri

FU `fu_questlines/tutorial` altında kaynakta **42 questtemplate** bulunuyor. Bunlardan `start_basics1`, yarıda kesilmiş metni ve hiçbir yerden çağrılmayan yapısı nedeniyle kırık/bağlantısız kaynak olarak dağıtıma alınmadı. Oyuncunun ulaşabildiği tutorial ailesi böylece **41/41 görev dosyası** olarak Türkçeleştirildi.

v0.9'da daha önce çevrilmemiş **25 tutorial görev dosyasında 90 oyuncu metni** yerelleştirildi. Görev hedeflerinin envanterle birebir eşleşmesi için ayrıca **19 hedef eşya/makine assetinde 41 alan** çevrildi. Toplam v0.9 eklemesi **131 yapılandırılmış alan / 44 hedef asset**tir.

Kaynakta oyuncuyu yanlış yönlendiren eski tutorial metinleri gerçek quest koşullarına göre düzeltildi: Extractor IV/V'nin eski Tissue Culture / Genetic Material yönlendirmeleri, `create_silicon` içindeki 10 yerine gerçek 1 Silisyum koşulu, Wooden Centrifuge teslim hedefindeki yanlış Armorworks adı ve Rock Breaker metnindeki bozuk renk kapanışı.

Science cephesi v0.10 ile kapandı. Klasör-bazlı yol haritasında sırada **75 görev dosyası** bulunuyor: Outpost 45, Battle 13, Other 13, BYOS 3 ve Exploration 1. Science denetiminde görüldüğü gibi, her kategori işlenirken yalnız klasör sayısına değil runtime quest-list/NPC bağlantılarına da bakılacak.

## v0.10 Science Görevleri

Science klasöründe ham olarak **36 questtemplate** bulunmasına rağmen runtime akışı klasör yapısıyla birebir değildir. `fuquest_dna` ve `fuquest_mineral` hiçbir NPC, prerequisite zinciri veya quest-list tarafından çağrılmadığı için bağlantısız legacy görev olarak dağıtım dışı bırakıldı. Buna karşılık `deprecated` klasöründeki `fuquest_powerstation`, `fuquest_battery` ve `fuquest_prototyper` hâlâ Science quest-list tarafından başlatılıyor. Ayrıca `fuquest_biochem` Tutorial alt zincirinden, `create_blackglass` ise Bilim Karakolu NPC'sinden erişilebilir.

Bu nedenle oyuncunun ulaşabildiği benzersiz Science bağlantılı kapsam **37/37 görev** olarak yerelleştirildi: Chemistry 8, Electronics 8, Genetics 9, Mechanical 8 ve Physics 4.

v0.10 eklemesi **204 yapılandırılmış alan / 64 yeni patch asset**tir. Görevlerdeki eski veya hatalı üretim yönlendirmeleri gerçek tarif ve quest koşullarıyla karşılaştırıldı. Öne çıkan düzeltmeler arasında eski Bio Lab yönlendirmesi, Silisyum Devre Kartının eski Madde Birleştirici tarifi, Wiring Tool adı, Genetics laboratuvar kademe hataları, eski Fission Furnace adı ve Tritium görevindeki artık geçerli olmayan Fisyon Reaktörü hedefi bulunur.

Yeni alanların tamamı kaynak/provenans kontrolünden geçti: **193/193 pinned FU alanı + 11/11 bağımsız vanilla alanı**, toplam **204/204 PASS**. Patch pairing **204 test + 204 replace PASS**. Oyun içi görev akışı, font ve panel taşma LQA'sı ayrıca yapılmalıdır.

## Yol haritası

- [x] Jeoloji araştırma ağacının ilk çevirisi
- [x] Başlangıç görevlerinin ilk paketi
- [x] Başlangıç telsiz ve öğretici mesajlarının ilk paketi
- [x] v0.1.1 Anayasa uyum düzeltmesi
- [x] Tarım araştırma ağacı
- [x] Kimya araştırma ağacı
- [x] Mühendislik araştırma ağacı
- [x] v0.4 geriye dönük statik QA ve eksik alan temizliği
- [x] v0.5 Güç Sistemleri ve bağlı temel makineler
- [x] Güç Sistemleri araştırma ağacı
- [x] Zanaatkârlık araştırma ağacı
- [x] Zırh ve Silahlar araştırma ağacı
- [x] v0.7 geriye dönük aktif-düğüm / ölü-string QA
- [x] Delilik araştırma ağacı
- [x] Tutorial görev ailesi
- [x] Science görev zincirleri
- [ ] Outpost görev zincirleri
- [ ] Battle görev zincirleri
- [ ] Other görev zincirleri
- [ ] BYOS kalan görevleri
- [ ] Exploration görev zinciri
- [ ] Eşya ve makine açıklamalarının geniş kapsamlı çevirisi
- [ ] Görevlerin kalan bölümü
- [ ] Oyun içi tam LQA ve taşma kontrolleri

## Kaynak ve lisans

Orijinal çalışma: Frackin' Universe, sayter ve katkıda bulunanlar.

Frackin' Universe kaynak deposu CC BY 4.0 lisansı belirtmektedir. Ayrıntılar `docs/KAYNAK_VE_LISANS.txt` içindedir.

Bu proje Frackin' Universe ekibi, Chucklefish veya Starbound geliştiricileri tarafından hazırlanmış ya da onaylanmış resmî bir çeviri değildir.
