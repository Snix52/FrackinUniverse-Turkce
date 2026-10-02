import copy,json,sys,tempfile,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
import build_validate as build
import check_science_outpost_radio_20261003 as gate
from plan_translation import read
from qa_integrity import Terminology

class OutpostRadioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=read(TOOLS/'v0711_translations.json')
        cls.catalog=read(TOOLS/'ceviriler.json')
        cls.review=read(TOOLS.parent/'docs/reviews/science-outpost-radio-20261003.json')
    def test_scalar_array_and_nested_stagehands_are_inventoried(self):
        def obj(params):return {'properties':[{'name':'stagehand','value':'radiomessage'},{'name':'parameters','value':json.dumps(params)}]}
        data={'layers':[{'objects':[obj({'radioMessage':'one'})],'layers':[{'objects':[obj({'radioMessages':['two','one']})]}]}]}
        self.assertEqual(gate.map_messages(data),{'one':2,'two':1})
        with self.assertRaisesRegex(ValueError,'Unresolved'):
            gate.map_messages({'layers':[{'objects':[obj({})]}]})
    def test_new_runtime_message_or_removed_translation_is_rejected(self):
        rows=self.manifest['translations'];ids={r['pointer'].split('/')[1] for r in rows}
        gate.verify_coverage(ids,rows)
        with self.assertRaisesRegex(ValueError,'coverage gap'):gate.verify_coverage(ids|{'new_outpost_room'},rows)
        with self.assertRaisesRegex(ValueError,'coverage gap'):gate.verify_coverage(ids,rows[:-1])
    def test_missing_catalog_row_and_unapproved_translation_are_rejected(self):
        gate.validate_manifest(self.manifest,self.catalog,self.review)
        changed=copy.deepcopy(self.catalog)
        key=self.manifest['translations'][0]
        changed['translations']=[r for r in changed['translations'] if (r['asset'],r['pointer'])!=(key['asset'],key['pointer'])]
        with self.assertRaisesRegex(ValueError,'catalog mismatch'):gate.validate_manifest(self.manifest,changed,self.review)
        manifest=copy.deepcopy(self.manifest);manifest['translations'][0]['tr']='İncelenmemiş değişiklik'
        with self.assertRaisesRegex(ValueError,'approved translation'):gate.validate_manifest(manifest,self.catalog,self.review)
    def test_layered_provenance_and_game_parameters_remain_guarded(self):
        changed=copy.deepcopy(self.manifest)
        row=next(r for r in changed['translations'] if r.get('qa'))
        row.pop('qa')
        with self.assertRaisesRegex(ValueError,'provenance'):gate.validate_manifest(changed,self.catalog,self.review)
        for row in self.manifest['translations']:
            self.assertTrue(build.allowed(row['asset'],row['pointer']))
            self.assertFalse(build.allowed(row['asset'],row['pointer'].replace('/text','/type')))
            self.assertFalse(build.allowed(row['asset'],row['pointer'].replace('/text','/portraitSpeed')))
    def test_direct_and_layered_source_changes_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)
            direct=source/'example.radiomessages';direct.write_text('{"one":{"text":"Source"}}')
            row={'asset':direct.name,'pointer':'/one/text','en':'Source'}
            gate.validate_source([row],source)
            direct.write_text('{"one":{"text":"Changed"}}')
            with self.assertRaisesRegex(ValueError,'source mismatch'):gate.validate_source([row],source)
            patch=source/'example.radiomessages.patch';patch.write_text('[{"op":"add","path":"/one","value":{"text":"Source"}}]')
            row['qa']={'layered_source':True,'source_patch':patch.name}
            gate.validate_source([row],source)
            patch.write_text('[{"op":"add","path":"/one","value":{"text":"Changed"}}]')
            with self.assertRaisesRegex(ValueError,'Layered source mismatch'):gate.validate_source([row],source)
    def test_reported_messages_and_locked_names_are_retained(self):
        ids={r['pointer'].split('/')[1] for r in self.manifest['translations']}
        self.assertTrue({'fu_useStarbucks','fu_useBathroom','fu_useBooze','fu_useDrugs1','fu_useDrugs2','fu_useBees'}<=ids)
        term=Terminology(read(TOOLS/'locked_terms.json'))
        for en,tr,bad in [('Instafreud','Insta-Freud','Anında Freud'),('Kevin','Kevin','Kemal'),('Starbucks','Starbucks','Yıldız Kahvesi'),('The Tavern','Meyhane','Han')]:
            row={'asset':'test','pointer':'/text','en':en,'tr':tr};term.validate(row)
            with self.assertRaises(ValueError):term.validate(dict(row,tr=bad))

if __name__=='__main__':unittest.main()
