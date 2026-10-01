"""Prevent reviewed Nightar/Floran lore and inflected drink names from drifting."""
import json
from pathlib import Path
import sys
import unittest

TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from qa_integrity import Terminology


class DialogueTermsV070Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy=json.loads((TOOLS/'locked_terms.json').read_text(encoding='utf-8'))
        cls.terms=Terminology(cls.policy)

    def check(self,en,tr):
        self.terms.validate(dict(asset='dialog/converse.config',pointer='/converse/nightar/nightar/0',en=en,tr=tr))

    def test_matriarch_title_does_not_capture_generic_rat_mother(self):
        self.check('By the eyes of the Matriarch.',"Matriarch'ın gözleri adına.")
        self.check('The Rat Matriarch.', 'Sıçan Ana.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            self.check('By the eyes of the Matriarch.','Ana Matriğin gözleri adına.')

    def test_greenfinger_is_not_a_literal_green_finger(self):
        self.check('Your greenfingers are skilled.',"Greenfinger'larınız yetenekli.")
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            self.check('Your greenfingers are skilled.','Yeşil parmaklarınız yetenekli.')

    def test_lore_names_remain_present_when_inflected(self):
        for name in ('Conshak','Tenshae','Juux','Tenebhrae','Diathim','Sith'):
            with self.subTest(name=name):
                self.check('We know '+name+'.',name+"'yi biliyoruz.")
                with self.assertRaisesRegex(ValueError,'LOCKED'):
                    self.check('We know '+name+'.','Biliyoruz.')

    def test_izku_source_typo_uses_verified_species_title(self):
        self.check('Ikzu. A friend.','Izku. Dost.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            self.check('Ikzu. A friend.','Ikzu. Dost.')

    def test_veil_legacy_cover_exception_is_bound_to_exact_content(self):
        self.check('The Veil beyond.','Ötedeki Perde.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            self.check('The Veil beyond.','Ötedeki Peçe.')
        row=next(x for x in self.policy['context_exceptions'] if x['asset']=='tiles/materials/aenwood/aenfence.material')
        self.terms.validate(row)
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            self.terms.validate(dict(row,tr='Peçe ne işe yarıyor?'))

    def test_root_pop_inflections_and_named_flower_drink_exception(self):
        self.check('Which root pop?','Hangi kök gazozunu?')
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            self.check('Which root pop?','Hangi kök birasını?')
        row=next(x for x in self.policy['context_exceptions'] if x['asset']=='objects/themed/fastfood/sodafountain/sodafountain.object')
        self.terms.validate(row)
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            self.terms.validate(dict(row,tr='Karahindiba gazozu yok.'))

    def test_source_vow_does_not_lock_generic_source(self):
        self.check('By the Source.','Kaynak adına.')
        self.check('Find the source.','Kökenini bul.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            self.check('By the Source.','Köken adına.')

    def test_lightdweller_supports_turkish_capital_and_lowercase_inflections(self):
        self.check('You are a Lightdweller.', 'Sen Işıkta Yaşayanlardansın.')
        self.check('You are a Lightdweller.', 'Sen ışıkta yaşayanlardansın.')
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            self.check('You are a Lightdweller.', 'Sen güneşte yaşayanlardansın.')


if __name__=='__main__':
    unittest.main()
