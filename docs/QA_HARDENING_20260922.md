# v0.45.1 ana kontrol bakım raporu

## Kapsam ve kaynak

22 Eylül 2026 ana kontrolündeki F01-F08 bulguları için bakım paketi. Başlangıç main: `c2fb78b76d00cb9bc0aff9bbc904eba381de0a8c`. FU pini değiştirilmedi: `329e714b3fe87571055c8ad7aa38135d199d3317` (6.5.8). Yeni v0.46 içerik grubuna başlanmadı.

Yayımlanmış son paketin sürümü, kaynak commit'i, workflow run numarası, SHA-256 ve doğrulama sonucu için tek kaynak [`../dist/build-evidence.json`](../dist/build-evidence.json). Bu belgeye değişken paket hash'i veya CI run'ı kopyalanmaz. Kaynak değişikliği ile paket yayını arasındaki sürede son yayımlanmış sürüm evidence dosyasından okunur.

## Kapatılan kod ve içerik bulguları

| Bulgu | Uygulanan değişiklik | Geri dönüş koruması |
|---|---|---|
| F01: Lua güvenlik kontrolü eksikleri | Gerçek Lua string literal'leri ayrıştırılır. Değişebilen string indeksleri `text_literals` ile açıkça belirtilir. Kod, yorumlar, widget adları ve diğer stringler exact kalır. | Placeholder, printf sırası, renk, sayı, kaçış, kontrol tokeni, kod/widget değişikliği ve sahte metadata negatif testleri. |
| F02: Doğru terim yanlış varyantı gizliyor | Doğru terim bulunduğunda tüm cümleyi atlama kaldırıldı. Yalnız doğru ifadenin içinde kalan kısa yasaklı alt-sözcük muaf tutulur. | Ayrı doğru+yanlış kullanım reddedilir; doğru ve Türkçe çekimli kullanım geçer. |
| F03: `[Tile]` yanlış korunuyor | Beş görünür durum etiketi `[Zemin]` yapıldı; eski testin yanlış beklentisi düzeltildi. | İstisnalar asset/pointer/en/tr/gerekçeye bağlı. `[Fire]`, `<item>` ve `[(pause)...]` için genel geçiş yok. |
| F04: Mech yakıt uyarıları | Dolu depo ve farklı yakıt türü uyarıları Türkçeleştirildi. | Pinned blob doğrulaması, yalnız metin değişikliği, iki hata yolunda tüketim olmaması ve normal yakıt doldurma testleri. |
| F05: Checkpoint kanıtı eski | Güncel durum canonical evidence dosyasına bağlandı; eski sürüm bölümleri tarihsel olarak işaretlendi. README'den kopya hash kaldırıldı. | Son yayımlanmış sürüm/run/hash tek dosyadan takip edilir. |
| F06: PR/generated kontrolü | Salt okunur PR QA eklendi. Main paths-ignore kaldırıldı; doğrudan generated dosya değişikliği çıktı yenilenmeden önce reddedilir. | Generated-only ve mixed edit negatif testleri. Yayın botunun mevcut kaynak-SHA yarış kontrolü korunur. Sunucu tarafındaki required checks ayrı açık ayardır. |
| F07: Lua davranışı çalıştırılmıyor | Gerçek Lua 5.4 ile 14 yazı animasyonu ve 8 Mech yakıt senaryosu eklenir. | Testler önce kaynak şablonlarında, ardından pinned build'in ürettiği Lua'da çalışır. Lua kitaplığı yoksa sessiz atlama yoktur. |
| F08: Görev dili | Üç ifade ve bir nokta sonrası boşluk düzeltildi; katalog ve tarihsel manifestler birlikte güncellendi. | Manifest/katalog eşitliği, kaynak kilidi ve genel biçim kontrolleri. |

## Geriye dönük denetim

8.024 structured alanın tamamı korundu. Asset, pointer ve İngilizce kaynaklar değişmedi. Yalnız dokuz Türkçe hedef metni değişti: beş zemin etiketi, üç görev ifadesi ve bir görevde nokta sonrası boşluk. Beş zemin satırına ayrıca dar QA gerekçesi eklendi.

50 mevcut raw replacement, açık görünür string slotlarına taşındı. Bu eski Lua çevirilerinin metinleri değiştirilmedi. Mech için iki replacement eklendi: toplam 52 replacement, tekrar kullanım adetleriyle 57 görünür metin kullanımı. Raw override ağacı yedi asset içerir.

506 LOCKED karşılığın hiçbiri değiştirilmedi. Mevcut Research/Araştır eylemi, gerçek `researchTree.lua` düğme alanına bağlı bir bağlam istisnası ve TM varyantıyla açık hale getirildi. Lua metinleri artık ayrı, zayıf bir kontrol grubunda değil; gerçek literal içerikleriyle ortak LOCKED ve çeviri belleği denetimine girer.

Geriye dönük kontrol sırasında eksik olduğu görülen KheAA Router ve statWindow çevrimdışı şablonları tamamlandı. Yeni Mech şablonu da pinned kaynaktan üretilir. Full-source build, raw/runtime blob SHA'larını orijinal baytlarla ve yedi şablonun tamamını üretilen içerikle karşılaştırır. Eksik ya da eski şablon artık sessizce geçmez.

Mevcut on dekoratif kontrol-token istisnası korunarak tam satıra bağlandı; beş zemin etiketiyle toplam 15 bound exception bulunur. Gerekçesiz/global `allow_control_fix` tek başına yeterli değildir.

## Test kapsamı

152 Python test yöntemi: önceki 127 test korunur, 25 yeni yöntem eklenir. Bu sayıya dahil Lua testleri 14 yazı animasyonu ve 8 yakıt davranış senaryosu yürütür; yedi raw Lua dosyasını ayrıca derler. Alt senaryolar 152 sayısına tekrar eklenmez.

Yerel kontrol: compileall, tüm unittest paketi, qa_integrity, kaynak indirmeden build ve git diff --check. GitHub PR/main akışları ayrıca gerçek pinned FU checkout'u, v0.45 layered görev kaynakları, full-source build ve yeni üretilmiş Lua üzerinde davranış testlerini çalıştırır. Main yayın adımı ZIP bütünlüğünü, katalog/paket sayımlarını ve install-tree parity sonucunu evidence dosyasına yazar.

Yerel no-source build'in sonucu pinned-source doğrulaması diye sunulmaz. Son yayımlanmış paket için gerçek CI sonucu evidence dosyasından okunmalıdır.

## Kalan sınırlar

GitHub `main` branch protection / required status checks ayrı sunucu ayarıdır. Bu bakım workflowları ekler; sunucuda merge kurallarını zorunlu hale getirdiği iddia edilmez. Bu bağlantıda koruma ayarını yazacak işlem bulunmadığından ayar değiştirilmedi. Yapılandırılırken generated yayın botunun meşru yazma akışı korunmalıdır.

Oyun içi LQA: **NOT TESTED**. Lua davranış testleri minimal Starbound API taklitleri kullanır; font, satır taşması, gerçek oyun sürümü ve diğer modlarla uyumluluk onayı değildir. Hedefli kontrol listesi: [`LQA_CHECKLIST.md`](LQA_CHECKLIST.md).

Mech panelindeki diğer dinamik İngilizce metinlerin tamamı bu küçük hata paketinde çevrilmedi; yalnız denetimdeki iki uyarı kapatıldı. Kalan review/Lua havuzu ayrı kapsamdır. 8.024 satırın tamamına insan eliyle anlam/LQA onayı verilmiş sayılmaz.
