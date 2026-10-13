"""Guard new Greg sound bindings, bee puns, terrain clause and merchant field scope."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
from plan_translation import read,preserved_name
from qa_integrity import Terminology
import generate_v077 as gate
import build_validate as build
class V077Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=read(TOOLS/'v077_translations.json');cls.catalog=read(TOOLS/'ceviriler.json');cls.review=read(TOOLS.parent/'docs/reviews/crew3-20261013.json');cls.policy=read(TOOLS/'locked_terms.json')
    def unit(self,row):return dict(en=row['en'],tr=row['tr'],occurrences=[{k:row[k] for k in ('asset','pointer')}])
    def greg_row(self):return next(r for r in self.manifest['translations'] if r['asset']=='npcs/crew/crewmembergreg.npctype' and r['en']=='Greg?')
    def test_greg_speech_scope_and_rainbow_are_kept_distinct(self):
        sounds=[r for r in self.manifest['translations'] if r['asset']=='npcs/crew/crewmembergreg.npctype' and r['en']==r['tr']];self.assertEqual(len(sounds),36)
        for row in sounds:self.assertTrue(preserved_name(self.unit(row)))
        rainbow=[r for r in self.manifest['translations'] if r['en']=='Rainbow.'];self.assertEqual(len(rainbow),4)
        for row in rainbow:
            self.assertEqual(row['tr'],'Gökkuşağı.');self.assertFalse(preserved_name(self.unit(dict(row,tr=row['en']))))
        for key,value in [('asset','npcs/crew/neighbor.npctype'),('pointer','/scriptConfig/dialog/crewmember/follow/default/default/9999')]:
            row=dict(self.greg_row(),**{key:value});self.assertFalse(preserved_name(self.unit(row)))
        row=dict(self.greg_row(),en='Greg wants ordinary English.',tr='Greg wants ordinary English.');self.assertFalse(preserved_name(self.unit(row)))
        unit=self.unit(self.greg_row());unit['occurrences'].append(dict(asset='dialog/neighbor.config',pointer='/converse/0'));self.assertFalse(preserved_name(unit))
    def test_greg_binding_requires_active_preserve_and_complete_evidence(self):
        row=self.greg_row()
        for mutation in ('status','mode','reason','en','tr'):
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
                policy=copy.deepcopy(self.policy);term=next(t for t in policy['terms'] if t['source']=='Greg')
                if mutation=='status':term['status']='REVIEW'
                elif mutation=='mode':term.pop('mode')
                else:
                    binding=next(x for x in policy['context_exceptions'] if x.get('term_source')=='Greg' and x['asset']==row['asset'] and x['pointer']==row['pointer']);binding[mutation]=''
                tools=Path(directory);(tools/'locked_terms.json').write_text(json.dumps(policy),encoding='utf-8');self.assertFalse(preserved_name(self.unit(row),tools))
    def test_greg_intonation_cannot_change_while_retaining_name(self):
        row=self.greg_row();terms=Terminology(self.policy);terms.validate(row)
        for wrong in ('Greg.','Greg!?','Greg? Şaka yapıyorum.'):
            with self.subTest(wrong=wrong),self.assertRaisesRegex(ValueError,'LOCKED'):terms.validate(dict(row,tr=wrong))
    def test_reviewed_repeated_phrases_reject_original_regressions(self):
        terms=Terminology(self.policy)
        for correction in self.review['corrections']:
            row=dict(correction['occurrences'][0],en=correction['en'],tr=correction['after']);terms.validate(row)
            if correction['en'] in terms.exact or any(fragment in correction['en'] for fragment in ('bee-ing killed','tough-as-nails training','adrenal gland')):
                with self.subTest(en=row['en']),self.assertRaisesRegex(ValueError,'LOCKED'):terms.validate(dict(row,tr=correction['before']))
    def test_narrow_sail_and_bee_guards_do_not_capture_generic_verbs(self):
        terms=Terminology(self.policy);row=dict(asset='npcs/crew/fixture.npctype',pointer='/dialog/0',en='We interface with SAIL.',tr='SAIL ile bağlantı kuruyoruz.');terms.validate(row)
        with self.assertRaisesRegex(ValueError,'LOCKED'):terms.validate(dict(row,tr='Gemiyle bağlantı kuruyoruz.'))
        for en,tr in [('To sail among the stars.','Yıldızlar arasında yol almak.'),('Let us be friends.','Arkadaş olalım.'),('This gland is different.','Bu bez farklı.'),('Let us bee friends.','Arı-kadaş olalım.')]:terms.validate(dict(row,en=en,tr=tr))
        with self.assertRaisesRegex(ValueError,'LOCKED'):terms.validate(dict(row,en='Let us bee friends.',tr='Arkadaş olalım.'))
    def test_missing_terrain_clause_cannot_reuse_approval(self):
        gate.validate_manifest(self.manifest,self.catalog,self.review);broken=copy.deepcopy(self.manifest)
        row=next(r for r in broken['translations'] if r['en'].startswith('Floran will find enemy to ssstab!'));row['tr']=row['tr'].split('!')[0]+'!'
        with self.assertRaisesRegex(ValueError,'approved translation'):gate.validate_manifest(broken,self.catalog,self.review)
    def test_merchant_headings_do_not_open_price_or_item_fields(self):
        headings=[r for r in self.manifest['translations'] if r['pointer'].startswith('/scriptConfig/crew/interactData/')];self.assertEqual(len(headings),2)
        for row in headings:self.assertTrue(build.allowed(row['asset'],row['pointer']))
        for pointer in ('/scriptConfig/crew/interactData/buyFactor','/scriptConfig/crew/interactData/sellFactor','/scriptConfig/crew/interactData/items/0/item','/scriptConfig/crew/role/benefits/0/value'):
            self.assertFalse(build.allowed('npcs/crew/crewmembergeologist.npctype',pointer))
        broken=copy.deepcopy(self.manifest);broken['translations'][0]['qa']=dict(layered_source=True)
        with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(broken,self.catalog,self.review)
if __name__=='__main__':unittest.main()
