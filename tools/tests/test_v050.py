import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
from qa_integrity import validate_format


class V050Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((TOOLS / "v050_translations.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        cls.rows = cls.manifest["translations"]
        cls.by = {(row["asset"], row["pointer"]): row for row in cls.rows}

    def test_scope_is_exact_and_unique(self):
        self.assertEqual(self.manifest["translation_version"], "0.50.0-beta")
        self.assertEqual(len(self.rows), 537)
        self.assertEqual(len(self.by), 537)
        self.assertEqual(len({row["asset"] for row in self.rows}), 207)
        self.assertEqual(len({row["en"] for row in self.rows}), 308)
        self.assertTrue(all(row["asset"].startswith("bees/") for row in self.rows))
        self.assertTrue(all(row["section"] == "v0.50 arıcılık sistemi" for row in self.rows))

    def test_catalog_contains_exact_manifest_and_consistent_repeats(self):
        catalog = {(row["asset"], row["pointer"]): row for row in self.catalog["translations"]}
        self.assertEqual(self.catalog["translation_version"], "0.50.0-beta")
        by_source = {}
        for row in self.rows:
            current = catalog.get((row["asset"], row["pointer"]))
            self.assertIsNotNone(current, row["asset"] + row["pointer"])
            self.assertEqual((current["en"], current["tr"]), (row["en"], row["tr"]))
            by_source.setdefault(row["en"], set()).add(row["tr"])
        self.assertTrue(all(len(values) == 1 for values in by_source.values()))

    def test_beekeeping_terms_follow_project_decisions(self):
        self.assertEqual(self.by[("bees/bees/aquarum_queen.item", "/shortdescription")]["tr"], "Aquarum Ana Arısı")
        self.assertEqual(self.by[("bees/bees/aquarum_drone.item", "/shortdescription")]["tr"], "Aquarum Erkek Arısı")
        self.assertEqual(self.by[("bees/bees/aquarum_youngQueen.item", "/shortdescription")]["tr"], "Genç Aquarum Ana Arısı")
        forbidden = re.compile(r"\bkraliçe arı\b|\bdrone\b", re.IGNORECASE)
        self.assertFalse(any(forbidden.search(row["tr"]) for row in self.rows))

    def test_format_contracts(self):
        policy = json.loads((TOOLS / "rules/text_integrity.json").read_text(encoding="utf-8"))
        for row in self.rows:
            validate_format(row, policy)
            self.assertEqual(row["en"].count("\n"), row["tr"].count("\n"))


if __name__ == "__main__":
    unittest.main()
