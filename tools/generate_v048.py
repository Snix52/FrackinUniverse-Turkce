#!/usr/bin/env python3
"""Exact-source gate for the first v0.48 wood-building materials tranche."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit
from write_build_evidence import verify_source

MANIFEST = TOOLS / "v048_translations.json"
CATALOG = TOOLS / "ceviriler.json"
FAMILIES = {"darkwood", "lightwood", "treatedwood"}
EXPECTED_FIELDS = 151
EXPECTED_ASSETS = 32
EXPECTED_UNIQUE = 87
ALLOWED_POINTERS = {
    "/description", "/shortdescription", "/floranDescription",
    "/glitchDescription", "/novakidDescription",
}


def read_at(root: object, pointer: str) -> object:
    current = root
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def source_candidates(source: Path) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for family in sorted(FAMILIES):
        root = source / "tiles" / "materials" / family
        if not root.is_dir():
            raise FileNotFoundError(root)
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() in audit.BINARY_SUFFIXES:
                continue
            rel = PurePosixPath(path.relative_to(source).as_posix())
            data = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
            for candidate in audit.candidates_from_data(rel.as_posix(), data):
                candidate = audit.v046_candidate_visibility(candidate)
                if candidate is None or candidate.confidence != "confirmed":
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
    verify_source(args.source)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = manifest["translations"]
    if manifest["translation_version"] != "0.48.0-beta":
        raise ValueError("v0.48 manifest version drift")
    if len(rows) != EXPECTED_FIELDS:
        raise ValueError(f"v0.48 field drift: {len(rows)}")
    keys = {(row["asset"], row["pointer"]) for row in rows}
    if len(keys) != EXPECTED_FIELDS:
        raise ValueError("v0.48 duplicate field")
    if len({row["asset"] for row in rows}) != EXPECTED_ASSETS:
        raise ValueError("v0.48 asset drift")
    if len({row["en"] for row in rows}) != EXPECTED_UNIQUE:
        raise ValueError("v0.48 source drift")
    if any(not row["asset"].startswith("tiles/materials/")
           or PurePosixPath(row["asset"]).parts[2] not in FAMILIES for row in rows):
        raise ValueError("v0.48 asset outside the selected wood families")
    if {row["pointer"] for row in rows} - ALLOWED_POINTERS:
        raise ValueError("v0.48 pointer drift")
    if source_candidates(args.source) != keys:
        raise ValueError("v0.48 candidate set differs from the pinned source family")

    source_cache: dict[str, object] = {}
    for row in rows:
        path = args.source / row["asset"]
        if not path.is_file():
            raise FileNotFoundError(path)
        if row["asset"] not in source_cache:
            source_cache[row["asset"]] = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
        if read_at(source_cache[row["asset"]], row["pointer"]) != row["en"]:
            raise ValueError("v0.48 pinned source mismatch: " + row["asset"] + row["pointer"])

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if catalog["translation_version"] != "0.48.0-beta":
        raise ValueError("catalog version behind v0.48")
    index = {(row["asset"], row["pointer"]): row for row in catalog["translations"]}
    for row in rows:
        current = index.get((row["asset"], row["pointer"]))
        if not current or current["en"] != row["en"] or current["tr"] != row["tr"]:
            raise ValueError("v0.48 catalog mismatch: " + row["asset"] + row["pointer"])

    print(f"v0.48 source gate PASS: {len(rows)} alan / {len({r['asset'] for r in rows})} asset / {len({r['en'] for r in rows})} kaynak")


if __name__ == "__main__":
    main()
