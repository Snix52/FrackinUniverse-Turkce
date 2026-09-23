import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qa_integrity import validate_format
from rule_data import TOOLS


class V048Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((TOOLS / 'v048_translations.json').read_text(encoding='utf-8'))
        cls.catalog = json.loads((TOOLS / 'ceviriler.json').read_text(encoding='utf-8'))
        cls.rows = cls.manifest['translations']

    def test_catalog_contains_exact_manifest(self):
        catalog = {(row['asset'], row['pointer']): row for row in self.catalog['translations']}
        self.assertEqual(len(self.rows), 151)
        self.assertEqual(len({row['asset'] for row in self.rows}), 32)
        self.assertEqual(len({row['en'] for row in self.rows}), 87)
        for row in self.rows:
            current = catalog.get((row['asset'], row['pointer']))
            self.assertIsNotNone(current, row['asset'] + row['pointer'])
            self.assertEqual((current['en'], current['tr']), (row['en'], row['tr']))

    def test_scope_is_exact(self):
        families = {'darkwood', 'lightwood', 'treatedwood'}
        pointers = {
            '/description', '/shortdescription', '/floranDescription',
            '/glitchDescription', '/novakidDescription',
        }
        self.assertEqual(self.manifest['translation_version'], '0.48.0-beta')
        for row in self.rows:
            parts = Path(row['asset']).parts
            self.assertEqual(parts[:2], ('tiles', 'materials'))
            self.assertIn(parts[2], families)
            self.assertIn(row['pointer'], pointers)

    def test_repeated_source_strings_use_one_translation(self):
        translations = {}
        for row in self.rows:
            translations.setdefault(row['en'], set()).add(row['tr'])
        self.assertTrue(all(len(values) == 1 for values in translations.values()))

    def test_all_new_text_preserves_format_contracts(self):
        policy = json.loads((TOOLS / 'rules/text_integrity.json').read_text(encoding='utf-8'))
        for row in self.rows:
            validate_format(row, policy)


if __name__ == '__main__':
    unittest.main()
