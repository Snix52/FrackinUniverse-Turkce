import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"

class V031Tests(unittest.TestCase):
    def test_v031_manifest_is_applied_exactly(self):
        manifest = json.loads((TOOLS / "v031_translations.json").read_text(encoding="utf-8"))
        catalog = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["translation_version"], "0.31.0-beta")
        self.assertEqual(catalog["translation_version"], "0.31.0-beta")
        rows = manifest["translations"]
        self.assertEqual(len(rows), 89)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in rows}), 89)
        index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
        for row in rows:
            self.assertIn((row["asset"], row["pointer"]), index)
            self.assertEqual(index[(row["asset"], row["pointer"])]["en"], row["en"])
            self.assertEqual(index[(row["asset"], row["pointer"])]["tr"], row["tr"])

    def test_v031_scope_is_player_visible_ui(self):
        manifest = json.loads((TOOLS / "v031_translations.json").read_text(encoding="utf-8"))
        allowed_assets = {
            "zb/newSail/data.config", "zb/newSail/newSail.config",
            "interface/ai/ai.config", "interface/ai/fu_byosai.config",
            "fu_metagui/settings/settings.ui",
        }
        for row in manifest["translations"]:
            self.assertIn(row["asset"], allowed_assets)
            self.assertNotIn("/path", row["pointer"].lower())
            self.assertNotIn("/callback", row["pointer"].lower())
            self.assertEqual(row["section"], "v0.31 SAIL ve gemi arayüzü")

if __name__ == "__main__":
    unittest.main()
