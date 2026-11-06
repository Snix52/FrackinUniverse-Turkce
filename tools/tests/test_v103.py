"""Verify Protectorate overlay provenance, placeholders, uncertainty and missing-parent limits."""
import copy,json,sys,tempfile,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v103 as gate

class V103Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v103_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/protectorate-20261107.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_scope_and_mandatory_overlay_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('asset','npcs/base.npctype'),('pointer','/baseType'),('en','The unknown enemy is named.'),('tr','Kaynak dışı bir metin.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  for qa in(None,{},dict(layered_source=False),dict(layered_source=True,source_patch='npcs/unrelated.npctype.patch')):
   bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']=qa
   with self.subTest(qa=qa),self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_overlay_occurrence_rejects_wrong_translation(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r);self.assertEqual(r['qa'],dict(layered_source=True,source_patch=r['asset']+'.patch'))
   with self.subTest(asset=r['asset'],pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_overlay_validator_uses_post_patch_value_without_inventing_parent(self):
  with tempfile.TemporaryDirectory()as tmp:
   source=Path(tmp)
   for item in self.review['source_context']['patches']:
    path=source/item['source_patch'];path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(item['operations']),encoding='utf-8');self.assertFalse((source/item['asset']).exists())
   gate.validate_source(self.manifest['translations'],source)
   first=self.manifest['translations'][0];path=source/first['qa']['source_patch'];ops=read(path);next(x for x in ops if x['path']==first['pointer'])['value']='Wrong source value';path.write_text(json.dumps(ops),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'Layered source mismatch'):gate.validate_source(self.manifest['translations'],source)
 def test_meeting_placeholder_and_dialogue_events(self):
  rows=self.manifest['translations'];self.assertEqual((len(rows),len({r['en']for r in rows})),(8,8));self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[1,2,2,3]);self.assertEqual(self.review['scope']['dialogue_events'],dict(converse=7,speak=1));r=next(r for r in rows if'<entityname>'in r['en']);self.assertEqual(r['tr'].count('<entityname>'),1);self.assertIn('başlamadan',r['tr']);self.assertNotIn('geç kaldın',r['tr'])
  with self.assertRaisesRegex(ValueError,'LOCKED'):Terminology(self.policy).validate(dict(r,tr=r['tr'].replace('<entityname>','<isim>')))
 def test_communications_loss_and_unknown_fates_are_not_rewritten(self):
  r=self.row('I hear that Huxven II and Omicron Theta III have both gone dark.');self.assertIn('Duyduğuma göre hem Huxven II hem de Omicron Theta III',r['tr']);self.assertIn('iletişim kesilmiş',r['tr']);self.assertNotIn('yok edildi',r['tr']);enemy=self.row('My homeworld was wiped out by the unknown enemy. I want vengeance.');self.assertIn('bilinmeyen düşman',enemy['tr']);self.assertIn('İntikam istiyorum.',enemy['tr']);self.assertNotIn('Ruin',enemy['tr']);friend=self.row('The beautiful morning is tainted by the recent troubles...I had friends on Omicron Theta III.');self.assertIn('arkadaşlarım vardı',friend['tr']);self.assertNotIn('öldü',friend['tr']);self.assertTrue(self.review['source_context']['unknown_enemy_identity_not_inferred'])
 def test_military_response_condition_and_appearance_remain_distinct(self):
  r=self.row('Without a military strike in response to the attacks, the Protectorate will look weak.');self.assertEqual(r['tr'],'Saldırılara askerî bir harekâtla karşılık verilmezse Protectorate zayıf görünecek.');self.assertEqual([x['unit_index']for x in self.review['corrections']],[4]);self.assertEqual([x['changed_sentences']for x in self.review['corrections']],[1]);self.assertEqual((self.review['changes']['total_corrected_fields'],self.review['changes']['total_corrected_sentences']),(1,1));conditional=self.row("If I get assigned to some distant world, I'll always have friends here on Earth!");self.assertIn('atanırsam',conditional['tr']);self.assertIn("Dünya'da",conditional['tr'])
 def test_locked_names_and_tools_do_not_allow_ordinary_english_preservation(self):
  r=self.row("Soon I'll be a real Protector, with my very own Matter Manipulator like you! It must be exciting!");self.assertIn('Madde Manipülatörü',r['tr']);self.assertIn('gerçek bir Protector',r['tr'])
  for row in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=row['en'],tr=row['en'],occurrences=[dict(asset=row['asset'],pointer=row['pointer'])])))
  engine=Terminology(self.policy)
  for en,tr in [('The earth is damp.','Toprak nemli.'),('Theta is a variable.','Teta bir değişkendir.')]:engine.validate(dict(asset='ordinary',pointer='/description',en=en,tr=tr))
  self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(10,1345));self.assertEqual(self.review['context_bindings'],[]);self.assertEqual(self.review['preserve_bindings'],[]);self.assertEqual(self.review['existing_terms_modified'],[])
 def test_map_refs_and_missing_parents_are_not_live_results(self):
  import build_validate as build
  c=self.review['source_context'];m=c['mission'];self.assertEqual((c['direct_fields'],c['layered_fields']),(0,8));self.assertTrue(c['complete_fu_patch_family']);self.assertFalse(c['complete_parent_npctypes_read']);self.assertEqual(len(m['parent_npctypes_missing']),4);self.assertEqual((len(m['static_npcs']),len(m['selected_static_npcs'])),(12,5));self.assertEqual(Counter(x['npc']for x in m['selected_static_npcs']),dict(apex=2,human=2,hylotl=1));self.assertEqual((len(m['tilesets']),sum(not x['available']for x in m['tilesets'])),(17,17));self.assertEqual(m['radio_stagehands'],[]);self.assertEqual((len(m['quest_script_radio_context']),len(m['quest_script_radio_missing_fu_writes'])),(1,15));self.assertEqual(m['referenced_quest_scripts_missing'],['quests/scripts/tutorial/protectoratefu.lua']);self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertEqual(len(build.V103_PROTECTORATE_FIELDS),8)
  for a in self.review['scope']['assets']:
   for ptr in('/baseType','/items/override','/scriptConfig/behavior'):self.assertNotIn((a,ptr),build.V103_PROTECTORATE_FIELDS)

if __name__=='__main__':unittest.main()
