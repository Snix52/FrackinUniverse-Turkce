"""Guard Snow Crash dialogue meaning, bindings and bounded runtime evidence."""
import copy
import sys
import unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v086 as gate

class V086Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v086_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.review=read(TOOLS.parent/'docs/reviews/snowcrash-20261101.json');cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_manifest_direct_provenance_and_neighbor_rejected(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for key,value in [('pointer','/scriptConfig/dialog/attack/neighbor/0'),('asset','npcs/snowcrash/unknown.npctype'),('en','Invented source'),('tr','Başka bir cümle.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_all_sixteen_delivered_regressions_locked(self):
  engine=Terminology(self.policy);changes=self.review['corrections'];self.assertEqual(len(changes),16);self.assertEqual(sum(c['changed_sentences']for c in changes),18)
  for c in changes:
   row=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(row)
   with self.subTest(pointer=row['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(row,tr=c['before']))
 def test_hostage_uncertainty_present_fallback_and_stockup_scope(self):
  rows=self.manifest['translations'];hostage=next(r for r in rows if r['asset'].endswith('hostage.npctype') and '/apex/'in r['pointer'])
  self.assertIn('temizlediysen',hostage['tr']);self.assertIn('bakabilirim sanırım',hostage['tr']);self.assertIn('bodruma in',hostage['tr']);self.assertNotIn('düşmanlardan',hostage['tr'])
  fallbacks=[r for r in rows if r['en']=="You shouldn't be seeing this."];self.assertEqual(len(fallbacks),2);self.assertTrue(all(r['tr']=='Bunu görüyor olmamalısın.'for r in fallbacks))
  load=self.row("Don't forget to load up before you go. We don't have much, but we'll sell you what we can.");self.assertIn('malzemelerini tamamlamayı',load['tr']);self.assertIn('satabileceğimiz ne varsa',load['tr'])
 def test_switch_instruction_matches_existing_radio_without_global_switch_lock(self):
  row=self.row('Watch out for explosive barrels under switches. You can blow those up to destroy and deactivate the switch.')
  self.assertEqual(row['tr'],'Şalterlerin altındaki patlayıcı varillere dikkat et. Varilleri patlatarak şalteri yok edip devre dışı bırakabilirsin.')
  radio=next(r for r in self.catalog['translations']if r['asset']=='radiomessages/missions.radiomessages' and r['pointer']=='/snowcrash05/text');self.assertIn('şalteri',radio['tr']);self.assertFalse(any(t['source'].casefold()=='switch'for t in self.policy['terms']))
 def test_name_and_dacha_locked_but_ordinary_english_not_preserved(self):
  engine=Terminology(self.policy);winter=next(t for t in self.policy['terms']if t['source']=='Winter-Chan');self.assertEqual(winter['mode'],'preserve')
  engine.validate(dict(asset='fixture',pointer='/text',en='Beyond the dacha.',tr='Daçanın ötesinde.'))
  with self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(asset='fixture',pointer='/text',en='Beyond the dacha.',tr='Köşkün ötesinde.'))
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='Alakasız bir cümle.'))
   self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='Winter-Chan needs help.',tr='Winter-Chan needs help.',occurrences=[dict(asset='fixture',pointer='/text')])))
 def test_map_species_discrepancy_and_other_npc_counts_are_not_invented(self):
  c=self.review['source_context'];self.assertEqual(len(c['static_placements']),41);self.assertTrue(all(o['properties']['npc']=='apex'for o in c['static_placements']));self.assertEqual(c['placement_counts']['snowcrashrocketeer'],5)
  rows=[r for r in self.manifest['translations']if r['asset'].endswith('rocketeer.npctype') and '/avian/'in r['pointer']];self.assertEqual(len(rows),6)
  self.assertEqual(len(c['merchant_placements']),1);self.assertEqual(len(c['labscientist_placements']),2);self.assertEqual(len(c['radio_stagehands']),7)
 def test_missing_tilesets_and_event_consumers_remain_unverified(self):
  c=self.review['source_context'];self.assertFalse(c['active_consumer_verified']);self.assertEqual(c['map']['wire_records'],92);self.assertEqual(sum(not t['exists']for t in c['map']['tilesets']),20);self.assertEqual(c['world_definitions']['instance_worlds.config.patch']['dungeonWorld'],'snowcrash');self.assertEqual(self.review['lqa_status'],'NOT TESTED')
 def test_exact_allowlist_excludes_engine_identity_and_parent_fields(self):
  import build_validate as build
  self.assertEqual(len(build.V086_SNOWCRASH_FIELDS),53)
  for r in self.manifest['translations']:self.assertIn((r['asset'],r['pointer']),build.V086_SNOWCRASH_FIELDS)
  for pointer in ('/type','/baseType','/identity/name','/scriptConfig/behavior','/scriptConfig/dialog/attack'):
   self.assertNotIn(('npcs/snowcrash/snowcrashcomissar.npctype',pointer),build.V086_SNOWCRASH_FIELDS)
if __name__=='__main__':unittest.main()
