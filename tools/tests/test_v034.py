import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"

class V034Tests(unittest.TestCase):
    def test_v034_manifest_is_applied_exactly(self):
        manifest = json.loads((TOOLS / "v034_translations.json").read_text(encoding="utf-8"))
        catalog = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        rows = manifest["translations"]
        self.assertEqual(manifest["translation_version"], "0.34.0-beta")
        self.assertEqual(len(rows), 242)
        self.assertEqual(len({r["en"] for r in rows}), 193)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in rows}), 242)
        index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
        for row in rows:
            key = (row["asset"], row["pointer"])
            self.assertEqual(row["asset"], "interface/cockpit/cockpit.config")
            self.assertTrue(row["pointer"].startswith("/visitableTypeDescription/"))
            self.assertEqual(row["section"], "v0.34 cockpit gezegen açıklamaları")
            self.assertIn(key, index)
            self.assertEqual(index[key]["en"], row["en"])
            self.assertEqual(index[key]["tr"], row["tr"])

    def test_v034_repeated_source_strings_stay_consistent(self):
        manifest = json.loads((TOOLS / "v034_translations.json").read_text(encoding="utf-8"))
        seen = {}
        for row in manifest["translations"]:
            if row["en"] in seen:
                self.assertEqual(seen[row["en"]], row["tr"])
            else:
                seen[row["en"]] = row["tr"])

if __name__ == "__main__":
    unittest.main()
