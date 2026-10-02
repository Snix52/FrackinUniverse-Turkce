# Araçlar

Komutlar repo kökünden çalıştırılır. Kurulum ve test sırası [katkı rehberinde](../CONTRIBUTING.md).

| Araç | Görev |
| --- | --- |
| `qa_integrity.py` | Katalog, terim ve metin kontrolü; `--write-docs` sözlüğü yeniler. |
| `check_sources.py --source fu_source` | Sürüm, arayüz, gemi konuşması ve Bilim Karakolu radyo kaynak kontrollerini çalıştırır. |
| `generate_v045.py` … katalog sürümü | Sürüm bazında salt okunur kaynak kontrolü. |
| `check_ui_lqa_20260925.py` | Arayüz metinleri ve görsellerini kontrol eder. |
| `check_ship_sail_dialog_20260926.py` | Gemi S.A.I.L. konuşmalarını kontrol eder. |
| `check_science_outpost_radio_20261003.py` | Karakol haritasındaki radyo tetikleyicilerinin çeviri kapsamını kontrol eder. |
| `build_validate.py` | Mod ağacını üretir ve FU kaynağıyla doğrular. |
| `write_build_evidence.py` | ZIP'i oluşturur ve paket bilgilerini yazar. |
| `check_generated_changes.py` | Üretilen dosyalara doğrudan değişiklikleri kontrol eder. |
| `publish_generated.py` | CI'da güncel kaynak için paketi yayımlar. |
| `audit_remaining.py` | Kalan çeviri adaylarını tarar. |
| `plan_translation.py` | Çeviri taslağı hazırlar ve kontrol eder. |
| `prepare_ebrar_rose_art.ps1` | Gül görselini nesne ve envanter boyutlarına aktarır. |

## Dosyalar

- Katalog ve sürüm listeleri: `ceviriler.json`, `v*_translations.json`.
- FU kaynağı: `kaynaklar.json`.
- Terimler ve istisnalar: `locked_terms.json`, `translation_memory_exceptions.json`, `rules/`.
- Öncelikler: `translation_priorities.json`.
- Lua metinleri ve şablonlar: `raw_text_translations.json`, `raw_runtime_overrides.json`, `raw_overrides/`.
- Görseller ve ek oyun dosyaları: `custom_assets.json`, `custom_assets/`, `ui_lqa_20260925.json`, `art_sources/`.
- Testler: `tests/`. Diğer Python modülleri bu araçların yardımcılarını içerir.

`test_raporu.json` ve `GELISTIRME.txt` CI çıktılarıdır. [Terim belgesi](../docs/TERMINOLOGY.md) `locked_terms.json` dosyasından üretilir.

Eski katalog üreticileri [legacy/](legacy/README.md) altında tutulur. Yeni çeviri için [planlama rehberini](../docs/TRANSLATION_PLANNING.md) kullan.
