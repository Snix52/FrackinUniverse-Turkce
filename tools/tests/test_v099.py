"""Reject cultist scope drift, altered threats and invented runtime approval."""
import copy
import sys
import unittest
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from plan_translation import read, preserved_name
from qa_integrity import Terminology
import generate_v099 as gate


class V099Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read(TOOLS / 'v099_translations.json')
        cls.catalog = read(TOOLS / 'ceviriler.json')
        cls.policy = read(TOOLS / 'locked_terms.json')
        cls.review = read(TOOLS.parent / 'docs/reviews/forestoffae-20261106.json')

    def row(self, en):
        return next(r for r in self.manifest['translations'] if r['en'] == en)

    def test_exact_scope_neighbor_and_source_provenance(self):
        gate.validate_manifest(self.manifest, self.catalog, self.review)
        for key, value in [('asset', 'npcs/hostilefu.npctype'),
                           ('pointer', '/scriptConfig/behavior'),
                           ('en', 'The Shadow is a confirmed boss.'),
                           ('tr', 'Kaynakta olmayan bir varlık.')]:
            bad = copy.deepcopy(self.manifest)
            bad['translations'][0][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'scope/count drift|approved translation'):
                gate.validate_manifest(bad, self.catalog, self.review)
        bad = copy.deepcopy(self.manifest)
        bad['translations'][0]['qa'] = {'layered_source': True}
        with self.assertRaisesRegex(ValueError, 'provenance'):
            gate.validate_manifest(bad, self.catalog, self.review)

    def test_every_occurrence_rejects_unrelated_translation(self):
        engine = Terminology(self.policy)
        for row in self.manifest['translations']:
            engine.validate(row)
            with self.subTest(asset=row['asset'], pointer=row['pointer']), self.assertRaisesRegex(ValueError, 'LOCKED'):
                engine.validate(dict(row, tr='İlgisiz bir cümle.'))

    def test_both_complete_attack_lists_keep_all_six_replies_consistent(self):
        rows = self.manifest['translations']
        self.assertEqual((len(rows), len({r['en'] for r in rows})), (12, 6))
        self.assertEqual(sorted(Counter(r['asset'] for r in rows).values()), [6, 6])
        self.assertTrue(all('/attack/default/default/' in r['pointer'] for r in rows))
        for en in {r['en'] for r in rows}:
            group = [r for r in rows if r['en'] == en]
            self.assertEqual(len(group), 2)
            self.assertEqual(len({r['tr'] for r in group}), 1)

    def test_threat_and_imperative_do_not_become_new_mechanics(self):
        engine = Terminology(self.policy)
        pairs = [("I'll melt your face off!", 'Yüzünü eriteceğim!', 'Yüzünü donduracağım!'),
                 ('Speak the shadow words of pain!', 'Acının gölge sözlerini dile getir!', 'Acının ışık sözlerini dile getir!')]
        for en, tr, wrong in pairs:
            row = self.row(en)
            self.assertEqual(row['tr'], tr)
            with self.assertRaisesRegex(ValueError, 'LOCKED'):
                engine.validate(dict(row, tr=wrong))

    def test_ellipsis_and_tears_darkness_fragments_keep_their_meaning(self):
        self.assertEqual(self.row('Nothing...everything!')['tr'], 'Hiçbir şey...her şey!')
        row = self.row('No more tears. Only darkness.')
        self.assertEqual(row['tr'], 'Artık gözyaşı yok. Yalnızca karanlık.')
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            Terminology(self.policy).validate(dict(row, tr='Artık gözyaşı yok. Yalnızca aydınlık.'))

    def test_full_reply_locks_do_not_force_ordinary_shadow_or_corruption(self):
        engine = Terminology(self.policy)
        engine.validate(dict(asset='ordinary', pointer='/description', en='The shadow lengthens.', tr='Gölge uzuyor.'))
        engine.validate(dict(asset='ordinary', pointer='/description', en='Political corruption grows.', tr='Siyasi yozlaşma artıyor.'))
        self.assertEqual(self.row('The Shadow will consume all!')['tr'], 'Gölge her şeyi yutacak!')
        self.assertEqual(self.row('The Corruption spreads!')['tr'], 'Yozlaşma yayılıyor!')
        self.assertEqual((self.review['new_locked_terms'], self.review['locked_total']), (6, 1310))
        self.assertFalse(self.review['source_context']['generic_shadow_corruption_rules_added'])

    def test_retained_review_is_not_fake_correction_or_english_preservation(self):
        self.assertEqual(self.review['corrections'], [])
        self.assertEqual(self.review['changes']['total_corrected_sentences'], 0)
        self.assertEqual(self.review['changes']['total_corrected_fields'], 0)
        self.assertEqual(self.review['context_bindings'], [])
        self.assertEqual(self.review['preserve_bindings'], [])
        for row in self.manifest['translations']:
            self.assertFalse(preserved_name(dict(en=row['en'], tr=row['en'], occurrences=[dict(asset=row['asset'], pointer=row['pointer'])])))

    def test_static_maps_and_missing_dependencies_never_become_live_lqa(self):
        import build_validate as build
        context = self.review['source_context']
        self.assertEqual([n['base_type'] for n in context['npcs']], ['hostilefu', 'hostilefu'])
        self.assertEqual(len(context['maps']), 13)
        self.assertEqual(sum(m['selected_static_npcs'] for m in context['maps']), 50)
        fae = next(m for m in context['maps'] if '/forestoffae/' in m['asset'])
        evernight = next(m for m in context['maps'] if '/evernight/' in m['asset'])
        self.assertEqual((fae['all_static_npcs'], fae['selected_static_npcs'], len(fae['radio_stagehands'])), (14, 13, 6))
        self.assertEqual((evernight['all_static_npcs'], evernight['selected_static_npcs'], len(evernight['radio_stagehands'])), (55, 14, 12))
        self.assertEqual({x['properties']['npc'] for x in fae['selected']}, {'human'})
        self.assertEqual({x['properties']['npc'] for x in evernight['selected']}, {'hylotl'})
        self.assertEqual(len(context['radio_messages']), 17)
        self.assertFalse(context['active_consumer_verified'])
        self.assertFalse(context['actual_spawn_count_verified'])
        self.assertEqual(len(context['missing_vanilla_dependencies']), 3)
        self.assertEqual(self.review['lqa_status'], 'NOT TESTED')
        self.assertEqual(len(build.V099_FORESTOFFAE_FIELDS), 12)
        for asset in self.review['scope']['assets']:
            for pointer in ['/baseType', '/scriptConfig/behavior', '/items/override']:
                self.assertNotIn((asset, pointer), build.V099_FORESTOFFAE_FIELDS)


if __name__ == '__main__':
    unittest.main()
