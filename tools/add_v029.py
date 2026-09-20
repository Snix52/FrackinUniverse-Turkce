#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_validate import parse_jsonc

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "fu_upstream"
CATALOG = Path(__file__).with_name("ceviriler.json")
NODES = (
    "tritaniumgear",
    "enrichedgear",
    "violiumgear",
    "feroziumgear",
    "aegisaltgear",
    "densealloygear",
    "effigiumgear",
)

SET = "^orange;Set Bonusları^reset;:"

# itemName: (shortdescription, description)
TR = {
    # Sadaklar
    "quiverbackair": (
        "Beceri Sadakı",
        "+^green;30^reset;% Havada Hasar (Yaylar)",
    ),
    "quiverback5": (
        "Eşsiz Sadak",
        "+^green;30^reset;% Hasar (Yaylar)\n"
        "+^green;30^reset;% Germe Hızı (Yaylar)\n"
        "+^green;20^reset;% Havada Hasar (Yaylar)\n"
        "-^green;9^reset; Atış Başına Enerji (Yaylar)",
    ),

    # Capturenaut
    "pandorasboxcapturenautchest": (
        "Capturenaut Göğüslüğü",
        SET + "\n^yellow;^reset; ^cyan;Canavar Ustası^reset;: 30%\n^yellow;^reset; ^cyan;Capturenaut^reset;",
    ),
    "pandorasboxcapturenauthead": (
        "Capturenaut Miğferi",
        SET + "\n^yellow;^reset; ^cyan;Canavar Ustası^reset;: 30%\n^yellow;^reset; ^cyan;Capturenaut^reset;",
    ),
    "pandorasboxcapturenautpants": (
        "Capturenaut Pantolonu",
        SET + "\n^yellow;^reset; ^cyan;Canavar Ustası^reset;: 30%\n^yellow;^reset; ^cyan;Capturenaut^reset;",
    ),
    "pandorasboxcapturenautpack": (
        "Capturenaut Paketi",
        "Yanında ek bir evcil hayvan bulundurmanı sağlayan bir sırt çantası.",
    ),

    # Kral Katili
    "fukingslayerchest": (
        "Kral Katili Plakası",
        SET + "\n^yellow;^reset; Can x^green;1.12^reset;\n^yellow;^reset; Yakın Dövüş: +^green;3^reset;%/^green;6^reset;% Kritik Şansı\n^yellow;^reset; ^cyan;Bağışıklık^reset;: Asit, Oksijensizlik",
    ),
    "fukingslayerhead": (
        "Kral Katili Miğferi",
        SET + "\n^yellow;^reset; Can x^green;1.12^reset;\n^yellow;^reset; Yakın Dövüş: +^green;3^reset;%/^green;6^reset;% Kritik Şansı\n^yellow;^reset; ^cyan;Bağışıklık^reset;: Asit, Oksijensizlik",
    ),
    "fukingslayerpants": (
        "Kral Katili Baldırlıkları",
        SET + "\n^yellow;^reset; Can x^green;1.12^reset;\n^yellow;^reset; Yakın Dövüş: +^green;3^reset;%/^green;6^reset;% Kritik Şansı\n^yellow;^reset; ^cyan;Bağışıklık^reset;: Asit, Oksijensizlik",
    ),

    # Kutup
    "sciencefuchest": ("Kutup Parkası", "Set Bonusları:\nBağışıklık: Tüm Soğuk Etkileri"),
    "sciencefuhead": ("Kutup Kapüşonu", "Set Bonusları:\nBağışıklık: Tüm Soğuk Etkileri"),
    "sciencefulegs": ("Kutup Kar Pantolonu", "Set Bonusları:\nBağışıklık: Tüm Soğuk Etkileri"),

    # Decker
    "kirhostier5mchest": (
        "Decker Giysisi",
        "Set Bonusları:\nPompalı Tüfek/Bombaatar: Hasar x1.25\nBağışıklık: Sıvı Azot, İrin, Zehirlenme",
    ),
    "kirhostier5mhead": (
        "Decker Vizörü",
        "^cyan;Kafa Lambası 2^reset;\nSet Bonusları:\nPompalı Tüfek/Bombaatar: Hasar x1.25\nBağışıklık: Sıvı Azot, İrin, Zehirlenme",
    ),
    "kirhostier5mpants": (
        "Decker Baldırlıkları",
        "Set Bonusları:\nPompalı Tüfek/Bombaatar: Hasar x1.25\nBağışıklık: Sıvı Azot, İrin, Zehirlenme",
    ),

    # Gishinanki
    "ff_diamondarmorchest": (
        "Gishinanki Göğüslüğü",
        "Set Bonusları:\nKatana Ustalığı: +32%\nKaçınma Teknolojileri: +20%\nSavunma Teknolojileri: +20%\nBağışıklık: Asit, Biyo-Balçık",
    ),
    "ff_diamondarmorhead": (
        "Gishinanki Miğferi",
        "Set Bonusları:\nKatana Ustalığı: +32%\nKaçınma Teknolojileri: +20%\nSavunma Teknolojileri: +20%\nBağışıklık: Asit, Biyo-Balçık",
    ),
    "ff_diamondarmorpants": (
        "Gishinanki Baldırlıkları",
        "Set Bonusları:\nKatana Ustalığı: +32%\nKaçınma Teknolojileri: +20%\nSavunma Teknolojileri: +20%\nBağışıklık: Asit, Biyo-Balçık",
    ),

    # Leviathan
    "fudiverchest3": (
        "Leviathan Zırhı",
        "Set Bonusları:\nYüzme Takviyesi 3\nOkyanus/Tidewater: +5% Kritik, Hasar x1.15\nBağışıklık: Asit, Zehirlenme, Biyo-Balçık, Gaz, Basınç, Oksijensizlik",
    ),
    "fudiverhead3": (
        "Leviathan Miğferi",
        "^cyan;Kafa Lambası 4^reset;\nSet Bonusları:\nYüzme Takviyesi 3\nOkyanus/Tidewater: +5% Kritik, Hasar x1.15\nBağışıklık: Asit, Zehirlenme, Biyo-Balçık, Gaz, Basınç, Oksijensizlik",
    ),
    "fudiverlegs3": (
        "Leviathan Tozlukları",
        "Set Bonusları:\nYüzme Takviyesi 3\nOkyanus/Tidewater: +5% Kritik, Hasar x1.15\nBağışıklık: Asit, Zehirlenme, Biyo-Balçık, Gaz, Basınç, Oksijensizlik",
    ),

    # Warp Madencisi
    "fuwarphunterchest": (
        "Warp Madencisi Tekno Ceketi",
        "Set Bonusları:\nYerçekimi Normalleştirmesi\nMaden Lazeri: Savaş Hasarı x3.4\nBağışıklık: Yanma, Proto-Zehir, Basınç, Oksijensizlik, Gaz, Buzda Kayma, Yerçekimi Yağmuru",
    ),
    "fuwarphunterhead": (
        "Warp Madencisi Miğferi",
        "^cyan;Kafa Lambası 3^reset;\nSet Bonusları:\nYerçekimi Normalleştirmesi\nMaden Lazeri: Savaş Hasarı x3.4\nBağışıklık: Yanma, Proto-Zehir, Basınç, Oksijensizlik, Gaz, Buzda Kayma, Yerçekimi Yağmuru",
    ),
    "fuwarphunterpants": (
        "Warp Madencisi Tekno Pantolonu",
        "Set Bonusları:\nYerçekimi Normalleştirmesi\nMaden Lazeri: Savaş Hasarı x3.4\nBağışıklık: Yanma, Proto-Zehir, Basınç, Oksijensizlik, Gaz, Buzda Kayma, Yerçekimi Yağmuru",
    ),

    # Cehennem Ateşi
    "hellfirechest": (
        "Cehennem Ateşi Göğüslüğü",
        "Set Bonusları:\nDarbe Alınca Ateş Novası\n^#ac522b;Parıltı^reset;\nAlev Makinesi/Cehennem Ateşi: Hasar x1.25\nBağışıklık: Aşırı Sıcak, Yanma",
    ),
    "hellfirelegs": (
        "Cehennem Ateşi Baldırlıkları",
        "Set Bonusları:\nDarbe Alınca Ateş Novası\n^#ac522b;Parıltı^reset;\nAlev Makinesi/Cehennem Ateşi: Hasar x1.25\nBağışıklık: Aşırı Sıcak, Yanma",
    ),
    "hellfirehelm": (
        "Cehennem Ateşi Miğferi",
        "Set Bonusları:\nDarbe Alınca Ateş Novası\n^#ac522b;Parıltı^reset;\nAlev Makinesi/Cehennem Ateşi: Hasar x1.25\nBağışıklık: Aşırı Sıcak, Yanma",
    ),

    # Legionii
    "fumantizitier5mchest": (
        "Legionii Segmentorum",
        "Set Bonusları:\n+30% Kalkan Yenilenmesi, +20% Geri Tepme Direnci\nMızrak, Kısa Mızrak: +4% Kritik\nBağışıklık: Gaz",
    ),
    "fumantizitier5mhead": (
        "Legionii Miğferi",
        "Set Bonusları:\n+30% Kalkan Yenilenmesi, +20% Geri Tepme Direnci\nMızrak, Kısa Mızrak: +4% Kritik\nBağışıklık: Gaz",
    ),
    "fumantizitier5mpants": (
        "Legionii Baldırlıkları",
        "Set Bonusları:\n+30% Kalkan Yenilenmesi, +20% Geri Tepme Direnci\nMızrak, Kısa Mızrak: +4% Kritik\nBağışıklık: Gaz",
    ),

    # Millenion
    "fumantizitier5schest": (
        "Millenion Paltosu",
        "Set Bonusları:\n+30% Kalkan Yenilenmesi, Blok, Dayanıklılık\nKalkan + Kılıç: Can x1.2, +25% Geri Tepme Direnci\nBağışıklık: Katran, Gaz",
    ),
    "fumantizitier5shead": (
        "Millenion Miğferi",
        "Set Bonusları:\n+30% Kalkan Yenilenmesi, Blok, Dayanıklılık\nKalkan + Kılıç: Can x1.2, +25% Geri Tepme Direnci\nBağışıklık: Katran, Gaz",
    ),
    "fumantizitier5spants": (
        "Millenion Baldırlıkları",
        "Set Bonusları:\n+30% Kalkan Yenilenmesi, Blok, Dayanıklılık\nKalkan + Kılıç: Can x1.2, +25% Geri Tepme Direnci\nBağışıklık: Katran, Gaz",
    ),

    # Morphite
    "fuquantumchest": ("Morphite Göğüslüğü", "Set Bonusları:\nBağışıklık: Sülfürik Asit"),
    "fuquantumhead": ("Morphite Miğferi", "Set Bonusları:\nBağışıklık: Sülfürik Asit"),
    "fuquantumlegs": ("Morphite Baldırlıkları", "Set Bonusları:\nBağışıklık: Sülfürik Asit"),

    # Rifter
    "kirhostier5schest": (
        "Rifter Ağır Giysisi",
        "Set Bonusları:\nDüşme Hasarı x0.75\nMagnorb, Çakram, Bumerang: Hasar x1.25, +3% Kritik Şansı\nBağışıklık: Gaz, Proto-Zehir",
    ),
    "kirhostier5shead": (
        "Rifter Miğferi",
        "Set Bonusları:\nDüşme Hasarı x0.75\nMagnorb, Çakram, Bumerang: Hasar x1.25, +3% Kritik Şansı\nBağışıklık: Gaz, Proto-Zehir",
    ),
    "kirhostier5spants": (
        "Rifter Baldırlıkları",
        "Set Bonusları:\nDüşme Hasarı x0.75\nMagnorb, Çakram, Bumerang: Hasar x1.25, +3% Kritik Şansı\nBağışıklık: Gaz, Proto-Zehir",
    ),

    # Nöbetçi
    "mobiuschest": (
        "Nöbetçi Plakası",
        "Set Bonusları:\nEnerji/Can x1.15\nEnerji Tüfekleri: Hasar x1.25",
    ),
    "mobiushead": (
        "Nöbetçi Miğferi",
        "Set Bonusları:\nEnerji/Can x1.15\nEnerji Tüfekleri: Hasar x1.25",
    ),
    "mobiuspants": (
        "Nöbetçi Pantolonu",
        "Set Bonusları:\nEnerji/Can x1.15\nEnerji Tüfekleri: Hasar x1.25",
    ),

    # Valkyrie
    "kirhostier5ahead2": (
        "Valkyrie Tam Miğferi",
        "Set Bonusları:\nYavaş Düşüş\nBağışıklık: Oksijensizlik, Basınç, Gaz, Aşırı Radyasyon",
    ),
    "kirhostier5achest": (
        "Valkyrie Ağır Giysisi",
        "Set Bonusları:\nYavaş Düşüş\nBağışıklık: Oksijensizlik, Basınç, Gaz, Aşırı Radyasyon",
    ),
    "kirhostier5ahead": (
        "Valkyrie Miğferi",
        "Set Bonusları:\nYavaş Düşüş\nBağışıklık: Oksijensizlik, Basınç, Gaz, Aşırı Radyasyon",
    ),
    "kirhostier5apants": (
        "Valkyrie Baldırlıkları",
        "Set Bonusları:\nYavaş Düşüş\nBağışıklık: Oksijensizlik, Basınç, Gaz, Aşırı Radyasyon",
    ),

    # Warframe
    "fumantizitier5achest": (
        "Warframe Zırhı",
        "Set Bonusları:\nTaarruz Tüfeği, Tabanca: Hasar x1.25\nBağışıklık: Basınç, Gaz",
    ),
    "fumantizitier5ahead": (
        "Warframe Miğferi",
        "Set Bonusları:\nTaarruz Tüfeği, Tabanca: Hasar x1.25\nBağışıklık: Basınç, Gaz",
    ),
    "fumantizitier5apants": (
        "Warframe Pantolonu",
        "Set Bonusları:\nTaarruz Tüfeği, Tabanca: Hasar x1.25\nBağışıklık: Basınç, Gaz",
    ),

    # Şampiyon
    "fumantizitier6schest": (
        "Şampiyon Kabuğu",
        "Set Bonusları:\nÇekiç, Balta, Topuz: Hasar x1.3, +3% Kritik Şansı\nBağışıklık: Orta Dereceli Soğuk, Katran, Çamur, Kil",
    ),
    "fumantizitier6shead": (
        "Şampiyon Çenesi",
        "Set Bonusları:\nÇekiç, Balta, Topuz: Hasar x1.3, +3% Kritik Şansı\nBağışıklık: Orta Dereceli Soğuk, Katran, Çamur, Kil",
    ),
    "fumantizitier6spants": (
        "Şampiyon Taytı",
        "Set Bonusları:\nÇekiç, Balta, Topuz: Hasar x1.3, +3% Kritik Şansı\nBağışıklık: Orta Dereceli Soğuk, Katran, Çamur, Kil",
    ),

    # Güneş Gezgini
    "fusunwalkerchest": (
        "Güneş Gezgini Göğüslüğü",
        "Set Bonusları:\nPlazma Silahları: Hasar x1.15\nBağışıklık: Aşırı Sıcak/Soğuk/Radyasyon, Basınç, Oksijensizlik",
    ),
    "fusunwalkerhead": (
        "Güneş Gezgini Miğferi",
        "Set Bonusları:\nPlazma Silahları: Hasar x1.15\nBağışıklık: Aşırı Sıcak/Soğuk/Radyasyon, Basınç, Oksijensizlik",
    ),
    "fusunwalkerpants": (
        "Güneş Gezgini Cübbesi",
        "Set Bonusları:\nPlazma Silahları: Hasar x1.15\nBağışıklık: Aşırı Sıcak/Soğuk/Radyasyon, Basınç, Oksijensizlik",
    ),

    # Morphite Mk. 2
    "fuquantumchestadv": (
        "Morphite Göğüslüğü Mk. 2",
        "Set Bonusları:\nBağışıklık: Aşırı Sıcak/Soğuk/Radyasyon, Asit",
    ),
    "fuquantumheadadv": (
        "Morphite Miğferi Mk. 2",
        "Set Bonusları:\nBağışıklık: Aşırı Sıcak/Soğuk/Radyasyon, Asit",
    ),
    "fuquantumlegsadv": (
        "Morphite Baldırlıkları Mk. 2",
        "Set Bonusları:\nBağışıklık: Aşırı Sıcak/Soğuk/Radyasyon, Asit",
    ),

    # Replikant
    "kirhostier6achest": (
        "Replikant Ağır Giysisi",
        "Set Bonusları:\nTek Kılıç: +2% Kritik,\nÇift Kılıçlar: Hasar x1.25\nBağışıklık: Gaz, Gölge Lekesi, Katran^reset;",
    ),
    "kirhostier6ahead": (
        "Replikant Miğferi",
        "Set Bonusları:\nTek Kılıç: +2% Kritik,\nÇift Kılıçlar: Hasar x1.25\nBağışıklık: Gaz, Gölge Lekesi, Katran^reset;",
    ),
    "kirhostier6apants": (
        "Replikant Baldırlıkları",
        "Set Bonusları:\nTek Kılıç: +2% Kritik,\nÇift Kılıçlar: Hasar x1.25\nBağışıklık: Gaz, Gölge Lekesi, Katran^reset;",
    ),
}


def green(value: str) -> str:
    return f"^green;{value}^reset;"


def cyan(value: str) -> str:
    return f"^cyan;{value}^reset;"


def stats(*lines: str) -> str:
    bullet = "^yellow;^reset; "
    return SET + "\n" + "\n".join(bullet + line for line in lines)


# Renk ve ikon kodları Starbound tooltip düzeninin parçasıdır. Aşağıdaki ortak
# set metinleri, kaynakla birebir aynı kod çokluğunu koruyarak adları Türkçeleştirir.
DESCRIPTIONS = {
    "arctic": stats(cyan("Bağışıklık") + ": Tüm Soğuk Etkileri"),
    "decker": stats(
        "Pompalı Tüfek/Bombaatar: Hasar x" + green("1.25"),
        cyan("Bağışıklık") + ": Sıvı Azot, İrin, Zehirlenme",
    ),
    "gishinanki": stats(
        "Katana Ustalığı:  +" + cyan("32") + "%",
        "Kaçınma Teknolojileri:  +" + green("20") + "%",
        "Savunma Teknolojileri:  +" + green("20") + "%",
        cyan("Bağışıklık") + ": Asit, Biyo-Balçık",
    ),
    "leviathan": stats(
        cyan("Yüzme Takviyesi 3"),
        "Okyanus/Tidewater: +" + green("5") + "% Kritik, Hasar x" + green("1.15"),
        cyan("Bağışıklık") + ": Asit, Zehirlenme, Biyo-Balçık, Gaz, Basınç, Oksijensizlik",
    ),
    "warp": stats(
        cyan("Yerçekimi Normalleştirmesi"),
        "Maden Lazeri: Savaş Hasarı x" + green("3.4"),
        cyan("Bağışıklık") + ": Yanma, Proto-Zehir, Basınç, Oksijensizlik, Gaz, Buzda Kayma, Yerçekimi Yağmuru",
    ),
    "hellfire": stats(
        cyan("Darbe Alınca Ateş Novası"),
        "^#ac522b;Parıltı^reset;",
        "Alev Makinesi/Cehennem Ateşi: Hasar x" + green("1.25"),
        cyan("Bağışıklık") + ": Aşırı Sıcak, Yanma",
    ),
    "legionii": stats(
        "+" + green("30") + "% Kalkan Yenilenmesi, +" + green("20") + "% Geri Tepme Direnci",
        "Mızrak, Kısa Mızrak: +" + green("4") + "% Kritik",
        cyan("Bağışıklık") + ": Gaz",
    ),
    "millenion": stats(
        "+" + green("30") + "% Kalkan Yenilenmesi, Blok, Dayanıklılık",
        "Kalkan + Kılıç: Can x" + green("1.2") + ", +" + green("25") + "% Geri Tepme Direnci",
        cyan("Bağışıklık") + ": Katran, Gaz",
    ),
    "morphite": stats(cyan("Bağışıklık") + ": Sülfürik Asit"),
    "rifter": stats(
        "Düşme Hasarı x" + green("0.75"),
        "Magnorb, Çakram, Bumerang: Hasar x" + green("1.25") + ", +" + green("3") + "% Kritik Şansı",
        cyan("Bağışıklık") + ": Gaz, Proto-Zehir",
    ),
    "sentry": stats(
        "Enerji/Can x" + green("1.15"),
        "Enerji Tüfekleri: Hasar x" + green("1.25"),
    ),
    "valkyrie": stats(
        cyan("Yavaş Düşüş"),
        cyan("Bağışıklık") + ": Oksijensizlik, Basınç, Gaz, Aşırı Radyasyon",
    ),
    "warframe": stats(
        "Taarruz Tüfeği, Tabanca: Hasar x" + green("1.25"),
        cyan("Bağışıklık") + ": Basınç, Gaz",
    ),
    "champion": stats(
        "Çekiç, Balta, Topuz: Hasar x" + green("1.3") + ", +" + green("3") + "% Kritik Şansı",
        cyan("Bağışıklık") + ": Orta Dereceli Soğuk, Katran, Çamur, Kil",
    ),
    "sunwalker": stats(
        "Plazma Silahları: Hasar x" + green("1.15"),
        cyan("Bağışıklık") + ": Aşırı Sıcak/Soğuk/Radyasyon, Basınç, Oksijensizlik",
    ),
    "morphite2": stats(cyan("Bağışıklık") + ": Aşırı Sıcak/Soğuk/Radyasyon, Asit"),
    "replicant": stats(
        "Tek Kılıç: +" + green("2") + "% Kritik,",
        "Çift Kılıçlar: Hasar x" + green("1.25"),
        cyan("Bağışıklık") + ": Gaz, Gölge Lekesi, Katran^reset;",
    ),
}

GROUPS = {
    "arctic": ("sciencefuchest", "sciencefuhead", "sciencefulegs"),
    "decker": ("kirhostier5mchest", "kirhostier5mhead", "kirhostier5mpants"),
    "gishinanki": ("ff_diamondarmorchest", "ff_diamondarmorhead", "ff_diamondarmorpants"),
    "leviathan": ("fudiverchest3", "fudiverhead3", "fudiverlegs3"),
    "warp": ("fuwarphunterchest", "fuwarphunterhead", "fuwarphunterpants"),
    "hellfire": ("hellfirechest", "hellfirelegs", "hellfirehelm"),
    "legionii": ("fumantizitier5mchest", "fumantizitier5mhead", "fumantizitier5mpants"),
    "millenion": ("fumantizitier5schest", "fumantizitier5shead", "fumantizitier5spants"),
    "morphite": ("fuquantumchest", "fuquantumhead", "fuquantumlegs"),
    "rifter": ("kirhostier5schest", "kirhostier5shead", "kirhostier5spants"),
    "sentry": ("mobiuschest", "mobiushead", "mobiuspants"),
    "valkyrie": ("kirhostier5ahead2", "kirhostier5achest", "kirhostier5ahead", "kirhostier5apants"),
    "warframe": ("fumantizitier5achest", "fumantizitier5ahead", "fumantizitier5apants"),
    "champion": ("fumantizitier6schest", "fumantizitier6shead", "fumantizitier6spants"),
    "sunwalker": ("fusunwalkerchest", "fusunwalkerhead", "fusunwalkerpants"),
    "morphite2": ("fuquantumchestadv", "fuquantumheadadv", "fuquantumlegsadv"),
    "replicant": ("kirhostier6achest", "kirhostier6ahead", "kirhostier6apants"),
}

HEADLAMPS = {
    "kirhostier5mhead": 2,
    "fudiverhead3": 4,
    "fuwarphunterhead": 3,
}

for group, item_names in GROUPS.items():
    for item_name in item_names:
        short_tr, _ = TR[item_name]
        description = DESCRIPTIONS[group]
        if item_name in HEADLAMPS:
            description = f"^cyan;Kafa Lambası {HEADLAMPS[item_name]}^reset;\n" + description
        TR[item_name] = (short_tr, description)


def recipe_outputs() -> set[str]:
    outputs: set[str] = set()
    for path in SOURCE.rglob("*.recipe"):
        try:
            data = parse_jsonc(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        output = data.get("output")
        if isinstance(output, dict) and isinstance(output.get("item"), str):
            outputs.add(output["item"])
    return outputs


def armor_assets() -> dict[str, tuple[str, dict]]:
    assets: dict[str, tuple[str, dict]] = {}
    for pattern in ("*.back", "*.chest", "*.head", "*.legs"):
        for path in SOURCE.rglob(pattern):
            try:
                data = parse_jsonc(path.read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            item_name = data.get("itemName")
            if isinstance(item_name, str):
                if item_name in assets:
                    raise SystemExit(f"Yinelenen zırh itemName: {item_name}")
                assets[item_name] = (path.relative_to(SOURCE).as_posix(), data)
    return assets


def main() -> None:
    ledger = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = ledger["translations"]
    existing = {(row["asset"], row["pointer"]) for row in rows}
    tree = parse_jsonc(
        (SOURCE / "zb/researchTree/fu_warcraft.config").read_text(encoding="utf-8-sig")
    )["researchTree"]["fu_warcraft"]
    unlocked = {item for node in NODES for item in tree[node]["unlocks"]}
    outputs = recipe_outputs()
    assets = armor_assets()

    selected: dict[str, tuple[str, dict]] = {}
    for item_name in sorted(unlocked):
        if item_name not in outputs or item_name not in assets:
            continue
        asset, data = assets[item_name]
        if (asset, "/shortdescription") in existing:
            continue
        selected[item_name] = (asset, data)

    missing = sorted(set(selected) - set(TR))
    extra = sorted(set(TR) - set(selected))
    if missing or extra:
        raise SystemExit(f"TR kapsamı uyuşmuyor. Eksik={missing!r}, fazla={extra!r}")
    if len(selected) != 61:
        raise SystemExit(f"Beklenen 61 yeni Kademe 5 zırh asseti yerine {len(selected)} bulundu")

    for item_name, (asset, data) in sorted(selected.items(), key=lambda pair: pair[1][0]):
        short_tr, description_tr = TR[item_name]
        for pointer, source_key, translated in (
            ("/shortdescription", "shortdescription", short_tr),
            ("/description", "description", description_tr),
        ):
            source_text = data.get(source_key)
            if not isinstance(source_text, str):
                raise SystemExit(f"Görünür alan eksik: {asset}{pointer}")
            rows.append(
                {
                    "asset": asset,
                    "pointer": pointer,
                    "en": source_text,
                    "tr": translated,
                    "section": "v0.29 Kademe 5 aktif zırh setleri",
                }
            )

    ledger["translation_version"] = "0.29.0-beta"
    ledger["note"] = (
        "v0.29 Kademe 5 aktif zırh setleri: Zırh ve Silahlar araştırma ağacındaki "
        "tritaniumgear, enrichedgear, violiumgear, feroziumgear, aegisaltgear, "
        "densealloygear ve effigiumgear düğümlerinin açtığı, gerçek üretim tarifi "
        "bulunan 61 zırh assetinde 122 görünür alan yerelleştirildi. Runtime araştırma "
        "ve tarif zinciri esas alındığı için kaynak yolu tier4 veya tier6 olan erişilebilir parçalar "
        "da kapsama dahildir. Toplam 5190 structured + 15 Lua, 1673 patch asset + 1 "
        "raw override. Oyun içi LQA bekliyor."
    )
    CATALOG.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "new_assets": len(selected),
                "new_fields": len(selected) * 2,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
