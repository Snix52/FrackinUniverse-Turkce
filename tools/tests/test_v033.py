import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rule_data import TOOLS


class V033Tests(unittest.TestCase):
    def test_v033_manifest_is_applied_exactly(self):
        manifest = json.loads((TOOLS / "v033_translations.json").read_text(encoding="utf-8"))
        catalog = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        rows = manifest["translations"]
        self.assertEqual(manifest["translation_version"], "0.33.0-beta")
        self.assertEqual(catalog["translation_version"], "0.33.0-beta")
        self.assertEqual(len(rows), 281)
        self.assertEqual({r["asset"] for r in rows}, {"interface/cockpit/cockpit.config"})
        self.assertEqual(len({r["en"] for r in rows}), 262)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in rows}), 281)
        index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
        for row in rows:
            key = (row["asset"], row["pointer"])
            self.assertIn(key, index)
            self.assertEqual(index[key]["en"], row["en"])
            self.assertEqual(index[key]["tr"], row["tr"])
            self.assertEqual(row["section"], "v0.33 cockpit ve navigasyon arayüzü")
            self.assertFalse(row["pointer"].startswith("/visitableTypeDescription/"))

    def test_v033_preserves_runtime_tokens(self):
        manifest = json.loads((TOOLS / "v033_translations.json").read_text(encoding="utf-8"))
        by_pointer = {r["pointer"]: r for r in manifest["translations"]}
        self.assertIn("%s", by_pointer["/clusterMoons/plural"]["tr"])
        self.assertIn("%i", by_pointer["/jumpDialog/invalid"]["tr"])
        self.assertIn("%i", by_pointer["/jumpDialog/valid"]["tr"])
        self.assertIn("^red;", by_pointer["/jumpDialog/invalid"]["tr"])
        self.assertIn("^green;", by_pointer["/jumpDialog/valid"]["tr"])
        self.assertIn("^reset;", by_pointer["/jumpDialog/invalid"]["tr"])
        self.assertIn("^reset;", by_pointer["/jumpDialog/valid"]["tr"])


if __name__ == "__main__":
    unittest.main()
