"""Verify the final item scope and effect text boundaries."""

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import generate_v109 as gate
from plan_translation import preserved_name, read
from qa_integrity import Terminology, validate_format


class ProduceItemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read(TOOLS / 'v109_translations.json')
        cls.review = read(TOOLS.parent / cls.manifest['language_review'])
        cls.engine = Terminology(read(TOOLS / 'locked_terms.json'))
        cls.format_policy = read(TOOLS / 'rules/text_integrity.json')

    def test_exact_membership_and_overlay(self):
        rows = self.manifest['translations']
        self.assertEqual(len(rows), 225)
        self.assertEqual(len({r['asset'] for r in rows}), 113)
        self.assertTrue(all(r['pointer'] in ('/description', '/shortdescription') for r in rows))
        catalog = read(TOOLS / 'ceviriler.json')
        gate.validate_manifest(self.manifest, catalog, self.review)
        overlays = [r for r in rows if 'qa' in r]
        self.assertEqual(len(overlays), 1)
        row = overlays[0]
        self.assertEqual((row['asset'], row['pointer']), ('items/generic/produce/crystalplant.item', '/description'))
        changed = [dict(item) for item in rows]
        del next(item for item in changed if 'qa' in item)['qa']
        with self.assertRaisesRegex(ValueError, 'provenance'):
            gate.validate_manifest(dict(self.manifest, translations=changed), catalog, self.review)

    def test_crystal_broccoli_name_matches_extraction_text(self):
        rows = self.manifest['translations']
        broccoli = next(row for row in rows if row['en'] == 'Crystal Broccoli')
        extraction = next(row for row in rows if row['asset'].endswith('/crystalplant.item'))
        self.assertIn(broccoli['tr'], extraction['tr'])
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.engine.validate(dict(broccoli, tr='Kristal Bitki'))

    def test_effect_signature_rejects_different_value_or_glyph(self):
        rows = self.manifest['translations']
        for row in rows:
            validate_format(row, self.format_policy)
            self.engine.validate(row)
        fuel = next(r for r in rows if r['asset'].endswith('/erithianalgae.item') and r['pointer'] == '/description')
        with self.assertRaisesRegex(ValueError, 'Number mismatch'):
            validate_format(dict(fuel, tr=fuel['tr'].replace('3', '4')), self.format_policy)
        glyph = next(r for r in rows if '\ue024' in r['en'])
        with self.assertRaisesRegex(ValueError, 'glyph'):
            validate_format(dict(glyph, tr=glyph['tr'].replace('\ue024', '')), self.format_policy)

    def test_ordinary_english_is_not_preserved_as_an_item_description(self):
        row = dict(asset='items/generic/produce/other.item', pointer='/description',
                   en='This is a new ordinary description.', tr='Bu yeni bir açıklama.')
        self.engine.validate(row)
        self.assertFalse(preserved_name(dict(en=row['en'], tr=row['en'], occurrences=[row])))

    def test_garp_berry_preserve_metadata_matches_short_title(self):
        title = dict(asset='items/generic/produce/garpberry.consumable', pointer='/shortdescription')
        unit = dict(en='Garp Berry', tr='Garp Berry', occurrences=[title])
        self.assertTrue(preserved_name(unit))
        self.assertFalse(preserved_name(dict(unit, occurrences=[dict(title, pointer='/description')])))
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.engine.validate(dict(title, en='Garp Berry', tr='Garp Yemişi'))


if __name__ == '__main__':
    unittest.main()
