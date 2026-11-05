"""Guard merchant dialogue meaning, exact field scope and narrow terminology."""
import copy
import sys
import unittest
from collections import Counter
from pathlib import Path

TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v090 as gate

class V090Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v090_translations.json')
  cls.catalog=read(TOOLS/'ceviriler.json')
  cls.review=read(TOOLS.parent/'docs/reviews/merchants-20261105.json')
  cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_manifest_content_and_neighbor_scope_are_closed(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('pointer','/scriptConfig/dialog/merchant/start/avian/default/999'),('asset','npcs/unsorted-anid/fuwastelandraidertenant.npctype'),('en','A made-up merchant reply.'),('tr','Başka bir replik.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_all_eight_language_regressions_reject_original_wording(self):
  e=Terminology(self.policy);changes=self.review['corrections']
  self.assertEqual(len(changes),8);self.assertEqual(sum(c['changed_sentences']for c in changes),8)
  for c in changes:
   r=dict(c['occurrences'][0],en=c['en'],tr=c['after']);e.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(r,tr=c['before']))
 def test_every_exact_reply_and_caption_has_a_lock(self):
  e=Terminology(self.policy)
  for r in self.manifest['translations']:
   e.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_dialogue_event_speaker_and_title_counts(self):
  rows=self.manifest['translations'];dialog=[r for r in rows if '/dialog/merchant/'in r['pointer']]
  self.assertEqual(len(dialog),53);self.assertEqual(len(rows)-len(dialog),10)
  self.assertEqual(dict(Counter(r['pointer'].split('/')[4]for r in dialog)),dict(converse=3,end=12,follow=8,start=13,tout=3,welcome=14))
  self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[12,14,18,19])
  repeated=[r for r in rows if r['en']=='Live a little, buy a corpse!'];self.assertEqual(len(repeated),3);self.assertEqual(len({r['tr']for r in repeated}),1)
 def test_royal_rarity_need_and_comparative_meanings(self):
  royal=self.row('Plenty of corpses. Got some royal stuff too.')['tr'];self.assertIn('Kraliyete ait mallarım',royal);self.assertNotIn('soylu',royal)
  good=self.row('Good wood! Get good wood here!')['tr'];self.assertNotIn('En iyi',good);self.assertIn('alın',good)
  self.assertIn('nadir',self.row('The rarest stuff in the galaxy!')['tr']);self.assertIn('İhtiyacın',self.row("I've got what you need...")['tr'])
  self.assertEqual(self.row("Whatever you're going to do with them, I don't wanna know.")['tr'],'Onlarla ne yapacağını bilmek istemiyorum.')
 def test_name_locks_do_not_grant_ordinary_english_preservation(self):
  e=Terminology(self.policy)
  for en,tr in [('Penumbrite','Penumbrite'),('Kluex','Kluex'),('Igor','Igor'),('Frankenstein','Frankenstein'),('Blacksmith','Demirci'),('Gravedigger','Mezarcı')]:
   r=dict(asset='fixture',pointer='/text',en=en,tr=tr);e.validate(r)
   with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(r,tr='Başka'))
  e.validate(dict(asset='fixture',pointer='/text',en='The brain is still good.',tr='Beyin hâlâ sağlam.'))
  e.validate(dict(asset='fixture',pointer='/text',en='Her craftsmanship is fine.',tr='İşçiliği iyi.'))
  for r in self.manifest['translations']:
   self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='Igor needs help.',tr='Igor needs help.',occurrences=[dict(asset='fixture',pointer='/text')])))
 def test_missing_consumer_and_source_copy_are_not_live_proof(self):
  c=self.review['source_context'];self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertEqual(c['related_review_rows'],26)
  self.assertEqual(sorted(c['pool_item_counts'].values()),[4,4,13,14]);self.assertEqual(len(c['tenants']),4)
  self.assertFalse(c['nested_smuggler_ui']['active_nested_consumer_verified']);self.assertFalse(c['nested_smuggler_ui']['technical_structure_changed'])
  self.assertEqual(self.row(' Geologist')['tr'],' Jeolog');self.assertEqual(self.row('  Smuggler')['tr'],'  Kaçakçı')
  self.assertIn('npcs/merchanttenant.npctype',c['missing_vanilla_dependencies'])
 def test_technical_data_typos_and_layout_spaces_are_retained(self):
  import build_validate as build
  self.assertEqual(len(build.V090_MERCHANT_FIELDS),63)
  for r in self.manifest['translations']:self.assertIn((r['asset'],r['pointer']),build.V090_MERCHANT_FIELDS)
  asset='npcs/unsorted-anid/humansmuggler.npctype'
  for pointer in ['/type','/baseType','/scriptConfig/merchant/interactAction','/scriptConfig/merchant/buyFactorRange/0','/scriptConfig/questGenerator/graduation/nextNpcType/0/1']:
   self.assertNotIn((asset,pointer),build.V090_MERCHANT_FIELDS)
  self.assertEqual(self.row('Legal things for sale!.')['tr'],'Yasal mallar satılık!.')
  self.assertIn('Puruse',self.row('My skill is supreme. Puruse my wares.')['en'])
  self.assertTrue(self.row('  Lethally crafted penumbrite.')['tr'].startswith('  '));self.assertEqual(self.review['new_locked_terms'],63)

if __name__=='__main__':unittest.main()
