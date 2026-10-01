"""Keep reviewed glyph terminology and boss identity without matching ruins."""
import json
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from qa_integrity import Terminology


class DialogueTermsV068Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terms = Terminology(json.loads((TOOLS / 'locked_terms.json').read_text(encoding='utf-8')))

    def check(self, en, tr):
        self.terms.validate(dict(asset='dialog/converse.config', pointer='/converse/avian/skath/0', en=en, tr=tr))

    def test_glyphs_do_not_become_runes(self):
        self.check('The glyphs of the Stargazers.', 'Yıldız Gözlemcilerinin glifleri.')
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.check('The glyphs of the Stargazers.', 'Yıldız Gözlemcilerinin rünleri.')

    def test_boss_identity_does_not_lock_generic_ruins(self):
        self.check('The Ruin, stronger.', 'Ruin, daha güçlü.')
        self.check('The ruins were abandoned.', 'Harabeler terk edilmişti.')
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.check('The Ruin, stronger.', 'Yıkım, daha güçlü.')

    def test_legacy_symbol_exception_is_bound_to_exact_content(self):
        row = dict(asset='objects/minibiome/elder/eldercarving1.object', pointer='/description',
                   en='I can only guess at the potential meaning of these glyphs.',
                   tr='Bu sembollerin ne anlama geldiğini ancak tahmin edebilirim.')
        self.terms.validate(row)
        row['tr'] = 'Bu rünlerin ne anlama geldiğini ancak tahmin edebilirim.'
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.terms.validate(row)


if __name__ == '__main__':
    unittest.main()
