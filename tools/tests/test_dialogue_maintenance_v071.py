"""A re-reviewed old line must not regain its original mistranslation."""
import copy,sys,unittest
from pathlib import Path
TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from plan_translation import read
import generate_v069,generate_v070

class DialogueMaintenanceV071Tests(unittest.TestCase):
    def test_old_sky_lines_are_reapproved_and_original_error_is_rejected(self):
        catalog=read(TOOLS/'ceviriler.json')
        for version,gate,report_name in [('069',generate_v069,'dialogue3-20261001.json'),('070',generate_v070,'dialogue4-20261001.json')]:
            with self.subTest(version=version):
                manifest=read(TOOLS/f'v{version}_translations.json')
                report=read(TOOLS.parent/'docs/reviews'/report_name)
                revision=report['subsequent_reviews'][-1]
                self.assertEqual(revision['release'],'0.71.0-beta')
                self.assertNotEqual(revision['previous_approval']['approved_rows_sha256'],report['approved_rows_sha256'])
                gate.validate_manifest(manifest,catalog,report)
                changed=copy.deepcopy(manifest)
                row=next(r for r in changed['translations'] if r['en'].startswith('Is that a rocket'))
                self.assertIn('Cebindeki',row['tr'])
                row['tr']='Gökyüzündeki roket senin mi, yoksa beni gördüğüne mi sevindin?'
                with self.assertRaisesRegex(ValueError,'approved translation'):gate.validate_manifest(changed,catalog,report)

if __name__=='__main__':unittest.main()
