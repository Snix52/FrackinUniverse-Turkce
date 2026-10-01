"""Exact-source gate for the approved P1 dialogue v0.67 tranche."""
from __future__ import annotations

import argparse
from pathlib import Path

import build_validate as build
from plan_translation import digest, read
from write_build_evidence import verify_source

TOOLS = Path(__file__).resolve().parent
APPROVED_ROWS_SHA256 = '6859d8e118200e3ac824b29dd98d3cdf6b4bad6913a430ae2790130649c4eaec'


def validate_manifest(manifest, catalog, review):
    rows = manifest['translations']
    keys = {(r['asset'], r['pointer']) for r in rows}
    if (manifest['translation_version'] != '0.67.0-beta' or len(rows) != 376
            or len(keys) != 376 or len({r['asset'] for r in rows}) != 3):
        raise ValueError('v0.67 scope/count drift')
    core = sorted([{k: r[k] for k in ('asset', 'pointer', 'en', 'tr')} for r in rows],
                  key=lambda r: (r['asset'], r['pointer']))
    if digest(core) != APPROVED_ROWS_SHA256:
        raise ValueError('v0.67 approved translation membership/content drift')
    if (review['status'] != 'APPROVED_LANGUAGE_AND_SOURCE_PREFLIGHT'
            or manifest['approved_packet_sha256'] != review['approved_packet_sha256']
            or review['approved_rows_sha256'] != APPROVED_ROWS_SHA256):
        raise ValueError('v0.67 language approval mismatch')
    version = tuple(map(int, catalog['translation_version'].split('-')[0].split('.')))
    if version < (0, 67, 0):
        raise ValueError('Catalog version behind v0.67')
    index = {(r['asset'], r['pointer']): r for r in catalog['translations']}
    for row in rows:
        key = (row['asset'], row['pointer'])
        expected_qa = ({'layered_source': True, 'source_patch': row['asset'] + '.patch'}
                       if row['asset'] == 'dialog/converse.config' else None)
        if row.get('qa') != expected_qa:
            raise ValueError('v0.67 source provenance mismatch: ' + repr(key))
        current = index.get(key)
        if not current or any(current.get(k) != row.get(k) for k in ('en', 'tr', 'qa')):
            raise ValueError('v0.67 catalog mismatch: ' + repr(key))


def validate_source(rows, source):
    cache, assets = {}, {}
    for row in rows:
        if row.get('qa', {}).get('layered_source'):
            build.verify_layered_row(row, source, cache)
            continue
        asset = row['asset']
        if asset not in assets:
            assets[asset] = build.parse_jsonc((source / asset).read_bytes().decode('utf-8-sig'))
        if build.read_at(assets[asset], row['pointer']) != row['en']:
            raise ValueError('v0.67 pinned source mismatch: ' + asset + row['pointer'])
        touched, value = build.source_patch_value(asset, row['pointer'], source, cache)
        if touched and value != row['en']:
            raise ValueError('v0.67 unreviewed FU overlay: ' + asset + row['pointer'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    verify_source(args.source.resolve())
    manifest = read(TOOLS / 'v067_translations.json')
    pin = read(TOOLS / 'kaynaklar.json')
    if (manifest['source_commit'] != pin['commit']
            or manifest['source_repository'] != pin['repository']
            or manifest['source_declared_version'] != pin['declared_version']):
        raise ValueError('v0.67 manifest source pin drift')
    validate_manifest(manifest, read(TOOLS / 'ceviriler.json'),
                      read(TOOLS.parent / 'docs/reviews/dialogue-20261001.json'))
    validate_source(manifest['translations'], args.source)
    print('v0.67 source gate PASS: 376 fields / 3 assets / 307 unique source strings / 220 FU-layered fields')


if __name__ == '__main__':
    main()
