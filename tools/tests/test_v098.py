"""Reject Letheia scope drift, access overstatement and invented runtime proof."""
import copy,sys,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v098 as gate

class V098Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v098_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/letheia-20261106.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_scope_neighbor_and_source_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for k,v in [('asset','npcs/hostile.npctype'),('pointer','/scriptConfig/behavior'),('en','The player is a confirmed spy.'),('tr','Oyuncu kesin casustur.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][k]=v
   with self.subTest(k=k),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_occurrence_rejects_unrelated_translation(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(asset=r['asset'],pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_complete_attack_scope_and_repeated_meanings(self):
  rows=self.manifest['translations'];self.assertEqual(len(rows),14);self.assertEqual(len({r['en']for r in rows}),10);self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[2,3,3,3,3]);self.assertTrue(all('/attack/'in r['pointer']for r in rows))
  for en,n in [('A corporate spy!',2),('This is a restricted zone!',3),("Where's your ID?",2)]:
   group=[r for r in rows if r['en']==en];self.assertEqual(len(group),n);self.assertEqual(len({r['tr']for r in group}),1)
  self.assertEqual([c['unit_index']for c in self.review['corrections']],[1,4,9,12]);self.assertEqual(self.review['changes']['total_corrected_fields'],4);self.assertEqual(self.review['changes']['total_corrected_sentences'],4);self.assertEqual(self.review['changes']['unique_source_strings_corrected'],2)
 def test_restricted_zone_keeps_authorized_entry_distinction(self):
  engine=Terminology(self.policy);group=[r for r in self.manifest['translations']if r['en']=='This is a restricted zone!'];self.assertEqual({r['tr']for r in group},{'Buraya izinsiz girilmez!'})
  for r in group:
   with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='Burası girilmesi yasak bir bölge!'))
  self.assertIn('çalışanları girebilir',self.row('Only employees of Letheia Corp allowed here!')['tr'])
 def test_more_guests_and_hylotl_speaker_are_not_repeated_visits_or_target_species(self):
  r=self.row('Oh my! More guests!');self.assertEqual(r['tr'],'Vay canına! Daha fazla misafir!');self.assertEqual(r['pointer'],'/scriptConfig/dialog/attack/hylotl/default/0')
  with self.assertRaisesRegex(ValueError,'LOCKED'):Terminology(self.policy).validate(dict(r,tr='Vay canına! Yine misafirler!'))
  boss=next(x for x in self.review['source_context']['maps'][1]['static_npcs']if x.get('typeName')=='letheiaboss');self.assertEqual(boss['npc'],'hylotl')
 def test_existing_company_name_and_attack_are_reused_without_global_corp_rule(self):
  r=self.row('Only employees of Letheia Corp allowed here!');self.assertIn('Letheia Corporation',r['tr']);self.assertEqual(self.row('Attack!')['tr'],'Saldır!');engine=Terminology(self.policy)
  with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=r['tr'].replace('Letheia Corporation','Başka Şirket')))
  legacy=next(r for r in self.catalog['translations']if r['asset']=='monsters/crawlers/fumechspider/fumechspiderletheiafacility.monstertype'and r['pointer']=='/shortdescription');self.assertEqual(legacy['tr'],'Letheia Şirketi Örümceği');engine.validate(legacy)
  self.assertEqual(self.review['reused_locked_names'],['Attack!']);self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(9,1304));self.assertFalse(self.review['source_context']['company_name_review']['global_corp_suffix_rule_added'])
 def test_proper_names_do_not_allow_ordinary_english_preservation(self):
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='Letheia Corporation hires visitors.',tr='Letheia Corporation hires visitors.',occurrences=[dict(asset='neighbor',pointer='/description')])));Terminology(self.policy).validate(dict(asset='ordinary',pointer='/description',en='Corporate policy excludes visitors.',tr='Şirket politikası ziyaretçilere izin vermez.'));self.assertEqual(self.review['context_bindings'],[]);self.assertEqual(self.review['preserve_bindings'],[])
 def test_static_maps_missing_parent_and_dependency_do_not_become_lqa(self):
  import build_validate as build
  c=self.review['source_context'];self.assertTrue(all(x['base_type']=='hostile'for x in c['npcs']));self.assertFalse(c['active_consumer_verified']);self.assertEqual(c['missing_vanilla_dependencies'],['npcs/hostile.npctype']);self.assertFalse(c['missing_direct_dependencies'][0]['exists_in_fu']);self.assertEqual([(m['static_total'],m['selected_static_total'],len(m['npc_parameter_spawners']))for m in c['maps']],[(31,31,6),(18,12,21)]);self.assertTrue(all(m['static_fu_spawner_chain_verified']and not m['live_spawn_tested']for m in c['maps']));self.assertEqual(len(c['radio_messages']),6);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertEqual(self.review['scope']['excluded_review_fields'],0)
  self.assertEqual(len(build.V098_LETHEIA_FIELDS),14)
  for a in self.review['scope']['assets']:
   for p in ['/baseType','/scriptConfig/behavior','/identity/gender','/items/override']:self.assertNotIn((a,p),build.V098_LETHEIA_FIELDS)

if __name__=='__main__':unittest.main()
