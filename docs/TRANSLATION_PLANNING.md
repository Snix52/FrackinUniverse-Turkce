# Oynanış önceliği ve çeviri hazırlığı

`tools/plan_translation.py` mevcut kalan-kapsam auditini kullanır. Kaynak pini, katalog, generated paketler ve yayın kapıları aynı sistem üzerinden devam eder. Araç çeviri üretmez; çevrilecek işleri ve inceleme bağlamını hazırlar.

## Öncelik

| Düzey | İlk değerlendirme |
|---|---|
| P0 | Görev, araştırma, kritik uyarı veya gereksinim |
| P1 | Diyaloglar; arayüz, S.A.I.L., karakter, üretim ve enerji sistemleri |
| P2 | Ekipman, malzeme ve keşif |
| P3 | Dekorasyon, atmosfer, kodeks ve güncelleme arşivi |

Kurallar `tools/translation_priorities.json` içindedir. Her satırda kural kimliği ve gerekçesi bulunur. Bunlar karşılaşma sıklığı ölçümleri değildir. Örneğin üretimi öğreten bir kodeks veya çalışan dekoratif görünümlü makine daha yüksek öncelik isteyebilir; kural değişikliğinin gerekçesini kaydet ve kuyruğu yeniden üret. Belirsiz satırlar `unclassified` gerekçesiyle P2'de görünür. `confirmed`, `review` ve `lua_review` ayrı görünürlük havuzlarıdır; düşük öncelik düşük çeviri kalitesi anlamına gelmez.

Paket yalnız `confirmed` havuzundan seçilir. Çeviriye başlamadan önce kuyruktaki daha yüksek öncelikli `review` / `lua_review` adaylarının görünürlüğünü incele; gerekiyorsa mevcut audit kurallarında kaynak dayanağıyla kesinleştir ve paketi yeniden üret. `confirmed` P0 sayısının sıfır olması, P0 incelemesinin bittiği anlamına gelmez. Otomatik seçilen paket bir sonraki çeviri için taslak öneridir.

Nesnelerin kendi verilerindeki görev sunma, üretim/panel/ışınlanma/dükkân açma ve kablo bağlantısı anahtarları da okunur; böylece dekorasyon klasöründe duran işlevsel nesneler yalnız klasör adından dolayı geriye atılmaz. `.patch` içindeki bu anahtarlar da kaynak pointerlarıyla ipucu olarak kaydedilir. Statik anahtar bulunması tek başına canlı erişim kanıtı değildir; patch koşulları ve sonraki mod katmanları ayrıca incelenir.

Nesnelerdeki ırka özel inceleme replikleri P3'tür; makinenin işlev açıklamasıyla aynı önceliği otomatik almaz. Mekanik yönlendirme içeren istisnalar incelemede yükseltilir.

Pinli `bb58383c0d16c1152e3439e606b39ff82288b586` kaynağında `frackinship/quests/fu_byos.questtemplate` ve `fu_shipupgrades.questtemplate` dosyalarının dört gösterim bayrağı (`showInLog`, `showAcceptDialog`, `showCompleteDialog`, `showFailDialog`) kapalıdır. Bağlı `frackinship/scripts/quest/frackinship.lua` ve `shipupgrades.lua` bu görevlerin `title`, `text`, `completionText` alanlarını göstermez. Bu iki takip görevi mevcut `tools/rules/dead_assets.json` dışlama listesine eklendi: 6 görünmeyen metin alanı ve 2 teknik portre kimliği kuyruktan çıkarıldı. Kaynak pini değişince görünürlük dayanakları yeniden incelenir.

Bu pinde P0 `review` havuzundaki 429 alan tek tek işaretlendi. 428 alan; görev `scriptConfig` içindeki portre/ödül/görev kimlikleri veya GUI'nin callback, hizalama ve renk ayarlarıdır. Örneğin `questGiver`, `giveBlueprints`, `vAnchor=bottom` oyuncuya metin olarak gösterilmez; auditin teknik anahtarları bu bağlamlarda dışlaması gerekir. Kalan bir alan, `quests/story/gaterepair.questtemplate.patch` içindeki `/scriptConfig/outpostBookmark2/bookmarkName = Science Outpost`; `quests/scripts/story/gaterepair.lua` değeri `player.addTeleportBookmark` ile oyuncu listesine ekler. Bu alan `confirmed` olarak yükseltildi. Aynı `outpostBookmark2/target` içindeki dünya kimliği dışarıda kalır. Böylece görünen yer imi, teknik değerlerle birlikte kaybolmaz.

P0 taslağındaki görünen yer imi için mevcut LOCKED karşılık `Bilim Karakolu`dur. Luna kaynak ve oyundaki bağlamı kontrol edip karşılığı kendisi pakete yazar; bu tarama çeviri kataloğunu değiştirmez. P0 taslağı `../local-runtime/translation-planning-v0652-p0-triaged/` içindedir. Sıradaki P1 yetiştirme ailesi ayrı bir `--family objects/farmables` paketi olarak hazırlanabilir.

## Kullanım

1 Ekim 2026 kullanıcı tercihiyle sıradaki çeviri işi diyaloglardır. `dialog`, `npcs` ve `radiomessages` aileleri ile nesnelerin konuşma alanları P1'e yükseltildi. İlk taslak `--family dialog`, ikinci taslak `--family radiomessages` ile hazırlanır. Görev ve kritik uyarıların P0 önceliği korunur; `review` ve `lua_review` kayıtları görünürlük kanıtı olmadan çeviri havuzuna taşınmaz. Yetiştirme ve kablolu sistemlerin kalanları daha sonraki kapsamdır. Paket değiştikçe güncel dosya ve sıra checkpoint'te belirtilir.

Repo kökünde, UTF-8 Python ortamında:

```powershell
$env:PYTHONUTF8 = '1'
python tools/plan_translation.py --source ../local-runtime/fu_source --output ../local-runtime/translation-planning-next
```

`queue.json` bütün kalan structured alanları ve Lua inceleme kayıtlarını içerir. Eski auditin 20/100 örnek sınırı bu çıktıya uygulanmaz. `summary.md` öncelik ve aile toplamlarını gösterir. `packet.json` ilk aday paketidir. Varsayılan yaklaşık 500 alan / en fazla 350 bağlam grubudur; aile küçükse kota doldurulmaz. Tek grup sınırı aşıyorsa araç durur, yüksek öncelikli grubu atlayıp düşük önceliğe geçmez. Aynı çıktı klasörüne ikinci kez yazmayı reddeder; başlanmış çeviri ezilmez.

Bir aileyi seçmek için özet rapordaki tam aile değerini ver:

```powershell
python tools/plan_translation.py --source ../local-runtime/fu_source --family objects/crafting --output ../local-runtime/translation-planning-machines
```

## Luna için paket

1. `selection.family`, kaynak pini ve `inputs` hashlerini kontrol et. Adayın bütün ailenin kaç alanını içerdiği raporda ayrı yazılıdır.
2. `direct_dependencies` içindeki script/config bağlantılarını, `related_review_rows` içindeki ek adayları ve ailenin kuyrukta kalan alanlarını incele. Bağlantılar bir adım derinlikte ipucudur; Lua'nın dinamik dosya adları, temel oyun ve harici mod dosyaları ayrıca araştırılır. Otomatik tarama bütün bir sistemin bulunduğunu kanıtlamaz.
3. Tarif/araştırma/görev/dükkân/yerleşim gibi canlı erişim ve görünürlük kanıtını `runtime_review.evidence` alanına `{ "source": "dosya veya kaynak bağlantısı", "note": "hangi bağlantıyı kanıtladığı" }` biçiminde ekle; incelemeden sonra `reviewed=true` yap. Her grubun `runtime_evidence` listesine o grubun dayanağını yaz.
4. Her grup `en`, bütün `occurrences`, bağlam anahtarı, birebir kaynak eşleşen `tm_suggestions` ve ilgili `locked_terms` ile gelir. Türkçe alanı boştur. Aynı İngilizce metin farklı aile, konuşmacı veya inceleme sesiyle otomatik birleştirilmez. Belgeli TM istisnası bulunan kaynaklar alan başına ayrılır. Grup birleştirmesi yine insan onayı gerektirir; uygun bulduğunda `context_reviewed=true` yap.
5. Mevcut karşılığı kullanırken konuşmacı ve anlamı doğrula; TM önerisinin bulunması otomatik onay değildir. Çakışmalı önerileri ve bütün ilgili LOCKED bağlamlarını değerlendir. Çeviriyi `tr` alanına yaz. Sadece `tr`, `context_reviewed`, `runtime_evidence`, `runtime_review` ve `measurements` düzenlenir. Yanlış gruplama varsa aracı/kuralı düzeltip yeniden üret; alan listesini elle değiştirme.
6. Sol'a göndermeden önce teknik ön denetimi çalıştır:

```powershell
python tools/plan_translation.py --source ../local-runtime/fu_source --check-packet ../local-runtime/translation-planning-next/packet.json
```

Bu komut temiz pinli kaynağı yeniden tarar; kaynak/katalog/kurallar değişmişse veya paket alanı kayıp/fazlaysa reddeder. Tek Türkçe karşılığı grubun bütün alanlarına bellekte uygular; mevcut katalog ve manifestlerle birlikte proje QA'sını çalıştırır. Sayı, kontrol kodu, renk, satır sonu, terminoloji ve TM kuralları geçerlidir. Boş çeviri, aynı kalan İngilizce veya eksik insan bağlam onayı reddedilir. Kanıt notlarının içeriği insan tarafından doğrulanır; script bir metin notundan gerçek oyun erişilebilirliğini ispatlamaz.

Tam metni bir LOCKED `mode=preserve` kaydıyla eşleşen özel ad, yalnız ad alanında (`shortdescription`, `title`, `displayName`, `speciesName`) kaynakla aynı kalabilir. `Bella Morte` ve `Kramil` bu kapsamdadır. Aynı kural bir açıklama cümlesinin İngilizce bırakılmasına izin vermez; insan bağlam incelemesi ve bütün QA kuralları yine gerekir.

1 Ekim Sol incelemesinde `objects/farmables/fu_scriptedfarmableexample/fu_scriptedfarmableexample.object` normal oynanışa bağlanmayan geliştirme örneği olarak mevcut dışlama listesine alındı. Kaynakta bu kimliğe tarif, araştırma, satıcı, düşürme veya yerleşim bağlantısı yok; `printable=false`. Normal buğday nesneleri kapsamda kalır. Diğer bir nesnenin statik bağlantısının bulunamaması tek başına ölü asset kararı değildir; dinamik, temel oyun ve harici mod bağlantıları ayrıca inceleme notunda belirtilir.

## Sol ve yayın

Sol her yeni/değişen bağlam grubunu anlam, doğal Türkçe ve karakter sesi açısından inceler. Aynı çevirinin kullanıldığı bütün alanların bağlama uyumunu kontrol eder. Dil incelemesi sonrasında mevcut sürüm manifesti, allowlist, exact-source kapısı, tam build, CI ve oyun içi LQA akışı sürer. Ön denetim bu kapıların yerine geçmez ve paketi kataloğa otomatik eklemez.

`measurements` alanında gerçek `translation_minutes`, `review_minutes`, `reviewed_units`, `corrected_units` ve `lqa_status` tutulur. En az bir normal paketle aynı kapsamda karşılaştırılmadan hız yüzdesi çıkarılmaz. Düzeltme oranı = düzeltilen grup / incelenen grup; hız = 100 grup başına toplam dakika. Gruplama tasarrufu, ölçülmüş çalışma süresi tasarrufu değildir.

CI audit çıktısına kuyruk ve taslak paket ekler. Yerel varsayılan `planning_output/` Git tarafından dışlanır. Çalışma alanındaki paylaşılan `local-runtime/` çıktısı Luna ve Sol tarafından okunabilir; aynı paketi aynı anda düzenlemeyin, inceleme öncesi ayrı bir kopya tutun.
