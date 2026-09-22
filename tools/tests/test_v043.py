import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TOOLS=ROOT/"tools"
SECTION="v0.43 canlı arayüzler"
EXCLUDED={'interface/scripted/fugravgen/fugravgenui.config', 'interface/chests/chest3.config', 'interface/kheAA/kheAA_toolforge/kheAA_toolforgegui.config', 'interface/mechstats/mechstats.config', 'interface/windowconfig/xenostation.config', 'interface/objectcrafting/fu_atmosfilter2.config', 'interface/windowconfig/craftingmech.config', 'interface/bees/industrialcentrifuge/jarringmachine.config', 'metagui/themes/frackin/theme.json', 'interface/windowconfig/fruitpress.config', 'interface/objectcrafting/fu_petnamer/fu_petnamer.config', 'interface/windowconfig/samplingarray2.config', 'interface/objectcrafting/fu_warped1.config', 'interface/objectcrafting/fu_atmosfilter3.config', 'interface/objectcrafting/fu_atmosfilter1.config', 'interface/objectcrafting/coffeemachine.config', 'interface/windowconfig/powerpress.config', 'interface/expandstation/expandstation.config', 'interface/stats/stats.config', 'interface/objectcrafting/fu_atmosfilter0.config', 'interface/objectcrafting/fu_atmosfilter5.config', 'interface/windowconfig/extractionlab.config', 'interface/objectcrafting/fu_warped3.config', 'interface/windowconfig/kitchen.config', 'metagui/themes/frackin/v2/theme.json', 'interface/objectcrafting/fu_atmosfilter4.config'}

class V043Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=json.loads((TOOLS/"v043_translations.json").read_text(encoding="utf-8"))
        cls.rows=cls.m["translations"]
        cls.by={(r["asset"],r["pointer"]):r for r in cls.rows}

    def test_scope_is_exact(self):
        self.assertEqual(self.m["translation_version"],"0.43.0-beta")
        self.assertEqual(len(self.rows),257)
        self.assertEqual(len({(r["asset"],r["pointer"]) for r in self.rows}),257)
        self.assertEqual(len({r["asset"] for r in self.rows}),69)
        self.assertEqual(len({r["en"] for r in self.rows}),156)
        self.assertTrue(all(r["section"]==SECTION for r in self.rows))
        self.assertTrue(EXCLUDED.isdisjoint({r["asset"] for r in self.rows}))

    def test_catalog_contains_manifest(self):
        catalog=json.loads((TOOLS/"ceviriler.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["translation_version"],"0.43.0-beta")
        idx={(r["asset"],r["pointer"]):r for r in catalog["translations"]}
        for row in self.rows:
            self.assertIn((row["asset"],row["pointer"]),idx)
            self.assertEqual(idx[(row["asset"],row["pointer"])]["tr"],row["tr"])

    def test_format_tokens_are_preserved(self):
        color=re.compile(r"\^[^;\s]*;")
        control=re.compile(r"\[(?![^\]]*\^)[^\]]+\]|<[^>]+>")
        printf=re.compile(r"%(?:\d+\$)?[-+0#]*(?:\d+|\*)?(?:\.\d+|\.\*)?(?:hh|h|ll|l|L|z|j|t)?[diuoxXfFeEgGaAcspn%]")
        brace=re.compile(r"\{(?:\d+|[A-Za-z_][A-Za-z0-9_.:-]*)\}")
        dollar=re.compile(r"\$(?:\{[A-Za-z_][A-Za-z0-9_.:-]*\}|[A-Za-z_][A-Za-z0-9_.:-]*)")
        for row in self.rows:
            for rx in (color,printf,brace,dollar):
                self.assertEqual(sorted(rx.findall(row["en"])),sorted(rx.findall(row["tr"])),row["asset"]+row["pointer"])
            if not row.get("qa",{}).get("allow_control_fix"):
                self.assertEqual(sorted(control.findall(row["en"])),sorted(control.findall(row["tr"])),row["asset"]+row["pointer"])
            self.assertEqual(row["en"].count("\n"),row["tr"].count("\n"),row["asset"]+row["pointer"])

    def test_locked_and_contextual_ui_choices(self):
        expected={
            ("interface/catalystfuelrefinery/refinery.config","/gui/windowtitle/title"):"  Yakıt Rafinerisi",
            ("interface/objectcrafting/fu_racialiser/fu_racialiser.config","/gui/toggleCrafting/caption"):"Irka Dönüştür",
            ("interface/scripted/fuvehiclerepair/fuvehiclerepairgui.config","/gui/repairButton/caption"):"Onar",
            ("interface/windowconfig/fucorpsewagon.config","/paneLayout/btnCraft/caption"):"Satın Al",
            ("interface/scripted/fu_upgradetable/fu_upgradetable.config","/gui/windowtitle/title"):" Yükseltme Tezgâhı",
            ("interface/mechfuelrefinery/fuelrefinery.config","/gui/windowtitle/title"):"  Yağ Damıtıcısı",
            ("interface/objectcrafting/colonystation.config","/paneLayout/windowtitle/title"):"  KOLONİ İSTASYONU",
        }
        for key,value in expected.items():
            self.assertEqual(self.by[key]["tr"],value)

    def test_loading_decoration_has_documented_control_exception(self):
        row=self.by[("interface/scripted/tunableoredetector/tunableoredetector.config","/gui/lb_currentOre/text")]
        self.assertEqual(row["tr"],"<^yellow;Yükleniyor...^reset;>")
        self.assertTrue(row.get("qa",{}).get("allow_control_fix"))

    def test_mechassembly_layered_source_is_pinned(self):
        rows=[r for r in self.rows if r["asset"]=="interface/scripted/mechassembly/mechassemblygui.config"]
        self.assertEqual(len(rows),3)
        for row in rows:
            self.assertTrue(row.get("qa",{}).get("layered_source"))
            self.assertEqual(row["qa"].get("source_patch"),"interface/scripted/mechassembly/mechassemblygui.config.patch")

    def test_signed_numbers_are_preserved(self):
        signed=re.compile(r"[+-]\s*%?\s*\d+(?:[.,]\d+)?")
        normalize=lambda values: sorted(x.replace(" ","").replace("%","").replace(",",".") for x in values)
        for row in self.rows:
            self.assertEqual(normalize(signed.findall(row["en"])),normalize(signed.findall(row["tr"])),row["asset"]+row["pointer"])

    def test_common_ui_actions(self):
        common={"Input":"Girdi","Output":"Çıktı","Drag & Drop":"Sürükle ve Bırak","Take all":"Tümünü Al","Craft":"Üret","Stop":"Durdur","Search":"Ara","Upgrade":"Yükselt","Cancel":"İptal"}
        for en,tr in common.items():
            vals={r["tr"] for r in self.rows if r["en"]==en}
            self.assertEqual(vals,{tr},en)

if __name__=="__main__":
    unittest.main()