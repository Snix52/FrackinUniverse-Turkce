"""Protect Magicka dialogue meanings, Glitch moods and source limitations."""
import copy
import sys
import unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v093 as gate

class V093Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v093_translations.json');cls.catalog=read(TOOLS/'ceviriler.json')
  cls.review=read(TOOLS.parent/'docs/reviews/magicka-20261105.json');cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_manifest_and_neighbor_scope_are_closed(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('pointer','/scriptConfig/dialog/attack/default/default/999'),('asset','npcs/hostilefu.npctype'),('en','A made-up monastery reply.'),('tr','Başka bir replik.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_all_four_regressions_reject_luna_original(self):
  engine=Terminology(self.policy);changes=self.review['corrections'];self.assertEqual(len(changes),4);self.assertEqual(sum(c['changed_sentences']for c in changes),4)
  for c in changes:
   r=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=c['before']))
 def test_every_occurrence_rejects_wrong_translation(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_events_repeated_taunts_and_emotion_prefixes(self):
  rows=self.manifest['translations'];self.assertEqual(dict(Counter(r['pointer'].split('/')[3]for r in rows)),dict(attack=18,converse=10));self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[4,7,7,10])
  guard=[r for r in rows if '/converse/glitch/'in r['pointer']];self.assertEqual(len(guard),9)
  self.assertEqual([r['tr'].split('.')[0]for r in guard],['Gergin','Endişeli','İyimser','Tereddütlü','Maceracı','Ciddi','Umutlu','İçten','Kararlı'])
  repeated=[r for r in rows if r['en']=='Tae battle!'];self.assertEqual(len(repeated),2);self.assertEqual({r['tr']for r in repeated},{'Savaşa!'})
 def test_service_period_passive_protection_and_present_capability(self):
  self.assertEqual(self.row('Nervous. This is my first tour of duty.')['tr'],'Gergin. İlk görev dönemimdeyim.')
  protect=self.row('Determined. These monasteries preserve much knowledge and culture in these dark times. They must be protected.')['tr'];self.assertTrue(protect.endswith('Korunmaları gerekiyor.'));self.assertNotIn('korumalıyız',protect)
  question=self.row('Tae Glitch can only send a wee craven to face me?')['tr'];self.assertIn('gönderebiliyor',question);self.assertNotIn('çıkarabildi',question);self.assertIn('küçücük bir korkak',question)
 def test_metaphors_do_not_invent_equipment_or_quest_mechanics(self):
  self.assertIn('hazırlıksız',self.row("Hopin' tae catch me with mah socks off, were ye?")['tr'])
  shear=self.row('Earnest. Shear a handful of those overgrown sheep for me, will you?')['tr'];self.assertIn('kırkıver',shear)
  c=self.review['source_context'];self.assertFalse(c['mission']['spawn_or_live_path_tested']);self.assertEqual(self.review['format_review']['control_exceptions_added'],0);self.assertEqual(self.review['preserve_bindings'],[])
 def test_names_and_terms_do_not_preserve_ordinary_english(self):
  engine=Terminology(self.policy)
  for en,tr in [('Glitch','Glitch'),('Alpaca','Alpaka'),('Monastery','Manastır'),('Grim.','Ciddi.')]:
   r=dict(asset='fixture',pointer='/text',en=en,tr=tr);engine.validate(r)
   with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='Başka'))
  for en,tr in [('There was a glitch in the signal.','Sinyalde bir hata vardı.'),('A grim fate.','Kasvetli bir kader.'),('A brave champion.','Cesur bir şampiyon.')]:engine.validate(dict(asset='fixture',pointer='/text',en=en,tr=tr))
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='Glitch need help.',tr='Glitch need help.',occurrences=[dict(asset='neighbor',pointer='/scriptConfig/dialog/converse/default/default/0')])))
 def test_missing_dependencies_species_and_technical_exclusions(self):
  import build_validate as build
  c=self.review['source_context'];m=c['mission'];self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertTrue(m['mixed_tiled_properties']);self.assertEqual(m['npc_total'],21);self.assertEqual(m['npc_species'],dict(human=17,glitch=4));self.assertEqual(m['guard_damage_team'],'ghostly')
  self.assertEqual((m['missing_tilesets'],m['available_fu_tilesets'],m['radio_stagehands']),(22,1,0));self.assertEqual(c['related_review_rows'],1);self.assertTrue(m['source_empty_guard_tail'])
  self.assertEqual(len(build.V093_MAGICKA_FIELDS),28)
  for pointer in ['/scriptConfig/behavior','/scriptConfig/dialog/converse/glitch/default/9','/damageTeamType','/baseType']:
   self.assertNotIn(('npcs/magickaforest/magickaguard.npctype',pointer),build.V093_MAGICKA_FIELDS)
  self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(24,1234))

if __name__=='__main__':unittest.main()
