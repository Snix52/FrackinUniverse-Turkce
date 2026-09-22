#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

TOOLS=Path(__file__).resolve().parent
MANIFEST=TOOLS/"v042_translations.json"
CATALOG=TOOLS/"ceviriler.json"
EXPECTED_ASSETS={
    "interface/objectcrafting/fu_pethouse/fu_pethouse.config": 16,
    "interface/objectcrafting/fu_pethouse/fu_pethouse_confirmation.config": 5,
    "interface/windowconfig/armory.config": 4,
    "interface/windowconfig/beestation.config": 4,
    "interface/windowconfig/boozekit.config": 4,
    "interface/windowconfig/chemlab.config": 4,
    "interface/windowconfig/clothingfabricator.config": 4,
    "interface/windowconfig/coffee.config": 4,
    "interface/windowconfig/crafting.config": 8,
    "interface/windowconfig/craftingcrewshop.config": 6,
    "interface/windowconfig/craftingeasel.config": 8,
    "interface/windowconfig/craftingesoteric.config": 8,
    "interface/windowconfig/craftingold.config": 8,
    "interface/windowconfig/craftingslimecentrifuge.config": 6,
    "interface/windowconfig/crystalloom.config": 4,
    "interface/windowconfig/designlab.config": 4,
    "interface/windowconfig/distill.config": 4,
    "interface/windowconfig/ferment.config": 4,
    "interface/windowconfig/fissionfurnace.config": 6,
    "interface/windowconfig/fruitpressnew.config": 4,
    "interface/windowconfig/fu_anvil.config": 4,
    "interface/windowconfig/fuburgerfool.config": 6,
    "interface/windowconfig/fufoodshopfloran.config": 6,
    "interface/windowconfig/fufoodstore.config": 6,
    "interface/windowconfig/fugemshop.config": 6,
    "interface/windowconfig/fupetshop.config": 6,
    "interface/windowconfig/furniturestation.config": 6,
    "interface/windowconfig/fushadowstore.config": 6,
    "interface/windowconfig/fustarbucks.config": 6,
    "interface/windowconfig/gemstation.config": 6,
    "interface/windowconfig/genesequencer.config": 4,
    "interface/windowconfig/hypercompressor.config": 6,
    "interface/windowconfig/kirhosshop.config": 6,
    "interface/windowconfig/lavalampstation.config": 6,
    "interface/windowconfig/mash.config": 4,
    "interface/windowconfig/medievalworkstation.config": 8,
    "interface/windowconfig/nanofabricator.config": 4,
    "interface/windowconfig/platingfood.config": 8,
    "interface/windowconfig/powerstation.config": 4,
    "interface/windowconfig/ppshop.config": 7,
    "interface/windowconfig/prototyper.config": 4,
    "interface/windowconfig/radien.config": 4,
    "interface/windowconfig/radienshop.config": 6,
    "interface/windowconfig/skathforgecrafting.config": 6,
    "interface/windowconfig/skathworktablecrafting.config": 6,
    "interface/windowconfig/tomedais.config": 4
}
DEAD_CONFIGS=[
    "interface/windowconfig/craftingmech.config",
    "interface/windowconfig/extractionlab.config",
    "interface/windowconfig/fruitpress.config",
    "interface/windowconfig/kitchen.config",
    "interface/windowconfig/powerpress.config",
    "interface/windowconfig/samplingarray2.config",
    "interface/windowconfig/xenostation.config"
]
PET_CONFIG="interface/objectcrafting/fu_pethouse/fu_pethouse.config"
PET_CONFIRM="interface/objectcrafting/fu_pethouse/fu_pethouse_confirmation.config"
PET_LUA="interface/objectcrafting/fu_pethouse/fu_pethouse.lua"

def value_at(data,pointer):
    cur=data
    for part in pointer.lstrip("/").split("/"):
        part=part.replace("~1","/").replace("~0","~")
        cur=cur[int(part)] if isinstance(cur,list) else cur[part]
    return cur

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    args=ap.parse_args()
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows=manifest["translations"]
    if manifest["translation_version"]!="0.42.0-beta":
        raise ValueError("v0.42 sürüm bilgisi bozuk")
    if len(rows)!=260:
        raise ValueError(f"v0.42 alan sayısı değişti: {len(rows)} != 260")
    if len({(r["asset"],r["pointer"]) for r in rows})!=260:
        raise ValueError("v0.42 manifestinde yinelenen alan var")
    counts={}
    parsed={}
    for asset in EXPECTED_ASSETS:
        parsed[asset]=audit.parse_jsonc((args.source/asset).read_text(encoding="utf-8-sig"))
    for row in rows:
        a,p=row["asset"],row["pointer"]
        if a not in EXPECTED_ASSETS:
            raise ValueError("v0.42 kapsam dışı asset: "+a)
        if a in DEAD_CONFIGS:
            raise ValueError("v0.42 runtime bağlantısı olmayan config: "+a)
        if value_at(parsed[a],p)!=row["en"]:
            raise ValueError("v0.42 kaynak uyuşmazlığı: "+a+p)
        counts[a]=counts.get(a,0)+1
    if counts!=EXPECTED_ASSETS:
        raise ValueError(f"v0.42 asset dağılımı değişti: {counts!r}")
    if counts.get(PET_CONFIG)!=16 or counts.get(PET_CONFIRM)!=5:
        raise ValueError("Pet House structured kapsamı 21 alan olmalı")
    catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
    idx={(r["asset"],r["pointer"]):r for r in catalog["translations"]}
    for row in rows:
        k=(row["asset"],row["pointer"])
        if k not in idx or idx[k]["tr"]!=row["tr"]:
            raise ValueError("v0.42 katalog eşleşmesi eksik: "+row["asset"]+row["pointer"])
    if catalog["translation_version"]!="0.42.0-beta":
        raise ValueError("Ana katalog v0.42 değil")
    raw=json.loads((TOOLS/"raw_text_translations.json").read_text(encoding="utf-8"))
    spec=next(x for x in raw["assets"] if x["asset"]==PET_LUA)
    if spec["source_blob_sha"]!="caf30e8c3d6816984f0ea46f3486bf1942038c65":
        raise ValueError("Pet House Lua kaynak SHA bozuk")
    if len(spec["replacements"])!=1 or int(spec["replacements"][0].get("expected_count",1))!=1:
        raise ValueError("Pet House Lua görünür replacement kapsamı değişti")
    print(json.dumps({"fields":len(rows),"assets":len(counts),"pet_house_fields":21,"pet_house_lua":1},ensure_ascii=False))

if __name__=="__main__":
    main()
