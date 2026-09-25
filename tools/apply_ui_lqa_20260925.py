#!/usr/bin/env python3
"""One-shot source migration; removed from the final PR diff after validation."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def replace_once(path, old, new):
    text = path.read_text(encoding='utf-8')
    if text.count(old) != 1:
        raise ValueError('Migration anchor differs: ' + str(path) + ' ' + old[:60])
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


def main(source):
    from write_build_evidence import verify_source
    from ui_lqa_assets import blob_sha, render_images, config_replacements, MECH_CONFIG
    from check_ui_lqa_20260925 import expected_welcome, rebuild_raw
    from audit_remaining import parse_jsonc
    from qa_raw import lua_parts
    verify_source(source)
    spec = read(TOOLS / 'ui_lqa_20260925.json')
    pin = read(TOOLS / 'kaynaklar.json')
    if pin['commit'] != spec['source_commit']:
        raise ValueError('Pinned source changed')
    catalog_path = TOOLS / 'ceviriler.json'
    catalog = read(catalog_path)
    if catalog['translation_version'] != '0.65.0-beta':
        raise ValueError('Concurrent catalog version change')
    index = {(r['asset'], r['pointer']): r for r in catalog['translations']}
    edits = {}
    selected = []
    for asset, pointer, en, old, tr, limit in spec['ui_edits']:
        key = asset, pointer
        row = index[key]
        if (row['en'], row['tr']) != (en, old) or len(tr) > limit:
            raise ValueError('Changed UI row: ' + repr(key))
        row['tr'] = tr
        edits[key] = (en, old, tr)
        selected.append(copy.deepcopy(row))
    for manifest_path in TOOLS.glob('v*_translations.json'):
        manifest = read(manifest_path)
        if not isinstance(manifest, dict) or not isinstance(manifest.get('translations'), list):
            continue
        changed = False
        for row in manifest['translations']:
            key = row['asset'], row['pointer']
            if key not in edits:
                continue
            en, old, tr = edits[key]
            if (row['en'], row['tr']) != (en, old):
                raise ValueError('Historical manifest drift: ' + str(manifest_path) + repr(key))
            row['tr'] = tr
            changed = True
        if changed:
            write(manifest_path, manifest)
    # Historical generators must not bring back the exact overflowing captions.
    for name in ('generate_v039.py', 'generate_v042.py', 'generate_v043.py'):
        path = TOOLS / name
        if not path.exists():
            continue
        before = path.read_text(encoding='utf-8')
        after = before
        for en, old, tr in edits.values():
            for quote in ('"', "'"):
                after = after.replace(quote + old + quote, quote + tr + quote)
        if after != before:
            path.write_text(after, encoding='utf-8')
    new_rows = []
    for asset, pointer, en, tr in spec['radio']:
        if (asset, pointer) in index:
            raise ValueError('Radio row already exists; review instead of overwriting')
        new_rows.append(dict(asset=asset, pointer=pointer, en=en, tr=tr,
                             section='v0.65.1 ekran LQA düzeltmeleri',
                             qa={'layered_source': True, 'source_patch': asset + '.patch'}))
    if ('_FUversioning.config', '/welcome') in index:
        raise ValueError('Welcome row already exists')
    new_rows.append(expected_welcome(source, spec))
    selected.extend(new_rows)
    catalog['translations'].extend(new_rows)
    catalog['translation_version'] = spec['translation_version']
    write(catalog_path, catalog)
    write(TOOLS / 'v0651_translations.json', dict(
        translation_version=spec['translation_version'], source_repository=spec['source_repository'],
        source_commit=spec['source_commit'], source_declared_version='6.5.8',
        scope='Screenshot-linked Pet House, Tricorder, Mech, welcome and radio fields', translations=selected))
    raw_path = TOOLS / 'raw_text_translations.json'
    raw_manifest = read(raw_path)
    raw_index = {s['asset']: s for s in raw_manifest['assets']}
    for asset, pairs in spec['raw_strings'].items():
        raw = (source / asset).read_bytes()
        source_text = raw.decode('utf-8-sig').replace('\r\n', '\n')
        entry = raw_index.get(asset)
        if entry is None:
            entry = dict(asset=asset, source_blob_sha=blob_sha(raw), replacements=[])
            raw_manifest['assets'].append(entry)
        elif entry['source_blob_sha'] != blob_sha(raw):
            raise ValueError('Raw source hash differs: ' + asset)
        for en, tr, count in pairs:
            matches = []
            for quote in ('"', "'"):
                def quoted(s):
                    return quote + s.replace('\\', '\\\\').replace(quote, '\\' + quote).replace('\n', '\\n') + quote
                old, new = quoted(en), quoted(tr)
                if source_text.count(old) == count:
                    matches.append((old, new))
            if len(matches) != 1:
                raise ValueError('Non-unique literal source: ' + asset + ' ' + en)
            old, new = matches[0]
            if any(r['old'] == old for r in entry['replacements']):
                raise ValueError('Duplicate raw UI replacement')
            entry['replacements'].append(dict(old=old, new=new, display_en=en, display_tr=tr,
                                               expected_count=count, text_literals=[0]))
    write(raw_path, raw_manifest)
    runtime_path = TOOLS / 'raw_runtime_overrides.json'
    runtime = read(runtime_path)
    mech_lua = 'interface/mechfuel/mechfuel.lua'
    if any(s['asset'] in (mech_lua, MECH_CONFIG) for s in runtime['assets']):
        raise ValueError('UI runtime override already exists')
    runtime['assets'].append(dict(asset=mech_lua,
        source_blob_sha=blob_sha((source / mech_lua).read_bytes()),
        reason='Display-only: Loading is a literal status label, not a placeholder. Fuel IDs stay unchanged; displayName is used only by the label renderer.',
        replacements=[
            dict(old='widget.setText("lblModuleCount", "^red;<Loading>^reset;")',
                 new='widget.setText("lblModuleCount", "^red;Yükleniyor^reset;")', expected_count=2),
            dict(old='.. ";" .. type)', new='.. ";" .. (fuelTypeData.displayName or type))', expected_count=1)
        ]))
    images, labels = render_images(source, spec)
    config_text = (source / MECH_CONFIG).read_text(encoding='utf-8-sig')
    runtime['assets'].append(dict(asset=MECH_CONFIG,
        source_blob_sha=blob_sha((source / MECH_CONFIG).read_bytes()),
        reason='Source-bound presentation override: text-free FU button/legend art with native Turkish labels; all fuel IDs, rates, callbacks and gameplay values are unchanged.',
        replacements=config_replacements(config_text, spec, labels)))
    write(runtime_path, runtime)
    for asset, text in rebuild_raw(source, set(spec['raw_strings']) | {MECH_CONFIG}).items():
        path = TOOLS / 'raw_overrides' / asset
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
    custom_path = TOOLS / 'custom_assets.json'
    custom = read(custom_path)
    for asset, content in images.items():
        if asset in custom['assets']:
            raise ValueError('Custom UI image already exists')
        path = TOOLS / 'custom_assets' / asset
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        custom['assets'].append(asset)
    write(custom_path, custom)
    provenance_paths = set(spec['raw_strings']) | {MECH_CONFIG, '_FUversioning.config'}
    provenance_paths.update(edit[0] for edit in spec['ui_edits'])
    provenance_paths.update(row[0] + '.patch' for row in spec['radio'])
    for asset in provenance_paths:
        actual = blob_sha((source / asset).read_bytes())
        previous = pin['assets'].get(asset)
        if previous is not None and previous != actual:
            raise ValueError('Existing provenance differs: ' + asset)
        pin['assets'][asset] = actual
    pin['assets'] = dict(sorted(pin['assets'].items()))
    write(TOOLS / 'kaynaklar.json', pin)
    builder = TOOLS / 'build_validate.py'
    old = 'def allowed(a,p):\n'
    new = "_V0651_UI_LQA = json.loads(Path(__file__).with_name('v0651_translations.json').read_text(encoding='utf-8'))\nV0651_UI_LQA_FIELDS = {(r['asset'], r['pointer']) for r in _V0651_UI_LQA['translations']}\nif len(V0651_UI_LQA_FIELDS) != 11:\n    raise ValueError('v0.65.1 UI LQA field inventory drift')\n\ndef allowed(a,p):\n    if (a,p) in V0651_UI_LQA_FIELDS:\n        return True\n"
    replace_once(builder, old, new)
    # Keep Lua compilation coverage precise after adding a JSON presentation template.
    path = TOOLS / 'tests' / 'test_lua_behavior.py'
    replace_once(path, "for s in json.loads((TOOLS/name).read_text(encoding='utf-8'))['assets']}",
                 "for s in json.loads((TOOLS/name).read_text(encoding='utf-8'))['assets'] if s['asset'].endswith('.lua')}")
    for filename in ('pr-qa.yml', 'build-package.yml'):
        path = ROOT / '.github' / 'workflows' / filename
        old = '          python tools/generate_v065.py --source fu_source\n'
        new = old + '          python -m pip install Pillow==11.3.0\n          python tools/check_ui_lqa_20260925.py --source fu_source\n'
        replace_once(path, old, new)
    audit = TOOLS / 'audit_remaining.py'
    replace_once(audit, '    key = parts[-1].lower() if parts else ""\n',
                 '    if asset == "_FUversioning.config" and parts == ["welcome"]:\n        return "confirmed"\n    key = parts[-1].lower() if parts else ""\n')
    replace_once(audit, '    path = asset.lower()\n',
                 '    path = asset.lower()\n    if path == "_fuversioning.config":\n        return "Arayüz"\n')
    checkpoint = ROOT / 'FU_SESSION_CHECKPOINT.md'
    text = checkpoint.read_text(encoding='utf-8')
    entry = '\n\n## 25 Eylül 2026: ekran görüntüsü temelli UI LQA düzeltmeleri\n\nAltı taşan/uzun etiket kısaltıldı. GPS Lua başlıkları ve gemi bilgileri, Mech dinamik durumları, SAIL atmosfer yanıtları, FU karşılama metni ve dört FU katmanlı telsiz mesajı kaynaklarına bağlandı. Mech bitmap İngilizce yazıları yedi kaynak-kilitli görselde temizlenip yerel UI etiketlerine taşındı; yakıt kimlikleri ve hesaplama değerleri korunuyor. Kaynak tarifi tools/ui_lqa_20260925.json, doğrulama tools/check_ui_lqa_20260925.py içindedir. Tam kaynak/CI sonuçları PR ve workflow kaydından kontrol edilir. Oyun içi tekrar testi: NOT TESTED. GPS gezegen sözlüklerindeki özel adlar ve eski değişiklik günlükleri bu dar kapsamın dışındadır.\n'
    checkpoint.write_text(text.rstrip() + entry, encoding='utf-8')
    for name in ('lqa-probe.yml', 'apply-ui-lqa.yml'):
        (ROOT / '.github' / 'workflows' / name).unlink(missing_ok=True)
    Path(__file__).unlink()
    print('Applied source-only UI LQA migration: 6 revised + 5 new structured fields; ' + str(len(images)) + ' source-derived UI images')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True, type=Path)
    args = parser.parse_args()
    main(args.source.resolve())
