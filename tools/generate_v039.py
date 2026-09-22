#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

ASSET = "interface/scripted/statWindow/statWindow.config"
SECTION = "v0.39 ana Tricorder ve durum arayüzü"
EXPECTED_FIELDS = 57
EXPECTED_UNIQUE = 56
# Reuse the approved field manifest, including bound QA metadata. Historical
# regeneration must not restore an obsolete second translation dictionary.
APPROVED_ROWS = json.loads(
    Path(__file__).with_name("v039_translations.json").read_text(encoding="utf-8")
)["translations"]
APPROVED = {(r["asset"], r["pointer"]): r for r in APPROVED_ROWS}
TRANSLATIONS = {r["en"]: r["tr"] for r in APPROVED_ROWS}


def translated_row(candidate):
    from copy import deepcopy
    approved = APPROVED.get((candidate.asset, candidate.pointer))
    if approved is None or approved["en"] != candidate.value:
        raise ValueError("v0.39 onaylı alan/kaynak uyuşmazlığı")
    return deepcopy(approved)


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
            translated_row(r)
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
