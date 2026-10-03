"""Prevent corrected dialogue terms from drifting or capturing unrelated words."""
import copy,json,sys,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from qa_integrity import Terminology
from plan_translation import read

class NpcTermsV073Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.terms=Terminology(read(TOOLS/'locked_terms.json'))
    def check(self,en,tr):self.terms.validate(dict(asset='npcs/barista.npctype',pointer='/scriptConfig/dialog/test/0',en=en,tr=tr))
    def test_brand_size_sequence_is_guarded_but_general_adjectives_are_free(self):
        en='Will that be a short, a tall, a grande, a venti?'
        self.check(en,'Short mu, Tall mı, Grande mi, Venti mi?')
        for tr in ('Kısa mı, uzun mu, grande mi, venti mi?','Grande mi, Venti mi?'):
            with self.subTest(tr=tr),self.assertRaisesRegex(ValueError,'LOCKED'):self.check(en,tr)
        self.check('A short path beside a tall tree.','Uzun bir ağacın yanındaki kısa yol.')
    def test_keep_noun_and_protector_title_do_not_capture_generic_uses(self):
        self.check('I could afford a keep.','Bir iç kale alabilirdim.')
        self.check('Are you a Protector?','Protector mısın?')
        self.check('Keep it safe.','Güvende tut.')
        self.check('Protector Plating','Koruyucu Kaplama')
        for en,tr in [('I could afford a keep.','Bir malikâne alabilirdim.'),('Are you a Protector?','Koruyucu musun?')]:
            with self.subTest(en=en),self.assertRaisesRegex(ValueError,'LOCKED'):self.check(en,tr)
    def test_lore_and_shop_names_keep_their_verified_stems(self):
        self.check('The Consul speaks of the Wanderers and Greenguard.','Konsül, Gezginler ve Greenguard’dan söz ediyor.')
        self.check("Four Felins' Coffee Corner sells kopi luwak near Marty's Place.",'Dört Felin Kahve Köşesi, Marty’nin Yeri yakınında kopi luwak satar.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):self.check('The Consul speaks.','Hükümdar konuşuyor.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):self.check('Greenguard help Floran!','Yeşil Muhafız Floran’a yardım et!')
    def test_ace_high_praise_cannot_become_a_different_card_game(self):
        self.check('My meals are ace-high!','Yemeklerim birinci sınıftır!')
        with self.assertRaisesRegex(ValueError,'LOCKED'):self.check('My meals are ace-high!','Yemeklerim papaz kaçtı!')
    def test_old_protector_lines_keep_reapproval_history_and_reject_old_text(self):
        import generate_v072
        manifest=read(TOOLS/'v072_translations.json');catalog=read(TOOLS/'ceviriler.json')
        review=read(TOOLS.parent/'docs/reviews/dialogue6-20261003.json')
        revision=review['subsequent_reviews'][-1]
        self.assertEqual(revision['release'],'0.73.0-beta')
        self.assertEqual(len(revision['changes']),2)
        self.assertNotEqual(revision['previous_approval']['approved_rows_sha256'],review['approved_rows_sha256'])
        generate_v072.validate_manifest(manifest,catalog,review)
        broken=copy.deepcopy(manifest)
        row=next(r for r in broken['translations'] if "No wonder you're a Protector." in r['en'])
        row['tr']=row['tr'].replace('Protector olman','Koruyucu olman')
        with self.assertRaisesRegex(ValueError,'approved translation'):generate_v072.validate_manifest(broken,catalog,review)

if __name__=='__main__':unittest.main()
