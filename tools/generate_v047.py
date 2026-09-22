#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit
from write_build_evidence import verify_source

MANIFEST = TOOLS / "v047_translations.json"
CATALOG = TOOLS / "ceviriler.json"
EXPECTED_FIELDS = 170
EXPECTED_ASSETS = 66
EXPECTED_UNIQUE = 110
ALLOWED_POINTERS = {"/description", "/shortdescription", "/floranDescription", "/glitchDescription"}

def version_tuple(value):
    return tuple(map(int, value.split("-", 1)[0].split(".")))

def read_at(root, pointer):
    cur = root
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()
    verify_source(args.source)

    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = m["translations"]
    if m["translation_version"] != "0.47.0-beta":
        raise ValueError("v0.47 manifest version drift")
    if len(rows) != EXPECTED_FIELDS:
        raise ValueError(f"v0.47 field drift: {len(rows)}")
    if len({(r["asset"], r["pointer"]) for r in rows}) != EXPECTED_FIELDS:
        raise ValueError("v0.47 duplicate field")
    if len({r["asset"] for r in rows}) != EXPECTED_ASSETS:
        raise ValueError("v0.47 asset drift")
    if len({r["en"] for r in rows}) != EXPECTED_UNIQUE:
        raise ValueError("v0.47 source drift")
    if any(not r["asset"].startswith("plants/") for r in rows):
        raise ValueError("v0.47 non-plant asset")
    if {r["pointer"] for r in rows} - ALLOWED_POINTERS:
        raise ValueError("v0.47 pointer drift")
    if "/description" not in audit.AUDIT_EXCLUDED_FIELDS.get("liquids/", frozenset()):
        raise ValueError("liquid description audit exclusion missing")

    cache = {}
    for r in rows:
        path = args.source / r["asset"]
        if not path.is_file():
            raise FileNotFoundError(path)
        if r["asset"] not in cache:
            cache[r["asset"]] = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
        if read_at(cache[r["asset"]], r["pointer"]) != r["en"]:
            raise ValueError("v0.47 pinned source mismatch: " + r["asset"] + r["pointer"])

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if version_tuple(catalog["translation_version"]) < (0, 47, 0):
        raise ValueError("catalog version behind v0.47")
    idx = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
    for r in rows:
        cur = idx.get((r["asset"], r["pointer"]))
        if not cur or cur["en"] != r["en"] or cur["tr"] != r["tr"]:
            raise ValueError("v0.47 catalog mismatch: " + r["asset"] + r["pointer"])

    print(f"v0.47 source gate PASS: {len(rows)} alan / {len({r['asset'] for r in rows})} asset / {len({r['en'] for r in rows})} kaynak")

if __name__ == "__main__":
    main()
