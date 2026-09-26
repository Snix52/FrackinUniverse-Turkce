#!/usr/bin/env python3
"""Read-only source gate for the screenshot-driven v0.65.1 UI corrections."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
SPEC = TOOLS / 'ui_lqa_20260925.json'
MANIFEST = TOOLS / 'v0651_translations.json'
MECH = 'interface/mechfuel/mechfuel.config'


def read(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def newline_pattern(text: str) -> str:
    return ''.join('C' if match == '\r\n' else 'L' for match in re.findall(r'\r\n|\n', text))


def expected_welcome(source: Path, spec: dict) -> dict:
    from audit_remaining import parse_jsonc
    from ui_lqa_assets import source_bytes
    original = parse_jsonc(source_bytes(source, '_FUversioning.config', spec['welcome_source_blob']).decode('utf-8-sig'))['welcome']
    en = original.replace('\r\n', '\n')
    lines = en.split('\n')
    translations = iter(spec['welcome_lines_tr'])
    if sum(bool(line.strip()) for line in lines) != len(spec['welcome_lines_tr']):
        raise ValueError('Welcome paragraph layout changed')
    translated = [next(translations) if line.strip() else line for line in lines]
    return dict(asset='_FUversioning.config', pointer='/welcome', en=en,
                tr='\n'.join(translated), section='v0.65.1 ekran LQA düzeltmeleri',
                qa={'source_newline_pattern': newline_pattern(original)})


def rebuild_raw(source: Path, assets: set[str]) -> dict[str, str]:
    from qa_raw import verify_source_blob, validate_manifest_pin
    result = {}
    for name in ('raw_text_translations.json', 'raw_runtime_overrides.json'):
        manifest = read(TOOLS / name)
        validate_manifest_pin(manifest, TOOLS)
        for spec in manifest['assets']:
            asset = spec['asset']
            if asset not in assets:
                continue
            path = source / asset
            verify_source_blob(spec, path)
            text = result.get(asset, path.read_text(encoding='utf-8-sig'))
            for replacement in spec['replacements']:
                if text.count(replacement['old']) != replacement['expected_count']:
                    raise ValueError('Raw source anchor differs: ' + asset)
                text = text.replace(replacement['old'], replacement['new'])
            result[asset] = text
    if set(result) != assets:
        raise ValueError('Missing raw UI asset')
    return result


def check(source: Path) -> dict:
    from write_build_evidence import verify_source
    from ui_lqa_assets import render_images, verify_config, config_replacements, same_image_pixels
    import build_validate as build
    verify_source(source)
    spec = read(SPEC)
    if read(TOOLS / 'kaynaklar.json')['commit'] != spec['source_commit']:
        raise ValueError('UI LQA source pin differs')
    catalog = read(TOOLS / 'ceviriler.json')
    index = {(r['asset'], r['pointer']): r for r in catalog['translations']}
    rows = read(MANIFEST)['translations']
    if len(rows) != 11 or len({(r['asset'], r['pointer']) for r in rows}) != 11:
        raise ValueError('UI LQA structured inventory differs')
    expected_keys = {(edit[0], edit[1]) for edit in spec['ui_edits'] + spec['radio']} | {('_FUversioning.config', '/welcome')}
    if {(r['asset'], r['pointer']) for r in rows} != expected_keys:
        raise ValueError('Unexpected UI LQA structured scope')
    cache = {}
    for row in rows:
        if index.get((row['asset'], row['pointer'])) != row:
            raise ValueError('UI manifest/catalog differs: ' + row['asset'] + row['pointer'])
        if row.get('qa', {}).get('layered_source'):
            build.verify_layered_row(row, source, cache)
        else:
            original = build.parse_jsonc((source / row['asset']).read_bytes().decode('utf-8-sig'))
            actual = build.read_at(original, row['pointer'])
            if actual.replace('\r\n', '\n') != row['en']:
                raise ValueError('Direct UI source differs')
            patched = build.simulate(original, build.translation_patch(row['asset'], [row]))
            if build.read_at(patched, row['pointer']) != row['tr']:
                raise ValueError('Real UI source did not translate')
    if index[('_FUversioning.config', '/welcome')] != expected_welcome(source, spec):
        raise ValueError('Welcome source, text or mixed newline contract differs')
    for asset, pointer, en, previous, tr, limit in spec['ui_edits']:
        row = index[asset, pointer]
        if row['tr'] != tr or row['en'] != en or len(tr) > limit:
            raise ValueError('UI caption length regression: ' + pointer)
    for asset, pointer, en, tr in spec['radio']:
        row = index[asset, pointer]
        if (row['en'], row['tr']) != (en, tr):
            raise ValueError('Radio text differs')
    affected = set(spec['raw_strings']) | {MECH}
    raw = rebuild_raw(source, affected)
    for asset, text in raw.items():
        if (TOOLS / 'raw_overrides' / asset).read_text(encoding='utf-8') != text:
            raise ValueError('UI raw template differs: ' + asset)
    original_config_text = (source / MECH).read_text(encoding='utf-8-sig')
    original_config = build.parse_jsonc(original_config_text)
    modified_config = build.parse_jsonc(raw[MECH])
    verify_config(original_config, modified_config, spec)
    relevant = [r for r in catalog['translations'] if r['asset'] == MECH]
    patched = build.simulate(modified_config, build.translation_patch(MECH, relevant))
    for row in relevant:
        if build.read_at(patched, row['pointer']) != row['tr']:
            raise ValueError('Mech image/layout override suppresses text patch')
    images, labels = render_images(source, spec)
    runtime = next(s for s in read(TOOLS / 'raw_runtime_overrides.json')['assets'] if s['asset'] == MECH)
    if runtime['replacements'] != config_replacements(original_config_text, spec, labels):
        raise ValueError('Mech config source recipe differs')
    for asset, content in images.items():
        if not same_image_pixels((TOOLS / 'custom_assets' / asset).read_bytes(), content):
            raise ValueError('UI image is not reproducible: ' + asset)
    return dict(structured_fields=len(rows), new_structured_fields=5,
                shortened_labels=6, raw_literal_replacements=sum(len(x) for x in spec['raw_strings'].values()),
                localized_image_assets=len(images), native_fuel_legend_labels=len(labels),
                gameplay_parameters='UNCHANGED', in_game_lqa='NOT TESTED')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    print('UI LQA source gate PASS: ' + json.dumps(check(args.source.resolve()), ensure_ascii=False))
