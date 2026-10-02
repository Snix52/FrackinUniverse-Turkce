# Sürüm notları arşivi

README’deki geçmiş kapsam kayıtları burada korunur. Bu liste tüm ara sürümlerin eksiksiz changelog’u değildir. Güncel yayın bilgisi [paket kanıtındadır](../../dist/build-evidence.json); ayrıntılı işlem geçmişi [çalışma günlüğündedir](FU_SESSION_CHECKPOINT_20261001.md).

## v0.45.1 bakım paketi

Lua görünür string güvenliği, LOCKED karma-varyant kontrolü, alan-bağlı kontrol kodu istisnaları, beş zemin etiketi, iki Mech yakıt uyarısı ve görev dili düzeltildi. PR QA salt okunur; generated çıktı değişiklikleri kaynak güncellemesi yerine kabul edilmez. Ayrıntılar: [bakım raporu](../audits/QA_HARDENING_20260922.md).

## Son tamamlanan çalışma

**v0.70.0** ile 375 NPC diyalog alanı eklendi; 350 konuşmacı/muhatap bağlamı incelendi. Hylotl, Pharitu, Mantizi, Nightar, Novakid, Shadow ve Skath sohbetleri yerelleştirildi. Katalog toplamı 16.147 alan, terim sözlüğü 637 LOCKED kayıttır. Önce/sonra düzeltmeler [inceleme raporunda](../reviews/dialogue4-20261001.json), kaynak ve oyun içi kontrol sınırları [LQA kaydında](../lqa/LQA_V070_20261001.md) bulunur.

**v0.69.0** üçüncü NPC diyalog diliminde 399, **v0.68.0** ikinci dilimde 380, **v0.67.0** ilk dilimde 376 alan ekledi. **v0.66.0** Bilim Karakolu yer imi ve ilk yetiştirme diliminde 454 alan ekledi. Diyalog önceliği sürer. Teknik doğrulama, her repliğin canlı oyunda denenmiş olduğu anlamına gelmez.

v0.46 Irklar ve SAIL/AI confirmed kapsamı kapatıldı.

- 53 canlı asset
- 129 oyuncuya gösterilen alan
- 89 SAIL/AI alanı
- 20 oynanabilir ırkta 40 species alanı
- Irklar ve SAIL/AI confirmed borcu: 0

v0.46.1-v0.46.3 bakımında Jungle ve görev/konum görünen adları geriye dönük denetlendi. **v0.47.0** ile 66 bitki assetindeki **170** oyuncu-yüzü ad, açıklama ve Floran/Glitch inceleme metni Türkçeleştirildi. `.biome/friendlyName` ve `.liquid/description` gibi runtime görünürlüğü doğrulanmayan metadata alanları çeviri borcundan çıkarıldı.

**v0.48.0** ile koyu, açık renkli ve süslü ahşap ailelerindeki 32 assetin **151** adı, açıklaması ve ırka özgü inceleme metni Türkçeleştirildi. **v0.49.0** ile Aen, oyuncak ev, Dynast, ham ahşap ve yıpranmış ahşap ailelerindeki 44 assetin **227** alanı çevrildi. Taş ve diğer karo aileleri ayrı kapsam olarak tutulur.

**v0.50.0** ile 207 arıcılık assetindeki **537** görünür alan çevrildi. Arı türleri ve koloni rolleri, petekler, çerçeveler ve arıcılık arayüzü aynı terim düzeniyle ele alındı.

**v0.51.0** ile 33 platform assetindeki **99** görünür alan çevrildi; Floran, Glitch ve Novakid inceleme metinleri bu kapsama dahildir.

**v0.52.0** ile 126 taş, toprak ve yapı bloğu assetindeki **318** görünür alan çevrildi. Sabitlenmiş FU kaynak sürümü korunur.

**v0.53.0** ile 14 Peglaci yapı, kablo ve Pykrete assetindeki **66** görünür alan çevrildi. Sabitlenmiş FU kaynak sürümü korunur.

**v0.54.0** ile 18 Honey ailesi assetindeki **71** görünür alan çevrildi. Sabitlenmiş FU kaynak sürümü korunur.

**v0.55.0** ile metal, teknoloji, kereste, cam ve pencere yapı ailelerindeki 177 assetin **466** görünür alanı çevrildi. Sabitlenmiş FU kaynak sürümü korunur.

**v0.56.0** ile kalan karo malzemeleri ve karo modlarındaki 197 assetin **365** görünür alanı çevrildi. Sabitlenmiş FU kaynak sürümü korunur.

**v0.57.0** ile yürüyen ve uçan canavar ailelerindeki 239 assetin **477** görünür ad ve açıklama alanı çevrildi. Sabitlenmiş FU kaynak sürümü korunur.

**v0.58.0** ile kalan arı, sürünen yaratık, küçük canlı, balık, Pandora ve parçalı yaratık ailelerindeki 261 assetin **522** görünür alanı çevrildi. Sabitlenmiş FU kaynak sürümü korunur.

**v0.59.0** ile kalan görünür canavar ve beceri adları ile açıklamalarındaki 259 assetin **341** alanı çevrildi. Oyun içinde görünmeyen iki dahili yardımcı yaratık kapsam dışında tutuldu; sabitlenmiş FU kaynak sürümü korunur.

**v0.60.0** ile Kadim ve Precursor mini-biome nesnelerindeki 196 assetin **536** görünür ad, açıklama ve arayüz alanı çevrildi. `Precursor`, `Cthulhu`, `Erchius` ve `Lunari` özel adları korunur.
