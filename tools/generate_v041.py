#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

TOOLS = Path(__file__).resolve().parent
MANIFEST = TOOLS / "v041_translations.json"
CATALOG = TOOLS / "ceviriler.json"
CONFIG = "interface/scripted/spaceStation/spaceStation.config"
TEXTS = "interface/scripted/spaceStation/texts.config"
DATA = "interface/scripted/spaceStation/spaceStationData.config"
ASSETS = {
    CONFIG: 14,
    TEXTS: 212,
    DATA: 48,
}
EXCLUDED = {
    (TEXTS, "/generic/chat4"),
    (TEXTS, "/generic/chat5"),
}
TEXT_TECHNICAL_KEYS = {
    "portraitPath", "talkTotalFrames", "talkTicksPerFrame",
    "blinkTotalFrames", "blinkTicksPerFrame", "blinkCooldownAvg",
    "sound", "volume", "cutoffSound", "chatCount", "cantAffordCount",
    "cooldownEnhancer",
}
LIVE_RACES = ("generic", "apex", "avian", "floran", "glitch", "human", "hylotl", "cari", "novakid")
BUTTON_INDEXES = (0, 2, 3, 4, 5)

def value_at(data, pointer):
    cur = data
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur

def expected_text_pointers(texts):
    pointers = {f"/defaultButtonStates/{i}" for i in BUTTON_INDEXES}
    for race in LIVE_RACES:
        block = texts.get(race)
        if not isinstance(block, dict):
            raise ValueError("v0.41 race block kayıp: " + race)
        for key, value in block.items():
            if not isinstance(value, str):
                continue
            if key in TEXT_TECHNICAL_KEYS or key.startswith("quest"):
                continue
            if race == "generic" and key in {"chat4", "chat5"}:
                continue
            pointers.add(f"/{race}/{key}")
    return pointers

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = manifest["translations"]
    if manifest["translation_version"] != "0.41.0-beta":
        raise ValueError("v0.41 sürüm bilgisi bozuk")
    if len(rows) != 274:
        raise ValueError(f"v0.41 alan sayısı değişti: {len(rows)} != 274")
    if len({(r["asset"], r["pointer"]) for r in rows}) != 274:
        raise ValueError("v0.41 manifestinde yinelenen alan var")

    parsed = {
        asset: audit.parse_jsonc((args.source / asset).read_text(encoding="utf-8-sig"))
        for asset in ASSETS
    }

    manifest_text_pointers = {r["pointer"] for r in rows if r["asset"] == TEXTS}
    runtime_text_pointers = expected_text_pointers(parsed[TEXTS])
    if manifest_text_pointers != runtime_text_pointers:
        missing = sorted(runtime_text_pointers - manifest_text_pointers)
        extra = sorted(manifest_text_pointers - runtime_text_pointers)
        raise ValueError(f"v0.41 texts runtime kapsamı değişti: missing={missing!r} extra={extra!r}")

    counts = {}
    for row in rows:
        asset, pointer = row["asset"], row["pointer"]
        if asset not in ASSETS:
            raise ValueError("v0.41 kapsam dışı asset: " + asset)
        if (asset, pointer) in EXCLUDED or (asset == TEXTS and ("/quest" in pointer or pointer.endswith("/cooldownEnhancer"))):
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
