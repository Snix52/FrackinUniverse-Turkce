"""Protect source-only questgiver translations, raw variants and unverified-visibility limits."""
import copy,sys,unittest
from collections import Counter
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v102 as gate

class V102Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=read(TOOLS/'v102_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.policy=read(TOOLS/'locked_terms.json');cls.review=read(TOOLS.parent/'docs/reviews/microdungeons-20261107.json')
 def row(self,en):return next(r for r in self.manifest['translations']if r['en']==en)
 def test_exact_scope_neighbor_and_provenance(self):
  gate.validate_manifest(self.manifest,self.catalog,self.review)
  for k,v in [('asset','npcs/outpostcivilian.npctype'),('pointer','/scriptConfig/offeredQuests'),('en','A new quest grants power.'),('tr','Kaynak dışı bir metin.')]:
   bad=copy.deepcopy(self.manifest);bad['translations'][0][k]=v
   with self.subTest(key=k),self.assertRaisesRegex(ValueError,'scope/count drift|approved translation'):gate.validate_manifest(bad,self.catalog,self.review)
  bad=copy.deepcopy(self.manifest);bad['translations'][0]['qa']={'layered_source':True}
  with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(bad,self.catalog,self.review)
 def test_every_occurrence_rejects_wrong_translation(self):
  e=Terminology(self.policy)
  for r in self.manifest['translations']:
   e.validate(r)
   with self.subTest(asset=r['asset'],pointer=r['pointer']),self.assertRaisesRegex(ValueError,'LOCKED'):e.validate(dict(r,tr='İlgisiz bir cümle.'))
 def test_complete_family_speaker_and_target_branches(self):
  rows=self.manifest['translations'];self.assertEqual((len(rows),len({r['en']for r in rows})),(9,6));self.assertEqual(sorted(Counter(r['asset']for r in rows).values()),[3,3,3]);self.assertTrue(all('/converse/'in r['pointer']for r in rows));self.assertEqual(sum('/converse/apex/apex/'in r['pointer']for r in rows),3);self.assertEqual(sum('/converse/apex/default/'in r['pointer']for r in rows),3);self.assertTrue(self.review['source_context']['speaker_and_target_branches_distinguished']);self.assertEqual(self.review['scope']['excluded_review_fields'],16)
 def test_title_is_preserved_without_preserving_english_sentence(self):
  en='I grew weary of watching Jersey Shore like all the other idiots out there. I turned to murder, instead.';r=self.row(en);self.assertEqual(r['tr'],'Diğer bütün aptallar gibi Jersey Shore izlemekten bıktım. Onun yerine cinayete yöneldim.');self.assertFalse(preserved_name(dict(en='Jersey Shore',tr='Jersey Shore',occurrences=[dict(asset='ordinary',pointer='/shortdescription')])));self.assertFalse(preserved_name(dict(en=en,tr=en,occurrences=[dict(asset=r['asset'],pointer=r['pointer'])])))
  with self.assertRaisesRegex(ValueError,'LOCKED'):Terminology(self.policy).validate(dict(r,tr=r['tr'].replace('Jersey Shore','Jersey Kıyısı')))
  Terminology(self.policy).validate(dict(asset='ordinary',pointer='/description',en='The shore is quiet.',tr='Kıyı sessiz.'))
 def test_absurd_humor_and_single_changed_expression(self):
  self.assertEqual(self.row("I don't think anyone should eat thumbtacks.")['tr'],'Bence kimse raptiye yememeli.');self.assertEqual(self.row("I've never seen a unicorn that farts fire before. Have you?")['tr'],'Daha önce ateş osuran bir tek boynuzlu at görmedim. Ya sen?');self.assertEqual([c['unit_index']for c in self.review['corrections']],[2]);self.assertEqual([c['changed_sentences']for c in self.review['corrections']],[1]);self.assertEqual((self.review['changes']['total_corrected_fields'],self.review['changes']['total_corrected_sentences']),(1,1));self.assertEqual((self.review['new_locked_terms'],self.review['locked_total']),(6,1335))
 def test_whitespace_variants_share_forms_without_changing_raw_source(self):
  a='I grew weary of watching my Apex brothers and sisters being tormented at the hands of the Miniknog, so I left.';b=a.replace('sisters being','sisters  being');rows=[r for r in self.manifest['translations']if r['en']in(a,b)];self.assertEqual(Counter(r['en']for r in rows),{a:2,b:2});self.assertEqual({r['tr']for r in rows},{'Miniknog’un Apex kardeşlerime eziyet etmesini izlemekten bıkınca oradan ayrıldım.'});term=next(t for t in self.policy['terms']if t['source']==a);self.assertEqual({x['en']for x in term['forms']},{a,b});self.assertEqual(self.review['reused_proper_names'],['Miniknog']);self.assertEqual(self.review['context_bindings'],[]);self.assertEqual(self.review['preserve_bindings'],[])
 def test_source_scope_decision_is_not_visibility_or_pool_promotion(self):
  d=self.review['source_context']['source_visibility_review'];self.assertEqual(d['status'],'SOURCE_REVIEW_RESOLVED');self.assertTrue(d['translation_source_scope_approved']);self.assertFalse(d['runtime_visibility_verified']);self.assertFalse(d['pool_promotion']);self.assertFalse(d['rule_exception_added']);self.assertEqual(d['packet_sha256'],self.review['luna_original_packet_sha256']);self.assertEqual(len(d['requests']),6);self.assertEqual({x['asset']for x in d['requests']},{'npcs/microdungeons/primevalquestgiver.npctype','npcs/microdungeons/wastelandquestgiver.npctype'});index={(r['asset'],r['pointer'],r['en']):r['tr']for r in self.manifest['translations']}
  for x in d['requests']:self.assertEqual(index[(x['asset'],x['pointer'],x['en'])],x['tr'])
  self.assertFalse(self.review['scope']['live_runtime_visibility_verified'])
 def test_pixels_quest_comments_and_missing_base_do_not_become_live_proof(self):
  import build_validate as build
  c=self.review['source_context'];m=c['mission'];self.assertEqual(m['primeval_exact_selected_rgba_pixels'],0);self.assertFalse(m['wasteland_active_world_reference_verified']);self.assertEqual([sum(sum(x['selected_color_pixels'].values())for x in d['pixels'])for d in m['image_dungeons']],[0,1]);self.assertEqual(len(m['image_dungeons'][0]['pixels']),6);self.assertEqual(len(m['biome_links']),22);self.assertEqual(m['tmx_maps'][0]['selected_static_npcs'][0]['npc'],'human');self.assertEqual((len(m['tmx_maps'][0]['tilesets']),sum(not t['available']for t in m['tmx_maps'][0]['tilesets'])),(38,34));self.assertEqual(m['tmx_maps'][0]['radio_parameters'],[]);self.assertEqual(next(x for x in c['npcs']if x['type']=='primevalquestgiver')['script_config_quest_links'],{});self.assertFalse(c['active_consumer_verified']);self.assertEqual(self.review['lqa_status'],'NOT TESTED');self.assertEqual(len(build.V102_MICRODUNGEONS_FIELDS),9)
  for asset in self.review['scope']['assets']:
   for ptr in('/baseType','/scriptConfig/offeredQuests','/items/override'):self.assertNotIn((asset,ptr),build.V102_MICRODUNGEONS_FIELDS)

if __name__=='__main__':unittest.main()
