"""Keep Pavillion meanings, proper identities and technical source scope closed."""
import copy
import sys
import unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v092 as gate

class V092Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v092_translations.json');cls.catalog=read(TOOLS/'ceviriler.json')
  cls.review=read(TOOLS.parent/'docs/reviews/pavillion-20261105.json');cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_manifest_and_neighbor_scope_are_closed(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('pointer','/scriptConfig/dialog/attack/hylotl/default/999'),('asset','npcs/hostilefu.npctype'),('en','A made-up castle reply.'),('tr','Başka bir replik.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_all_six_regressions_reject_luna_original(self):
  engine=Terminology(self.policy);changes=self.review['corrections']
  self.assertEqual(len(changes),6);self.assertEqual(sum(c['changed_sentences']for c in changes),6)
  for c in changes:
   r=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=c['before']))
 def test_every_occurrence_rejects_wrong_translation(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_events_speaker_branches_and_repeats(self):
  rows=self.manifest['translations'];self.assertEqual(dict(Counter(r['pointer'].split('/')[3]for r in rows)),dict(attack=23,converse=5,speak=1))
  self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[5,5,6,6,7])
  pairs=[r for r in rows if r['en']=="B-But I'm just a conscript..."];self.assertEqual(len(pairs),2);self.assertEqual({r['tr']for r in pairs},{'A-Ama ben sadece zorunlu askerlik yapıyorum...'})
 def test_identity_difference_is_preserved_and_thousand_has_no_added_actor(self):
  self.assertIn('Kigai',self.row('For the glory of Shogun Kigai!')['tr'])
  self.assertNotIn('Takeshi',self.row('For the glory of Shogun Kigai!')['tr'])
  mission=self.review['source_context']['mission'];self.assertEqual((mission['quest_shogun'],mission['samurai_shogun']),('Takeshi','Kigai'))
  blows=self.row('A thousand blows shall rain upon you!')['tr'];self.assertIn('bin darbe',blows);self.assertNotIn('yağdıracağım',blows)
  quote=next(r['tr']for r in self.manifest['translations']if r['en'].startswith('It is said,'));self.assertIn('bin savaştan',quote);self.assertTrue(quote.endswith('Kazanma umudun yok.'))
 def test_room_location_and_servile_metaphor_remain_source_bound(self):
  route=next(r['tr']for r in self.manifest['translations']if r['en'].startswith('We need to get out'))
  self.assertIn('Belki yukarıdaki odada bulunan Işınlayıcıyı',route);self.assertNotIn('üst kattaki',route)
  insult=self.row("One of the princess' lapdogs! Time to test my blade on you!")['tr'];self.assertIn('Prensesin uşaklarından biri!',insult);self.assertNotIn('kucak köpe',insult)
 def test_no_ordinary_english_or_neighbor_sound_preservation(self):
  engine=Terminology(self.policy)
  for en,tr in [('Koto','Koto'),('Kigai','Kigai'),('Takeshi','Takeshi'),('Shogun','Şogun')]:
   r=dict(asset='fixture',pointer='/text',en=en,tr=tr);engine.validate(r)
   with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='Başka'))
  for r in self.manifest['translations']:
   self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  for en in ['Koto needs help.','Banzai!','Yaaaaaah!']:
   self.assertFalse(preserved_name(dict(en=en,tr=en,occurrences=[dict(asset='neighbor',pointer='/scriptConfig/dialog/attack/default/default/0')])))
  self.assertEqual(self.row('Banzai!')['tr'],'Hücuuum!');self.assertEqual(self.review['preserve_bindings'],[])
 def test_missing_dependencies_ghostly_and_technical_exclusions_are_honest(self):
  import build_validate as build
  c=self.review['source_context'];m=c['mission'];self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED')
  self.assertEqual(m['princess_damage_team'],'ghostly');self.assertEqual(m['npc_total'],54);self.assertEqual(m['monster_layer_objects'],59);self.assertEqual(m['npc_placements']['pavillionsamurai'],13)
  self.assertEqual((m['missing_tilesets'],m['available_fu_tilesets'],m['radio_stagehands']),(27,1,0));self.assertEqual(c['related_review_rows'],3)
  self.assertEqual(len(build.V092_PAVILLION_FIELDS),29)
  for pointer in ['/scriptConfig/dialogMode','/scriptConfig/behavior','/scriptConfig/turnInQuests/0','/identity/name','/damageTeamType']:
   self.assertNotIn(('npcs/pavillion/pavillionprincess.npctype',pointer),build.V092_PAVILLION_FIELDS)
  self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(23,1210))

if __name__=='__main__':unittest.main()
