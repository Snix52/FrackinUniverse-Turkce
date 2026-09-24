import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from build_validate import read_at, seed, simulate, translation_patch
from write_build_evidence import verified_patch_fields


class CharacterCreationRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = json.loads((ROOT / "tools/ceviriler.json").read_text(encoding="utf-8"))["translations"]
        cls.ui = [r for r in rows if r["asset"] == "interface/windowconfig/charcreation.config"]
        cls.avian = next(r for r in rows if r["asset"] == "species/avian.species"
                         and r["pointer"] == "/charCreationTooltip/description")
        cls.brain = [r for r in rows if r["asset"] ==
                     "items/active/weapons/other/brainharvester/brainharvester.activeitem"]

    def test_unrelated_ui_label_survives_one_changed_field(self):
        self.assertEqual(len(self.ui), 19)
        patch = translation_patch("interface/windowconfig/charcreation.config", self.ui)
        self.assertEqual(verified_patch_fields("charcreation.config.patch", patch), 19)
        fixture = {}
        for row in self.ui:
            seed(fixture, row["pointer"], row["en"])
        changed = "/paneLayout/mode/buttons/2/data/description"
        fixture["paneLayout"]["mode"]["buttons"][2]["data"]["description"] = "other mod text"
        result = simulate(fixture, patch)
        for row in self.ui:
            expected = "other mod text" if row["pointer"] == changed else row["tr"]
            self.assertEqual(read_at(result, row["pointer"]), expected)

    def test_species_tooltip_accepts_pinned_lf_and_steam_crlf(self):
        row = self.avian
        self.assertIn("\n", row["en"])
        patch = translation_patch(row["asset"], [row])
        self.assertEqual(len(patch), 2)
        self.assertEqual(verified_patch_fields("avian.species.patch", patch), 1)
        for source in (row["en"], row["en"].replace("\n", "\r\n")):
            fixture = {}
            seed(fixture, row["pointer"], source)
            self.assertEqual(read_at(simulate(fixture, patch), row["pointer"]), row["tr"])

    def test_package_rejects_unreviewed_source_variant(self):
        patch = translation_patch(self.avian["asset"], [self.avian])
        patch[1][0]["value"] = "different source text"
        with self.assertRaisesRegex(ValueError, "Invalid line-ending source variant"):
            verified_patch_fields("avian.species.patch", patch)

    def test_other_multiline_asset_accepts_steam_crlf_and_keeps_name(self):
        self.assertEqual(len(self.brain), 2)
        asset = self.brain[0]["asset"]
        patch = translation_patch(asset, self.brain)
        self.assertEqual(verified_patch_fields(asset + ".patch", patch), 2)
        fixture = {}
        for row in self.brain:
            source = row["en"].replace("\n", "\r\n")
            seed(fixture, row["pointer"], source)
        result = simulate(fixture, patch)
        for row in self.brain:
            self.assertEqual(read_at(result, row["pointer"]), row["tr"])

    def test_reviewed_mixed_line_endings_apply_without_dropping_name(self):
        asset = "items/active/weapons/ranged/unique/futriangliumpistol.activeitem"
        rows = [r for r in json.loads((ROOT / "tools/ceviriler.json").read_text(encoding="utf-8"))["translations"]
                if r["asset"] == asset]
        description = next(r for r in rows if r["pointer"] == "/description")
        self.assertEqual(description["qa"]["source_newline_pattern"], "LC")
        parts = description["en"].split("\n")
        self.assertEqual(len(parts), 3)
        mixed = parts[0] + "\n" + parts[1] + "\r\n" + parts[2]
        fixture = {}
        for row in rows:
            seed(fixture, row["pointer"], mixed if row is description else row["en"])
        patch = translation_patch(asset, rows)
        self.assertEqual(verified_patch_fields(asset + ".patch", patch), 2)
        result = simulate(fixture, patch)
        self.assertEqual(read_at(result, "/description"), description["tr"])
        self.assertEqual(read_at(result, "/shortdescription"), "Şovbozan")

    def test_mismatch_in_one_field_does_not_suppress_its_neighbor(self):
        asset = "items/generic/produce/orange.consumable"
        rows = [r for r in json.loads((ROOT / "tools/ceviriler.json").read_text(encoding="utf-8"))["translations"]
                if r["asset"] == asset]
        self.assertEqual(len(rows), 2)
        fixture = {}
        for row in rows:
            seed(fixture, row["pointer"], row["en"])
        fixture["description"] = "changed by another mod"
        result = simulate(fixture, translation_patch(asset, rows))
        self.assertEqual(result["description"], "changed by another mod")
        self.assertEqual(result["shortdescription"], "Portakal")


if __name__ == "__main__":
    unittest.main()
