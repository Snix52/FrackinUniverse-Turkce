"""Keep reviewed crew names, feline puns and military hiss variants distinct."""
import copy,sys,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from plan_translation import read
from qa_integrity import Terminology

class CrewTermsV075Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.terms=Terminology(read(TOOLS/'locked_terms.json'))
    def check(self,en,tr):self.terms.validate(dict(asset='npcs/crew/fixture.npctype',pointer='/scriptConfig/dialog/test/0',en=en,tr=tr))
    def test_regular_and_floran_military_answers_cannot_be_interchanged(self):
        self.check('SIR, YES SIR!','EMREDERSİNİZ, EFENDİM!')
        for en in ('SSIR, YES SSSSIR!','SSIR, YESSSS SIR!'):
            self.check(en,'EMREDERSSİNİZ, EFENDİM!')
            for wrong in ('SSS, EVET EFENDİM!','EMREDERSİNİZ, EFENDİM!'):
                with self.subTest(en=en,wrong=wrong),self.assertRaisesRegex(ValueError,'LOCKED'):self.check(en,wrong)
        with self.assertRaisesRegex(ValueError,'LOCKED'):self.check('SIR, YES SIR!','EMREDERSSİNİZ, EFENDİM!')
        self.check('Wait here, sir.','Burada bekleyin, efendim.')
    def test_feline_pun_is_guarded_without_capturing_plain_perfect(self):
        self.check('A purrfect outfit.','Mır-kemmel bir kıyafet.')
        self.check('Meow! Purrfect!','Miyav! Mır-kemmel!')
        with self.assertRaisesRegex(ValueError,'LOCKED'):self.check('A purrfect outfit.','Mükemmel bir kıyafet.')
        self.check('A perfect outfit.','Mükemmel bir kıyafet.')
    def test_verified_names_keep_their_stems_without_capturing_generic_words(self):
        self.check('Lovelius Smythe enters Beast Mode.','Lovelius Smythe, Canavar Modu’na giriyor.')
        self.check('Greetings, Number One.','Selam, Bir Numara.')
        for en,tr in [('Lovelius Smythe speaks.','Lovelius konuşuyor.'),('Enter Beast Mode.','Savaş Modu’na gir.'),('Greetings, Number One.','Selam, Birinci Subay.')]:
            with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):self.check(en,tr)
        self.check('One captain sees a beast.','Bir kaptan bir canavar görüyor.')
    def test_old_ordinal_question_cannot_reuse_review_approval(self):
        import generate_v075 as gate
        manifest=read(TOOLS/'v075_translations.json');catalog=read(TOOLS/'ceviriler.json');review=read(TOOLS.parent/'docs/reviews/crew1-20261004.json')
        gate.validate_manifest(manifest,catalog,review)
        broken=copy.deepcopy(manifest)
        row=next(r for r in broken['translations'] if "THAT'SSS 42" in r['en'])
        row['tr']=row['tr'].replace('BU HAFTA 42 OLDU!','BU HAFTA 42. Mİ?!')
        with self.assertRaisesRegex(ValueError,'approved translation'):gate.validate_manifest(broken,catalog,review)

if __name__=='__main__':unittest.main()
