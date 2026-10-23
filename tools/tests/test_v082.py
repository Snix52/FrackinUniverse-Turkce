"""Protect the final confirmed radio tranche and its narrow name approvals."""
import copy
import sys
import unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology,plain,validate_format
import generate_v082 as gate


class V082Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=read(TOOLS/'v082_translations.json');cls.catalog=read(TOOLS/'ceviriler.json')
        cls.review=read(TOOLS.parent/'docs/reviews/radio3-20261023.json')
        cls.policy=read(TOOLS/'locked_terms.json');cls.format=read(TOOLS/'rules/text_integrity.json')

    def row(self,pointer):
        return next(r for r in self.manifest['translations'] if r['pointer']==pointer)

    def test_exact_fortythree_names_do_not_allow_english_or_neighbors(self):
        names=[r for r in self.manifest['translations'] if r['en']==r['tr']]
        self.assertEqual(len(names),43)
        for r in names:
            unit=dict(en=r['en'],tr=r['tr'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])
            self.assertTrue(preserved_name(unit))
            for en,asset,pointer in [(r['en'],r['asset'],r['pointer']+'/neighbor'),
                                     (r['en'],'radiomessages/unapproved.radiomessages',r['pointer']),
                                     ('Tonauac needs help.',r['asset'],r['pointer']),
                                     ('???',r['asset'],r['pointer'])]:
                with self.subTest(en=en,asset=asset,pointer=pointer):
                    self.assertFalse(preserved_name(dict(en=en,tr=en,occurrences=[dict(asset=asset,pointer=pointer)])))

    def test_baron_was_already_translated_and_not_counted_as_sol_edit(self):
        rows=[r for r in self.manifest['translations'] if r['en']=='The Baron']
        self.assertEqual(len(rows),4);self.assertTrue(all(r['tr']=='Baron' for r in rows))
        changed={(o['asset'],o['pointer']) for c in self.review['corrections'] for o in c['occurrences']}
        self.assertFalse(any((r['asset'],r['pointer']) in changed for r in rows))

    def test_new_device_names_reject_incorrect_variants_in_sentences(self):
        engine=Terminology(self.policy)
        for en,good,bad in [('Crew Beds','Mürettebat Yatakları','Kadro Yatakları'),
                            ('Kinetic Orb Cannon','Kinetik Küre Topu','Kinetik Küre Fırlatıcı'),
                            ('Bounce Pads','Sekme Platformları','Zıplama Rampaları'),
                            ('Distortion Sphere Tech II','Çarpıtma Küresi Tech II','Çarpıtma Küresi'),
                            ('Welcome Beacon','Karşılama İşaretçisi','Hoşgeldin Feneri')]:
            row=dict(asset='fixture',pointer='/text',en='You found '+en+'.',tr=good+' buldun.')
            engine.validate(row)
            with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):
                engine.validate(dict(row,tr=bad+' buldun.'))

    def test_all_thirtyfive_edited_replies_reject_delivered_regressions(self):
        self.assertEqual(len(self.review['corrections']),35)
        engine=Terminology(self.policy)
        for c in self.review['corrections']:
            row=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(row)
            with self.subTest(pointer=row['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):
                engine.validate(dict(row,tr=c['before']))

    def test_riddle_count_exclusion_and_small_leap_emphasis_preserved(self):
        first=self.row('/skytemple09b/text')['tr'];second=self.row('/skytemple10/text')['tr'];third=self.row('/skytemple11/text')['tr']
        self.assertIn('ikiyi',first)
        for phrase in ('üçü hariç','toplam sekiz','üç kolu'):self.assertIn(phrase,second)
        for phrase in ('dördü hariç','toplam on iki','dört kolu'):self.assertIn(phrase,third)
        self.assertIn('KÜÇÜK',self.row('/skytemple06b/text')['tr'])

    def test_green_scope_drift_cannot_reuse_language_approval(self):
        row=self.row('/gaterepair-findGate/text')
        self.assertIn('^green;Araştırmaya değer olma ihtimalinin %82^reset;',row['tr'])
        wrong=copy.deepcopy(self.manifest);bad=next(r for r in wrong['translations'] if r['pointer']==row['pointer'])
        bad['tr']=bad['tr'].replace('^green;Araştırmaya değer olma ihtimalinin %82^reset;','Araştırmaya değer olma ihtimalinin ^green;%82^reset;')
        self.assertEqual(plain(bad['tr']),plain(row['tr']))
        with self.assertRaisesRegex(ValueError,'approved translation'):
            gate.validate_manifest(wrong,self.catalog,self.review)

    def test_real_fire_f_tech_ii_and_source_numbers_are_not_relabelled(self):
        row=self.row('/techchallenge_morphball1/text');validate_format(row,self.format)
        self.assertIn('F tuşuna',row['tr']);self.assertIn('Tech II',row['tr']);self.assertIn('[Fire]',row['tr'])
        with self.assertRaisesRegex(ValueError,'Control token'):
            validate_format(dict(row,tr=row['tr'].replace('[Fire]','[Ateş]')),self.format)
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            Terminology(self.policy).validate(dict(row,tr=row['tr'].replace('F tuşuna','Bir tuşa')))
        for pointer in ('/volcanobase03/text','/volcanobase05a/text','/gaterepair-findGate/text'):
            validate_format(self.row(pointer),self.format)

    def test_natural_cave_brush_is_found_without_claiming_missing_image_placement(self):
        c=self.review['source_context'];self.assertEqual((c['message_ids'],c['qualified_static_message_ids'],c['qualified_text_message_ids'],c['qualified_fields']),(88,86,84,131))
        self.assertEqual(c['ids_without_radio_context_candidates'],['gaterepair-findGate','tentaclemission-bossroom'])
        self.assertEqual(c['natural_cave_review']['ids'],['naturalcave1','naturalcave2'])
        self.assertIn('absent',c['natural_cave_review']['limitation'])
        for mid in ('naturalcave1','naturalcave2'):
            self.assertTrue(any(r['radio_context'] and r['source'].endswith('naturalcave.dungeon') for r in c['references'][mid]))
        for mid in ('volcanobase11','volcanobase11a','volcanobase11b'):
            self.assertEqual(len({r['source'] for r in c['references'][mid]}),3)
        self.assertEqual(self.review['lqa_status'],'NOT TESTED')

    def test_all_fields_are_layered_and_exact_approval_membership_is_closed(self):
        gate.validate_manifest(self.manifest,self.catalog,self.review)
        self.assertEqual(sum(r['qa']['layered_source'] for r in self.manifest['translations']),133)
        wrong=copy.deepcopy(self.manifest);wrong['translations'][0]['qa']['source_patch']='wrong.patch'
        with self.assertRaisesRegex(ValueError,'provenance'):
            gate.validate_manifest(wrong,self.catalog,self.review)
        wrong=copy.deepcopy(self.manifest);wrong['translations'][0]['tr']+=' New mechanic.'
        with self.assertRaisesRegex(ValueError,'approved translation'):
            gate.validate_manifest(wrong,self.catalog,self.review)

    def test_old_sail_aether_is_aligned_without_altering_material_terminology(self):
        fixes=self.review['maintenance'];self.assertEqual(len(fixes),1);fix=fixes[0]
        self.assertTrue(fix['before'].startswith("Aether'de"));self.assertTrue(fix['after'].startswith('Eterde'))
        old=read(TOOLS/'v046_translations.json')['translations']
        for rows in (self.catalog['translations'],old):
            self.assertEqual(next(r['tr'] for r in rows if (r['asset'],r['pointer'])==(fix['asset'],fix['pointer'])),fix['after'])
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            Terminology(self.policy).validate(dict(asset=fix['asset'],pointer=fix['pointer'],en=fix['en'],tr=fix['before']))
        Terminology(self.policy).validate(dict(asset='fixture',pointer='/shortdescription',en='Aether',tr='Aether'))


if __name__=='__main__':
    unittest.main()
