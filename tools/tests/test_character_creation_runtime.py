import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from build_validate import read_at, seed, simulate, translation_patch


class CharacterCreationRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = json.loads((ROOT / "tools/ceviriler.json").read_text(encoding="utf-8"))["translations"]
        cls.ui = [r for r in rows if r["asset"] == "interface/windowconfig/charcreation.config"]
        cls.avian = next(r for r in rows if r["asset"] == "species/avian.species"
                         and r["pointer"] == "/charCreationTooltip/description")

    def test_unrelated_ui_label_survives_one_changed_field(self):
        self.assertEqual(len(self.ui), 19)
        patch = translation_patch("interface/windowconfig/charcreation.config", self.ui)
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
        for source in (row["en"], row["en"].replace("\n", "\r\n")):
            fixture = {}
            seed(fixture, row["pointer"], source)
            self.assertEqual(read_at(simulate(fixture, patch), row["pointer"]), row["tr"])


if __name__ == "__main__":
    unittest.main()
