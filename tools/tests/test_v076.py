"""Reject repeated crew regressions and any widening of fictional speech approval."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v076 as gate
import build_validate as build

class V076Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=read(TOOLS/'v076_translations.json');cls.catalog=read(TOOLS/'ceviriler.json')
        cls.review=read(TOOLS.parent/'docs/reviews/crew2-20261012.json');cls.policy=read(TOOLS/'locked_terms.json')
    def test_crew_hiss_target_and_speaker_regressions_are_locked(self):
        terms=Terminology(self.policy)
        for correction in self.review['corrections']:
            if correction['en'] not in terms.exact:continue
            row=dict(correction['occurrences'][0],en=correction['en'],tr=correction['after'])
            terms.validate(row)
            with self.subTest(en=row['en']),self.assertRaisesRegex(ValueError,'LOCKED'):
                terms.validate(dict(row,tr=correction['before']))
        terms.validate(dict(asset='npcs/crew/fixture.npctype',pointer='/dialog/0',en='Floran wants help.',tr='Floran yardım istiyor.'))
    def agaran_unit(self):
        row=next(r for r in self.manifest['translations'] if r['asset']=='npcs/crew/crewmemberagaran.npctype')
        return dict(en=row['en'],tr=row['tr'],occurrences=[{k:row[k] for k in ('asset','pointer')}])
    def test_only_seven_exact_agaran_fields_can_stay_unchanged(self):
        rows=[r for r in self.manifest['translations'] if r['asset']=='npcs/crew/crewmemberagaran.npctype']
        self.assertEqual(len(rows),7)
        for r in rows:
            unit=dict(en=r['en'],tr=r['tr'],occurrences=[{k:r[k] for k in ('asset','pointer')}])
            self.assertTrue(preserved_name(unit))
        for key,value in [('asset','npcs/crew/other.npctype'),('pointer','/scriptConfig/dialog/crewmember/offer/default/default/99999')]:
            unit=copy.deepcopy(self.agaran_unit());unit['occurrences'][0][key]=value
            self.assertFalse(preserved_name(unit))
        unit=self.agaran_unit();unit['en']=unit['tr']='Agaran says ordinary English.'
        self.assertFalse(preserved_name(unit))
        unit=self.agaran_unit();unit['occurrences'].append(dict(asset='dialog/neighbor.config',pointer='/converse/0'))
        self.assertFalse(preserved_name(unit))
    def test_agaran_binding_requires_active_preserve_lock_reason_and_text(self):
        unit=self.agaran_unit()
        for mutation in ('lock','mode','reason','en','tr'):
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
                policy=copy.deepcopy(self.policy);term=next(t for t in policy['terms'] if t['source']=='Agaran')
                if mutation=='lock':term['status']='REVIEW'
                elif mutation=='mode':term.pop('mode')
                else:
                    binding=next(x for x in policy['context_exceptions'] if x.get('term_source')=='Agaran' and x['pointer']==unit['occurrences'][0]['pointer'])
                    binding[mutation]=''
                tools=Path(directory);(tools/'locked_terms.json').write_text(json.dumps(policy),encoding='utf-8')
                self.assertFalse(preserved_name(unit,tools))
    def test_frakinmon_name_and_inflection_are_guarded(self):
        terms=Terminology(self.policy);row=dict(asset='npcs/crew/fixture.npctype',pointer='/dialog/0',en='What starter FrakinMon did you pick?',tr="Hangi başlangıç FrakinMon'unu seçtin?")
        terms.validate(row)
        for wrong in ('Hangi başlangıç FrackinMon’unu seçtin?','Hangi başlangıç yaratığını seçtin?'):
            with self.assertRaisesRegex(ValueError,'LOCKED'):terms.validate(dict(row,tr=wrong))
    def test_language_change_cannot_reuse_approval(self):
        gate.validate_manifest(self.manifest,self.catalog,self.review)
        broken=copy.deepcopy(self.manifest);next(r for r in broken['translations'] if 'Have you sseen' in r['en'])['tr']='Floran komutanı gördü mü?'
        with self.assertRaisesRegex(ValueError,'approved translation'):gate.validate_manifest(broken,self.catalog,self.review)
    def test_direct_fields_cannot_gain_unreviewed_provenance(self):
        broken=copy.deepcopy(self.manifest);broken['translations'][0]['qa']=dict(layered_source=True)
        with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(broken,self.catalog,self.review)
    def test_approved_dialogue_allowlist_keeps_technical_neighbors_closed(self):
        for r in self.manifest['translations']:self.assertTrue(build.allowed(r['asset'],r['pointer']))
        self.assertFalse(build.allowed('npcs/crew/crewmemberchef3.npctype','/scriptConfig/crew/role/benefits/0/value'))
        self.assertFalse(build.allowed('npcs/crew/crewmemberagaran.npctype','/scriptConfig/dialog/crewmember/offer/default/default/99999'))

if __name__=='__main__':unittest.main()
