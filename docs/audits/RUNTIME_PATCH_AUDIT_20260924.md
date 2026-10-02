# Çok satırlı yamalar — 24 Eylül 2026

v0.63.2'de LF/CRLF farkı nedeniyle uygulanmayan metin yamaları düzeltildi. 802 dosyada bir arada bulunan 1.606 alan, tek kaynak karşılaştırması yüzünden birlikte atlanabiliyordu. Bir S.A.I.L. satırı ve üç karışık satır sonlu açıklama da etkilendi.

FU'nun kendi yamalarının değiştirdiği altı açıklama eski temel değerleri bekliyordu: yağ, Tech Konsolu, Böcek Ağı, çakıl, portakal ve Erimiş Çekirdek. Kaynakları ve çevirileri düzeltildi.

Her alan bağımsız koşullu `test`/`replace` grubunda üretilir. LF ve CRLF seçenekleri aynı kaynak metne bağlanır. Build, yamaları ham FU değerlerine ve FU'nun kendi yama katmanına uygulayarak kontrol eder.

FU 6.5.8 kaynak commit'i korundu. Altı Türkçe açıklama değişti. 49 temel oyun alanı o incelemede kurulu `packed.pak` ile eşleşti; diğer modların yama sırası ayrı değerlendirilir. [Test ve paketleme](../QA_PIPELINE.md)
