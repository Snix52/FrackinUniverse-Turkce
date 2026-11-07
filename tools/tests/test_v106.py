"""Keep authored faces exact without permitting untranslated English dialogue."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology,validate_format
import generate_v106 as gate

class V106Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v106_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/frogg-20261107.json')
 def unit(self,row,**changes):return dict(en=row['en'],tr=row['tr'],occurrences=[dict(asset=row['asset'],pointer=row['pointer'])],**changes)
 def test_exact_three_source_fields_and_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review);rows=self.manifest['translations'];self.assertEqual((len(rows),len({r['asset']for r in rows}),len({r['en']for r in rows})),(3,3,1))
  for k,v in [('asset','npcs/evernight/unselected.npctype'),('pointer','/scriptConfig/dialog/attack/default/default/2'),('en','O_o'),('tr','Şaşırdım!')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][k]=v
   with self.subTest(key=k),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_authored_face_has_its_own_exact_preservation_binding(self):
  e=Terminology(self.policy)
  for r in self.manifest['translations']:
   self.assertEqual((r['en'],r['tr']),('0_o','0_o'));self.assertTrue(preserved_name(self.unit(r)));e.validate(r)
   self.assertTrue(any(all(x.get(k)==r[k]for k in('asset','pointer','en','tr'))and x.get('preserve_utterance')is True and x.get('term_source')=='0_o'for x in self.policy['context_exceptions']))
   for tr in('O_o','Şaşırdım!'):
    with self.subTest(asset=r['asset'],tr=tr),self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(r,tr=tr))
 def test_adjacent_variants_and_other_npc_dialogue_do_not_inherit_permission(self):
  for r in self.manifest['translations']:
   for i in(0,1,2,4):
    u=self.unit(r);u['occurrences'][0]['pointer']=f'/scriptConfig/dialog/attack/default/default/{i}';self.assertFalse(preserved_name(u))
   u=self.unit(r);u['occurrences'][0]['asset']='npcs/evernight/unselected.npctype';self.assertFalse(preserved_name(u))
 def test_ordinary_english_and_proper_entities_are_not_face_preservations(self):
  row=self.manifest['translations'][0]
  for en in('Hello, friend.','He wrote 0_o.','Meet Frogg, the hero.'):
   u=self.unit(row);u['en']=u['tr']=en;self.assertFalse(preserved_name(u))
  e=Terminology(self.policy);e.validate(dict(asset='ordinary',pointer='/description',en='Frogs carry rockets.',tr='Kurbağalar roket taşır.'));e.validate(dict(asset='ordinary',pointer='/description',en='Cthulhu',tr='Cthulhu'))
  with self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(asset='ordinary',pointer='/description',en='Cthulhu',tr='0_o'))
 def test_initial_block_remains_honest_and_final_preflight_is_separate(self):
  r=self.review;self.assertEqual(r['initial_preflight']['status'],'BLOCKED_UNCHANGED_TRANSLATION_REQUIRES_NARROW_APPROVAL');self.assertFalse(r['initial_preflight']['technical_preflight_passed']);self.assertIn('Missing or unchanged translation',r['initial_preflight']['error']);self.assertFalse(r['independent_frozen_preflight']['technical_preflight_passed']);self.assertFalse(r['independent_frozen_preflight']['preservation_approved']);self.assertEqual(r['preflight']['status'],'TECHNICAL_PREFLIGHT_PASS_LANGUAGE_REVIEW_REQUIRED')
  d=r['source_context']['source_preservation_review'];self.assertEqual(d['packet_sha256'],r['luna_original_packet_sha256']);self.assertEqual(d['status'],'SOURCE_REVIEW_RESOLVED');self.assertTrue(d['preservation_bindings_approved']);self.assertEqual(d['approved_bindings'],r['preserve_bindings']);self.assertEqual(len(d['requests']),3);self.assertFalse(d['new_global_qa_engine_rule']);self.assertFalse(d['runtime_visibility_verified']);self.assertFalse(d['pool_promotion'])
 def test_game_context_and_counts_do_not_become_newly_translated_sentences(self):
  import build_validate as build
  r=self.review;c=r['source_context'];m=c['source_context'];self.assertEqual((r['scope']['authored_emote_occurrences_preserved'],r['scope']['translated_english_sentences']),(3,0));self.assertEqual(r['corrections'],[]);self.assertEqual((r['new_locked_terms'],r['locked_total']),(1,1354));self.assertEqual(len(r['preserve_bindings']),3);self.assertEqual(r['existing_terms_modified'],[]);self.assertFalse(c['active_consumer_verified']);self.assertEqual(m['total_static_references'],41);self.assertEqual([len(x['selected_static_npcs'])for x in m['maps']],[40,1]);self.assertEqual(m['maps'][0]['type_counts'],{'frogsniper':14,'froggunner':26});self.assertFalse(m['frogrocketeer_runtime_placement_verified']);self.assertEqual(len(m['radio_messages']),12);self.assertEqual([(len(x['tilesets']),sum(not t['available']for t in x['tilesets']))for x in m['maps']],[(20,19),(35,34)]);self.assertEqual(r['lqa_status'],'NOT TESTED')
  self.assertEqual(len(build.V106_FROGG_FIELDS),3)
  for a,p in build.V106_FROGG_FIELDS:self.assertEqual(p,'/scriptConfig/dialog/attack/default/default/3');self.assertNotIn((a,'/items/override'),build.V106_FROGG_FIELDS)
 def test_digit_zero_underscore_and_lowercase_o_are_not_normalized(self):
  e=Terminology(self.policy);format_policy=read(TOOLS/'rules/text_integrity.json');term=next(t for t in self.policy['terms']if t['source']=='0_o');self.assertEqual(term['mode'],'preserve');self.assertEqual(term['forms'],[{'en':'0_o','tr':'0_o'}])
  for row in self.manifest['translations']:
   self.assertEqual(row['en'].encode('ascii'),bytes([48,95,111]));self.assertEqual(row['tr'].encode('ascii'),bytes([48,95,111]));validate_format(row,format_policy)
   for tr in('O_o','0_O','o_o'):
    with self.subTest(tr=tr),self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(row,tr=tr))
 def test_direct_sources_and_later_overlay_changes_are_rejected(self):
  rows=self.manifest['translations'];docs={r['asset']:{'scriptConfig':{'dialog':{'attack':{'default':{'default':['!!!','>=(','-_-','0_o',':3']}}}}}for r in rows}
  with tempfile.TemporaryDirectory()as d:
   root=Path(d)
   for a,doc in docs.items():f=root/a;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(doc),encoding='utf-8')
   gate.validate_source(rows,root);r=rows[0];f=root/r['asset'];bad=copy.deepcopy(docs[r['asset']]);bad['scriptConfig']['dialog']['attack']['default']['default'][3]='O_o';f.write_text(json.dumps(bad),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'pinned source'):gate.validate_source(rows,root)
   f.write_text(json.dumps(docs[r['asset']]),encoding='utf-8');Path(str(f)+'.patch').write_text(json.dumps([{'op':'replace','path':r['pointer'],'value':'A different utterance.'}]),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'unreviewed FU overlay'):gate.validate_source(rows,root)

if __name__=='__main__':unittest.main()
