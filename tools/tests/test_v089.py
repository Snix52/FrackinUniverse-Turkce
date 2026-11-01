"""Protect Infiltration dialogue, source provenance and narrow name/reply locks."""
import copy
import sys
import unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v089 as gate
class V089Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v089_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.review=read(TOOLS.parent/'docs/reviews/infiltration-20261102.json');cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_manifest_neighbor_and_provenance_closed(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('pointer','/scriptConfig/dialog/attack/default/neighbor/0'),('asset','npcs/infiltration/unknown.npctype'),('en','Invented line'),('tr','Başka bir replik.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_eight_regressions_and_all_exact_reply_locks(self):
  engine=Terminology(self.policy);changes=self.review['corrections'];self.assertEqual(len(changes),8);self.assertEqual(sum(c['changed_sentences']for c in changes),11)
  for c in changes:
   r=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=c['before']))
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_singular_target_and_no_added_big_intensity(self):
  self.assertEqual(self.row('Rebel scum! Today, you die!')['tr'],'Seni asi pislik! Bugün öleceksin!')
  self.assertEqual(self.row('Why do you fight? You cannot hope to win.')['tr'],'Niye savaşıyorsun? Kazanma umudun yok.')
  self.assertNotIn('büyük',self.row('Opposing Big Ape is a mistake!')['tr']);self.assertIn('büyük hata',self.row('You made a big mistake coming here!')['tr'])
 def test_digging_duration_and_actual_entry_are_retained(self):
  r=next(r for r in self.manifest['translations']if r['en'].startswith('Took me a little while'))
  self.assertIn('biraz zamanımı aldı',r['tr']);self.assertIn('tesisin atık sisteminin bir kısmını',r['tr']);self.assertNotIn('Tesisi ',r['tr'])
  self.assertIn('kolayca içeri girersin',self.row("Just poke at that there console and you'll be in no sweat.")['tr'])
 def test_names_nickname_and_ordinary_english_permission(self):
  e=Terminology(self.policy);e.validate(dict(asset='fixture',pointer='/text',en='Tavish',tr='Tavish'));e.validate(dict(asset='fixture',pointer='/text',en='the mad bomber',tr='Deli Bombacı'))
  for en,tr in [('Tavish','Taviş'),('the mad bomber','Çılgın Bombacı'),('Big Ape','Büyük Maymun')]:
   with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(asset='fixture',pointer='/text',en=en,tr=tr))
  e.validate(dict(asset='fixture',pointer='/text',en='A bomber arrived.',tr='Bir bombardıman uçağı geldi.'))
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='Tavish needs help.',tr='Tavish needs help.',occurrences=[dict(asset='fixture',pointer='/text')])))
 def test_event_sequence_fallback_and_placeholder_scope(self):
  rows=self.manifest['translations'];self.assertEqual(dict(Counter(r['pointer'].split('/')[3]for r in rows)),dict(attack=7,converse=22))
  fallbacks=[r for r in rows if r['en']=="You shouldn't be seeing this."];self.assertEqual(len(fallbacks),3);self.assertEqual({r['tr']for r in fallbacks},{'Bunu görüyor olmamalısın.'})
  r=next(r for r in rows if '<entityname>'in r['en']);self.assertEqual(r['tr'].count('<entityname>'),1)
  n={x['type']:x for x in self.review['source_context']['npcs']};self.assertEqual(n['infiltrationleader']['dialog_mode'],'sequence');self.assertEqual(n['infiltrationtavish']['identity']['name'],'Tavish')
 def test_static_counts_related_sources_and_no_live_claim(self):
  c=self.review['source_context'];self.assertEqual(c['main_placement_counts'],dict(infiltrationelite=8,infiltrationrebel=3,infiltrationleader=1,infiltrationtavish=1));self.assertEqual(c['radio_definition_count'],21);self.assertEqual(c['main_radio_id_count'],22);self.assertEqual(c['additional_radio']['id'],'needMicrosphere');self.assertFalse(c['additional_radio']['translation_changed']);self.assertEqual(c['related_review_rows'],5)
  other=[x for x in c['related_contexts']if 'exact_type_name_counts'in x];self.assertEqual([x['exact_type_name_counts']for x in other],[{},{},{'apexscout':1},{'apexscout':2},{'apexscout':3}]);self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED')
 def test_technical_fields_and_source_typos_not_silently_repaired(self):
  import build_validate as build
  self.assertEqual(len(build.V089_INFILTRATION_FIELDS),29)
  for r in self.manifest['translations']:self.assertIn((r['asset'],r['pointer']),build.V089_INFILTRATION_FIELDS)
  for p in ('/type','/baseType','/identity/name','/scriptConfig/dialogMode','/scriptConfig/behavior'):self.assertNotIn(('npcs/infiltration/infiltrationtavish.npctype',p),build.V089_INFILTRATION_FIELDS)
  self.assertTrue(any('would that close'in r['en']for r in self.manifest['translations']));self.assertTrue(any('radioed me to let you know you were coming'in r['en']for r in self.manifest['translations']));self.assertEqual(self.review['new_locked_terms'],26)
if __name__=='__main__':unittest.main()
