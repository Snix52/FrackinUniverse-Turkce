#!/usr/bin/env python3
"""Guard every pinned FU ship S.A.I.L. wake-up/reboot line against gaps."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from audit_remaining import parse_jsonc
from write_build_evidence import verify_source

TOOLS = Path(__file__).resolve().parent
MANIFEST = TOOLS / 'v0652_translations.json'
CATALOG = TOOLS / 'ceviriler.json'
PIN = 'bb58383c0d16c1152e3439e606b39ff82288b586'
STATIONS = {'slimepersontechstation', 'shadowtechstation'}


def source_dialogues(source: Path) -> dict[tuple[str, str], str]:
    result = {}
    ship = source / 'objects/ship'
    for path in sorted(ship.rglob('*.object')):
        if 'techstation' not in path.name.lower():
            continue
        asset = path.relative_to(source).as_posix()
        data = parse_jsonc(path.read_text(encoding='utf-8-sig'))
        for category in ('wakeUp', 'wakePlayer'):
            for index, pair in enumerate(data.get('dialog', {}).get(category, [])):
                if not isinstance(pair, list) or not pair or not isinstance(pair[0], str):
                    raise ValueError(f'Invalid S.A.I.L. dialogue source: {asset} {category}/{index}')
                key = asset, f'/dialog/{category}/{index}/0'
                if key in result:
                    raise ValueError(f'Duplicate S.A.I.L. dialogue source: {key}')
                result[key] = pair[0]
    return result


def verify_coverage(source_rows: dict[tuple[str, str], str], catalog_rows: list[dict],
                    expected_total: int | None = None) -> None:
    catalog = {(r['asset'], r['pointer']): r for r in catalog_rows}
    if len(catalog) != len(catalog_rows):
        raise ValueError('Duplicate catalog source pointer')
    if expected_total is not None and len(source_rows) != expected_total:
        raise ValueError(f'Pinned ship S.A.I.L. inventory drift: {len(source_rows)}')
    missing = set(source_rows) - set(catalog)
    if missing:
        raise ValueError(f'Untranslated ship S.A.I.L. dialogue: {sorted(missing)[:3]}')
    for key, source_text in source_rows.items():
        row = catalog[key]
        if row['en'] != source_text or not row.get('tr') or row['tr'] == source_text:
            raise ValueError(f'Ship S.A.I.L. source/translation drift: {key}')


def check(source: Path) -> dict[str, int]:
    verify_source(source)
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    if manifest['source_commit'] != PIN or manifest['source_commit'] != json.loads(
            (TOOLS / 'kaynaklar.json').read_text(encoding='utf-8'))['commit']:
        raise ValueError('Ship dialogue source pin differs')
    if manifest['translation_version'] != '0.65.2-beta':
        raise ValueError('Ship dialogue manifest version drift')
    version = tuple(int(part) for part in catalog['translation_version'].split('-', 1)[0].split('.'))
    if version < (0, 65, 2):
        raise ValueError('Catalog version behind v0.65.2')
    source_rows = source_dialogues(source)
    verify_coverage(source_rows, catalog['translations'], expected_total=205)
    new_rows = manifest['translations']
    new_index = {(r['asset'], r['pointer']): r for r in new_rows}
    if len(new_rows) != 23 or len(new_index) != 23:
        raise ValueError('Ship dialogue manifest inventory drift')
    expected_new = {key for key in source_rows if key[0].split('/')[2] in STATIONS}
    if set(new_index) != expected_new:
        raise ValueError(f'Slimeperson/Shadow dialogue coverage drift: {sorted(expected_new ^ set(new_index))[:3]}')
    catalog_index = {(r['asset'], r['pointer']): r for r in catalog['translations']}
    for key, row in new_index.items():
        if catalog_index[key] != row or row['en'] != source_rows[key]:
            raise ValueError(f'Ship dialogue manifest/catalog/source mismatch: {key}')
        if 'Fragment' in row['en'] and 'Fragment' not in row['tr']:
            raise ValueError(f'Shadow Fragment title changed: {key}')
    return {'ship_stations': len({asset for asset, _ in source_rows}),
            'all_dialogue_fields': len(source_rows),
            'new_dialogue_fields': len(new_rows)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    print('Ship S.A.I.L. source gate PASS:', json.dumps(check(args.source.resolve()), ensure_ascii=False))
