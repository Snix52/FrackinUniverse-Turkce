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
    "advancealloygear",
    "durasteelgear",
    "irradiumgear",
    "triangliumgear",
    "prisilitegear",
    "quietusgear",
    "bioweaponsgear",
)

TR: dict[str, tuple[str, str]] = {}


def add_set(names: dict[str, str], description: str) -> None:
    for item_name, shortdescription in names.items():
        if item_name in TR:
            raise ValueError(f"Yinelenen zırh kimliği: {item_name}")
        TR[item_name] = (shortdescription, description)


TR.update(
    {
        "cutewings": ("Sevimli Kanatlar", "Parıldayan sevimli bir çift kanat."),
        "shadowbonecape": (
            "Girdap Pelerini",
            "Gölge enerjisine doymuş bir pelerin. +^green;15^reset;% zıplama yüksekliği.",
        ),
        "quiverbackpower": ("Güç Sadağı", "+^green;30^reset;% Hasar (Yaylar)"),
        "quiverback4": (
            "Muhteşem Sadak",
            "+^green;25^reset;% Hasar (Yaylar)\n"
            "+^green;25^reset;% Germe Hızı (Yaylar)\n"
            "+^green;12^reset;% Havada Hasar (Yaylar)\n"
            "-^green;7^reset; Atış Başına Enerji (Yaylar)",
        ),
        "quiverbackspeed": ("Hız Sadağı", "+^green;30^reset;% Germe Hızı (Yaylar)"),
    }
)

QUIETUS_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Quietus Silahları: Hasar x^green;1.3^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Yanma, Delilik"
)
add_set(
    {
        "quietuschest": "Korucu Plakası",
        "quietushead": "Korucu Miğferi",
        "quietuslegs": "Korucu Baldırlığı",
    },
    QUIETUS_DESC,
)

SAVAGE_BEAR_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;30^reset;% Geri Tepme Direnci\n"
    "^yellow;^reset; Baltalar, İki Elli Yakın Dövüş: +^green;4.5^reset;% Kritik Şansı, Hasar x^green;1.25^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Buz durum etkileri"
)
add_set(
    {
        "fubearchest2": "Vahşi Ayı Paltosu",
        "fubearhead2": "Vahşi Ayı Kapüşonu",
        "fubearlegs2": "Vahşi Ayı Baldırlığı",
    },
    SAVAGE_BEAR_DESC,
)

PUSTULE_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^#969600;Parıltı^reset;\n"
    "^yellow;^reset; ^cyan;Direnç^reset;: Zihinsel ^green;20^reset;%\n"
    "^yellow;^reset; Biyo/Kabarcık Silahları: +^green;4^reset;% Kritik Şansı ve Hasar x^green;1.15^reset;^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Zehirlenme, Proto-Zehir, İrin, Sıvı Azot"
)
add_set(
    {
        "blisterchestalt": "Püstül Plakası",
        "blisterhelmalt": "Püstül Miğferi",
        "blisterpantsalt": "Püstül Bacak Plakaları",
    },
    PUSTULE_DESC,
)

CELLULAR_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^#3c3c00;Parıltı^reset;\n"
    "^yellow;^reset; +^green;0.06^reset;% Can Yenilenmesi,\n"
    "^yellow;^reset; Biyo-Silah: Hasar x^green;1.2^reset;\n"
    "^yellow;^reset; Düşme Hasarı x^green;0.88^reset;"
)
add_set(
    {
        "cellulararmorchest": "Hücresel Göğüslük",
        "cellulararmorhead": "Hücresel Miğfer",
        "cellulararmorpants": "Hücresel Tayt",
    },
    CELLULAR_DESC,
)

FLESH_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Tırpan/Biyo-Silah: +^green;3^reset;% Kritik Şansı\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Delilik"
)
add_set(
    {
        "cultfleshchest": "Et Göğüslüğü",
        "cultfleshhead": "Et Miğferi",
        "cultfleshlegs": "Et Taytı",
    },
    FLESH_DESC,
)

ENFORCER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Taarruz Tüfeği/Pompalı Tüfek: Hasar x^green;1.2^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Sıvı Azot, Karanlık"
)
add_set(
    {
        "enforcerchest": "İnfazcı Göğüslüğü",
        "enforcerhead": "İnfazcı Miğferi",
        "enforcerpants": "İnfazcı Baldırlığı",
    },
    ENFORCER_DESC,
)

GEOLOGIST_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Madencilik Lazeri: Savaş Hasarı x^green;1.5^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Sıvı Azot, Zehirlenme, İrin\n"
    "^yellow;^reset; Araştırma Bonusu +^green;2^reset;"
)
add_set(
    {
        "fieldscientistchest": "Jeolog Paltosu",
        "fieldscientisthead": "Jeolog Parlak Gözlüğü",
        "fieldscientistlegs": "Jeolog Pantolonu",
    },
    GEOLOGIST_DESC,
)

TR["fuarmoredcultistback"] = (
    "Kıvranan Dokunaçlar",
    "Ne kadar da neşeliler... üstelik enerji ve kalkan yenilenmesini artırıyorlar!",
)
CULTIST_CHEST_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^cyan;Göz Küreleri Fırlatır^reset;\n"
    "^yellow;^reset; Aether/Işıksız/Gece Yarısı/Gölge Dünyaları: Hasar x^green;1.15^reset;, Can x^green;1.25^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Zehirlenme, Asit"
)
CULTIST_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^cyan;Göz Küreleri Fırlatır^reset;\n"
    "^yellow;^reset; Aether/Işıksız Dünyalar: Hasar x^green;1.15^reset;, Can x^green;1.25^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Zehirlenme, Asit"
)
TR["fuarmoredcultistchest"] = ("Yozlaşmış Zırh", CULTIST_CHEST_DESC)
TR["fuarmoredcultisthead"] = ("Yozlaşmış Kapüşon", CULTIST_DESC)
TR["fuarmoredcultistlegs"] = (
    "Yozlaşmış Bacak Zırhı",
    "^cyan;Bağışıklık^reset;: Çoğu arazi etkisi.\n" + CULTIST_DESC,
)

KRAKEN_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^cyan;Yüzme Takviyesi 2^reset;\n"
    "^yellow;^reset; Okyanus/Tidewater: +^green;4^reset;% Kritik Şansı, Hasar x^green;1.15^reset;, +^green;5^reset;% Hız\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Asit, Zehirlenme, Biyo-Balçık, Gaz, Oksijensizlik"
)
add_set(
    {"fudiverchest2": "Kraken Zırhı", "fudiverlegs2": "Kraken Taytı"},
    KRAKEN_DESC,
)
TR["fudiverhead2"] = ("Kraken Miğferi", "^cyan;Kafa Lambası 3^reset;\n" + KRAKEN_DESC)

GUARDIAN_BODY_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "+^green;25^reset;% Kalkan Yenilenmesi/Kalkan Dayanıklılığı^reset;, +^green;20^reset;% Kalkan Darbesi\n"
    "Topuz: Hasar x^green;1.15^reset;\n"
    "Kalkan: +^green;25^reset;% Geri Tepme Direnci"
)
GUARDIAN_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;25^reset;% Kalkan Yenilenmesi/Kalkan Dayanıklılığı^reset;, +^green;20^reset;% Kalkan Darbesi\n"
    "^yellow;^reset; Topuz: Hasar x^green;1.15^reset;\n"
    "^yellow;^reset; Kalkan: +^green;25^reset;% Geri Tepme Direnci"
)
TR["fuguardianchest"] = ("Muhafız Kabuğu", GUARDIAN_BODY_DESC)
add_set(
    {"fuguardianhead": "Muhafız Vizörü", "fuguardianpants": "Muhafız Baldırlığı"},
    GUARDIAN_DESC,
)

INFERNO_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^cyan;Darbe alınca Ateş Novası^reset;\n"
    "^yellow;^reset; Alev Makinesi: Hasar x^green;1.3^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Orta Dereceli Sıcak, Yanma"
)
add_set(
    {
        "fuinfernochest": "İnferno Göğüslüğü",
        "fuinfernohead": "İnferno Miğferi",
        "fuinfernopants": "İnferno Pantolonu",
    },
    INFERNO_DESC,
)

INVADER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^cyan;Yavaş Düşüş^reset;\n"
    "^yellow;^reset; Düşme Hasarı x^green;0.75^reset;\n"
    "^yellow;^reset; Magnorb'lar/Enerji: Hasar x^green;1.2^reset; ve +^green;5^reset;% Kritik Şansı\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Proto-Zehir"
)
add_set(
    {
        "fuinvaderchest": "İstilacı Zırhı",
        "fuinvaderhead": "İstilacı Vizörü",
        "fuinvaderpants": "İstilacı Baldırlığı",
    },
    INVADER_DESC,
)

PROTECTOR_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Darbe alınca ^cyan;15^reset;% ihtimalle +^green;5^reset;% Can kazanılır\n"
    "^yellow;^reset; Enerji x^green;1.05^reset;\n"
    "^yellow;^reset; Kesici Silahlar: +^green;4^reset;% Kritik Şansı"
)
add_set(
    {"fuprotectorchest": "Koruyucu Kaplama", "fuprotectorhead": "Koruyucu Maske"},
    PROTECTOR_DESC,
)
TR["fuprotectorpants"] = (
    "Koruyucu Cübbe",
    "^cyan;Bağışıklık^reset;: Buzda Kayma, Çamur\n" + PROTECTOR_DESC,
)

RAVAGER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;20^reset;% Kritik Hasarı, Can x^green;1.05^reset;\n"
    "^yellow;^reset; Keskin Nişancı Tüfeği: Hasar x^green;1.25^reset;"
)
add_set(
    {
        "furavagerchest": "Tahripçi Kabuğu",
        "furavagerhead": "Tahripçi Miğferi",
        "furavagerpants": "Tahripçi Cübbesi",
    },
    RAVAGER_DESC,
)

STAR_KILLER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Güneş Işığı: Güç/Savunma/Enerji/Can x^green;1.25^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Basınç, Çamur, Balçık Yapışması, Buzda Kayma, Karda Yavaşlama, Oksijensizlik"
)
add_set(
    {"fustarkillerchest": "Yıldız Katili Plakası", "fustarkillerpants": "Yıldız Katili Cübbesi"},
    STAR_KILLER_DESC,
)
TR["fustarkillerhead"] = (
    "Yıldız Katili Maskesi",
    "^cyan;Kafa Lambası 2^reset;\n" + STAR_KILLER_DESC,
)

GRAPHENE_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Enerji Silahları: Hasar x^green;1.25^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Sersemletme, Elektriklenme"
)
add_set(
    {
        "graphenechest": "Grafen Ceketi",
        "graphenehead": "Grafen Miğferi",
        "graphenelegs": "Grafen Taytı",
    },
    GRAPHENE_DESC,
)

HUNTER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Enerji x^green;1.1^reset;\n"
    "^yellow;^reset; Roketatar/Bombaatar: Hasar x^green;1.2^reset;, +^green;6^reset;% Kritik Hasarı"
)
add_set(
    {
        "wastelandchest2": "Avcı Göğüslüğü",
        "wastelandhead2": "Avcı Maskesi",
        "wastelandlegs2": "Avcı Pantolonu",
    },
    HUNTER_DESC,
)

INTERSEC_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Taarruz Tüfeği, Tabanca: +^green;2^reset;% Kritik Şansı, +^green;25^reset;% Kritik Hasarı"
)
add_set(
    {
        "kirhostier4chest": "Intersec Göğüslüğü",
        "kirhostier4head": "Intersec Miğferi",
        "kirhostier4pants": "Intersec Baldırlığı",
    },
    INTERSEC_DESC,
)

IRRADIUM_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Irradium Silahları: +^green;3^reset;% Kritik Şansı, +^green;10^reset;% Radyasyon Direnci\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Tüm Radyasyon"
)
add_set(
    {
        "irradiumchest": "Irradium Göğüslüğü",
        "irradiumhelm": "Irradium Miğferi",
        "irradiumlegs": "Irradium Baldırlığı",
    },
    IRRADIUM_DESC,
)

MAVERICK_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;15^reset;% Hız, +^green;15^reset;% Zıplama\n"
    "^yellow;^reset; Kol Topu: Hasar x^green;1.15^reset;"
)
add_set(
    {
        "maverickhunterchest": "Maverick Avcısı Göğüslüğü",
        "maverickhunterhead": "Maverick Göz İmplantları",
        "maverickhunterpants": "Maverick Avcısı Taytı",
    },
    MAVERICK_DESC,
)

PRIMUS_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Yumruklar: Hasar x^green;1.15^reset;, +^green;3^reset;% Kritik Şansı\n"
    "^yellow;^reset; +^green;50^reset;% Geri Tepme Direnci"
)
add_set(
    {
        "fumantizitier4chest": "Primus Zırhı",
        "fumantizitier4head": "Primus Miğferi",
        "fumantizitier4pants": "Primus Eteği",
    },
    PRIMUS_DESC,
)

WARRIOR_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Can ve Hız x^green;1.1^reset;\n"
    "^yellow;^reset; Yakın Dövüş: Hasar x^green;1.1^reset;"
)
add_set(
    {
        "ff_scoutchest_melee": "Savaşçı Göğüslüğü",
        "ff_scouthelm_melee": "Savaşçı Miğferi",
        "ff_scoutpants_melee": "Savaşçı Baldırlığı",
    },
    WARRIOR_DESC,
)

SHADOW_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;10^reset;% Hız\n"
    "^yellow;^reset; Balta/Çekiç/Tırpan: Hasar x^green;1.3^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Gölge Lekesi"
)
add_set(
    {
        "shadowbonearmorchest": "Gölge Göğüslüğü",
        "shadowbonearmorhead": "Gölge Miğferi",
        "shadowbonearmorpants": "Gölge Baldırlığı",
    },
    SHADOW_DESC,
)

SPACEFARER_MK2_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^cyan;Yerçekimi Normalleştirmesi^reset;\n"
    "^yellow;^reset; Madencilik Lazeri: Savaş Hasarı x^green;2.4^reset;\n"
    "^yellow;^reset; +^cyan;50^reset;% Savunma Teknolojisi Verimliliği\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Yanma, Proto-Zehir, Basınç, Gaz, Buzda Kayma, Oksijensizlik"
)
add_set(
    {
        "spacefarerchestadv": "Uzay Yolcusu Mk. 2 Göğüslüğü",
        "spacefarerpantsadv": "Uzay Yolcusu Mk. 2 Baldırlığı",
    },
    SPACEFARER_MK2_DESC,
)
TR["spacefarerheadadv"] = (
    "Uzay Yolcusu Mk. 2 Miğferi",
    "^cyan;Kafa Lambası 2^reset;\n" + SPACEFARER_MK2_DESC,
)

SURVIVOR_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; -^green;50^reset;% Açlık Tüketim Hızı\n"
    "^yellow;^reset; Bombaatar/Roketatar, Yay/Arbalet: +^green;6^reset;% Kritik Hasarı, Hasar x^green;1.2^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Gaz, Zehirlenme, Proto-Zehir"
)
add_set(
    {
        "wastelandchest": "Hayatta Kalan Göğüslüğü",
        "wastelandhead": "Hayatta Kalan Maskesi",
        "wastelandlegs": "Hayatta Kalan Pantolonu",
    },
    SURVIVOR_DESC,
)

X10_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Düşme Hasarı x^green;0.7^reset;\n"
    "^yellow;^reset; Taarruz/Enerji Tüfeği: Hasar x^green;1.2^reset; ve +^green;2^reset;% Kritik Şansı\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Oksijensizlik, Gaz, Orta Dereceli Soğuk, Sıvı Azot"
)
add_set(
    {"xenochest": "X10 Güç Zırhı", "xenolegs": "X10 Güç Bacak Zırhı"},
    X10_DESC,
)
TR["xenohead"] = ("X10 Güç Miğferi", "^cyan;Kafa Lambası^reset;\n" + X10_DESC)

CUTE_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Sevimli Silahlar: Hasar x^green;1.2^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Gölge Lekesi"
)
add_set(
    {"cutechest": "Sevimli Bluz", "cutehead": "Sevimli Kurdele", "cutelegs": "Sevimli Tayt"},
    CUTE_DESC,
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
    if len(selected) != 87:
        raise SystemExit(f"Beklenen 87 Kademe 4 zırh asseti yerine {len(selected)} bulundu")

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
                    "section": "v0.27 Kademe 4 aktif zırh setleri",
                }
            )

    ledger["translation_version"] = "0.27.0-beta"
    ledger["note"] = (
        "v0.27 Kademe 4 aktif zırh setleri: Zırh ve Silahlar araştırma ağacındaki "
        "advancealloygear, durasteelgear, irradiumgear, triangliumgear, prisilitegear, "
        "quietusgear ve bioweaponsgear düğümlerinin açtığı, gerçek üretim tarifi bulunan "
        "87 yeni zırh parçasında 174 görünür alan yerelleştirildi. Toplam 4876 structured "
        "+ 15 Lua, 1516 patch asset + 1 raw override. Oyun içi LQA bekliyor."
    )
    CATALOG.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"new_assets": len(selected), "new_fields": len(selected) * 2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
