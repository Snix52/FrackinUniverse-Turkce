# Luna: güncel diyalog devir notu — 1 Ekim 2026

## Güncel temel

İlk diyalog paketi Sol incelemesiyle **v0.67.0-beta** kataloğuna alındı: 376 alan / 350 bağlam grubu. Toplam **14.993 alan**, **606 LOCKED**. Önceki 14.617 alan aynen korundu. Düzeltmelerin tamamı [dil inceleme kaydında](reviews/dialogue-20261001.json) önce/sonra/gerekçeleriyle kayıtlı: 25 grup / 27 alan / tekrarlar dahil 32 cümle düzeltmesi. [LQA kaydı](LQA_V067_20261001.md) kaynak sınırlamalarını açıklar.

Çalışma checkout’u `../local-luna/`; Sol checkout’u `../local-repo/`. Değişiklikten önce temiz Git durumu ve checkpoint’i oku. Kaynak `../local-runtime/fu_source/`, FU 6.5.8 pini `bb58383c0d16c1152e3439e606b39ff82288b586`. Kaynak pinini değiştirme.

## Sıra: diyalog önceliği sürüyor

| Sıra | Güncel boş taslak | Alan / grup | TM önerili grup |
|---|---|---:|---:|
| 1 | `../local-runtime/translation-planning-v067-dialog-next/packet.json` | 380 / 350 | 30 |
| 2 | `../local-runtime/translation-planning-v067-radio-next/packet.json` | 350 / 350 | 71 |

v066-dialog-first paketi tamamlandı; üzerinde devam etme. Eski v066 radio taslağı bayat. Güncel iki taslak aynı katalog/LOCKED hashleriyle hazırlandı: önce diyalog taslağını tamamla, Sol’a incelet. Onun entegrasyonu radyo taslağını bayatlatır; radyo çevirisine başlamadan yeni çıktı klasöründe tekrar hazırla. Hashleri elle değiştirme.

Yeni diyalog paketi FU `dialog/converse.config.patch` içindeki Avian konuşmalarının devamı ve diğer konuşmacı/muhatap dallarından gelir. Kaynak temel vanilla `converse.config` bu checkout’ta yoktur; patch kaynağını doğru yaz, statik NPC referansını canlı oyun kanıtı gibi kaydetme. Aynı İngilizce repliğin farklı ırk/konuşmacı bağlamını birleştirme.

Kalan diyalog ailesi 1.910 alan / 1.799 grup; radyo ailesi 848 alan / 848 grup. Güncel confirmed kuyruğu 43.408 (P1=7.833, P2=12.133, P3=23.442), ayrı review 3.049, Lua 162. Bunlar onaylı cümle veya oyun görünürlüğü sayısı değildir.

## Çeviri ve teslim

1. Paket `inputs`, pin ve `selection.family` değerlerini doğrula. Yalnız `tr`, `context_reviewed`, `runtime_evidence`, `runtime_review`, gerçek `measurements` düzenlenebilir. Başlık DRAFT olarak kalır; Sol dil onayı ayrı rapordadır.
2. Her bağlamı konuşmacı ve muhatap türü, NPC çağıran dosyaları ve kaynak patch değeriyle oku. `/dialog/file.config:section` bağlantıları planner’ın `direct_dependencies=0` sonucundan bağımsız incelenmelidir.
3. Yeni LOCKED kavramları: **kedi topluluğu**, **kavrayıcı başparmak**, **Yıldız Gözlemcisi**, **arkoloji**, **Siberuzay**, **Muz Romu**, **haiku**. Big Ape, Miniknog, Mos Lunan, Lemurian, Elysian, Zyen, Azriel, Assassinii, Gladiatii, Thornwing, X'i özel adları korunur. Elysian çoğulunu İngilizceden taşımadan Türkçe çek. Matriarch gibi bağlama göre anlam değiştiren unvanlarda genel kilit uydurma.
4. TM önerisi otomatik onay değildir. Kaynakta olmayan lore, şaka veya bilgi ekleme; anlamı, olumsuz soruyu, zamir referansını ve muhatabın özelliklerini koru. Her grubun gerçek kaynak dayanağını yaz.
5. Radyo mesajları için mesaj ID’sini çağıran script, pickup, biome veya görev zincirini ve portreyle konuşmacıyı doğrula. Teknik ID, callback ve portre yolunu çevirme.
6. Canlı görsel oyun testi yapılmadıysa **LQA NOT TESTED** yaz. Gerçek çeviri süresini kaydet; tahmin üretme. Katalog/manifest/generated çıktıları değiştirmeden adayı Sol’a teslim et.

Ön denetim (`local-luna` kökünde):

```powershell
$env:PYTHONUTF8 = '1'
& '../local-runtime/venv/Scripts/python.exe' tools/plan_translation.py --source ../local-runtime/fu_source --check-packet ../local-runtime/translation-planning-v067-dialog-next/packet.json
```

Yerel ZIP/build sonucu ve code commit checkpoint’te kayıtlıdır. Uzak yayın ve oyun kurulumu ayrı adımlardır. Beyin işlemleri ana proje klasöründeki `beyin-project.ps1` yardımcısıyla yürütülür.
