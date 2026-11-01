"""Guard against faction-name drift, lost Floran voice and mixed NPC source provenance."""
import copy
import sys
import unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology,validate_format
import generate_v084 as gate

class V084Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v084_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.review=read(TOOLS.parent/'docs/reviews/dungeon-20261101.json');cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations'] if r['en']==en)
 def test_exact_source_scope_rejects_neighbor_and_added_fields(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('pointer','/scriptConfig/dialog/hail/neighbor/0'),('asset','npcs/dungeon/unapproved.npctype'),('tr','A new ability.')]:
   wrong=copy.deepcopy(self.manifest);wrong['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(wrong,self.catalog,self.review)
 def test_thirtyfive_layered_and_thirty_direct_fields_require_exact_provenance(self):
  self.assertEqual(sum(bool(r.get('qa',{}).get('layered_source')) for r in self.manifest['translations']),35)
  wrong=copy.deepcopy(self.manifest);r=next(r for r in wrong['translations'] if 'qa'in r);r['qa']['source_patch']='wrong.patch'
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(wrong,self.catalog,self.review)
  wrong=copy.deepcopy(self.manifest);r=next(r for r in wrong['translations'] if 'qa'not in r);r['qa']={'layered_source':True,'source_patch':r['asset']+'.patch'}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(wrong,self.catalog,self.review)
 def test_all_delivered_regressions_are_locked(self):
  engine=Terminology(self.policy);self.assertEqual(len(self.review['corrections']),34);self.assertEqual(sum(x['changed_sentences'] for x in self.review['corrections']),38)
  for c in self.review['corrections']:
   r=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=c['before']))
 def test_grounded_name_does_not_force_electrical_or_ordinary_english(self):
  engine=Terminology(self.policy);engine.validate(dict(asset='fixture',pointer='/text',en='You are grounded against lightning.',tr='Yıldırıma karşı topraklandın.'))
  name=next(t for t in self.policy['terms'] if t['source']=='Grounded');self.assertEqual(name['mode'],'preserve');self.assertFalse(name.get('enforce_in_text',False))
  self.assertIn('Grounded',self.row('Filthy Grounded scum! Today, you die!')['tr'])
  for en in ('Grounded needs help.','This is ordinary English.','Filthy Grounded scum! Today, you die!'):
   self.assertFalse(preserved_name(dict(en=en,tr=en,occurrences=[dict(asset='npcs/dungeon/aviantemple/templeguard.npctype',pointer='/scriptConfig/dialog/attack/avian/avian/0')])))
 def test_floran_hiss_future_threat_and_source_emphasis(self):
  rows=[r for r in self.manifest['translations'] if r['asset'].endswith('/hellguard.npctype') and '/floran/'in r['pointer']];self.assertEqual(len(rows),7)
  for r in rows:self.assertRegex(r['tr'].casefold(),r's{3,}');validate_format(r,read(TOOLS/'rules/text_integrity.json'))
  r=self.row('Prisssoner will be ssstabbed to death!');self.assertIn('öldürülecek',r['tr']);self.assertNotIn('öldürülmeli',r['tr'])
  self.assertEqual(self.row('There isss no escape!')['tr'],'Kaçamazsssın!')
 def test_authored_hesitation_imperative_and_soul_meanings(self):
  self.assertTrue(self.row('I... I must destroy you, heretic! I have no choice!')['tr'].startswith('Ben...'))
  self.assertTrue(self.row('They... they want you gone...')['tr'].startswith('Onlar... onlar'))
  self.assertEqual(self.row('Die by my sword...')['tr'],'Kılıcımla can ver...')
  self.assertEqual(self.row('Today, Kluex claims another soul!')['tr'],'Bugün Kluex bir ruh daha alacak!')
  self.assertIn('Buna zorlanıyorum',self.row('I must... defend. I am compelled...')['tr'])
 def test_all_six_npc_contexts_have_static_not_live_source_evidence(self):
  c=self.review['source_context'];self.assertEqual((c['direct_fields'],c['layered_fields']),(30,35));self.assertFalse(c['active_consumer_verified'])
  for n in c['npcs']:
   self.assertEqual(n['base_type'],'hostilefu' if n['direct'] else None);self.assertEqual(len(n['entries']),n['fields'])
  self.assertEqual({k:v['files'] for k,v in c['spawn_summary'].items()},dict(labguard=23,labguardlookout=3,templeguard=18,tombguard=5,hellguard=2,pyramidguard=2));self.assertEqual(self.review['lqa_status'],'NOT TESTED')
 def test_old_merchant_faction_is_aligned_and_electrical_text_unchanged(self):
  f=self.review['maintenance'][0];self.assertEqual(f['changed_sentences'],1);self.assertIn('Grounded halkının',f['after'])
  r=next(r for r in self.catalog['translations'] if (r['asset'],r['pointer'])==(f['asset'],f['pointer']));self.assertEqual(r['tr'],f['after'])
  with self.assertRaisesRegex(ValueError,'LOCKED'):Terminology(self.policy).validate(dict(r,tr=f['before']))
  electric=next(r for r in self.catalog['translations'] if r['asset']=='radiomessages/exploration.radiomessages' and r['pointer']=='/ffbiomeelectricsurface/text');self.assertIn('Topraklanacağın'.casefold(),electric['tr'].casefold());self.assertNotIn('Grounded',electric['tr'])
 def test_exact_allowlist_and_full_reply_locks_exclude_motor_ids(self):
  import build_validate as build
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   self.assertTrue(build.allowed(r['asset'],r['pointer']));engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='Alakasız bir cümle.'))
  for pointer in ('/baseType','/scriptConfig/dialog/attack','/scriptConfig/behavior'):
   self.assertNotIn(('npcs/dungeon/apexbase/labguard.npctype',pointer),build.V084_DUNGEON_FIELDS)
if __name__=='__main__':unittest.main()
