"""Reject Grand Arena scope drift, distorted warnings and fabricated live proof."""
import copy,sys,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v100 as gate

class V100Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v100_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/grandarena-20261106.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_scope_neighbor_and_source_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('asset','npcs/base.npctype'),('pointer','/scriptConfig/behavior'),('en','Only a knife can win the arena.'),('tr','Kaynakta olmayan bir oyun şartı.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_occurrence_rejects_unrelated_translation(self):
  engine=Terminology(self.policy)
  for row in self.manifest['translations']:
   engine.validate(row)
   with self.subTest(asset=row['asset'],pointer=row['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(row,tr='İlgisiz bir cümle.'))
 def test_complete_family_and_speaker_branch_are_retained(self):
  rows=self.manifest['translations'];self.assertEqual((len(rows),len({r['en']for r in rows})),(12,11));self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[2,10]);self.assertTrue(all('/converse/'in r['pointer']for r in rows));self.assertEqual(sum('/converse/floran/default/'in r['pointer']for r in rows),10);self.assertTrue(self.review['source_context']['floran_speaker_not_target']);self.assertEqual(self.review['scope']['excluded_review_fields'],2)
  group=[r for r in rows if r['en']=='I have nothing to sssay to you'];self.assertEqual(len(group),2);self.assertEqual({r['tr']for r in group},{'Sana sssöyleyecek bir şeyim yok.'})
 def test_grand_arena_name_and_source_third_person_are_not_replaced(self):
  en='Floran welcomesss you to grand arena! Sssurvive all wavesss of monstersss to gain victory, but if you die during challenge then you mussst ssstart all over again!';r=self.row(en);self.assertIn('Floran',r['tr']);self.assertIn('Büyük Arena',r['tr']);self.assertNotIn('15',r['tr'])
  with self.assertRaisesRegex(ValueError,'LOCKED'):Terminology(self.policy).validate(dict(r,tr=r['tr'].replace('Büyük Arena','Küçük Arena')))
 def test_surviving_last_wave_does_not_remove_all_enemy_condition(self):
  r=self.row('Even if you sssurvive the lassst wave, you mussst ssstab all enemiesss to win.');self.assertIn('Ssson dalgadan sssağ çıksan bile',r['tr']);self.assertIn('bütün düşmanları bıçaklamalısssın',r['tr'])
  with self.assertRaisesRegex(ValueError,'LOCKED'):Terminology(self.policy).validate(dict(r,tr='Ssson dalgadan sssağ çıkman yeterli.'))
  torch=self.row('The number of torchesss tellsss you how many wavesss remain.');self.assertIn('kaldığını',torch['tr']);self.assertIn('düşman dalgası',torch['tr'])
 def test_swamped_is_not_invented_encirclement_or_death(self):
  r=self.row('Floran wasss ssslow in ssstabbing monstersss lassst time. Got ssswamped.');self.assertEqual(r['tr'],'Floran geçen sssefer canavarları bıçaklamakta yavaştı. Onlarla baş edemedi.');self.assertNotIn('sardılar',r['tr']);self.assertNotIn('öldü',r['tr']);self.assertEqual([c['unit_index']for c in self.review['corrections']],[6,8]);self.assertEqual([c['changed_sentences']for c in self.review['corrections']],[1,2]);self.assertEqual((self.review['changes']['total_corrected_fields'],self.review['changes']['total_corrected_sentences']),(2,3));self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(10,1320))
 def test_names_and_hiss_do_not_allow_english_preservation_or_global_arena_rule(self):
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  Terminology(self.policy).validate(dict(asset='ordinary',pointer='/description',en='The arena is quiet.',tr='Arena sessiz.'));self.assertEqual(self.review['context_bindings'],[]);self.assertEqual(self.review['preserve_bindings'],[]);self.assertEqual(self.review['reused_locked_names'],['I have nothing to sssay to you']);self.assertEqual(self.review['existing_terms_modified'],[])
 def test_static_counts_and_missing_consumers_are_not_live_lqa(self):
  import build_validate as build
  m=self.review['source_context']['mission'];self.assertEqual((m['static_npc_total'],m['selected_static_total']),(5,4));self.assertEqual(m['selected_type_counts'],dict(grandarenausher=1,grandarenacompetitor=3));self.assertTrue(all(x['npc']=='floran'for x in m['static_npcs']));self.assertEqual(len(m['monster_spawner_parameters']),21);self.assertEqual(m['configured_monster_stock'],46);self.assertFalse(m['actual_spawn_count_verified']);self.assertEqual(len(m['radio_messages']),2);self.assertEqual((len(m['tilesets']),m['missing_tilesets']),(21,20));self.assertTrue(all(not x['available']for x in m['parameter_gid_resolutions']));self.assertEqual(m['fu_turnin_chain']['local_id'],6);self.assertFalse(m['fu_turnin_chain']['live_quest_completion_verified']);self.assertFalse(self.review['source_context']['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertEqual(len(build.V100_GRANDARENA_FIELDS),12)
  for asset in self.review['scope']['assets']:
   for pointer in ('/baseType','/scriptConfig/behavior','/items/override'):self.assertNotIn((asset,pointer),build.V100_GRANDARENA_FIELDS)

if __name__=='__main__':unittest.main()
