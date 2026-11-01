"""Protect Volcano Base event scope, tone, sources and narrow term permissions."""
import copy
import sys
import unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v087 as gate

class V087Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v087_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.review=read(TOOLS.parent/'docs/reviews/volcanobase-20261101.json');cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_manifest_provenance_and_neighbor_closed(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('pointer','/scriptConfig/dialog/follower/attack/neighbor/0'),('asset','npcs/volcanobase/unknown.npctype'),('en','Invented line'),('tr','Başka bir replik.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_nine_delivered_regressions_and_all_reply_locks(self):
  engine=Terminology(self.policy);changes=self.review['corrections'];self.assertEqual(len(changes),9);self.assertEqual(sum(c['changed_sentences']for c in changes),10)
  for c in changes:
   r=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=c['before']))
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_follower_events_are_not_flattened_or_reordered(self):
  rows=[r for r in self.manifest['translations']if '/dialog/follower/'in r['pointer']];self.assertEqual(len(rows),18)
  from collections import Counter
  self.assertEqual(dict(Counter(r['pointer'].split('/')[4]for r in rows)),dict(attack=3,join=3,returnFromCombat=5,returnFromWait=3,wait=4))
  en='Unhappy. Must you go on without me? I wish to fight for glory!';self.assertIn('zorunda mısın?',self.row(en)['tr']);self.assertIn('Şan kazanmak için',self.row(en)['tr'])
 def test_pike_loan_favourite_and_slaughter_meaning(self):
  rows=self.manifest['translations'];smug=next(r for r in rows if 'lend your head'in r['en']);self.assertIn('onca mızrağımdan',smug['tr']);self.assertIn('ödünç ver',smug['tr']);self.assertNotIn('Bir adım',smug['tr'])
  hero=next(r for r in rows if 'my favourite type'in r['en']);self.assertIn('en sevdiğim tip',hero['tr']);self.assertNotIn('kahramanımız',hero['tr'])
  slaughters=[r for r in rows if 'slaughter'in r['en']];self.assertEqual(len(slaughters),2);self.assertTrue(all('katle'in r['tr']for r in slaughters))
 def test_moods_roar_hiss_and_existing_title_retained_without_english_permission(self):
  rows=self.manifest['translations'];self.assertEqual(self.row('Enraged. Raaaarrrgh!')['tr'],'Çileden çıkmış. Raaaarrrgh!');self.assertEqual(self.row('I have nothing to sssay to you')['tr'],'Sana sssöyleyecek bir şeyim yok.')
  self.assertEqual(next(t for t in self.policy['terms']if t['source']=='a Protector')['tr'],'Protector');self.assertEqual(self.review['new_locked_terms'],44);self.assertEqual(self.review['reused_locked_names'],['Attack!'])
  for r in rows:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='A Protector needs help.',tr='A Protector needs help.',occurrences=[dict(asset='fixture',pointer='/text')])))
 def test_warlord_singular_plural_and_neighbor_meanings(self):
  engine=Terminology(self.policy)
  for en,tr in [('The warlord is waiting.','Savaş ağası bekliyor.'),('Fear the warlords!','Savaş ağalarından kork!')]:engine.validate(dict(asset='fixture',pointer='/text',en=en,tr=tr))
  with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(asset='fixture',pointer='/text',en='The warlord is waiting.',tr='Savaş beyi bekliyor.'))
  engine.validate(dict(asset='fixture',pointer='/text',en='An arrow through an eye.',tr='Göze saplanan bir ok.'))
 def test_main_micro_and_tenant_contexts_not_collapsed(self):
  c=self.review['source_context'];main=c['maps']['dungeons/missions/volcanobase/volcanobase.json'];self.assertEqual(len(main['placements']),58);self.assertEqual(c['main_placement_counts']['volcanobasebrute'],11);self.assertEqual(c['main_placement_counts']['volcanobasesentinel'],16)
  self.assertEqual(sum(len(m['placements'])for a,m in c['maps'].items()if '/microdungeons/'in a),6);self.assertEqual(c['tenant']['tenants'][0]['species'],'fumantizi');self.assertEqual(c['tenant']['tenants'][0]['type'],'volcanobasefollower');self.assertEqual(c['radio_definition_count'],21)
 def test_technical_fields_and_unverified_runtime_remain_outside_claims(self):
  import build_validate as build
  self.assertEqual(len(build.V087_VOLCANOBASE_FIELDS),48)
  for r in self.manifest['translations']:self.assertIn((r['asset'],r['pointer']),build.V087_VOLCANOBASE_FIELDS)
  for pointer in ('/type','/baseType','/identity/name','/scriptConfig/dialogMode','/damageTeamType'):
   self.assertNotIn(('npcs/volcanobase/volcanobasehostage.npctype',pointer),build.V087_VOLCANOBASE_FIELDS)
  c=self.review['source_context'];self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');main=c['maps']['dungeons/missions/volcanobase/volcanobase.json'];self.assertEqual(main['wire_count'],204);self.assertEqual(sum(not x['exists']for x in main['tilesets']),30)
if __name__=='__main__':unittest.main()
