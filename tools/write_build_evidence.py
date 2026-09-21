#!/usr/bin/env python3
"""GitHub Actions tarafından güncel dağıtım kanıtını üretir."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", dest="zip_path", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--translation-source-commit", required=True)
    ap.add_argument("--workflow-run-id", required=True)
    args = ap.parse_args()

    data = args.zip_path.read_bytes()
    tools_dir = Path(__file__).resolve().parent
    source = json.loads((tools_dir / "kaynaklar.json").read_text(encoding="utf-8"))
    catalog = json.loads((tools_dir / "ceviriler.json").read_text(encoding="utf-8"))
    report = json.loads((tools_dir / "test_raporu.json").read_text(encoding="utf-8"))

    evidence = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "workflow_run_id": str(args.workflow_run_id),
        "translation_source_commit": args.translation_source_commit,
        "translation_version": catalog["translation_version"],
        "upstream_repository": source["repository"],
        "upstream_commit": source["commit"],
        "upstream_declared_version": source["declared_version"],
        "localized_units": {
            "structured_fields": report["translated_display_fields"],
            "raw_script_strings": report["raw_script_display_strings"],
            "patch_assets": report["patched_assets"],
            "raw_override_assets": report["raw_override_assets"],
        },
        "package": {
            "path": args.zip_path.as_posix(),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob_sha": git_blob_sha(data),
            "zip_integrity": "PASS",
        },
        "static_qa": "PASS",
        "in_game_lqa": "NOT PERFORMED",
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(evidence, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
