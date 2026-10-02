# Depo düzenleme denetimi — 2 Ekim 2026

İncelenen başlangıç: `main` commit `df58b4cd08e13c7f35442e8363975446d2e6145b`, katalog v0.70.0-beta. Kapsam yalnız repository düzenidir.

## Bulgular ve düzenlemeler

| Bulgu | Düzenleme |
| --- | --- |
| Kök README güncel sürümün yanında uzun, kısmi eski sürüm notları taşıyordu | Geçmiş kapsam kayıtları `docs/history/RELEASE_NOTES.md` içine alındı; ana sayfada güncel durum ve arşiv bağlantısı kaldı |
| 690 satırı aşan checkpoint'in başı eski sürümleri, sonu güncel sürümü anlatıyordu; geçmiş “bekliyor” kayıtları güncel bilgiyle karışıyordu | Tam günlük `docs/history/FU_SESSION_CHECKPOINT_20261001.md` içinde korundu; kök checkpoint güncel durum ve kanonik kanıt bağlantılarına indirildi |
| Güncel rehberler, tarihli denetim/LQA/devir kayıtları aynı belge klasöründeydi | 15 tarihsel belge `audits/`, `lqa/`, `handoffs/`, `history/` altında toplandı; bağlantılar yeni konumlara taşındı ve belge dizini eklendi |
| 25 eski, katalog yazan tek seferlik üretici aktif kaynak kontrolleriyle yan yanaydı | `tools/legacy/` içine taşındı; doğrudan çalıştırma dosya yazmadan durur; v039 yardımcı işlev regresyonu yeni konuma uyarlandı |
| Main ve PR workflow'ları aynı 28 kaynak kontrolünü ayrı ayrı listeliyordu | `tools/check_sources.py` ortak komutu eklendi; katalog sürümüne kadar eksik kapı/manifest reddedilir, ilk hata zinciri durdurur; yinelenen Pillow kurulumu kaldırıldı |
| QA rehberinin Bash paket adı komutu eksik kapanıyordu; Windows örneğinde görsel test bağımlılığı eksikti | Komut kapatıldı, Windows Pillow bağımlılığı ve ortak kaynak kontrolü eklendi |
| Yerel kaynak/build/audit klasörleri yanlışlıkla izlenebilir durumdaydı | Yalnız bu geçici klasörler için ignore kuralları eklendi; paketler ve mod kaynakları izlenmeye devam eder |

## Korunan sözleşmeler

Ana katalog, bütün sürüm manifestleri, terminoloji kararları, review JSON kayıtları, raw/custom asset kaynakları, FU pini ve oyuncuya sunulan çeviriler değiştirilmedi. Katalog/manifest yolları aktif araçların ortak sözleşmesi olduğu için aynı yerde kaldı. `FU_Turkce/`, `dist/` ve generated raporlar elle düzenlenmedi; CI bakım değişikliklerinden sonra aynı sürümü yeniden doğrular ve yayın kanıtını yeniler.

Kök README, katkı rehberi, belge ve araç dizinleri güncel giriş noktalarıdır. Tarihsel dosyalar kayıt tarihleriyle okunur. Oyunun kurulumu ve yeni çeviri kapsamı bu çalışmaya dahil değildir.

## Doğrulama

Taşınan belgelerin yerel bağlantıları ve Git whitespace kontrolü denetlenir. Regresyonlar; eski üreticilerin yazmadan durmasını, eksik/yeni sürüm kapılarının reddedilmesini ve bir kaynak kapısı hata verdiğinde sonraki kontrollerin çalışmamasını kapsar. Tam regresyon, pinli kaynağa karşı tüm 28 kapı, full-source build ve üretilen mod ağacının mevcut paketle bayt eşitliği kontrolü uygulanır. Son hosted çalışmanın sonucu GitHub Actions'tan, paket kanıtı [dist/build-evidence.json](../../dist/build-evidence.json) üzerinden okunur. Oyun içi LQA durumu bu bakım çalışmasıyla değişmez.

## Doğrulanan sonuçlar

- Yerel Python compile ve **277 regresyon**: PASS.
- Belge bağlantıları: **100 kontrol, 0 kırık bağlantı**.
- Katalog, manifest, terminoloji ve inceleme kayıtları: korunmuş **58 kaynak/paket dosyası**; 25 arşiv üreticisinin özgün işlevleri korundu, doğrudan yazma engeli doğrulandı.
- Yerel pinli FU ile full-source build: PASS; yeni mod ağacının mevcut yayınla **4.948 dosyada bayt eşitliği** PASS.
- [GitHub Build and QA](https://github.com/Snix52/FrackinUniverse-Turkce/actions/runs/36992639478): **SUCCESS**; 277 regresyon, **28 kaynak kapısı**, tam build, yeni Lua/UI testleri, deterministik ZIP ve generated yayın adımı geçti.
- Bakım kaynak commit'i: `4c0ed0a127cb5f1f72cfb34579a8fcafba1918cf`. CI generated commit'i: `4cb773f9a27a682a63f0905df15f30fedae88c83`.
- Yayımlanan v0.70 ZIP SHA-256 değeri önceki yayınla aynı: `ffbf0a0532fed6ff4dad4a1252d1478036bf6f80ee01639938ea55ff68874dfa`. Oyuncu içerikleri değişmedi; build kanıtı yeni bakım girdileri için CI tarafından yenilendi.

Tam kaynak kapısı dizisi hosted CI'da doğrulandı. Yerelde v045–v051 geçtikten sonra aynı taramanın ikinci kopyası durduruldu; yerel full-source build, bayt karşılaştırması ve bütün regresyonlar tamamlandı. Oyun içi LQA ve bilgisayardaki kurulum bu işlemin kapsamına alınmadı.
