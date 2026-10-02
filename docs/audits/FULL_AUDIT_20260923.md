# 23 Eylül 2026 depo denetimi

İncelenen başlangıç: `3f54a6900de2ffa75e24f5cc2ec9306e6172d033`.
FU kaynağı: `329e714b3fe87571055c8ad7aa38135d199d3317`, sürüm 6.5.8.

## Bulgular ve düzeltmeler

| Öncelik | Bulgu / etkisi | Uygulanan düzeltme |
|---|---|---|
| P1 | `build_validate.py`, v0.46 dışındaki eksik base assetleri `layered_source` bayrağıyla atlıyordu. Hatalı kaynak metni olan bir yama statik build'den geçebiliyordu. | FU patch'ine bağlı 120 alanın tamamı exact kaynak değerine bağlandı. Kaynak `test` değerleri sayılmaz; son parent değişikliği eski değeri geçersiz kılar. |
| P1 | Paket kanıtı yalnız ana katalog hash'ini bağlıyordu; kural/validator değişikliğinden önceki rapor yeniden kullanılabiliyordu. Yerel raporun commit'i `null` olabiliyordu. | Tüm Python/JSON/Lua girdileri ve terminoloji hash'lenir; gerçek Git HEAD kaydedilir. Commit edilmemiş, eski veya kimliksiz raporla paketleme reddedilir. |
| P2 | Genel `allow_color_fix` ve `allow_number_fix` bayrakları ilgisiz renk/sayı kaybını da geçirebiliyordu. | Mevcut 18 renk ve 20 sayı düzeltmesi asset/pointer/en/tr/gerekçeye bağlandı; bayrak tek başına geçiş sağlamaz. |
| P2 | Liste ve `translations` biçimindeki manifestlerin ana katalogla kaynak/pointer eşleşmesi genel kontrolde zorunlu değildi. | Tüm manifest şemalarında asset/pointer/en/tr eşitliği, alan varlığı ve tekillik zorunlu. |
| P2 | FU kaynak kontrolü untracked/ignored dosyaları dışlıyordu; tarayıcı ise okuyabiliyordu. | Kaynak checkout kökü doğrulanır; ek dosyalar reddedilir. |
| P2 | Tarayıcı patch `test` değerlerini çeviri adayı sayıyor, aynı alanın eski base değerini tutabiliyordu. Lua'da Unicode'u bozuyor ve `display_en` açıklamasına güveniyordu. | Yalnız add/replace değerleri; patch değerine öncelik; gerçek Lua literal çözümlemesi ve görünür manifest slotları. |
| P2 | Windows'ta sekiz test UTF-8 dosyalarını varsayılan kod sayfasıyla okuyamıyor, Lua kitaplığı bulunamıyordu. CRLF checkout/build baytları Linux paketiyle eşleşmiyordu. | Açık UTF-8, LF checkout/üretim, Lua 5.4 Lupa alternatifi ve Windows PR test işi. |
| P2 | Kurulum belgesi silinmiş v0.30 paketine yönlendiriyor; eski klasörün üzerine kopyalama kaldırılmış yamaları bırakabiliyordu. | Kanonik README/evidence yönlendirmesi ve temiz yükseltme. |
| P3 | QA özeti ve checkpoint eski verileri güncel başlığı altında sunuyor; kaynak belgesi Lua davranış değişikliklerini belirtmiyordu. | Tarihsel kayıt ayrımı, güncel checkpoint ve dağıtılan raw override kapsamının açıklanması. |
| P3 | Kapsam workflow'u kullandığı kural yükleyici ve Lua ayrıştırıcı değiştiğinde çalışmıyordu. | İki bağımlılık tetikleyiciye eklendi. |

## Doğrulama

- Windows / Python 3.14.5: **180 test PASS**. Başlangıç koşusunda 166 test çalışmış, 9 hata oluşmuştu (8 UTF-8, 1 eksik Lua sınıf kurulumu); üç Lua testi o koşuda başlayamamıştı.
- Gerçek Lua 5.4: 14 yazı animasyonu ve 8 Mech yakıt senaryosu; yedi raw Lua dosyasında syntax kontrolü PASS.
- Full pinned-source build: **8.323 structured alan, 2.395 patch, 7 raw asset, 57 raw metin kullanım yeri** PASS.
- Kaynak kapsamı: **8.149 doğrudan FU alanı + 120 FU patch alanı + 54 harici ledger alanı**. Son grup bağımsız vanilla oyun dosyalarından bu denetimde yeniden doğrulanmadı.
- v0.45 / v0.46 / v0.47 exact-source kapıları PASS.
- Mevcut ZIP CRC/envanter/bayt kontrolü PASS; yeniden üretilen mod ağacı yayımlanmış mod ağacıyla bayt bazında aynı. Oyuncuya giden çeviri metinleri ve sürüm bu bakımda değişmedi.
- Çeviri kataloğu, sürüm manifestleri, 529 LOCKED terim, kontrol kodları, sayılar, placeholder'lar, raw source pinleri ve şablon eşleşmeleri denetlendi. Kod/CI/kurulum akışları elle incelendi; bu bütün metinlerin satır satır dil editörlüğü yapıldığı anlamına gelmez.

## Açık sınırlar

- **Oyun içi LQA: NOT TESTED.** Starbound içinde font, taşma, ekran bağlamı ve oynanış zinciri doğrulanmadı.
- Çeviri kapsamı tamamlanmış değildir. Kalan içerik otomatik kapsam raporuyla ayrı izlenir; bu bakım yeni çeviri kampanyası değildir.
- Raw Lua override'ları sabitlenmiş FU 6.5.8 kaynağına bağlıdır. Başka FU sürümüne uyumluluk otomatik garanti edilmez.
- Kapsam tarayıcısı şema/heuristic adaylarını sayar. Koşullu patch dalları, silmeler, diğer modların birleşimi ve bütün dinamik Lua metinleri için tam runtime çözümlemesi yapmaz.
- GitHub API kontrolünde `main` için **protected: false** görüldü. Branch protection/required checks sunucu ayarı değiştirilmedi; mevcut generated yayın botunun push yetkisiyle birlikte yapılandırılmalıdır. Bir workflow'un bulunması zorunlu merge kontrolü anlamına gelmez.
- Yeni dağıtım paketi/evidence `main` yayın workflow'u tarafından üretilmelidir; generated dosyalar bakım PR'ında elle güncellenmez.
