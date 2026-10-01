# Luna: diyalog öncelikli güncel devir — v0.68

## Tamamlanan dilim

İkinci diyalog paketi Sol incelemesiyle v0.68.0-beta kataloğuna alındı: **380 alan / 350 bağlam grubu**. Önceki 14.993 alan aynen korunarak toplam **15.373** oldu. **9 yeni LOCKED**, toplam **615**. 37 grupta 38 alan, tekrarlar ve kısa konuşma ifadeleri dahil **48 düzeltme**; tüm önce/sonra ve gerekçeler [inceleme kaydında](reviews/dialogue2-20261001.json). [LQA kaydı](LQA_V068_20261001.md) kaynak erişimi sınırlarını içerir.

Çalışma checkout’u `../local-luna/`; Sol `../local-repo/`. Başlamadan Git durumunu ve checkpoint’i oku. FU 6.5.8 kaynağı `../local-runtime/fu_source/`, pin `bb58383c0d16c1152e3439e606b39ff82288b586` korunur.

## Sıradaki paket

**`../local-runtime/translation-planning-v068-dialog-next/packet.json`**: 399 alan / 350 grup, 65 grupta birebir TM önerisi. Kaynak `dialog/converse.config.patch`; konuşmacı ve muhatap türü ayrı tutulur. Eski v067-dialog-next tamamlandı; onun üzerinde devam etme. Eski v067-radio-next yeni katalog ve LOCKED hashleriyle bayattır. Radyo ailesine geçerken güncel katalogla yeni çıktı klasöründe yeniden hazırla; hashleri elle değiştirme.

Diyalog ailesinde 1.530 alan / 1.449 grup kaldı. Confirmed kuyruk 43.028 (P1=7.453), ayrı review 3.049, Lua 162. Bu adaylar onaylı cümle veya oyun görünürlüğü sayısı değildir.

## Çeviri ve teslim

1. Paket inputs/basis, kaynak pini ve family=dialog doğrulanır. Yalnız tr, context_reviewed, runtime_evidence, runtime_review ve gerçek measurements değişebilir. DRAFT başlığı kalır; Sol dil onayı ayrı raporda tutulur.
2. Her pointerın konuşmacı ve muhatap türünü, EN değerini ve çağıran NPC/script dosyalarını oku. Converse.config temel vanilla dosyası FU checkout’unda yoktur; patch değeri veya genel NPC referansı canlı oyun kanıtı sayılmaz. ElDuukhar köylüsü kendi elduuconverse.config dosyasını kullanır; base converse.config yalnız breakObject için bağlıdır. Erişimi belirsiz dalı olumlu kanıt gibi yazma.
3. LOCKED ve TM, bağlama göre doğrulanır; öneri otomatik onay değildir. Yeni kavramlar Avolite Kristali, Glif, Su Ejderhası, Balık Surat, Pofuduk Popo; Pharitu, Myphis, Ma'ez ve Ruin adları korunur. Ruin yalnız The Ruin özel varlık ifadesiyle kilitlidir; genel harabe anlamını buna zorlama. Glif için beş eski sembol istisnası tam EN/TR alanına bağlıdır, yeni repliklerde kullanılacak genel izin değildir.
4. Floran’ın s tıslamasını uygun Türkçe s sesleriyle aktar; rastgele ünlü uzatma ekleme. Fenerox ve Pharitu’nun kısa/kırık ifadelerini koru. Özne ve zamirleri, kutsallık karşılaştırmalarını, olumsuzluk ve soru anlamını doğrula. Kaynakta olmayan lore ekleme; teknik ID/portre/callback çevirme.
5. Her gruba gerçek kaynak dosyası ve açıklama ile kanıt yaz. Canlı görsel LQA yapılmadıysa NOT TESTED kalır. Gerçek çeviri süresini kaydet; tahmin üretme. Katalog/manifest/generated çıktıları değiştirmeden Sol’a teslim et.

Ön denetim, local-luna kökünde:

```powershell
$env:PYTHONUTF8 = '1'
& '../local-runtime/venv/Scripts/python.exe' tools/plan_translation.py --source ../local-runtime/fu_source --check-packet ../local-runtime/translation-planning-v068-dialog-next/packet.json
```

Build/yayın sonuçları checkpoint’te yer alır. Generated çıktıları mevcut CI yayımlar; elle düzenleme. Beyin işlemleri ana proje kökündeki beyin-project.ps1 yardımcısıyla yapılır.
