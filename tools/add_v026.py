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
    "titaniumgear",
    "carbonarmorgear",
    "wastelandgear",
    "protocitegear",
    "penumbritegear",
    "zerchesiumgear",
)

TR: dict[str, tuple[str, str]] = {}


def add_set(names: dict[str, str], description: str) -> None:
    for item_name, shortdescription in names.items():
        if item_name in TR:
            raise ValueError(f"Yinelenen zırh kimliği: {item_name}")
        TR[item_name] = (shortdescription, description)


BATTLEBORN_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Büyük Kılıç Ustalığı: +^green;15^reset;%\n"
    "^yellow;^reset; Siber/Çorak/Kavrulmuş: Can x^green;1.24^reset;, Hasar x^green;1.12^reset;, ^cyan;10^reset;% Fiziksel/Zehir Direnci\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Asit"
)
add_set(
    {
        "battlebornchest": "Savaşdoğan Göğüslük",
        "battlebornhead": "Savaşdoğan Miğfer",
        "battlebornpants": "Savaşdoğan Baldırlık",
    },
    BATTLEBORN_DESC,
)

TR.update(
    {
        "bmcglowscoutvisor": (
            "Işıklı Keşif Vizörü",
            "Bu modifiye karaborsa keşif vizörünün tümleşik ^green;ışık yayma^reset; özelliği, karanlık alanlarda görmeni sağlar.",
        ),
        "bmcjumpscoutvisor": (
            "Zıplama Keşif Vizörü",
            "Bu modifiye karaborsa keşif vizörünün tümleşik özelliği, ^green;daha yükseğe zıplamanı^reset; sağlar.",
        ),
        "bmcspeedscoutvisor": (
            "Hız Keşif Vizörü",
            "Bu modifiye karaborsa keşif başlığının tümleşik özelliği, ^green;daha hızlı koşmanı^reset; sağlar.",
        ),
    }
)

DAYWALKER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Enerji x^green;1.05^reset;\n"
    "^yellow;^reset; Tek Elli Kılıçlar: +^green;1.5^reset;% Kritik Şansı/+^green;25^reset;% Kritik Hasarı\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Balçık, Çamur, Buz, Kar, Katran\n"
    "^yellow;^reset; ^orange;Nightar/Tenebrhae Işık Cezalarını Azaltır^reset;"
)
add_set(
    {
        "daywalkerchest": "Gündüz Gezgini Göğüslüğü",
        "daywalkerhead": "Gündüz Gezgini Miğferi",
        "daywalkerpants": "Gündüz Gezgini Baldırlığı",
    },
    DAYWALKER_DESC,
)

EVA_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Orta Dereceli Radyasyon, Radyasyon Yanığı, İrin, Sıvı Azot"
)
add_set({"evachest": "E.V.A. Giysisi", "evapants": "E.V.A. Pantolonu"}, EVA_DESC)
TR["evahead"] = ("E.V.A. Miğferi", "^cyan;Kafa Lambası^reset;\n" + EVA_DESC)

SCOUT_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;200^reset; sn Oksijen\n"
    "^yellow;^reset; +^green;8^reset;% Enerji Yenilenmesi\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Gaz, Proto-Zehir"
)
add_set(
    {
        "ff_scoutchest": "Gözcü Göğüslüğü",
        "ff_scouthelm": "Gözcü Miğferi",
        "ff_scoutpants": "Gözcü Baldırlığı",
    },
    SCOUT_DESC,
)

BOUNTY_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Düşme Hasarı x^green;0.12^reset;\n"
    "^yellow;^reset; Alev Makinesi/Roketatar: Hasar x^green;1.2^reset;"
)
add_set(
    {
        "fubountyhunterchest": "Ödül Avcısı Göğüslüğü",
        "fubountyhunterpants": "Ödül Avcısı Pantolonu",
    },
    BOUNTY_DESC,
)
TR["fubountyhunterhead"] = (
    "Ödül Avcısı Miğferi",
    "^cyan;Bağışıklık^reset;: Caliginous Gazı\n" + BOUNTY_DESC,
)

NAUTILUS_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;175^reset; sn Hava, +^green;50^reset;% Nefes Yenilenmesi\n"
    "^yellow;^reset; Okyanuslar: Hasar x^green;1.15^reset;, +^green;5^reset;% Hız, +^green;3^reset;% Kritik Hasarı\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Asit, Zehirlenme, Gaz"
)
add_set(
    {"fudiverchest": "Nautilus Göğüslüğü", "fudiverlegs": "Nautilus Pantolonu"},
    NAUTILUS_DESC,
)
TR["fudiverhead"] = (
    "Nautilus Miğferi",
    "^cyan;Yüzme Takviyesi 1^reset;, ^cyan;Kafa Lambası 2^reset;\n" + NAUTILUS_DESC,
)

ASSAULT_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;20^reset;% Zıplama\n"
    "^yellow;^reset; Taarruz Tüfekleri, Enerji Silahları: Hasar x^green;1.2^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Oksijensizlik, Gaz, Orta Dereceli Soğuk, Sıvı Azot"
)
add_set(
    {
        "fuexplorerchest": "Taarruz Zırhı",
        "fuexplorerhead": "Taarruz Miğferi",
        "fuexplorerlegs": "Taarruz Baldırlığı",
    },
    ASSAULT_DESC,
)
TR["fuexplorerhead"] = (
    "Taarruz Miğferi",
    "^cyan;Kafa Lambası 3^reset;\n" + ASSAULT_DESC,
)

HOPLITE_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;20^reset;% Kalkan Yenilenmesi, +^green;10^reset;% Kalkan Darbesi/İtme Gücü\n"
    "^yellow;^reset; +^green;12^reset;% Geri Tepme Direnci\n"
    "^yellow;^reset; (Kısa) Mızraklar: +^green;3^reset;% Kritik Şansı\n"
    "^yellow;^reset; Dağlık^reset;: +^green;2.5^reset;% Kritik Şansı\n"
    "^yellow;^reset; ^cyan;Bağışıklık: Proto-Zehir^reset;"
)
add_set(
    {
        "fuhoplitechest": "Hoplit Göğüslüğü",
        "fuhoplitehead": "Hoplit Miğferi",
        "fuhoplitepants": "Hoplit Baldırlığı",
    },
    HOPLITE_DESC,
)

INTREPID_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;15^reset;% Geri Tepme Direnci^reset;\n"
    "^yellow;^reset; Ezici, Çekiç: +^green;2^reset;% Kritik Şansı, Hasar x^green;1.2^reset;\n"
    "^yellow;^reset; Dağlık: +^green;12^reset;% Geri Tepme Direnci"
)
add_set(
    {
        "fuintrepidchest": "Gözüpek Zırhı",
        "fuintrepidhead": "Gözüpek Kapüşonu",
        "fuintrepidpants": "Gözüpek Cübbesi",
    },
    INTREPID_DESC,
)

JUNKER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;200^reset; sn Oksijen, +^green;15^reset;% Enerji Yenilenmesi, -^green;10^reset;% Enerji Yenilenme Gecikmesi\n"
    "^yellow;^reset; +^green;450^reset;% Bomba Teknolojisi Hasarı\n"
    "^yellow;^reset; +^green;35^reset;% Atılma/Kaçınma Teknolojisi Hızı\n"
    "^yellow;^reset; +^green;15^reset;% Zıplama Teknolojisi Yüksekliği\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Asit, Gaz"
)
add_set(
    {
        "fujunkerchest": "Hurdacı Göğüslüğü",
        "fujunkerhead": "Hurdacı Miğferi",
        "fujunkerpants": "Hurdacı Baldırlığı",
    },
    JUNKER_DESC,
)
TR["fujunkerhead"] = ("Hurdacı Miğferi", "^cyan;Kafa Lambası 2^reset;\n" + JUNKER_DESC)

SLAYER_DESC = "^orange;Set Bonusları^reset;:\nYumruk/Balta: Hasar x^green;1.25^reset;"
TR.update(
    {
        "fumantizitier3chest": ("Cellat Eldivenleri", "^cyan;Dikenler^reset;\n" + SLAYER_DESC),
        "fumantizitier3head": ("Cellat Miğferi", SLAYER_DESC),
        "fumantizitier3pants": ("Cellat Çizmeleri", SLAYER_DESC),
    }
)

WANDERER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;2^reset;% Kritik Şansı\n"
    "^yellow;^reset; Enerji Silahları: Hasar x^green;1.15^reset; ve +^green;15^reset;% Kritik Hasarı"
)
add_set(
    {
        "fupioneerchest": "Gezgin Göğüs Koruması",
        "fupioneerhead": "Gezgin Miğferi",
    },
    WANDERER_DESC,
)
TR["fupioneerpants"] = (
    "Gezgin Pantolonu",
    "^cyan;Bağışıklık^reset;: Çamur Yavaşlatması\n" + WANDERER_DESC,
)

EVADER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;25^reset;% Kalkan Yenilenmesi, Dayanıklılık, Blok\n"
    "^yellow;^reset; Kalkan ve Kılıç: +^green;8^reset;% Fiziksel Direnç"
)
add_set(
    {
        "fuplatinumarmorchest": "Kaçınmacı Göğüslüğü",
        "fuplatinumarmorhead": "Kaçınmacı Miğferi",
        "fuplatinumarmorpants": "Kaçınmacı Baldırlığı",
    },
    EVADER_DESC,
)

GENDARME_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Roketatar/Bombaatar: Hasar x^green;1.2^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Yanma"
)
add_set(
    {
        "furustedchest": "Jandarma Göğüslüğü",
        "furustedhead": "Jandarma Miğferi",
        "furustedlegs": "Jandarma Baldırlığı",
    },
    GENDARME_DESC,
)

STEAMPUNK_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;5^reset;% Hız^reset;\n"
    "^yellow;^reset; Elektrik/Enerji Silahları: Hasar x^green;1.2^reset;, Enerji x^green;1.25^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Oksijensizlik, Yanma, Elektriklenme"
)
add_set(
    {
        "fusteampunkchest": "Steampunk Paltosu",
        "fusteampunkhead": "Steampunk Maskesi",
        "fusteampunklegs": "Steampunk Pantolonu",
    },
    STEAMPUNK_DESC,
)

CORSAIR_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;5^reset;% Zıplama, Hız\n"
    "^yellow;^reset; +^green;150^reset;% Bomba Teknolojisi Hasarı\n"
    "^yellow;^reset; +^green;100^reset; sn Oksijen\n"
    "^yellow;^reset; Taarruz Tüfekleri, (Makineli) Tabancalar: Hasar x^green;1.15^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: İrin, Kara Katran"
)
add_set(
    {
        "kirhostier3chest": "Korsan Göğüslüğü",
        "kirhostier3head": "Korsan Miğferi",
        "kirhostier3pants": "Korsan Pantolonu",
    },
    CORSAIR_DESC,
)

MASQUERADE_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;25^reset;% Enerji Yenilenmesi\n"
    "^yellow;^reset; Ezici: +^green;1^reset;% Kritik Şansı\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Gaz"
)
add_set(
    {
        "masqueradechest": "Maskeli Balo Göğüslüğü",
        "masqueradehead": "Maskeli Balo Miğferi",
        "masqueradepants": "Maskeli Balo Baldırlığı",
    },
    MASQUERADE_DESC,
)

MUTAVISK_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Düşme Hasarı x^green;0.75^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Tüm Radyasyon"
)
TR.update(
    {
        "mutaviskchest": ("Mutavisk Göğüslüğü", MUTAVISK_DESC),
        "mutavisklegs": ("Mutavisk Baldırlığı", MUTAVISK_DESC),
        "quiverback3": (
            "Üstün Sadak",
            "+^green;20^reset;% Hasar (Yaylar)\n"
            "+^green;20^reset;% Germe Hızı (Yaylar)\n"
            "+^green;8^reset;% Havada Hasar (Yaylar)\n"
            "-^green;4^reset; Atış Başına Enerji (Yaylar)",
        ),
        "quiverbackenergy": ("Enerji Sadağı", "-^green;6^reset; Atış Başına Enerji (Yaylar)"),
    }
)

SHIELDED_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; +^green;15^reset;% Hız\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Oksijensizlik, Gaz^reset;"
)
add_set(
    {
        "rustchest2": "Kalkanlı Göğüslük",
        "rusthead2": "Kalkanlı Miğfer",
        "rustlegs2": "Kalkanlı Bacak Zırhı",
    },
    SHIELDED_DESC,
)

NEISHIN_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Katana: Hasar x^green;1.15^reset;, +^green;3^reset;% Kritik Şansı, +^green;10^reset;% Kritik Hasarı^reset;\n"
    "^yellow;^reset; Katana + Hançer: Ek +^green;1^reset;% Kritik Şansı, Savunma x^green;1.14^reset;^reset;"
)
add_set(
    {
        "samurai2chest": "Neishin Göğüslüğü",
        "samurai2head": "Neishin Miğferi",
        "samurai2pants": "Neishin Baldırlığı",
    },
    NEISHIN_DESC,
)

SPACEFARER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Madencilik Lazeri: Savaş Hasarı x^green;2^reset;\n"
    "^yellow;^reset; +^green;350^reset; sn Oksijen\n"
    "^yellow;^reset; +^green;50^reset;% Savunma Teknolojisi Verimliliği\n"
    "^cyan;Bağışıklık^reset;: Yanma, Proto-Zehir, Gaz"
)
add_set(
    {
        "spacefarerchest": "Uzay Yolcusu Göğüslüğü",
        "spacefarerpants": "Uzay Yolcusu Baldırlığı",
    },
    SPACEFARER_DESC,
)
TR["spacefarerhead"] = (
    "Uzay Yolcusu Miğferi",
    "^cyan;Kafa Lambası^reset;\n" + SPACEFARER_DESC,
)

RESEARCHER_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Magnorb'lar: Hasar x^green;1.25^reset;\n"
    "^yellow;^reset; ^cyan;Bağışıklık^reset;: Oksijensizlik, Zehirlenme, Gaz\n"
    "^yellow;^reset; Araştırma Bonusu +^green;1^reset;"
)
add_set(
    {
        "tw_fieldresearchchest": "Araştırmacı Göğüslüğü",
        "tw_fieldresearchpants": "Araştırmacı Baldırlığı",
    },
    RESEARCHER_DESC,
)
for item_name in ("tw_fieldresearchhead", "tw_fieldresearchhead1", "tw_fieldresearchhead2"):
    TR[item_name] = (
        "Araştırmacı Miğferi",
        "^cyan;Kafa Lambası 2^reset;\n" + RESEARCHER_DESC,
    )

SPACEPUNK_DESC = (
    "^orange;Set Bonusları^reset;:\n"
    "^yellow;^reset; Oksijen x^green;30^reset;"
)
add_set(
    {"tw_spacepunkchest": "Spacepunk Paltosu", "tw_spacepunklegs": "Spacepunk Pantolonu"},
    SPACEPUNK_DESC,
)
TR["tw_spacepunkhead"] = (
    "Spacepunk Miğferi",
    "^cyan;Kafa Lambası^reset;\n" + SPACEPUNK_DESC,
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
    if len(selected) != 75:
        raise SystemExit(f"Beklenen 75 Kademe 3 zırh asseti yerine {len(selected)} bulundu")

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
                    "section": "v0.26 Kademe 3 aktif zırh setleri",
                }
            )

    ledger["translation_version"] = "0.26.0-beta"
    ledger["note"] = (
        "v0.26 Kademe 3 aktif zırh setleri: Zırh ve Silahlar araştırma ağacındaki "
        "titaniumgear, carbonarmorgear, wastelandgear, protocitegear, penumbritegear "
        "ve zerchesiumgear düğümlerinin açtığı, gerçek üretim tarifi bulunan 75 yeni "
        "zırh parçasında 150 görünür alan yerelleştirildi. Önceden çevrilmiş Mutavisk "
        "miğferi korundu. Toplam 4702 structured + 15 Lua, 1429 patch asset + 1 raw "
        "override. Oyun içi LQA bekliyor."
    )
    CATALOG.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"new_assets": len(selected), "new_fields": len(selected) * 2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
