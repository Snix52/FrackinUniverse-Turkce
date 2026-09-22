#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
import audit_remaining as audit

TOOLS = Path(__file__).resolve().parent
MANIFEST = TOOLS / "v046_translations.json"
CATALOG = TOOLS / "ceviriler.json"
CORE = ['species/apex.species', 'species/avian.species', 'species/elduukhar.species', 'species/fenerox.species', 'species/floran.species', 'species/fukirhos.species', 'species/fumantizi.species', 'species/fupeglaci.species', 'species/glitch.species', 'species/human.species', 'species/hylotl.species', 'species/juux.species', 'species/nightar.species', 'species/novakid.species', 'species/radien.species', 'species/shadow.species', 'species/skath.species', 'species/slimeperson.species', 'species/thelusian.species', 'species/veluu.species']

def value_at(data, pointer):
    cur = data
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur

def patch_value(ops, pointer):
    found = None
    for op in ops:
        if not isinstance(op, dict):
            continue
        path = str(op.get("path", ""))
        if path == pointer and "value" in op:
            found = op["value"]
            continue
        if path and pointer.startswith(path + "/") and "value" in op:
            try:
                found = value_at(op["value"], pointer[len(path):])
            except (KeyError, IndexError, TypeError, ValueError):
                pass
    return found

def version_tuple(value):
    return tuple(map(int, value.split("-", 1)[0].split(".")))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = m["translations"]
    if m["translation_version"] != "0.46.0-beta":
        raise ValueError("v0.46 sürüm bilgisi bozuk")
    if len(rows) != 129 or len({(r["asset"], r["pointer"]) for r in rows}) != 129:
        raise ValueError("v0.46 alan kapsamı bozuk")
    if len({r["asset"] for r in rows}) != 53 or len({r["en"] for r in rows}) != 127:
        raise ValueError("v0.46 asset/kaynak kapsamı bozuk")
    if sum(r["asset"].startswith("ai/") for r in rows) != 89:
        raise ValueError("v0.46 SAIL/AI alan sayısı bozuk")
    species = [r for r in rows if r["asset"].startswith("species/")]
    if len(species) != 40 or {r["asset"] for r in species} != set(CORE):
        raise ValueError("v0.46 çekirdek ırk kapsamı bozuk")
    if set(CORE) != set(audit.AUDIT_CORE_PLAYABLE_SPECIES_ASSETS):
        raise ValueError("v0.46 audit çekirdek ırk listesi bozuk")

    cache = {}
    for row in rows:
        qa = row.get("qa", {})
        asset = row["asset"]
        pointer = row["pointer"]
        if qa.get("layered_source"):
            src = qa.get("source_patch")
            if not src or not src.endswith(".patch"):
                raise ValueError("v0.46 layered source eksik: " + asset + pointer)
            if src not in cache:
                path = args.source / src
                if not path.is_file():
                    raise FileNotFoundError(path)
                cache[src] = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
            actual = patch_value(cache[src], pointer)
        else:
            if asset not in cache:
                path = args.source / asset
                if not path.is_file():
                    raise FileNotFoundError(path)
                cache[asset] = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
            actual = value_at(cache[asset], pointer)
        if actual != row["en"]:
            raise ValueError("v0.46 pinned kaynak uyuşmazlığı: " + asset + pointer)

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if version_tuple(catalog["translation_version"]) < (0, 46, 0):
        raise ValueError("Ana katalog v0.46 öncesinde")
    idx = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
    for row in rows:
        got = idx.get((row["asset"], row["pointer"]))
        if not got or got["en"] != row["en"] or got["tr"] != row["tr"]:
            raise ValueError("v0.46 katalog eşleşmesi eksik: " + row["asset"] + row["pointer"])
    print(json.dumps({
        "fields": 129,
        "assets": 53,
        "unique_source": 127,
        "ai_fields": 89,
        "species_fields": 40,
        "source_documents": len(cache),
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
