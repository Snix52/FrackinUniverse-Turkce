import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
ASSET = "interface/shipnameplate/fu_shipnameplate.config"

class V036Tests(unittest.TestCase):
    def test_v036_manifest_is_applied_exactly(self):
        manifest = json.loads((TOOLS / "v036_translations.json").read_text(encoding="utf-8"))
        catalog = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        rows = manifest["translations"]
        self.assertEqual(manifest["translation_version"], "0.36.0-beta")
        self.assertEqual(len(rows), 36)
        self.assertEqual(len({r["en"] for r in rows}), 36)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in rows}), 36)
        self.assertEqual({r["asset"] for r in rows}, {ASSET})
        index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
        for row in rows:
            key = (row["asset"], row["pointer"])
            self.assertIn(key, index)
            self.assertEqual(index[key]["en"], row["en"])
            self.assertEqual(index[key]["tr"], row["tr"])
            self.assertEqual(row["section"], "v0.36 gemi isim plakası arayüzü")

    def test_v036_scope_contains_only_live_nameplate_text(self):
        manifest = json.loads((TOOLS / "v036_translations.json").read_text(encoding="utf-8"))
        pointers = {r["pointer"] for r in manifest["translations"]}
        self.assertIn("/gui/windowtitle/title", pointers)
        self.assertIn("/gui/windowtitle/subtitle", pointers)
        self.assertIn("/gui/btnAccept/caption", pointers)
        self.assertIn("/gui/lblName/value", pointers)
        self.assertIn("/gui/label2/value", pointers)
        self.assertIn("/gui/tboxName/hint", pointers)
        self.assertEqual(sum(bool(re.fullmatch(r"/shipTypes/\\d+", p)) for p in pointers), 30)
        self.assertNotIn("/gui/lblType/value", pointers)
        self.assertNotIn("/gui/lblDate/value", pointers)
        self.assertFalse(any("/callback" in p or "/file" in p or "/scripts" in p for p in pointers))

    def test_v036_locked_shared_terms(self):
        manifest = json.loads((TOOLS / "v036_translations.json").read_text(encoding="utf-8"))
        by_en = {r["en"]: r["tr"] for r in manifest["translations"]}
        self.assertEqual(by_en["Accept"], "Kabul Et")
        self.assertEqual(by_en["Unknown"], "Bilinmiyor")

if __name__ == "__main__":
    unittest.main()
