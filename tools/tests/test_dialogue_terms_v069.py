"""Preserve reviewed names and distinguish Pyreite from the real mineral pyrite."""
import json
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from qa_integrity import Terminology


class DialogueTermsV069Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terms = Terminology(json.loads((TOOLS / 'locked_terms.json').read_text(encoding='utf-8')))

    def test_new_names_keep_their_stems_when_inflected(self):
        for name in ('Barbatus', 'CySol', 'Zaibatsu', 'Pyreite'):
            with self.subTest(name=name):
                row = dict(asset='dialog/converse.config', pointer='/converse/human/default/0',
                           en='I heard of ' + name + '.', tr=name + "'ın adını duydum.")
                self.terms.validate(row)
                row['tr'] = 'Adını duydum.'
                with self.assertRaisesRegex(ValueError, 'LOCKED'):
                    self.terms.validate(row)

    def test_pyreite_is_not_pyrite(self):
        row = dict(asset='dialog/converse.config', pointer='/converse/human/radien/0',
                   en='I like pyreite curry.', tr='Pyreite Körisini severim.')
        self.terms.validate(row)
        row['tr'] = 'Pirit körisini severim.'
        with self.assertRaisesRegex(ValueError, 'LOCKED'):
            self.terms.validate(row)
        self.terms.validate(dict(row, en='Pyrite is a mineral.', tr='Pirit bir mineraldir.'))


if __name__ == '__main__':
    unittest.main()
