import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TOOLS=ROOT/"tools"
SECTION="v0.42 işlevsel arayüzler ve Pet House"
PET="interface/objectcrafting/fu_pethouse/fu_pethouse.config"
PET_CONFIRM="interface/objectcrafting/fu_pethouse/fu_pethouse_confirmation.config"
PET_LUA="interface/objectcrafting/fu_pethouse/fu_pethouse.lua"
DEAD={
"interface/windowconfig/craftingmech.config",
"interface/windowconfig/extractionlab.config",
"interface/windowconfig/fruitpress.config",
"interface/windowconfig/kitchen.config",
"interface/windowconfig/powerpress.config",
"interface/windowconfig/samplingarray2.config",
"interface/windowconfig/xenostation.config",
}

class V042Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=json.loads((TOOLS/"v042_translations.json").read_text(encoding="utf-8"))
        cls.rows=cls.m["translations"]
        cls.by={(r["asset"],r["pointer"]):r for r in cls.rows}

    def test_scope_is_exact(self):
        self.assertEqual(self.m["translation_version"],"0.42.0-beta")
        self.assertEqual(len(self.rows),260)
        self.assertEqual(len({(r["asset"],r["pointer"]) for r in self.rows}),260)
        self.assertEqual(len({r["asset"] for r in self.rows}),46)
        self.assertTrue(all(r["section"]==SECTION for r in self.rows))
        counts=Counter(r["asset"] for r in self.rows)
        self.assertEqual(counts[PET],16)
        self.assertEqual(counts[PET_CONFIRM],5)
        self.assertTrue(DEAD.isdisjoint(counts))

    def test_pet_house_manual_runtime_fields_are_present(self):
        required={
            "/popupMessages/noPod",
            "/popupMessages/captureFail",
            "/popupMessages/petMissing",
            "/popupMessages/invalidTechstation",
            "/interactionTypes/0/name",
            "/interactionTypes/1/name",
            "/interactionTypes/2/name",
        }
        actual={r["pointer"] for r in self.rows if r["asset"]==PET}
        self.assertTrue(required.issubset(actual))
        self.assertEqual(self.by[(PET,"/gui/title/title")]["tr"],"Evcil Hayvan Ayarları")
        self.assertEqual(self.by[(PET,"/gui/capturePet/caption")]["tr"],"Kapsülle Yakala")

    def test_format_tokens_are_preserved(self):
        color=re.compile(r"\^[^;\s]*;")
        control=re.compile(r"\[(?![^\]]*\^)[^\]]+\]|<[^>]+>")
        printf=re.compile(r"%(?:\d+\$)?[-+0#]*(?:\d+|\*)?(?:\.\d+|\.\*)?(?:hh|h|ll|l|L|z|j|t)?[diuoxXfFeEgGaAcspn%]")
        brace=re.compile(r"\{(?:\d+|[A-Za-z_][A-Za-z0-9_.:-]*)\}")
        dollar=re.compile(r"\$(?:\{[A-Za-z_][A-Za-z0-9_.:-]*\}|[A-Za-z_][A-Za-z0-9_.:-]*)")
        for row in self.rows:
            for rx in (color,control,printf,brace,dollar):
                self.assertEqual(sorted(rx.findall(row["en"])),sorted(rx.findall(row["tr"])),row["asset"]+row["pointer"])
            self.assertEqual(row["en"].count("\n"),row["tr"].count("\n"),row["asset"]+row["pointer"])

    def test_core_actions_and_contexts(self):
        self.assertEqual(self.by[("interface/windowconfig/armory.config","/paneLayout/btnCraft/caption")]["tr"],"Üret")
        self.assertEqual(self.by[("interface/windowconfig/fuburgerfool.config","/paneLayout/btnCraft/caption")]["tr"],"Satın Al")
        self.assertEqual(self.by[("interface/windowconfig/craftingcrewshop.config","/paneLayout/btnCraft/caption")]["tr"],"İşe Al")
        self.assertEqual(self.by[("interface/windowconfig/fu_anvil.config","/paneLayout/btnCraft/caption")]["tr"],"Birleştir")\n        self.assertEqual(self.by[("interface/windowconfig/craftingslimecentrifuge.config","/paneLayout/btnCraft/caption")]["tr"],"Döv")
        self.assertEqual(self.by[("interface/windowconfig/fissionfurnace.config","/paneLayout/btnCraft/caption")]["tr"],"Ergit")
        self.assertEqual(self.by[("interface/windowconfig/mash.config","/paneLayout/btnCraft/caption")]["tr"],"Mayşele")
        self.assertEqual(self.by[("interface/windowconfig/distill.config","/paneLayout/btnCraft/caption")]["tr"],"Damıt")
        self.assertEqual(self.by[("interface/windowconfig/ferment.config","/paneLayout/btnCraft/caption")]["tr"],"Fermente Et")

    def test_linked_object_names_stay_aligned(self):
        expected={
            ("interface/windowconfig/fufoodstore.config","/paneLayout/lblTitle/value"):" Murder-Twig'in Lezzetleri",
            ("interface/windowconfig/fugemshop.config","/paneLayout/lblTitle/value"):" Ruhun Mücevherleri",
            ("interface/windowconfig/gemstation.config","/paneLayout/lblTitle/value"):" Kristal Füzyon İstasyonu",
            ("interface/windowconfig/kirhosshop.config","/paneLayout/lblTitle/value"):" Lorewalker'ın Dükkânı",
            ("interface/windowconfig/platingfood.config","/paneLayout/windowtitle/title"):" Sunum Tezgâhı",
            ("interface/windowconfig/medievalworkstation.config","/paneLayout/windowtitle/title"):"  ORTA ÇAĞ ÇALIŞMA İSTASYONU",
            ("interface/windowconfig/radienshop.config","/paneLayout/lblTitle/value"):" Silene'nin Mineralleri",
        }
        for key,value in expected.items():
            self.assertEqual(self.by[key]["tr"],value)

    def test_pet_house_lua_is_source_locked(self):
        raw=json.loads((TOOLS/"raw_text_translations.json").read_text(encoding="utf-8"))
        spec=next(x for x in raw["assets"] if x["asset"]==PET_LUA)
        self.assertEqual(spec["source_blob_sha"],"caf30e8c3d6816984f0ea46f3486bf1942038c65")
        self.assertEqual(len(spec["replacements"]),1)
        r=spec["replacements"][0]
        self.assertEqual(int(r.get("expected_count",1)),1)
        self.assertIn("Çağırdığı evcil hayvan:",r["new"])
        self.assertIn("shipPetType",r["new"])

if __name__=="__main__":
    unittest.main()
