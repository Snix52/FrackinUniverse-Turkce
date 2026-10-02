# Katkı ve bakım rehberi

Komutları repository kökünden çalıştır. Güncel sürüm ve çalışma durumu [checkpoint](FU_SESSION_CHECKPOINT.md), belge haritası [docs/README.md](docs/README.md), araçların görevleri [tools/README.md](tools/README.md) içinde bulunur.

## Hangi dosya düzenlenir?

| Amaç | Düzenlenen kaynak |
| --- | --- |
| Yapılandırılmış çeviri | `tools/ceviriler.json` ve ilgili `tools/v*_translations.json` |
| Lua metni veya kaynak kilitli runtime düzenlemesi | `tools/raw_text_translations.json`, `tools/raw_runtime_overrides.json`, `tools/raw_overrides/` |
| Terminoloji ve bağlama bağlı istisna | `tools/locked_terms.json`, `tools/translation_memory_exceptions.json`, `tools/rules/` |
| Ek oyun asseti ve üretim tarifi | `tools/custom_assets.json`, `tools/custom_assets/`, `tools/ui_lqa_20260925.json` |
| FU kaynak sürümü | `tools/kaynaklar.json`; bütün kaynak doğrulamalarıyla birlikte |
| Rehber, inceleme veya tarihsel kayıt | `docs/`; tarihli raporu ilgili alt klasöre koy |

`FU_Turkce/`, `dist/`, `tools/test_raporu.json`, `tools/GELISTIRME.txt` ve `docs/TERMINOLOGY.md` üretilen çıktılardır. Elle paket veya kurulum ağacı düzenleme; kaynak değişikliğinden sonra CI doğrulayıp üretir. Terminoloji belgesi `python tools/qa_integrity.py --write-docs` ile yenilenir.

## Yerel doğrulama

Python 3.11+ kullan. Windows'ta davranış ve görsel asset testleri için `python -m pip install lupa==2.8 Pillow==11.3.0`; Linux'ta Pillow ve sistem `liblua5.4-0` kitaplığı gerekir.

```text
python -m compileall -q tools
python -m unittest discover -s tools/tests -v
python -X utf8 tools/qa_integrity.py
python -X utf8 tools/check_sources.py --source fu_source
python -X utf8 tools/build_validate.py --source-dir fu_source --output build_output
git diff --check
```

`fu_source`, `tools/kaynaklar.json` içindeki committe temiz bir FU Git checkout'u olmalıdır. `build_output` henüz mevcut olmayan bir çıktı klasörü olmalıdır. Kaynak checkout'larını, taslakları ve deneme build'lerini commit etme. Paket kanıtı için kaynak değişikliklerini önce commit et, ardından yeniden build çalıştır; ayrıntılar [QA pipeline](docs/QA_PIPELINE.md) içinde.

Yeni sürüm manifesti, aynı numaralı salt okunur kaynak kapısı ve uygun regresyon kontrolleri birlikte eklenir. `check_sources.py` v0.45'ten katalog sürümüne kadar tüm kapıları ve UI/S.A.I.L. ek kontrollerini çalıştırır; eksik bir manifest veya kapı hata verir. İki workflow'a ayrı ayrı sürüm komutu eklenmez.

## Belgelerin yeri

- `docs/` kökü: güncel dil, QA, planlama ve kurulum rehberleri.
- `docs/audits/`: tarihli denetim ve bakım raporları.
- `docs/lqa/`: belirli sürüm veya ekran için kontrol kayıtları; test edilmemiş durumlar açıkça korunur.
- `docs/reviews/`: kaynak kapılarının okuduğu onay ve dil incelemesi JSON kayıtları.
- `docs/handoffs/`: tarihli çalışma devirleri; yerel taslak yolu yeni checkout'ta mevcut olmayabilir.
- `docs/history/`: eski sürüm notları ve uzun çalışma günlüğü.

Güncel durumu kök checkpoint'te kısa tut; önceki çalışma kanıtlarını arşiv bağlantılarıyla koru. Oyun içi görünüm, font ve taşma kontrolleri yapılmadan statik QA'yı oyun içi LQA olarak yazma.
