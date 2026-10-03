"""Protect the reviewed final dialogue tranche and narrow sound/text exceptions."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import build_validate as build
import generate_v072 as gate
from plan_translation import read, preserved_name
from qa_integrity import Terminology, validate_format


class V072Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read(TOOLS / 'v072_translations.json')
        cls.catalog = read(TOOLS / 'ceviriler.json')
        cls.review = read(TOOLS.parent / 'docs/reviews/dialogue6-20261003.json')
        cls.policy = read(TOOLS / 'locked_terms.json')
        cls.format_policy = read(TOOLS / 'rules/text_integrity.json')

    def test_translation_change_cannot_reuse_approval(self):
        gate.validate_manifest(self.manifest, self.catalog, self.review)
        changed = copy.deepcopy(self.manifest)
        changed['translations'][0]['tr'] = 'İncelenmemiş değişiklik'
        with self.assertRaisesRegex(ValueError, 'approved translation'):
            gate.validate_manifest(changed, self.catalog, self.review)

    def test_direct_sources_cannot_acquire_unreviewed_provenance(self):
        changed = copy.deepcopy(self.manifest)
        row = next(r for r in changed['translations'] if 'qa' not in r)
        row['qa'] = dict(layered_source=True, source_patch=row['asset'] + '.patch')
        with self.assertRaisesRegex(ValueError, 'provenance'):
            gate.validate_manifest(changed, self.catalog, self.review)

    def test_allowlist_keeps_neighboring_game_fields_closed(self):
        for row in self.manifest['translations']:
            self.assertTrue(build.allowed(row['asset'], row['pointer']))
        self.assertFalse(build.allowed('dialog/greg.config', '/scriptDelta'))
        self.assertFalse(build.allowed('dialog/greg.config', '/converse/default/default/99999'))

    def test_direct_source_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            asset = source / 'dialog.config'
            asset.write_text(json.dumps({'converse': ['Original']}), encoding='utf-8')
            row = dict(asset='dialog.config', pointer='/converse/0', en='Original')
            gate.validate_source([row], source)
            asset.write_text(json.dumps({'converse': ['Different']}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'pinned source'):
                gate.validate_source([row], source)

    def greg_unit(self):
        row = next(r for r in self.manifest['translations'] if r['asset']=='dialog/greg.config' and r['en']=='Greg.')
        return dict(en=row['en'], tr=row['tr'], occurrences=[dict(asset=row['asset'], pointer=row['pointer'])])

    def test_only_bound_greg_sound_can_stay_unchanged(self):
        unit = self.greg_unit()
        self.assertTrue(preserved_name(unit))
        for key,value in [('asset','dialog/slimenpchuman.config'), ('pointer','/converse/default/default/99999')]:
            changed = copy.deepcopy(unit)
            changed['occurrences'][0][key] = value
            self.assertFalse(preserved_name(changed))
        changed = copy.deepcopy(unit)
        changed['en'] = changed['tr'] = 'Greg says ordinary English.'
        self.assertFalse(preserved_name(changed))

    def test_sound_binding_requires_active_lock_and_reason(self):
        unit = self.greg_unit()
        for mutation in ('lock','reason','text'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                policy = copy.deepcopy(self.policy)
                if mutation=='lock':
                    next(t for t in policy['terms'] if t['source']=='Greg')['status']='REVIEW'
                else:
                    binding = next(x for x in policy['context_exceptions'] if x.get('preserve_utterance') and x['asset']==unit['occurrences'][0]['asset'] and x['pointer']==unit['occurrences'][0]['pointer'])
                    binding['reason' if mutation=='reason' else 'en'] = ''
                tools = Path(directory)
                (tools/'locked_terms.json').write_text(json.dumps(policy), encoding='utf-8')
                self.assertFalse(preserved_name(unit, tools))

    def test_visible_gibberish_exception_does_not_open_placeholders(self):
        row = next(r for r in self.manifest['translations'] if r['asset']=='dialog/macready.config')
        validate_format(row, self.format_policy)
        for key,value in [('pointer','/converse/default/default/99999'), ('en','<playerName>')]:
            changed = dict(row, **{key:value})
            with self.assertRaisesRegex(ValueError, 'Control token'):
                validate_format(changed, self.format_policy)
        changed = copy.deepcopy(self.manifest)
        next(r for r in changed['translations'] if r['asset']=='dialog/macready.config').pop('qa')
        with self.assertRaisesRegex(ValueError, 'provenance'):
            gate.validate_manifest(changed, self.catalog, self.review)

    def test_hiccup_and_parent_drink_cannot_regress(self):
        terms = Terminology(self.policy)
        row = dict(asset='dialog/towndrunk.config',pointer='/converse/default/default/0',en='*HIC*',tr='*hık*')
        terms.validate(row)
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            terms.validate(dict(row,tr='*HÖÖRT*'))
        terms.validate(dict(row,en='Drink mummy juice.',tr='Anne şarabına aban.'))
        with self.assertRaisesRegex(ValueError,'LOCKED'):
            terms.validate(dict(row,en='Drink mummy juice.',tr='Ana sütünü iç.'))
        terms.validate(dict(row,en='Drink milk.',tr='Süt iç.'))


if __name__ == '__main__':
    unittest.main()
