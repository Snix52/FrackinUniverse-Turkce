"""Protect Mount Gigant rumours, fragmented speech and exact ruin disambiguation."""
import copy,sys,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology,bound_exception
import generate_v094 as gate

class V094Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v094_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/japaneseruins-20261105.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_membership_neighbor_scope_and_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('asset','npcs/hostilefu.npctype'),('pointer','/scriptConfig/behavior'),('en','A fabricated puzzle solution.'),('tr','Bulmacanın çözümü budur.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_corrected_expressions_reject_luna_originals(self):
  self.assertEqual(len(self.review['corrections']),2);engine=Terminology(self.policy)
  for c in self.review['corrections']:
   r=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(r)
   with self.subTest(en=r['en']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr=c['before']))
 def test_every_occurrence_rejects_unrelated_translation(self):
  engine=Terminology(self.policy)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_repeated_attack_fragments_keep_speaker_branches_and_ellipsis(self):
  rows=self.manifest['translations'];self.assertEqual(dict(Counter(r['pointer'].split('/')[3]for r in rows)),dict(attack=10,converse=10));self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[5,5,10])
  for en,tr in [('Attack!','Saldır!'),('Cursed...','Lanetli...'),('No...','Hayır...'),('You should not...be here...','Burada...olmamalısın...'),('This place...will be your death...','Burası...senin sonun olacak...')]:
   repeated=[r for r in rows if r['en']==en];self.assertEqual(len(repeated),2);self.assertEqual({r['tr']for r in repeated},{tr});self.assertEqual(en.count('...'),tr.count('...'))
 def test_rumour_markers_five_gems_and_no_invented_puzzle_solution(self):
  rows=self.manifest['translations'];rumours=[r for r in rows if 'said'in r['en']or'Rumour'in r['en']or'supposed'in r['en']];self.assertEqual(len(rumours),6)
  for r in rumours:self.assertTrue('söyleniyor'in r['tr']or'Söylentiye göre'in r['tr'])
  gems=self.row("Five gems of power are said to lead the way to the ruins' treasure.")['tr'];self.assertTrue(gems.startswith('Beş güç mücevherinin'));self.assertIn('söyleniyor',gems)
  tale=self.row("Vicious oni are said to live in the ruins, men warped by power...but that's just a tale.")['tr'];self.assertIn('gücün bozduğu',tale);self.assertIn('sadece bir hikâye',tale)
  self.assertFalse(self.review['source_context']['mission']['spawn_or_live_path_tested'])
 def test_generic_ruin_binding_is_closed_to_wrong_translation_and_neighbors(self):
  binding=self.review['context_bindings'][0];engine=Terminology(self.policy);row={k:binding[k]for k in ('asset','pointer','en','tr')};engine.validate(row);self.assertIn('Harabe duvarlarında',row['tr']);self.assertIn('Madde Manipülatörü',row['tr'])
  baseline=copy.deepcopy(self.policy);baseline['context_exceptions']=[x for x in baseline['context_exceptions']if x!=binding]
  with self.assertRaisesRegex(ValueError,"missing stem 'ruin'"):Terminology(baseline).validate(row)
  for k,v in [('asset','neighbor.npctype'),('pointer','/scriptConfig/dialog/converse/hylotl/default/6'),('en',row['en']+' Extra.'),('tr',row['tr']+' Ek.')]:
   bad=dict(row,**{k:v});self.assertFalse(bound_exception(bad,binding))
   with self.subTest(k=k),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(bad)
  for x in [dict(asset='fixture',pointer='/text',en='The Ruin, stronger.',tr='Yıkım, daha güçlü.'),dict(row,tr=row['tr'].replace('Madde Manipülatörü','Matter Manipulator'))]:
   with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(x)
  engine.validate(dict(asset='fixture',pointer='/text',en='The Ruin, stronger.',tr='Ruin, daha güçlü.'))
 def test_name_lock_does_not_preserve_ordinary_english(self):
  Terminology(self.policy).validate(dict(asset='fixture',pointer='/shortdescription',en='Oni',tr='Oni'))
  for r in self.manifest['translations']:self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  b=self.review['context_bindings'][0];self.assertFalse(b.get('preserve_utterance',False))
  with self.assertRaisesRegex(ValueError,'LOCKED'):Terminology(self.policy).validate({k:(b['en']if k=='tr'else b[k])for k in ('asset','pointer','en','tr')})
 def test_actual_map_inventory_missing_consumers_and_technical_exclusions(self):
  import build_validate as build
  c=self.review['source_context'];m=c['mission'];self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertEqual((m['static_villagers'],m['other_static_npcs']),(6,1));self.assertEqual(m['static_species'],dict(hylotl=6,avian=1));self.assertEqual(m['dynamic_spawner_counts'],dict(oni=12,archer=6));self.assertEqual(m['dynamic_spawner_species'],'hylotl');self.assertEqual(m['villager_damage_team'],'friendly')
  self.assertEqual((len(m['tileset_references']),m['missing_tilesets'],m['available_fu_tilesets']),(24,23,1));self.assertEqual(len(m['radio_stagehands']),1);self.assertEqual(m['radio_stagehands'][0]['object_id'],2678);self.assertEqual(c['related_review_rows'],1);self.assertEqual(len(build.V094_JAPANESE_RUINS_FIELDS),20)
  for a in self.review['scope']['assets']:
   for p in ['/baseType','/scriptConfig/behavior','/movementParameters/runSpeed']:self.assertNotIn((a,p),build.V094_JAPANESE_RUINS_FIELDS)
  self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(14,1248))

if __name__=='__main__':unittest.main()
