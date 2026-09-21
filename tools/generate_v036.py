#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import audit_remaining as audit

ASSET = "interface/shipnameplate/fu_shipnameplate.config"
SECTION = "v0.36 gemi isim plakası arayüzü"
EXPECTED_FIELDS = 36
EXPECTED_UNIQUE = 36
TRANSLATIONS = json.loads(r'''{" Ship Commemoration Plaque":" Gemi Hatıra Plaketi"," Configuration":" Ayarlar","Accept":"Kabul Et","Ship Name:":"Gemi Adı:","Ship Type:":"Gemi Türü:","Name":"Ad","Cruiser":"Kruvazör","Freighter":"Yük Gemisi","Escort":"Refakat Gemisi","Starship":"Yıldız Gemisi","Battleship":"Savaş Gemisi","Peacekeeper":"Barış Gücü Gemisi","Science":"Bilim Gemisi","Medical":"Hastane Gemisi","Patrol":"Devriye Gemisi","Recon":"Keşif Gemisi","Stealth":"Gizli Operasyon Gemisi","Explorer":"Kâşif Gemisi","Colony":"Koloni Gemisi","Transport":"Nakliye Gemisi","Courier":"Kurye Gemisi","Fighter":"Avcı","Destroyer":"Muhrip","Dreadnought":"Dretnot","Flagship":"Amiral Gemisi","Carrier":"Taşıyıcı Gemi","Repair":"Onarım Gemisi","Utility":"Hizmet Gemisi","Envoy":"Elçi Gemisi","Shuttle":"Mekik","Pirate":"Korsan Gemisi","Raider":"Akıncı Gemisi","Experimental":"Deneysel Gemi","Special":"Özel Amaçlı Gemi","Derelict":"Terk Edilmiş Gemi","Unknown":"Bilinmiyor"}''')

def remaining_rows(source: Path):
    translated, _ = audit.load_translations(Path(__file__).with_name("ceviriler.json"))
    data = audit.parse_jsonc((source / ASSET).read_text(encoding="utf-8-sig"))
    return sorted([
        row for row in audit.candidates_from_data(ASSET, data)
        if row.confidence == "confirmed"
        and (row.asset, row.pointer) not in translated
    ], key=lambda r: r.pointer)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()
    rows = remaining_rows(args.source)
    if len(rows) != EXPECTED_FIELDS:
        raise ValueError(f"v0.36 alan sayısı değişti: {len(rows)} != {EXPECTED_FIELDS}")
    sources = {r.value for r in rows}
    if len(sources) != EXPECTED_UNIQUE:
        raise ValueError(f"v0.36 kaynak metin sayısı değişti: {len(sources)} != {EXPECTED_UNIQUE}")
    missing = sorted(sources - TRANSLATIONS.keys())
    if missing:
        raise ValueError(f"v0.36 eksik çeviri: {missing!r}")

    catalog_path = Path(__file__).with_name("ceviriler.json")
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    manifest = {
        "schema_version": 1,
        "translation_version": "0.36.0-beta",
        "scope": "Aktif gemi isim plakası arayüzü: pencere başlığı/alt başlığı, kabul düğmesi, gemi adı/türü etiketleri, ad giriş ipucu ve 30 canlı gemi türü. Runtime şablon değerleri lblType=Cruiser ile lblDate=%stardate% ve teknik callback/path/script alanları korunur.",
        "translations": [
            {"asset": r.asset, "pointer": r.pointer, "en": r.value, "tr": TRANSLATIONS[r.value], "section": SECTION}
            for r in rows
        ],
    }
    Path(__file__).with_name("v036_translations.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
    for row in manifest["translations"]:
        key = (row["asset"], row["pointer"])
        if key in index:
            raise ValueError(f"v0.36 alanı zaten katalogda: {key}")
        catalog["translations"].append(row)
        index[key] = row
    catalog["translation_version"] = manifest["translation_version"]
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"v0.36: {len(rows)} alan / {len(sources)} benzersiz metin")
    print(f"katalog: {len(catalog['translations'])} structured alan")

if __name__ == "__main__":
    main()
