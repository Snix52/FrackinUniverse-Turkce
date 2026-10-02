# Katkı rehberi

Çeviri kuralları [dil rehberinde](docs/STYLE_GUIDE.md), mevcut karşılıklar [terim sözlüğünde](docs/TERMINOLOGY.md). Bir metni değiştirirken kullanıldığı görev, ekran veya karakteri de kontrol et.

## Kaynak dosyaları

| Dosya | İçerik |
| --- | --- |
| `tools/ceviriler.json` | Ana çeviri kataloğu |
| `tools/v*_translations.json` | Sürüm bazında çeviri listeleri |
| `tools/locked_terms.json` | Sabit terim karşılıkları |
| `tools/translation_memory_exceptions.json` | Bağlama göre farklı çevrilen metinler |
| `tools/raw_text_translations.json`, `tools/raw_runtime_overrides.json`, `tools/raw_overrides/` | Lua metinleri ve kaynak şablonları |
| `tools/custom_assets.json`, `tools/custom_assets/`, `tools/ui_lqa_20260925.json` | Ek görseller ve arayüz düzenlemeleri |
| `tools/kaynaklar.json` | Kullanılan FU commit'i ve kaynak dosya listesi |

Yeni çeviri hazırlamak için [planlama rehberini](docs/TRANSLATION_PLANNING.md) kullan. Aynı metnin bütün kullanımlarını incele; görevdeki eşya adıyla envanter adını eşleştir.

## Kontrol

Python 3.11+ gerekir. Windows testleri için `lupa==2.8` ve `Pillow==11.3.0` kurulmalıdır. Linux'ta Pillow ve `liblua5.4-0` kullanılır.

Komutları repo kökünde çalıştır:

```text
python -m compileall -q tools
python -m unittest discover -s tools/tests -v
python -X utf8 tools/qa_integrity.py
python -X utf8 tools/check_sources.py --source fu_source
python -X utf8 tools/build_validate.py --source-dir fu_source --output build_output
git diff --check
```

`fu_source`, `tools/kaynaklar.json` içindeki committe temiz bir FU Git kopyası olmalı. `build_output` için henüz oluşturulmamış bir klasör seç. [Test ve paketleme ayrıntıları](docs/QA_PIPELINE.md)

## Paket ve belgeler

CI, kaynak değişikliklerinden `FU_Turkce/`, `dist/`, `tools/test_raporu.json` ve `tools/GELISTIRME.txt` dosyalarını üretir. Bu çıktıları elle düzenleme. Terim belgesi `python tools/qa_integrity.py --write-docs` ile yenilenir.

Yeni sürümün çeviri listesi ve kaynak kontrolü birlikte eklenir. `tools/check_sources.py` bütün sürüm kontrollerini çalıştırır.

Sürüm değişikliklerini [CHANGELOG.md](CHANGELOG.md) içinde kısa tut. Belgeler genel kullanım adımlarını anlatmalı; kişisel klasörler ve oturum günlükleri repoya eklenmez. Bir hata bildirirken sürüm, dosya/alan, beklenen sonuç ve görülen sonucu yaz.
