#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

TOOLS=Path(__file__).resolve().parent
MANIFEST=TOOLS/"v045_translations.json"
CATALOG=TOOLS/"ceviriler.json"
EXPECTED_ASSETS={"quests/other/transponder.questtemplate": 1, "quests/outpost/mechunlock.questtemplate": 1, "quests/outpost/mechupgrade1.questtemplate": 1, "quests/outpost/outpostclue.questtemplate": 1, "quests/outpost/shipupgrade/illegalshipupgrade2.questtemplate": 1, "quests/outpost/shipupgrade/illegalshipupgrade3.questtemplate": 1, "quests/outpost/shipupgrade/illegalshipupgrade4.questtemplate": 1, "quests/outpost/shipupgrade/illegalshipupgrade5.questtemplate": 1, "quests/outpost/shipupgrade/shipupgrade2.questtemplate": 1, "quests/outpost/shipupgrade/shipupgrade3.questtemplate": 1, "quests/outpost/shipupgrade/shipupgrade4.questtemplate": 1, "quests/outpost/shipupgrade/shipupgrade5.questtemplate": 1, "quests/outpost/techscientist4.questtemplate": 1, "quests/outpost/techscientist5.questtemplate": 2, "quests/outpost/techscientist6.questtemplate": 2, "quests/story/gaterepair.questtemplate": 5, "quests/story/protectorate.questtemplate": 3, "quests/story/shiprepair.questtemplate": 4}

def value_at(data,pointer):
    cur=data
    for part in pointer.lstrip("/").split("/"):
        part=part.replace("~1","/").replace("~0","~")
        cur=cur[int(part)] if isinstance(cur,list) else cur[part]
    return cur

def patch_value(ops,pointer):
    found=None
    for op in ops:
        if not isinstance(op,dict):
            continue
        path=str(op.get("path",""))
        if path==pointer and "value" in op:
            found=op["value"]
            continue
        if path and pointer.startswith(path+"/") and "value" in op:
            try:
                found=value_at(op["value"],pointer[len(path):])
            except (KeyError,IndexError,TypeError,ValueError):
                pass
    return found

def version_tuple(value):
    return tuple(map(int,value.split("-",1)[0].split(".")))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    args=ap.parse_args()
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows=m["translations"]
    if m["translation_version"]!="0.45.0-beta":
        raise ValueError("v0.45 sürüm bilgisi bozuk")
    if len(rows)!=29 or len({(r["asset"],r["pointer"]) for r in rows})!=29:
        raise ValueError("v0.45 alan kapsamı bozuk")
    if len({r["asset"] for r in rows})!=18 or len({r["en"] for r in rows})!=29:
        raise ValueError("v0.45 asset/benzersiz kaynak kapsamı bozuk")
    counts={}
    cache={}
    for row in rows:
        a,p=row["asset"],row["pointer"]
        qa=row.get("qa",{})
        patch=qa.get("source_patch")
        if not qa.get("layered_source") or not patch or not patch.endswith(".questtemplate.patch"):
            raise ValueError("v0.45 layered source eksik: "+a+p)
        if patch not in cache:
            source=args.source/patch
            if not source.is_file():
                raise FileNotFoundError(source)
            cache[patch]=audit.parse_jsonc(source.read_text(encoding="utf-8-sig"))
        if patch_value(cache[patch],p)!=row["en"]:
            raise ValueError("v0.45 pinned patch kaynak uyuşmazlığı: "+a+p)
        counts[a]=counts.get(a,0)+1
    if counts!=EXPECTED_ASSETS:
        raise ValueError("v0.45 asset dağılımı değişti")
    c=json.loads(CATALOG.read_text(encoding="utf-8"))
    if version_tuple(c["translation_version"]) < (0,45,0):
        raise ValueError("Ana katalog v0.45 öncesinde")
    idx={(r["asset"],r["pointer"]):r for r in c["translations"]}
    for row in rows:
        if idx.get((row["asset"],row["pointer"]),{}).get("tr")!=row["tr"]:
            raise ValueError("v0.45 katalog eşleşmesi eksik: "+row["asset"]+row["pointer"])
    print(json.dumps({"fields":29,"assets":18,"unique_source":29,"pinned_patch_sources":len(cache)},ensure_ascii=False))

if __name__=="__main__":
    main()