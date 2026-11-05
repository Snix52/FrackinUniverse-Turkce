"""Reject scope drift, wrong religious meanings and invented runtime approval."""
import copy,sys,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v095 as gate

class V095Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v095_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/skytemple-20261105.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_scope_neighbor_and_source_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for k,v in [('asset','npcs/hostilefu.npctype'),('pointer','/scriptConfig/behavior'),('en','Faith proves a new mechanic.'),('tr','Kaynakta olmayan bir güç.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][k]=v
   with self.subTest(k=k),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_occurrence_rejects_unrelated_translation(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(asset=r['asset'],pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_repeated_lines_and_actual_speaker_branches(self):
  rows=self.manifest['translations'];self.assertEqual(dict(Counter(r['pointer'].split('/')[3]for r in rows)),dict(attack=20));self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[5,5,5,5])
  for en,count in [('Attack!',3),('Protect the temple!',3),('You dare intrude upon the most holy of places?',3),('The divine light of Kluex empowers me to slay you!',2)]:
   group=[r for r in rows if r['en']==en];self.assertEqual(len(group),count);self.assertEqual(len({r['tr']for r in group}),1)
  sun=[r for r in rows if r['asset'].endswith('skytemplesunsword.npctype')];self.assertTrue(all('/attack/default/default/'in r['pointer']for r in sun));self.assertEqual(sum('/attack/avian/default/'in r['pointer']for r in rows),12)
 def test_religious_aether_is_distinct_from_world_name(self):
  engine=Terminology(self.policy);r=self.row('You are not worthy of ascending to the aether!');self.assertIn('Etere',r['tr']);engine.validate(r)
  with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=r['tr'].replace('Etere','Aether’a')))
  chill=self.row('The piercing wrath of the aether will chill you, fiend!');self.assertIn('Eterin',chill['tr']);self.assertIn('üşütecek',chill['tr'])
  engine.validate(dict(asset='fixture',pointer='/shortdescription',en='Aether',tr='Aether'))
  with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(asset='fixture',pointer='/shortdescription',en='Aether',tr='Eter'))
 def test_kluex_and_taunts_do_not_add_names_or_profanity(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   if'Kluex'in r['en']:
    self.assertIn('Kluex',r['tr'])
    with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=r['tr'].replace('Kluex','BaşkaTanrı')))
  self.assertIn('aptal',self.row('Begone, fool!')['tr']);self.assertIn('işgalci',self.row('My thorns will crush you, interloper!')['tr'])
 def test_all_retained_text_is_reviewed_without_fake_corrections(self):
  self.assertEqual(self.review['corrections'],[]);self.assertEqual(self.review['changes']['total_corrected_sentences'],0);self.assertEqual(self.review['changes']['total_corrected_fields'],0);self.assertTrue(self.review['runtime_review']['reviewed']);self.assertEqual(len(self.manifest['translations']),20);self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(12,1260))
 def test_proper_names_do_not_preserve_ordinary_english_dialogue(self):
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='Kluex empowers me.',tr='Kluex empowers me.',occurrences=[dict(asset='neighbor',pointer='/scriptConfig/dialog/attack/default/default/0')])));self.assertEqual(self.review['preserve_bindings'],[]);self.assertEqual(self.review['context_bindings'],[])
 def test_actual_source_inventory_and_missing_consumers_stay_explicit(self):
  import build_validate as build
  c=self.review['source_context'];m=c['mission'];self.assertEqual(Counter(x['base_type']for x in c['npcs']),dict(hostilefu=3,hostile=1));self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertFalse(m['spawn_or_live_path_tested']);self.assertEqual((m['npc_total'],m['selected_npc_total'],m['other_npc_total']),(39,34,5));self.assertEqual(m['npc_species'],dict(avian=39));self.assertEqual(len(m['radio_stagehands']),18);self.assertEqual(len(m['radio_unique_ids']),36);self.assertEqual((len(m['tileset_references']),m['missing_tilesets'],m['available_fu_tilesets']),(28,27,1));self.assertEqual(c['related_review_rows'],0)
  self.assertEqual(len(build.V095_SKYTEMPLE_FIELDS),20)
  for a in self.review['scope']['assets']:
   for p in ['/baseType','/scriptConfig/behavior','/statusControllerSettings/stats/maxHealth/baseValue']:self.assertNotIn((a,p),build.V095_SKYTEMPLE_FIELDS)

if __name__=='__main__':unittest.main()
