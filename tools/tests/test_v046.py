import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit

SECTION = "v0.46 Irklar ve SAIL/AI"

class V046Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads((TOOLS / "v046_translations.json").read_text(encoding="utf-8"))
        cls.rows = cls.m["translations"]
        cls.by = {(r["asset"], r["pointer"]): r for r in cls.rows}

    def test_scope_is_exact(self):
        self.assertEqual(self.m["translation_version"], "0.46.0-beta")
        self.assertEqual(len(self.rows), 129)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in self.rows}), 129)
        self.assertEqual(len({r["asset"] for r in self.rows}), 53)
        self.assertEqual(len({r["en"] for r in self.rows}), 127)
        self.assertEqual(sum(r["asset"].startswith("ai/") for r in self.rows), 89)
        self.assertEqual(sum(r["asset"].startswith("species/") for r in self.rows), 40)
        self.assertTrue(all(r["section"] == SECTION for r in self.rows))

    def test_catalog_contains_exact_manifest(self):
        c = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        self.assertEqual(c["translation_version"], "0.46.0-beta")
        idx = {(r["asset"], r["pointer"]): r for r in c["translations"]}
        for r in self.rows:
            self.assertEqual(idx[(r["asset"], r["pointer"])]["en"], r["en"])
            self.assertEqual(idx[(r["asset"], r["pointer"])]["tr"], r["tr"])

    def test_species_runtime_scope(self):
        assets = {r["asset"] for r in self.rows if r["asset"].startswith("species/")}
        self.assertEqual(assets, set(audit.AUDIT_CORE_PLAYABLE_SPECIES_ASSETS))
        self.assertEqual(len(assets), 20)
        optional = audit.Candidate(
            "species/avali.species", "/charCreationTooltip/title", "Avali",
            "confirmed", "Irklar ve SAIL/AI", "species/avali.species", "title"
        )
        self.assertEqual(audit.v046_candidate_visibility(optional).confidence, "review")
        core = audit.Candidate(
            "species/fukirhos.species", "/charCreationTooltip/title", "Kirhos",
            "confirmed", "Irklar ve SAIL/AI", "species/fukirhos.species", "title"
        )
        self.assertEqual(audit.v046_candidate_visibility(core).confidence, "confirmed")

    def test_technical_raceeffect_labels_are_excluded(self):
        for asset, pointer in (
            ("species/irken.raceeffect", "/envEffects/0/scripts/0/args/label"),
            ("species/skelekin.raceeffect", "/liquidEffects/0/scripts/0/args/label"),
        ):
            row = audit.Candidate(
                asset, pointer, "env1", "confirmed", "Irklar ve SAIL/AI", asset, "label"
            )
            self.assertIsNone(audit.v046_candidate_visibility(row))

    def test_layered_sources_are_explicit(self):
        layered = [r for r in self.rows if r.get("qa", {}).get("layered_source")]
        self.assertEqual(len(layered), 30)
        for r in layered:
            self.assertTrue(r["qa"]["source_patch"].endswith(".patch"))

    def test_format_contracts(self):
        color = re.compile(r"\^[^;\s]*;")
        control = re.compile(r"\[(?![^\]]*\^)[^\]]+\]|<[^>]+>")
        number = re.compile(r"\d+(?:[.,]\d+)?")
        signed = re.compile(r"[+-]\s*%?\s*\d+(?:[.,]\d+)?")
        norm = lambda xs: sorted(
            x.replace(" ", "").replace("%", "").replace(",", ".") for x in xs
        )
        for r in self.rows:
            self.assertEqual(sorted(color.findall(r["en"])), sorted(color.findall(r["tr"])))
            self.assertEqual(sorted(control.findall(r["en"])), sorted(control.findall(r["tr"])))
            self.assertEqual(
                sorted(x.replace(",", ".") for x in number.findall(color.sub("", r["en"]))),
                sorted(x.replace(",", ".") for x in number.findall(color.sub("", r["tr"]))),
            )
            self.assertEqual(norm(signed.findall(r["en"])), norm(signed.findall(r["tr"])))
            self.assertEqual(r["en"].count("\n"), r["tr"].count("\n"))

    def test_reference_consistency_choices(self):
        juux = self.by[("species/juux.species", "/charCreationTooltip/description")]["tr"]
        self.assertIn("Psiyonik Odak", juux)
        self.assertNotIn("Psiyonik Fırlatıcı", juux)
        fenerox = self.by[("species/fenerox.species", "/charCreationTooltip/description")]["tr"]
        self.assertIn("Avcı Pençeleri", fenerox)
        floran = self.by[("species/floran.species", "/charCreationTooltip/description")]["tr"]
        self.assertIn("İğneleyici/Floran Silahları/Fırlatılanlar", floran)
        hylotl = self.by[("species/hylotl.species", "/charCreationTooltip/description")]["tr"]
        self.assertIn("Hylotl'lar", hylotl)

if __name__ == "__main__":
    unittest.main()
