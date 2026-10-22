"""Guard named speakers, pseudo-controls, chronology and the actual trial tool."""
import copy
import sys
import unittest
from pathlib import Path
TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from plan_translation import read, preserved_name
from qa_integrity import Terminology, plain, validate_format
import generate_v081 as gate


class V081Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read(TOOLS / 'v081_translations.json')
        cls.catalog = read(TOOLS / 'ceviriler.json')
        cls.review = read(TOOLS.parent / 'docs/reviews/radio2-20261022.json')
        cls.policy = read(TOOLS / 'locked_terms.json')
        cls.format = read(TOOLS / 'rules/text_integrity.json')

    def unit(self, row):
        return dict(en=row['en'], tr=row['tr'], occurrences=[{k: row[k] for k in ('asset','pointer')}])

    def test_only_sixtyeight_exact_person_names_preserved_and_baron_translates(self):
        rows = self.manifest['translations']
        names = [r for r in rows if r['en'] == r['tr']]
        self.assertEqual(len(names), 68)
        self.assertEqual(sum(r['en'] == 'The Baron' and r['tr'] == 'Baron' for r in rows), 6)
        for row in names:
            self.assertTrue(preserved_name(self.unit(row)))
            for wrong in (dict(row,pointer=row['pointer']+'/neighbor'),
                          dict(row,asset='radiomessages/unapproved.radiomessages'),
                          dict(row,en='Esther Bright needs help.',tr='Esther Bright needs help.'),
                          dict(row,en='???',tr='???')):
                self.assertFalse(preserved_name(self.unit(wrong)))

    def test_pseudo_controls_translate_only_inside_two_bound_fields(self):
        rows = [r for r in self.manifest['translations'] if r.get('qa',{}).get('allow_control_fix')]
        self.assertEqual(len(rows), 2)
        for row in rows:
            validate_format(row,self.format)
            for wrong in (dict(row,pointer=row['pointer']+'/neighbor'),
                          dict(row,tr=row['tr']+'!'),
                          dict(row,en='<entityname>',tr='<oyuncu>'),
                          dict(row,en='<frame>',tr='<kare>'),
                          dict(row,en='[DOWN]',tr='[UP]')):
                with self.assertRaisesRegex(ValueError,'Control token'):
                    validate_format(wrong,self.format)

    def test_new_terms_reject_delivered_wrong_names_in_other_sentences(self):
        terms = Terminology(self.policy)
        for en,good,bad in [('The Baron','Baron','The Baron'),
                            ('Upgrade Modules','Yükseltme Modülleri','Geliştirme Modülleri'),
                            ('Spike Sphere','Dikenli Küre','Sivri Uçlu Küre'),
                            ('Sonic Sphere Tech','Sonik Küre Tech','Ses Küresi Tech'),
                            ('Grappling Hook','Tutunma Kancası','Kancalı Halat'),
                            ('Relocator','Taşıyıcı','Işınlayıcı'),
                            ('Translocator','Işınlayıcı','Taşıyıcı')]:
            row=dict(asset='fixture',pointer='/text',en='You found '+en+'.',tr=good+' buldun.')
            terms.validate(row)
            with self.assertRaisesRegex(ValueError,'LOCKED'):
                terms.validate(dict(row,tr=bad+' buldun.'))

    def test_locked_full_replies_reject_before_review_regressions(self):
        terms=Terminology(self.policy);count=0
        for c in self.review['corrections']:
            row=dict(c['occurrences'][0],en=c['en'],tr=c['after']);terms.validate(row)
            if plain(row['en']) in terms.exact and plain(c['before'])!=plain(c['after']):
                with self.assertRaisesRegex(ValueError,'LOCKED'):
                    terms.validate(dict(row,tr=c['before']))
                count+=1
        self.assertGreaterEqual(count,40)

    def test_source_bug_binding_is_exact_and_does_not_relabel_other_relocators(self):
        fix=self.review['source_corrections'][0];terms=Terminology(self.policy)
        self.assertIn('Işınlayıcı',fix['tr']);terms.validate(fix)
        for wrong in (dict(fix,pointer=fix['pointer']+'/neighbor'),
                      dict(fix,asset='fixture.item',pointer='/description'),
                      dict(fix,tr=fix['en'])):
            with self.assertRaisesRegex(ValueError,'LOCKED'):
                terms.validate(wrong)
        row=next(r for r in self.manifest['translations'] if r['pointer']=='/extrachallengelabs305/text')
        self.assertTrue(row['qa']['source_bug_fix'])
        wrong=copy.deepcopy(self.manifest)
        next(r for r in wrong['translations'] if r['pointer']==row['pointer'])['qa'].pop('source_bug_fix')
        with self.assertRaisesRegex(ValueError,'provenance'):
            gate.validate_manifest(wrong,self.catalog,self.review)

    def test_trial_map_loot_tool_and_launcher_evidence_cannot_drift(self):
        treasure={'extrachallengelabtranslocator':[[0,{'fill':[{'item':'translocator'}]}]]}
        mapdata={'layers':[{'objects':[{'id':53,'properties':{'parameters':'{"treasurePools":["extrachallengelabtranslocator"]}'}}]}]}
        device={'itemName':'translocator','description':'Fires teleport-node discs.'}
        projectile='world.spawnProjectile("translocatordisc", position)'
        gate.validate_trial_evidence(treasure,mapdata,device,projectile)
        for target in ('loot','map','tool','launcher'):
            a,b,c,d=map(copy.deepcopy,(treasure,mapdata,device,projectile))
            if target=='loot':a['extrachallengelabtranslocator'][0][1]['fill'][0]['item']='relocator'
            elif target=='map':b['layers'][0]['objects'][0]['properties']['parameters']='{"treasurePools":["wrongpool"]}'
            elif target=='tool':c['itemName']='relocator'
            else:d='world.spawnProjectile("wrongprojectile", position)'
            with self.subTest(target=target),self.assertRaisesRegex(ValueError,'v0.81 trial'):
                gate.validate_trial_evidence(a,b,c,d)

    def test_layered_source_and_exact_approved_translation_membership(self):
        gate.validate_manifest(self.manifest,self.catalog,self.review)
        self.assertEqual(sum(r.get('qa',{}).get('layered_source',False) for r in self.manifest['translations']),317)
        wrong=copy.deepcopy(self.manifest)
        next(r for r in wrong['translations'] if r.get('qa',{}).get('layered_source'))['qa']['source_patch']='wrong.patch'
        with self.assertRaisesRegex(ValueError,'provenance'):
            gate.validate_manifest(wrong,self.catalog,self.review)
        wrong=copy.deepcopy(self.manifest);wrong['translations'][0]['tr']+=' New mechanic.'
        with self.assertRaisesRegex(ValueError,'approved translation'):
            gate.validate_manifest(wrong,self.catalog,self.review)

    def test_static_consumers_include_helpers_and_sender_only_silences(self):
        context=self.review['source_context']
        self.assertEqual((context['message_ids'],context['qualified_static_message_ids'],context['qualified_text_message_ids']),(278,257,255))
        self.assertEqual(len(context['unverified_fields']),22)
        self.assertEqual(context['sender_only_message_ids'],['lethialabs15c','lethialabs15d'])
        self.assertEqual(len({r['message_id'] for r in context['additional_consumer_links']}),15)
        for mid in ['futestdrive00','futestdrive01','futestdrive02','futestdrive03','futestdrive03b','futestdrive03c','futestdrive04','futestdrive05','testdrive05']:
            self.assertTrue(any(r['radio_context'] and '<encoded-json>' in r.get('pointer','') for r in context['references'][mid]))
        self.assertEqual(self.review['lqa_status'],'NOT TESTED')

    def test_one_old_mission_hook_name_matches_its_prior_manifest(self):
        fixes=self.review['maintenance'];self.assertEqual(len(fixes),1);fix=fixes[0]
        rows={(r['asset'],r['pointer']):r for r in self.catalog['translations']}
        old={(r['asset'],r['pointer']):r for r in read(TOOLS/'v046_translations.json')['translations']}
        key=(fix['asset'],fix['pointer']);self.assertEqual(rows[key]['tr'],fix['after']);self.assertEqual(old[key]['tr'],fix['after'])
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            Terminology(self.policy).validate(dict(rows[key],tr=fix['before']))


if __name__=='__main__':
    unittest.main()
