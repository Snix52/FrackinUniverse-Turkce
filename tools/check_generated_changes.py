"""Reject direct edits to derived output before a main build can overwrite them.

PRs carry source only. The trusted main publisher writes derived outputs in a
separate [skip ci] commit. A manual rebuild introduces no incoming diff.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

EXACT={'tools/test_raporu.json','tools/GELISTIRME.txt'}


def generated(path: str) -> bool:
    return path in EXACT or path.startswith(('FU_Turkce/','dist/'))


def validate_paths(paths: list[str]) -> None:
    forbidden=[p for p in paths if generated(p)]
    if forbidden:
        raise ValueError('Edit sources, not generated output: '+', '.join(forbidden))


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--base')
    parser.add_argument('--head',default=os.environ.get('GITHUB_SHA','HEAD'))
    args=parser.parse_args()
    base=args.base
    if not base:
        event_path=os.environ.get('GITHUB_EVENT_PATH')
        if not event_path:
            parser.error('--base or GITHUB_EVENT_PATH is required')
        event=json.loads(Path(event_path).read_text())
        if os.environ.get('GITHUB_EVENT_NAME')=='workflow_dispatch':
            print('Explicit rebuild; no incoming change set.')
            return 0
        base=event.get('pull_request',{}).get('base',{}).get('sha') or event.get('before')
    if not base or base=='0'*40 or not re.fullmatch(r'[0-9a-f]{40}',base):
        raise ValueError('A valid comparison base is required')
    names=subprocess.run(['git','diff','--name-only','-z',base,args.head,'--'],check=True,capture_output=True).stdout
    validate_paths([p.decode('utf-8') for p in names.split(b'\0') if p])
    print('Generated-output edit guard: PASS')
    return 0

if __name__=='__main__':raise SystemExit(main())
