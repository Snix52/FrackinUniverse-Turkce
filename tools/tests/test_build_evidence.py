import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import write_build_evidence as evidence


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tools = self.root / 'tools'
        self.tools.mkdir()
        self.mock = patch.object(evidence, 'TOOLS', self.tools)
        self.mock.start()
        self.addCleanup(self.mock.stop)
        self.sha = '1' * 40
        self.pin = '2' * 40
        self.source = {'commit': self.pin, 'repository': 'test/FU', 'declared_version': 'fixture'}
        evidence.write_json(self.tools / 'kaynaklar.json', self.source)
        evidence.write_json(self.tools / 'ceviriler.json', {'translation_version': 'fixture', 'translations': []})
        evidence.write_json(self.tools / 'raw_text_translations.json', {'assets': []})
        self.files = {'_metadata': b'{}', 'item.patch': json.dumps([
            {'op': 'test', 'path': '/name', 'value': 'Source'},
            {'op': 'replace', 'path': '/name', 'value': 'Kaynak'}]).encode()}
        self.mod, self.install = self.root / 'build/FU_Turkce', self.root / 'FU_Turkce'
        for directory in (self.mod, self.install):
            directory.mkdir(parents=True)
            for name, data in self.files.items():
                (directory / name).write_bytes(data)
        self.report = {'static_qa': 'PASS', 'source_commit': self.sha,
                       'source_inputs_dirty': False,
                       'build_inputs_sha256': evidence.build_inputs_digest(),
                       'source_validation': {'status': 'PASS', 'verified_commit': self.pin},
                       'catalog_sha256': hashlib.sha256((self.tools / 'ceviriler.json').read_bytes()).hexdigest(),
                       'install_tree_sha256': evidence.tree_digest(self.files),
                       'fields': 1, 'patch_assets': 1, 'raw_assets': 0, 'raw_strings': 0}
        self.report_path = self.root / 'validation.json'
        self.zip = self.root / 'mod.zip'
        evidence.deterministic_zip(self.zip, self.files)
        self.save_report()

    def save_report(self):
        evidence.write_json(self.report_path, self.report)

    def build(self):
        return evidence.build_evidence(self.zip, self.mod, self.install, self.report_path, self.sha, 'fixture')

    def test_actual_hash_size_counts_and_lqa(self):
        result = self.build()
        self.assertEqual(result['package']['bytes'], self.zip.stat().st_size)
        self.assertEqual(result['package']['sha256'], hashlib.sha256(self.zip.read_bytes()).hexdigest())
        self.assertEqual(result['localized_units']['structured_fields'], 1)
        self.assertEqual(result['in_game_lqa'], 'NOT TESTED')
        self.assertNotIn('generated_commit', result)

    def test_deterministic_zip(self):
        other = self.root / 'second.zip'
        evidence.deterministic_zip(other, dict(reversed(list(self.files.items()))))
        self.assertEqual(self.zip.read_bytes(), other.read_bytes())

    def test_stale_source_or_catalog_report_rejected(self):
        for change in ({'source_commit': '3' * 40}, {'catalog_sha256': 'old'},
                       {'source_commit': None}, {'source_inputs_dirty': True},
                       {'build_inputs_sha256': 'old'},
                       {'install_tree_sha256': 'old'}, {'fields': 2}, {'static_qa': 'NOT RUN'},
                       {'source_validation': {'status': 'NOT RUN'}},
                       {'source_validation': {'status': 'PASS', 'verified_commit': '4' * 40}}):
            with self.subTest(change=change):
                original = copy.deepcopy(self.report)
                self.report.update(change)
                self.save_report()
                with self.assertRaises(ValueError):
                    self.build()
                self.report = original
        self.save_report()

    def test_changed_rules_or_lua_cannot_reuse_old_build(self):
        for filename in ('qa_integrity.py', 'rules/policy.json', 'raw_overrides/test.lua'):
            with self.subTest(filename=filename):
                path = self.tools / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'changed after validation')
                with self.assertRaisesRegex(ValueError, 'build inputs mismatch'):
                    self.build()
                path.unlink()

    def test_custom_patch_and_png_are_accounted_for_and_source_bound(self):
        custom = self.tools / 'custom_assets'
        (custom / 'objects').mkdir(parents=True)
        (custom / 'player.config.patch').write_bytes(b'[[{"op":"add"}]]')
        (custom / 'objects/star.png').write_bytes(b'png bytes')
        evidence.write_json(self.tools / 'custom_assets.json',
                            {'assets': ['player.config.patch', 'objects/star.png']})
        self.files['player.config.patch'] = (custom / 'player.config.patch').read_bytes()
        self.files['objects/star.png'] = (custom / 'objects/star.png').read_bytes()
        for directory in (self.mod, self.install):
            (directory / 'player.config.patch').write_bytes(self.files['player.config.patch'])
            (directory / 'objects').mkdir()
            (directory / 'objects/star.png').write_bytes(self.files['objects/star.png'])
        self.report['custom_assets'] = 2
        self.report['assets'] = 3
        self.report['build_inputs_sha256'] = evidence.build_inputs_digest()
        self.report['install_tree_sha256'] = evidence.tree_digest(self.files)
        self.save_report()
        evidence.deterministic_zip(self.zip, self.files)
        self.assertEqual(self.build()['custom_game_assets'], 2)
        missing = dict(self.files)
        del missing['objects/star.png']
        evidence.deterministic_zip(self.zip, missing)
        with self.assertRaisesRegex(ValueError, 'Custom asset missing'):
            evidence.verify_package(self.zip, missing, self.report)
        (custom / 'objects/star.png').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'build inputs mismatch'):
            self.build()

    def test_root_mismatch_rejected(self):
        (self.install / 'item.patch').write_bytes(b'[]')
        with self.assertRaisesRegex(ValueError, 'Root/install-tree'):
            self.build()

    def test_zip_inventory_and_bytes_rejected(self):
        for files in ({**self.files, 'extra': b'extra'}, {**self.files, 'item.patch': b'[]'}):
            evidence.deterministic_zip(self.zip, files)
            with self.assertRaises(ValueError):
                self.build()

    def test_unguarded_patch_rejected(self):
        files = {**self.files, 'item.patch': b'[{"op":"replace","path":"/name","value":"unsafe"}]'}
        evidence.deterministic_zip(self.zip, files)
        with self.assertRaisesRegex(ValueError, 'pairing'):
            evidence.verify_package(self.zip, files, self.report)

    def test_flat_multi_field_patch_rejected(self):
        operations = [
            {'op': 'test', 'path': '/description', 'value': 'A'},
            {'op': 'test', 'path': '/shortdescription', 'value': 'B'},
            {'op': 'replace', 'path': '/description', 'value': 'C'},
            {'op': 'replace', 'path': '/shortdescription', 'value': 'D'},
        ]
        with self.assertRaisesRegex(ValueError, 'independent conditional batches'):
            evidence.verified_patch_fields('fixture.patch', operations)

    def test_corrupt_zip_rejected(self):
        self.zip.write_bytes(b'not a zip')
        with self.assertRaises(zipfile.BadZipFile):
            self.build()

    def test_refresh_replaces_stale_metadata(self):
        (self.tools / 'GELISTIRME.txt').write_text('old hash old timestamp')
        evidence.write_json(self.tools / 'test_raporu.json', {'old_commit': 'deadbeef'})
        result = self.build()
        evidence.refresh_tracked(result)
        actual = evidence.read_json(self.tools / 'test_raporu.json')
        self.assertNotIn('old_commit', actual)
        self.assertEqual(actual['package'], result['package'])
        self.assertNotIn('old hash', (self.tools / 'GELISTIRME.txt').read_text())
        self.assertEqual(actual['in_game_lqa'], 'NOT TESTED')

    def test_source_revision_and_dirty_tree_fail_closed(self):
        git_source = self.root / 'source'
        subprocess.run(['git', 'init', str(git_source)], check=True, capture_output=True)
        def git(*args):
            return subprocess.run(['git', '-C', str(git_source), *args], check=True,
                                  capture_output=True, text=True).stdout.strip()
        git('config', 'user.name', 'test')
        git('config', 'user.email', 'test@example.invalid')
        (git_source / 'asset').write_text('pinned')
        git('add', '.')
        git('commit', '-m', 'source fixture')
        with self.assertRaisesRegex(ValueError, 'not the pinned'):
            evidence.verify_source(git_source)
        self.source['commit'] = git('rev-parse', 'HEAD')
        evidence.write_json(self.tools / 'kaynaklar.json', self.source)
        self.assertEqual(evidence.verify_source(git_source)['status'], 'PASS')
        with self.assertRaisesRegex(ValueError, 'checkout root'):
            (git_source/'nested').mkdir()
            evidence.verify_source(git_source/'nested')
        for name in ('extra.item', '.hidden-source.item'):
            extra = git_source/name
            extra.write_text('untracked source')
            with self.assertRaisesRegex(ValueError, 'extra files'):
                evidence.verify_source(git_source)
            extra.unlink()
        (git_source/'.git/info/exclude').write_text('ignored.item\n')
        extra = git_source/'ignored.item'
        extra.write_text('ignored source')
        with self.assertRaisesRegex(ValueError, 'extra files'):
            evidence.verify_source(git_source)
        extra.unlink()
        (git_source / 'asset').write_text('modified')
        with self.assertRaisesRegex(ValueError, 'modifications'):
            evidence.verify_source(git_source)
        self.assertEqual(evidence.verify_source(None)['status'], 'NOT RUN')


if __name__ == '__main__':
    unittest.main()
