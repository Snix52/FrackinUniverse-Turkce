"""Prevent Greg scope leaks and recurring technical/music translation regressions."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v078 as gate
import build_validate as build
class V078Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=read(TOOLS/'v078_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.review=read(TOOLS.parent/'docs/reviews/crew4-20261017.json');cls.policy=read(TOOLS/'locked_terms.json')
    def unit(self,row):return dict(en=row['en'],tr=row['tr'],occurrences=[{k:row[k] for k in ('asset','pointer')}])
    def sounds(self):return [r for r in self.manifest['translations'] if r['en']==r['tr']]
    def test_greg_sounds_exact_nine_do_not_authorize_rainbow_or_neighbors(self):
        self.assertEqual(len(self.sounds()),9)
        for row in self.sounds():self.assertTrue(preserved_name(self.unit(row)))
        rainbow=[r for r in self.manifest['translations'] if r['en']=='Rainbow.'];self.assertEqual(len(rainbow),1);self.assertEqual(rainbow[0]['tr'],'Gökkuşağı.')
        row=self.sounds()[0]
        for wrong in [dict(row,pointer=row['pointer']+'/unapproved'),dict(row,asset='npcs/crew/neighbor.npctype'),dict(row,en='Greg needs help.',tr='Greg needs help.'),dict(rainbow[0],tr='Rainbow.')]:
            with self.subTest(wrong=wrong):self.assertFalse(preserved_name(self.unit(wrong)))
        unit=self.unit(row);unit['occurrences'].append(dict(asset='dialog/greg.config',pointer='/converse/default/default/9999'));self.assertFalse(preserved_name(unit))
    def test_greg_approval_requires_full_record_and_active_preserve(self):
        row=self.sounds()[0]
        for mutation in ('reason','en','tr','status','mode'):
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
                policy=copy.deepcopy(self.policy);term=next(t for t in policy['terms'] if t['source']=='Greg')
                if mutation=='status':term['status']='REVIEW'
                elif mutation=='mode':term.pop('mode')
                else:next(x for x in policy['context_exceptions'] if x.get('term_source')=='Greg' and x['asset']==row['asset'] and x['pointer']==row['pointer'])[mutation]=''
                tools=Path(directory);(tools/'locked_terms.json').write_text(json.dumps(policy),encoding='utf-8');self.assertFalse(preserved_name(self.unit(row),tools))
    def test_greg_spelling_and_intonation_cannot_change_while_name_remains(self):
        terms=Terminology(self.policy)
        for row in self.sounds():
            terms.validate(row)
            with self.subTest(en=row['en']),self.assertRaisesRegex(ValueError,'LOCKED'):terms.validate(dict(row,tr=row['tr']+' Greg?'))
    def test_technical_and_weapon_metaphors_reject_literal_regressions(self):
        terms=Terminology(self.policy);base=dict(asset='npcs/crew/fixture.npctype',pointer='/dialog/0')
        cases=[('Do not forget your bio-antivirus!','Biyoantivirüsünü unutma!','Biyovirüs koruyucunu unutma!'),('I can overclock the warp drive.','Warp motoruna hız aşırtma uygulayabilirim.','Warp motorunu hız aşırtabilirim.'),('BIOSTRUCTURE REINFORCED.','BİYOLOJİK YAPI GÜÇLENDİRİLDİ.','BİYÖNİTE GÜÇLENDİRİLDİ.'),('IFF SYSTEMS DAMAGED.','DOST-DÜŞMAN TANIMA SİSTEMLERİ HASARLI.','IFF SİSTEMLERİ HASARLI.'),('I can help cure poison!','Zehirlenmeyi gidermeye yardım edebilirim!','Zehri iyileştirmeye yardım edebilirim!'),('I lend my arms and skill in battle.','Silahlarımı ve savaş becerimi sunarım.','Kollarımı ve savaş becerimi sunarım.')]
        for en,good,bad in cases:
            terms.validate(dict(base,en=en,tr=good))
            with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):terms.validate(dict(base,en=en,tr=bad))
    def test_music_and_exact_repeated_lines_reject_old_wording(self):
        terms=Terminology(self.policy)
        for correction in self.review['corrections']:
            row=dict(correction['occurrences'][0],en=correction['en'],tr=correction['after']);terms.validate(row)
            if correction['en'] in terms.exact or 'badass lick' in correction['en']:
                with self.subTest(en=row['en']),self.assertRaisesRegex(ValueError,'LOCKED'):terms.validate(dict(row,tr=correction['before']))
    def test_narrow_terms_do_not_capture_anatomy_cat_licks_or_other_hardware(self):
        terms=Terminology(self.policy);base=dict(asset='npcs/crew/fixture.npctype',pointer='/dialog/0')
        for en,tr in [('My arms are tired.','Kollarım yoruldu.'),('The cat licks its fur.','Kedi kürkünü yalıyor.'),('I overclock a processor.','İşlemciyi hızlandırıyorum.'),('The metal is cold.','Metal soğuk.'),('Riffs and scales.','Riffler ve gamlar.')]:terms.validate(dict(base,en=en,tr=tr))
    def test_language_approval_cannot_be_reused_after_clause_loss_or_scope_change(self):
        gate.validate_manifest(self.manifest,self.catalog,self.review)
        broken=copy.deepcopy(self.manifest);row=next(r for r in broken['translations'] if r['en'].startswith('DANGER: FOREIGN ELEMENTS'));row['tr']=row['tr'].split('.')[0]+'.'
        with self.assertRaisesRegex(ValueError,'approved translation'):gate.validate_manifest(broken,self.catalog,self.review)
        for pointer in ('/scriptConfig/crew/role/benefits/0/value','/scriptConfig/crew/role/benefits/0/duration','/scriptConfig/crew/role/benefits/0/effect'):
            self.assertFalse(build.allowed('npcs/crew/crewmemberprecursor.npctype',pointer))
        broken=copy.deepcopy(self.manifest);broken['translations'][0]['qa']=dict(layered_source=True)
        with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(broken,self.catalog,self.review)
if __name__=='__main__':unittest.main()
