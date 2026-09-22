#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

TOOLS=Path(__file__).resolve().parent
MANIFEST=TOOLS/"v043_translations.json"
CATALOG=TOOLS/"ceviriler.json"
EXPECTED_ASSETS={'interface/bees/alveary/alveary.config': 3, 'interface/bees/apiary/apiary.config': 3, 'interface/bees/industrialcentrifuge/industrialcentrifuge.config': 4, 'interface/bees/industrialcentrifuge/industrialcentrifuge2.config': 4, 'interface/bees/industrialcentrifuge/industrialcentrifuge3.config': 4, 'interface/bees/ironcentrifuge/ironcentrifuge.config': 4, 'interface/bees/woodencentrifuge/woodencentrifuge.config': 4, 'interface/catalystfuelrefinery/refinery.config': 4, 'interface/chests/cdx/chest1.config': 3, 'interface/chests/cdx/chest12.config': 3, 'interface/chests/cdx/chest16.config': 3, 'interface/chests/cdx/chest24.config': 3, 'interface/chests/cdx/chest32.config': 3, 'interface/chests/cdx/chest40.config': 3, 'interface/chests/cdx/chest48.config': 3, 'interface/chests/cdx/chest56.config': 3, 'interface/chests/cdx/chest60.config': 3, 'interface/chests/cdx/chest64.config': 3, 'interface/chests/cdx/chest9.config': 3, 'interface/chests/genechest128.config': 3, 'interface/chests/multitether.config': 1, 'interface/chests/voidchest200.config': 1, 'interface/extractor/brainsiphon.config': 4, 'interface/extractor/embalming.config': 3, 'interface/extractor/extractor.config': 4, 'interface/extractor/extractor2.config': 4, 'interface/extractor/extractor3.config': 4, 'interface/extractor/handmill.config': 4, 'interface/gnomefactory.config': 2, 'interface/kheAA/kheAA_terminal/kheAA_terminalGui.config': 6, 'interface/kukagps/kukagps.config': 2, 'interface/mechfuel/mechfuel.config': 4, 'interface/mechfuelrefinery/fuelrefinery.config': 4, 'interface/mfgstation.config': 2, 'interface/objectcrafting/aex.config': 2, 'interface/objectcrafting/colonystation.config': 8, 'interface/objectcrafting/fu_petrenamer/fu_petrenamer.config': 2, 'interface/objectcrafting/fu_precursorspawner.config': 1, 'interface/objectcrafting/fu_racialiser/fu_racialiser.config': 1, 'interface/objectcrafting/fu_racializer/fu_racializer.config': 2, 'interface/objectcrafting/pethealingauto.config': 1, 'interface/objectcrafting/warpedcompressor.config': 2, 'interface/scripted/fm_musicplayer/fm_musicplayer.config': 6, 'interface/scripted/fu_craftinfo/fu_craftinfo.config': 6, 'interface/scripted/fu_lootbox/lootboxData.config': 3, 'interface/scripted/fu_planetcockpit/fu_planetcockpit.config': 3, 'interface/scripted/fu_planetsail/fu_planetsail.config': 6, 'interface/scripted/fu_upgradetable/fu_upgradetable.config': 7, 'interface/scripted/fu_upgradetable/fu_upgradetable2.config': 7, 'interface/scripted/fu_upgradetable/fu_upgradetable3.config': 7, 'interface/scripted/fuvehiclerepair/fuvehiclerepairgui.config': 6, 'interface/scripted/fuweaponshuffler/fuweaponshuffler.config': 2, 'interface/scripted/logicgates/3statecyclerGUI.config': 8, 'interface/scripted/mannequin/cravenmannequingui.config': 3, 'interface/scripted/mannequin/fubustgui.config': 2, 'interface/scripted/mechassembly/mechassemblygui.config': 3, 'interface/scripted/mmupgrade/mmupgradegui.config': 3, 'interface/scripted/mmutility/mmutility.config': 6, 'interface/scripted/sbvn/pandorasboxsbvngui.config': 1, 'interface/scripted/stickynotepadfu/stickynotepadfu.config': 4, 'interface/scripted/techshop/techshop.config': 5, 'interface/scripted/tunableoredetector/tunableoredetector.config': 3, 'interface/scripted/xcustomcodex/xcodexui.config': 4, 'interface/windowconfig/fucorpsewagon.config': 6, 'interface/windowconfig/fuempty.config': 6, 'interface/windowconfig/fupeglacicraftingsnowpeoplegenerator.config': 4, 'interface/windowconfig/radienshopdrug.config': 6, 'interface/windowconfig/skathcodex.config': 6, 'interface/xenolab/xenolab.config': 4}
EXCLUDED_ASSETS=['interface/bees/industrialcentrifuge/jarringmachine.config', 'interface/chests/chest3.config', 'interface/expandstation/expandstation.config', 'interface/kheAA/kheAA_toolforge/kheAA_toolforgegui.config', 'interface/mechstats/mechstats.config', 'interface/objectcrafting/coffeemachine.config', 'interface/objectcrafting/fu_atmosfilter0.config', 'interface/objectcrafting/fu_atmosfilter1.config', 'interface/objectcrafting/fu_atmosfilter2.config', 'interface/objectcrafting/fu_atmosfilter3.config', 'interface/objectcrafting/fu_atmosfilter4.config', 'interface/objectcrafting/fu_atmosfilter5.config', 'interface/objectcrafting/fu_petnamer/fu_petnamer.config', 'interface/objectcrafting/fu_warped1.config', 'interface/objectcrafting/fu_warped3.config', 'interface/scripted/fugravgen/fugravgenui.config', 'interface/stats/stats.config', 'interface/windowconfig/craftingmech.config', 'interface/windowconfig/extractionlab.config', 'interface/windowconfig/fruitpress.config', 'interface/windowconfig/kitchen.config', 'interface/windowconfig/powerpress.config', 'interface/windowconfig/samplingarray2.config', 'interface/windowconfig/xenostation.config', 'metagui/themes/frackin/theme.json', 'metagui/themes/frackin/v2/theme.json']

LAYERED_PATCH_ASSETS={
    "interface/scripted/mechassembly/mechassemblygui.config":"interface/scripted/mechassembly/mechassemblygui.config.patch",
    "interface/scripted/mmupgrade/mmupgradegui.config":"interface/scripted/mmupgrade/mmupgradegui.config.patch",
}


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
            found=op.get("value")
            continue
        if path and pointer.startswith(path+"/") and "value" in op:
            suffix=pointer[len(path):]
            try:
                found=value_at(op["value"],suffix)
            except (KeyError,IndexError,TypeError,ValueError):
                pass
    return found

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    args=ap.parse_args()
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows=manifest["translations"]
    if manifest["translation_version"]!="0.43.0-beta":
        raise ValueError("v0.43 sürüm bilgisi bozuk")
    if len(rows)!=257:
        raise ValueError(f"v0.43 alan sayısı değişti: {len(rows)} != 257")
    if len({(r["asset"],r["pointer"]) for r in rows})!=257:
        raise ValueError("v0.43 manifestinde yinelenen alan var")
    if len({r["asset"] for r in rows})!=69:
        raise ValueError("v0.43 asset sayısı 69 olmalı")
    if len({r["en"] for r in rows})!=156:
        raise ValueError("v0.43 benzersiz kaynak metin sayısı 156 olmalı")
    counts={}
    parsed={}
    for asset in EXPECTED_ASSETS:
        source_path=args.source/(LAYERED_PATCH_ASSETS.get(asset,asset))
        parsed[asset]=audit.parse_jsonc(source_path.read_text(encoding="utf-8-sig"))
    for row in rows:
        a,p=row["asset"],row["pointer"]
        if a not in EXPECTED_ASSETS:
            raise ValueError("v0.43 kapsam dışı asset: "+a)
        if a in EXCLUDED_ASSETS:
            raise ValueError("v0.43 runtime kanıtı eksik asset: "+a)
        source_value=layered_patch_value(parsed[a],p) if a in LAYERED_PATCH_ASSETS else value_at(parsed[a],p)
        if source_value!=row["en"]:
            raise ValueError("v0.43 kaynak uyuşmazlığı: "+a+p)
        counts[a]=counts.get(a,0)+1
    if counts!=EXPECTED_ASSETS:
        raise ValueError(f"v0.43 asset dağılımı değişti: {counts!r}")
    catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
    idx={(r["asset"],r["pointer"]):r for r in catalog["translations"]}
    for row in rows:
        k=(row["asset"],row["pointer"])
        if k not in idx or idx[k]["tr"]!=row["tr"]:
            raise ValueError("v0.43 katalog eşleşmesi eksik: "+row["asset"]+row["pointer"])
    if catalog["translation_version"]!="0.43.0-beta":
        raise ValueError("Ana katalog v0.43 değil")
    print(json.dumps({"fields":len(rows),"assets":len(counts),"unique_source":len({r['en'] for r in rows}),"excluded_assets":len(EXCLUDED_ASSETS)},ensure_ascii=False))

if __name__=="__main__":
    main()