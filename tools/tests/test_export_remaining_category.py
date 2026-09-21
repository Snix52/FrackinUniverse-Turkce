import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import export_remaining_category as exporter


class ExportRemainingCategoryTests(unittest.TestCase):
    def test_exports_only_untranslated_confirmed_category_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "objects").mkdir()
            (source / "objects" / "crafting").mkdir(parents=True, exist_ok=True)
            asset = source / "objects" / "crafting" / "demo.object"
            asset.write_text(json.dumps({
                "shortdescription": "Demo Machine",
                "description": "Processes things.",
                "objectName": "technical_id"
            }), encoding="utf-8")
            catalog = root / "catalog.json"
            catalog.write_text(json.dumps({
                "translations": [{
                    "asset": "objects/crafting/demo.object",
                    "pointer": "/shortdescription",
                    "en": "Demo Machine",
                    "tr": "Demo Makinesi"
                }]
            }), encoding="utf-8")
            out = root / "out.json"
            with patch.object(exporter, "verify_source", return_value={"status": "PASS"}):
                data = exporter.export_category(
                    source, catalog, "Makineler, üretim ve dükkân nesneleri"
                )
            self.assertEqual(data["fields"], 1)
            self.assertEqual(data["rows"][0]["pointer"], "/description")
            self.assertEqual(data["rows"][0]["source"], "Processes things.")

    def test_source_grouping_counts_repeated_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            for name in ("a", "b"):
                path = source / "objects" / "crafting" / f"{name}.object"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({"category": "crafting"}), encoding="utf-8")
            catalog = root / "catalog.json"
            catalog.write_text('{"translations":[]}', encoding="utf-8")
            with patch.object(exporter, "verify_source", return_value={"status": "PASS"}):
                data = exporter.export_category(
                    source, catalog, "Makineler, üretim ve dükkân nesneleri"
                )
            self.assertEqual(data["fields"], 2)
            self.assertEqual(data["unique_source_strings"], 1)
            self.assertEqual(len(data["by_source"][0]["occurrences"]), 2)


if __name__ == "__main__":
    unittest.main()
