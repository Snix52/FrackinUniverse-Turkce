import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import build_validate as build
import generate_v071 as gate
from plan_translation import read


class V071Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read(TOOLS / 'v071_translations.json')
        cls.catalog = read(TOOLS / 'ceviriler.json')
        cls.review = read(TOOLS.parent / 'docs/reviews/dialogue5-20261002.json')

    def test_changed_translation_cannot_reuse_language_approval(self):
        gate.validate_manifest(self.manifest, self.catalog, self.review)
        changed = copy.deepcopy(self.manifest)
        changed['translations'][0]['tr'] = 'Değiştirilen onaysız karşılık'
        with self.assertRaisesRegex(ValueError, 'approved translation'):
            gate.validate_manifest(changed, self.catalog, self.review)

    def test_patch_only_crew_and_fenerox_require_layered_provenance(self):
        for asset in ('dialog/crewmember.config','dialog/fenerox.config'):
            with self.subTest(asset=asset):
                changed=copy.deepcopy(self.manifest)
                row=next(r for r in changed['translations'] if r['asset']==asset)
                self.assertEqual(row['qa']['source_patch'],asset+'.patch')
                row.pop('qa')
                with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(changed,self.catalog,self.review)

    def test_field_allowlist_does_not_open_neighboring_game_parameters(self):
        for row in self.manifest['translations']:
            self.assertTrue(build.allowed(row['asset'], row['pointer']))
        self.assertFalse(build.allowed('dialog/brewmaster.config', '/scriptDelta'))
        self.assertFalse(build.allowed('dialog/converse.config', '/converse/apex/nightar/99999'))

    def test_source_change_is_rejected_for_direct_and_layered_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            direct = source / 'test.object'
            direct.write_text(json.dumps({'description': 'Correct source'}), encoding='utf-8')
            row = {'asset': 'test.object', 'pointer': '/description', 'en': 'Correct source'}
            gate.validate_source([row], source)
            direct.write_text(json.dumps({'description': 'Changed source'}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'pinned source'):
                gate.validate_source([row], source)
            patch = source / 'test.object.patch'
            patch.write_text(json.dumps([{'op': 'replace', 'path': '/description', 'value': 'Correct source'}]), encoding='utf-8')
            row['qa'] = {'layered_source': True, 'source_patch': 'test.object.patch'}
            gate.validate_source([row], source)
            patch.write_text(json.dumps([{'op': 'replace', 'path': '/description', 'value': 'Changed source'}]), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Layered source mismatch'):
                gate.validate_source([row], source)


if __name__ == '__main__':
    unittest.main()
