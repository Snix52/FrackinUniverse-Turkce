import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
TOOLS=ROOT/"tools"
SECTION="v0.44 arayüz kapanışı"
DEAD=["interface/bees/industrialcentrifuge/jarringmachine.config","interface/expandstation/expandstation.config","interface/kheAA/kheAA_toolforge/kheAA_toolforgegui.config","interface/mechstats/mechstats.config","interface/objectcrafting/coffeemachine.config","interface/objectcrafting/fu_atmosfilter0.config","interface/objectcrafting/fu_atmosfilter2.config","interface/objectcrafting/fu_atmosfilter3.config","interface/objectcrafting/fu_atmosfilter4.config","interface/objectcrafting/fu_atmosfilter5.config","interface/objectcrafting/fu_petnamer/fu_petnamer.config","interface/scripted/fugravgen/fugravgenui.config","interface/windowconfig/craftingmech.config","interface/windowconfig/extractionlab.config","interface/windowconfig/fruitpress.config","interface/windowconfig/kitchen.config","interface/windowconfig/powerpress.config","interface/windowconfig/samplingarray2.config","interface/windowconfig/xenostation.config"]
TODO=["/darkregen/description","/fuCharisma/description","/lightregen/description","/upgradeable/description"]
class V044Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=json.loads((TOOLS/"v044_translations.json").read_text(encoding="utf-8")); cls.rows=cls.m["translations"]; cls.by={(r["asset"],r["pointer"]):r for r in cls.rows}
    def test_scope_is_exact(self):
        self.assertEqual(self.m["translation_version"],"0.44.0-beta"); self.assertEqual(len(self.rows),13); self.assertEqual(len({(r["asset"],r["pointer"]) for r in self.rows}),13); self.assertEqual(len({r["asset"] for r in self.rows}),7); self.assertEqual(len({r["en"] for r in self.rows}),12); self.assertTrue(all(r["section"]==SECTION for r in self.rows)); self.assertTrue(set(DEAD).isdisjoint({r["asset"] for r in self.rows}))
    def test_catalog_contains_manifest(self):
        c=json.loads((TOOLS/"ceviriler.json").read_text(encoding="utf-8")); self.assertGreaterEqual(tuple(map(int,c["translation_version"].split("-")[0].split("."))),(0,44,0)); idx={(r["asset"],r["pointer"]):r for r in c["translations"]}
        for r in self.rows: self.assertEqual(idx[(r["asset"],r["pointer"])]["tr"],r["tr"])
    def test_runtime_closure_choices(self):
        e={("interface/chests/chest3.config","/gui/count/value"):"3 YUVA",("interface/objectcrafting/fu_atmosfilter1.config","/gui/lblText/value"):"^#b9b5b2;Eklentileri yuvalara yerleştir. Etkileri menzil içinde uygulanır.",("interface/stats/stats.config","/fuCharisma/label"):"Karizma",("interface/stats/stats.config","/upgradeable/label"):"Yükseltilebilir",("metagui/themes/frackin/theme.json","/name"):"Frackin' Klasik",("metagui/themes/frackin/v2/theme.json","/name"):"Frackin' Standart"}
        for k,v in e.items(): self.assertEqual(self.by[k]["tr"],v)
    def test_warped_unknown_markers_are_preserved(self):
        for a in ("interface/objectcrafting/fu_warped1.config","interface/objectcrafting/fu_warped3.config"):
            r=self.by[(a,"/gui/lblText/value")]; self.assertEqual(r["en"].count("???"),2); self.assertEqual(r["tr"].count("???"),2)
    def test_stats_layered_source_is_documented(self):
        rs=[r for r in self.rows if r["asset"]=="interface/stats/stats.config"]; self.assertEqual(len(rs),4)
        for r in rs: self.assertTrue(r.get("qa",{}).get("layered_source")); self.assertEqual(r["qa"].get("source_patch"),"interface/stats/stats.config.patch")
    def test_dead_and_dev_placeholders_are_audit_excluded(self):
        rules=json.loads((TOOLS/"rules"/"dead_assets.json").read_text(encoding="utf-8"))["rules"]; self.assertTrue(set(DEAD).issubset(set(rules["AUDIT_EXCLUDED_PATHS"]["value"]))); self.assertTrue(set(TODO).issubset(set(rules["AUDIT_EXCLUDED_FIELDS"]["value"]["interface/stats/stats.config"])))
    def test_format_tokens_are_preserved(self):
        color=re.compile(r"\^[^;\s]*;")
        for r in self.rows: self.assertEqual(sorted(color.findall(r["en"])),sorted(color.findall(r["tr"])),r["asset"]+r["pointer"]); self.assertEqual(r["en"].count("\n"),r["tr"].count("\n"),r["asset"]+r["pointer"])
if __name__=="__main__": unittest.main()
