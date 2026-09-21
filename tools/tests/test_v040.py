import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TOOLS=ROOT/"tools"
ASSET="interface/windowconfig/charcreation.config"

class V040Tests(unittest.TestCase):
    def test_manifest_is_applied_exactly(self):
        m=json.loads((TOOLS/"v040_translations.json").read_text(encoding="utf-8"))
        c=json.loads((TOOLS/"ceviriler.json").read_text(encoding="utf-8"))
        rows=m["translations"]
        self.assertEqual(m["translation_version"],"0.40.0-beta")
        self.assertEqual(len(rows),19)
        self.assertEqual(len({r["en"] for r in rows}),18)
        self.assertEqual({r["asset"] for r in rows},{ASSET})
        idx={(r["asset"],r["pointer"]):r for r in c["translations"]}
        for r in rows:
            self.assertIn((r["asset"],r["pointer"]),idx)
            self.assertEqual(idx[(r["asset"],r["pointer"])]["tr"],r["tr"])
            self.assertEqual(r["section"],"v0.40 karakter oluşturma arayüzü")

    def test_runtime_portrait_template_stays_out(self):
        ps={r["pointer"] for r in json.loads((TOOLS/"v040_translations.json").read_text(encoding="utf-8"))["translations"]}
        self.assertNotIn("/paneLayout/labelPortrait/value",ps)
        self.assertIn("/paneLayout/labelSpeciesRadio/value",ps)
        self.assertIn("/paneLayout/labelSpeciesRadio2/value",ps)
        self.assertIn("/paneLayout/mode/buttons/0/data/description",ps)
        self.assertIn("/paneLayout/mode/buttons/1/data/description",ps)
        self.assertIn("/paneLayout/mode/buttons/2/data/description",ps)

    def test_shared_ui_terms_and_colors(self):
        rows=json.loads((TOOLS/"v040_translations.json").read_text(encoding="utf-8"))["translations"]
        by={r["en"]:r["tr"] for r in rows}
        self.assertEqual(by["Cancel"],"İptal")
        self.assertEqual(by["Name"],"Ad")
        self.assertEqual(by["^#8d8d8d;SPECIES"],"^#8d8d8d;IRK")
        self.assertEqual(by["^#8d8d8d;DIFFICULTY"],"^#8d8d8d;ZORLUK")
        self.assertEqual(by["Done"],"Tamam")

if __name__=="__main__":
    unittest.main()
