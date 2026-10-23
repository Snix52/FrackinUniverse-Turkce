"""Protect reviewed guard/chef language, direct-source scope and narrow policy."""
import copy
import sys
import unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology,validate_format
import generate_v083 as gate

class V083Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=read(TOOLS/'v083_translations.json');cls.catalog=read(TOOLS/'ceviriler.json')
        cls.review=read(TOOLS.parent/'docs/reviews/mobs-20261023.json');cls.policy=read(TOOLS/'locked_terms.json')

    def test_exact_direct_source_scope_rejects_added_or_neighbor_fields(self):
        gate.validate_manifest(self.manifest,self.catalog,self.review)
        self.assertEqual(len(self.manifest['translations']),66)
        self.assertTrue(all('qa' not in r for r in self.manifest['translations']))
        for key,value in [('pointer','/scriptConfig/dialog/attack/default/default/99'),('asset','npcs/mobs/friendlycastleguard.npctype'),('tr','Invented new mechanic')]:
            wrong=copy.deepcopy(self.manifest);wrong['translations'][0][key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):
                gate.validate_manifest(wrong,self.catalog,self.review)

    def test_source_provenance_cannot_be_changed_to_layered(self):
        wrong=copy.deepcopy(self.manifest);wrong['translations'][0]['qa']={'layered_source':True,'source_patch':'wrong.patch'}
        with self.assertRaisesRegex(ValueError,'provenance'):
            gate.validate_manifest(wrong,self.catalog,self.review)

    def test_all_sixteen_delivered_language_regressions_are_rejected(self):
        engine=Terminology(self.policy);changes=self.review['corrections'];self.assertEqual(len(changes),16)
        self.assertEqual(sum(c['changed_sentences'] for c in changes),20)
        for c in changes:
            row=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(row)
            with self.subTest(pointer=row['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):
                engine.validate(dict(row,tr=c['before']))

    def test_all_thirtyone_full_replies_locked_and_ordinary_english_not_preserved(self):
        engine=Terminology(self.policy)
        self.assertEqual(len(self.review['new_locked_names']),31)
        for row in self.manifest['translations']:
            engine.validate(row)
            with self.subTest(pointer=row['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):
                engine.validate(dict(row,tr='Alakasız bir cümle.'))
            for pointer,en in [(row['pointer'],row['en']),(row['pointer']+'/neighbor','The guard needs help.')]:
                self.assertFalse(preserved_name(dict(en=en,tr=en,occurrences=[dict(asset=row['asset'],pointer=pointer)])))

    def test_repeated_guard_emotion_and_second_person_are_consistent(self):
        rows=[r for r in self.manifest['translations'] if '/hail/' in r['pointer']]
        self.assertEqual(len(rows),44)
        for en in {r['en'] for r in rows}:
            self.assertEqual(len({r['tr'] for r in rows if r['en']==en}),1)
        for r in rows:
            if r['en'].startswith('Intimidating.'):self.assertTrue(r['tr'].startswith('Göz korkutucu.'))
            if r['en'].startswith('Contemptuous.'):self.assertEqual(r['tr'],'Küçümseyici. Ne iğrenç bir yaratıksın!')

    def test_chef_emphasis_compound_and_natural_floran_hiss(self):
        rows=[r for r in self.manifest['translations'] if '/attack/' in r['pointer']]
        self.assertEqual(len(rows),22)
        for r in rows:
            validate_format(r,read(TOOLS/'rules/text_integrity.json'))
            if 'RAAAAAAWWWWW' in r['en']:
                self.assertIn('resmen ÇİİİİİİĞ!!!',r['tr']);self.assertNotIn("Frackin'",r['tr'])
            if 'AN IDIOT' in r['en']:self.assertIn('BİR APTAL ',r['tr']);self.assertTrue(r['tr'].endswith('SANDVİÇİ!') or r['tr'].endswith('SSSSSANDVİÇİ!'))
            if 'fressssh' in r['en']:self.assertEqual(r['tr'],'İşte ssssana bugünün taze eti!');self.assertNotIn('tazess',r['tr'])
            if r['en'].startswith('Enraged.'):self.assertTrue(r['tr'].startswith('Çileden çıkmış.'))

    def test_inheritance_and_static_spawn_do_not_claim_active_hail(self):
        c=self.review['source_context'];parents={r['npc_type']:r['base_type'] for r in c['npcs']}
        self.assertEqual(parents,dict(castleguard='hostilefu',castleguardbasic='villageguard',castleguardlookout='hostilelookout',castleroyalguard='hostilefu',fuevilchef='hostilefu'))
        self.assertEqual(sum(r['fields'] for r in c['npcs']),66)
        self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED')
        links=[r for r in c['spawn_references'] if r['data'].get('typeName')=='castleguardlookout']
        self.assertEqual(len(links),1);self.assertIn('glitchunderground',links[0]['source'])
        bandit=next(r for r in c['spawn_references'] if 'banditasteroid' in r['source'])
        self.assertEqual(bandit['data']['npcTypes'],['fuevilchef']);self.assertNotIn('npcSpecies',bandit['data'])

    def test_exact_allowlist_excludes_machine_identifiers_and_wrong_event(self):
        import build_validate as build
        for r in self.manifest['translations']:self.assertTrue(build.allowed(r['asset'],r['pointer']))
        for asset,pointer in [('npcs/mobs/precursormob.npctype','/scriptConfig/behavior'),('npcs/mobs/fuevilchef.npctype','/baseType'),('npcs/mobs/castleguard.npctype','/scriptConfig/dialog/attack/default/default/0')]:
            self.assertNotIn((asset,pointer),build.V083_MOB_FIELDS)
            self.assertFalse(build.allowed(asset,pointer))

if __name__=='__main__':unittest.main()
