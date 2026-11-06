"""Keep SMASH dialogue scope, uncertainty and static-consumer limits exact."""
import copy,sys,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v097 as gate

class V097Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v097_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/penguinhighway-20261106.json')
 def row(self,fragment):return next(r for r in self.manifest['translations']if fragment in r['en'])
 def test_exact_scope_neighbor_and_layered_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for k,v in [('asset','npcs/guard.npctype'),('pointer','/scriptConfig/dialogMode'),('en','Backup has arrived.'),('tr','Takviye kesin geldi.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][k]=v
   with self.subTest(k=k),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_occurrence_rejects_unrelated_translation(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(asset=r['asset'],pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_complete_sequence_scope_and_actual_speaker_identities(self):
  rows=self.manifest['translations'];self.assertEqual(dict(Counter(r['pointer'].split('/')[3]for r in rows)),dict(converse=15,speak=1));self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[5,5,6]);self.assertEqual(len({r['en']for r in rows}),16)
  npc={x['type']:x for x in self.review['source_context']['npcs']};self.assertTrue(all(x['dialog_mode']=='sequence'for x in npc.values()));self.assertEqual(npc['highwayzeldia']['identity']['race'],'avian');self.assertEqual(npc['highwayjinrei']['identity']['race'],'hylotl');self.assertEqual(npc['highwaygirulian']['identity']['race'],'human')
 def test_guardian_and_protector_titles_and_proper_names_stay_distinct(self):
  engine=Terminology(self.policy);r=self.row('A Protector, you say?');self.assertIn('Protector',r['tr']);self.assertIn('Koruyucu',r['tr'])
  with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=r['tr'].replace('Protector','Koruyucu')))
  for name in ['SMASH','Zeldia','Jinrei','Girulian','Techno City']:
   for r in self.manifest['translations']:
    if name in r['en']:
     self.assertIn(name,r['tr'])
     with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=r['tr'].replace(name,'Başkaİsim')))
 def test_inference_question_and_energy_meaning_are_not_flattened(self):
  r=self.row('intense and invigorating');self.assertIn('canlandıran',r['tr']);self.assertIn('olmalıyız',r['tr']);q=self.row('I take it');self.assertIn('sanırım?',q['tr']);self.assertIn('pek vaktimiz yok',q['tr']);engine=Terminology(self.policy)
  for x in [r,q]:
   c=next(c for c in self.review['corrections']if c['en']==x['en'])
   with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(x,tr=c['before']))
  self.assertEqual([c['changed_sentences']for c in self.review['corrections']],[2,2,1,2]);self.assertEqual(self.review['changes']['total_corrected_sentences'],7);self.assertEqual(self.review['changes']['total_corrected_fields'],4)
 def test_passive_threat_and_relative_odds_do_not_add_an_actor(self):
  r=self.row('threat must be eliminated');self.assertIn('ortadan kaldırılmalı',r['tr']);self.assertNotIn('kaldırmalıyız',r['tr']);odds=self.row('heavily outnumbered');self.assertIn('sayıca çok gerideyiz',odds['tr']);self.assertIn('şansın çok düşük',odds['tr']);engine=Terminology(self.policy)
  for x in [r,odds]:
   c=next(c for c in self.review['corrections']if c['en']==x['en'])
   with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(x,tr=c['before']))
 def test_new_names_do_not_preserve_ordinary_english(self):
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='SMASH will save you.',tr='SMASH will save you.',occurrences=[dict(asset='neighbor',pointer='/scriptConfig/dialog/converse/default/default/5')])));self.assertEqual(self.review['context_bindings'],[]);self.assertEqual(self.review['preserve_bindings'],[]);self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(20,1295))
  self.assertFalse(any(t['source']=='SMASH'for t in self.policy['terms']));term=next(t for t in self.policy['terms']if t['source']=='SMASH unit / with SMASH');self.assertEqual({f['en']for f in term['forms']},{'SMASH unit','with SMASH'});self.assertNotEqual(term.get('mode'),'preserve')
  engine=Terminology(self.policy);engine.validate(dict(asset='ordinary-fixture',pointer='/description',en='Smash the rocks.',tr='Kayaları parçala.'))
  ordinary=next(r for r in self.catalog['translations']if r['asset']=='items/active/weapons/melee/mace/cutemace.activeitem'and r['pointer']=='/description');engine.validate(ordinary)
  self.assertFalse(preserved_name(dict(en='SMASH unit',tr='SMASH unit',occurrences=[dict(asset='ordinary-fixture',pointer='/description')])));
  with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(asset='fixture',pointer='/description',en='with SMASH',tr='başka bir birlikle'))
 def test_real_fu_spawner_chain_is_distinct_from_live_behavior_approval(self):
  import build_validate as build
  c=self.review['source_context'];m=c['mission'];self.assertEqual(len(m['static_npcs']),1);self.assertEqual(len(m['npc_parameter_spawners']),6);self.assertTrue(m['static_spawner_chain_verified']);self.assertEqual(m['spawner_gid'],3991);self.assertEqual(m['spawner_local_tileid'],34);self.assertEqual(m['spawner_object'],'extrainvisiblenpcspawner');self.assertIn('npcParameter or {}',m['npc_params_forwarding']);self.assertFalse(m['live_spawn_tested']);self.assertFalse(c['active_consumer_verified']);self.assertEqual((len(m['tilesets']),sum(not x['available']for x in m['tilesets'])),(23,22));self.assertEqual(m['radio_stagehands'],[]);self.assertEqual(self.review['scope']['excluded_review_fields'],4);self.assertEqual(self.review['lqa_status'],'NOT TESTED')
  self.assertEqual(len(build.V097_PENGUINHIGHWAY_FIELDS),16)
  for a in self.review['scope']['assets']:
   for p in ['/baseType','/scriptConfig/dialogMode','/scriptConfig/behavior','/identity/name']:self.assertNotIn((a,p),build.V097_PENGUINHIGHWAY_FIELDS)

if __name__=='__main__':unittest.main()
