"""Regressions for Sunset Riders negation, modality and exact source scope."""
import copy
import sys
import unittest
from collections import Counter
from pathlib import Path

TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v091 as gate

class V091Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v091_translations.json');cls.catalog=read(TOOLS/'ceviriler.json')
  cls.review=read(TOOLS.parent/'docs/reviews/sunset-20261105.json');cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_manifest_and_neighbor_scope_are_closed(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('pointer','/scriptConfig/dialog/attack/default/default/999'),('asset','npcs/hostilefu.npctype'),('en','A different cowboy reply.'),('tr','Başka bir replik.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_all_language_regressions_reject_original_wording(self):
  engine=Terminology(self.policy);changes=self.review['corrections']
  self.assertEqual(len(changes),13);self.assertEqual(sum(c['changed_sentences']for c in changes),14)
  for c in changes:
   r=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=c['before']))
 def test_every_occurrence_is_locked_against_wrong_translation(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_speaker_events_and_repeated_variants(self):
  rows=self.manifest['translations']
  self.assertEqual(dict(Counter(r['pointer'].split('/')[3]for r in rows)),dict(attack=28,converse=18))
  self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[2,2,3,7,8,8,16])
  variants=[r for r in rows if r['en']=='I feel like I might need to shoot you now!']
  self.assertEqual(len(variants),3);self.assertEqual({r['tr']for r in variants},{'Sanırım artık seni vurmam gerekebilir!'})
 def test_hank_denials_amount_and_frontier_direction(self):
  first=self.row("I ain't kilt nobody, I swear it. It was that eyed tentercle thang!")['tr']
  self.assertIn('Kimseyi öldürmedim',first);self.assertNotIn('tek göz',first)
  denial=self.row("Fer the last time...I ain't kilt no girl and I ain't let no creature snack on 'er!")['tr']
  self.assertTrue(denial.startswith('Son kez söylüyorum...'));self.assertIn('Ne bir kızı öldürdüm ne de bir yaratığın',denial);self.assertIn('izin verdim',denial)
  bounty=next(r['tr']for r in self.manifest['translations']if r['en'].startswith('Two thousand'))
  self.assertIn('sağ ya da ölü',bounty);self.assertIn('iki bin',bounty);self.assertNotIn('2000',bounty)
  frontier=next(r['tr']for r in self.manifest['translations']if r['en'].startswith("We're pretty far"))
  self.assertIn('Sınır boyunda',frontier);self.assertNotIn('boyunun',frontier)
 def test_name_locks_do_not_preserve_ordinary_english_or_neighbors(self):
  engine=Terminology(self.policy)
  for en in ['Hawkeye Hank','Hawkeye','Hank','Ginger','Fort Nova','Screwbolt']:
   r=dict(asset='fixture',pointer='/text',en=en,tr=en);engine.validate(r)
   with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='Başka'))
  for r in self.manifest['translations']:
   self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='Hank needs help.',tr='Hank needs help.',occurrences=[dict(asset='fixture',pointer='/text')])))
  engine.validate(dict(asset='fixture',pointer='/text',en='The ginger root is fresh.',tr='Zencefil kökü taze.'))
 def test_missing_dependencies_are_not_live_proof(self):
  ctx=self.review['source_context'];mission=ctx['mission']
  self.assertFalse(ctx['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED')
  self.assertEqual(ctx['related_review_rows'],2);self.assertEqual(mission['missing_tilesets'],18)
  self.assertEqual(mission['available_fu_tilesets'],2);self.assertEqual(len(mission['tileset_references']),20)
  self.assertEqual(mission['money_range'],[2000,2000]);self.assertEqual(mission['radio_stagehands'],7);self.assertEqual(len(mission['radio_ids']),9)
  self.assertEqual(mission['monster_layer_objects'],73);self.assertFalse(mission['spawn_or_live_path_tested'])
  self.assertIn('behaviors/npc/spectator.behavior',ctx['missing_vanilla_dependencies'])
 def test_technical_ids_and_sound_policy_remain_closed(self):
  import build_validate as build
  self.assertEqual(len(build.V091_SUNSET_FIELDS),46)
  for r in self.manifest['translations']:self.assertIn((r['asset'],r['pointer']),build.V091_SUNSET_FIELDS)
  for asset,pointer in [('sunsethank','/identity/name'),('sunsetsheriff','/scriptConfig/behavior'),('sunsetvillager','/baseType'),('sunsetshotgun','/statusControllerSettings/stats/powerMultiplier/baseValue')]:
   self.assertNotIn(('npcs/sunsetriders/'+asset+'.npctype',pointer),build.V091_SUNSET_FIELDS)
  self.assertEqual(self.row('Yeeeeeeehaw!')['tr'],'Vuhuuuu!');self.assertEqual(self.review['preserve_bindings'],[])
  self.assertEqual(self.review['new_locked_terms'],35);self.assertEqual(self.review['locked_total'],1187)

if __name__=='__main__':unittest.main()
