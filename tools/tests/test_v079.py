"""Reject source-preservation leaks, inverted comparisons and merchandise drift."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from plan_translation import read, preserved_name
from qa_integrity import Terminology, plain
import generate_v079 as gate
import build_validate as build


class V079Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read(TOOLS / 'v079_translations.json')
        cls.catalog = read(TOOLS / 'ceviriler.json')
        cls.review = read(TOOLS.parent / 'docs/reviews/scienceoutpost-20261021.json')
        cls.policy = read(TOOLS / 'locked_terms.json')

    def unit(self, row):
        return dict(en=row['en'], tr=row['tr'], occurrences=[{k: row[k] for k in ('asset', 'pointer')}])

    def sounds(self):
        return [r for r in self.manifest['translations'] if r['en'] == r['tr']]

    def test_only_seventeen_exact_placeholders_clicks_and_scott_calls_are_preserved(self):
        self.assertEqual(len(self.sounds()), 17)
        for row in self.sounds():
            self.assertTrue(preserved_name(self.unit(row)))
            for wrong in (dict(row, pointer=row['pointer'] + '/neighbor'),
                          dict(row, asset='npcs/scienceoutpost/unapproved.npctype'),
                          dict(row, en='Steve needs your help.', tr='Steve needs your help.'),
                          dict(row, en='<playername>', tr='<playername>')):
                with self.subTest(row=row, wrong=wrong):
                    self.assertFalse(preserved_name(self.unit(wrong)))
        unit = self.unit(self.sounds()[0])
        unit['occurrences'].append(dict(asset='npcs/scienceoutpost/neighbor.npctype', pointer='/scriptConfig/dialog/0'))
        self.assertFalse(preserved_name(unit))

    def test_bound_permission_requires_active_preserve_term_and_complete_reason(self):
        row = self.sounds()[0]
        binding = next(x for x in self.review['preserve_bindings'] if x['asset'] == row['asset'] and x['pointer'] == row['pointer'])
        for mutation in ('reason', 'tr', 'status', 'mode'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                policy = copy.deepcopy(self.policy)
                term = next(t for t in policy['terms'] if t['source'] == binding['term_source'])
                if mutation == 'status':
                    term['status'] = 'REVIEW'
                elif mutation == 'mode':
                    term.pop('mode')
                else:
                    next(x for x in policy['context_exceptions'] if x['asset'] == row['asset'] and x['pointer'] == row['pointer'])[mutation] = ''
                tools = Path(directory)
                (tools / 'locked_terms.json').write_text(json.dumps(policy), encoding='utf-8')
                self.assertFalse(preserved_name(self.unit(row), tools))

    def test_locked_comparisons_deyims_and_sound_actions_reject_delivered_regressions(self):
        terms = Terminology(self.policy)
        checked = 0
        for correction in self.review['corrections']:
            row = dict(correction['occurrences'][0], en=correction['en'], tr=correction['after'])
            terms.validate(row)
            if plain(row['en']) in terms.exact or 'garflipp' in row['en'].lower():
                with self.subTest(en=row['en']), self.assertRaisesRegex(ValueError, 'LOCKED'):
                    terms.validate(dict(row, tr=correction['before']))
                checked += 1
        self.assertGreater(checked, 45)

    def test_locked_garflipp_name_does_not_approve_ordinary_english_dialogue(self):
        row = dict(asset='npcs/scienceoutpost/fixture.npctype', pointer='/scriptConfig/dialog/converse/default/0', en='Garflipp is over there.', tr='Garflipp is over there.')
        self.assertFalse(preserved_name(self.unit(row)))
        terms = Terminology(self.policy)
        terms.validate(dict(row, tr='Garflipp orada.'))
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            terms.validate(dict(row, tr='Garflip orada.'))
        terms.validate(dict(row, en='The worm ate bread.', tr='Solucan ekmek yedi.'))

    def test_exact_source_gate_rejects_changed_words_and_added_gameplay_fields(self):
        gate.validate_manifest(self.manifest, self.catalog, self.review)
        broken = copy.deepcopy(self.manifest)
        broken['translations'][0]['tr'] += ' Yeni mekanik.'
        with self.assertRaisesRegex(ValueError, 'approved translation'):
            gate.validate_manifest(broken, self.catalog, self.review)
        asset = 'npcs/scienceoutpost/lostandfoundnpc.npctype'
        for pointer in ('/scriptConfig/merchant/buyFactorRange/0', '/scriptConfig/merchant/numItems', '/scriptConfig/merchant/categories/override/0'):
            self.assertFalse(build.allowed(asset, pointer))

    def test_merchant_two_space_prefix_and_legacy_path_are_never_silently_rewritten(self):
        rows = self.manifest['translations']
        subtitle = next(r for r in rows if r['pointer'].endswith('/windowtitle/subtitle'))
        self.assertTrue(subtitle['tr'].startswith('  '))
        self.assertFalse(subtitle['tr'].startswith('   '))
        self.assertEqual(sum('/scriptConfig/converse/dialog/' in r['pointer'] for r in rows), 13)
        self.assertEqual(self.review['scope']['legacy_fields_active_consumer_unverified'], 13)
        self.assertEqual(self.review['lqa_status'], 'NOT TESTED')
        broken = copy.deepcopy(self.manifest)
        next(r for r in broken['translations'] if r['pointer'].endswith('/windowtitle/subtitle'))['tr'] = subtitle['tr'].lstrip()
        with self.assertRaisesRegex(ValueError, 'approved translation'):
            gate.validate_manifest(broken, self.catalog, self.review)

    def test_scientist_filename_cannot_invent_floran_speaker_identity(self):
        npc = next(x for x in self.review['source_context']['npcs'] if x['type'] == 'fuoutpostfloranscientist')
        self.assertEqual(npc['map_placements'][0]['npc'], 'human')
        self.assertEqual(npc['map_placements'][0]['npcname'], 'Acheron')
        row = next(r for r in self.manifest['translations'] if r['asset'] == npc['asset'])
        self.assertEqual(row['tr'], 'Benim için bir ağaca bıçak sssaplar mısın?')
        broken = copy.deepcopy(self.manifest)
        next(r for r in broken['translations'] if r['asset'] == npc['asset'])['tr'] = 'Floran için bir ağaca bıçak sssaplar mısın?'
        with self.assertRaisesRegex(ValueError, 'approved translation'):
            gate.validate_manifest(broken, self.catalog, self.review)


if __name__ == '__main__':
    unittest.main()
