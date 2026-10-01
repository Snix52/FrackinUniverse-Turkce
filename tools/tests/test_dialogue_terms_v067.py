"""Reject reviewed dialogue regressions while accepting Turkish inflections."""
import json
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from qa_integrity import Terminology


class DialogueTermTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terms = Terminology(json.loads((TOOLS / 'locked_terms.json').read_text(encoding='utf-8')))

    def check(self, en, tr):
        self.terms.validate(dict(asset='dialog/catconverse.config', pointer='/converse/default/0', en=en, tr=tr))

    def test_clowder_does_not_acquire_a_purring_meaning(self):
        self.check('We call it a clowder.', 'Ona kedi topluluğu deriz.')
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.check('We call it a clowder.', 'Ona mırıltı kümesi deriz.')

    def test_opposable_thumbs_are_not_mutual_thumbs(self):
        self.check('I wish I had opposable thumbs.', 'Keşke kavrayıcı başparmaklarım olsaydı.')
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.check('I wish I had opposable thumbs.', 'Keşke karşılıklı başparmaklarım olsaydı.')

    def test_elysian_plural_is_not_imported_then_pluralized_again(self):
        self.check("I can't stand Elysians.", 'Elysianların hiçbirine tahammül edemiyorum.')
        with self.assertRaisesRegex(ValueError, 'İngilizce çoğul'):
            self.check("I can't stand Elysians.", 'Elysians’ların hiçbirine tahammül edemiyorum.')

    def test_names_and_translated_terms_accept_inflected_forms(self):
        self.check("Big Ape and X'i are watching.", "Big Ape’ten ve X'i’den söz ediliyor.")
        self.check('Stargazers live in an arcology.', 'Yıldız Gözlemcilerinin arkolojisindeyiz.')
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.check('Big Ape is watching.', 'Büyük Maymun seni izliyor.')


if __name__ == '__main__':
    unittest.main()
