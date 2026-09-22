#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

TOOLS = Path(__file__).resolve().parent
MANIFEST = TOOLS / "v041_translations.json"
CATALOG = TOOLS / "ceviriler.json"
ASSETS = {
    "interface/scripted/spaceStation/spaceStation.config": 14,
    "interface/scripted/spaceStation/texts.config": 183,
    "interface/scripted/spaceStation/spaceStationData.config": 48,
}
EXCLUDED = {
    ("interface/scripted/spaceStation/texts.config", "/generic/chat4"),
    ("interface/scripted/spaceStation/texts.config", "/generic/chat5"),
    ("interface/scripted/spaceStation/texts.config", "/defaultButtonStates/0"),
    ("interface/scripted/spaceStation/texts.config", "/defaultButtonStates/2"),
    ("interface/scripted/spaceStation/texts.config", "/defaultButtonStates/3"),
    ("interface/scripted/spaceStation/texts.config", "/defaultButtonStates/4"),
    ("interface/scripted/spaceStation/texts.config", "/defaultButtonStates/5"),
}

def value_at(data, pointer):
    cur = data
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = manifest["translations"]
    if manifest["translation_version"] != "0.41.0-beta":
        raise ValueError("v0.41 sürüm bilgisi bozuk")
    if len(rows) != 245:
        raise ValueError(f"v0.41 alan sayısı değişti: {len(rows)} != 245")
    if len({(r["asset"], r["pointer"]) for r in rows}) != 250:
        raise ValueError("v0.41 manifestinde yinelenen alan var")

    parsed = {
        asset: audit.parse_jsonc((args.source / asset).read_text(encoding="utf-8-sig"))
        for asset in ASSETS
    }
    counts = {}
    for row in rows:
        asset, pointer = row["asset"], row["pointer"]
        if asset not in ASSETS:
            raise ValueError("v0.41 kapsam dışı asset: " + asset)
        if (asset, pointer) in EXCLUDED or "/quests/" in pointer:
            raise ValueError("v0.41 erişilemeyen/manuel inceleme alanı: " + asset + pointer)
        if value_at(parsed[asset], pointer) != row["en"]:
            raise ValueError("v0.41 kaynak uyuşmazlığı: " + asset + pointer)
        counts[asset] = counts.get(asset, 0) + 1
    if counts != ASSETS:
        raise ValueError(f"v0.41 asset dağılımı değişti: {counts!r}")

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
    for row in rows:
        key = (row["asset"], row["pointer"])
        if key not in index or index[key]["tr"] != row["tr"]:
            raise ValueError("v0.41 katalog eşleşmesi eksik: " + row["asset"] + row["pointer"])
    if catalog["translation_version"] != "0.41.0-beta":
        raise ValueError("Ana katalog v0.41 değil")

    print(json.dumps({"fields": len(rows), "assets": counts}, ensure_ascii=False))

if __name__ == "__main__":
    main()
