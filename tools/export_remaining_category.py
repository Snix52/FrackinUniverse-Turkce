#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path, PurePosixPath
import audit_remaining as audit

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--category",required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()

    translated,_=audit.load_translations(Path(__file__).with_name("ceviriler.json"))
    candidates={}
    for path in sorted(args.source.rglob("*")):
        if not path.is_file():
            continue
        rel=PurePosixPath(path.relative_to(args.source).as_posix())
        if audit.excluded_path(rel):
            continue
        if path.suffix.lower() in audit.BINARY_SUFFIXES or path.stat().st_size>8_000_000:
            continue
        try:
            raw=path.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError,OSError):
            continue
        if not raw.lstrip().startswith(("{","[")):
            continue
        try:
            data=audit.parse_jsonc(raw)
        except Exception:
            continue
        for row in audit.candidates_from_data(rel.as_posix(),data):
            if audit.nonvisible_research_candidate(row.asset,row.pointer):
                continue
            key=(row.asset,row.pointer)
            prev=candidates.get(key)
            if prev is None or (prev.confidence=="review" and row.confidence=="confirmed"):
                candidates[key]=row

    rows=[
        {"asset":r.asset,"pointer":r.pointer,"en":r.value,"key":r.key,"origin":r.origin}
        for key,r in sorted(candidates.items())
        if r.confidence=="confirmed" and r.category==args.category and key not in translated
    ]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps({"category":args.category,"count":len(rows),"rows":rows},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"{args.category}: {len(rows)} fields / {len({r['asset'] for r in rows})} assets")
if __name__=="__main__":
    main()
