#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path, PurePosixPath

import audit_remaining as audit
from write_build_evidence import verify_source


def export_category(source: Path, catalog: Path, category: str) -> dict:
    verify_source(source.resolve())
    translated, _ = audit.load_translations(catalog.resolve())
    candidates = {}

    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel = PurePosixPath(path.relative_to(source).as_posix())
        if audit.excluded_path(rel):
            continue
        if path.suffix.lower() in audit.BINARY_SUFFIXES or path.stat().st_size > 8_000_000:
            continue
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, OSError):
            continue
        if not raw.lstrip().startswith(("{", "[")):
            continue
        try:
            data = audit.parse_jsonc(raw)
        except Exception:
            continue
        for candidate in audit.candidates_from_data(rel.as_posix(), data):
            if audit.nonvisible_research_candidate(candidate.asset, candidate.pointer):
                continue
            if candidate.confidence != "confirmed" or candidate.category != category:
                continue
            key = (candidate.asset, candidate.pointer)
            if key in translated:
                continue
            candidates[key] = candidate

    rows = [
        {
            "asset": row.asset,
            "pointer": row.pointer,
            "source": row.value,
            "origin": row.origin,
            "key": row.key,
        }
        for row in sorted(candidates.values(), key=lambda x: (x.asset, x.pointer))
    ]
    by_source = defaultdict(list)
    for row in rows:
        by_source[row["source"]].append({"asset": row["asset"], "pointer": row["pointer"]})

    return {
        "schema_version": 1,
        "category": category,
        "fields": len(rows),
        "assets": len({row["asset"] for row in rows}),
        "unique_source_strings": len(by_source),
        "rows": rows,
        "by_source": [
            {"source": source_text, "occurrences": occurrences}
            for source_text, occurrences in sorted(
                by_source.items(), key=lambda item: (-len(item[1]), item[0].casefold())
            )
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--catalog", type=Path, default=Path("tools/ceviriler.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = export_category(args.source, args.catalog, args.category)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: data[k] for k in ("category", "fields", "assets", "unique_source_strings")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
