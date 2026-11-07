"""Verify the Agaran merchant wording and exact visible-field boundary."""

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import generate_v107 as gate
from plan_translation import preserved_name, read
from qa_integrity import Terminology


class AgaranMerchantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read(TOOLS / 'v107_translations.json')
        cls.review = read(TOOLS.parent / cls.manifest['language_review'])
        cls.engine = Terminology(read(TOOLS / 'locked_terms.json'))

    def test_window_title_membership_and_leading_spaces(self):
        asset = 'npcs/biome/shroommerchant.npctype'
        base = '/scriptConfig/merchant/paneLayoutOverride/windowtitle/'
        expected = {(asset, base + key) for key in ('title', 'subtitle')}
        self.assertEqual(gate.build.V107_SHROOMMERCHANT_FIELDS, expected)
        by_name = {row['pointer'].rsplit('/', 1)[1]: row for row in self.manifest['translations']}
        self.assertEqual(by_name['title']['tr'], '  Agaran Tüccarı')
        self.assertEqual(by_name['subtitle']['tr'], '  Mantar kılıklı satıcı, öteberi satar')
        for row in by_name.values():
            self.assertTrue(row['en'].startswith('  ') and row['tr'].startswith('  '))
            self.engine.validate(row)
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.engine.validate(dict(by_name['subtitle'], tr='  Mantar satar'))

    def test_proper_name_and_ordinary_english_have_separate_scope(self):
        occurrence = dict(asset='ordinary.object', pointer='/description')
        self.engine.validate(dict(occurrence, en='A merchant sells goods.', tr='Bir satıcı mal satıyor.'))
        self.engine.validate(dict(occurrence, en='Agaran', tr='Agaran'))
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.engine.validate(dict(occurrence, en='Agaran', tr='Mantarcı'))
        self.assertFalse(preserved_name(dict(en='A merchant sells goods.', tr='A merchant sells goods.',
                                             occurrences=[occurrence])))

    def test_manifest_rejects_neighbor_field(self):
        catalog = read(TOOLS / 'ceviriler.json')
        gate.validate_manifest(self.manifest, catalog, self.review)
        rows = [dict(row) for row in self.manifest['translations']]
        rows[0]['pointer'] = '/scriptConfig/merchant/paneLayoutOverride/windowtitle/icon'
        with self.assertRaisesRegex(ValueError, 'membership'):
            gate.validate_manifest(dict(self.manifest, translations=rows), catalog, self.review)


if __name__ == '__main__':
    unittest.main()
