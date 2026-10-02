# Güncel çalışma durumu

Son içerik sürümü **v0.70.0-beta**, hedef **FU 6.5.8**. Ana katalogda **16.147** alan, LOCKED sözlükte **637** kayıt bulunur. 4.923 patch, 10 raw ve 14 ek asset ile toplam 4.947 oyun asseti vardır. Son yayımlanan paketin commit, SHA-256 ve QA bilgileri için tek kaynak [dist/build-evidence.json](dist/build-evidence.json) dosyasıdır.

## 2 Ekim 2026 — repository düzeni

Kapsam yalnız repository temizliğidir. Belgeler tarihli denetim, LQA, devir ve geçmiş kayıt klasörlerine ayrıldı; eski tek seferlik üreticiler `tools/legacy/` içine taşındı. Main ve PR kaynak kontrolleri `tools/check_sources.py` ortak komutunda toplandı. Çeviri içeriği ve FU pini korunur.

- [Düzenleme denetimi ve doğrulama kapsamı](docs/audits/REPO_ORGANIZATION_20261002.md)
- [Katkı ve bakım rehberi](CONTRIBUTING.md)
- [Belge dizini](docs/README.md)
- [Aktif araçlar ve kaynak dosyaları](tools/README.md)

## Son içerik ve inceleme kaydı

v0.70'te dördüncü NPC diyalog diliminin 375 alanı, 350 konuşmacı/muhatap bağlamıyla incelendi. Önceki 15.772 alan korundu. Tam önce/sonra ve gerekçeler [inceleme JSON'unda](docs/reviews/dialogue4-20261001.json), kaynak ve erişim sınırları [v0.70 LQA kaydında](docs/lqa/LQA_V070_20261001.md) korunur.

**Oyun içi LQA: NOT TESTED.** Statik kaynak bağlantısı her NPC dalının oyunda erişilebildiğini kanıtlamaz; Sefton REVIEW durumundadır. Bu bakım çalışması oyun içi testi veya kurulum güncellemesi içermez.

## Geçmiş ve sonraki içerik çalışması

1 Ekim'e kadar yapılan işlemler [tarihsel günlükte](docs/history/FU_SESSION_CHECKPOINT_20261001.md), eski kapsam notları [sürüm arşivinde](docs/history/RELEASE_NOTES.md) bulunur. Geçmiş “bekliyor” ifadeleri güncel durum değildir.

Son içerik devri [v0.70 diyalog handoff](docs/handoffs/LUNA_DIALOGUE_HANDOFF_20261001.md) belgesidir. Buradaki yerel taslaklar başka checkout'ta bulunmayabilir; yeni içerik çalışması başladığında güncel katalog ve pinli kaynakla [planlama aracı](docs/TRANSLATION_PLANNING.md) üzerinden yeniden hazırlanır. Yeni çeviri bu repository bakımının kapsamı değildir.
