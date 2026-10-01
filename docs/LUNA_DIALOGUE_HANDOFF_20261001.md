# Luna: diyalog öncelikli sonraki kapsam

Kullanıcı 1 Ekim'de diyalogların önce çevrilmesini istedi. Mevcut politika P0 kritik yönlendirmeyi korur; diyaloglar P1'dir. Bu çalışma yeni diyalog çevirisi içermez.

## Güncel temel ve çalışma yolu

- Çalışma checkout'u: `../local-luna/`. Aynı Git deposunun Luna dalı; değişiklik yapmadan önce `git status` ve checkpoint'i oku.
- Katalog: `0.66.0-beta`, 14.617 alan. Yeni eklenen P0 yer imi ve ilk P1 yetiştirme dilimi 454 alandır; önceki 14.163 alan korunur.
- FU 6.5.8 kaynağı: `../local-runtime/fu_source/`, pin `bb58383c0d16c1152e3439e606b39ff82288b586`. Kaynak checkout'unu değiştirme.
- Yerel paket: `../local-runtime/build-v066-20261001-final/FU_Turkce_v0.66.0_Beta.zip`; güncel yerel kanıt `package-evidence.json`. Build, ZIP, 241 regresyon ve kaynak kapıları PASS; uzak yayın ve oyun içi LQA ayrı durumlardır. Generated `FU_Turkce/`, `dist/` ve raporları elle değiştirme.

## Sıra

| Sıra | Taslak yolu | Alan / bağlam grubu | Kapsam |
|---|---|---:|---|
| 1 | `../local-runtime/translation-planning-v066-dialog-first/packet.json` | 376 / 350 | 46 brewmaster, 110 catconverse, 220 converse alanı |
| 2 | `../local-runtime/translation-planning-v066-radio-next/packet.json` | 350 / 350 | 11 radyo mesajı asseti; 70 grupta birebir TM önerisi |

İlk paket `dialog` ailesinin tamamı değildir; ailenin kalan toplamı 2.286 alan / 2.149 bağlam grubudur. Radyo ailesinin toplamı 848 alan / 848 gruptur. Paketleri doldururken aynı ailede kaynak veya hitap edilen ırk bağlamını birleştirme.

Her iki taslak aynı katalog tabanıyla hazırlanmıştır. **Önce birinciyi tamamla ve Sol'a incelet.** Birinci paketin kataloğa alınması, ikinci paketin katalog hashini geçersiz yapar: ikinciye başlamadan önce güncel katalogla `--family radiomessages` taslağını yeni bir çıktı klasöründe yeniden üret. Eski dosyanın girdi hashlerini elle değiştirme. Bu iki taslak paralel katalog düzenleme yetkisi veya otomatik çeviri onayı değildir.

## Kaynak bağlamı ve erişim incelemesi

Taslaklar `DRAFT_CONTEXT_REVIEW_REQUIRED`; `tr` boş, bağlam ve runtime onayı verilmemiştir. `direct_dependencies=0`, runtime bağlantısı olmadığı anlamına gelmez: `/dialog/file.config:section` referansları ve radyo mesajı kimliği tetikleyicileri ayrıca incelenmelidir.

İlk kaynak ipuçları:

- `npcs/brewmasterciv.npctype` içinde `/dialog/brewmaster.config:converse` ve diğer konuşma dalları var. `tenants/vanillaraces/brewmaster.tenant` bu NPC tipini kullanır. Şarap/bira uzmanı sesini ve kiracı davranışlarını doğrula; bu statik bağlantı oyunda her repliğin denendiği anlamına gelmez.
- `npcs/catvillager.npctype` içinde `/dialog/catconverse.config` için `breakObject`, `greeting` ve `converse` referansları var. Kedi konuşmacının sesi, hitap edilen ırk ve çağıran kiracı/yerleşim ayrıca doğrulanmalı.
- `npcs/fuvillageguard.npctype`, `npcs/newhumansurvivor.npctype` ve Nightar NPC tipleri `/dialog/converse.config` kullanır. FU patch katmanı ve vanilla fallback birlikte değerlendirilir. İlk paket `converse/avian/radien/13` alanında biter; ailenin diğer konuşma dalları sonraki dilimlerde kalır.
- Radyo metninin oyuncuya gösterilmesi için yalnız `type=tutorial` veya metin dosyası yeterli değildir. Her mesaj kimliğini kullanan pickup, biome, quest veya `player.radioMessage` zincirini araştır; konuşmacıyı portre ve çağıran script ile eşleştir.

Güncel kuyruk 43.784 confirmed, 3.049 review, 162 Lua inceleme adayı içerir. P0 confirmed/review sıfırdır; P1 review 2.718 ve P1 Lua 106 adayın tümünün görünür olduğu varsayılmaz. İlgili konuşma zincirlerindeki belirsiz adayları önce kaynak dayanağıyla incele; teknik ID, portre, ses veya callback değerini çevrilecek metin sayma. Kaynak dışındaki vanilla/harici mod dayanağı eksikse bunu açıkça kaydet.

## Çeviri ve teslim

1. Paket `inputs` hashlerini, kaynak pinini ve `selection.family` değerini doğrula. `tr`, `context_reviewed`, `runtime_evidence`, `runtime_review` ve gerçek `measurements` dışında paket alanlarını değiştirme.
2. Önce bağlam: `converse/<konuşmacı>/<muhatap>/<indeks>` gibi pointerları, NPC çağıran dosyaları ve patch kökenini oku. Teknik veya görünmeyen aday için görünürlük kuralını kaynak dayanağıyla düzelt ve taslağı yeniden üret; sessizce kapsamdan silme.
3. LOCKED ve birebir TM önerilerini kaynak/konuşmacı uyumuyla kontrol et. Öneri otomatik kabul değildir. Yeni tekrarlı terimi belirsizse REVIEW olarak, kesin karşılığı doğrulandıysa LOCKED için gerekçesiyle Sol'a bildir.
4. Kaynakta olmayan şaka, küfür, bilgi veya lore ekleme. Floran, Glitch ve diğer konuşmacı seslerini koru. Placeholder, renk, sayı ve satır sonlarını değiştirme. Eksik vanilla metin için İngilizce fallback uydurma.
5. `runtime_review.evidence` ve her grubun `runtime_evidence` kaydını gerçek kaynak dosyası ve açıklamayla tamamla. Görsel LQA yapılmadıysa `NOT TESTED` durumunu koru; kaynak ipucunu oyun testi gibi yazma.
6. Gerçek çeviri süresini kaydet. İlk paket için süre tahmini veya hız yüzdesi uydurma. Sol her yeni/değişen Türkçe bağlam grubunu inceler.
7. `local-luna` kökünde UTF-8 Python ortamıyla ön denetim:

```powershell
$env:PYTHONUTF8 = '1'
& '../local-runtime/venv/Scripts/python.exe' tools/plan_translation.py --source ../local-runtime/fu_source --check-packet ../local-runtime/translation-planning-v066-dialog-first/packet.json
```

Tamamlanan aday, ön denetim sonucu, gerçek süreler ve belirsiz bağlam notlarıyla Sol'a teslim edilir. İlk paketin dil incelemesi ve kaynak kapısı bitmeden katalog/sürüm manifestini değiştirme veya yayın yapma. Beyin işlemleri gerekiyorsa ana çalışma alanındaki `beyin-project.ps1` yardımcısını kullan.
