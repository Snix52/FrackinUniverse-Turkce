#!/usr/bin/env python3
"""Exact-source gate for the v0.50 beekeeping-system translation tranche."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit
from write_build_evidence import verify_source

MANIFEST = TOOLS / "v050_translations.json"
CATALOG = TOOLS / "ceviriler.json"
EXPECTED_FIELDS = 537
EXPECTED_ASSETS = 207
EXPECTED_UNIQUE = 308


def read_at(root: object, pointer: str) -> object:
    current = root
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def source_candidates(source: Path) -> set[tuple[str, str]]:
    translated, _ = audit.load_translations(CATALOG)
    target_rows = json.loads(MANIFEST.read_text(encoding="utf-8"))["translations"]
    target_keys = {(row["asset"], row["pointer"]) for row in target_rows}
    translated.difference_update(target_keys)
    found: set[tuple[str, str]] = set()
    bee_root = source / "bees"
    if not bee_root.is_dir():
        raise FileNotFoundError(bee_root)
    for path in sorted(bee_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() in audit.BINARY_SUFFIXES:
            continue
        rel = PurePosixPath(path.relative_to(source).as_posix())
        if audit.excluded_path(rel):
            continue
        try:
            data = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
        except (UnicodeDecodeError, OSError, ValueError):
            continue
        for candidate in audit.candidates_from_data(rel.as_posix(), data):
            candidate = audit.v046_candidate_visibility(candidate)
            if candidate is None or candidate.confidence != "confirmed":
                continue
            if (candidate.asset, candidate.pointer) in translated:
                continue
            if (candidate.asset in audit.V018_DEAD_OBJECT_ASSETS
                    or candidate.asset in audit.V020_INACTIVE_QUEST_ASSETS
                    or candidate.asset in audit.NONVISIBLE_QUEST_ASSETS
                    or candidate.asset in audit.AUDIT_EXCLUDED_PATHS):
                continue
            if (audit.audit_excluded_candidate(candidate.asset, candidate.pointer)
                    or audit.nonvisible_research_candidate(candidate.asset, candidate.pointer)):
                continue
            found.add((candidate.asset, candidate.pointer))
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    verify_source(args.source.resolve())

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = manifest["translations"]
    if manifest["translation_version"] != "0.50.0-beta":
        raise ValueError("v0.50 manifest version drift")
    keys = {(row["asset"], row["pointer"]) for row in rows}
    if len(rows) != EXPECTED_FIELDS or len(keys) != EXPECTED_FIELDS:
        raise ValueError(f"v0.50 field count/duplicate drift: {len(rows)}")
    if len({row["asset"] for row in rows}) != EXPECTED_ASSETS:
        raise ValueError("v0.50 asset count drift")
    if len({row["en"] for row in rows}) != EXPECTED_UNIQUE:
        raise ValueError("v0.50 unique source count drift")
    if any(not row["asset"].startswith("bees/") for row in rows):
        raise ValueError("v0.50 asset outside the bee-system scope")
    if source_candidates(args.source) != keys:
        raise ValueError("v0.50 candidate set differs from the pinned bee-system source")

    source_cache: dict[str, object] = {}
    for row in rows:
        path = args.source / row["asset"]
        if row["asset"] not in source_cache:
            source_cache[row["asset"]] = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
        if read_at(source_cache[row["asset"]], row["pointer"]) != row["en"]:
            raise ValueError("v0.50 pinned source mismatch: " + row["asset"] + row["pointer"])

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if catalog["translation_version"] != "0.50.0-beta":
        raise ValueError("catalog version behind v0.50")
    index = {(row["asset"], row["pointer"]): row for row in catalog["translations"]}
    for row in rows:
        current = index.get((row["asset"], row["pointer"]))
        if not current or current["en"] != row["en"] or current["tr"] != row["tr"]:
            raise ValueError("v0.50 catalog mismatch: " + row["asset"] + row["pointer"])

    print(f"v0.50 source gate PASS: {len(rows)} alan / {len({r['asset'] for r in rows})} asset / {len({r['en'] for r in rows})} kaynak")


if __name__ == "__main__":
    main()
