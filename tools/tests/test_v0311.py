import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"

class V0311Tests(unittest.TestCase):
    def test_v0311_manifest_is_applied_exactly(self):
        manifest = json.loads((TOOLS / "v0311_translations.json").read_text(encoding="utf-8"))
        catalog = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["translation_version"], "0.31.1-beta")
        rows = manifest["translations"]
        self.assertEqual(len(rows), 26)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in rows}), 26)
        index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
        for row in rows:
            self.assertIn((row["asset"], row["pointer"]), index)
            self.assertEqual(index[(row["asset"], row["pointer"])]["en"], row["en"])
            self.assertEqual(index[(row["asset"], row["pointer"])]["tr"], row["tr"])

    def test_v0311_scope_is_quest_terminal_only(self):
        manifest = json.loads((TOOLS / "v0311_translations.json").read_text(encoding="utf-8"))
        allowed = {"zb/questList/data.config", "zb/questList/questList.config"}
        for row in manifest["translations"]:
            self.assertIn(row["asset"], allowed)
            self.assertEqual(row["section"], "v0.31.1 Görev Terminali arayüzü")

if __name__ == "__main__":
    unittest.main()
