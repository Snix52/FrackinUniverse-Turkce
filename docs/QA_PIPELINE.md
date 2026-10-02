# Test ve paketleme

## Girdiler

Ana katalog `tools/ceviriler.json`, sürüm listeleri `tools/v*_translations.json`, FU kaynak commit'i `tools/kaynaklar.json` içindedir. Lua metinleri, istisnalar ve görsellerin kaynak dosyaları [araç dizininde](../tools/README.md) listelenir.

`docs/TERMINOLOGY.md`, `tools/locked_terms.json` dosyasından üretilir. Sözlük değiştiğinde `python tools/qa_integrity.py --write-docs` çalıştır.

## Kaynak kontrolü

FU kopyası, kayıtlı committe temiz bir Git kökü olmalı. Değiştirilmiş, izlenmeyen veya ignore edilmiş ek dosyalar tarama sonuçlarını etkileyebileceği için reddedilir.

`tools/check_sources.py`, v0.45'ten katalog sürümüne kadar bütün sürüm kontrollerini, arayüz, gemi S.A.I.L. ve Bilim Karakolu radyo kontrollerini çalıştırır. Karakol kontrolü haritadaki bütün `radioMessage` ve `radioMessages` kimliklerini çeviri kapsamıyla karşılaştırır. Eksik dosyada, çevrilmemiş tetikleyicide veya ilk hatada durur.

`build_validate.py`, kaynak alanlarını ve üretilen yamaları karşılaştırır. LF/CRLF seçenekleri aynı kaynak metin için desteklenir. FU'nun yamaladığı alanlar ilgili yama değerinden kontrol edilir. FU kopyasında bulunmayan temel oyun alanları ayrı kaynak kayıtlarıyla izlenir.

## Yerel testler

Python 3.11+ kullan. Linux'ta `Pillow==11.3.0` ve `liblua5.4-0`; Windows'ta `Pillow==11.3.0` ve `lupa==2.8` gerekir. Lua kitaplığı bulunamazsa davranış testleri hata verir.

Linux:

```bash
python -m compileall -q tools
python -m unittest discover -s tools/tests -v
python tools/qa_integrity.py
python tools/check_sources.py --source fu_source
python tools/build_validate.py --source-dir fu_source --output build_output
FU_TEST_MOD_DIR=build_output/FU_Turkce python -m unittest discover -s tools/tests -p 'test_lua_behavior.py' -v
FU_TEST_MOD_DIR=build_output/FU_Turkce python -m unittest discover -s tools/tests -p 'test_ui_lqa_20260925.py' -v
git diff --check
```

Windows PowerShell:

```powershell
python -m pip install lupa==2.8 Pillow==11.3.0
python -m unittest discover -s tools/tests -v
python -X utf8 tools/qa_integrity.py
python -X utf8 tools/check_sources.py --source ..\fu_source
python -X utf8 tools/build_validate.py --source-dir ..\fu_source --output ..\build_output
$env:FU_TEST_MOD_DIR = '..\build_output\FU_Turkce'
python -m unittest discover -s tools/tests -p test_lua_behavior.py -v
```

Build için yeni bir çıktı klasörü seç. `validation.json` mod klasörünün dışında oluşur; kaynak commit'ini, girdi hashlerini ve kontrol sonuçlarını tutar. Kaynak verilmeden yapılan deneme build'i dağıtım için yeterli değildir.

## ZIP ve paket raporu

Paketleme öncesinde kaynak değişikliklerini commit et ve build'i yeniden çalıştır. Paketleyici, build raporunu kullanılan katalog, kurallar, araçlar, şablonlar ve mod ağacıyla karşılaştırır. Build'den sonra bir girdi değiştiyse yeniden build gerekir.

Linux'ta doğrulanmış build'i paketlemek için:

```bash
rm -rf FU_Turkce && cp -a build_output/FU_Turkce FU_Turkce
PACKAGE_PATH="$(python -c 'import json; v=json.load(open("tools/ceviriler.json", encoding="utf-8"))["translation_version"]; print("dist/FU_Turkce_v" + v.split("-", 1)[0] + ("_Beta" if "beta" in v.lower() else "") + ".zip")')"
python tools/write_build_evidence.py --zip "$PACKAGE_PATH" \
  --output dist/build-evidence.json --create-zip --refresh-tracked \
  --translation-source-commit "$(git rev-parse HEAD)" --workflow-run-id local
unzip -t "$PACKAGE_PATH"
```

ZIP dosya listesi ve baytları kök `FU_Turkce/` ağacıyla eşleşir. Paket sırası, tarihler ve izinler sabittir. Sonuçlar `dist/build-evidence.json`, `tools/test_raporu.json` ve `tools/GELISTIRME.txt` dosyalarına yazılır.

## GitHub akışı

- PR kontrolleri Windows ve Linux testlerini, kaynak doğrulamasını ve deneme paketini çalıştırır; paket yayımlamaz.
- Main akışı doğrulanmış mod ağacı ve ZIP'i üretir. Doğrudan çıktı dosyası düzenlemelerini başlangıçta reddeder.
- Yayın sırasında main ilerlediyse eski build yayımlanmaz. Yeniden tabanlama veya zorla push kullanılmaz. Üretilen çıktı commit'i `[skip ci]` taşır.
- Kalan kapsam taraması raporları workflow artifact'ına yükler; main'e ikinci bir paket yazmaz.

Otomatik raporlar dosya ve betik kontrollerini içerir. Kullanıcıların oynanış denemeleri [oyun testi belgesinde](LQA_CHECKLIST.md) tutulur.
