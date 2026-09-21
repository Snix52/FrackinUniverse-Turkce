import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];TOOLS=ROOT/"tools"
ASSET="interface/kheAA/kheAA_router/kheAA_routerGui.config";LUA_ASSET="interface/kheAA/kheAA_router/kheAA_routerGui.lua"
class V037Tests(unittest.TestCase):
    def test_manifest_is_applied_exactly(self):
        m=json.loads((TOOLS/"v037_translations.json").read_text(encoding="utf-8"));c=json.loads((TOOLS/"ceviriler.json").read_text(encoding="utf-8"));rows=m["translations"]
        self.assertEqual(m["translation_version"],"0.37.0-beta");self.assertEqual(len(rows),35);self.assertEqual(len({r["en"] for r in rows}),18);self.assertEqual({r["asset"] for r in rows},{ASSET})
        idx={(r["asset"],r["pointer"]):r for r in c["translations"]}
        for r in rows:self.assertEqual(idx[(r["asset"],r["pointer"])]["tr"],r["tr"])
    def test_structured_scope_excludes_runtime_templates(self):
        ps={r["pointer"] for r in json.loads((TOOLS/"v037_translations.json").read_text(encoding="utf-8"))["translations"]}
        self.assertNotIn("/gui/filterFunctionsLabel/value",ps);self.assertNotIn("/gui/filterFunctionsLabel2/value",ps);self.assertFalse(any("slotNr" in p for p in ps))
        self.assertEqual(sum(bool(re.fullmatch(r"/gui/item[1-5](ButtonInvert/caption|Label/value|Label(Category|Exact|Type)/value)",p)) for p in ps),25)
    def test_help_mode_raw_strings_are_complete(self):
        raw=json.loads((TOOLS/"raw_text_translations.json").read_text(encoding="utf-8"));spec=next(x for x in raw["assets"] if x["asset"]==LUA_ASSET)
        self.assertEqual(len(spec["replacements"]),20);self.assertEqual(len({r["old"] for r in spec["replacements"]}),20);self.assertTrue(all(r["expected_count"]==1 for r in spec["replacements"]))
        trs={r["display_tr"] for r in spec["replacements"]};self.assertIn("İşlevler: Otomasyonda çıktıları bölmek için bunları kullan.",trs);self.assertIn("'T' düğmeleri: ilgili taraftaki yuva filtresi seçimini tersine çevirir.",trs)
if __name__=="__main__":unittest.main()
