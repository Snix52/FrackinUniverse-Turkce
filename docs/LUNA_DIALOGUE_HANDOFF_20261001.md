# Luna: diyalog öncelikli güncel devir — v0.69

## Tamamlanan dilim

Üçüncü diyalog paketi Sol incelemesiyle v0.69.0-beta kataloğuna alındı: **399 alan / 350 bağlam grubu**. Önceki 15.373 alan aynen korunarak toplam **15.772** oldu. **4 yeni LOCKED**, toplam **619**. 44 grupta 45 alan, tekrarlar ve kısa konuşma ifadeleri dahil **50 düzeltme**; tüm önce/sonra ve gerekçeler [inceleme kaydında](reviews/dialogue3-20261001.json). [LQA kaydı](LQA_V069_20261001.md) kaynak erişimi sınırlarını içerir.

Çalışma checkout’u `../local-luna/`; Sol `../local-repo/`. Başlamadan Git durumunu ve checkpoint’i oku. FU 6.5.8 kaynağı `../local-runtime/fu_source/`, pin `bb58383c0d16c1152e3439e606b39ff82288b586` korunur.

## Sıradaki paket

**`../local-runtime/translation-planning-v069-dialog-next/packet.json`**: 375 alan / 350 grup, 137 grupta birebir TM önerisi. İlk alan `/converse/hylotl/skath/0`, son `/converse/skath/human/10`. Kaynak `dialog/converse.config.patch`; konuşmacı ve muhatap türü ayrı tutulur. Eski v068-dialog-next tamamlandı; onun üzerinde devam etme. Eski v067-radio-next yeni katalog ve LOCKED hashleriyle bayattır. Radyo ailesine geçerken güncel katalogla yeni çıktı klasöründe yeniden hazırla; hashleri elle değiştirme.

Diyalog ailesinde 1.131 alan / 1.099 grup kaldı. Confirmed kuyruk 42.629 (P1=7.054), ayrı review 3.049, Lua 162. Bu adaylar onaylı cümle veya oyun görünürlüğü sayısı değildir.

## Çeviri ve teslim

1. Paket inputs/basis, kaynak pini ve family=dialog doğrulanır. Yalnız tr, context_reviewed, runtime_evidence, runtime_review ve gerçek measurements değişebilir. DRAFT başlığı kalır; Sol dil onayı ayrı raporda tutulur.
2. Her pointerın konuşmacı ve muhatap türünü, EN değerini ve çağıran NPC/script dosyalarını oku. Converse.config temel vanilla dosyası FU checkout’unda yoktur; patch değeri veya genel NPC referansı canlı oyun kanıtı sayılmaz. ElDuukhar köylüsü kendi elduuconverse.config dosyasını kullanır; base converse.config yalnız breakObject için bağlıdır. Erişimi belirsiz dalı olumlu kanıt gibi yazma.
3. LOCKED ve TM, bağlama göre doğrulanır; öneri otomatik onay değildir. Yeni kavramlar Avolite Kristali, Glif, Su Ejderhası, Balık Surat, Pofuduk Popo; Pharitu, Myphis, Ma'ez ve Ruin adları korunur. Ruin yalnız The Ruin özel varlık ifadesiyle kilitlidir; genel harabe anlamını buna zorlama. Glif için beş eski sembol istisnası tam EN/TR alanına bağlıdır, yeni repliklerde kullanılacak genel izin değildir.
4. Floran’ın s tıslamasını uygun Türkçe s sesleriyle aktar; rastgele ünlü uzatma ekleme. Fenerox ve Pharitu’nun kısa/kırık ifadelerini koru. Özne ve zamirleri, kutsallık karşılaştırmalarını, olumsuzluk ve soru anlamını doğrula. Kaynakta olmayan lore ekleme; teknik ID/portre/callback çevirme. Mantizi’de hitapları özel kişi sanma: Aunt Nell=koku, ball of chalk=yürüyüş, Pope of Rome=ev, bu para/vergi bağlamında saucepan lid=para. Kaynak argo sözlükleri ve çıkarımlar inceleme kaydında; başka anlamdaki kullanımlara kör TM uygulama. Sefton REVIEW, kesin anlamı doğrulanana kadar kaynak hitabı korunur; özel ad olduğu iddia edilmez. Pyreite, Pirit değildir; mevcut Pyreite Körisi adı kullanılır. Barbatus, CySol, Zaibatsu ve Pyreite yeni LOCKED kayıtlarıdır. Almost/may/capable kiplerini ve your/my zamirlerini kaybetme.
5. Her gruba gerçek kaynak dosyası ve açıklama ile kanıt yaz. Canlı görsel LQA yapılmadıysa NOT TESTED kalır. Gerçek çeviri süresini kaydet; tahmin üretme. Katalog/manifest/generated çıktıları değiştirmeden Sol’a teslim et.

Ön denetim, local-luna kökünde:

```powershell
$env:PYTHONUTF8 = '1'
& '../local-runtime/venv/Scripts/python.exe' tools/plan_translation.py --source ../local-runtime/fu_source --check-packet ../local-runtime/translation-planning-v069-dialog-next/packet.json
```

Build/yayın sonuçları checkpoint’te yer alır. Generated çıktıları mevcut CI yayımlar; elle düzenleme. Beyin işlemleri ana proje kökündeki beyin-project.ps1 yardımcısıyla yapılır.
