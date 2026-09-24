#!/usr/bin/env python3
"""Exact-source gate for the v0.64 deep generic food tranche."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit
from write_build_evidence import verify_source

MANIFEST = TOOLS / "v064_translations.json"
CATALOG = TOOLS / "ceviriler.json"
EXPECTED_FIELDS = 168
EXPECTED_ASSETS = 152
EXPECTED_UNIQUE = 168
EXPECTED_LAYERED_FIELDS = 136


def source_candidates(source: Path) -> dict[tuple[str, str], audit.Candidate]:
    translated, _ = audit.load_translations(CATALOG)
    target_rows = json.loads(MANIFEST.read_text(encoding="utf-8"))["translations"]
    target_keys = {(row["asset"], row["pointer"]) for row in target_rows}
    translated.difference_update(target_keys)
    candidates: dict[tuple[str, str], audit.Candidate] = {}
    for path in sorted((source / "items" / "generic" / "food").rglob("*")):
        if not path.is_file() or path.suffix.lower() in audit.BINARY_SUFFIXES or path.stat().st_size > 8_000_000:
            continue
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, OSError):
            continue
        if not raw.lstrip().startswith(("{", "[")):
            continue
        try:
            data = audit.parse_jsonc(raw)
        except ValueError:
            continue
        rel = PurePosixPath(path.relative_to(source).as_posix())
        if audit.excluded_path(rel):
            continue
        if len(rel.parts) < 5 or rel.parts[3] == "tier1":
            continue
        for candidate in audit.candidates_from_data(rel.as_posix(), data):
            candidate = audit.v046_candidate_visibility(candidate)
            if candidate is None or candidate.confidence != "confirmed" or not candidate.asset.startswith("items/generic/food/") or candidate.pointer not in {"/shortdescription", "/description"}:
                continue
            if candidate.pointer == "/category":
                continue
            if (
                candidate.asset in audit.V018_DEAD_OBJECT_ASSETS
                or candidate.asset in audit.V020_INACTIVE_QUEST_ASSETS
                or candidate.asset in audit.NONVISIBLE_QUEST_ASSETS
                or candidate.asset in audit.AUDIT_EXCLUDED_PATHS
            ):
                continue
            if audit.audit_excluded_candidate(candidate.asset, candidate.pointer) or audit.nonvisible_research_candidate(candidate.asset, candidate.pointer):
                continue
            key = (candidate.asset, candidate.pointer)
            previous = candidates.get(key)
            if (
                previous is None
                or candidate.origin.startswith(candidate.asset + ".patch")
                or (previous.confidence == "review" and candidate.confidence == "confirmed")
            ):
                candidates[key] = candidate
    return {key: candidate for key, candidate in candidates.items() if key not in translated}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    verify_source(args.source.resolve())

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = manifest["translations"]
    if manifest["translation_version"] != "0.64.0-beta":
        raise ValueError("v0.64 manifest version drift")
    keys = {(row["asset"], row["pointer"]) for row in rows}
    if len(rows) != EXPECTED_FIELDS or len(keys) != EXPECTED_FIELDS:
        raise ValueError(f"v0.64 field count/duplicate drift: {len(rows)}")
    if len({row["asset"] for row in rows}) != EXPECTED_ASSETS:
        raise ValueError("v0.64 asset count drift")
    if len({row["en"] for row in rows}) != EXPECTED_UNIQUE:
        raise ValueError("v0.64 unique source count drift")
    if sum(bool(row.get("qa", {}).get("layered_source")) for row in rows) != EXPECTED_LAYERED_FIELDS:
        raise ValueError("v0.64 FU overlay provenance count drift")
    candidates = source_candidates(args.source)
    if set(candidates) != keys:
        missing = sorted(set(candidates) - keys)
        extra = sorted(keys - set(candidates))
        raise ValueError(f"v0.64 candidate set differs: missing={missing[:3]} extra={extra[:3]}")
    for row in rows:
        asset = row["asset"]
        expected_qa = (
            {"layered_source": True, "source_patch": asset + ".patch"}
            if not (args.source / asset).is_file() else None
        )
        if row.get("qa") != expected_qa:
            raise ValueError("v0.64 source provenance mismatch: " + asset + row["pointer"])
        if candidates[(row["asset"], row["pointer"])].value != row["en"]:
            raise ValueError("v0.64 pinned source mismatch: " + row["asset"] + row["pointer"])
        if re.search(r"\bmech\b", row["en"], re.I) and not re.search(r"\bMech\b", row["tr"]):
            raise ValueError("v0.64 LOCKED Mech term missing: " + row["asset"] + row["pointer"])
        if "Madness Gain" in row["en"] and "Delilik Kazanımı" not in row["tr"]:
            raise ValueError("v0.64 LOCKED Madness Gain term missing: " + row["asset"] + row["pointer"])
        if re.search(r"\bCherry\b", row["en"], re.I) and not re.search(r"\bKiraz\b", row["tr"], re.I):
            raise ValueError("v0.64 LOCKED Cherry term missing: " + row["asset"] + row["pointer"])

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    version = tuple(int(part) for part in catalog["translation_version"].split("-", 1)[0].split("."))
    if version < (0, 64, 0):
        raise ValueError("catalog version behind v0.64")
    index = {(row["asset"], row["pointer"]): row for row in catalog["translations"]}
    for row in rows:
        current = index.get((row["asset"], row["pointer"]))
        if not current or any(current.get(field) != row.get(field) for field in ("en", "tr", "qa")):
            raise ValueError("v0.64 catalog mismatch: " + row["asset"] + row["pointer"])

    print(f"v0.64 source gate PASS: {len(rows)} alan / {len({row['asset'] for row in rows})} asset / {len({row['en'] for row in rows})} kaynak")


if __name__ == "__main__":
    main()
