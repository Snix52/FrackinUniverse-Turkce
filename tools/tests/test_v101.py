"""Guard complete Alien Jungle dialogue scope, temporal meaning and source/runtime limits."""
import copy,sys,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v101 as gate

class V101Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v101_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/alienjungle-20261107.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_scope_neighbor_and_source_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('asset','npcs/hostile.npctype'),('pointer','/baseType'),('en','The tribe gains a new ability.'),('tr','Kaynakta olmayan bir oyun etkisi.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_wrong_translation_rejected_for_every_occurrence(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(asset=r['asset'],pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_complete_family_and_speaker_fallback_are_preserved(self):
  rows=self.manifest['translations'];self.assertEqual((len(rows),len({r['en']for r in rows})),(10,10));self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[5,5]);self.assertTrue(all('/attack/'in r['pointer']for r in rows));self.assertEqual(sum('/attack/floran/default/'in r['pointer']for r in rows),4);self.assertTrue(self.review['source_context']['floran_speaker_not_target']);self.assertEqual(self.review['scope']['excluded_review_fields'],0)
 def test_existing_attack_translation_and_bare_commands_are_retained(self):
  self.assertEqual(self.row('Attack!')['tr'],'Saldır!');self.assertEqual(self.row('Sstab it! Sstab it!')['tr'],'Sssapla! Sssapla!');self.assertEqual(self.row('Sstab! Sstab! And then sstab again!')['tr'],'Sssapla! Sssapla! Sonra bir daha sssapla!');self.assertEqual(self.review['reused_locked_names'],['Attack!'])
  with self.assertRaisesRegex(ValueError,'LOCKED'):Terminology(self.policy).validate(dict(self.row('Attack!'),tr='Dur!'))
 def test_aeons_does_not_become_a_specific_number_or_eternal_claim(self):
  r=self.row('Tribe hass lived here for aeonss!');self.assertEqual(r['tr'],'Kabile burada çağlardır yaşamını sssürdürüyor!');self.assertNotIn('asır',r['tr']);self.assertNotIn('ezel',r['tr']);self.assertFalse(any(c.isdigit()for c in r['tr']));self.assertEqual([c['unit_index']for c in self.review['corrections']],[8]);self.assertEqual([c['changed_sentences']for c in self.review['corrections']],[1])
  with self.assertRaisesRegex(ValueError,'LOCKED'):Terminology(self.policy).validate(dict(r,tr='Kabile burada asssırlardır yaşıyor!'))
 def test_tribal_ownership_and_devour_rhetoric_do_not_create_items(self):
  self.assertEqual(self.row('Sshiny thingss belongss to tribe! Not you!')['tr'],'Parlak şeyler kabileye ait! Sssana değil!');r=self.row('Devour meatss! Devour sshiniess! Floran becomess powerful!');self.assertEqual(r['tr'],'Etleri yut! Parlak nesssneleri yut! Floran güçlenir!');self.assertNotIn('piksel',r['tr'].lower());self.assertNotIn('%',r['tr']);self.assertEqual((self.review['changes']['total_corrected_fields'],self.review['changes']['total_corrected_sentences']),(1,1));self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(9,1329))
 def test_full_replies_do_not_preserve_english_or_lock_ordinary_words(self):
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  engine=Terminology(self.policy)
  for en,tr in [('The tribe waits.','Kabile bekliyor.'),('The shiny cup is empty.','Parlak fincan boş.'),('The power is low.','Güç düşük.')]:engine.validate(dict(asset='ordinary',pointer='/description',en=en,tr=tr))
  self.assertEqual(self.review['context_bindings'],[]);self.assertEqual(self.review['preserve_bindings'],[]);self.assertEqual(self.review['existing_terms_modified'],[])
 def test_source_map_configuration_is_not_live_lqa(self):
  import build_validate as build
  m=self.review['source_context']['mission'];self.assertEqual([x['static_npc_total']for x in m['maps']],[21,3]);self.assertEqual([len(x['selected_static_npcs'])for x in m['maps']],[20,3]);self.assertTrue(all(x['npc']=='floran'for a in m['maps']for x in a['selected_static_npcs']));self.assertEqual([(len(x['tilesets']),sum(not t['available']for t in x['tilesets']))for x in m['maps']],[(29,25),(23,15)]);self.assertEqual(len(m['radio_messages']),16);self.assertEqual(list(m['radio_stagehand_counts'].values()),[7]);self.assertEqual(len(m['selected_dynamic_parameters']),2);self.assertEqual(m['fu_spawner_chain']['configured_stock'],4);self.assertFalse(m['fu_spawner_chain']['npcParams_forwarding_verified']);self.assertFalse(m['fu_spawner_chain']['live_spawn_verified']);self.assertEqual(m['fu_turnin_chain']['local_id'],39);self.assertFalse(self.review['source_context']['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertEqual(len(build.V101_ALIENJUNGLE_FIELDS),10)
  for asset in self.review['scope']['assets']:
   for pointer in('/baseType','/items/override','/statusControllerSettings'):self.assertNotIn((asset,pointer),build.V101_ALIENJUNGLE_FIELDS)

if __name__=='__main__':unittest.main()
