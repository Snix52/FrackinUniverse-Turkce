#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

ASSET="interface/windowconfig/charcreation.config"
SECTION="v0.40 karakter oluşturma arayüzü"
EXPECTED_FIELDS=19
EXPECTED_UNIQUE=18
TRANSLATIONS=json.loads(r'''{"Cancel":"İptal","CASUAL":"RAHAT","^#8d8d8d;CUSTOMISE":"^#8d8d8d;ÖZELLEŞTİR","^#8d8d8d;DIFFICULTY":"^#8d8d8d;ZORLUK","^#8d8d8d;FEMALE":"^#8d8d8d;KADIN","HARDCORE":"ZORLU","^#8d8d8d;MALE":"^#8d8d8d;ERKEK","^#8d8d8d;NAME":"^#8d8d8d;AD","RANDOMISE:":"RASTGELE:","^#8d8d8d;SPECIES":"^#8d8d8d;IRK","SURVIVAL":"HAYATTA KAL","Show clothing":"Kıyafetleri göster","Skip intro mission":"Giriş görevini atla","No need to eat and no death penalties.":"Yemek gerekmez ve ölmenin cezası yoktur.","Eat to survive, drop items on death.":"Hayatta kalmak için ye; ölünce eşyaların düşer.","When you die your character stays dead!":"Ölürsen karakterin kalıcı olarak ölür!","Name":"Ad","Done":"Tamam"}''')

def remaining_rows(source: Path):
    translated,_=audit.load_translations(Path(__file__).with_name("ceviriler.json"))
    data=audit.parse_jsonc((source/ASSET).read_text(encoding="utf-8-sig"))
    return sorted([
        r for r in audit.candidates_from_data(ASSET,data)
        if r.confidence=="confirmed" and (r.asset,r.pointer) not in translated
    ],key=lambda r:r.pointer)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    args=ap.parse_args()
    rows=remaining_rows(args.source)
    if len(rows)!=EXPECTED_FIELDS:
        raise ValueError(f"v0.40 alan sayısı değişti: {len(rows)} != {EXPECTED_FIELDS}")
    sources={r.value for r in rows}
    if len(sources)!=EXPECTED_UNIQUE:
        raise ValueError(f"v0.40 kaynak metin sayısı değişti: {len(sources)} != {EXPECTED_UNIQUE}")
    missing=sorted(sources-TRANSLATIONS.keys())
    if missing:
        raise ValueError(f"v0.40 eksik çeviri: {missing!r}")
    cp=Path(__file__).with_name("ceviriler.json")
    c=json.loads(cp.read_text(encoding="utf-8"))
    m={
        "schema_version":1,
        "translation_version":"0.40.0-beta",
        "scope":"Karakter oluşturma ekranındaki 19 canlı oyuncu metni; labelPortrait runtime şablonu ve teknik alanlar korunur.",
        "translations":[
            {"asset":r.asset,"pointer":r.pointer,"en":r.value,"tr":TRANSLATIONS[r.value],"section":SECTION}
            for r in rows
        ]
    }
    Path(__file__).with_name("v040_translations.json").write_text(
        json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )
    idx={(r["asset"],r["pointer"]) for r in c["translations"]}
    for r in m["translations"]:
        k=(r["asset"],r["pointer"])
        if k in idx:
            raise ValueError(f"v0.40 alanı zaten katalogda: {k}")
        c["translations"].append(r);idx.add(k)
    c["translation_version"]=m["translation_version"]
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"v0.40: {len(rows)} alan / {len(sources)} benzersiz metin")

if __name__=="__main__":
    main()
