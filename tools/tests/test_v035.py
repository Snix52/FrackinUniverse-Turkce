import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
ASSET = "interface/scripted/fu_matmodplacer/fu_matmodplacer.config"

class V035Tests(unittest.TestCase):
    def test_v035_manifest_is_applied_exactly(self):
        manifest = json.loads((TOOLS / "v035_translations.json").read_text(encoding="utf-8"))
        catalog = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        rows = manifest["translations"]
        self.assertEqual(manifest["translation_version"], "0.35.0-beta")
        self.assertEqual(len(rows), 263)
        self.assertEqual(len({r["en"] for r in rows}), 259)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in rows}), 263)
        self.assertEqual({r["asset"] for r in rows}, {ASSET})
        index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
        for row in rows:
            key = (row["asset"], row["pointer"])
            self.assertIn(key, index)
            self.assertEqual(index[key]["en"], row["en"])
            self.assertEqual(index[key]["tr"], row["tr"])
            self.assertEqual(row["section"], "v0.35 malzeme modu yerleştirici arayüzü")

    def test_v035_scope_excludes_technical_matmod_fields(self):
        manifest = json.loads((TOOLS / "v035_translations.json").read_text(encoding="utf-8"))
        pointers = {r["pointer"] for r in manifest["translations"]}
        self.assertIn("/gui/windowtitle/title", pointers)
        self.assertIn("/gui/windowtitle/subtitle", pointers)
        self.assertIn("/gui/filter/hint", pointers)
        self.assertEqual(sum(bool(re.fullmatch(r"/matMods/\d+/name", p)) for p in pointers), 130)
        self.assertEqual(sum(bool(re.fullmatch(r"/matMods/\d+/description", p)) for p in pointers), 130)
        self.assertFalse(any(re.fullmatch(r"/matMods/\d+/(matMod|category)", p) for p in pointers))
        self.assertFalse(any("/callback" in p or "/file" in p or "/base" in p or "/hover" in p or "/press" in p for p in pointers))

    def test_v035_repeated_sources_are_consistent(self):
        manifest = json.loads((TOOLS / "v035_translations.json").read_text(encoding="utf-8"))
        seen = {}
        for row in manifest["translations"]:
            if row["en"] in seen:
                self.assertEqual(seen[row["en"]], row["tr"])
            else:
                seen[row["en"]] = row["tr"]

if __name__ == "__main__":
    unittest.main()
