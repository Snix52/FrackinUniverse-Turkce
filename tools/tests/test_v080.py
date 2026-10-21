"""Prevent English narration, source-layer drift and terminology regressions."""
import copy
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from plan_translation import read, preserved_name
from qa_integrity import Terminology, plain, validate_format
import generate_v080 as gate
import build_validate as build


class V080Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read(TOOLS / 'v080_translations.json')
        cls.catalog = read(TOOLS / 'ceviriler.json')
        cls.review = read(TOOLS.parent / 'docs/reviews/radio1-20261022.json')
        cls.policy = read(TOOLS / 'locked_terms.json')
        cls.format = read(TOOLS / 'rules/text_integrity.json')

    def unit(self, row):
        return dict(en=row['en'], tr=row['tr'], occurrences=[{k: row[k] for k in ('asset', 'pointer')}])

    def test_exact_proper_names_and_fictional_calls_do_not_allow_english_sentences(self):
        rows = [r for r in self.manifest['translations'] if r['en'] == r['tr']]
        self.assertEqual(len(rows), 73)
        self.assertEqual(sum(r['pointer'].endswith('/senderName') for r in rows), 69)
        for row in rows:
            self.assertTrue(preserved_name(self.unit(row)))
            for wrong in (dict(row, pointer=row['pointer'] + '/neighbor'),
                          dict(row, asset='radiomessages/unapproved.radiomessages'),
                          dict(row, en='Vinalisj needs help.', tr='Vinalisj needs help.'),
                          dict(row, en='<the whispers are growing louder>', tr='<the whispers are growing louder>')):
                self.assertFalse(preserved_name(self.unit(wrong)))

    def test_angle_narrations_translate_without_weakening_placeholder_checks(self):
        narrations = [r for r in self.manifest['translations'] if r['en'].startswith('<')]
        self.assertEqual(len(narrations), 3)
        for row in narrations:
            self.assertNotEqual(row['en'], row['tr'])
            self.assertFalse(preserved_name(self.unit(dict(row, tr=row['en']))))
            validate_format(row, self.format)
            for wrong in (dict(row, pointer=row['pointer'] + '/neighbor'),
                          dict(row, tr=row['tr'] + '!'),
                          dict(row, en='<entityname>', tr='<oyuncu>'),
                          dict(row, en='<frame>', tr='<kare>')):
                with self.assertRaisesRegex(ValueError, 'Control token'):
                    validate_format(wrong, self.format)
        validate_format(dict(asset='fixture', pointer='/text', en='Hello <entityname>!', tr='Merhaba <entityname>!'), self.format)

    def test_existing_and_new_material_terms_reject_wrong_names_inside_sentences(self):
        terms = Terminology(self.policy)
        for en, good, bad in [('Armorworks', 'Zırh Atölyesi', 'Armorworks'),
                               ('Fungal Ichor', 'Mantar Özsuyu', 'Mantar İçi'),
                               ('Cinnabar', 'Zinober', 'Cinnabar'),
                               ('Mascagnite', 'Maskagnit', 'Mascagnite'),
                               ('Neutronium', 'Nötronyum', 'Nötronium'),
                               ('Microsphere', 'Mikroküre', 'Mikro Küre')]:
            row = dict(asset='fixture', pointer='/text', en='You obtained ' + en + '.', tr=good + ' edindin.')
            terms.validate(row)
            with self.assertRaisesRegex(ValueError, 'LOCKED'):
                terms.validate(dict(row, tr=bad + ' edindin.'))
        terms.validate(dict(asset='fixture', pointer='/text', en='This will ruin the experiment.', tr='Bu, deneyi mahvedecek.'))

    def test_locked_full_replies_reject_delivered_regressions(self):
        terms = Terminology(self.policy)
        count = 0
        for correction in self.review['corrections']:
            row = dict(correction['occurrences'][0], en=correction['en'], tr=correction['after'])
            terms.validate(row)
            if plain(row['en']) in terms.exact and plain(correction['before']) != plain(correction['after']):
                with self.assertRaisesRegex(ValueError, 'LOCKED'):
                    terms.validate(dict(row, tr=correction['before']))
                count += 1
        self.assertGreaterEqual(count, 24)

    def test_exact_source_gate_rejects_wrong_provenance_and_new_gameplay_fields(self):
        gate.validate_manifest(self.manifest, self.catalog, self.review)
        self.assertEqual(sum(r.get('qa', {}).get('layered_source', False) for r in self.manifest['translations']), 45)
        for key in ('source_patch', 'layered_source'):
            wrong = copy.deepcopy(self.manifest)
            next(r for r in wrong['translations'] if r.get('qa', {}).get('layered_source'))['qa'].pop(key)
            with self.assertRaisesRegex(ValueError, 'provenance'):
                gate.validate_manifest(wrong, self.catalog, self.review)
        for pointer in ('/fubiomepressure/text/unapproved', '/fubiomepressure/speed', '/fubiomepressure/type', '/fubiomepressure/unique'):
            self.assertFalse(build.allowed('radiomessages/fu_exploration.radiomessages', pointer))
        wrong = copy.deepcopy(self.manifest)
        wrong['translations'][0]['tr'] += ' New mechanic.'
        with self.assertRaisesRegex(ValueError, 'approved translation'):
            gate.validate_manifest(wrong, self.catalog, self.review)

    def test_static_evidence_does_not_claim_live_activation(self):
        context = self.review['source_context']
        self.assertEqual(context['ids_with_radio_context_candidates'], 205)
        self.assertEqual(len(context['ids_without_radio_context_candidates']), 37)
        self.assertFalse(any(r['radio_context'] for r in context['references']['biomeairless'] if r['source'] == 'dungeon_worlds.config.patch'))
        self.assertTrue(any('<encoded-json>' in r.get('pointer', '') for r in context['references']['shoggothmission4']))
        self.assertEqual(self.review['lqa_status'], 'NOT TESTED')

    def test_existing_source_bug_exceptions_are_exact_and_material_maintenance_is_consistent(self):
        terms = Terminology(self.policy)
        bindings = self.review['existing_source_bug_bindings']
        self.assertEqual(len(bindings), 5)
        for row in bindings:
            terms.validate(row)
            with self.assertRaisesRegex(ValueError, 'LOCKED'):
                terms.validate(dict(row, pointer=row['pointer'] + '/neighbor'))
        fixes = self.review['maintenance']
        self.assertEqual(len(fixes), 2)
        catalog = {(r['asset'], r['pointer']): r for r in self.catalog['translations']}
        old = {(r['asset'], r['pointer']): r for r in read(TOOLS / 'v056_translations.json')['translations']}
        for fix in fixes:
            row = catalog[(fix['asset'], fix['pointer'])]
            self.assertEqual(row['tr'], fix['after'])
            self.assertEqual(row['tr'], old[(fix['asset'], fix['pointer'])]['tr'])
            with self.assertRaisesRegex(ValueError, 'LOCKED'):
                terms.validate(dict(row, tr=fix['before']))


if __name__ == '__main__':
    unittest.main()
