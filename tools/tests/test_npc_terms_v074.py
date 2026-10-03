"""Guard occupation titles, source names and a reviewed price localization."""
import json,sys,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from qa_integrity import Terminology,validate_format
from plan_translation import read

class NpcTermsV074Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terms=Terminology(read(TOOLS/'locked_terms.json'))
        cls.policy=read(TOOLS/'rules/text_integrity.json')
    def check(self,en,tr):
        self.terms.validate(dict(asset='npcs/itamae.npctype',pointer='/scriptConfig/dialog/test/0',en=en,tr=tr))
    def test_itamae_occupation_cannot_revert_to_english(self):
        self.check('  Itamae','  Suşi Şefi')
        self.check('An Itamae works here.','Burada bir Suşi Şefi çalışıyor.')
        for tr in ('  Itamae','  Şef'):
            with self.subTest(tr=tr),self.assertRaisesRegex(ValueError,'LOCKED'):
                self.check('  Itamae',tr)
    def test_svetlana_full_name_is_not_shortened_or_translated(self):
        self.check('Svetlana Twofeather speaks.','Svetlana Twofeather konuşuyor.')
        self.check('Ask Svetlana.','Svetlana’ya sor.')
        for tr in ('Svetlana konuşuyor.','Svetlana İki Tüy konuşuyor.'):
            with self.subTest(tr=tr),self.assertRaisesRegex(ValueError,'LOCKED'):
                self.check('Svetlana Twofeather speaks.',tr)
    def test_source_handles_are_preserved_without_capturing_generic_words(self):
        self.check('The Observer made Extra Dungeons.','Extra Dungeons’ı The Observer yaptı.')
        for tr in ('Extra Dungeons’ı Gözlemci yaptı.','Ek Zindanlar’ı The Observer yaptı.'):
            with self.subTest(tr=tr),self.assertRaisesRegex(ValueError,'LOCKED'):
                self.check('The Observer made Extra Dungeons.',tr)
        self.check('An observer visits the dungeons.','Bir gözlemci zindanları geziyor.')
    def test_price_separator_localization_preserves_the_entire_amount(self):
        row=dict(asset='npcs/parlorvendor.npctype',pointer='/scriptConfig/dialog/test/0',
                 en='A single scoop starts at 300,000 pixels... kidding! Just kidding!',
                 tr='Bir top dondurma 300.000 pikselden başlıyor... şaka! Şaka yaptım!')
        validate_format(row,self.policy)
        for bad in ('300','30.000','300.001'):
            with self.subTest(bad=bad),self.assertRaisesRegex(ValueError,'Number mismatch'):
                validate_format(dict(row,tr=row['tr'].replace('300.000',bad)),self.policy)

if __name__=='__main__':unittest.main()
