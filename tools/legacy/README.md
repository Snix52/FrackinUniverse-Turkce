# Tarihsel tek seferlik üreticiler

Bu 25 script eski sürümlerin nasıl hazırlandığını belgelemek için korunur. Katalog veya manifest yazan eski üreticiler oldukları için güncel çeviri ve CI komutları arasından ayrılmıştır. Doğrudan çalıştırıldıklarında dosya yazmadan açıklayıcı hata ile dururlar.

İçerikleri eski kaynak checkout'u, katalog sürümü ve dosya konumu varsayımları taşır. Güncel kataloğu yeniden üretmek için kullanılmazlar. Yeni çeviriler [planlama akışından](../../docs/TRANSLATION_PLANNING.md) hazırlanır ve güncel salt okunur kaynak kapılarıyla doğrulanır.

`generate_v039` içindeki onaylı satır yardımcı işlevi mevcut regresyon testinde kullanılmaya devam eder. Bu modülün import edilmesi ana kataloğu değiştirmez; onaylı veriyi üst klasördeki `v039_translations.json` manifestinden okur.
