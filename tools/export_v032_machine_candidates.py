#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path, PurePosixPath

from audit_remaining import (
    BINARY_SUFFIXES,
    Candidate,
    candidates_from_data,
    excluded_path,
    load_translations,
    nonvisible_research_candidate,
    parse_jsonc,
)

CATEGORY = "Makineler, üretim ve dükkân nesneleri"

def collect(source: Path, catalog: Path) -> list[dict[str, str]]:
    translated, _ = load_translations(catalog)
    candidates: dict[tuple[str, str], Candidate] = {}
    roots = [
        source / "bees/objects",
        source / "objects/crafting",
        source / "objects/power",
        source / "objects/bees",
        source / "objects/scienceoutpost",
    ]
    paths = sorted(path for root in roots if root.exists() for path in root.rglob("*"))
    for path in paths:
        if not path.is_file():
            continue
        rel = PurePosixPath(path.relative_to(source).as_posix())
        if excluded_path(rel):
            continue
        if path.suffix.lower() in BINARY_SUFFIXES or path.stat().st_size > 8_000_000:
            continue
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, OSError):
            continue
        if not raw.lstrip().startswith(("{", "[")):
            continue
        try:
            data = parse_jsonc(raw)
        except Exception:
            continue
        for candidate in candidates_from_data(rel.as_posix(), data):
            if nonvisible_research_candidate(candidate.asset, candidate.pointer):
                continue
            key = (candidate.asset, candidate.pointer)
            previous = candidates.get(key)
            if previous is None or (previous.confidence == "review" and candidate.confidence == "confirmed"):
                candidates[key] = candidate

    rows = []
    for key, row in sorted(candidates.items()):
        if row.confidence != "confirmed" or row.category != CATEGORY or key in translated:
            continue
        rows.append({
            "asset": row.asset,
            "pointer": row.pointer,
            "source": row.value,
            "key": row.key,
            "origin": row.origin,
        })
    return rows

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--catalog", type=Path, default=Path(__file__).with_name("ceviriler.json"))
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    rows = collect(args.source, args.catalog)
    payload = {
        "schema_version": 1,
        "category": CATEGORY,
        "fields": len(rows),
        "assets": len({r["asset"] for r in rows}),
        "non_category_fields": sum(r["key"].lower() != "category" for r in rows),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("fields", "assets", "non_category_fields")}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
