import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import audit_remaining as audit
from rule_data import TOOLS, rule as load_rule


class V032Tests(unittest.TestCase):
    def test_machine_scope_false_positives_stay_excluded(self):
        self.assertIsNone(audit.visible_confidence("objects/test/test.object", ["category"], "crafting"))
        self.assertEqual(
            audit.visible_confidence("objects/test/test.object", ["category"], "^orange;Extraction Device^reset;"),
            "confirmed",
        )
        self.assertIsNone(audit.visible_confidence("objects/test/test.object", ["tooltip"], "base"))
        self.assertIsNone(audit.visible_confidence("objects/test/test.object", ["gui", "value"], "Replace Me"))
        self.assertIsNone(
            audit.visible_confidence(
                "objects/test/test.object",
                ["gui", "listTemplate", "level", "value"],
                "Lvl. 100",
            )
        )

    def test_nested_item_assets_are_not_machine_category(self):
        self.assertEqual(
            audit.category_for("objects/crafting/eggstra/items/primedegg.consumable"),
            "Malzeme, tüketilebilir ve diğer eşyalar",
        )
        self.assertEqual(
            audit.category_for("objects/crafting/example/example.object"),
            "Makineler, üretim ve dükkân nesneleri",
        )

    def test_machine_audit_exclusions_are_narrow_and_machine_readable(self):
        technical = load_rule("AUDIT_TECHNICAL_CATEGORY_VALUES")
        excluded = load_rule("AUDIT_EXCLUDED_PATHS")
        dead = load_rule("V018_DEAD_OBJECT_ASSETS")
        self.assertIn("crafting", technical)
        self.assertIn("wire", technical)
        self.assertIn("objects/power/fu_atmosfilter/warpedItemList.json", excluded)
        self.assertIn("objects/power/fu_upgrade/fu_upgrade.object", dead)
        append_indexes = load_rule("AUDIT_PATCH_APPEND_INDEXES")
        self.assertEqual(
            append_indexes["objects/crafting/upgradeablecraftingobjects/craftingwheel/craftingwheel.object"],
            2,
        )

    def test_v032_manifest_is_applied_exactly(self):
        manifest = json.loads((TOOLS / "v032_translations.json").read_text(encoding="utf-8"))
        catalog = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        rows = manifest["translations"]
        self.assertEqual(manifest["translation_version"], "0.32.0-beta")
        self.assertEqual(len(rows), 107)
        self.assertEqual(len({r["asset"] for r in rows}), 38)
        self.assertEqual(len({r["en"] for r in rows}), 76)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in rows}), 107)
        index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
        dead = load_rule("V018_DEAD_OBJECT_ASSETS")
        excluded = load_rule("AUDIT_EXCLUDED_PATHS")
        for row in rows:
            key = (row["asset"], row["pointer"])
            self.assertIn(key, index)
            self.assertEqual(index[key]["en"], row["en"])
            self.assertEqual(index[key]["tr"], row["tr"])
            self.assertEqual(row["section"], "v0.32 makine, üretim ve dükkân arayüzü")
            self.assertNotIn(row["asset"], dead)
            self.assertNotIn(row["asset"], excluded)

if __name__ == "__main__":
    unittest.main()
