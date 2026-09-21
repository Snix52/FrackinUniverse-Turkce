import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import publish_generated as pub


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / 'remote.git'
        subprocess.run(['git', 'init', '--bare', '--initial-branch=main', str(self.remote)], check=True, capture_output=True)
        self.repo = self.root / 'build'
        subprocess.run(['git', 'clone', str(self.remote), str(self.repo)], check=True, capture_output=True)
        self.identify(self.repo)
        (self.repo / 'source.txt').write_text('base')
        pub.git(self.repo, 'add', '.')
        pub.git(self.repo, 'commit', '-m', 'base')
        pub.git(self.repo, 'push', 'origin', 'main')
        self.sha = pub.git(self.repo, 'rev-parse', 'HEAD').stdout.strip()
        self.other = self.root / 'other'
        subprocess.run(['git', 'clone', str(self.remote), str(self.other)], check=True, capture_output=True)
        self.identify(self.other)
        (self.repo / 'dist').mkdir()
        (self.repo / 'dist/package.txt').write_text('generated')

    def identify(self, repo):
        pub.git(repo, 'config', 'user.name', 'Regression Test')
        pub.git(repo, 'config', 'user.email', 'tests@users.noreply.github.com')

    def advance(self):
        (self.other / 'source.txt').write_text('newer source')
        pub.git(self.other, 'add', '.')
        pub.git(self.other, 'commit', '-m', 'newer')
        pub.git(self.other, 'push', 'origin', 'main')
        return pub.git(self.other, 'rev-parse', 'HEAD').stdout.strip()

    def test_current_build_publishes_despite_generated_head_change(self):
        self.assertEqual(pub.publish(self.repo, self.sha), 'PUBLISHED')
        head = pub.remote_head(self.repo, 'origin', 'main')
        self.assertNotEqual(head, self.sha)
        self.assertEqual(pub.git(self.repo, 'rev-parse', head + '^').stdout.strip(), self.sha)
        self.assertIn('[skip ci]', pub.git(self.repo, 'log', '-1', '--format=%B').stdout)

    def test_already_stale_build_skips_without_commit(self):
        newer = self.advance()
        self.assertEqual(pub.publish(self.repo, self.sha), 'SKIP_STALE')
        self.assertEqual(pub.git(self.repo, 'rev-parse', 'HEAD').stdout.strip(), self.sha)
        self.assertEqual(pub.remote_head(self.repo, 'origin', 'main'), newer)

    def test_main_advances_after_generated_commit(self):
        original = pub.git
        def hook(repo, *args, **kwargs):
            result = original(repo, *args, **kwargs)
            if args and args[0] == 'commit' and repo == self.repo:
                self.advance()
            return result
        with patch.object(pub, 'git', side_effect=hook):
            self.assertEqual(pub.publish(self.repo, self.sha), 'SKIP_STALE_BEFORE_PUSH')

    def test_race_during_push_does_not_overwrite_newer_source(self):
        original = pub.git
        def hook(repo, *args, **kwargs):
            if args and args[0] == 'push' and repo == self.repo:
                self.advance()
            return original(repo, *args, **kwargs)
        with patch.object(pub, 'git', side_effect=hook):
            self.assertEqual(pub.publish(self.repo, self.sha), 'SKIP_STALE_DURING_PUSH')
        self.assertEqual(pub.remote_head(self.repo, 'origin', 'main'), pub.git(self.other, 'rev-parse', 'HEAD').stdout.strip())

    def test_non_race_push_failure_stays_failure(self):
        original = pub.git
        def hook(repo, *args, **kwargs):
            if args and args[0] == 'push' and repo == self.repo:
                return subprocess.CompletedProcess(args, 1, '', 'permission denied')
            return original(repo, *args, **kwargs)
        with patch.object(pub, 'git', side_effect=hook), self.assertRaisesRegex(RuntimeError, 'without a newer'):
            pub.publish(self.repo, self.sha)

    def test_unrelated_staged_changes_rejected(self):
        (self.repo / 'source.txt').write_text('unexpected')
        pub.git(self.repo, 'add', 'source.txt')
        with self.assertRaises(ValueError):
            pub.publish(self.repo, self.sha)

    def test_no_changes_skips(self):
        (self.repo / 'dist/package.txt').unlink()
        self.assertEqual(pub.publish(self.repo, self.sha), 'SKIP_UNCHANGED')


if __name__ == '__main__':
    unittest.main()
