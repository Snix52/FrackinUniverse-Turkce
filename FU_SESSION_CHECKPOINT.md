# FU Session Checkpoint

## Durum
22 Eylül 2026 - v0.41 Arayüz çalışması. Son sağlam sürüm v0.40.0-beta.

## v0.41 hedefi
Tek sistem: Space Station.

Pinned FU kaynağı:
- repository: `sayterdarkwynd/FrackinUniverse`
- commit: `329e714b3fe87571055c8ad7aa38135d199d3317`
- declared version: 6.5.8

## Doğrulanmış kapsam
Toplam hedef: **261 görünür metin birimi**

### Structured: 250
- `interface/scripted/spaceStation/spaceStation.config`: 14 audit-confirmed alan / 12 benzersiz kaynak metin.
- `interface/scripted/spaceStation/texts.config`: 188 canlı alan.
  - Runtime `spaceStation.lua` tarafından doğrudan okunuyor.
  - `defaultButtonStates`: Chat / Shop / Trade Goods / Special / Goodbye canlı.
  - Irk bazlı welcome, chat, station-type special, cantAfford, enhancer ve mercenary metinleri canlı.
  - `generic/chat4` ve `generic/chat5` uzun dış eser alıntıları içerdiği için v0.41 kapsamından çıkarıldı; manuel inceleme bekliyor.
- `interface/scripted/spaceStation/spaceStationData.config`: 48 canlı alan.
  - 18 medical special: ad + açıklama = 36.
  - 6 military special: ad + açıklama = 12.

### Lua runtime: 11 benzersiz metin
Asset: `interface/scripted/spaceStation/spaceStation.lua`
- ERROR - No station object found
- Your pixels:
- Station stock:
- Your stock:
- Wrong type / Special hata metni
- No item selected... hata/fallback metni
- tradeA no-selection hata metni
- tradeB no-selection hata metni
- Lvl
- Required:
- Fully upgraded!

Lua metinleri `tools/raw_text_translations.json` source-locked replacement sistemiyle ele alınacak; script mantığı değiştirilmeyecek.

## Runtime doğrulaması
- `spaceStation.lua`, `spaceStation.config`, `spaceStationData.config` ve `texts.config` dosyalarını doğrudan yüklüyor.
- Eski Quest dalı Lua içinde mevcut, fakat `texts.config/defaultButtonStates` ana menüsünde Quest düğmesi yok.
- Quest metinleri ve `spaceStationData.config/quests` v0.41'e alınmayacak.
- `scientificSpecial` bazı ırklarda literal `deprecated` değerini taşıyor ve station-type welcome akışında okunabildiği için görünür kaynak olarak ayrıca değerlendirilecek.

## Teknik plan
1. `tools/v041_translations.json`: 250 structured satır.
2. `tools/ceviriler.json`: aynı 250 satır append, translation_version = 0.41.0-beta.
3. `tools/raw_text_translations.json`: Space Station Lua için 11 source-locked replacement.
4. `tools/build_validate.py`: v0.41 field allowlist + duplicate guard.
5. `tools/generate_v041.py`: pinned source üzerinden kapsam/field guard.
6. `tools/tests/test_v041.py`: structured kapsam, runtime exclusion ve Lua replacement testleri.
7. Dar QA sonrası tek feature commit.

## Sonraki başlangıç noktası
Çeviri tablosunu üret; placeholder/format kodlarını koru:
- `{STATIONNAME}`
- `[(playername)]`
- `[(pause)N]`
- `^color;...^reset;`

Pet House v0.41'e alınmayacak; Space Station tek başına hedef paket boyutunu doldurdu.
