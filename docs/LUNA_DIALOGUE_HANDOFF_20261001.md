# Luna: diyalog öncelikli güncel devir — v0.70

## Tamamlanan dilim

Dördüncü diyalog paketi Sol incelemesiyle v0.70.0-beta kataloğuna alındı: **375 alan / 350 bağlam**. Önceki 15.772 satır korunarak toplam **16.147**. **18 yeni LOCKED, toplam 637**. 33 bağlamda 37 alan; tekrarlar dahil **38 cümle/kısa ifade**, bağlam başına 34 değişti. Tam önce/sonra ve gerekçeler [inceleme kaydında](reviews/dialogue4-20261001.json), sınırlar [LQA kaydında](LQA_V070_20261001.md).

Çalışma checkout'u `../local-luna/`; Sol `../local-repo/`. Git durumunu ve checkpoint'i oku. FU 6.5.8 `../local-runtime/fu_source/`, pin `bb58383c0d16c1152e3439e606b39ff82288b586` korunur.

## Sıradaki paket: ne çevriliyor?

**`../local-runtime/translation-planning-v070-dialog-next/packet.json`**: **352 alan / 350 bağlam**, 57 grupta birebir TM önerisi. Skath sohbetlerinin devamı, Thelusian/Veluu sohbetleri ve ırklara göre selamlaşmalar; ayrıca Slime, ElDuukhar, Fenerox ve mürettebat replikleri. Kaynak dağılımı: `converse.config.patch` **256**, `fuslimeperson.config` **72**, `elduuconverse.config` **11**, `fenerox.config` **8**, `crewmember.config` **5** alan. Patch ve doğrudan kaynak provenance'ları ayrı korunur. Konuşmacı/özel dosya dağılımı: **apex: 1, avian: 3, dialog/crewmember.config: 5, dialog/fenerox.config: 8, dialog/fuslimeperson.config: 72, elduukhar: 11, fenerox: 28, floran: 1, fudarkizku: 13, fuizku: 13, fumantizi: 4, glitch: 1, human: 7, hylotl: 1, juux: 28, mantizi: 4, nightar: 25, novakid: 5, shadow: 3, skath: 59, thelusian: 25, veluu: 35**. ID'lerin oyun görünen adlarını ilgili species dosyasından doğrula; özel dosyaların `default` anahtarını bir ırk adı sanma.

İlk alan `/converse/skath/human/11`, son `/converse/default/default/6`. Konuşmacı/muhatap bağlamları ayrıdır. Diyalog ailesinde **756 alan / 749 bağlam** kaldı; confirmed toplam **42.254** (P1=6.679), review **3.049**, Lua **162**. Bunlar onaylı cümle/canlı erişim sayıları değildir.

Eski v069-dialog-next tamamlandı; üzerinde devam etme. Eski radio paketi yeni katalog/LOCKED girdileri nedeniyle bayat. Radyo ailesine geçerken yeni klasöre güncel kaynakla hazırla; hashleri elle değiştirme.

## Çeviri ve teslim

1. Paket inputs/basis, kaynak pini ve family=dialog doğrulanır. Yalnız tr, context_reviewed, runtime_evidence, runtime_review ve gerçek measurements değişebilir. DRAFT başlığı kalır; Sol dil onayı ayrı raporda tutulur.
2. Her pointerın konuşmacı ve muhatap türünü, EN değerini ve çağıran NPC/script dosyalarını oku. Converse.config temel vanilla dosyası FU checkout’unda yoktur; patch değeri veya genel NPC referansı canlı oyun kanıtı sayılmaz. ElDuukhar köylüsü kendi elduuconverse.config dosyasını kullanır; base converse.config yalnız breakObject için bağlıdır. Erişimi belirsiz dalı olumlu kanıt gibi yazma.
3. LOCKED ve TM, bağlama göre doğrulanır; öneri otomatik onay değildir. Yeni kavramlar Avolite Kristali, Glif, Su Ejderhası, Balık Surat, Pofuduk Popo; Pharitu, Myphis, Ma'ez ve Ruin adları korunur. Ruin yalnız The Ruin özel varlık ifadesiyle kilitlidir; genel harabe anlamını buna zorlama. Glif için beş eski sembol istisnası tam EN/TR alanına bağlıdır, yeni repliklerde kullanılacak genel izin değildir.
4. Floran’ın s tıslamasını uygun Türkçe s sesleriyle aktar; rastgele ünlü uzatma ekleme. Fenerox ve Pharitu’nun kısa/kırık ifadelerini koru. Özne ve zamirleri, kutsallık karşılaştırmalarını, olumsuzluk ve soru anlamını doğrula. Kaynakta olmayan lore ekleme; teknik ID/portre/callback çevirme. Mantizi’de hitapları özel kişi sanma: Aunt Nell=koku, ball of chalk=yürüyüş, Pope of Rome=ev, bu para/vergi bağlamında saucepan lid=para. Kaynak argo sözlükleri ve çıkarımlar inceleme kaydında; başka anlamdaki kullanımlara kör TM uygulama. Sefton REVIEW, kesin anlamı doğrulanana kadar kaynak hitabı korunur; özel ad olduğu iddia edilmez. Pyreite, Pirit değildir; mevcut Pyreite Körisi adı kullanılır. Barbatus, CySol, Zaibatsu ve Pyreite yeni LOCKED kayıtlarıdır. Almost/may/capable kiplerini ve your/my zamirlerini kaybetme.
5. Yeni LOCKED kurallarını `docs/TERMINOLOGY.md` ve `tools/locked_terms.json` üzerinden oku: Matriarch/Greenfinger özel unvanları, Izku (Ikzu kaynak yazım hatası), Conshak ayini, Tenshae yara izi, Perde, Kaynak yeminleri ve Işıkta Yaşayan. Genel rat matriarch/source/veil anlamlarını lore'a zorlama. İki exact eski istisnayı yeni satıra kopyalama. Novakid ışık göndermesinde konuşmacı/muhatap ve my/your/us zamirlerini doğrula.
6. Her gruba gerçek kaynak dosyası ve açıklama ile kanıt yaz. Canlı görsel LQA yapılmadıysa NOT TESTED kalır. Gerçek çeviri süresini kaydet; tahmin üretme. Katalog/manifest/generated çıktıları değiştirmeden Sol’a teslim et.

Ön denetim, local-luna kökünde:

```powershell
$env:PYTHONUTF8 = '1'
& '../local-runtime/venv/Scripts/python.exe' tools/plan_translation.py --source ../local-runtime/fu_source --check-packet ../local-runtime/translation-planning-v070-dialog-next/packet.json
```

Build/yayın sonuçları checkpoint’te yer alır. Generated çıktıları mevcut CI yayımlar; elle düzenleme. Beyin işlemleri ana proje kökündeki beyin-project.ps1 yardımcısıyla yapılır.
