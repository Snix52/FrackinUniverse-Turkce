#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
import audit_remaining as audit
ASSET="interface/kheAA/kheAA_router/kheAA_routerGui.config"
SECTION="v0.37 KheAA yönlendirici arayüzü"
EXPECTED_FIELDS=35
EXPECTED_UNIQUE=18
TRANSLATIONS=json.loads(r'''{"Filtered Items:":"Filtrelenen Eşyalar:","^yellow;Help Mode^reset;:":"^yellow;Yardım Modu^reset;:","Input Slots:":"Giriş Yuvaları:","I":"T","Inv. Logic":"Ters Mantık","Item 1":"Eşya 1","Item 2":"Eşya 2","Item 3":"Eşya 3","Item 4":"Eşya 4","Item 5":"Eşya 5","Category":"Kategori","Exact":"Tam","Type":"Tür","Leave One":"Birini Bırak","Stack Only":"Yığına Ekle","Output Slots:":"Çıkış Yuvaları:","Even Split":"Eşit Böl","Slot Split":"Yuvaya Böl"}''')
def remaining_rows(source:Path):
    translated,_=audit.load_translations(Path(__file__).with_name("ceviriler.json"))
    data=audit.parse_jsonc((source/ASSET).read_text(encoding="utf-8-sig"))
    return sorted([r for r in audit.candidates_from_data(ASSET,data) if r.confidence=="confirmed" and (r.asset,r.pointer) not in translated],key=lambda r:r.pointer)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--source",type=Path,required=True);args=ap.parse_args()
    rows=remaining_rows(args.source)
    if len(rows)!=EXPECTED_FIELDS:raise ValueError(f"v0.37 alan sayısı değişti: {len(rows)} != {EXPECTED_FIELDS}")
    sources={r.value for r in rows}
    if len(sources)!=EXPECTED_UNIQUE:raise ValueError(f"v0.37 kaynak metin sayısı değişti: {len(sources)} != {EXPECTED_UNIQUE}")
    missing=sorted(sources-TRANSLATIONS.keys())
    if missing:raise ValueError(f"v0.37 eksik çeviri: {missing!r}")
    cp=Path(__file__).with_name("ceviriler.json");c=json.loads(cp.read_text(encoding="utf-8"))
    m={"schema_version":1,"translation_version":"0.37.0-beta","scope":"KheAA Eşya Aktarım Cihazı yönlendirici panelinin 35 canlı config alanı; yardım modu Lua metinleri aynı sürümde raw_text_translations.json ile kapatılır.","translations":[{"asset":r.asset,"pointer":r.pointer,"en":r.value,"tr":TRANSLATIONS[r.value],"section":SECTION} for r in rows]}
    Path(__file__).with_name("v037_translations.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    idx={(r["asset"],r["pointer"]) for r in c["translations"]}
    for r in m["translations"]:
        k=(r["asset"],r["pointer"])
        if k in idx:raise ValueError(f"v0.37 alanı zaten katalogda: {k}")
        c["translations"].append(r);idx.add(k)
    c["translation_version"]=m["translation_version"];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
