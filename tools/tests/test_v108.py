"""Protect produce-object variants and FU's technical transfer categories."""

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import generate_v108 as gate
from audit_remaining import visible_confidence
from plan_translation import preserved_name, read
from qa_integrity import Terminology


class ProduceObjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read(TOOLS / 'v108_translations.json')
        cls.review = read(TOOLS.parent / cls.manifest['language_review'])
        cls.engine = Terminology(read(TOOLS / 'locked_terms.json'))

    def test_exact_source_scope_keeps_technical_and_neighbor_fields_out(self):
        rows = self.manifest['translations']
        self.assertEqual(len(rows), 337)
        self.assertEqual(len({r['asset'] for r in rows}), 39)
        self.assertTrue(all(r['asset'].startswith('objects/produce/') and r['pointer'] != '/category' for r in rows))
        catalog = read(TOOLS / 'ceviriler.json')
        gate.validate_manifest(self.manifest, catalog, self.review)
        bad = [dict(row) for row in rows]
        bad[0]['pointer'] = '/category'
        with self.assertRaisesRegex(ValueError, 'membership'):
            gate.validate_manifest(dict(self.manifest, translations=bad), catalog, self.review)

    def test_compound_names_and_ordinary_english(self):
        for row in self.manifest['translations']:
            self.engine.validate(row)
        names = {r['en']: r for r in self.manifest['translations'] if r['pointer'] == '/shortdescription'}
        pear = names['Pearlpea Basket']
        self.assertEqual(pear['tr'], 'İnci Bezelyesi Sepeti')
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.engine.validate(dict(pear, tr='Bezelye Sepeti'))
        ordinary = dict(asset='ordinary.object', pointer='/description', en='A basket of peas.', tr='Bir sepet bezelye.')
        self.engine.validate(ordinary)
        self.assertFalse(preserved_name(dict(en=ordinary['en'], tr=ordinary['en'], occurrences=[ordinary])))

    def test_transfer_ids_are_technical_but_description_is_visible(self):
        cases = {
            'avikanspices.item': 'cookingIngredient',
            'dunestalk.item': 'cookingIngredient',
            'erithianalgae.item': 'fuel',
            'shoggothessence.consumable': 'medicine',
        }
        for name, category in cases.items():
            asset = 'items/generic/produce/' + name
            self.assertIsNone(visible_confidence(asset, ['category'], category))
            self.assertEqual(visible_confidence(asset, ['description'], 'Strong spices from Kadavan.'), 'confirmed')


if __name__ == '__main__':
    unittest.main()
