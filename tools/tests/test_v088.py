"""Guard Ancient Temple source scope, rescue tone and narrow dialogue locks."""
import copy
import sys
import unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v088 as gate

class V088Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v088_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.review=read(TOOLS.parent/'docs/reviews/ancienttemple-20261102.json');cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_manifest_provenance_and_neighbor_closed(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('pointer','/scriptConfig/dialog/follower/attack/neighbor/0'),('asset','npcs/ancienttemple/unknown.npctype'),('en','Invented line'),('tr','Başka bir replik.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_three_regressions_and_every_exact_reply_lock(self):
  engine=Terminology(self.policy);changes=self.review['corrections'];self.assertEqual(len(changes),3);self.assertEqual(sum(c['changed_sentences']for c in changes),3)
  for c in changes:
   row=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(row)
   with self.subTest(pointer=row['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(row,tr=c['before']))
  for row in self.manifest['translations']:
   engine.validate(row)
   with self.subTest(pointer=row['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(row,tr='İlgisiz bir cümle.'))
 def test_follower_event_nesting_and_rescue_intent(self):
  rows=[r for r in self.manifest['translations']if '/dialog/follower/'in r['pointer']];self.assertEqual(len(rows),15)
  self.assertEqual(dict(Counter(r['pointer'].split('/')[4]for r in rows)),dict(attack=2,join=2,returnFromCombat=5,returnFromWait=3,wait=3))
  self.assertIn('edecektin, öyle mi?',self.row('Sacrifice me, will you?')['tr'])
  escape=self.row("I'll escape or die trying!")['tr'];self.assertTrue(escape.startswith('Ya '));self.assertIn('ya da kaçmaya çalışırken öleceğim',escape);self.assertNotIn('ölsem bile',escape)
 def test_priest_repeated_occurrences_keep_force_and_hesitation(self):
  rows=[r for r in self.manifest['translations']if r['asset'].endswith(('battlepriest.npctype','templehighpriest.npctype'))];self.assertEqual(len(rows),28)
  groups={}
  for row in rows:groups.setdefault(row['en'],[]).append(row)
  self.assertEqual(len(groups),14)
  for variants in groups.values():self.assertEqual(len(variants),2);self.assertEqual(len({r['tr']for r in variants}),1)
  self.assertEqual(self.row('I... I must destroy you, heretic! I have no choice!')['tr'],'Ben... Seni yok etmeliyim, sapkın! Başka çarem yok!')
  self.assertIn('katletmeye zorluyor',self.row('The power of Kluex compels me to slay you!')['tr'])
 def test_grounded_name_does_not_preserve_ordinary_english_or_other_sense(self):
  engine=Terminology(self.policy);engine.validate(dict(asset='fixture',pointer='/text',en='Grounded',tr='Grounded'))
  with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(asset='fixture',pointer='/text',en='Grounded',tr='Yere Bağlılar'))
  engine.validate(dict(asset='fixture',pointer='/text',en='This wire is grounded.',tr='Bu tel topraklanmış.'))
  for row in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=row['en'],tr=row['en'],occurrences=[dict(asset=row['asset'],pointer=row['pointer'])])))
  self.assertFalse(preserved_name(dict(en='The Grounded need help.',tr='The Grounded need help.',occurrences=[dict(asset='fixture',pointer='/text')])))
 def test_flame_and_ashes_meaning_without_new_identity(self):
  self.assertEqual(self.row('Ashes to ashes!')['tr'],'Külden küle!')
  self.assertEqual(self.row('Be wreathed in holy flame!')['tr'],'Kutsal alevler seni sarsın!')
  self.assertEqual(self.row('I shall purify your mind with my sacred flame!')['tr'],'Kutsal alevimle zihnini arındıracağım!')
  self.assertEqual(self.review['new_locked_terms'],24);self.assertEqual(len(self.review['reused_locked_names']),10)
 def test_static_map_registration_and_radio_counts_remain_separate(self):
  c=self.review['source_context'];self.assertEqual(c['main_placement_counts'],dict(firebird=4,battlepriest=2,templefollower=3,templehighpriest=1));self.assertEqual(c['radio_definition_count'],14);self.assertEqual(len(c['main_radio_ids']),14)
  self.assertEqual(c['worldgen_raw_placement_records'],8);self.assertEqual(c['worldgen_anchor2_maps_to'],'anchor1.json');self.assertFalse(c['worldgen_anchor2_file_registered']);self.assertEqual(c['related_review_rows'],0)
  main=c['maps']['dungeons/missions/ancienttemple/ancienttemple.json'];self.assertEqual(len(main['relevant_spawners']),6);self.assertEqual(main['wire_count'],231);self.assertEqual(sum(not x['exists']for x in main['tilesets']),22)
 def test_technical_fields_and_unverified_runtime_not_claimed(self):
  import build_validate as build
  self.assertEqual(len(build.V088_ANCIENTTEMPLE_FIELDS),48)
  for row in self.manifest['translations']:self.assertIn((row['asset'],row['pointer']),build.V088_ANCIENTTEMPLE_FIELDS)
  for pointer in ('/type','/baseType','/items/override','/scriptConfig/behavior','/movementParameters/runSpeed'):self.assertNotIn(('npcs/ancienttemple/firebird.npctype',pointer),build.V088_ANCIENTTEMPLE_FIELDS)
  self.assertFalse(self.review['source_context']['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED')
if __name__=='__main__':unittest.main()
