import fnmatch
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]


class WorkflowTests(unittest.TestCase):
    def test_audit_translation_paths_and_not_unrelated(self):
        text = (ROOT / '.github/workflows/audit-remaining.yml').read_text()
        block = text.split('    paths:', 1)[1].split('\nconcurrency:', 1)[0]
        paths = re.findall(r'- [\"\']([^\"\']+)[\"\']', block)
        for changed in ('tools/ceviriler.json', 'tools/raw_text_translations.json',
                        'tools/v030_translations.json', 'tools/v999_translations.json',
                        'tools/kaynaklar.json', 'tools/rule_data.py', 'tools/qa_raw.py'):
            self.assertTrue(any(fnmatch.fnmatchcase(changed, pattern) for pattern in paths), changed)
        for changed in ('README.md', 'dist/package.zip', 'FU_Turkce/thing.patch'):
            self.assertFalse(any(fnmatch.fnmatchcase(changed, pattern) for pattern in paths), changed)

    def test_build_source_and_regressions_preserved(self):
        text = (ROOT / '.github/workflows/build-package.yml').read_text()
        for part in ('cancel-in-progress: true', 'BUILD_SOURCE_SHA: ${{ github.sha }}',
                     'python -m unittest discover -s tools/tests -v', '--source-dir fu_source',
                     '--create-zip --refresh-tracked', 'publish_generated.py --source-sha',
                     'diff -qr build_output/FU_Turkce FU_Turkce'):
            self.assertIn(part, text)
        self.assertNotIn('git push', text)
        self.assertNotIn('git rebase', text)
        self.assertIn('python tools/generate_v049.py --source fu_source', text)
        pr_text = (ROOT / '.github/workflows/pr-qa.yml').read_text()
        self.assertIn('python tools/generate_v049.py --source fu_source', pr_text)


if __name__ == '__main__':
    unittest.main()
