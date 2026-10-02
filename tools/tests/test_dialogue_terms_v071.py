"""Keep Skath inflections and Nightar blessings distinct from generic words."""
import json,sys,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from qa_integrity import Terminology

class DialogueTermsV071Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.terms=Terminology(json.loads((TOOLS/'locked_terms.json').read_text(encoding='utf-8')))
    def check(self,en,tr):self.terms.validate(dict(asset='dialog/converse.config',pointer='/converse/skath/skath/0',en=en,tr=tr))
    def test_skath_proper_names_remain_present_in_inflected_dialogue(self):
        for name in ('Vanguard',"Thel'Mara","Zah'Kal",'Nosverah'):
            with self.subTest(name=name):
                self.check('We know '+name+'.',name+"'yı biliyoruz.")
                with self.assertRaisesRegex(ValueError,'LOCKED'):self.check('We know '+name+'.','Biliyoruz.')
    def test_seekers_source_typo_uses_caste_name_without_locking_generic_seeker(self):
        self.check("The Seeker's found it.","Seekers'ın bulduğu şey.")
        self.check('The Seekers found it.','Seekers onu buldu.')
        self.check('A seeker found it.','Bir arayıcı buldu.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):self.check('The Seekers found it.','Arayıcılar onu buldu.')
    def test_plasma_weapon_core_and_profession_accept_turkish_inflection(self):
        self.check('My Plasmaspear plasmacore needs a phasesmith.','Plazma mızrağımın plazma çekirdeğini faz demircisine götürmeliyim.')
        for en,tr in [('My Plasmaspear.','Mızrağım.'),('The plasmacore.','Çekirdek.'),('A phasesmith.','Bir demirci.')]:
            with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):self.check(en,tr)
    def test_devourer_title_and_celestial_towers_have_guarded_stems(self):
        self.check('The Devourer and Celestial Towers.',"Yutucu ve Göksel Kuleleri.")
        self.check('A hungry devourer.','Aç bir yiyici.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):self.check('The Devourer.','Yiyip Bitiren.')
    def test_source_blessing_does_not_capture_general_source(self):
        self.check('May the Source be with you, kinsman.','Kaynak seninle olsun, soydaşım.')
        self.check('Find the source.','Kökeni bul.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):self.check('May the Source be with you, kinsman.','Köken seninle olsun.')

if __name__=='__main__':unittest.main()
