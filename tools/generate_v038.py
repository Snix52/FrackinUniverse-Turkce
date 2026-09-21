#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

ASSET="interface/scripted/statWindow/extraStatsWindow.config"
SECTION="v0.38 gelişmiş istatistikler arayüzü"
EXPECTED_FIELDS=22
EXPECTED_UNIQUE=22
TRANSLATIONS=json.loads(r'''{"Hover over a stat for its description":"Açıklaması için bir istatistiğin üzerine gel","Advanced stats":"Gelişmiş İstatistikler","Maximum Health":"Maksimum Can","Maximum Energy":"Maksimum Enerji","Power Multiplier":"Güç Çarpanı","Breath Duration":"Nefes Süresi","Knockback Resist":"Geri Tepme Direnci","Shield Bash Chance":"Kalkan Darbesi Şansı","Healing Bonus":"İyileştirme Bonusu","Health Regen":"Can Yenilenmesi","Energy Regen":"Enerji Yenilenmesi","Crit Multiplier":"Kritik Çarpanı","Breath Regen Time":"Nefes Yenilenme Süresi","Knockback Threshold":"Geri Tepme Eşiği","Shield Bash Push":"Kalkan Darbesi İtme Gücü","Charisma":"Karizma","Protection":"Koruma","Energy Block Duration":"Enerji Yenilenme Gecikmesi","Crit Chance":"Kritik Şansı","Starvation (Minutes from Full)":"Açlığa Kalan Süre (Dakika)","Fall Damage Mult":"Düşme Hasarı Çarpanı","Madness Resistance":"Delilik Direnci"}''')

def remaining_rows(source: Path):
    translated,_=audit.load_translations(Path(__file__).with_name("ceviriler.json"))
    data=audit.parse_jsonc((source/ASSET).read_text(encoding="utf-8-sig"))
    return sorted([
        r for r in audit.candidates_from_data(ASSET,data)
        if r.confidence=="confirmed" and (r.asset,r.pointer) not in translated
    ],key=lambda r:r.pointer)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--source",type=Path,required=True);args=ap.parse_args()
    rows=remaining_rows(args.source)
    if len(rows)!=EXPECTED_FIELDS: raise ValueError(f"v0.38 alan sayısı değişti: {len(rows)} != {EXPECTED_FIELDS}")
    sources={r.value for r in rows}
    if len(sources)!=EXPECTED_UNIQUE: raise ValueError(f"v0.38 kaynak metin sayısı değişti: {len(sources)} != {EXPECTED_UNIQUE}")
    missing=sorted(sources-TRANSLATIONS.keys())
    if missing: raise ValueError(f"v0.38 eksik çeviri: {missing!r}")
    cp=Path(__file__).with_name("ceviriler.json");c=json.loads(cp.read_text(encoding="utf-8"))
    m={"schema_version":1,"translation_version":"0.38.0-beta",
       "scope":"Gelişmiş istatistikler penceresinin başlığı, 20 canlı stat tooltip'i ve varsayılan tooltip metni. Runtime sayısal şablonları ve teknik alanlar korunur.",
       "translations":[{"asset":r.asset,"pointer":r.pointer,"en":r.value,"tr":TRANSLATIONS[r.value],"section":SECTION} for r in rows]}
    Path(__file__).with_name("v038_translations.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    idx={(r["asset"],r["pointer"]) for r in c["translations"]}
    for r in m["translations"]:
        k=(r["asset"],r["pointer"])
        if k in idx: raise ValueError(f"v0.38 alanı zaten katalogda: {k}")
        c["translations"].append(r);idx.add(k)
    c["translation_version"]=m["translation_version"]
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"v0.38: {len(rows)} alan / {len(sources)} benzersiz metin")
if __name__=="__main__": main()
