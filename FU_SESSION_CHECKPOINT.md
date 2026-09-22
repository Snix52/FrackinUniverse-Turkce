# FU Session Checkpoint

## Güncel çalışma
22 Eylül 2026: **v0.45.1 bakım paketi**, 22 Eylül ana kontrol bulgularının düzeltilmesi.
Kaynak sürüm: `tools/ceviriler.json`. Yayımlanmış son paketin gerçek sürümü, kaynak commit'i, CI run'ı, SHA-256 ve PASS durumu için tek referans: [`dist/build-evidence.json`](dist/build-evidence.json).
Bu checkpoint bir build kanıtı kopyası değildir; aşağıdaki v0.42-v0.45 sonuçları tarihsel kayıtlardır.

Pinned FU: `sayterdarkwynd/FrackinUniverse` @ `329e714b3fe87571055c8ad7aa38135d199d3317` (6.5.8).

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
