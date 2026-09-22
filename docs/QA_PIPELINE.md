# Doğrulama ve paket kanıtı

## Tek kaynaklar

- Oyuna uygulanan structured çeviriler: `tools/ceviriler.json`.
- Sürüm manifestleri: `tools/*_translations.json`. Ana katalogdaki aynı asset/pointer ile eşit olmalıdır. Ham Lua manifesti kendi şemasıyla denetlenir.
- Terminoloji kararları: `tools/locked_terms.json`. Bütün LOCKED kayıtlar genel validator tarafından okunur. `docs/TERMINOLOGY.md` bu dosyadan üretilir; `tools/TERIMLER.txt` yalnız yönlendirmedir.
- Asset kapsamı, devre dışı içerik ve kural envanterleri: `tools/rules/*.json`. CLI ve mevcut source-test/replace politikası korunur.
- FU revision pini: `tools/kaynaklar.json`. Build ve remaining audit aynı kaynağı kullanır.

Terminolojiyi değiştirdikten sonra `python tools/qa_integrity.py --write-docs` çalıştırılır. LOCKED tam kaynak adlarının kanonik karşılığı zorunludur. Birden fazla onaylı anlamı olan tam kaynak adları açık asset/pointer/context istisnası olmadan geçmez. Cümle içindeki çok sözcüklü terimlerde sözlüğün bilinen yanlış varyantları aranır; Türkçe çekimlerin ve bütün serbest metinlerin eksiksiz anlamsal doğruluğu iddia edilmez.

## İstisnalar

Translation Memory istisnaları kaynak metin, asset, pointer, Türkçe karşılık ve gerekçeyle sınırlandırılmıştır. Yeni üçüncü bir karşılık, aynı İngilizce metin istisna dosyasında bulunsa bile reddedilir. Research, Electronics, Incinerator gibi gerçek context ayrımları korunur.

İki TAB istisnası, `plebiancap.questtemplate` ve `nightarshortsword.activeitem` içindeki cümle arası kaynak TAB'ının normal boşluğa düzeltilmesidir. Kaynak ve hedefin tamamı bağlanır; genel `allow_tab_fix` bayrağı yeni bir istisna yaratmaz. JSON'da `\t` olarak kodlanan gerçek U+0009 ile bir string içindeki literal ters eğik çizgi+t birbirine karıştırılmaz.

İkon koruması mevcut corpus'taki U+E024 ve private-use UI glyphleri içindir. Normal Türkçe Unicode harfler ikon sayılmaz. Mevcut renk/kontrol/printf/süslü parantez/değişken/normal sayı ve satır sonu kontrolleri korunur. İşaretli sayılar yüzde konumu ve ondalık ayırıcı normalizasyonuyla, işaret dahil karşılaştırılır.

## Gerçek build kanıtı

`build_validate.py` bütün kontrolleri başarıyla bitirince `build_output/validation.json` oluşturur. Bu dosya mod ağacının **dışındadır**. Gerçek source checkout'u verilen build, git HEAD'in pin ile aynı olduğunu, kaynakta izlenen dosyaların değiştirilmediğini ve mevcut source pointer/patch simülasyonlarını doğrular. Kaynak verilmeden yapılan fixture kontrolü `source_validation: NOT RUN` yazar ve dağıtım kanıtı üretmek için yeterli değildir.

FU'nun doğrudan sahip olmadığı vanilla/katmanlı alanlarda mevcut ledger provenansı korunur. Bu alanlar bağımsız bir vanilla oyun çalıştırması gibi raporlanmaz. Oyun içi test hiçbir otomatik adımla yapılmış sayılmaz.

Paketleme scripti gerçek build raporunu kaynak SHA, katalog SHA256, mod ağacı SHA256 ve güncel pin ile eşleştirir. ZIP CRC'si, dosya envanteri, dosya baytları, test/replace eşleşmeleri ve alan/asset/raw sayıları yeniden denetlenir. Kök `FU_Turkce` ağacı aynı build ile bayt bazında eşit olmalıdır. ZIP sırası, timestamp ve izinler sabittir; aynı içerik ve aynı paketleme ortamı yeniden aynı ZIP'i üretir.

`dist/build-evidence.json`, `tools/test_raporu.json` ve `tools/GELISTIRME.txt` bu doğrulanmış paketten birlikte üretilir. Eski raporlar sayısal girdi olarak kullanılmaz. `source_commit` çeviri/build kaynak commit'idir; `upstream_commit` ayrı FU pinidir. Henüz oluşturulmamış generated commit SHA'sı tracked dosyalara yazılmaz. Generated commit oluşturulup push edilince yalnız GitHub step summary'ye yazılır.

## Publication yarışları

Main workflow concurrency eski işi iptal eder. Publication scripti ayrıca başlangıç kaynak SHA'sını tutar, generated commit öncesinde ve push öncesinde remote main'i yeniden fetch eder. Daha yeni kaynak varsa skip eder; rebase veya force-push yoktur. Push reddedilirse ancak remote'un gerçekten ilerlediği doğrulanınca skip edilir. Yetki, ağ veya koruma hataları sessiz başarıya çevrilmez. Generated commit `[skip ci]` kullanır. İnsan eliyle generated-only değişikliklerin sessizce atlanmaması için main build trigger'ında paths-ignore kullanılmaz. `check_generated_changes.py`, incoming diff içindeki generated değişikliğini çıktı ağacı yenilenmeden önce reddeder.

Remaining scope workflow ana, raw ve sürümlü katalog değişikliklerinde çalışır. Raporu workflow artifact'ına yükler; `main`e ikinci bir generated commit yazan yarışçı oluşturmaz.

## Komutlar

```bash
python -m compileall -q tools
python -m unittest discover -s tools/tests -v
python tools/qa_integrity.py
python tools/build_validate.py --source-dir fu_source --output build_output
# Kök kurulum ağacını yeni build ile eşitle.
rm -rf FU_Turkce && cp -a build_output/FU_Turkce FU_Turkce
python tools/write_build_evidence.py --zip dist/FU_Turkce_v0.30.0_Beta.zip \
  --output dist/build-evidence.json --create-zip --refresh-tracked \
  --translation-source-commit "$(git rev-parse HEAD)" --workflow-run-id local
unzip -t dist/FU_Turkce_v0.30.0_Beta.zip
python tools/audit_remaining.py --source fu_source
git diff --check
```

Yerel kaynak ağacı FU pininde gerçek bir git checkout'u olmalıdır. `build_output` önceden varsa üretici onu yanlışlıkla ezmemek için durur. Yeni sürümde paket adı yeni sürüme göre seçilir; CI bunu katalogdan hesaplar.

`in_game_lqa: NOT TESTED` korunur. Yapılacak manuel kontroller: `docs/LQA_CHECKLIST.md`.

## v0.45.1 ek güvenlik sözleşmesi
`tools/qa_raw.py` Lua parçalarını çalıştırmadan string ve kod parçalarına ayırır. Raw manifestte her replacement için `text_literals` sıfır tabanlı görünür string indeksleridir. Diğer stringler ve bütün string-dışı kod/yorumlar exact kalır. `display_en/display_tr` açıklama metadata'sıdır; gerçek QA bu alanlara güvenmek yerine ayrıştırılan gerçek Lua stringleri üzerinde çalışır. Raw format düzeltmesi için genel bypass yoktur.

Gerçek raw stringler, `/replacements/<index>/literals/<slot>` bağlamıyla LOCKED ve ortak TM kontrolüne girer. Research eylemi yalnız tek gerçek widget bağlamında tanımlıdır. Doğru kanonik terim, aynı cümledeki ayrı yasaklı varyantı maskelemez; kanonik ifadenin içinde kalan kısa yasaklı alt-sözcük yanlış pozitif sayılmaz.

Kontrol-token farklılıkları `text_integrity.json/control_exceptions` içinde tam satıra bağlıdır. Kaynak/hedef/asset/pointer değişince istisna geçersizdir. `[Fire]`, `<item>` ve `[(pause)...]` korunur; görünür `[Tile]` etiketi yalnız beş belgeli stat adı için çevrilir.

Raw manifest pinleri merkezi FU piniyle karşılaştırılır. Full-source build, raw/runtime kaynak blob SHA'larını gerçek dosya baytlarıyla karşılaştırır; bütün raw şablonlar pinned build ile aynı metni üretmelidir.

`pr-qa.yml` tüm PR değişikliklerinde salt okunur çalışır; paket yayımlamaz, ref güncellemez ve credential saklamaz. PR'lar kaynak değişiklikleri taşır; `FU_Turkce/`, `dist/` ve generated raporlara doğrudan değişiklik kabul edilmez. Main build aynı kuralı çıktı yenilemeden önce uygular. Botun mevcut source-SHA yarış koruması korunur.

Test ortamı: Python 3.11 ve işletim sistemi Lua 5.4 kitaplığı. Ubuntu: `sudo apt-get install liblua5.4-0`. Lua kitaplığı yoksa davranış testleri atlanmaz, hata verir. Full-source build sonrasında `FU_TEST_MOD_DIR=build_output/FU_Turkce python -m unittest discover -s tools/tests -p 'test_lua_behavior.py' -v` komutu yeni üretilen Lua'yı da test eder. Bunlar Starbound API stub'larıyla yapılan testlerdir; gerçek oyun içi LQA değildir.

GitHub branch protection/required checks ayrı sunucu ayarıdır. Workflow eklemek tek başına zorunlu merge engeli oluşturmaz. Bu ayar, mevcut generated yayın botunun erişimi dikkate alınarak uygulanmalıdır.
