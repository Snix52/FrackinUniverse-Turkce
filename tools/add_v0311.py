#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
CATALOG = TOOLS / "ceviriler.json"
MANIFEST = TOOLS / "v0311_translations.json"

def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = catalog["translations"]
    index = {(r["asset"], r["pointer"]): r for r in rows}
    for row in manifest["translations"]:
        key = (row["asset"], row["pointer"])
        current = index.get(key)
        if current:
            if current["en"] != row["en"] or current["tr"] != row["tr"]:
                raise ValueError(f"v0.31.1 catalog conflict: {key}")
            continue
        rows.append(row)
        index[key] = row
    catalog["translation_version"] = manifest["translation_version"]
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"v0.31.1 catalog: {len(rows)} structured fields")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
