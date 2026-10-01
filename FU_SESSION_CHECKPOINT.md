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

### 26 Eylül PR #36 incelemesi ve gemi sürprizi onarımı
- PR #35 ana dalda; PR #36 Tricorder/GPS/Mech/SAIL UI düzeltmeleri kaynaklarıyla incelendi. Türkçe metinlerde ek değişiklik yapılmadı (inceleme düzeltmesi: 0 cümle). Windows'ta PNG sıkıştırması farklı olsa da yedi görselin tüm pikselleri aynıydı; kaynak kapısı artık biçim, mod, boyut ve pikselleri karşılaştırıyor. Tek piksel ve boyut sapmasını reddeden regresyon eklendi; paket bayt/hash denetimleri korunuyor.
- Ebrar yıldızının çıkmama hatası Starbound 1.4.4 + FU ile ayrı kayıt kopyasında yeniden üretildi: oyuncu deployment ortamında `mcontroller` yok. Oyuncu konumu `world.entityPosition(player.id())` ile okunuyor; dünya yüklenirken konum hazır değilse yeniden deneniyor. Test ortamı artık bulunmayan `mcontroller` API'sini taklit etmiyor; 12 gemi senaryosu geçiyor.
- Yeni build ile aynı mevcut FU gemisinde yıldız ışınlayıcının sağında otomatik oluştu; ışığı, Türkçe karakterleri ve inceleme mesajı oyun içinde görüldü. Asıl oyuncu kayıtlarına dokunulmadı. Bu, bütün gemi tasarımlarının veya PR içindeki tüm arayüz durumlarının görsel onayı değildir.
- 216 birim testi, UI tam kaynak kapısı, katalog QA, pinli FU build ve yeni çıktı üzerinde 4 temel Lua / 8 UI testi PASS. Paket: 14.140 çeviri alanı / 4.766 patch / 10 raw / 14 özel dosya; kaynak pini değişmedi. Son PR CI ve ana dal yayını bu inceleme commitinden sonra izlenir.

25 Eylül 2026: Oyun içi LQA sırasında gemi S.A.I.L. yeniden başlatma/açılış konuşmalarının İngilizce kaldığı doğrulandı. Kök neden, metinlerin ai/ veya species/ altında değil 17 adet objects/ship/*techstation*.object içindeki /dialog/wakeUp ve /dialog/wakePlayer dizilerinde bulunması ve audit kategorisinin bunları genel gemi nesnesi olarak sınıflandırmasıydı. 17 assette 182 görünür alan / 15 benzersiz kaynak metin Türkçeleştirildi; Kirhos ve Fenerox özel açılış replikleri ayrı tonla korundu. Techstation diyalogları bundan sonra Irklar ve SAIL/AI kategorisine bağlandı ve regresyon testi eklendi. Generated dosyalara elle dokunulmadı. Oyun içi tekrar testi: NOT TESTED.

## 25 Eylül 2026: ekran görüntüsü temelli UI LQA düzeltmeleri

Altı taşan/uzun etiket kısaltıldı. GPS Lua başlıkları ve gemi bilgileri, Mech dinamik durumları, SAIL atmosfer yanıtları, FU karşılama metni ve dört FU katmanlı telsiz mesajı kaynaklarına bağlandı. Mech bitmap İngilizce yazıları yedi kaynak-kilitli görselde temizlenip yerel UI etiketlerine taşındı; yakıt kimlikleri ve hesaplama değerleri korunuyor. Kaynak tarifi tools/ui_lqa_20260925.json, doğrulama tools/check_ui_lqa_20260925.py içindedir. Tam kaynak/CI sonuçları PR ve workflow kaydından kontrol edilir. Oyun içi tekrar testi: NOT TESTED. GPS gezegen sözlüklerindeki özel adlar ve eski değişiklik günlükleri bu dar kapsamın dışındadır.

### 26 Eylül: Ebrar'ın Gülü

- Kullanıcının seçimiyle yıldız görseli, Küçük Prens'ten esinlenen cam fanusta kırmızı güle dönüştürüldü. Imagegen kaynak resmi ve deterministik PowerShell dışa aktarımı `tools/art_sources/ebrar-rose/` ve `tools/prepare_ebrar_rose_art.ps1` içinde. Oyun sprite'ı 24×40, envanter simgesi 16×16; çevresinde yükselen sıcak renkli ışıltı parçacıkları var.
- `futrebrarstar` kimliği, tarif ve yerleştirme işareti korundu. Aynı kopya kaydı yeniden açınca önceki yıldız güle dönüştü; ikinci nesne oluşmadı. Fanus, değişen ışıltılar ve Türkçe inceleme mesajı Starbound 1.4.4 + FU gemisinde görüldü. Gül veya deployment kaynaklı hata loglanmadı; bağımsız Discord lobby hatası test ortamında devam etti. Asıl kayıtlar kullanılmadı.
- Katalogda ek düzeltme 0 cümle. Özgün hediyede 3 benzersiz cümle ve 1 nesne adı değişti (9 görünür alan). 216 birim testi ve pinli build PASS; yeni çıktı üzerinde 4 temel Lua / 8 UI testi PASS. Bu görsel test yalnız hediyeyi kapsar; yukarıdaki tüm UI durumlarının LQA durumu değişmedi.

### PR #36 sonrası paketleme kapısı onarımı

- PR #36 Windows/Linux kontrollerinden sonra birleştirildi. Ana build ve Lua testleri geçti; yayın kanıtı üretimi Mech config için durdu. Sebep: yerel etiket ekleyen replacement eski JSON başlangıcını yeni içerikte bilinçli olarak koruyor; yayın kapısının eski parçanın tamamen yok olmasını istemesi yanlış pozitifti.
- Runtime dosyaları artık pinli build sırasında replacement'lar sırayla uygulanarak doğrulanmış şablonla dosyanın tamamı üzerinden byte eşleştiriliyor. Eksik, fazla, bozulmuş veya fazladan boşluk içeren paket içeriğini reddeden regresyon eklendi. Kaynak eşleşmesi, build-input hashleri ve ZIP/ağaç byte denetimleri korunuyor.
- Aynı paket kanıtı üretimi PR akışına da eklendi; bu tür bir yayın hatası bundan sonra birleştirmeden önce yakalanır. Mod açıklamasındaki eski hediye adı da güle uyarlandı; bu ek ad güncellemesiyle toplam değişen farklı cümle sayısı 4, eşya adı değişikliği 1.

### 26 Eylül: v0.65.2 Slimeperson ve Shadow S.A.I.L. konuşmaları

- Oyuncunun üç görüntüsündeki İngilizce Slimeperson S.A.I.L. açılış replikleri pinli FU 6.5.8 kaynağında bulundu; kurulu oyunun günlüğü aynı metinleri gösteriyor. Kaynak envanterinde 19 gemi techstation nesnesi / 205 diyalog alanı var. Önceki katalog 17 istasyondaki 182 alanı kapsıyordu; Slimeperson'ın 12 ve Shadow'un 11 görünür alanı eksikti.
- Bu 23 alanın 23 farklı kaynak metni / 32 cümlesi çevrildi. Shadow'un `Fragment` özel unvanı ilgili alanlarda kaynak kapısına bağlandı; iki tekrarlanan S.A.I.L. cümlesi mevcut çeviri belleğinden aynen alındı. Katalog v0.65.2-beta; FU 6.5.8 pini korundu. Kaynak blob kimlikleri, manifest, tam S.A.I.L. envanter kapısı, CI çağrıları ve eksik satır regresyonu eklendi. Oyun içi yeni paket kontrolü: NOT TESTED; build/CI/yayın sonuçları daha sonra kaydedilecek.

## 26 Eylül: oynanış önceliği ve çeviri hazırlığı

- Kullanıcının onayıyla mevcut audite isteğe bağlı tam aday çıktısı, `tools/plan_translation.py`, `tools/translation_priorities.json` ve `docs/TRANSLATION_PLANNING.md` eklendi. Paket politikası bu akışa bağlandı. Kaynak pini `bb58383c0d16c1152e3439e606b39ff82288b586`, katalog sürümü `0.65.2-beta` ve mevcut çeviriler değişmedi. Değişen çeviri cümlesi: **0**.
- Araç P0–P3 önceliği, kaynak/pointer bağlamı, dosya bağlantıları, birebir kaynak TM önerileri ve ilgili LOCKED kayıtlarıyla taslak hazırlar. Çeviri otomatik kabul edilmez. Her grubun bağlam ve runtime incelemesi gerekir; teknik ön denetim mevcut tam katalog QA'sını kullanır. Kaynak, katalog, araç veya kural değişince paket eski sayılır. Eski çıktı üzerine yazma reddedilir; varsayılan `planning_output/` Git dışında tutulur.
- Mevcut `dead_assets.json` listesinde iki görünmeyen gemi takip görevi dışlandı: `frackinship/quests/fu_byos.questtemplate` ve `fu_shipupgrades.questtemplate`. Dört gösterim bayrağı kapalı; bağlı scriptler bu metinleri göstermiyor. 6 görünmeyen metin ve 2 teknik portre kimliği kalan sayıdan çıktı. Kanıt ve pin dokümanda; görünür komşu görevin sayılmaya devam ettiğini doğrulayan regresyon var.
- Son kuyruk: **44.247 confirmed** (P0=0, P1=2.570, P2=18.227, P3=23.450), **4.329 review**, **162 lua_review**. Bunlar alan/aday sayılarıdır, cümle sayısı değildir. Öncelikler ilk kural tahmini; gerçek karşılaşma sıklığı ölçülmedi. **P0 review=429** önce görünürlük incelemesi bekler; confirmed P0=0 olması tüm kritik işlerin bittiği anlamına gelmez.
- Güncel paylaşılan çıktı: `../local-runtime/translation-planning-v0652-ready/` (`summary.md`, `queue.json`, `packet.json`). Önceki `translation-planning-v0652` ve `translation-planning-v0652-final` deneme çıktıları güncel değildir; hash denetimi bunları reddeder. İlk confirmed aday aile `objects/farmables`: **456 alan / 350 bağlam grubu**, tamamı P1; 9 grupta mevcut TM önerisi, 12 doğrudan dosya bağlantısı. Ailenin tamamı 1.151 alan / 801 gruptur. Paket **DRAFT_CONTEXT_REVIEW_REQUIRED** durumunda, çeviri alanları boştur.
- **233 birim testi PASS**; kuyruktaki 48.738 kaydın kimlikleri benzersiz ve paket hashleri güncel. Pinli kaynağın temiz Git durumu doğrulandı; `git diff --check` PASS. Test logu: `../local-runtime/translation-planning-tests-final.txt`. GitHub audit workflow'una hazırlık testi ve çıktı üretimi eklendi; uzaktaki CI henüz çalıştırılmadı. Oyun dosyası, kurulum ve yayın değişmedi; bu çalışma için oyun içi LQA yapılmadı. İlk gerçek paketin çeviri/inceleme süreleri ve düzeltme oranı henüz ölçülmedi.
- Gerçek pinli kaynakta taslağın CLI ön denetimi yeniden çalıştırıldı; eksik bağlam/runtime incelemesi nedeniyle beklenen biçimde **exit 1** ile reddedildi. Log: `../local-runtime/translation-planning-blank-check.txt`. Bu negatif kontrol, boş taslağın yanlışlıkla onaylanmadığını doğrular; tamamlanmış çeviri incelemesi anlamına gelmez.

### P0 görünürlük taraması ve Luna devri

- Önceki kuyruktaki **429 P0 review** alanının tümü kaynak pointerı ve değeriyle sınıflandırıldı. **428** alan teknik değerdi: görev `scriptConfig` altındaki portre, ödül, görev/dünya kimlikleri ile GUI callback, hizalama ve renk ayarları. Audit bu alanları artık dışlıyor. Bunlarla aynı tipte başka önceliklerdeki teknik adaylar da temizlendi. Görünür `text`, görev açıklaması ve UI `value` alanlarının kalmasını yeni regresyon doğruluyor.
- Kalan **1** alan `quests/story/gaterepair.questtemplate.patch#5` içindeki `/scriptConfig/outpostBookmark2/bookmarkName = Science Outpost`. `quests/scripts/story/gaterepair.lua` dosyası bu yer imi bilgisini `player.addTeleportBookmark(config.getParameter("outpostBookmark2"))` ile oyuncuya ekliyor. `/target` teknik kimliği dışarıda kaldı; görünen ad P0 confirmed oldu. LOCKED karşılığı **Bilim Karakolu** zaten terminoloji listesinde bulunuyor; bu oturumda katalog çevirisi yazılmadı.
- Yeniden üretilmiş kuyruk `../local-runtime/translation-planning-v0652-p0-triaged/`: **44.248 confirmed** (P0=1, P1=2.570, P2=18.227, P3=23.450), **3.049 review** (P0=0) ve **162 lua_review**. Önceki kuyrukla fark: 1.280 teknik review kaydı çıkarıldı, 1 görünür kayıt confirmed'a taşındı. P0 taslağı 1 alan/1 gruptur; çeviri ve insan incelemesi bekler. FU 6.5.8 pini korunuyor.
- **234 birim testi PASS**; log `../local-runtime/translation-planning-p0-tests.txt`. GitHub `main` ile yerel `HEAD` tarama anında aynı committeydi (`91e8b827`). Çeviri cümlesi değişikliği **0**. Oyun içi yer imi görünümü bu oturumda açılıp doğrulanmadı; script bağlantısı görünürlük dayanağıdır.
- Luna için ikinci, güncel girdi hashli taslak `../local-runtime/translation-planning-v0652-p1-farmables/` içinde üretildi: `objects/farmables` ailesinden **456 alan / 350 bağlam grubu**, 9 grupta mevcut TM önerisi. Bu paket P0 yer imi alanından ayrı tutulur; ikisi de hâlâ `DRAFT_CONTEXT_REVIEW_REQUIRED` durumunda. Eski `translation-planning-v0652-ready/` taslağı kural değişikliği sonrası bayattır.

### 1 Ekim: P0/P1 Sol incelemesi ve aday onayı

- Luna'nın `translation-planning-local-luna-20261001-p0` ve `translation-planning-local-luna-20261001-p1-farmables` paketleri incelendi; katalog henüz bu adayları içermiyor. Güncel uzak `main` üzerindeki README/Atölye bağlantısı ve kanıt güncellemesi yerel `main` ile birleştirildi; kaynak/katalog girdileri değişmedi.
- P0 yer imi **1 alan / 1 grup** olarak onaylandı. P1'de **11 farklı cümle ve 5 eşya adı**, toplam **14 bağlam grubu / 19 alan** düzeltildi. Etçiçeği, Copperbeak, Ironbeak ve Apalit adları kaynak veya önceki onaylı karşılıklarla eşlendi; barnacle benzetmesi, Diodia'nın bakır tadı, Ighant'ın sekme etkisi ve oyuncuya verilen korumalar düzeltildi. Emera açıklamasındaki doğru eski birebir TM karşılığı korundu. Önce/sonra metinleri ve gerekçeler `docs/reviews/p0-p1-20261001.json` içinde.
- **27 yeni LOCKED kayıt** eklendi; toplam **588** kilitli kayıt var. Adların tohum, yumurta ve cümle içindeki çekimleri QA kök denetimine bağlandı. `Bella Morte` ve `Kramil` kaynakla aynı kalabilen özel adlardır. Hazırlık kapısı yalnız tam LOCKED `mode=preserve` eşleşmesini ve ad pointerlarını kabul eder; İngilizce açıklama cümlesi bu istisnadan yararlanamaz. Ad/yanlış varyant ve açıklama reddi regresyonları eklendi; generated terminoloji dokümanı araçla üretildi.
- `fu_scriptedfarmableexample` normal oynanışa bağlanmayan geliştirme örneği olduğundan mevcut dışlama listesine alındı. Adaydan **3 alan / 3 grup** çıkarıldı; kalan P1 **453 alan / 347 grup** olarak yeniden hazırlandı. Yeniden seçimde eski adaydan başka alan eklenmediği ve kaynak/occurrence kümelerinin birebir eşleştiği doğrulandı. Yeni audit **44.238 confirmed**, **3.049 review**, **162 Lua** adayı içeriyor; dışlanan örneğin tüm 10 görünür ad/inceleme alanı bu toplamdan çıktı.
- **237 birim testi PASS**. Güncel pinli kaynakla hazırlık, iki paketin ayrı teknik ön denetimi ve bütün ek alanların birleşik katalog QA'sı PASS: **454 yeni alan**, **23.414 katalog/manifest birimi**, **115 raw birim**, **588 LOCKED kayıt**. `git diff --check` PASS. Kaynak FU 6.5.8 commit `bb58383c0d16c1152e3439e606b39ff82288b586` korunuyor.
- Dil ve kaynak ön denetimi onaylı dosyalar `../local-runtime/sol-review-p0-p1-20261001/p0.approved.packet.json` ve `p1.approved.packet.json`; rapor içerik SHA-256 değerleriyle bu dosyalara bağlı. Paketlerin değiştirilemeyen taslak başlığı korunur; insan dil onayı rapordaki `APPROVED_LANGUAGE_AND_SOURCE_PREFLIGHT` durumuyla kaydedilir. Eski Luna paketleri yeni LOCKED/kural hashlerine göre güncel değildir.
- Görsel oyun içi LQA yapılmadı. Beş yabani varyanta FU ağacında statik dış bağlantı bulunmadı; dinamik/harici mod erişimi doğrulanmadı ve olumlu runtime kanıtı sayılmadı. 11 script bağlantısı iki vanilla dosyaya (`farmableegg.lua`, `harvestable.lua`) gidiyor; varlıkları bu incelemede doğrulanmadı. `flowerspring.object` ve `gaterepair.questtemplate` alanları FU patch katmanından geliyor. Bu sınırlamalar rapor ve paket kanıtlarında açık. Onay katalog entegrasyonu, release build veya yayın tamamlandığı anlamına gelmez; bu adımlar henüz uygulanmadı.

### 1 Ekim: v0.66 entegrasyonu ve diyalog önceliği

- Kullanıcı onaylı adayları pakete eklemeyi ve sıradakileri hazırlamayı istedi; ardından diyalogların öncelikli olmasını belirtti. P0 **1** ve P1 yetiştirme **453** alanı `tools/v066_translations.json` üzerinden `0.66.0-beta` kataloğuna alındı. Toplam **14.617 alan**; önceki **14.163** çeviri satırı birebir korundu. Bu entegrasyonda yeni dil düzeltmesi **0**; önceki incelemenin 11 cümle / 5 eşya adı / 19 alan düzeltmesi aynen kullanıldı. Mevcut **588 LOCKED** kayıt korunur.
- Yeni dilim **155 asset / 198 farklı İngilizce metin / 348 incelenmiş bağlam grubu** içerir. İki alan FU patch katmanına kaynak kilidiyle bağlıdır. `generate_v066.py`, onaylı EN/TR/kapsam digestini, rapor hash bağını, manifest/katalog eşitliğini ve pinli kaynak değerlerini denetler. Tam allowlist ve iki CI kaynak kapısı mevcut düzene eklendi; generated kurulum ağacı veya eski yayın kanıtı elle değiştirilmedi. Ayrıntı: `docs/LQA_V066_20261001.md`.
- **241 birim testi PASS**; log `../local-runtime/sol-review-p0-p1-20261001/integration-tests.txt`. Yeni v0.66 kaynak kapısı ve QA PASS: **23.868 katalog/manifest birimi**, **115 raw birim**, **588 LOCKED**. Tam kaynak build ve yerel ZIP kanıtı bu giriş yazıldığı anda hazırlanmayı bekliyor; uzakta yayın yapılmadı. Oyun içi LQA ve önceki runtime sınırlamaları sürer.
- Kullanıcı tercihi `translation_priorities.json` içinde kalıcı: `dialog`, NPC ve radyo konuşmaları ile nesnelerin konuşma alanları P1; kritik P0 korunur. Görünürlük havuzları birleşmez. Güncel kuyruk **43.784 confirmed** (P0=0, P1=8.209, P2=12.133, P3=23.442), **3.049 review** (P1=2.718) ve **162 Lua** (P1=106). Bu adaylar cümle veya çeviri onayı sayıları değildir.
- Luna için ilk taslak `../local-runtime/translation-planning-v066-dialog-first/packet.json`: **376 alan / 350 grup**, `brewmaster`, `catconverse`, `converse` kaynakları. İkinci taslak `../local-runtime/translation-planning-v066-radio-next/packet.json`: **350 alan / 350 grup**, 11 asset, 70 TM önerili grup. İki paket de yeni katalog/politika hashleriyle üretildi, Türkçeleri boş ve insan incelemesi bekliyor. Birinci kataloğa alındığında ikinci bayatlayacağı için yeniden üretilir. Sıra ve kaynak ipuçları: `docs/LUNA_DIALOGUE_HANDOFF_20261001.md`. Farmables ve wired kalanları diyaloglardan sonraya bırakıldı.

### v0.66 yerel paket sonucu

- Entegrasyon/kod commit'i **`4b898bee3299c2d1b9d7dfae43385b9b798c9479`**. Son, güncel build **`../local-runtime/build-v066-20261001-final/`** içinde; kullanılacak ZIP **`FU_Turkce_v0.66.0_Beta.zip`**. SHA-256: **`7a8e8229987693d203c2759e03e2eed1d50f36bd9ed4081c4a0383cd2f29f9cc`**. ZIP **4.944 oyun dosyasının** doğrulanmış build ağacıyla eşleşir. Güncel yerel kanıt: aynı klasörde `validation.json` ve `package-evidence.json`. Önceki `build-v066-20261001/` ara çıktısı yerine `-final` klasörünü kullan.
- Tam pinli kaynak build **PASS**: **14.617 alan / 4.920 patch asset / 10 raw asset / 126 raw metin gösterimi**, 14 custom game asset. **241** genel regresyon, üretilen paket üzerinde **4 Lua davranış + 8 UI regresyonu PASS**. v0.45–v0.66 arasındaki **22 kaynak kapısı**, UI kaynak kapısı ve **19 S.A.I.L. istasyonunun 205 alanı** PASS. Kaynak/build girdileri commit edilmiş, dirty=false; ZIP bütünlüğü ve build/kurulum ağacı eşitliği PASS.
- İlk build, `interface/kukagps/kukagps.lua` dosyasının Windows checkout'unda 423 CRLF satır sonuyla durduğunu ve pinli Git blobuyla bayt düzeyinde eşleşmediğini yakaladı. Dosya aynı committeki özgün LF blobuyla geri eşlendi; değişmemiş indeks girdisinin stat önbelleği yenilendi. Bütün **10 raw kaynak asseti** Git blobuyla birebir doğrulandı. Kaynak commit, kod ve Git içeriği değişmedi; kaynak checkout'u temizdir. Detay: `../local-runtime/sol-review-p0-p1-20261001/raw-source-byte-repair.json`.
- Luna checkout'unda kalan altı eski araç dosyasının CRLF/LF farkı da Git'teki LF baytlarıyla eşlendi. İndeks/HEAD içeriği değişmedi. Sol ve Luna'nın **tam build input digestleri**, katalog hashleri ve iki yeni taslağın girdi hashleri artık aynıdır. Detay: `repo-input-byte-repair.json`. İki boş taslağın ön denetimde onaylanmadığı ayrıca doğrulandı; `next-packets-verified.json` paket SHA'larını içerir.
- `local-repo` ve `local-luna` aynı güncel yerel kaynağı kullanır. **Uzak push/yayın, Steam Atölye güncellemesi ve oyun kurulumu yapılmadı.** Oyun içi görsel LQA **NOT TESTED**; beş yabani varyantın erişimi ve iki vanilla scriptin kurulumda varlığı önceki LQA listesinde açık kalır. Generated tracked dosyalar mevcut yayımlanmış sürüme aittir; onları yeni yerel sürüm kanıtı gibi kullanma. Kaynak dışı build/ZIP/taslaklar `local-runtime` altında tutulur.
- Beyin kaynak eşitlemesi başarılı oldu; yeni v0.66 sonuç notu ise güvenlik denetiminde `Memory safety policy rejected source` ile reddedildi. Daha kısa olgusal kayıt da kabul edilmedi; yeni not/receipt kaydedilmedi. Kapsam kimliği veya oturum bağı değiştirilmedi. Bu oturumun geçerli proje kaydı bu checkpoint ve devir/LQA belgeleridir; paket hazırlığı tamamlanmıştır.

### 1 Ekim: Luna’nın ilk diyalog paketi — Sol incelemesi ve v0.67

- Luna’nın 376 alan / 350 bağlam grubunun tamamı EN/TR karşılaştırmasıyla incelendi. 25 grupta 27 alan, bağlam bazında 30 cümle ve alan tekrarları dahil **32 cümle düzeltmesi** yapıldı. Ayrıntılı önce/sonra/gerekçeler `docs/reviews/dialogue-20261001.json` içinde; özgün Luna paketi `../local-runtime/sol-review-dialog-20261001/luna-original.packet.json`, onaylı aday `approved.packet.json`. Özgün paket değiştirilmedi.
- **18 LOCKED** eklendi; toplam **606**. Yeni terim hashleriyle taslak yeniden hazırlandı; EN/bağlam/occurrence üyeliği birebir doğrulanarak yalnız izinli düzenlenebilir alanlar taşındı. Teknik ön denetim PASS; manuel dil onayı ayrı raporda `APPROVED_LANGUAGE_AND_SOURCE_PREFLIGHT` ve tam paket SHA-256 ile kayıtlı. Teknik PASS tek başına insan dil onayı sayılmadı.
- `0.67.0-beta`: yeni 376 alan `tools/v067_translations.json` ile entegre; toplam **14.993 alan**. Önceki 14.617 çeviri satırı aynen korundu. 3 asset / 307 farklı EN / 350 ayrı bağlam. **220 alan FU converse.config.patch katmanından**, 46 brewmaster ve 110 catconverse doğrudan kaynaktan. FU 6.5.8 commit pini korunuyor.
- `generate_v067.py` onaylı EN/TR/kapsam digestini, rapor bağını, kaynak provenance’ını, manifest/katalog eşitliğini ve pinli kaynak değerlerini doğrular. Tam allowlist ve iki mevcut CI kaynak kapısı güncellendi. **248 regresyon PASS**, QA: **24.620 katalog/manifest birimi / 115 raw / 606 LOCKED**. Log `../local-runtime/sol-review-dialog-20261001/integration-tests.txt`. Generated-output edit guard ve tam build/ZIP sonucunun devam kaydı aşağıda yapılacak.
- Oyun içi LQA **NOT TESTED**. Temel vanilla converse.config FU kaynak checkout’unda yok; FU patch değeri kontrolü tam oyun katmanını kanıtlamaz. Catvillager NPC dialog referansı var; FU tenant/dungeon statik üretim bağlantısı bulunmadı, dinamik/harici erişim doğrulanmadı. Bunlar olumlu oyun görünürlüğü kanıtı sayılmadı. Liste `docs/LQA_V067_20261001.md`.
- Sıradaki taslak: `../local-runtime/translation-planning-v067-dialog-next/packet.json`, **380 alan / 350 grup**, 30 TM önerili grup. Radyo bekleyen taslak `../local-runtime/translation-planning-v067-radio-next/packet.json`, **350 / 350**, 71 TM önerili grup. İki taslak güncel input/basis hashleriyle boş; onaysız oldukları doğrulandı. Diyalog önce; entegrasyon ardından radyo yeniden üretilmeli. Eski v066 taslaklarına devam edilmez. Güncel handoff `docs/LUNA_DIALOGUE_HANDOFF_20261001.md`.
- Kalan confirmed **43.408**, review **3.049**, Lua **162**; diyalog ailesi **1.910 alan / 1.799 grup**. Onaylı çeviri/cümle veya kesin görünürlük sayıları değildir. Uzak push/yayın ve oyun kurulumu yapılmadı; build çıktıları `local-runtime` altında tutulur.

### v0.67 yerel paket sonucu

- Kaynak/entegrasyon commit’i **`54255f0591e593228dd7f00bc91e1de1ad8a0420`**. Tam build `../local-runtime/build-v067-20261001/`, ZIP **`FU_Turkce_v0.67.0_Beta.zip`**. SHA-256 **`fe3378c1e01c420e985f4e1df75b7f5d656ac325a3ca6b6065e2966fd3b19d89`**; 2.624.237 byte. Güncel yerel doğrulama/kanıt aynı klasörde `validation.json` ve `package-evidence.json`. Mevcut published tracked kanıtının yerine elle geçirilmedi.
- Tam build **PASS**: **14.993 alan / 4.923 patch asset / 10 raw asset / 126 raw metin gösterimi / 14 custom asset**, toplam **4.947 oyun dosyası**. Kaynak kapsamı direct=14.357, FU patch=587, mevcut external ledger=49; external/vanilla sınırları görsel oyun testi sayılmaz. Code build girdileri commit edilmiş ve dirty=false; build input hash `c8fcdebfb0b2e1aa97058b5610456a9a4453ab81be925fb5991123d6dbec1600`.
- **248** genel regresyon, üretilen paket üzerinde **4 Lua + 8 UI testi PASS**. Yeni v0.67 kaynak kapısı, UI kaynak kapısı, **19 S.A.I.L. istasyonunun 205 alanı**, generated-output edit guard, ZIP integrity ve ZIP/build-tree byte eşitliği **PASS**. Önceki v0.45–v0.66 kapıları önceki pakette geçti; değişmemiş eski dilimler için bu tur tekrar çalıştırılmadı. Loglar `../local-runtime/sol-review-dialog-20261001/` altında; yeni kaynak/build/ZIP sonuçları yerel raporlarda kayıtlı.
- Oyun içi LQA **NOT TESTED**; temel vanilla converse dosyası ve catvillager üretim erişimi inceleme listesinde açık. **Uzak push/yayın, Steam Atölye yüklemesi ve oyun kurulumu yapılmadı.** Sonraki çeviri diyalog taslağıyla başlar; diyalog entegrasyonundan sonra radyo yeniden üretilir.

### 1 Ekim: ikinci diyalog paketi — v0.68 Sol incelemesi

- Kullanıcı yeni çeviriyi kontrol edip sonunda yayımlamayı istedi. GitHub v0.67 Build/QA ve Remaining Scope Audit başarıyla tamamlanmış; generated yayın commit’i `4c4a0f99a59664fafea14cbb27506ec5d6a1ab61` yerel main’e fast-forward alındı.
- `translation-planning-v067-dialog-next/packet.json` içindeki **380 alan / 350 grup** tam EN/TR karşılaştırmasıyla incelendi. **37 grup / 38 alan** düzeltildi; değişmiş cümle/kısa konuşma ifadeleri bağlam bazında **47**, alan tekrarları dahil **48**. Detaylı önce/sonra ve sayım `docs/reviews/dialogue2-20261001.json`. Özgün aday `../local-runtime/sol-review-dialog2-20261001/luna-original.packet.json` korunur; onaylı paket `approved.packet.json` ayrı tam SHA ile bağlı.
- **9 LOCKED** eklendi, toplam **615**. Eski katalogdaki beş semantik olarak geçerli glyph→sembol karşılığı değiştirilmedi; yalnız tam asset/pointer/EN/TR içeriklerine bağlı istisnalar eklendi. Genel yeni çeviri izni veya rün karşılığına izin sayılmaz; değişmiş metni reddeden test var. Konuşmacının selfname’i, sacred karşılaştırması, race eylemi, imminent/immense/quixotic anlamları ve Ruin özel adı düzeltildi. Floran tıslaması kaynak ses özelliğiyle tutarlı hale getirildi.
- Yeni LOCKED hashleriyle taslak yeniden hazırlandı; immutable EN/bağlam/occurrence üyeliği birebir doğrulanarak yalnız izinli düzenlenebilir alanlar taşındı. Teknik ön denetim PASS ve manuel `APPROVED_LANGUAGE_AND_SOURCE_PREFLIGHT` ayrı raporda. **380 alanın tamamı FU patch katmanından**, 272 farklı EN, 350 ayrı bağlam. FU 6.5.8 pini `bb58383c0d16c1152e3439e606b39ff82288b586` değişmedi.
- `0.68.0-beta` kataloğu **15.373 alan**: önceki 14.993 satır birebir korundu, yeni `tools/v068_translations.json` eklendi. `generate_v068.py`, sabit onaylı EN/TR/kapsam digestini, rapor hash bağını, provenance ve source pinini denetler. Allowlist yalnız 380 alanı açar; iki mevcut CI kaynak kapısı yeni sürümü çalıştırır.
- **254 birim testi PASS**; kaynak kapısı, UI kaynak kapısı ve **19 S.A.I.L. istasyonunun 205 alanı PASS**. Tam QA **25.380 katalog/manifest birimi / 115 raw / 615 LOCKED**. Loglar `../local-runtime/sol-review-dialog2-20261001/`. Yerel build ve GitHub yayın sonucunun devam kaydı ayrı yapılacak.
- Oyun içi LQA **NOT TESTED**. Temel vanilla converse.config mevcut FU checkout’unda yok. ElDuukhar köylüsünün converse referansı elduuconverse.config; base converse.config yalnız breakObject. Genel NPC referansları tüm konuşmacı/muhatap dallarının canlı erişimini kanıtlamaz. Bu sınırlamalar `docs/LQA_V068_20261001.md` ve onay raporunda korunur.
- Luna için güncel boş taslak `../local-runtime/translation-planning-v068-dialog-next/packet.json`, **399 alan / 350 grup**, 65 TM önerili grup; input/basis hashleri güncel, boş paketin onaylanmadığı doğrulandı. Önceki radyo taslağı bayat; radyo başlamadan yeni çıktı klasöründe hazırlanmalı. Diyalog ailesi kalan **1.530 alan / 1.449 grup**. Confirmed **43.028**, review **3.049**, Lua **162**. Güncel handoff `docs/LUNA_DIALOGUE_HANDOFF_20261001.md`.

### v0.68 yerel paket ve yayın hazırlığı

- Kaynak/entegrasyon commit’i **`4d1f8e9c95425ea855f0391e458d9593fb97275e`**. Build `../local-runtime/build-v068-20261001/`, ZIP **`FU_Turkce_v0.68.0_Beta.zip`**; SHA-256 **`e64d5208465fccfd84c488ca1ffecf8d0210895dac09bba02c10dd6bec0a5eb6`**, 2.637.969 byte. Güncel yerel kanıt aynı klasörde `validation.json` / `package-evidence.json`.
- Tam build **PASS**: 15.373 alan / 4.923 patch asset / 10 raw asset / 126 raw metin gösterimi / 14 ek oyun asseti, toplam **4.947 oyun dosyası**. Source field coverage direct=14.357, FU patch=967, existing external ledger=49. Build girdileri commit edilmiş, dirty=false; input hash `fbb8141a503972960a0b8ed2f7170250721e3058363b32cbb2a729e200f6fed5`.
- **254** genel regresyon; yeni pakette **4 Lua + 8 UI test PASS**. V0.68, UI ve S.A.I.L. kaynak kapıları, generated-output edit guard, ZIP integrity ve ZIP/build-tree byte eşitliği PASS. Önceki kaynak kapıları GitHub’ın v0.67 yayınında geçti; yeni yayın CI’sı hepsini yeniden çalıştıracak.
- README’nin eski v0.65.0 sürümü, sayıları ve artık bulunmayan ZIP’e indirme bağlantısı v0.68 paketine güncellendi. SHA ve run ID README’ye kopyalanmadı; mevcut dist/build-evidence.json kanıt yolu korundu. Steam Atölye’nin ayrı yayın akışı açıklandı. Gizli içerik yayın metinlerine eklenmedi.
- Bu giriş yazılırken GitHub push/yayın sonucu bekliyor; canlı oyun LQA NOT TESTED. Steam Atölye ve oyun kurulumu bu GitHub yayını kapsamında yapılmadı. Beyin kaynak bağlı sonuç notu/receipt yayın doğrulamasından sonra kaydedilecek.

### v0.68 GitHub yayını tamamlandı

- GitHub kaynak/yayın girdisi **`8c9bb6c9ba71caaf02eeb52ab2c378be03626d2e`**, generated yayın commit’i **`e7d8612ea26ed2aab530593c6c8b66ee86663e29`**. Build/QA run **36899433303** ve Remaining Scope Audit run **36899433341** başarıyla tamamlandı. V0.45–v0.68 kaynak kapılarının tümü, 254 regresyon, tam build, paket Lua/UI ve yayın kapıları CI’da geçti.
- Yayımlanan paket `dist/FU_Turkce_v0.68.0_Beta.zip`; güncel kanıt `dist/build-evidence.json`. ZIP SHA-256 **`e64d5208465fccfd84c488ca1ffecf8d0210895dac09bba02c10dd6bec0a5eb6`**, yerel v0.68 ZIP ile birebir aynı. Generated FU_Turkce ağacı ve ZIP bütün dosyalar bazında eşitlendi: **4.948 dosya (_metadata dahil), 4.947 oyun asseti**. Catalog/build-input/install-tree hashleri yerel kanıtla aynı, source pin değişmedi. Yayın dosyaları GitHub’ın mevcut generated akışından alındı; elle üretilen tracked commit yapılmadı.
- README güncel v0.68 ZIP’e bağlanır. Oyun içi LQA NOT TESTED; vanilla ve özel NPC erişim sınırlamaları devam eder. Steam Atölye veya bu PC’ye oyun kurulumu bu GitHub yayını kapsamında yapılmadı.
- Beyin ilk sonuç notunu reddetti: güvenlik filtresi 11 haneli herkese açık GitHub run ID’lerini hassas sayı olarak algıladı. Motor/politika/kapsam/oturum bağı değiştirilmedi. Sonuç notunda gereksiz run ID’leri çıkarılıp yayın kanıtı ve inceleme dosyası bağlantıları korundu; safety PASS, note-create ve geri okuma başarılı, sync başarılı (warnings/conflicts yok). Yeni not **`notes/p-local-c9ce88775f19f9eb7e39/fu-v068-dialogue-published-20261001.md`**; receipt event **`fu-v068-dialogue-published-20261001`**, harness codex, session `71a0e71aec3716420c7d0fb2` başarıyla kaydedildi. Source **`receipts/2c7ee92eab9940528a14d1676336ae6ae6f51c2cdbf9da49de3bec5e8bd19693.md`**.


## 1 Ekim 2026 — v0.69 Sol incelemesi ve yerel paket

399 alan / 350 bağlam / 269 benzersiz EN incelendi; 44 grupta 45 alan düzeltildi. Bağlam başına 48, tekrarlar dahil 50 cümle/kısa ifade değişti. Katalog 15.772, LOCKED 619 (Barbatus, CySol, Zaibatsu, Pyreite). Önceki 15.373 alan aynen korunur. Tam önce/sonra: docs/reviews/dialogue3-20261001.json; LQA ve Sefton REVIEW sınırı: docs/LQA_V069_20261001.md.

Kod/inceleme commit: 0f7e3f6f774cabfc5e7bccb6af8fa91a780dc52f. Statik QA, pinli tam build, source/UI/SAIL kapıları, generated koruması, yeni paket üzerinde 4 Lua + 8 UI testi PASS. Genel suite ilk 259 testte eski gate sürüm sabiti hatasını yakaladı; sabit düzeltildi ve üç v069 regresyonu tekrar PASS. CI tüm suite’i son kaynakta çalıştıracak. FU pini aynı. Yerel build ../local-runtime/build-v069-20261001, paket kanıtı package-evidence.json.

Sıradaki boş ve güncel paket ../local-runtime/translation-planning-v069-dialog-next/packet.json: 375 alan / 350 grup, 137 TM öneri grubu. Kalan confirmed 42.629, dialog 1.131; review 3.049, Lua 162. Eski radio paketi bayat, radyo başlayınca yeniden üret. Local Sol yolu local-repo, Luna yolu local-luna. GitHub generated yayını ve son iki checkout eşitlemesi bu kayıtta henüz bekliyor. Oyun içi LQA NOT TESTED.


### v0.69 yayın tamamlandı — 1 Ekim 2026

GitHub kaynak commit ba08b98c9899904dc03818508013411ea46c1b6f; generated yayın commit 61f66931f10841cb2be77df905eac37f1b596762. Build/QA https://github.com/Snix52/FrackinUniverse-Turkce/actions/runs/36912154641 ve Remaining Scope Audit https://github.com/Snix52/FrackinUniverse-Turkce/actions/runs/36912155039 SUCCESS. CI tüm 259 regresyonu, bütün v045–v069 kaynak kapılarını, tam build/ZIP/generated yayın kapısını tamamladı.

Yayımlanan v0.69.0-beta ZIP, 4.948 dosyalık FU_Turkce ağacı, katalog ve build input hashleri yerel doğrulanmış paketle birebir eşleşiyor. Tek güncel kamuya açık paket kanıtı dist/build-evidence.json. Doğrudan main yayını yapıldı; PR yok. Bu çalışma Steam Atölye veya oyuna kurulum yapmadı.

Son cümle muhasebesi: Bender repliğinin iki cümlesi de değişmiştir. Bağlam toplamı 48, alan tekrarları dahil **50** değişmiş cümle/kısa ifade. İlk ara sayım 47/49 idi; yalnız kayıt sayımı düzeltildi, onaylı EN/TR ve paket içeriği değişmedi. İnceleme raporundaki sözlük atfı bankayı kanıtlayan sözlük maddesi gibi sunulmayacak şekilde ayrıldı; banka yorumu bağlam çıkarımıdır.

Beyin kayıt/receipt sonuçları aşağıda; son docs commit sonrası local-repo ve temiz local-luna main ile ff-only eşitlenir. Güncel sonraki paket ../local-runtime/translation-planning-v069-dialog-next/packet.json, 375 alan/350 bağlam, input ve basis doğrulandı, boş taslak teknik kabulden reddedildi. Oyun içi LQA NOT TESTED; Sefton sözlük/lore karşılığı REVIEW.

Beyin: notes/p-local-c9ce88775f19f9eb7e39/fu-v069-dialogue-published-20261001.md başarıyla oluşturuldu ve kind/project/body geri okundu. Ana proje kökünden beyin-project.ps1 sync PASS, warnings/conflicts yok. Receipt fu-v069-dialogue-published-20261001, codex harness ve geçerli session/refs geri okuma PASS. Receipt kaynağı receipts/aac91509d4254ddff19512a5edefc02b23be90f8ea34f1e8be797a5c4eebf35f.md. Gereksiz public CI run numaraları hafıza gövdesine alınmadı; güvenlik denetimi bypass edilmedi.


## 1 Ekim 2026 — v0.70 Sol incelemesi ve yerel paket

375 alan / 350 bağlam / 248 benzersiz EN incelendi; 33 grupta 37 alan düzeltildi. Bağlam başına 34, tekrarlar dahil **38 değişmiş cümle/kısa ifade**. Katalog **16.147**, yeni LOCKED **18**, toplam **637**. Önceki 15.772 satır aynen korundu. Tam önce/sonra ve gerekçeler: docs/reviews/dialogue4-20261001.json. Oyun içi LQA NOT TESTED; Sefton REVIEW, statik NPC bağlantısı her dalın canlı erişimini kanıtlamaz.

Kaynak/entegrasyon commit cd89ae1e73e7c7ef9091627abc7ae1dd611cad27. **270 regresyon, compileall, v070/UI/SAIL kaynak kapıları, tam build, generated-output edit guard, yeni pakette 4 Lua + 8 UI testi PASS**. 4.923 patch + 10 raw + 14 custom = 4.947 oyun asseti; metadata ile 4.948 dosya. Kaynak girdileri temiz/commit edilmiş; FU 6.5.8 pini bb58383c0d16c1152e3439e606b39ff82288b586 korunur. Yerel build ../local-runtime/build-v070-20261001/, package-evidence.json. ZIP SHA256 ffbf0a0532fed6ff4dad4a1252d1478036bf6f80ee01639938ea55ff68874dfa, 2674368 byte. ZIP integrity ve kurulum ağacı byte eşitliği PASS; build input SHA 7098435d86fab689e643eb5bee2d43415c2fa0b1775db0def0d8dedffebaa6e9.

Yeni güncel ve boş taslak ../local-runtime/translation-planning-v070-dialog-next/packet.json: **352 alan / 350 bağlam**, 57 TM önerili grup. Skath devamı, Thelusian/Veluu sohbetleri, ırklara göre selamlaşmalar ve Slime/ElDuukhar/Fenerox/mürettebat replikleri. Patch 256 + Slime 72 + ElDuukhar 11 + Fenerox 8 + crew 5 alan. Fresh inputs doğrulandı, boş/onaysız taslak teknik kabulden reddedildi. Dialog kalan 756 alan/749 bağlam; confirmed 42.254 (P1 6.679), review 3.049, Lua 162. Eski radyo taslağı bayat, başlayınca yeniden hazırla. Sol local-repo; Luna local-luna. Güncel handoff içerik ve kaynak dağılımını açıklar.

Bu girişte GitHub push/CI/generated yayını ve son local-luna ff-only eşitlemesi bekliyor. Beyin kaynak bağlı sonuç notu/receipt yayın doğrulanınca kaydedilecek. Steam Atölye ve oyun kurulumu bu GitHub yayını kapsamında değil.


### v0.70 GitHub yayını tamamlandı — 1 Ekim 2026

Kaynak/yayın girdisi c86aebf75ad99985496ccf810d9c8eb4159d9668; generated yayın commit 1f7779730c2dc9eb681b9785729603b68ff472a8. İki CI SUCCESS: FU Turkce Remaining Scope Audit: https://github.com/Snix52/FrackinUniverse-Turkce/actions/runs/36920530856; FU Turkce Build and QA: https://github.com/Snix52/FrackinUniverse-Turkce/actions/runs/36920530849. Bütün 270 regresyon, v045–v070 kaynak kapıları, tam build/ZIP/generated yayın kapısı ve ayrı Remaining Scope Audit tamamlandı. Direkt main yayını; PR yok.

Yayımlanan `dist/FU_Turkce_v0.70.0_Beta.zip` ve 4.948 dosyalık FU_Turkce ağacı bağımsız yerel v0.70 build ile birebir byte eşleşti. ZIP SHA256 ffbf0a0532fed6ff4dad4a1252d1478036bf6f80ee01639938ea55ff68874dfa, build input hash 7098435d86fab689e643eb5bee2d43415c2fa0b1775db0def0d8dedffebaa6e9; catalog/install-tree hashleri de aynı. FU 6.5.8 pini korundu. Tek güncel kamuya açık paket kanıtı `dist/build-evidence.json`; lokal doğrulama `../local-runtime/sol-review-dialog4-20261001/published-evidence.json`.

18 yeni LOCKED (637 toplam), 375 yeni alan (16.147 katalog); 33 bağlam/37 alanda tekrarlar dahil 38 cümle/kısa ifade düzeltildi (bağlam başına 34). Tam önce/sonra/gerekçe commit edilen `docs/reviews/dialogue4-20261001.json` içinde. Oyun içi LQA NOT TESTED; Sefton REVIEW. Steam Atölye ve oyun kurulumu bu GitHub yayını kapsamında yapılmadı.

Beyin becerisi ana proje kökünden beyin-project.ps1 ile kullanıldı. notes/p-local-c9ce88775f19f9eb7e39/fu-v070-dialogue-published-20261001.md oluşturuldu; kind/project/body geri okuma PASS. Sync warnings/conflicts olmadan başarılı. Receipt event fu-v070-dialogue-published-20261001, codex harness ve mevcut session/refs/body geri okuma PASS; kaynak receipts/3bd6a7b6fa3880a213d1b46447e983fcf076abc85490607c77815cda4b132d1d.md. Gereksiz public Actions run ID'leri hafıza gövdesine alınmadı, güvenlik filtresi/kapsam/oturum değiştirilmedi.

Son docs commit ardından temiz local-luna main'e ff-only alınır. Sonraki paket `../local-runtime/translation-planning-v070-dialog-next/packet.json`, 352 alan/350 bağlam: Skath devamı, Thelusian/Veluu sohbetleri, ırklara göre selamlaşmalar ve Slime/ElDuukhar/Fenerox/mürettebat replikleri. Fresh input/basis ve boş taslağın onaysız olduğu doğrulandı. Eski radio taslağı bayat; başlarken yeni katalogla hazırla. İki checkout'un son temiz HEAD, remote ve build-input eşleşmesi ayrı `worktrees-verified.json` dosyasına yazılır.
