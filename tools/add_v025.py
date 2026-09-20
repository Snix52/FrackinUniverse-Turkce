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
    "bonegear",
    "slimegear1",
    "irongear",
    "cottongear",
    "telebriumgear",
    "lunarigear",
    "elduugear",
    "skathgear",
    "tungstengear",
)

TR: dict[str, tuple[str, str]] = {}


def add_set(names: dict[str, str], description: str) -> None:
    for item_name, shortdescription in names.items():
        if item_name in TR:
            raise ValueError(f"Yinelenen zırh kimliği: {item_name}")
        TR[item_name] = (shortdescription, description)


add_set(
    {
        "fubonearmorlegs": "Kemik Baldırlık",
        "fubonearmorchest": "Kemik Göğüslük",
        "fubonearmorhead": "Kemik Maske",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Can x^green;1.05^reset;, Düşme Hasarı x^green;0.85^reset;^reset;\n"
    "^yellow;^reset; Uzun Kılıç veya Balta: Hasar x^green;1.15^reset;\n"
    "^yellow;^reset; ^cyan;Yemyeşil/Orman^reset;: Can x^green;1.05^reset;, Hasar x^green;1.05^reset;, +^green;5^reset;% Fiziksel Direnç^reset;",
)

add_set(
    {
        "invisibleslimeback": "Görünmez Sırtlık",
        "invisibleslimelegs": "Görünmez Pantolon",
        "invisibleslimechest": "Görünmez Gömlek",
        "invisibleslimehead": "Görünmez Maske",
    },
    "Burada görülecek bir şey yok.",
)
add_set(
    {
        "ff_slimelegs": "Balçık Baldırlık",
        "ff_slimechest": "Balçık Göğüslük",
        "ff_slimehead": "Balçık Miğfer",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^cyan;Yardımcı Çağırır^reset;: Balçıklar\n"
    "^yellow;^reset; Can x^green;1.1^reset;\n"
    "^yellow;^reset; Balçık silahları: Hasar x^green;1.1^reset;/^green;1.2^reset;, +^green;5%^reset; Kritik Şansı;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Balçık, Çamur, Kil",
)

TR.update(
    {
        "funoobpack": (
            "Çekirdek Paketi",
            "^yellow;60 sn^reset; oksijen, ^orange;soluk bir ışık^reset; ve %10 ^blue;soğuk direnci^reset; sağlayan son derece basit bir tüp.",
        ),
        "armoredsnowpants": (
            "Takviyeli Kar Pantolonu",
            "Bu pantolonla karda hız kesmezsin.\n+^green;15^reset;% Buz Direnci\n^cyan;Bağışıklık: Kar, Buz ve Sulu Kar^reset;",
        ),
        "snowgoggles": (
            "Kar Gözlüğü",
            "Tipide gözlerini korur.\n+^green;8^reset;% Buz Direnci",
        ),
    }
)
add_set(
    {
        "fumantizitier1pants": "Sıradan Baldırlık",
        "fumantizitier1chest": "Sıradan Zırh",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;15^reset;% Kalkan Canı ve Yenilenmesi\n"
    "^yellow;^reset; Kılıç/Topuz + Kalkan: Can x^green;1.2^reset;, +^green;15^reset;% Geri Tepme Direnci",
)
add_set(
    {
        "fuspacediverlegs": "Uzay Dalgıcı Pantolonu",
        "fuspacediverchest": "Uzay Dalgıcı Giysisi",
        "fuspacediverhead": "Uzay Dalgıcı Miğferi",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;20^reset;% Geri Tepme Direnci, ^green;2x^reset; Nefes\n"
    "^yellow;^reset; Zıpkın Tüfeği: Hasar x^green;1.2^reset;",
)
add_set(
    {
        "bloodhoundlegs": "Kan Tazısı Baldırlığı",
        "bloodhoundchest": "Kan Tazısı Göğüslüğü",
        "bloodhoundhead": "Kan Tazısı Miğferi",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Hasar x^green;1.05^reset;\n"
    "^yellow;^reset; Tırpan/Keskin Nişancı Tüfeği: +^green;2^reset;% Kritik Şansı, Hasar x^green;1.15^reset;\n"
    "^yellow;^reset; Çorak/Eden: Hasar/Can x^green;1.25^reset;",
)
add_set(
    {
        "missionaryrobepants": "Keşiş Pantolonu",
        "missionaryrobechest": "Keşiş Cübbesi",
        "missionaryrobehead": "Keşiş Kapüşonu",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;5^reset;% Hız ve Zıplama\n"
    "^yellow;^reset; +^green;5^reset;% Kritik Hasarı^reset;\n"
    "^yellow;^reset; Çift Yumruk/Dövüş Asası: Hasar x^green;1.15^reset;",
)
add_set(
    {
        "leatherpants": "Deri Pantolon",
        "leatherchest": "Deri Yelek",
        "leatherhead": "Deri Başlık",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;1^reset;% Kritik Şansı, +^green;2.5^reset;% Hız\n"
    "^yellow;^reset; Bahçe/Orman: Enerji x^green;1.05^reset;, +^green;5^reset;% Geri Tepme Direnci\n"
    "^yellow;^reset; Yay/Arbalet^reset;: +^green;2^reset;% Kritik Şansı, Hasar x^green;1.15^reset;, -^green;4^reset; Atış Başına Enerji, +^green;5^reset; Havada Hasar, +^green;10^reset;% Germe Hızı",
)
add_set(
    {
        "kirhostier1pants": "Yeraltı Baldırlığı",
        "kirhostier1chest": "Yeraltı Göğüslüğü",
        "kirhostier1head": "Yeraltı Gözlüğü",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Tabanca/Makineli Tabanca: +^green;1^reset;/+^green;2.5^reset;% Kritik Şansı\n"
    "^yellow;^reset; Taarruz/Keskin Nişancı Tüfeği: +^green;2^reset;% Kritik Şansı^reset;",
)

add_set(
    {
        "fubearlegs": "Savaş Totemi Baldırlığı",
        "fubearchest": "Savaş Totemi Zırhı",
        "fubearhead": "Savaş Totemi Maskesi",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Çekiç ve Büyük Balta Ustalığı: +^green;20^reset;%\n"
    "^yellow;^reset; +^green;20^reset;% Geri Tepme Direnci\n"
    "^yellow;^reset; Baltalar, Çift Elli Yakın Dövüş: +^green;3.5^reset;% Kritik Şansı, Hasar x^green;1.15^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Sulu Kar, Üşüme",
)
add_set(
    {
        "bloodgarbpants": "Kan Kızılı Çizme",
        "bloodgarbchest": "Kan Kızılı Yelek",
        "bloodgarbhead": "Kan Kızılı Taç",
    },
    "+^green;5^reset;% İyileştirme Gücü\n"
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;10^reset;% Hız\n"
    "^yellow;^reset; +^green;5^reset;% Can Çalma\n"
    "^yellow;^reset; Hançer/Kırbaç/Ezici: +^green;4^reset;% Kritik Şansı, +^green;5^reset;% Can Çalma",
)
add_set(
    {
        "deckardpants": "Avare Pantolonu",
        "deckardchest": "Avare Paltosu",
        "deckardhead": "Avare Vizörü",
    },
    "^orange;^orange;Set Bonusları^reset;: ^reset;\n"
    "^yellow;^reset; +^green;10^reset;% Hız\n"
    "^yellow;^reset; Tabanca/Makineli Tabanca: Hasar x^green;1.075/1.15^reset;",
)
add_set(
    {
        "fuoperativelegs": "Ajan Bacak Zırhı",
        "fuoperativechest": "Ajan Göğüs Zırhı",
        "fuoperativehead": "Ajan Başlığı",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;4^reset;% Kritik Şansı, +^green;20^reset;% Kritik Hasarı\n"
    "^yellow;^reset; +^green;8^reset;% Hız/Zıplama",
)
add_set(
    {
        "fuwolflegs": "Diş Şamanı Pantolonu",
        "fuwolfchest": "Diş Şamanı Paltosu",
        "fuwolfhead": "Diş Şamanı Kapüşonu",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Hançer Ustalığı: +^green;15^reset;%\n"
    "^yellow;^reset; Hançer/Kısa Kılıç: +^green;10^reset;/^green;20^reset;% Kritik Hasarı\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Kar, Üşüme^reset;",
)
add_set(
    {
        "fubeesuitpants": "Arıcı Pantolonu",
        "fubeesuitchest": "Arıcı Zırhı",
        "fubeesuithead": "Arıcı Miğferi",
    },
    "Can yakıcı arı sokmalarını önler!",
)
add_set(
    {
        "fudesertwalkerpants": "Göçebe Pantolonu",
        "fudesertwalkerchest": "Göçebe Cübbesi",
        "fudesertwalkerhead": "Göçebe Kapüşonu",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;20^reset;% Kalkan Yenilenmesi^reset;\n"
    "^yellow;^reset; Hançer/Kısa Mızrak: Hasar x^green;1.15^reset;\n"
    "^yellow;^reset; Taarruz/Keskin Nişancı Tüfeği: Hasar x^green;1.08^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Yanma, Kum Fırtınaları, Batak Kum",
)
add_set(
    {
        "cannoneerlegs": "Kılıçbaz Pantolonu",
        "cannoneerchest": "Kılıçbaz Paltosu",
        "cannoneerhead": "Kılıçbaz Şapkası",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Meç Ustalığı: +^green;15^reset;%\n"
    "^yellow;^reset; +^green;8^reset;% Zıplama, -^green;20^reset;% Açlık Tüketimi\n"
    "^yellow;^reset; Meç/Tabanca: Hasar x^green;1.075^reset;/^green;1.15^reset;",
)
add_set(
    {
        "kirhostier2pants": "Hacker Pantolonu",
        "kirhostier2chest": "Hacker Paltosu",
        "kirhostier2head": "Hacker Maskesi",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;25^reset;% Enerji Yenilenmesi\n"
    "^yellow;^reset; Ezici: +^green;1^reset;% Kritik Şansı\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Gaz",
)

TELEBRIUM_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Can x^green;1.1^reset;\n"
    "^yellow;^reset; Pompalı/Taarruz Tüfeği: Hasar x^green;1.15^reset;"
)
add_set(
    {
        "fumantizitier2pants": "Telebrium Baldırlık",
        "fumantizitier2chest": "Telebrium Zırh",
    },
    TELEBRIUM_DESC,
)
TR["fumantizitier2head"] = (
    "Telebrium Miğfer",
    "^cyan;Kafa Lambası^reset;\n" + TELEBRIUM_DESC,
)
add_set(
    {
        "lunarilegs": "Lunari Baldırlık",
        "lunarichest": "Lunari Zırh",
        "lunarihead": "Lunari Miğfer",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;12^reset;% Enerji Yenilenmesi\n"
    "^yellow;^reset; Lunari silahları: Hasar x^green;1.15^reset;, +^green;4^reset;% Kritik Şansı",
)

TR.update(
    {
        "templeguardpants": ("Tapınak Şortu", "Altın halhallı bir şort."),
        "templeguardchest": ("Tapınak Gömleği", "Kristalden dokunmuş kolsuz bir gömlek."),
        "templeguardhead": ("Tapınak Miğferi", "Eld'uukhar muhafızlarının giydiği bir miğfer."),
    }
)
add_set(
    {
        "worshipperpants": "Mürit Örtüsü",
        "worshipperchest": "Mürit Gömleği",
        "worshipperhead": "Mürit Miğferi",
        "worshipperhead2": "Mürit Miğferi",
        "worshipperhead3": "Mürit Miğferi",
        "worshipperhead4": "Mürit Miğferi",
        "worshipperhead5": "Mürit Miğferi",
    },
    "Ahvis müritlerinin giysisi.",
)
add_set(
    {
        "inviselduuhead": "Görünmez Şapka",
        "inviselduuchest": "Görünmez Gömlek",
        "inviselduupants": "Görünmez Pantolon",
    },
    "Bunların giysi olduğuna emin misin?",
)


def skath_description(multiplier: str, oxygen: bool = False) -> str:
    value = (
        "^orange;Set Bonusları^reset;:\n"
        f"^yellow;^reset; Taarruz Tüfeği/Kısa Kılıç: Hasar x^green;{multiplier}^reset;"
    )
    if oxygen:
        value += "\n^yellow;^reset; ^cyan;Bağışıklık^reset;: Oksijensizlik"
    return value


add_set(
    {
        "skathtier1pants": "Ağcı Pantolonu",
        "skathtier1chest": "Ağcı Göğüslüğü",
        "skathtier1head": "Ağcı Miğferi",
    },
    skath_description("1.1"),
)
add_set(
    {
        "skathtier2pants": "Bataklık Gezgini Pantolonu",
        "skathtier2chest": "Bataklık Gezgini Göğüslüğü",
        "skathtier2head": "Bataklık Gezgini Miğferi",
    },
    skath_description("1.13"),
)
add_set(
    {
        "skathtier3spants": "Vizyoner Pantolonu",
        "skathtier3schest": "Vizyoner Tekno Ceketi",
        "skathtier3shead": "Vizyoner Miğferi",
    },
    skath_description("1.16", oxygen=True),
)
add_set(
    {
        "skathtier3mpants": "Dracon Pantolonu",
        "skathtier3mchest": "Dracon Göğüs Koruması",
        "skathtier3mhead": "Dracon Miğferi",
    },
    skath_description("1.19", oxygen=True),
)
add_set(
    {
        "skathtier3apants": "Warscorned Pantolonu",
        "skathtier3achest": "Warscorned Göğüs Koruması",
        "skathtier3ahead": "Warscorned Miğferi",
    },
    skath_description("1.22", oxygen=True),
)

TR.update(
    {
        "quiverback2": (
            "Kaliteli Sadak",
            "+^green;15^reset;% Hasar (Yaylar)\n"
            "+^green;15^reset;% Germe Hızı (Yaylar)\n"
            "+^green;4^reset;% Havada Hasar (Yaylar)\n"
            "-^green;3^reset; Atış Başına Enerji (Yaylar)",
        ),
        "fuhoodedmask": (
            "Kapüşonlu Hayatta Kalma Maskesi",
            "Yenileyici kaplama ve biraz gizem. Eğlenceli!",
        ),
    }
)
add_set(
    {
        "fudarkrobespants": "İz Sürücü Pantolonu",
        "fudarkrobeschest": "İz Sürücü Cübbesi",
        "fudarkrobeshelmet": "İz Sürücü Kapüşonu",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;8^reset;% Hız, Düşme Hasarı x^green;0.75^reset;\n"
    "^yellow;^reset; Yay/Arbalet, Keskin Nişancı Tüfeği: Hasar x^green;1.15^reset;, +^green;3^reset;% Kritik Şansı\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Zehirlenme, Biyo-Balçık",
)
HAZARD_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Azami Nefes x^green;2^reset;\n"
    "^yellow;^reset; Uzun Kılıç/Enerji: Hasar x^green;1.12^reset;"
)
add_set(
    {
        "tw_spacesuitlegs": "Tehlikeli Ortam Pantolonu",
        "tw_spacesuitchest": "Tehlikeli Ortam Göğüslüğü",
    },
    HAZARD_DESC,
)
TR["tw_spacesuithead"] = (
    "Tehlikeli Ortam Miğferi",
    "^cyan;Kafa Lambası^reset;\n" + HAZARD_DESC,
)
add_set(
    {
        "fumantiziroyalguardpants": "Yılmaz Pantolon",
        "fumantiziroyalguardchest": "Yılmaz Zırh",
        "fumantiziroyalguardhead": "Yılmaz Miğfer",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Kısa Mızrak Ustalığı: +^green;15^reset;%\n"
    "^yellow;^reset; +^green;15^reset;% Geri Tepme Direnci\n"
    "^yellow;^reset; Savunma x^green;1.15^reset;\n"
    "^yellow;^reset; Tüm Mızraklar: Hasar x^green;1.15^reset;",
)
add_set(
    {
        "fumantiziroyalguardornatepants": "Piyade Pantolonu",
        "fumantiziroyalguardornatechest": "Piyade Zırhı",
        "fumantiziroyalguardornatehead": "Piyade Miğferi",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Kısa Kılıç/Uzun Kılıç/Topuz Ustalığı: +^green;15^reset;%\n"
    "^yellow;^reset; +^green;17^reset;% Kalkan Canı ve Yenilenmesi\n"
    "^yellow;^reset; Kılıç/Topuz ve Kalkan: +^green;2^reset;% Kritik Şansı, +^green;15^reset;% Kritik Hasarı, +^green;15^reset;% Geri Tepme Direnci",
)
add_set(
    {
        "fusamurailegs": "Samuray Pantolonu",
        "fusamuraichest": "Samuray Göğüslüğü",
        "fusamuraihead": "Samuray Miğferi",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Katana Ustalığı: +^green;15^reset;%\n"
    "^yellow;^reset; Kaçınma Teknolojileri: +^green;10^reset;%\n"
    "^yellow;^reset; Savunma Teknolojileri: +^green;10^reset;%",
)
add_set(
    {
        "fubonearmor2legs": "Kemik Çelik Baldırlık",
        "fubonearmor2chest": "Kemik Çelik Göğüslük",
        "fubonearmor2head": "Kemik Çelik Maske",
    },
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Düşme Hasarı x^green;0.75^reset;\n"
    "^yellow;^reset; Kılıçlar: Hasar x^green;1.15^reset;",
)
add_set(
    {
        "fureconpants": "Keşif Pantolonu",
        "fureconchest": "Keşif Yeleği",
        "fureconhead": "Keşif Başlığı",
    },
    "^orange;^orange;Set Bonusları^reset;: ^reset;\n"
    "^yellow;^reset; +^green;5^reset;% Hız\n"
    "^yellow;^reset; Taarruz/Keskin Nişancı Tüfeği: Hasar x^green;1.15^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Radyasyon Yanığı^reset;",
)


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
    for pattern in ("*.head", "*.chest", "*.legs", "*.back"):
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
    if len(selected) != 114:
        raise SystemExit(f"Beklenen 114 erken oyun zırh asseti yerine {len(selected)} bulundu")

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
                    "section": "v0.25 Kademe 1-2 aktif zırh setleri",
                }
            )

    ledger["translation_version"] = "0.25.0-beta"
    ledger["note"] = (
        "v0.25 Kademe 1-2 aktif zırh setleri: Zırh ve Silahlar araştırma ağacındaki "
        "bonegear, slimegear1, irongear, cottongear, telebriumgear, lunarigear, "
        "elduugear, skathgear ve tungstengear düğümlerinin açtığı, gerçek üretim tarifi "
        "bulunan 114 zırh parçasında 228 görünür alan yerelleştirildi. Toplam 4552 "
        "structured + 15 Lua, 1354 patch asset + 1 raw override. Oyun içi LQA bekliyor."
    )
    CATALOG.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"new_assets": len(selected), "new_fields": len(selected) * 2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
