import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from check_sources import EXTRA_GATES, gate_paths, run_gates


class SourceGateTests(unittest.TestCase):
    def fixture(self, tools, minor=46):
        (tools / 'ceviriler.json').write_text(json.dumps({'translation_version': f'0.{minor}.0-beta'}))
        for release in range(45, minor + 1):
            (tools / f'generate_v{release:03d}.py').touch()
            (tools / f'v{release:03d}_translations.json').touch()
        for name in EXTRA_GATES:
            (tools / name).touch()

    def test_current_catalog_runs_every_release_and_both_extra_gates(self):
        names = [p.name for p in gate_paths()]
        self.assertEqual(names, [f'generate_v{release:03d}.py' for release in range(45, 71)] + list(EXTRA_GATES))
        self.assertFalse(any('legacy' in str(p) for p in gate_paths()))

    def test_missing_manifest_or_gate_is_rejected_before_running(self):
        for missing in ('generate_v046.py', 'v046_translations.json', EXTRA_GATES[0]):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as directory:
                tools = Path(directory)
                self.fixture(tools)
                (tools / missing).unlink()
                with self.assertRaises(ValueError):
                    gate_paths(tools)

    def test_new_catalog_release_requires_new_source_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            tools = Path(directory)
            self.fixture(tools)
            (tools / 'ceviriler.json').write_text(json.dumps({'translation_version': '0.47.0-beta'}))
            with self.assertRaisesRegex(ValueError, 'v0.47'):
                gate_paths(tools)
            (tools / 'generate_v047.py').touch()
            (tools / 'v047_translations.json').touch()
            self.assertIn(tools / 'generate_v047.py', gate_paths(tools))

    def test_unhandled_major_version_requires_policy_update(self):
        with tempfile.TemporaryDirectory() as directory:
            tools = Path(directory)
            self.fixture(tools)
            (tools / 'ceviriler.json').write_text(json.dumps({'translation_version': '1.0.0'}))
            with self.assertRaisesRegex(ValueError, 'policy'):
                gate_paths(tools)

    def test_failed_gate_stops_before_later_gates(self):
        gates = [TOOLS / f'generate_v{release:03d}.py' for release in range(45, 48)]
        failure = subprocess.CalledProcessError(1, 'second gate')
        with patch('check_sources.subprocess.run', side_effect=[None, failure]) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                run_gates(Path('FU source'), gates)
            self.assertEqual(run.call_count, 2)

    def test_source_path_is_a_single_argument_and_utf8_is_enabled(self):
        source = Path('çalışma klasörü/FU source')
        script = TOOLS / 'generate_v045.py'
        with patch('check_sources.subprocess.run') as run:
            run_gates(source, [script])
            run.assert_called_once_with([sys.executable, '-X', 'utf8', str(script), '--source', str(source)], check=True)

    def test_archived_generators_stop_without_changing_catalog_or_manifest(self):
        scripts = sorted((TOOLS / 'legacy').glob('*.py'))
        self.assertEqual(len(scripts), 25)
        before = {p.name: p.read_bytes() for p in TOOLS.glob('*.json')}
        for script in scripts:
            with self.subTest(script=script.name):
                result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=10)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Archived one-shot generator', result.stderr)
        self.assertEqual(before, {p.name: p.read_bytes() for p in TOOLS.glob('*.json')})


if __name__ == '__main__':
    unittest.main()
