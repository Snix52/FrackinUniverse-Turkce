"""Reject dialogue scope drift, invented identities and false runtime approval."""
import copy,sys,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v096 as gate

class V096Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v096_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/colourful-20261106.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_scope_neighbor_and_source_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for k,v in [('asset','npcs/biome/shroommerchant.npctype'),('pointer','/scriptConfig/questGenerator/pools/0'),('en','A new experiment created me.'),('tr','Kaynakta olmayan bir deney.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][k]=v
   with self.subTest(k=k),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_occurrence_rejects_unrelated_translation(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_actual_speaker_target_branches_and_repeated_fallback(self):
  rows=self.manifest['translations'];self.assertEqual(dict(Counter('/'.join(r['pointer'].split('/')[4:6])for r in rows)),{'apex/apex':8,'apex/default':7,'default/default':1})
  same=[r for r in rows if r['en']=='What... have I become?'];self.assertEqual(len(same),2);self.assertEqual({r['tr']for r in same},{'Neye... dönüştüm ben?'})
  self.assertEqual(len({r['en']for r in rows}),15);self.assertTrue(all('/converse/'in r['pointer']for r in rows))
 def test_generic_ape_is_not_invented_big_ape_identity(self):
  engine=Terminology(self.policy)
  for en in ['Were we once alike, Ape?','Have we met before, Ape?','My dreams are haunted by a giant ape. What does this mean?']:
   r=self.row(en);self.assertIn('maymun',r['tr']);self.assertNotIn('Big Ape',r['tr'])
   with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=r['tr'].replace('maymun','Big Ape')))
  for name in ['Greenfinger','Miniknog']:
   for r in self.manifest['translations']:
    if name in r['en']:
     self.assertIn(name,r['tr'])
     with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=r['tr'].replace(name,'Başkaİsim')))
 def test_nostalgia_keeps_past_longing_and_counts_one_changed_sentence(self):
  r=self.row('Seeing you makes me feel an alarming nostalgia. Why?');self.assertIn('geçmiş özlemi',r['tr']);self.assertTrue(r['tr'].endswith('Neden?'))
  engine=Terminology(self.policy)
  with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='Seni görünce içimde ürkütücü bir özlem uyanıyor. Neden?'))
  changes=self.review['corrections'];self.assertEqual(len(changes),1);self.assertEqual(changes[0]['changed_sentences'],1);self.assertEqual(changes[0]['en'],r['en']);self.assertEqual(self.review['changes']['total_corrected_sentences'],1);self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(15,1275))
 def test_memories_keep_uncertainty_without_experiment_or_family_identity(self):
  r=self.row('I feel like everything has changed overnight.');self.assertIn('gibi geliyor',r['tr']);engine=Terminology(self.policy)
  for en,bad in [('I had... a family, once. They were like you.','Sen ailemdensin.'),('What... have I become?','Miniknog beni dönüştürdü.'),('Outside I am colourful, inside I am grey.','Deney kürkümü renklendirdi.')]:
   with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(self.row(en),tr=bad))
 def test_names_do_not_allow_ordinary_english_preservation(self):
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='Miniknog changed my fur.',tr='Miniknog changed my fur.',occurrences=[dict(asset='neighbor',pointer='/scriptConfig/dialog/converse/apex/default/8')])));self.assertEqual(self.review['preserve_bindings'],[]);self.assertEqual(self.review['context_bindings'],[])
 def test_source_palette_ambiguity_and_missing_consumers_are_not_runtime_proof(self):
  import build_validate as build
  c=self.review['source_context'];self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertEqual(c['missing_vanilla_dependencies'],['npcs/villager.npctype','npcs/base.npctype','npcs/main.lua']);self.assertEqual(len(c['png_dungeons']),2)
  for d in c['png_dungeons']:
   self.assertEqual(len(d['shared_entries']),3);self.assertFalse(d['spawn_tested']);self.assertFalse(d['engine_brush_merge_order_tested'])
  self.assertEqual(sorted(x['shared_colour_pixels']for x in c['png_source_signals']if x['shared_colour_pixels']),[1,2,2]);self.assertEqual(self.review['scope']['excluded_review_fields'],15);self.assertFalse(self.review['scope']['confirmed_family_remainder']);self.assertEqual(self.review['scope']['deferred_unrelated_confirmed_fields'],2)
  self.assertEqual(len(build.V096_COLOURFUL_FIELDS),16)
  for p in ['/baseType','/scriptConfig/questGenerator/pools/0','/matchColorIndices','/items/override']:self.assertNotIn(('npcs/biome/colourfulvillager.npctype',p),build.V096_COLOURFUL_FIELDS)

if __name__=='__main__':unittest.main()
