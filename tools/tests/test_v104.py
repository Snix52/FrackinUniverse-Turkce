"""Protect feline dialogue meanings, exact source writes and missing-parent limits."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v104 as gate

class V104Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v104_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/catvisitor-20261107.json')
 def test_exact_scope_neighbor_and_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for k,v in [('asset','npcs/outpostcivilian.npctype'),('pointer','/scriptConfig/dialog/converse/default/default/4'),('en','The cats sell armor.'),('tr','Kediler zırh satar.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][k]=v
   with self.subTest(key=k),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_reply_rejects_wrong_translation(self):
  e=Terminology(self.policy)
  for r in self.manifest['translations']:
   e.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(r,tr='Kaynakla ilgisiz bir cümle.'))
 def test_full_english_is_not_preserved_and_ordinary_words_are_free(self):
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  e=Terminology(self.policy)
  for en,tr in [('The cat sleeps.','Kedi uyuyor.'),('The shop is closed.','Dükkân kapalı.'),('The paw is muddy.','Pati çamurlu.'),('A crowd gathered.','Bir kalabalık toplandı.')]:e.validate(dict(asset='ordinary',pointer='/description',en=en,tr=tr))
 def test_source_paw_joke_cat_sound_and_question(self):
  r=self.manifest['translations'][0];self.assertEqual(r['tr'],'Miyav! Karakol patişahane dükkânlarla dolu, ha?');self.assertIn('pawesome',r['en']);self.assertEqual(self.review['corrections'],[]);self.assertEqual((self.review['changes']['total_corrected_fields'],self.review['changes']['total_corrected_sentences']),(0,0));self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(4,1349));self.assertEqual(self.review['preserve_bindings'],[]);self.assertEqual(self.review['context_bindings'],[])
 def test_normal_cat_tag_question_does_not_invent_identity(self):
  r=self.manifest['translations'][1];self.assertEqual(r['tr'],'Miyav. ...Seni sıradan bir kedi olduğuma inandırdım, değil mi?');self.assertTrue(r['tr'].endswith('değil mi?'));self.assertFalse(self.review['source_context']['appearance_verified']);self.assertTrue(self.review['source_context']['speaker_target_fallback_not_species'])
 def test_mild_cold_and_crowded_telepathy_remain_dialogue(self):
  a,b=self.manifest['translations'][2:];self.assertIn('biraz serin',a['tr']);self.assertIn('tercih eder',a['tr']);self.assertTrue(a['tr'].endswith('orası kesin!'));self.assertEqual(b['tr'],'Miyav? Ne dedin? Kusura bakma, bu yoğun kalabalık telepatimi bozuyor.');self.assertFalse(self.review['source_context']['telepathy_mechanic_verified'])
 def test_missing_parent_and_context_gear_are_not_live_proof_or_scope(self):
  import build_validate as build
  c=self.review['source_context'];self.assertEqual(c['npcs'][0]['base_type'],'outpostvisitor');self.assertFalse(c['active_consumer_verified']);self.assertFalse(c['source_context']['vanilla_base_available']);self.assertEqual(c['equipment_scope'],'context only;not translated');self.assertEqual(len(c['files']),7);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertFalse(self.review['scope']['live_runtime_visibility_verified']);self.assertEqual(self.review['scope']['excluded_review_fields'],0)
  self.assertEqual(len(build.V104_CATVISITOR_FIELDS),4)
  for a,p in build.V104_CATVISITOR_FIELDS:self.assertEqual(a,'npcs/outpost/visitors/catvisitor.npctype');self.assertTrue(p.startswith('/scriptConfig/dialog/converse/default/default/'))
  for p in('/baseType','/type','/items/override','/statusControllerSettings/statusProperties/effectDirectives'):self.assertNotIn(('npcs/outpost/visitors/catvisitor.npctype',p),build.V104_CATVISITOR_FIELDS)
 def test_direct_source_and_later_overlay_changes_are_rejected(self):
  rows=self.manifest['translations'];asset=rows[0]['asset'];doc={'scriptConfig':{'dialog':{'converse':{'default':{'default':[r['en']for r in rows]}}}}}
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);f=root/asset;f.parent.mkdir(parents=True);f.write_text(json.dumps(doc),encoding='utf-8');gate.validate_source(rows,root)
   bad=copy.deepcopy(doc);bad['scriptConfig']['dialog']['converse']['default']['default'][0]='Different source.';f.write_text(json.dumps(bad),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'pinned source'):gate.validate_source(rows,root)
   f.write_text(json.dumps(doc),encoding='utf-8');Path(str(f)+'.patch').write_text(json.dumps([{'op':'replace','path':rows[1]['pointer'],'value':'Changed by overlay.'}]),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'unreviewed FU overlay'):gate.validate_source(rows,root)

if __name__=='__main__':unittest.main()
