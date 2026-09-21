import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"

class V0312Tests(unittest.TestCase):
    def test_v0312_manifest_is_applied_exactly(self):
        manifest = json.loads((TOOLS / "v0312_translations.json").read_text(encoding="utf-8"))
        catalog = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["translation_version"], "0.31.2-beta")
        rows = manifest["translations"]
        self.assertEqual(len(rows), 27)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in rows}), 27)
        index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
        for row in rows:
            self.assertIn((row["asset"], row["pointer"]), index)
            self.assertEqual(index[(row["asset"], row["pointer"])]["en"], row["en"])
            self.assertEqual(index[(row["asset"], row["pointer"])]["tr"], row["tr"])

    def test_v0312_only_targets_active_ui(self):
        manifest = json.loads((TOOLS / "v0312_translations.json").read_text(encoding="utf-8"))
        self.assertFalse(any("_bak" in r["asset"] for r in manifest["translations"]))
        self.assertFalse(any(r["asset"] == "zb/zb_scaninteraction.questtemplate" for r in manifest["translations"]))
        self.assertFalse(any(r["pointer"] == "/gui/path/value" for r in manifest["translations"]))

if __name__ == "__main__":
    unittest.main()
