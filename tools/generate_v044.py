#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit
TOOLS=Path(__file__).resolve().parent
MANIFEST=TOOLS/"v044_translations.json"
CATALOG=TOOLS/"ceviriler.json"
EXPECTED_ASSETS={"interface/chests/chest3.config":2,"interface/objectcrafting/fu_atmosfilter1.config":1,"interface/objectcrafting/fu_warped1.config":1,"interface/objectcrafting/fu_warped3.config":1,"interface/stats/stats.config":4,"metagui/themes/frackin/theme.json":2,"metagui/themes/frackin/v2/theme.json":2}
LAYERED_PATCH_ASSETS={"interface/stats/stats.config":"interface/stats/stats.config.patch"}
DEAD_ASSETS=["interface/bees/industrialcentrifuge/jarringmachine.config","interface/expandstation/expandstation.config","interface/kheAA/kheAA_toolforge/kheAA_toolforgegui.config","interface/mechstats/mechstats.config","interface/objectcrafting/coffeemachine.config","interface/objectcrafting/fu_atmosfilter0.config","interface/objectcrafting/fu_atmosfilter2.config","interface/objectcrafting/fu_atmosfilter3.config","interface/objectcrafting/fu_atmosfilter4.config","interface/objectcrafting/fu_atmosfilter5.config","interface/objectcrafting/fu_petnamer/fu_petnamer.config","interface/scripted/fugravgen/fugravgenui.config","interface/windowconfig/craftingmech.config","interface/windowconfig/extractionlab.config","interface/windowconfig/fruitpress.config","interface/windowconfig/kitchen.config","interface/windowconfig/powerpress.config","interface/windowconfig/samplingarray2.config","interface/windowconfig/xenostation.config"]
TODO_FIELDS=["/darkregen/description","/fuCharisma/description","/lightregen/description","/upgradeable/description"]
def value_at(data,pointer):
    cur=data
    for part in pointer.lstrip("/").split("/"):
        part=part.replace("~1","/").replace("~0","~")
        cur=cur[int(part)] if isinstance(cur,list) else cur[part]
    return cur
def layered_patch_value(ops,pointer):
    found=None
    for op in ops:
        path=op.get("path","")
        if pointer==path:
            found=op.get("value"); continue
        if path and pointer.startswith(path+"/") and "value" in op:
            try: found=value_at(op["value"],pointer[len(path):])
            except (KeyError,IndexError,TypeError,ValueError): pass
    return found
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source",type=Path,required=True); args=ap.parse_args()
    m=json.loads(MANIFEST.read_text(encoding="utf-8")); rows=m["translations"]
    if m["translation_version"]!="0.44.0-beta": raise ValueError("v0.44 sürüm bilgisi bozuk")
    if len(rows)!=13 or len({(r["asset"],r["pointer"]) for r in rows})!=13: raise ValueError("v0.44 alan kapsamı bozuk")
    if len({r["asset"] for r in rows})!=7 or len({r["en"] for r in rows})!=12: raise ValueError("v0.44 asset/benzersiz kaynak kapsamı bozuk")
    parsed={}; counts={}
    for a in EXPECTED_ASSETS:
        p=args.source/(LAYERED_PATCH_ASSETS.get(a,a)); parsed[a]=audit.parse_jsonc(p.read_text(encoding="utf-8-sig"))
    for r in rows:
        a,p=r["asset"],r["pointer"]
        if a not in EXPECTED_ASSETS: raise ValueError("v0.44 kapsam dışı asset: "+a)
        v=layered_patch_value(parsed[a],p) if a in LAYERED_PATCH_ASSETS else value_at(parsed[a],p)
        if v!=r["en"]: raise ValueError("v0.44 kaynak uyuşmazlığı: "+a+p)
        counts[a]=counts.get(a,0)+1
    if counts!=EXPECTED_ASSETS: raise ValueError("v0.44 asset dağılımı değişti")
    if not set(DEAD_ASSETS).issubset(audit.AUDIT_EXCLUDED_PATHS): raise ValueError("runtime-inaktif UI listesi audit kurallarında eksik")
    if not set(TODO_FIELDS).issubset(audit.AUDIT_EXCLUDED_FIELDS.get("interface/stats/stats.config",frozenset())): raise ValueError("-todo- audit dışlaması eksik")
    c=json.loads(CATALOG.read_text(encoding="utf-8")); idx={(r["asset"],r["pointer"]):r for r in c["translations"]}
    for r in rows:
        if idx.get((r["asset"],r["pointer"]),{}).get("tr")!=r["tr"]: raise ValueError("v0.44 katalog eşleşmesi eksik")
    if c["translation_version"]!="0.44.0-beta": raise ValueError("Ana katalog v0.44 değil")
    print(json.dumps({"fields":13,"assets":7,"unique_source":12,"dead_assets":19,"dev_placeholders":4},ensure_ascii=False))
if __name__=="__main__": main()
