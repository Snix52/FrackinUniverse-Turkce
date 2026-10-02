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
