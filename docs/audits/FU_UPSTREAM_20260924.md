# FU upstream kaynak kontrolü — 24 Eylül 2026

## Kaynak karşılaştırması

- Önceki pin ve son etiketli 6.5.8 sürümü: `329e714b3fe87571055c8ad7aa38135d199d3317`.
- İncelenen güncel `master` ve yeni pin: `bb58383c0d16c1152e3439e606b39ff82288b586` (21 Eylül 2026).
- `.metadata` içindeki sürüm her iki committe de **6.5.8**. Arada 3 commit ve 12 değişen dosya var.
- Sekiz `bees/frames/*.item` dosyasında görünmeyen `functionParams` değerleri temizlendi. Dört `items/materials/*.matitem` dosyasında yalnız İngilizce `/shortdescription` büyük harfleri düzeltildi.
- Değişen dört görünür alanın hiçbiri mevcut Türkçe kataloğunda yer almıyordu. **Yeni çeviri alanı: 0; değişen mevcut çeviri: 0.** Bu dört alan zaten aşağıdaki kalan kapsamın içindedir.

| Alan | Önceki pin | Yeni pin | Katalogda çevrili? |
|---|---|---|---|
| `fukirhosstairs.matitem` `/shortdescription` | Alloy stairs | Alloy Stairs | Hayır |
| `fukirhosstairs2.matitem` `/shortdescription` | Alloy red stairs | Alloy Red Stairs | Hayır |
| `penumbradirtmaterial.matitem` `/shortdescription` | Umbral dirt | Umbral Dirt | Hayır |
| `penumbrastonematerial.matitem` `/shortdescription` | Umbral stone | Umbral Stone | Hayır |

## Kalan çeviri kapsamı

Mevcut v0.61 kataloğuyla eski ve yeni kaynak üzerinde aynı `audit_remaining.py` çalıştırıldı. Sonuçlar birebir aynı:

| Havuz | Asset | Görünür alan |
|---|---:|---:|
| Doğrulanmış çevrilmemiş | 10.499 | 45.517 |
| Bağlam incelemesi gereken ek havuz | 620 | 4.331 |
| Doğrudan gösterilen Lua inceleme havuzu | 33 | 165 literal |

Bu sayılar kaynak taramasıdır; oyun içi LQA sonucu değildir. Katalogda 12.898 yapılandırılmış alan bulunur. Kaynak pininin güncellenmesi çeviri içeriğini değiştirmez. Yeni kaynak commitinin ve paket doğrulamasının nihai sonucu `dist/build-evidence.json` dosyasında tutulur.

Kaynaklar: `tools/kaynaklar.json`, `tools/ceviriler.json`, `tools/audit_remaining.py`, FU upstream Git geçmişi ve `.metadata`, eski/yeni kaynak audit JSON raporları.
