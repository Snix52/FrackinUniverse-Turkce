"""Protect merchant UI labels, source wordplay and unverified consumer limits."""
import copy,json,sys,tempfile,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v105 as gate

class V105Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v105_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/cultistmerchants-20261107.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en'].strip()==en)
 def test_exact_scope_neighbor_and_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for k,v in [('asset','npcs/merchant.npctype'),('pointer','/scriptConfig/merchant/numItems'),('en','  New construction quest'),('tr','  Yeni bir inşaat görevi')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][k]=v
   with self.subTest(key=k),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_ui_text_rejects_wrong_translation_and_whole_english(self):
  e=Terminology(self.policy)
  for r in self.manifest['translations']:
   e.validate(r);self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
   with self.subTest(asset=r['asset'],pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(r,tr='  İlgisiz bir başlık'))
 def test_leading_spaces_and_ui_roles_are_exact(self):
  rows=self.manifest['translations'];self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[2,2]);self.assertEqual(Counter(r['pointer'].rsplit('/',1)[1]for r in rows),{'title':2,'subtitle':2});self.assertEqual((self.review['scope']['dialogue_fields'],self.review['scope']['title_fields']),(0,4));self.assertEqual(self.review['scope']['dialogue_events'],{});self.assertEqual(self.review['scope']['excluded_review_fields'],54)
  for r in rows:
   for k in('en','tr'):self.assertEqual(len(r[k])-len(r[k].lstrip(' ')),2)
 def test_artist_role_and_nightmare_inspiration_do_not_force_ordinary_prose(self):
  self.assertEqual(self.row('Artist')['tr'],'  Sanatçı');self.assertEqual(self.row('Inspired by nightmares')['tr'],'  Kâbuslardan ilham alan');t=next(t for t in self.policy['terms']if t['source']=='Artist');self.assertFalse(t.get('enforce_in_text',False));self.assertNotIn('tr_stem',t)
  e=Terminology(self.policy)
  for en,tr in [('An artist draws.','Bir ressam çiziyor.'),('The nightmare ended.','Kâbus sona erdi.'),('A temple bell rings.','Bir tapınak çanı çalıyor.')]:e.validate(dict(asset='ordinary',pointer='/description',en=en,tr=tr))
 def test_building_blocks_wordplay_is_bound_to_actual_construction_pool(self):
  self.assertEqual(self.row('The Building Blocks of Madness')['tr'],'  Deliliğin Yapı Taşları');c=self.review['source_context'];writes=c['source_context']['selected_pool_writes'];self.assertEqual({(w['operation_index'],w['op'],w['path'])for w in writes},{(45,'add','/futemplemerchant'),(54,'add','/fucultistart')});self.assertTrue(c['pool_entries_not_observed_inventory']);self.assertFalse(c['extra_goods_translated'])
 def test_existing_eldritch_madness_and_proper_identity_remain_distinct(self):
  self.assertEqual(self.row('Eldritch Temple Construction')['tr'],'  Tekinsiz Tapınak İnşaatı');self.assertEqual(next(t for t in self.policy['terms']if t['source']=='Eldritch')['tr'],'tekinsiz');self.assertEqual(next(t for t in self.policy['terms']if t['source']=='Madness')['tr'],'Delilik');self.assertEqual(set(self.review['reused_locked_names']),{'Eldritch','Madness'});self.assertEqual(self.review['existing_terms_modified'],[])
  e=Terminology(self.policy);e.validate(dict(asset='ordinary',pointer='/description',en='Cthulhu',tr='Cthulhu'))
  with self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(asset='ordinary',pointer='/description',en='Cthulhu',tr='Tekinsiz'))
 def test_tenant_and_missing_ui_sources_do_not_become_live_proof(self):
  import build_validate as build
  c=self.review['source_context'];self.assertEqual({n['base_type']for n in c['npcs']},{'merchant'});self.assertFalse(c['active_consumer_verified']);self.assertTrue(c['tenant_definitions_not_live_spawns']);self.assertEqual(len(c['source_context']['missing_vanilla']),4);self.assertEqual(len(c['source_context']['tenant_definitions']),2);self.assertEqual({x['species']for x in c['source_context']['tenant_definitions']},{'fudarkizku'});self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertFalse(self.review['scope']['live_runtime_visibility_verified']);self.assertEqual(self.review['corrections'],[]);self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(4,1353));self.assertEqual(self.review['preserve_bindings'],[]);self.assertEqual(self.review['context_bindings'],[]);self.assertEqual(len(build.V105_CULTISTMERCHANTS_FIELDS),4)
  for a,p in build.V105_CULTISTMERCHANTS_FIELDS:self.assertTrue(a.startswith('npcs/tenants/'));self.assertIn(p.rsplit('/',1)[1],('title','subtitle'))
  for a in self.review['scope']['assets']:
   for p in('/baseType','/scriptConfig/merchant/categories','/scriptConfig/merchant/buyFactorRange','/items/override'):self.assertNotIn((a,p),build.V105_CULTISTMERCHANTS_FIELDS)
 def test_direct_sources_and_later_overlay_changes_are_rejected(self):
  rows=self.manifest['translations'];docs={}
  for r in rows:docs.setdefault(r['asset'],{'scriptConfig':{'merchant':{'paneLayoutOverride':{'windowtitle':{}}}}})['scriptConfig']['merchant']['paneLayoutOverride']['windowtitle'][r['pointer'].rsplit('/',1)[1]]=r['en']
  with tempfile.TemporaryDirectory()as d:
   root=Path(d)
   for a,doc in docs.items():f=root/a;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(doc),encoding='utf-8')
   gate.validate_source(rows,root);r=rows[0];f=root/r['asset'];bad=copy.deepcopy(docs[r['asset']]);bad['scriptConfig']['merchant']['paneLayoutOverride']['windowtitle'][r['pointer'].rsplit('/',1)[1]]='  Different source';f.write_text(json.dumps(bad),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'pinned source'):gate.validate_source(rows,root)
   f.write_text(json.dumps(docs[r['asset']]),encoding='utf-8');Path(str(f)+'.patch').write_text(json.dumps([{'op':'replace','path':r['pointer'],'value':'  Changed by overlay'}]),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'unreviewed FU overlay'):gate.validate_source(rows,root)

if __name__=='__main__':unittest.main()
