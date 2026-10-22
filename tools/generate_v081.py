"""Exact-source gate for the approved P1 dialogue v0.81 tranche."""
from __future__ import annotations

import argparse
from pathlib import Path

import build_validate as build
from plan_translation import digest, read
from write_build_evidence import verify_source

TOOLS = Path(__file__).resolve().parent
APPROVED_ROWS_SHA256 = '890488e985a5bcd3cd49c2eabbe608456fc8207b25d32ba902397de1f0372c53'


def validate_manifest(manifest, catalog, review):
    rows = manifest['translations']
    keys = {(r['asset'], r['pointer']) for r in rows}
    if (manifest['translation_version'] != '0.81.0-beta' or len(rows) != 350
            or len(keys) != 350 or len({r['asset'] for r in rows}) != 7):
        raise ValueError('v0.81 scope/count drift')
    core = sorted([{k: r[k] for k in ('asset', 'pointer', 'en', 'tr')} for r in rows],
                  key=lambda r: (r['asset'], r['pointer']))
    if digest(core) != APPROVED_ROWS_SHA256:
        raise ValueError('v0.81 approved translation membership/content drift')
    if (review['status'] != 'APPROVED_LANGUAGE_AND_SOURCE_PREFLIGHT'
            or manifest['approved_packet_sha256'] != review['approved_packet_sha256']
            or review['approved_rows_sha256'] != APPROVED_ROWS_SHA256):
        raise ValueError('v0.81 language approval mismatch')
    version = tuple(map(int, catalog['translation_version'].split('-')[0].split('.')))
    if version < (0, 81, 0):
        raise ValueError('Catalog version behind v0.81')
    index = {(r['asset'], r['pointer']): r for r in catalog['translations']}
    for row in rows:
        key = (row['asset'], row['pointer'])
        exceptions = read(TOOLS / 'rules/text_integrity.json')['control_exceptions']
        bound = next((x for x in exceptions if all(x.get(k) == row[k] for k in ('asset','pointer','en','tr'))), None)
        expected_qa = {}
        if row['asset'] in {'radiomessages/intro.radiomessages', 'radiomessages/mech.radiomessages', 'radiomessages/missions.radiomessages'}:
            expected_qa.update(layered_source=True, source_patch=row['asset'] + '.patch')
        if bound:
            expected_qa.update(allow_control_fix=True, semantic_override=bound['reason'])
        source_fix = next((x for x in review['source_corrections'] if all(x.get(k) == row[k] for k in ('asset', 'pointer', 'en', 'tr'))), None)
        if source_fix:
            expected_qa.update(source_bug_fix=True, reason=source_fix['reason'])
        expected_qa = expected_qa or None
        if row.get('qa') != expected_qa:
            raise ValueError('v0.81 source provenance mismatch: ' + repr(key))
        current = index.get(key)
        if not current or any(current.get(k) != row.get(k) for k in ('en', 'tr', 'qa')):
            raise ValueError('v0.81 catalog mismatch: ' + repr(key))


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
            raise ValueError('v0.81 pinned source mismatch: ' + asset + row['pointer'])
        touched, value = build.source_patch_value(asset, row['pointer'], source, cache)
        if touched and value != row['en']:
            raise ValueError('v0.81 unreviewed FU overlay: ' + asset + row['pointer'])



def validate_trial_evidence(treasure, mapdata, device, launcher):
    if treasure['extrachallengelabtranslocator'][0][1]['fill'] != [{'item': 'translocator'}]:
        raise ValueError('v0.81 trial chest must grant translocator')
    def walk(value):
        if isinstance(value, dict):
            yield value
            for child in value.values():
                yield from walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)
    chest = next((x for x in walk(mapdata) if x.get('id') == 53 and 'properties' in x), None)
    if not chest or build.parse_jsonc(chest['properties']['parameters'])['treasurePools'] != ['extrachallengelabtranslocator']:
        raise ValueError('v0.81 trial map chest pool drift')
    if device.get('itemName') != 'translocator' or 'teleport-node discs' not in device.get('description', ''):
        raise ValueError('v0.81 trial tool identity drift')
    if 'world.spawnProjectile(' not in launcher or '"translocatordisc"' not in launcher:
        raise ValueError('v0.81 trial disc launcher evidence drift')


def validate_trial_source(source):
    load = lambda path: build.parse_jsonc((source / path).read_text(encoding='utf-8-sig'))
    validate_trial_evidence(load('treasure/extradungeons.treasurepools'),
                            load('dungeons/challengelabs/challengelab3.json'),
                            load('items/active/unsorted/translocator/translocator.activeitem'),
                            (source / 'items/active/unsorted/translocator/translocator.lua').read_text(encoding='utf-8-sig'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    verify_source(args.source.resolve())
    manifest = read(TOOLS / 'v081_translations.json')
    pin = read(TOOLS / 'kaynaklar.json')
    if (manifest['source_commit'] != pin['commit']
            or manifest['source_repository'] != pin['repository']
            or manifest['source_declared_version'] != pin['declared_version']):
        raise ValueError('v0.81 manifest source pin drift')
    validate_manifest(manifest, read(TOOLS / 'ceviriler.json'),
                      read(TOOLS.parent / 'docs/reviews/radio2-20261022.json'))
    validate_source(manifest['translations'], args.source)
    validate_trial_source(args.source)
    print('v0.81 source gate PASS: 350 fields /7 assets /278 unique source strings /33 direct /317 FU patch fields')


if __name__ == '__main__':
    main()
