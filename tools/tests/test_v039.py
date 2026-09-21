import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
ASSET = "interface/scripted/statWindow/statWindow.config"
LUA_ASSET = "interface/scripted/statWindow/statWindow.lua"

class V039Tests(unittest.TestCase):
    def test_manifest_is_applied_exactly(self):
        m = json.loads((TOOLS / "v039_translations.json").read_text(encoding="utf-8"))
        c = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        rows = m["translations"]
        self.assertEqual(m["translation_version"], "0.39.0-beta")
        self.assertEqual(len(rows), 57)
        self.assertEqual(len({r["en"] for r in rows}), 56)
        self.assertEqual({r["asset"] for r in rows}, {ASSET})
        idx = {(r["asset"],r["pointer"]):r for r in c["translations"]}
        for r in rows:
            self.assertIn((r["asset"],r["pointer"]), idx)
            self.assertEqual(idx[(r["asset"],r["pointer"])]["tr"], r["tr"])

    def test_scope_is_ui_and_status_names(self):
        rows = json.loads((TOOLS / "v039_translations.json").read_text(encoding="utf-8"))["translations"]
        ps = {r["pointer"] for r in rows}
        self.assertEqual(sum(p.startswith("/statuses/") and p.endswith("/name") for p in ps), 44)
        self.assertEqual(sum(p.startswith("/gui/") for p in ps), 13)
        self.assertFalse(any(p.startswith("/races/") or p.startswith("/elements/") for p in ps))
        self.assertFalse(any("/callback" in p for p in ps))

    def test_locked_terms_and_colors(self):
        rows = json.loads((TOOLS / "v039_translations.json").read_text(encoding="utf-8"))["translations"]
        by = {r["en"]:r["tr"] for r in rows}
        self.assertEqual(by["Research"], "Araştırma")
        self.assertEqual(by[" ^#00eaff;Personal Tricorder^reset;"], " ^#00eaff;Kişisel Tricorder^reset;")
        self.assertEqual(by["^#4BF3FD;Moderate Cold"], "^#4BF3FD;Orta Dereceli Soğuk")
        self.assertEqual(by["^yellow;Moderate Radiation"], "^yellow;Orta Dereceli Radyasyon")
        self.assertEqual(by["^#78f04f;Proto-Poison"], "^#78f04f;Proto-Zehir")
        self.assertEqual(by["^yellow;Pus"], "^yellow;İrin")
        self.assertEqual(by["^#3F2E4D;Shadow Taint"], "^#3F2E4D;Gölge Lekesi")

    def test_research_menu_context_is_explicit(self):
        locked = json.loads((TOOLS / "locked_terms.json").read_text(encoding="utf-8"))
        matches = [
            x for x in locked.get("context_exceptions", [])
            if x.get("asset") == ASSET
            and x.get("pointer") == "/gui/expandButton1Label/value"
        ]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["en"], "Research")
        self.assertEqual(matches[0]["tr"], "Araştırma")
        self.assertTrue(matches[0]["reason"].strip())

    def test_runtime_racial_strings_are_translated(self):
        raw = json.loads((TOOLS / "raw_text_translations.json").read_text(encoding="utf-8"))
        spec = next(x for x in raw["assets"] if x["asset"] == LUA_ASSET)
        self.assertEqual(len(spec["replacements"]), 3)
        trs = {r["display_tr"] for r in spec["replacements"]}
        self.assertIn("TANINMAYAN IRK", trs)
        self.assertIn("Irk Özellikleri - ", trs)

if __name__ == "__main__":
    unittest.main()
