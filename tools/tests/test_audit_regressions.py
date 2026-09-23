"""Regression cases reproduced during the full repository audit."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import audit_remaining as audit
import build_validate as build
import qa_integrity as qa


class ManifestBindingTests(unittest.TestCase):
    def test_all_row_manifest_schemas_bind_both_languages_and_keys(self):
        row = dict(asset='fixture.item', pointer='/description', en='Hello', tr='Merhaba')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file = root/'v999_translations.json'
            for as_list in (True, False):
                for mutation in ({'en': 'Changed source'}, {'tr': 'Başka çeviri'},
                                 {'pointer': '/title'}, {'asset': 'missing.item'}):
                    with self.subTest(as_list=as_list, mutation=mutation):
                        rows = [dict(row, **mutation)]
                        file.write_text(json.dumps(rows if as_list else {'translations': rows}), encoding='utf-8')
                        with self.assertRaises(ValueError):
                            qa.manifest_rows([row], root)
                file.write_text(json.dumps([row] if as_list else {'translations': [row]}), encoding='utf-8')
                self.assertEqual(len(qa.manifest_rows([row], root)), 2)

    def test_duplicates_fail_in_catalog_and_manifest(self):
        row = dict(asset='fixture.item', pointer='/description', en='Hello', tr='Merhaba')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                qa.manifest_rows([row, row], root)
            (root/'v999_translations.json').write_text(json.dumps([row,row]), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                qa.manifest_rows([row], root)


class LayeredSourceTests(unittest.TestCase):
    def verify(self, ops, pointer='/description', en='Displayed', asset='fixture.item'):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root/(asset+'.patch')
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(json.dumps(ops), encoding='utf-8')
            row = dict(asset=asset, pointer=pointer, en=en,
                       qa={'layered_source': True, 'source_patch': asset+'.patch'})
            build.verify_layered_row(row, root, {})

    def test_test_operations_are_not_source_values(self):
        with self.assertRaisesRegex(ValueError, 'Layered source mismatch'):
            self.verify([dict(op='test',path='/description',value='Displayed')])

    def test_direct_nested_and_later_overwrites(self):
        self.verify([dict(op='add',path='/pane',value={'title':'Displayed'})], '/pane/title')
        self.verify([dict(op='replace',path='/description',value='Displayed')])
        for op in (dict(op='replace',path='/pane',value={}),dict(op='remove',path='/pane')):
            with self.subTest(op=op), self.assertRaisesRegex(ValueError, 'Layered source mismatch'):
                self.verify([dict(op='add',path='/pane',value={'title':'Displayed'}),op], '/pane/title')

    def test_pinned_array_append_uses_documented_index(self):
        asset='objects/crafting/upgradeablecraftingobjects/craftingwheel/craftingwheel.object'
        self.verify([dict(op='add',path='/upgradeStages/-',value={'itemSpawnParameters':{'description':'Displayed'}})],
                    '/upgradeStages/2/itemSpawnParameters/description',asset=asset)

    def test_wrong_source_text_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Layered source mismatch'):
            self.verify([dict(op='replace',path='/description',value='Different')])


class ScopeAuditTests(unittest.TestCase):
    def test_patch_test_values_do_not_become_translation_debt(self):
        rows=list(audit.candidates_from_data('fixture.item.patch',[
            dict(op='test',path='/description',value='Old source'),
            dict(op='replace',path='/description',value='Displayed source')]))
        self.assertEqual([r.value for r in rows], ['Displayed source'])

    def test_lua_uses_real_literals_instead_of_display_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            manifest=root/'raw.json'
            manifest.write_text(json.dumps({'assets':[{'asset':'visible.lua','replacements':[{
                'old':'widget.setText("label", "^red;Çağrı^reset;")',
                'new':'widget.setText("label", "^red;Oyuncu^reset;")',
                'display_en':'Misleading metadata','text_literals':[1],'expected_count':1}]}]}),encoding='utf-8')
            (root/'visible.lua').write_text('widget.setText("label", "^red;Çağrı^reset;")\n'
                                            'widget.setText("label", "İşlem hazır")\n',encoding='utf-8')
            result=audit.audit_lua(root,manifest)
            self.assertEqual(result['detected_remaining_literals'],1)
            self.assertEqual(result['samples'][0]['source'],'İşlem hazır')


if __name__=='__main__':
    unittest.main()
