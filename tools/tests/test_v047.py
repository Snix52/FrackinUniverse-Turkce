import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit

SECTION = "v0.47 bitkiler"

class V047Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads((TOOLS / "v047_translations.json").read_text(encoding="utf-8"))
        cls.rows = cls.m["translations"]
        cls.by = {(r["asset"], r["pointer"]): r for r in cls.rows}

    def test_scope_is_exact(self):
        self.assertEqual(self.m["translation_version"], "0.47.0-beta")
        self.assertEqual(len(self.rows), 170)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in self.rows}), 170)
        self.assertEqual(len({r["asset"] for r in self.rows}), 66)
        self.assertEqual(len({r["en"] for r in self.rows}), 110)
        self.assertTrue(all(r["asset"].startswith("plants/") for r in self.rows))
        self.assertEqual(
            {r["pointer"] for r in self.rows},
            {"/description", "/shortdescription", "/floranDescription", "/glitchDescription"},
        )
        self.assertTrue(all(r["section"] == SECTION for r in self.rows))

    def test_catalog_contains_exact_manifest(self):
        c = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(
            tuple(map(int, c["translation_version"].split("-")[0].split("."))),
            (0, 47, 0),
        )
        idx = {(r["asset"], r["pointer"]): r for r in c["translations"]}
        for r in self.rows:
            self.assertEqual(idx[(r["asset"], r["pointer"])]["en"], r["en"])
            self.assertEqual(idx[(r["asset"], r["pointer"])]["tr"], r["tr"])

    def test_liquid_config_descriptions_are_not_translation_debt(self):
        self.assertIn("/description", audit.AUDIT_EXCLUDED_FIELDS["liquids/"])
        self.assertTrue(audit.audit_excluded_candidate("liquids/blood.liquid", "/description"))
        self.assertFalse(audit.audit_excluded_candidate(
            "items/liquids/liquidblood.liqitem", "/description"
        ))
        self.assertFalse(any(r["asset"].startswith("liquids/") for r in self.rows))

    def test_project_terminology_and_character_tone(self):
        self.assertEqual(
            self.by[("plants/grass/ground/decorative/aethersea/aethergrass.grass", "/shortdescription")]["tr"],
            "Aether Yosunu",
        )
        self.assertEqual(
            self.by[("plants/grass/ground/decorative/bloodstoneplant/bloodstoneplant.grass", "/shortdescription")]["tr"],
            "Kan Taşı Filizi",
        )
        self.assertEqual(
            self.by[("plants/grass/ground/decorative/rainforestgrasses/rainforestgrasses.grass", "/shortdescription")]["tr"],
            "Yağmur Ormanı Çimleri",
        )
        self.assertEqual(
            self.by[("plants/grass/ground/decorative/sulphurpebbles/sulphurpebbles.grass", "/shortdescription")]["tr"],
            "Kükürtlü çakıllar.",
        )
        self.assertIn(
            "Gelgit Suları",
            self.by[("plants/grass/ground/decorative/tidewatergrass/tidewatergrass.grass", "/description")]["tr"],
        )
        self.assertTrue(
            self.by[("plants/bushes/ground/buglike/buglike.bush", "/floranDescription")]["tr"].count("ş") >= 3
        )
        self.assertTrue(
            self.by[("plants/bushes/ground/buglike/buglike.bush", "/glitchDescription")]["tr"].startswith("Merak.")
        )

    def test_format_contracts(self):
        color = re.compile(r"\^[^;\s]*;")
        control = re.compile(r"\[(?![^\]]*\^)[^\]]+\]|<[^>]+>")
        number = re.compile(r"\d+(?:[.,]\d+)?")
        for r in self.rows:
            self.assertEqual(sorted(color.findall(r["en"])), sorted(color.findall(r["tr"])))
            self.assertEqual(sorted(control.findall(r["en"])), sorted(control.findall(r["tr"])))
            self.assertEqual(
                sorted(x.replace(",", ".") for x in number.findall(color.sub("", r["en"]))),
                sorted(x.replace(",", ".") for x in number.findall(color.sub("", r["tr"]))),
            )
            self.assertEqual(r["en"].count("\n"), r["tr"].count("\n"))

if __name__ == "__main__":
    unittest.main()
