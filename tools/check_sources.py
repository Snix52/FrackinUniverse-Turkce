#!/usr/bin/env python3
"""Run every maintained source gate against the same pinned FU checkout."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from write_build_evidence import verify_source

TOOLS = Path(__file__).resolve().parent
FIRST_GATE = 45
EXTRA_GATES = ('check_ui_lqa_20260925.py', 'check_ship_sail_dialog_20260926.py')


def gate_paths(tools: Path = TOOLS) -> list[Path]:
    version = json.loads((tools / 'ceviriler.json').read_text(encoding='utf-8'))['translation_version']
    major, minor, _ = map(int, version.split('-', 1)[0].split('.'))
    if major != 0 or minor < FIRST_GATE:
        raise ValueError('Source gate policy must be updated for catalog version ' + version)
    gates = []
    for release in range(FIRST_GATE, minor + 1):
        manifest = tools / f'v{release:03d}_translations.json'
        script = tools / f'generate_v{release:03d}.py'
        if not manifest.is_file() or not script.is_file():
            raise ValueError(f'Missing source manifest or gate for v0.{release}: {manifest.name}, {script.name}')
        gates.append(script)
    for name in EXTRA_GATES:
        script = tools / name
        if not script.is_file():
            raise ValueError('Missing source gate: ' + name)
        gates.append(script)
    return gates


def run_gates(source: Path, gates: list[Path]) -> None:
    for script in gates:
        print('Checking ' + script.name, flush=True)
        subprocess.run([sys.executable, '-X', 'utf8', str(script), '--source', str(source)], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    gates = gate_paths()
    source = args.source.resolve()
    verify_source(source)
    run_gates(source, gates)
    print(f'All {len(gates)} pinned source gates PASS')


if __name__ == '__main__':
    main()
