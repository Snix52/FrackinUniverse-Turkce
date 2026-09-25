# FU Session Checkpoint

## Güncel çalışma
24 Eylül 2026: v0.65.0-beta için codex/documents kapsamındaki doğrulanmış görünür kodeks belge alanları çevrildi: 331 alan / 47 asset / 312 benzersiz kaynak metin. Katalog v0.64.0-beta'deki 13.622 alanı koruyarak 13.953 alana çıktı. Önceki Codex metinleriyle birebir TM eşleşmesi bulunmadı. Aday codex/luna-v065 dalında yerel; Sol incelemesi, QA, build ve yayın bekliyor. Bu çalışmada test, QA, source gate veya build çalıştırılmadı.
24 Eylül 2026: v0.63.2 runtime yama denetimi. Pinli FU kaynağının ham değerleri ile katalog karşılaştırıldığında 802 çok satırlı assetin 1.606 alanlık düz yaması LF/CRLF farkıyla atlanabiliyordu; bir SAIL alanı ve üç karışık satır sonlu açıklama da tespit edildi. FU'nun kendi yamalarının değiştirdiği altı açıklama (yağ, Tech Konsolu, Böcek Ağı, çakıl, portakal, Erimiş Çekirdek) eski vanilla değeri beklediği için altı kısa adla birlikte uygulanmıyordu. Altı açıklamanın Türkçesi ve kaynak dayanağı düzeltildi. Tüm alanlar bağımsız koşullu yamaya çevrildi; ham pinli kaynak ve FU katmanı üzerinde gerçek uygulama build kapısı eklendi. Kalan 49 vanilla alan kurulu `packed.pak` ile eşleşiyor. Ayrıntı: `docs/RUNTIME_PATCH_AUDIT_20260924.md`. Yerel tam kaynak build ve 203 test PASS; GitHub paketi ve yayın bekliyor.

24 Eylül 2026: v0.63.1 karakter oluşturma runtime düzeltmesi hazırlandı. Eski karakter ekranı yaması, FU'nun zorlu mod açıklamasını değiştirmesi yüzünden 19 alanı birden sessizce atlıyordu; alanlar bağımsız test gruplarına ayrıldı ve açıklama doğru FU kaynağına göre düzeltildi. Steam FU paketindeki CRLF ile pinli Git kaynağındaki LF farkı Avian dahil 10 çok satırlı tür açıklamasını atlıyordu; iki biçim kaynak-kilitli alternatifler olarak desteklendi. Oyun içi kontrol: `IRK` ve Avian/Fenerox/Thelusian açıklamaları Türkçe; son kısaltılmış zorlu mod metni 800×630 pencerede sığıyor. CI paket kanıtı doğrulayıcısı koşullu grupları doğrulayacak şekilde yenilendi. Görsele işlenmiş İngilizce başlık ile katalog dışı türe özgü özelleştirme etiketleri ayrı kaldı. Ayrıntı: `docs/CHAR_CREATION_RUNTIME_20260924.md`. İkinci CI doğrulaması bekliyor.

24 Eylül 2026: v0.63.0-beta kök yiyecek ve `tier1` adayındaki 259 benzersiz kaynak metin Sol tarafından incelendi. 37 farklı çeviri metni, 37 alanda düzeltildi. `Madness Gain` mevcut LOCKED karşılığı olan `Delilik Kazanımı` biçimine getirildi ve cümle içi denetimi açıldı; `Cherry` → `Kiraz` kilitlendi. Anlam ve sayı kayması olan açıklamalar düzeltildi. Kök dosyalar ile `tier1` kapsamı 261 alan / 142 asset / 259 kaynak olarak pinli kaynak kapısında doğrulandı; daha derin yiyecek alt klasörlerindeki 168 görünür alan sonraki kapsama bırakıldı. FU'nun vanilla tabanlı 23 `tier1` alanı katmanlı kaynak kanıtına bağlandı. Statik QA, tam kaynak build (13.454 alan / 4.546 patch asset / 7 raw asset / 57 raw metin), 195 birim testi ve build çıktısında 3 Lua davranış testi PASS. GitHub yayını ve paket kanıtı doğrulaması sürüyor; oyun içi LQA yapılmadı.
24 Eylül 2026: v0.63.0-beta yerel yiyecek çevirisi adayı hazırlandı. `items/generic/food/**` içindeki doğrulanmış görünür ad/açıklama alanları 261 alan / 142 varlık / 259 benzersiz kaynak metin olarak çevrildi; iki tam kaynak TM karşılığı korundu. Katalog 13.454 alana güncellendi. Pinli FU 6.5.8 kaynağı `bb58383c0d16c1152e3439e606b39ff82288b586`; tam kaynak kapısı CI’a eklendi. Aday kaynak kapısı, test, QA, build ve yayın bu aşamada çalıştırılmadı; Sol incelemesi bekleniyor.
24 Eylül 2026: v0.62.0-beta Mech parçası adayındaki 248 benzersiz kaynak metin Sol tarafından incelendi. 100 farklı çeviri metni, 123 alan boyunca düzeltildi. Kilitli `Mech`, `Moderate Radiation` ve `Moderate Cold` karşılıkları uygulandı; beş İngilizce kalmış hareket birimi açıklaması çevrildi. v0.62 kaynak kapısı, kaynakta `mech` geçen aday alanlarında `Mech` yazımını da doğruluyor. FU'nun vanilla tabanlı 38 parça patch dosyasındaki 39 alan katmanlı kaynak kanıtına bağlandı. Pinli kaynak kapısı, statik QA ve tam kaynak build geçti: 13.193 alan / 4.404 patch asset / 7 raw asset / 57 raw metin. 195 birim testi ve build çıktısında 3 Lua davranış testi geçti. GitHub yayını ve paket kanıtı doğrulaması sürüyor; oyun içi LQA yapılmadı.
24 Eylül 2026: v0.62.0-beta yerel aday paketi hazırlandı. `items/generic/mechparts/` içindeki görünür ad ve açıklamalardan 295 alan / 166 asset / 248 benzersiz kaynak metin çevrildi. `/category` alanlarındaki `mechPart` oyun kodları çevrilmeden kapsam dışında bırakıldı. `Lunari` ve `Densinium` terimleri korundu; Sol incelemesi, QA, build ve yayın bekliyor.
24 Eylül 2026: FU upstream `master` commit `bb58383c0d16c1152e3439e606b39ff82288b586` incelendi. 6.5.8 etiketi `329e714b3fe87571055c8ad7aa38135d199d3317` sonrasında 3 commit / 12 dosya değişmiş; `.metadata` sürümü 6.5.8 kalmıştır. Dört görünür `/shortdescription` alanında yalnız İngilizce büyük harf düzeltmesi var ve dördü de mevcut katalogda çevrilmemişti; diğer sekiz dosyada teknik parametre temizliği var. Eski ve yeni kaynak auditleri aynı sonucu verdi: 45.517 doğrulanmış kalan alan / 10.499 asset; 4.331 review alanı / 620 asset; 165 Lua inceleme literal'i / 33 asset. Ek çeviri borcu 0, mevcut Türkçe cümle değişikliği 0. Kaynak pini ve manifest provenance yeni commit'e taşındı; doğrulama ve yayın durumu `dist/build-evidence.json` üzerinden kontrol edilir. Ayrıntı: `docs/FU_UPSTREAM_20260924.md`.
24 Eylül 2026: v0.61.0-beta kafe/fast-food/pazar/suşi barı adayında Sol incelemesi yapıldı. 375 benzersiz kaynak metin tarandı; 15 farklı çeviri cümlesi (15 alan) anlam, karakter sesi ve terminoloji için düzeltildi. Trixie'nin Burger Fool kurucusunun evcil hayvanı olduğu açıklaştırıldı; Cupcake/Küçük Kek ile altı yinelenen özel ad LOCKED olarak eklendi ve terminoloji belgesi yenilendi. Pinli v0.61 kaynak kapısı 399 alan / 48 asset / 375 kaynak için PASS; statik QA ve pinli tam kaynak build PASS (12.898 alan / 4.238 patch asset / 7 raw asset / 57 raw metin). Proje sanal ortamıyla 195 birim testi ve build çıktısında 3 Lua davranış testi PASS. GitHub CI, ZIP ve doğrudan main yayını bu kaydın yazıldığı anda bekliyor; oyun içi LQA yapılmadı.
24 Eylül 2026: v0.61.0-beta yerel çeviri adayı hazırlandı. Kafe, fast-food, pazar ve suşi barı dekoratif nesneleri kapsamı 399 alan / 48 asset / 375 benzersiz kaynak metin içeriyor; önceki katalog TM eşleşmesi çıkmadı. Sol incelemesi, QA, build ve yayın bekleniyor.
24 Eylül 2026: v0.60.0-beta Kadim ve Precursor mini-biome adayı Sol incelemesinden geçti. Kapsam 536 alan / 196 asset / 314 benzersiz kaynak metin; üç değer yayımlanmış Translation Memory karşılığından tekrar kullanıldı. Kaynak/çeviri kontrolü, QA ve pinli build başarılı; doğrudan `main` yayını hazırlanıyor.
24 Eylül 2026: `Precursor` zaten LOCKED olmasına karşın tek sözcüklü terimler
QA'nın cümle içi kontrolünden geçmiyordu. Terime özgü `enforce_in_text`
denetimi eklendi; kaynakta `Precursor` geçen ad ve cümlelerde özel adın
korunması ve `Öncül` varyantının reddi artık zorunlu. v0.59 çeviri metinleri
değişmedi; bu sürümde eklenen bakım yalnız QA kuralı ve testidir.
24 Eylül 2026: v0.59.0-beta kalan görünür canavarlar ve beceri adları Sol incelemesinden geçti.
Kapsam 341 alan / 259 asset / 260 benzersiz kaynak metin; üç metin mevcut TM'den
alındı. Test/debug yaratıkları, dahili spawn seçicileri ve iki görünmez script
yardımcısı dışarıda tutuldu. Kaynak/çeviri kontrolü, QA ve pinli build başarılı;
doğrudan `main` yayını hazırlanıyor.
24 Eylül 2026: v0.58.0-beta kalan yaratık aileleri çeviri adayı yerelde hazırlandı.
Kapsam 522 alan / 261 asset / 257 benzersiz kaynak metin; üç metin önceki TM
karşılıklarından kullanıldı. Sol kaynak/çeviri kontrolü, QA ve pinli FU kaynak
build'i tamamlandı; doğrudan `main` yayınına hazırlandı.
23 Eylül 2026: v0.54.0 Honey ailesi yapı malzemeleri yerel doğrulaması tamamlandı; yayımlanmış paket durumu `dist/build-evidence.json` içindedir.
v0.49.0 main dalına alındı. Teknik depo denetimi ayrıntıları:
`docs/FULL_AUDIT_20260923.md`. Oyun içi LQA tamamlandığı iddia edilmez.
Yeni çeviri paketlerinde varsayılan hedef yaklaşık **500 alan / 250–400 benzersiz kaynak metin**; tekrarlı ve tutarlı ailelerde **800–1000 alan** olabilir. v0.54 küçük kapsamı bu kural öncesinde hazırlanmış adaydır; boyut politikası sonraki paketlerden uygulanır. Ayrıntı: [`docs/TRANSLATION_BATCH_POLICY.md`](docs/TRANSLATION_BATCH_POLICY.md).
Kaynak sürüm: `tools/ceviriler.json`. Yayımlanmış son paketin gerçek sürümü, kaynak commit'i, CI run'ı, SHA-256 ve PASS durumu için tek referans: [`dist/build-evidence.json`](dist/build-evidence.json).
Bu checkpoint bir build kanıtı kopyası değildir; v0.42-v0.50 sürüm sonuçları ve
"Sonraki başlangıç noktası" bölümleri tarihsel kayıtlardır.

23 Eylül 2026: v0.57.0-beta walker ve flyer canavar çeviri adayı yerelde hazırlandı.
Kapsam 477 alan / 239 asset / 344 benzersiz kaynak metin; bir değer mevcut katalog
TM'sinden tekrar kullanıldı. Altı test varlığının debug alanı adaydan çıkarıldı.
Sol kaynak/çeviri kontrolü, QA, paket build'i ve yayın bekleniyor.

Pinned FU: `sayterdarkwynd/FrackinUniverse` @ `bb58383c0d16c1152e3439e606b39ff82288b586` (6.5.8).

## v0.42 tamamlanan kapsam
- Structured: **260 alan / 46 asset / 82 benzersiz kaynak metin**
- Pet House:
  - `fu_pethouse.config`: 16 alan
  - `fu_pethouse_confirmation.config`: 5 alan
  - `fu_pethouse.lua`: 1 source-locked görünür Lua parçası
- Windowconfig: **44 runtime-bağlı panel / 239 alan**
- v0.42 toplam katkı: **261 görünür metin birimi**

## Runtime doğrulaması
- 34 üretim/tezgâh configi gerçek nesne veya upgrade patch referansıyla doğrulandı.
- 10 dükkân configi gerçek nesne referansıyla doğrulandı.
- Pet House ana configi `fu_byospethouse.object` ve `newSail/fu_customFunctions.lua` tarafından kullanılıyor.
- Pet House confirmation ve Lua bağlantıları ana configten doğrulandı.

## Bilinçli kapsam dışı
Runtime referansı bulunmayan:
- `interface/windowconfig/craftingmech.config`
- `interface/windowconfig/extractionlab.config`
- `interface/windowconfig/fruitpress.config`
- `interface/windowconfig/kitchen.config`
- `interface/windowconfig/powerpress.config`
- `interface/windowconfig/samplingarray2.config`
- `interface/windowconfig/xenostation.config`

## Teknik/terminoloji kararları
- Pet House popup ve interactionType alanları audit'in otomatik havuzunda olmasa da Lua tarafından canlı gösterildiği için dahil edildi.
- `groundPet.lua`, `techstation`, `shipPetType`, mod adı `Purchasable Pets` gibi teknik referanslar korunur.
- `Buy`: Takas Et / Satın Al / İşe Al bağlamları Translation Memory'de açıkça ayrılır.
- Craft → **Üret**
- Forge → **Döv** (eylem); Forge nesne adı → **Dövme Ocağı**
- Smelt → **Ergit**
- Distill → **Damıt**
- Ferment → **Fermente Et**
- Mash bağlama ayrılır:
  - ürün/kavram → **Mayşe**
  - Mayşeleme Kazanı eylemi → **Mayşele**
  - Meyve Presi eylemi → **Ez**
- Bağlı nesne adlarıyla panel başlıkları eşitlendi.

## Doğrulama sonucu
Feature/fix zinciri:
- `81085dd` - v0.42 işlevsel arayüzler + Pet House
- `8984600` - Forge eylem bağlamı
- `27ec3f0` - v0.42 regresyon testindeki syntax düzeltmesi
- `424b615` - Mash bağlam ayrımı
- `995e701` - doğrulanmış build/package refresh

Build evidence:
- translation version: **0.42.0-beta**
- structured fields: **7.725**
- patch assets: **2.182**
- raw override assets: **6**
- raw script strings: **55**
- static QA: **PASS**
- pinned source validation: **PASS**
- ZIP integrity: **PASS**
- install-tree parity: **PASS**
- package: `dist/FU_Turkce_v0.42.0_Beta.zip`
- package sha256: `932c4dcf5399d1a527edddbb9c2e3329e2f376c1a33e1322987bd0b4fe061969`
- oyun içi LQA: **NOT TESTED**

## v0.42 sonrası audit
Kalan doğrulanmış **Arayüz** kapsamı:
- **95 asset**
- **347 alan**
- **200 benzersiz kaynak metin**

Genel audit:
- kalan doğrulanmış kapsam: **13.103 asset / 51.563 alan**
- review havuzu: **599 asset / 4.496 alan**
- Lua inceleme havuzu: **35 asset / 171 literal**

## Sonraki başlangıç noktası
v0.43 için yalnız kalan **Arayüz** havuzundan devam et.
Repo çapında yeniden keşif yapma; bu checkpoint ve son Remaining Scope Audit sonuçlarından devam et.
Oyun içi LQA ayrı bir aşamadır.


## v0.43 feature kapsamı
- Kalan Arayüz havuzundan runtime bağlantısı doğrulanan: **69 asset / 257 alan / 156 benzersiz kaynak metin**
- Kapsam dışı bırakılan şüpheli/artık grup: **26 asset / 90 alan**
- CDX chest ailesi tekil string referansı yerine aile/pattern kullanımıyla canlı kabul edildi.
- Doğrudan runtime kanıtı bulunmayan eski/fallback/dev adayları bu sürüme zorla alınmadı.
- `Repair` bağlama ayrıldı: gemi sınıfı **Onarım Gemisi**, araç onarım düğmesi **Onar**.
- `Buy` corpse wagon panelinde gerçek satın alma eylemi olarak **Satın Al**.
- `Racialise` eylemi kilitli **Irk Dönüştürücü** nesne adıyla uyumlu biçimde **Irka Dönüştür**.
- `<^yellow;Loading...^reset;>` görünür dekoratif UI metnidir; **Yükleniyor...** olarak çevrildi ve yalnız bu satır için belgeli kontrol-token QA istisnası kullanıldı.
- Oyun içi LQA: **NOT TESTED**

## v0.43 doğrulama sonucu
Feature/fix zinciri:
- `c8baefc` - v0.43 canlı arayüz paketi
- `03d911a` - `Request All-1` işaretli sayı düzeltmesi
- `d492e4b` - Mech assembly layered-source doğrulaması
- `b259cd5` - işaretli sayı regresyon testi düzeltmesi
- `f11154b` - MM upgrade layered-source doğrulaması
- `6da59bb` - doğrulanmış build/package refresh

Build evidence:
- translation version: **0.43.0-beta**
- structured fields: **7.982**
- patch assets: **2.251**
- raw override assets: **6**
- raw script strings: **55**
- static QA: **PASS**
- pinned source validation: **PASS**
- ZIP integrity: **PASS**
- install-tree parity: **PASS**
- package: `dist/FU_Turkce_v0.43.0_Beta.zip`
- package sha256: `5ac74d7551570778a0031e3a58891369729a3aa35dd1b2c7e996eeebecd3c8d5`
- Build & QA run: **35695710269 / SUCCESS**
- Remaining Scope Audit run: **35695710287 / SUCCESS**
- oyun içi LQA: **NOT TESTED**

## v0.43 sonrası audit
Kalan doğrulanmış **Arayüz** kapsamı:
- **26 asset**
- **90 alan**
- **58 benzersiz kaynak metin**

Genel audit:
- kalan doğrulanmış kapsam: **13.034 asset / 51.306 alan**
- review havuzu: **599 asset / 4.496 alan**
- Lua inceleme havuzu: **35 asset / 171 literal**

## Sonraki başlangıç noktası
v0.44 için yalnız kalan **26 asset / 90 alanlık Arayüz artık havuzunu** ele al.
Bu 90 alanı körlemesine çevirmeden önce runtime/fallback/dev ayrımını tamamla.
Repo çapında yeniden keşif yapma; v0.43 final audit ve bu checkpoint'ten devam et.
Oyun içi LQA ayrı bir aşamadır.


### v0.43 CI düzeltmesi
- İlk regresyon koşusu `Request All-1` içindeki `-1` işaretli sayısının Türkçede kaybolduğunu yakaladı; **Tümünü İste -1** olarak düzeltildi.
- Tam pinned-source QA, `mechassemblygui.config` hedefinin FU ağacında tam dosya değil `mechassemblygui.config.patch` katmanı olduğunu yakaladı.
- İlgili 3 alan layered-source olarak işaretlendi ve pinned patch blobu `cde45dd1767885e222158d75eb96c024139e7237` ile provenance kaydına bağlandı.


- Audit origin çapraz kontrolünde 257 v0.43 alan içinde katmanlı kaynağa sahip yalnız iki asset bulundu: `mechassemblygui.config` ve `mmupgradegui.config`. Başka seçili layered asset yok.
- `mmupgradegui.config` içindeki 3 alan etkisi açıklaması pinned `mmupgradegui.config.patch` blobu `8b1c6b1c98a802d89129d164f0b376ecab0b1de2` ile source-lock altına alındı.


## v0.44 feature kapsamı
- v0.43 sonrası kalan Arayüz: **26 asset / 90 alan / 58 benzersiz kaynak metin**.
- Runtime doğrulaması sonunda gerçek canlı kapsam: **7 asset / 13 alan / 12 benzersiz kaynak metin**.
- `chest3.config`, gerçek `slotCount: 3` nesnelerin `/interface/chests/chest<slots>.config` bağıyla canlıdır.
- Atmospheric Filter yalnız `slotCount: 1` kullandığı için `fu_atmosfilter1.config` canlıdır.
- `fu_warped1.config` ve `fu_warped3.config`, gerçek 1/3 slotlu nesnelerin `fu_warped<slots>.config` bağıyla canlıdır.
- `interface/stats/stats.config` pinned `stats.config.patch` katmanından gelir; 4 stat etiketi çevrildi.
- MetaGUI `frackin` ve `frackin.v2` temaları registry üzerinden canlıdır; ad ve açıklamaları çevrildi.
- **19 asset** runtime-inaktif/superseded olarak audit confirmed kapsamından çıkarıldı.
- Stats patch içindeki dört `-todo-` açıklaması geliştirici placeholder'ıdır; çeviri borcu sayılmaz.
- Oyun içi LQA: **NOT TESTED**.

## v0.44 doğrulama sonucu
Feature/fix zinciri:
- `8ec662c` - v0.44 Arayüz artık havuzu kapanışı
- `6854d07` - v0.43 tarihsel katalog sürüm testini ileri uyumlu yap
- `3efd535` - doğrulanmış build/package refresh

Build evidence:
- translation version: **0.44.0-beta**
- structured fields: **7.995**
- patch assets: **2.258**
- raw override assets: **6**
- raw script strings: **55**
- toplam yerelleştirilmiş görünür birim: **8.050**
- static QA: **PASS**
- pinned source validation: **PASS**
- ZIP integrity: **PASS**
- install-tree parity: **PASS**
- package: `dist/FU_Turkce_v0.44.0_Beta.zip`
- package sha256: `c50ee3f95c3ca04dbd380fe4796508c072758dfb020172a2fd060aa1abc2e769`
- Build & QA run: **35697423309 / SUCCESS**
- Remaining Scope Audit run: **35697316152 / SUCCESS**
- oyun içi LQA: **NOT TESTED**

## v0.44 sonrası audit
Kalan doğrulanmış **Arayüz** kapsamı:
- **0 asset**
- **0 alan**

Genel audit:
- kalan doğrulanmış kapsam: **13.008 asset / 51.216 alan**
- review havuzu: **588 asset / 4.438 alan**
- Lua inceleme havuzu: **35 asset / 171 literal**

Arayüz kategorisinin otomatik confirmed borcu kapanmıştır. Review havuzu ve Lua literal havuzu ayrı iş sınıflarıdır; bunlar Arayüz confirmed kapsamına geri eklenmez.

## Sonraki başlangıç noktası
v0.45'te Arayüz confirmed havuzuna geri dönme.
Proje öncelik sırasına göre sıradaki yüksek değerli alan **Görevler**dir: auditte **101 asset / 368 doğrulanmış alan** kalıyor.
Çalışma protokolü gereği 368 alan tek turda alınmayacak; ilk runtime-bağlı görev paketi **250-300 alanı geçmeyecek** biçimde ayrılmalıdır.
Oyun içi LQA ayrı bir aşamadır.


## v0.45 görev kapsamı
- v0.44 checkpointinde Görevler için audit başlangıç sayımı **101 asset / 368 alan** görünüyordu.
- Kök neden incelemesinde `audit_remaining.py` aracının iki mevcut runtime kuralını uygulamadığı bulundu:
  - `V020_INACTIVE_QUEST_ASSETS`
  - `NONVISIBLE_QUEST_ASSETS`
- Bu iki audit kaçağı düzeltildi; görev raporuna tam `quest_confirmed_rows` listesi eklendi.
- Düzeltilmiş gerçek kalan Görev kapsamı: **18 asset / 29 alan / 29 benzersiz kaynak metin**.
- 29 alanın tamamı vanilla görev hedeflerine FU'nun pinned `.questtemplate.patch` katmanıyla eklediği/değiştirdiği canlı oyuncu metnidir.
- Her v0.45 satırı `qa.layered_source` + `qa.source_patch` ile kaynak patchine bağlandı.
- Build workflowuna `python tools/generate_v045.py --source fu_source` exact-source doğrulaması eklendi.
- Terminoloji:
  - FTL Drive -> **FTL Motoru**
  - STL Drive -> **STL Motoru**
  - Machining Table -> **İmalat Tezgâhı**
  - Engineering -> **Mühendislik**
  - Power Core -> **Güç Çekirdeği**
  - Carbon Plate -> **Karbon Plaka**
  - Advanced Circuit -> **Gelişmiş Devre**
  - Distortion Sphere -> **Çarpıtma Küresi**
  - Upgrade Module -> **Yükseltme Modülü**
  - Station Transponder -> **İstasyon Transponderi**
  - Kestrel/Falcon/Eagle/Condor özel sınıf adları korunur; **Lisansı** Türkçeleştirilir.
  - Pulse Jump -> **Enerji Sıçraması**. Tech adı oyuncu işlevine göre yerelleştirilir; daha önce onaylı karşılığın bulunmaması İngilizce bırakma gerekçesi değildir.
- Oyun içi LQA: **NOT TESTED**.

## v0.45 doğrulama sonucu
Feature/fix zinciri:
- `c5c5a53` - görünmez görevleri audit kapsamından çıkar
- `025946b` - runtime-inaktif görevleri audit kapsamından çıkar
- `aa3a335` - görev confirmed satırlarını audit raporuna ekle
- `cfbb01c` - v0.45 kalan görev metinlerini kapat
- `b5974d7` - doğrulanmış build/package refresh

Build evidence:
- translation version: **0.45.0-beta**
- structured fields: **8.024**
- patch assets: **2.276**
- raw override assets: **6**
- raw script strings: **55**
- toplam yerelleştirilmiş görünür birim: **8.079**
- static QA: **PASS**
- pinned source validation: **PASS**
- ZIP integrity: **PASS**
- install-tree parity: **PASS**
- package: `dist/FU_Turkce_v0.45.0_Beta.zip`
- package sha256: `ef426c4fac78f82113f469d6ec5599aebb427e6500bbaafad6541f722df5f9cb`
- Build & QA run: **35702963628 / SUCCESS**
- Remaining Scope Audit run: **35702963616 / SUCCESS**
- oyun içi LQA: **NOT TESTED**

## v0.45 sonrası audit
Kalan doğrulanmış **Görevler** kapsamı:
- **0 asset**
- **0 alan**

Genel audit:
- kalan doğrulanmış kapsam: **12.907 asset / 50.848 alan**
- review havuzu: **508 asset / 4.200 alan**
- Lua inceleme havuzu: **35 asset / 171 literal**

## Sonraki başlangıç noktası
v0.46 için temiz tek-paket adayı: **Irklar ve SAIL/AI**
- **167 asset**
- **262 doğrulanmış alan**
- **247 benzersiz kaynak metin**

Alan sayısı çalışma protokolündeki 250-300 bandına tam oturuyor. Çeviri öncesi species/raceeffect ile gerçek SAIL/AI görünür metinlerini runtime bağlamına göre ayır; teknik stat/ID alanlarını dahil etme.
Oyun içi LQA ayrı bir aşamadır.

## v0.45.1 bakım checkpoint'i
- Hedef: F01-F08 ana kontrol bulguları; v0.46 yeni içerik kapsamına başlanmadı.
- Raw metinlerde gerçek Lua stringleri ayrıştırılır. Yalnız `text_literals` ile belirtilen stringler değişebilir; callback, widget adı, teknik string, kod ve yorum değişikliği reddedilir.
- Raw yer tutucuları, renkler, sayılar, kaçışlar, kontrol kodları ve görünür metinler ortak terminoloji/çeviri belleğiyle kontrol edilir.
- Research düğmesi için yalnız gerçek Lua eylem alanına bağlı bağlam istisnası eklendi. 506 LOCKED terimin karşılıkları değiştirilmedi.
- Beş `[Tile]` görünür etiketi `[Zemin]` yapıldı. Mevcut 10 dekorasyon istisnası ve bu beş etiket asset/pointer/en/tr/gerekçeye bağlandı; genel allow_control_fix artık tek başına geçiş sağlamaz.
- Mech yakıtının dolu/uyumsuz depo uyarıları çevrildi. Bu paneldeki diğer dinamik metinler ayrı kapsamdır; tam panel kapanışı iddia edilmez.
- Üç görev ifadesi ve bir görevde cümle arası boşluk düzeltildi. 8.024 mevcut alan korunur; yalnız 9 structured hedef metin değişti. 2 raw metin eklendi: 57 kullanım yeri / 7 raw asset.
- Eksik KheAA Router ve statWindow çevrimdışı kaynak şablonları tamamlandı. Pinned build ile bütün raw şablonların eşleşmesi zorunlu.
- Testler: 152 Python test yöntemi; bunların içinde 14 yazı animasyonu ve 8 Mech yakıt davranış senaryosu gerçek Lua 5.4 ile yürütülür. Bütün raw Lua dosyaları syntax kontrolünden geçer.
- Değişen ana kaynaklar: qa_integrity.py, qa_raw.py, build_validate.py, raw manifest/şablonları, v039/v045 manifestleri, katalog, text_integrity politikası, dar bağlam kayıtları, testler, PR/main workflowları ve dokümantasyon.
- Generated çıktı elle değiştirilmez. Güncel paket ve pinned-source sonuçları için üstteki build-evidence bağlantısı esas alınır.
- Açık dış ayar: `main` için zorunlu PR/status rule yapılandırması bu bağlantının yazma araçlarıyla değiştirilemedi. CI işleri eklendi; GitHub sunucusunda zorunlu merge kuralı yapılandırıldığı iddia edilmez. Yayın botunun generated commit akışı korunarak ayrıca ele alınmalıdır.
- Oyun içi LQA: **NOT TESTED**. Tricorder zemin etiketleri, Mech yakıt uyarıları, SAIL harfleri ve düzeltilen görev ekranları odaklı kontrol bekler.
- Sonraki başlangıç: bu bakım paketinin build-evidence sürümünü kontrol et; ardından mevcut v0.46 Irklar ve SAIL/AI planından devam et. Ana kontrolü yeniden başlatma.


## v0.46 Irklar ve SAIL/AI kaynak kapanışı
- İlk audit havuzu: **167 asset / 262 confirmed alan / 247 benzersiz kaynak metin**.
- Runtime sınıflandırması sonrası çekirdek canlı kapsam: **53 asset / 129 alan / 127 benzersiz kaynak metin**.
  - SAIL/AI: **89 alan**
  - çekirdek oynanabilir species: **40 alan / 20 ırk**
- **105** üçüncü taraf oynanabilir ırk uyumluluk alanı çekirdek FU borcu sayılmadı; confirmed'dan review havuzuna taşındı.
- İki teknik false positive confirmed kapsamdan çıkarıldı:
  - `species/irken.raceeffect /envEffects/0/scripts/0/args/label`
  - `species/skelekin.raceeffect /liquidEffects/0/scripts/0/args/label`
- Çekirdek ırklar: Apex, Avian, Floran, Glitch, Human, Hylotl, Novakid, Fenerox, Shadow, Skath, Peglaci, Thelusian, Kirhos, X'i/Radien, Mantizi, Nightar, Eld'uukhar, Slimeperson, Vel'uu ve Pharitu/Juux.
- Tür özel adları mevcut terminolojiye göre korunur; oyuncuya gösterilen açıklama, beslenme, avantaj, direnç, bağışıklık, çevre, silah ustalığı ve zayıflık metinleri Türkçeleştirildi.
- SAIL/AI görev adları ve açıklamaları mevcut görev terminolojisiyle eşlendi; ör. **Sızma**, **Letheia Tesisi**, **Erchius Madencilik Tesisi**, **Bilim Karakolu**.
- v0.46 provenance satır bazında doğrulanır. Nightar gibi aynı asset içinde base + `.patch` kaynaklı alanlar ayrı ayrı pinned kaynağa bağlanır.
- QA sırasında yakalanıp düzeltilen iki format hatası:
  - Kirhos açıklamasında `%Fiziksel` printf gibi algılanıyordu; `% Fiziksel` yapıldı.
  - Vel'uu açıklamasında kaynakta olmayan `+13/+6` işaretleri kaldırıldı.
- Doğrulama runı **35747010234 / SUCCESS**:
  - **159/159** Python test yöntemi PASS
  - `qa_integrity`: **11.116 katalog birimi / 52 raw birim / 506 LOCKED terim**
  - v0.45 source gate PASS
  - v0.46 source gate: **129 alan / 53 asset / 127 kaynak / 54 kaynak dokümanı**
  - full pinned FU build PASS
  - Remaining Scope Audit PASS
  - **Irklar ve SAIL/AI confirmed borcu: 0 asset / 0 alan**
  - audit sonrası genel confirmed: **12.740 asset / 50.586 alan**
  - review: **620 asset / 4.331 alan**
  - Lua review: **35 asset / 169 literal**
- Test edilmiş kaynak commit: `a887a9647662318c6aa47939182c9516f3eb7150`. Kalıcı CI workflow güncellemeleri aynı çalışma dalında ayrıca eklendi; geçici v0.46 workflowları silindi.
- Generated çıktı elle değiştirilmedi. v0.46 paket/evidence değeri main merge ve yayın buildinden sonra `dist/build-evidence.json` ile kanonikleşecektir.
- Oyun içi LQA: **NOT TESTED**.

## v0.46.1 terminoloji bakım checkpoint
- Generic Jungle -> Tropik Orman LOCKED.
- Eski karşılık kaynak, manifest, test, dokümantasyon ve katalog katmanlarında geriye dönük temizlendi.
- Evernight Jungle gibi özel görev/konum adları korunur.
- Katalog sürümü 0.46.1-beta; structured alan sayısı değişmez: 8.153.
- Oyun içi LQA: NOT TESTED.

## v0.46.2 görev/konum adı denetim checkpoint
- Eski toplu "özel ad" varsayımı kaldırıldı.
- Çevrilen başlıklar: Kadim Tapınak, Su Dağıtım Merkezi, Evernight Tropik Ormanı, Fae Ormanı, Büyük Arena, Gigant Dağı, Yenilmez Kule, Yemyeşil Harabeler.
- Exact korunan kanıtlı referans/özel adlar: Brine Star, Snow Crash, Sunset Riders, Sky Boulevard, Techno City, Delta Freya II, Dantalion, Dreadwing.
- Takeshi's Castle exact dış referans olarak korunur; Castle Takeshi varyantı buna eşitlenir.
- Katalog sürümü: 0.46.2-beta.
- Oyun içi LQA: NOT TESTED.

## v0.46.3 Nightfort bakım checkpoint
- Oyuncuya görünen Nightfort adı **Gece Hisarı** olarak yerelleştirildi.
- SAIL: `Visit Nightfort` -> **Gece Hisarı'nı Ziyaret Et**.
- Teknik `nightfort` mission/world/dungeon kimlikleri aynen korunur.
- Katalog sürümü: 0.46.3-beta.
- Oyun içi LQA: NOT TESTED.

## v0.47 başlangıç: biome friendlyName audit düzeltmesi
- En güncel main auditinde **Biyom, zindan ve dünya sistemleri** kategorisi başlangıçta **1.028 asset / 2.240 confirmed alan** gösteriyordu.
- Dar v0.47 ilk grup olarak yalnız `biomes/` kökü incelendi: **288 asset / 288 alan / 276 benzersiz kaynak metin**.
- 288 alanın tamamı `/friendlyName` idi. FU kaynağında `extraskymission`, `extraoceanfloormission`, `extraswampmission` gibi teknik/dummy değerlerin de aynı alanda bulunması ve FU runtime kodunda bu metadata için görünür UI bağı bulunmaması nedeniyle oyuncu çeviri borcu sayılmadı.
- Starbound biome şemasındaki `friendlyName` normal oyun UI metni olarak doğrulanamadı; oyuncunun navigasyonda gördüğü gezegen/biyom adları ayrı cockpit/world metinlerinden geliyor.
- Audit politikası kör global `friendlyName` dışlaması yapmaz. Yalnız **`biomes/` prefix + `/friendlyName`** kombinasyonu `AUDIT_EXCLUDED_FIELDS` üzerinden dışlanır.
- `audit_excluded_candidate` klasör-prefix kurallarını destekleyecek biçimde genişletildi; başka asset ailelerindeki `friendlyName` alanları etkilenmez.
- Regresyon testi iki gerçek biome örneğini dışlar ve biome dışındaki `/friendlyName` alanının dışlanmadığını doğrular.
- Pinned FU 6.5.8 doğrulama runı **35759299914 / SUCCESS**:
  - `biomes/` confirmed: **0 asset / 0 alan**
  - Biyom, zindan ve dünya sistemleri: **740 asset / 1.952 confirmed alan**
  - genel confirmed: **12.452 asset / 50.298 alan**
  - review havuzu değişmedi: **620 asset / 4.331 alan**
- Bu tur çeviri eklemedi; paket sürümü **0.46.3-beta** olarak kalır.
- Sonraki dar başlangıç: aynı kategoride gerçek oyuncu metni olma ihtimali yüksek olan **plants + liquids** havuzunu ayrı turda sınıflandır. `tiles/` (641 asset / 1.763 alan) tek parçada ele alınmayacak.
- Oyun içi LQA: **NOT TESTED**.

## v0.47.0 bitkiler checkpoint
- İlk Plants + Liquids audit havuzu: **102 asset / 206 confirmed alan**.
- Runtime sınıflandırması:
  - **Plants:** 66 asset / 170 gerçek oyuncu metni
  - **Liquids:** 36 asset / 36 `/description` metadata false positive
- v0.47 manifesti: **170 alan / 66 asset / 110 benzersiz kaynak**.
- Bitki kapsamı: ad, açıklama, Floran ve Glitch inceleme replikleri.
- Liquid config açıklamaları audit confirmed kapsamından çıkarıldı; `items/liquids/*.liqitem` görünür metinleri ayrı ve etkilenmiyor.
- Katalog sürümü: **0.47.0-beta**.
- Beklenen structured toplam: **8.323**; patch asset: **2.395**.
- Beklenen audit sonrası Biyom/Zindan/Dünya confirmed borcu: **638 asset / 1.746 alan**.
- Beklenen genel confirmed borç: **12.350 asset / 50.092 alan**.
- Oyun içi LQA: **NOT TESTED**.

## v0.48 ahşap yapı malzemeleri
- İlk karo/zemin materyali grubu runtime görünürlüğü ve dosya ailesi üzerinden ele alındı; yalnız `tiles/materials/darkwood/`, `lightwood/` ve `treatedwood/` içindeki confirmed oyuncu alanları seçildi.
- **32 asset / 151 alan / 87 benzersiz kaynak metin**: ad, açıklama ve Floran/Glitch/Novakid inceleme metinleri.
- `tiles/materials/` alanları için build validator'a genel izin eklenmedi; yalnız v0.48 manifestindeki alanlara izin verilir.
- Yeni sabit terimler: Timber -> **Kereste**, Baseboard -> **Süpürgelik**, Window Lattice -> **Pencere Kafesi**, Shoji Screen Panel -> **Şoji Paravan Paneli**, Ornate Timber -> **Süslü Kereste**.
- v0.48 kataloğu: **8.474 structured alan**, **2.427 patch asset**, 7 raw asset. Yerel tam kaynak build ve 151/151 pinned source gate PASS.
- Oyun içi font/taşma ve gerçek kullanım LQA: **NOT TESTED**.
- Sonraki odak: diğer tiles/materials ailelerini alt gruplar hâlinde runtime ve terim bağlamıyla sınıflandır; 1.763 alanlık karo havuzunu topluca ekleme.

## v0.49 ahşap yapı malzemeleri
- v0.48 sonrasında kaynak/katalog karşılaştırmasında **44 asset / 227 alan / 174 benzersiz kaynak metin** kaldı; kapsam beş ilişkili ahşap ailesiyle sınırlandı: `aenwood`, `dollhouse`, `dynastwood`, `rawwood`, `weathered wood`.
- Taş, bal, biyom, pencere ve diğer karo aileleri bu pakete dahil edilmedi.
- Alanlar ad, açıklama ve Floran/Glitch/Novakid inceleme metinlerinden oluşur; tekrarlı ortak repliklerde v0.48 terminolojisi kullanılır.
- Yeni kilitli terimler: Aen (özel aile adı), Dollhouse -> **Oyuncak Ev**, Dynast (özel aile adı), Weathered -> **Yıpranmış**, Wood Plank -> **Ahşap Kalas**.
- Pinned source kapısı, katalog regresyonu, tam kaynak derlemesi ve CI sonuçları bu dalda doğrulanacak.
- Oyun içi font/taşma ve gerçek kullanım LQA: **NOT TESTED**.
- Sonraki adım: `tiles/materials/` dışındaki yüksek değerli Biyom/Zindan/Dünya alanlarından küçük, runtime-bağlı grup seç; tüm 1.595 alanı tek pakette alma.

## v0.50 arıcılık sistemi
- v0.49 kataloğunda henüz bulunmayan `bees/` görünür alanları: **537 alan / 207 asset / 308 benzersiz kaynak metin**.
- Arı türleri ve koloni rolleri, petekler, arılık çerçeveleri, eşya açıklamaları ve arıcılık arayüz etiketleri birlikte ele alındı.
- Ana Arı / Erkek Arı ve Bal Peteği kararları mevcut kilitli sözlükle eşlendi; özel tür adları korunarak işlevsel tür adları çevrildi.
- Pinned source gate, katalog/format testleri ve tam kaynak statik build: **PASS**; main CI sonucu bekleniyor.
- Yerel Lua davranış testi `lupa` olmadığı için çalıştırılamadı; CI Lua testi ayrıca çalıştıracak.
- Oyun içi font/taşma ve gerçek kullanım LQA: **NOT TESTED**.
- Sonraki adım: kalan biyom/zindan/dünya sistemleri kapsamından küçük, runtime-bağlı aile seç.


## v0.51 platformlar
- Pinned 6.5.8 auditinden `tiles/platforms/` içindeki **99 alan / 33 asset / 78 benzersiz kaynak metin** seçildi; katmanlı patch kaynakları da nihai değer önceliğiyle kapsama alındı.
- Platform adları, açıklamaları ve Floran/Glitch/Novakid incelemeleri çevrildi. Aen, Aether, Dynast, Precursor, Nightar, Tethyde, Telebrium ve Pykrete özel/malzeme adları korunur; Slime için kilitli Balçık kullanılır.
- `low impact` ifadesi görünmez platform dokusu/yerleşim bağlamıyla `göze batmayan` olarak yorumlandı; anlam tercihi gözden geçirilebilir. İnceleme sonrası Nightar/Novakid anlam hatası düzeltildi ve 11 Floran repliğinde karakter sesi korundu.
- Eski v0.50 kaynak kapısı ve testi, katalog sürümünü alt sınır olarak kabul edecek biçimde düzeltildi; v0.51 kapısı da sonraki sürümlerle uyumlu. v0.45-v0.51 kaynak kapıları ve **193 test** PASS.
- Pinned source gate PASS (**99 alan / 33 asset / 78 kaynak**); `qa_integrity.py` PASS (**13.484 katalog birimi / 52 raw birim / 542 LOCKED terim**). Statik build PASS (**9.337 alan / 2.703 patch asset / 7 raw asset / 57 raw metin**), build çıktısı üzerinde **3 Lua testi** PASS; güncel çıktı `local-runtime/build-v051-fixed/` altında. Oyun içi LQA: **NOT TESTED**.

## v0.52 taş, toprak ve yapı blokları
- v0.51 sonrasındaki pinned FU 6.5.8 auditinden `tiles/materials/` içindeki tutarlı taş/toprak/tuğla/blok ailesi seçildi: **318 alan / 126 asset / 282 benzersiz kaynak metin**.
- Yeni sürüm `0.52.0-beta`; her alan kaynakta doğrulanıyor ve manifestte kilitli. `generate_v052.py` pinned source gate: **PASS (318/126/282)**.
- `qa_integrity.py`: **PASS (14.120 katalog birimi / 52 raw birim / 542 LOCKED terim)**. Pinned kaynakla statik build **PASS (9.655 alan / 2.829 patch asset / 7 raw asset / 57 raw metin)**; kaynak doğrulaması da PASS.
- Önceki 9.337 katalog satırı ve katmanlı/harici kaynak kanıtları birebir korundu. Yeni alanlarda kilitli Silt/Jungle/Penumbral terimleri, anlam hataları ve Floran konuşma biçimi gözden geçirildi.
- v0.45-v0.52 kaynak kapıları, **193 birim testi** ve üretilen paket üzerinde **3 Lua davranış testi** yerelde PASS. Oyun içi LQA: **NOT TESTED**.

## v0.53 Peglaci yapı ve kablo malzemeleri
- v0.52 kataloğu sonrası `tiles/materials/` içinden Peglaci yapı, soğutmalı kablo ve Pykrete yapı malzemeleri seçildi: **66 alan / 14 asset / 54 benzersiz kaynak metin**.
- Peglaci/Glitch/Floran inceleme metinlerinde kaynak karakter sesi korundu; Peglaci ve Pykrete özel adları tutarlı bırakıldı.
- Pinned kaynak kapısı PASS (**66/14/54**); katalog bütünlük QA'sı PASS (**14.252 katalog birimi / 52 raw birim / 542 LOCKED terim**). **193 birim testi**, pinli kaynakla tam build (**9.721 alan / 2.843 patch asset / 7 raw asset / 57 raw metin**) ve build üzerinde **3 Lua davranış testi** PASS. Pykrete temel bloğunun yanlış açıklaması incelemede düzeltildi.
- Oyun içi LQA: **NOT TESTED**.

## v0.54 bal ve altın ahşap yapı malzemeleri
- v0.53 sonrası güncel main kataloğunda kalan karo malzemelerinden Honey ailesinin bal peteği, altın ahşap, cam ve balmumu alanları seçildi: **71 alan / 18 asset / 62 benzersiz kaynak metin**.
- Kaynak manifesti pinned FU 6.5.8 commitine sabit; yalnız Honey ailesi assetleri dahil. v0.54 exact-source gate ve build allowlist eklendi.
- Pinned kaynak kapısı PASS (**71/18/62**); katalog bütünlük QA'sı PASS (**14.394 katalog birimi / 52 raw birim / 542 LOCKED terim**). **193 birim testi**, pinli kaynakla tam build (**9.792 alan / 2.861 patch asset / 7 raw asset / 57 raw metin**) ve build üzerinde **3 Lua davranış testi** PASS. Floran replikleri, Golden Wood kilidi ve çeviri belleği incelemede eşlendi.
- Oyun içi LQA: **NOT TESTED**.

## v0.55 metal, ahşap, cam ve pencere yapı malzemeleri
- v0.54 sonrası güncel katalog ve pinned FU 6.5.8 auditinden `tiles/materials/` içindeki metal/teknoloji, kereste, cam ve pencere yapı aileleri seçildi: **466 alan / 177 asset / 393 benzersiz kaynak metin**.
- Boyut, yeni paket politikasıyla uyumlu: yaklaşık 500 alan ve 250–400 benzersiz metin; çalışma tematik yapı malzemeleri altında tutuldu.
- Aday `codex/luna-v055` dalında hazırlandı. Exact-source manifesti ve kaynak kapısı eklendi; Sol incelemesi sonrasında doğrudan `main` dalına yayımlandı.
- Oyun içi LQA: **NOT TESTED**.
- Sol incelemesinde katalogdaki 466 yinelenen v0.55 satırı çıkarıldı; önceki 9.792 alan birebir korundu. Camın öbür tarafını görme repliğindeki kopyalama hatası dört assette, Floran sesi sekiz alanda düzeltildi.
- Yerel katalog QA'sı **PASS (15.326 katalog birimi / 52 raw birim / 542 LOCKED terim)**; **193 birim testi** ve pinned FU 6.5.8 tam kaynak build **PASS (10.258 alan / 3.038 patch asset / 7 raw asset / 57 raw metin)**. Build çıktısı üzerinde **3 Lua davranış testi** ve v0.55 exact-source gate **PASS (466/177/393)**. GitHub build/audit CI başarılı; `dist/FU_Turkce_v0.55.0_Beta.zip` kanıttaki SHA-256 ve ZIP CRC denetiminden geçti.

## v0.56 kalan karo malzemeleri
- v0.55 sonrası güncel main ve pinned FU 6.5.8 auditinde `tiles/` altında kalan görünür kapsam seçildi: **365 alan / 197 asset / 323 benzersiz kaynak metin**.
- Bu paket `tiles/materials/` içindeki kalan malzemeleri ve ilişkili `tiles/mods/` girdilerini kapatır. Doğal klasör sınırı 500 alan hedefinin altında kaldığı için ilgisiz içerik eklenmedi.
- Aday `codex/luna-v056` dalında hazırlandı. Exact-source manifesti, kaynak kapısı ve build allowlisti eklendi; Sol ayrı çalışma ağacında doğrulayıp doğrudan `main` yayınına hazırladı.
- Oyun içi LQA: **NOT TESTED**.
- `tiles/mods/moonstone.matmod` açıklaması pinli FU ağacında yalnız FU `.patch` katmanından geldiği için manifest ve katalogda katmanlı kaynak olarak işaretlendi. Neon tüp açıklamasındaki kullanım anlamı, bazı adlar ve Floran replikleri kaynakla eşlendi; önceki 10.258 alan birebir korundu.
- Yerel katalog QA'sı **PASS (16.056 katalog birimi / 52 raw birim / 542 LOCKED terim)**; **193 birim testi**, pinli FU 6.5.8 ile tam kaynak build **PASS (10.623 alan / 3.235 patch asset / 7 raw asset / 57 raw metin)** ve build çıktısında **3 Lua davranış testi** PASS. v0.56 exact-source gate **PASS (365 alan / 197 asset / 323 kaynak)**.
- Yayın sonrası ikinci dil incelemesinde Irradium, Plütonyum ve Uranyum döşemelerinin açıklamalarındaki `Slab` → `külçe` anlam hatası düzeltildi. v0.56 adayıyla karşılaştırıldığında toplam **17 çeviri alanı / 14 benzersiz kaynak cümle veya etiket** değişti. Oyun içi LQA hâlâ yapılmadı.

## v0.57 yürüyen ve uçan canavarlar
- `codex/luna-v057` adayı güncel `main` üstüne alındı; önceki 10.623 katalog satırı birebir korundu. Yeni kapsam **477 alan / 239 asset / 344 benzersiz kaynak metin**; toplam **11.100** yapılandırılmış alan oldu.
- `monopus.monstertype` açıklamasının pinli FU ağacında yalnız FU `.patch` katmanından geldiği doğrulandı; manifest ve katalogda mevcut katmanlı kaynak politikasıyla işaretlendi. Pinli FU 6.5.8 commit `329e714b3fe87571055c8ad7aa38135d199d3317` değişmedi.
- Sol dil incelemesinde v0.57 adayına göre **12 benzersiz kaynak cümle veya etiket / 13 çeviri alanı** düzeltildi. Arı ana rolü, Precursor/Penumbra/Densinium/Jungle terimleri, `Cosmic Ray` sözcük oyunu ve anlamı kayan açıklamalar gözden geçirildi.
- v0.57 exact-source gate **PASS (477/239/344)**; katalog QA **PASS (17.010 katalog birimi / 52 raw birim / 542 LOCKED terim)**. **193 birim testi**, pinli kaynakla tam build **PASS (11.100 alan / 3.474 patch asset / 7 raw asset / 57 raw metin)** ve build çıktısında **3 Lua davranış testi** PASS.
- Oyun içi LQA: **NOT TESTED**.

### v0.57 yayın sonrası Slime adlandırma düzeltmesi
- Aynı canavar ailesindeki diğer adlar `Balçık` kullanırken altı genel yaratık adı `Slime` kalmıştı; altı `/shortdescription` alanı `Balçık` olarak düzeltildi. Önceki katalogdaki oynanabilir tür adı `Slime` korundu; iki bağlam için çeviri belleğine yalnız yedi alanı kapsayan kesin istisna eklendi.
- Luna v0.57 adayından bu sonuca kadar toplam **13 benzersiz kaynak cümle veya etiket / 19 çeviri alanı** düzeltildi. Önceki 10.623 katalog alanı değişmedi.
- Katalog QA, **193 birim testi**, v0.57 exact-source gate, pinli FU 6.5.8 tam build ve build çıktısındaki **3 Lua davranış testi** yeniden PASS. Oyun içi LQA: **NOT TESTED**.

## v0.58 kalan yaratık aileleri
- `codex/luna-v058` adayı güncel `main` üstüne alındı; önceki 11.100 katalog alanı birebir korundu. Yeni kapsam **522 alan / 261 asset / 257 benzersiz kaynak metin**; toplam **11.622** yapılandırılmış alan oldu.
- Sol incelemesinde Luna adayına göre **12 benzersiz kaynak cümle veya etiket / 12 çeviri alanı** düzeltildi. Precursor özel adı ve Jungle/Tropik Orman terimi eşlendi; Ansible videosu ve yaratık açıklamalarındaki anlam, yaratık adları ve cupcake adı gözden geçirildi.
- Pinli FU 6.5.8 commit `329e714b3fe87571055c8ad7aa38135d199d3317` korundu. v0.58 exact-source gate **PASS (522/261/257)**; katalog QA **PASS (18.054 katalog birimi / 52 raw birim / 542 LOCKED terim)**. **193 birim testi**, pinli kaynakla tam build **PASS (11.622 alan / 3.735 patch asset / 7 raw asset / 57 raw metin)** ve build çıktısında **3 Lua davranış testi** PASS.
- Oyun içi LQA: **NOT TESTED**.

## v0.59 kalan görünür canavarlar ve beceri adları
- `codex/luna-v059` adayı güncel `main` üstüne alındı; önceki 11.622 katalog alanı birebir korundu. Yeni kapsam **341 alan / 259 asset / 260 benzersiz kaynak metin**; toplam **11.963** yapılandırılmış alan oldu.
- Sol incelemesinde adayın **18 benzersiz kaynak cümle veya etiketi / 21 çeviri alanı** düzeltildi. `Precursor` özel adı ve kilitli `Bozulmuş Nöbetçi` karşılığı korundu; beceri, mermi ve yaratık adlarındaki anlam hataları giderildi.
- Oyun içinde görünmeyen iki script yardımcısının dört alanı kapsamdan çıkarıldı. `pogolem` ve `nautileech` için temel canavar dosyası bulunmadığından dört alanın pinli FU `.patch` kaynak kökeni mevcut katmanlı kaynak kuralıyla kaydedildi. Pinli FU 6.5.8 commit `329e714b3fe87571055c8ad7aa38135d199d3317` değişmedi.
- v0.59 exact-source gate **PASS (341/259/260)**; katalog QA **PASS (18.736 katalog birimi / 52 raw birim / 542 LOCKED terim)**. **193 birim testi**, pinli kaynakla tam build **PASS (11.963 alan / 3.994 patch asset / 7 raw asset / 57 raw metin)** ve build çıktısında **3 Lua davranış testi** PASS.
- Oyun içi LQA: **NOT TESTED**.

## v0.60 Kadim ve Precursor mini-biome nesneleri
- `codex/luna-v060` adayı güncel `main` üstüne alındı; önceki **11.963** katalog alanı birebir korundu. Yeni kapsam **536 alan / 196 asset / 314 benzersiz kaynak metin**; toplam **12.499** yapılandırılmış alan oldu.
- Sol incelemesinde Luna adayına göre **38 benzersiz kaynak cümle veya etiket / 91 çeviri alanı** düzeltildi. Floran konuşma biçimi, vivisection ve aygıt açıklamalarındaki anlam ile Precursor nesne adlarının Türkçe yapısı gözden geçirildi. `Medi-Vac` ürün adı korundu.
- Kesinleşmiş ve tekrar eden `Cthulhu`, `Erchius`, `Lunari` adları LOCKED kuralına ve olumsuz QA testine eklendi; iki eski Türkçe ekli kullanım alan-bağlı istisnayla korundu. v0.60 görünür alanları build izin listesine kesin manifest kümesiyle bağlandı. Pinli FU 6.5.8 commit `329e714b3fe87571055c8ad7aa38135d199d3317` değişmedi.
- v0.60 exact-source gate **PASS (536/196/314)**; katalog QA **PASS (19.808 katalog birimi / 52 raw birim / 545 LOCKED terim)**. **195 birim testi**, pinli kaynakla tam build **PASS (12.499 alan / 4.190 patch asset / 7 raw asset / 57 raw metin)** ve build çıktısında **3 Lua davranış testi** PASS.
- Oyun içi LQA: **NOT TESTED**.

## v0.64 derin yiyecekler — Luna adayı
- Sol'un v0.63 sonrasında bıraktığı `items/generic/food/` alt klasörlerinden, doğrudan kök dosyalar ve `tier1/` hariç, **168 görünür ad/açıklama alanı / 152 asset** çevrildi; 168 kaynak metin farklıdır.
- Kaynak FU 6.5.8 commit `bb58383c0d16c1152e3439e606b39ff82288b586`; katalog önceki **13.454** alanını koruyup v0.64 adayında **13.622** alana çıktı. `Delilik Kazanımı` ve `Kiraz` için Sol'un v0.63'te netleştirdiği karşılıklar kaynak kapısına eklendi.
- Manifest, exact-source gate, build izin listesi ve CI çağrıları eklendi. Dal `codex/luna-v064`; bu Luna adayı henüz Sol'un teknik inceleme/doğrulamasından veya yayınından geçmedi. Test, build ve yayın bu çalışmada çalıştırılmadı.

## v0.64 Sol incelemesi
- Güncel `main` tabanı üstüne alınırken önceki **13.454** alan birebir korundu; v0.63.2 kaynak ve runtime korumaları kaldı. Luna adayındaki **25 çeviri alanı** düzeltildi. Cupcake kilidi, yinelenen kaynak metnin eski karşılığı ve kayıp satır sonu düzeltildi. `Bacon`, `Pussplum`, `Pearlpea` için yerleşik Türkçe karşılıklar çekimli cümlelerde de LOCKED denetimine bağlandı.
- Yeni 168 alanın **136'sı** temel oyundaki dosyaya FU'nun uyguladığı `.patch` üzerinden geliyor. Bu alanların pinli FU 6.5.8 yamasındaki kaynak değeri ve katalog kökeni tek tek doğrulandı. Kaynak pini `bb58383c0d16c1152e3439e606b39ff82288b586` olarak kaldı.
- v0.64 kaynak kapısı **PASS (168 alan / 152 asset / 168 kaynak)**; katalog QA **PASS (22.054 katalog birimi / 52 raw birim / 556 LOCKED terim)**. **204 birim testi**, pinli kaynakla tam build **PASS (13.622 alan / 4.698 patch asset / 7 raw asset / 57 raw metin)** ve build çıktısında **3 Lua davranış testi** PASS.
- Oyun içi LQA: **NOT TESTED**.

## v0.65 kodeks belgeleri ve Ebrar'ın Yıldızı
- Luna'nın 331 alan / 47 asset / 312 kaynak metin içeren v0.65 adayı güncel v0.64 ana dalı üstünde incelendi. Sol incelemesinde 55 çeviri alanındaki 70 cümle veya kısa metin düzeltildi. Kayıp sayı ve yüzde işaretleri, kaynakta görünür köşeli parantezler, karışık satır sonu biçimi, sayfa sınırları, ITN kurulum adımı ve önemli anlam kaymaları kaynakla eşlendi. Beş yinelenebilir terim LOCKED kuralına alındı.
- Özgün `Ebrar'ın Yıldızı` lambası, üç 16×16 görsel, eşya açıklaması, inceleme metni ve 1 cam + 1 bakır külçesi tarifiyle eklendi. Oyuncu gemisi betiği yalnız sahibinin gemisinde, dolu karoları değiştirmeden, ışınlayıcı yakınındaki uygun duvara bir kez yerleştirmeyi dener. Yeni ve mevcut karakterler tarifi öğrenir. Tamamen dolu gemide otomatik yerleştirme garanti değildir; tarif yedektir.
- FU 6.5.8 kaynak pini `bb58383c0d16c1152e3439e606b39ff82288b586` korundu. v0.65 kaynak kapısı ve katalog QA PASS; 207 birim testi PASS. Pinli kaynakla tam build PASS: 13.953 çeviri alanı / 4.745 patch / 7 raw / 7 özgün dosya. Lua testinde 11 gemi senaryosu PASS. Starbound paketleyici/açıcı 4.759 dosyada byte eşleşmesi verdi; ayrı sunucu ve geçici istemci FU ile sürpriz dosyalarını yükledi. Gemi içi görünüm ve gerçek yerleştirme henüz görsel olarak doğrulanmadı.

25 Eylül 2026: Oyun içi LQA sırasında gemi S.A.I.L. yeniden başlatma/açılış konuşmalarının İngilizce kaldığı doğrulandı. Kök neden, metinlerin ai/ veya species/ altında değil 17 adet objects/ship/*techstation*.object içindeki /dialog/wakeUp ve /dialog/wakePlayer dizilerinde bulunması ve audit kategorisinin bunları genel gemi nesnesi olarak sınıflandırmasıydı. 17 assette 182 görünür alan / 15 benzersiz kaynak metin Türkçeleştirildi; Kirhos ve Fenerox özel açılış replikleri ayrı tonla korundu. Techstation diyalogları bundan sonra Irklar ve SAIL/AI kategorisine bağlandı ve regresyon testi eklendi. Generated dosyalara elle dokunulmadı. Oyun içi tekrar testi: NOT TESTED.
