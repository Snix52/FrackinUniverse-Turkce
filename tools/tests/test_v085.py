"""Protect Nightar rhetoric, authored identities and bounded source evidence."""
import copy
import sys
import unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v085 as gate

class V085Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v085_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.review=read(TOOLS.parent/'docs/reviews/nightar-20261101.json');cls.policy=read(TOOLS/'locked_terms.json')
 def row(self,en):return next(r for r in self.manifest['translations'] if r['en']==en)
 def test_exact_manifest_and_direct_provenance_closed(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review);self.assertEqual(len(self.manifest['translations']),58)
  for key,value in [('pointer','/scriptConfig/dialog/attack/neighbor/0'),('asset','npcs/nightar/unknown.npctype'),('tr','A new power.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][key]=value
   with self.subTest(key=key),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True,'source_patch':'wrong.patch'}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_all_eight_delivered_regressions_rejected(self):
  engine=Terminology(self.policy);changes=self.review['corrections'];self.assertEqual(len(changes),8);self.assertEqual(sum(x['changed_sentences'] for x in changes),9)
  for c in changes:
   row=dict(c['occurrences'][0],en=c['en'],tr=c['after']);engine.validate(row)
   with self.subTest(pointer=row['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(row,tr=c['before']))
 def test_matriarch_was_already_correct_and_not_counted_as_sol_edit(self):
  rows=[r for r in self.manifest['translations'] if 'Matriarch' in r['tr']];self.assertEqual(len(rows),4)
  changed={(o['asset'],o['pointer']) for c in self.review['corrections'] for o in c['occurrences']};self.assertTrue(all((r['asset'],r['pointer'])not in changed for r in rows))
  self.assertTrue(all('Avemnedara'not in r['tr'] for r in self.manifest['translations']))
  old=next(t for t in self.policy['terms'] if t['source']=='The Matriarch');self.assertEqual(old['tr'],'Matriarch')
 def test_king_identity_and_self_designation_are_not_reconciled_by_invention(self):
  c=self.review['source_context'];kings=[n for n in c['npcs'] if n['type'] in ('nightarking','nightarking2')];self.assertEqual(len(kings),2)
  self.assertTrue(all(n['identity']['name']=='Gin_Yorukishi_III' for n in kings));self.assertEqual(len({n['type'] for n in kings}),2)
  en='I am Heptarch. I alone defeated one-thousand foes and was made glorious through victory. Kneel.'
  rows=[r for r in self.manifest['translations'] if r['en']==en];self.assertEqual(len(rows),2)
  for r in rows:self.assertIn('Heptarch',r['tr']);self.assertIn('bin düşmanı',r['tr']);self.assertNotIn('Gin_',r['tr'])
  friend=next(n for n in c['npcs'] if n['type']=='friendlykingslayer');foe=next(n for n in c['npcs'] if n['type']=='nightarkingslayer');self.assertEqual(friend['damage_team_type'],'assistant');self.assertEqual(friend['base_type'],'friendlyguard');self.assertEqual(foe['base_type'],'hostile')
 def test_parallel_statement_and_physical_strength_not_revenge_or_anatomy_label(self):
  self.assertEqual(self.row('Honor meets honor. Blood meets blood.')['tr'],'Şeref şerefle buluşur. Kan kanla buluşur.')
  self.assertEqual(self.row('Blade and sinew. The way is clear.')['tr'],'Kılıç ve kas gücü. Yol açık.')
  self.assertEqual(self.row('Your death comes this day.')['tr'],'Bugün öleceksin.')
 def test_base_patch_is_broader_than_timings_and_map18_not_registered(self):
  c=self.review['source_context'];self.assertIn('/scriptConfig/chatSounds/nightar',c['base_patch_paths']);self.assertIn('/statusControllerSettings/primaryScriptSources/-',c['base_patch_paths'])
  self.assertEqual(len(c['static_placements']),3);self.assertEqual(c['root_dungeon_anchors'],['funderground'+str(i) for i in range(1,18)]);self.assertEqual(c['root_dungeon_parts'],c['root_dungeon_anchors']);self.assertFalse(c['active_consumer_verified']);self.assertEqual(len(c['exact_identifier_reference_files']),11)
 def test_full_replies_locked_without_ordinary_english_permission(self):
  engine=Terminology(self.policy);self.assertEqual(self.review['new_locked_terms'],25)
  for r in self.manifest['translations']:
   engine.validate(r)
   with self.subTest(pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):engine.validate(dict(r,tr='Alakasız bir cümle.'))
   self.assertFalse(preserved_name(dict(en=r['en'],tr=r['en'],occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  self.assertFalse(preserved_name(dict(en='Heptarch needs help.',tr='Heptarch needs help.',occurrences=[dict(asset='fixture',pointer='/text')])))
 def test_allowlist_excludes_identity_and_motor_fields(self):
  import build_validate as build
  for r in self.manifest['translations']:self.assertTrue(build.allowed(r['asset'],r['pointer']))
  for pointer in ('/type','/baseType','/identity/name','/scriptConfig/dialog/attack'):
   self.assertNotIn(('npcs/nightar/nightarking.npctype',pointer),build.V085_NIGHTAR_FIELDS)
if __name__=='__main__':unittest.main()
