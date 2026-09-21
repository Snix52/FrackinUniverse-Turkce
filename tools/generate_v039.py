#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

ASSET = "interface/scripted/statWindow/statWindow.config"
SECTION = "v0.39 ana Tricorder ve durum arayüzü"
EXPECTED_FIELDS = 57
EXPECTED_UNIQUE = 56
TRANSLATIONS = json.loads(r'''{"Research":"Araştırma","GPS":"GPS","Codex":"Codex","Tech Equip":"Tech Donanımı","Tech Craft":"Tech Üretimi","Mech Gear":"Mech Donanımı","Mech Fuel":"Mech Yakıtı","Upgrade":"Yükselt","Adv. Stats":"Gelişmiş İstat.","Immunities":"Bağışıklıklar"," ^#bbbbbb;Accesses Stats, Research, Mechs and more.":" ^#bbbbbb;İstatistik, Araştırma, Mech ve daha fazlasına erişim."," ^#00eaff;Personal Tricorder^reset;":" ^#00eaff;Kişisel Tricorder^reset;"," ^#ffffff;Resistances^reset;":" ^#ffffff;Dirençler^reset;","^#E33FFF;Aether":"^#E33FFF;Aether","^#ffae00;Bee Sting":"^#ffae00;Arı Sokması","^#4BF3FD;Moderate Cold":"^#4BF3FD;Orta Dereceli Soğuk","^#4BF3FD;Lightning":"^#4BF3FD;Yıldırım","^#FDBE4B;Moderate Heat":"^#FDBE4B;Orta Dereceli Sıcaklık","^yellow;Moderate Radiation":"^yellow;Orta Dereceli Radyasyon","^#78f04f;Bio-Ooze":"^#78f04f;Biyo-Balçık","^#5B6177;Black Tar":"^#5B6177;Kara Katran","Breath":"Oksijensizlik","^#EA907E;Darkness":"^#EA907E;Karanlık","^#FFE149;Shock":"^#FFE149;Elektrik Şoku","^gray;Pressure":"^gray;Basınç","^#4BF3FD;Extreme Cold":"^#4BF3FD;Aşırı Soğuk","^#FDBE4B;Extreme Heat":"^#FDBE4B;Aşırı Sıcak","^yellow;Extreme Radiation":"^yellow;Aşırı Radyasyon","^#FDBE4B;Burning":"^#FDBE4B;Yanma","^green;Jungle [Tile]":"^green;Cangıl [Zemin]","^brown;Mud [Tile]":"^brown;Çamur [Zemin]","^#D1E160;Gas":"^#D1E160;Gaz","^gray;Gravity Rain":"^gray;Yerçekimi Yağmuru","^#FFEC84;Honey Slow":"^#FFEC84;Bal Yavaşlatması","^#4BF3FD;Freeze":"^#4BF3FD;Donma","^#4BF3FD;Ice [Tile]":"^#4BF3FD;Buz [Zemin]","^#EA907E;Insanity":"^#EA907E;Delilik","^#C83E14;Lava":"^#C83E14;Lav","^#4BF3FD;Liquid Nitrogen":"^#4BF3FD;Sıvı Azot","^#4BF3FD;Nitrogen Freeze":"^#4BF3FD;Azot Donması","^#D1E160;Poisoning":"^#D1E160;Zehirlenme","^#78f04f;Proto-Poison":"^#78f04f;Proto-Zehir","^yellow;Pus":"^yellow;İrin","^yellow;Quick Sand":"^yellow;Batak Kum","^yellow;Radiation Burn":"^yellow;Radyasyon Yanığı","^orange;Sandstorm":"^orange;Kum Fırtınası","^#3F2E4D;Shadow Taint":"^#3F2E4D;Gölge Lekesi","^#61D13F;Slow (Slime)":"^#61D13F;Yavaşlama (Balçık)","^#61D13F;Slimed":"^#61D13F;Balçığa Bulanma","^#61D13F;Sticky Slime":"^#61D13F;Yapışkan Balçık","^#4BF3FD;Slush [Tile]":"^#4BF3FD;Sulu Kar [Zemin]","^#4BF3FD;Snow [Tile]":"^#4BF3FD;Kar [Zemin]","^gray;Stun":"^gray;Sersemletme","^#ffd800;Sulph. Acid":"^#ffd800;Sülfürik Asit","^#5B6177;Tar":"^#5B6177;Katran","^blue;Drowning":"^blue;Boğulma"}''')

def remaining_rows(source: Path):
    translated, _ = audit.load_translations(Path(__file__).with_name("ceviriler.json"))
    data = audit.parse_jsonc((source / ASSET).read_text(encoding="utf-8-sig"))
    return sorted([
        r for r in audit.candidates_from_data(ASSET, data)
        if r.confidence == "confirmed" and (r.asset, r.pointer) not in translated
    ], key=lambda r: r.pointer)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()
    rows = remaining_rows(args.source)
    if len(rows) != EXPECTED_FIELDS:
        raise ValueError(f"v0.39 alan sayısı değişti: {len(rows)} != {EXPECTED_FIELDS}")
    sources = {r.value for r in rows}
    if len(sources) != EXPECTED_UNIQUE:
        raise ValueError(f"v0.39 kaynak metin sayısı değişti: {len(sources)} != {EXPECTED_UNIQUE}")
    missing = sorted(sources - TRANSLATIONS.keys())
    if missing:
        raise ValueError(f"v0.39 eksik çeviri: {missing!r}")
    cp = Path(__file__).with_name("ceviriler.json")
    c = json.loads(cp.read_text(encoding="utf-8"))
    m = {
        "schema_version": 1,
        "translation_version": "0.39.0-beta",
        "scope": "Ana Kişisel Tricorder penceresinin 13 sabit UI metni ve runtime bağışıklık listesindeki 44 durum adı; teknik alanlar korunur.",
        "translations": [
            {"asset":r.asset,"pointer":r.pointer,"en":r.value,"tr":TRANSLATIONS[r.value],"section":SECTION}
            for r in rows
        ]
    }
    Path(__file__).with_name("v039_translations.json").write_text(
        json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    idx = {(r["asset"],r["pointer"]) for r in c["translations"]}
    for r in m["translations"]:
        k = (r["asset"],r["pointer"])
        if k in idx:
            raise ValueError(f"v0.39 alanı zaten katalogda: {k}")
        c["translations"].append(r)
        idx.add(k)
    c["translation_version"] = m["translation_version"]
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"v0.39: {len(rows)} alan / {len(sources)} benzersiz metin")

if __name__ == "__main__":
    main()
