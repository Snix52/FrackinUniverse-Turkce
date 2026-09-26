import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_ship_sail_dialog_20260926 import verify_coverage


class ShipSailCoverageTests(unittest.TestCase):
    def test_untranslated_or_changed_source_dialogue_fails(self):
        a = ('objects/ship/slimepersontechstation/slimepersontechstation.object', '/dialog/wakeUp/0/0')
        b = ('objects/ship/shadowtechstation/shadowtechstation.object', '/dialog/wakePlayer/0/0')
        source = {a: "I'm alive!", b: 'Fragment should interface with the system.'}
        translated = [{'asset': a[0], 'pointer': a[1], 'en': source[a], 'tr': 'Yaşıyorum!'}]
        with self.assertRaisesRegex(ValueError, 'Untranslated ship'):
            verify_coverage(source, translated, expected_total=2)
        translated.append({'asset': b[0], 'pointer': b[1], 'en': source[b],
                           'tr': 'Fragment sistemle bağlantı kurmalı.'})
        verify_coverage(source, translated, expected_total=2)
        source[b] = 'Changed upstream dialogue.'
        with self.assertRaisesRegex(ValueError, 'source/translation drift'):
            verify_coverage(source, translated, expected_total=2)
