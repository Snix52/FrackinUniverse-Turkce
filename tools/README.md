# Araç ve kaynak dizini

Bu klasör çeviri kaynaklarını, kaynak doğrulamalarını, paket üreticisini ve testleri içerir. Komutlar repository kökünden çalıştırılır; kurulum ve tam doğrulama sırası [katkı rehberindedir](../CONTRIBUTING.md).

## Aktif komutlar

| Araç | Görev |
| --- | --- |
| `qa_integrity.py` | Manifest/katalog, terminoloji ve metin bütünlüğü; `--write-docs` terim belgesini üretir |
| `check_sources.py --source fu_source` | Bütün sürüm, UI ve gemi S.A.I.L. kaynak kapılarını tek komutla çalıştırır |
| `generate_v045.py` … `generate_v070.py` | Adları tarihsel olsa da güncel, salt okunur sürüm kaynak kontrolleridir |
| `check_ui_lqa_20260925.py`, `check_ship_sail_dialog_20260926.py` | Ek UI/SAIL kaynak ve asset üretilebilirlik kontrolleri |
| `build_validate.py --source-dir fu_source --output build_output` | Tam kaynak doğrulaması, mod ağacı ve build raporu |
| `write_build_evidence.py` | Doğrulanmış build'den deterministik ZIP ve yayın kanıtı |
| `check_generated_changes.py` | Üretilen dosyalara doğrudan değişiklikleri reddeder |
| `publish_generated.py` | CI'da başlangıç kaynak commit'i ve remote yarış korumasıyla yayın yapar |
| `audit_remaining.py --source fu_source` | Kalan oyuncu metni adaylarını ve inceleme havuzunu raporlar |
| `plan_translation.py` | Güncel girdilerle çeviri taslağı hazırlar/doğrular; [planlama rehberi](../docs/TRANSLATION_PLANNING.md) |
| `prepare_ebrar_rose_art.ps1` | [Özgün görsel kaynağından](art_sources/ebrar-rose/README.md) ilgili assetleri hazırlar |

`qa_raw.py`, `rule_data.py`, `custom_assets.py` ve `ui_lqa_assets.py` diğer araçların kullandığı yardımcı modüllerdir. `tests/` regresyon ve Lua davranış kontrollerini içerir.

## Veri ve asset kaynakları

| Konum | İçerik |
| --- | --- |
| `ceviriler.json`, `v*_translations.json` | Ana katalog ve denetlenen sürüm manifestleri |
| `kaynaklar.json` | Sabit FU repository/commit ve kaynak envanteri |
| `locked_terms.json`, `translation_memory_exceptions.json` | Terminoloji ve bağlama bağlı karşılıklar |
| `translation_priorities.json` | Oynanış önceliği kuralları |
| `rules/` | Asset kapsamı, teknik korumalar ve belgeli istisnalar |
| `raw_text_translations.json`, `raw_runtime_overrides.json`, `raw_overrides/` | Pinli Lua/runtime metin kaynakları ve baytları korunan şablonlar |
| `custom_assets.json`, `custom_assets/`, `ui_lqa_20260925.json`, `art_sources/` | Ek oyun assetleri, tarifleri ve özgün görseller |
| `test_raporu.json`, `GELISTIRME.txt` | CI tarafından üretilen raporlar; elle düzenlenmez |
| `TERIMLER.txt` | Üretilen [terminoloji belgesine](../docs/TERMINOLOGY.md) yönlendirme |

Manifestlerin ve raw/custom kaynakların mevcut yolları build ve test sözleşmesinin parçasıdır. Yeni yerel taslaklar ve test çıktıları bu kaynakların arasına konmaz.

## Eski üreticiler

`add_v022`–`add_v0312` ve `generate_v032`–`generate_v044` araçları [legacy/](legacy/README.md) altında arşivlenmiştir. Eski katalogları yazan bu tek seferlik araçlar aktif kaynak kapılarıyla karıştırılmamalıdır. Doğrudan çalıştırma engellenir; yeni içerik için güncel planlama ve onay akışı kullanılır.
