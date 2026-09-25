#!/usr/bin/env python3
"""Validate/package the actual build and derive fresh, non-self-referential QA evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from custom_assets import load_custom_assets

TOOLS = Path(__file__).resolve().parent


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f'blob {len(data)}\0'.encode('ascii') + data).hexdigest()


def tree_files(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        raise ValueError('Missing install tree: ' + str(root))
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlink not allowed in package: ' + str(path))
        if path.is_file():
            result[path.relative_to(root).as_posix()] = path.read_bytes()
    if '_metadata' not in result:
        raise ValueError('Missing package _metadata')
    return result


def tree_digest(files: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name, data in sorted(files.items()):
        digest.update(name.encode('utf-8') + b'\0' + hashlib.sha256(data).digest())
    return digest.hexdigest()


def build_inputs_digest() -> str:
    """Bind evidence to validators, rules, manifests and raw templates as well as the catalog."""
    files = {p.relative_to(TOOLS.parent).as_posix(): p.read_bytes()
             for p in TOOLS.rglob('*')
             if p.is_file() and (p.suffix in ('.py', '.json', '.lua')
                                 or 'custom_assets' in p.relative_to(TOOLS).parts)
             and '__pycache__' not in p.parts and p.name != 'test_raporu.json'}
    terminology = TOOLS.parent / 'docs/TERMINOLOGY.md'
    if terminology.is_file():
        files['docs/TERMINOLOGY.md'] = terminology.read_bytes()
    return tree_digest(files)


def verify_source(source_dir: Path | None) -> dict:
    pinned = read_json(TOOLS / 'kaynaklar.json')['commit']
    if source_dir is None:
        return {'status': 'NOT RUN', 'pinned_commit': pinned, 'verified_commit': None}
    actual = subprocess.run(['git', '-C', str(source_dir), 'rev-parse', 'HEAD'],
                            check=True, capture_output=True, text=True).stdout.strip()
    if actual != pinned:
        raise ValueError('FU source is not the pinned commit: ' + actual)
    top = subprocess.run(['git', '-C', str(source_dir), 'rev-parse', '--show-toplevel'],
                         check=True, capture_output=True, text=True).stdout.strip()
    if Path(top).resolve() != source_dir.resolve():
        raise ValueError('FU source must be the checkout root')
    # Extra and ignored files are also consumed by the build/audit filesystem scans.
    dirty = subprocess.run(['git', '-C', str(source_dir), 'status', '--porcelain', '--untracked-files=all', '--ignored'],
                           check=True, capture_output=True, text=True).stdout
    if dirty.strip():
        raise ValueError('Pinned FU source has modifications or extra files')
    return {'status': 'PASS', 'pinned_commit': pinned, 'verified_commit': actual,
            'layered_external_policy': 'Existing ledger provenance retained; not an independent vanilla runtime test.'}


def record_validation(output: Path, stats: dict, catalog: Path, source: dict) -> dict:
    commit = subprocess.run(['git', '-C', str(TOOLS.parent), 'rev-parse', 'HEAD'],
                            check=True, capture_output=True, text=True).stdout.strip()
    inputs_dirty = subprocess.run(
        ['git', '-C', str(TOOLS.parent), 'status', '--porcelain', '--untracked-files=all',
         '--', 'tools', 'docs/TERMINOLOGY.md', ':!tools/test_raporu.json', ':!tools/GELISTIRME.txt'],
        check=True, capture_output=True, text=True).stdout.strip()
    if os.environ.get('GITHUB_SHA') not in (None, commit):
        raise ValueError('Build checkout does not match GITHUB_SHA')
    result = dict(stats, schema_version=2,
                  generated_at_utc=datetime.now(timezone.utc).isoformat(),
                  source_commit=commit, source_inputs_dirty=bool(inputs_dirty),
                  build_inputs_sha256=build_inputs_digest(),
                  catalog_sha256=hashlib.sha256(catalog.read_bytes()).hexdigest(),
                  install_tree_sha256=tree_digest(tree_files(output / 'FU_Turkce')),
                  source_validation=source, in_game_lqa='NOT TESTED')
    write_json(output / 'validation.json', result)
    return result


def deterministic_zip(path: Path, files: dict[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in sorted(files.items()):
                info = zipfile.ZipInfo('FU_Turkce/' + name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def verified_patch_fields(name: str, operations: list) -> int:
    if not isinstance(operations, list) or not operations:
        raise ValueError('Invalid patch operations: ' + name)
    if all(isinstance(batch, list) for batch in operations):
        seen = {}
        for batch in operations:
            if (len(batch) != 2 or not all(isinstance(op, dict) for op in batch)
                    or [op.get('op') for op in batch] != ['test', 'replace']
                    or batch[0].get('path') != batch[1].get('path')
                    or not isinstance(batch[0].get('value'), str)
                    or not isinstance(batch[1].get('value'), str)):
                raise ValueError('Source-test/replace pairing mismatch: ' + name)
            path = batch[0]['path']
            source, translation = batch[0]['value'], batch[1]['value']
            if path in seen:
                previous_source, previous_translation, variants = seen[path]
                if ('\n' not in previous_source or '\r' in previous_source
                        or source.replace('\r\n', '\n') != previous_source
                        or source in variants or translation != previous_translation):
                    raise ValueError('Invalid line-ending source variant: ' + name + path)
                variants.add(source)
            else:
                seen[path] = (source, translation, {source})
        return len(seen)
    if not all(isinstance(op, dict) for op in operations):
        raise ValueError('Invalid patch operation shape: ' + name)
    tests = [x for x in operations if x.get('op') == 'test']
    replacements = [x for x in operations if x.get('op') == 'replace']
    if (len(operations) != 2 * len(tests) or len(tests) != len(replacements)
            or [x['path'] for x in tests] != [x['path'] for x in replacements]
            or len({x['path'] for x in tests}) != len(tests)
            or operations != tests + replacements):
        raise ValueError('Source-test/replace pairing mismatch: ' + name)
    if len(replacements) > 1:
        raise ValueError('Multi-field patch must use independent conditional batches: ' + name)
    return len(replacements)


def verify_package(path: Path, files: dict[str, bytes], stats: dict) -> None:
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC failure')
        names = archive.namelist()
        expected = {'FU_Turkce/' + name for name in files}
        if len(names) != len(set(names)) or set(names) != expected:
            raise ValueError('ZIP/install-tree inventory mismatch')
        for name, data in files.items():
            if archive.read('FU_Turkce/' + name) != data:
                raise ValueError('ZIP/install-tree byte mismatch: ' + name)
    custom = load_custom_assets(TOOLS)
    missing_custom = set(custom) - set(files)
    if missing_custom:
        raise ValueError('Custom asset missing from package: ' + ', '.join(sorted(missing_custom)))
    fields = patches = raw = 0
    for name, data in files.items():
        if name == '_metadata':
            continue
        if name in custom:
            if data != custom[name]:
                raise ValueError('Custom asset source/package mismatch: ' + name)
            continue
        if not name.endswith('.patch'):
            raw += 1
            continue
        patches += 1
        operations = json.loads(data)
        fields += verified_patch_fields(name, operations)
    if (fields, patches, raw, len(custom)) != (stats['fields'], stats['patch_assets'],
                                               stats['raw_assets'], stats.get('custom_assets', 0)):
        raise ValueError('Build report/package count mismatch')
    if stats.get('assets') is not None and stats['assets'] != patches + raw + len(custom):
        raise ValueError('Build report total asset count mismatch')


def build_evidence(zip_path: Path, mod_dir: Path, install_dir: Path, report_path: Path,
                   source_commit: str, run_id: str, create_zip: bool = False) -> dict:
    if not re.fullmatch(r'[0-9a-f]{40}', source_commit):
        raise ValueError('A full translation source commit is required')
    report = read_json(report_path)
    source = read_json(TOOLS / 'kaynaklar.json')
    catalog_path = TOOLS / 'ceviriler.json'
    catalog = read_json(catalog_path)
    if report.get('static_qa') != 'PASS' or report.get('source_validation', {}).get('status') != 'PASS':
        raise ValueError('Current full-source validation report is required')
    if report['source_validation'].get('verified_commit') != source['commit']:
        raise ValueError('Validation report is not for the pinned FU revision')
    if report.get('source_commit') != source_commit:
        raise ValueError('Validation report belongs to a different translation source commit')
    if report.get('source_inputs_dirty') is not False:
        raise ValueError('Validation report was built from uncommitted source inputs')
    if report.get('build_inputs_sha256') != build_inputs_digest():
        raise ValueError('Validation report/build inputs mismatch; rebuild after source changes')
    if report['catalog_sha256'] != hashlib.sha256(catalog_path.read_bytes()).hexdigest():
        raise ValueError('Validation report/catalog mismatch')
    files = tree_files(mod_dir)
    if tree_files(install_dir) != files:
        raise ValueError('Root/install-tree byte mismatch')
    if tree_digest(files) != report['install_tree_sha256']:
        raise ValueError('Validation report/install-tree mismatch')
    if create_zip:
        deterministic_zip(zip_path, files)
    verify_package(zip_path, files, report)
    raw_count = 0
    for spec in read_json(TOOLS / 'raw_text_translations.json')['assets']:
        text = files[spec['asset']].decode('utf-8')
        for replacement in spec['replacements']:
            count = int(replacement.get('expected_count', 1))
            if text.count(replacement['new']) != count or replacement['old'] in text:
                raise ValueError('Packaged raw text replacement mismatch: ' + spec['asset'])
            raw_count += count
    if raw_count != report['raw_strings']:
        raise ValueError('Raw string count mismatch')
    runtime_manifest = TOOLS / 'raw_runtime_overrides.json'
    if runtime_manifest.is_file():
        for spec in read_json(runtime_manifest).get('assets', []):
            text = files[spec['asset']].decode('utf-8')
            for replacement in spec.get('replacements', []):
                count = int(replacement.get('expected_count', 1))
                if text.count(replacement['new']) != count or replacement['old'] in text:
                    raise ValueError('Packaged runtime override mismatch: ' + spec['asset'])
    data = zip_path.read_bytes()
    return {'schema_version': 2, 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
            'workflow_run_id': str(run_id), 'source_commit': source_commit,
            'translation_source_commit': source_commit,
            'translation_version': catalog['translation_version'],
            'custom_game_assets': report.get('custom_assets', 0),
            'upstream_repository': source['repository'], 'upstream_commit': source['commit'],
            'upstream_declared_version': source['declared_version'],
            'localized_units': {'structured_fields': report['fields'], 'patch_assets': report['patch_assets'],
                                'raw_override_assets': report['raw_assets'], 'raw_script_strings': raw_count},
            'package': {'path': zip_path.as_posix(), 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest(), 'git_blob_sha': git_blob_sha(data),
                        'zip_integrity': 'PASS', 'root_install_tree_parity': 'PASS'},
            'install_tree_sha256': report['install_tree_sha256'],
            'build_inputs_sha256': report['build_inputs_sha256'],
            'catalog_sha256': report['catalog_sha256'], 'static_qa': report['static_qa'],
            'source_validation': report['source_validation'], 'in_game_lqa': 'NOT TESTED'}


def refresh_tracked(evidence: dict) -> None:
    catalog = read_json(TOOLS / 'ceviriler.json')
    units = evidence['localized_units']
    report = dict(evidence,
                  translated_display_fields=units['structured_fields'], patched_assets=units['patch_assets'],
                  raw_override_assets=units['raw_override_assets'], raw_script_display_strings=units['raw_script_strings'],
                  total_localized_display_units=units['structured_fields'] + units['raw_script_strings'],
                  target_assets_total=units['patch_assets'] + units['raw_override_assets']
                                      + evidence.get('custom_game_assets', 0),
                  categories=dict(Counter(r.get('section', 'Uncategorized') for r in catalog['translations'])),
                  checks={'static_qa': evidence['static_qa'], 'source_validation': evidence['source_validation'],
                          'zip_integrity': evidence['package']['zip_integrity'], 'root_install_tree_parity': 'PASS'},
                  documented_source_fixes=[{'asset': r['asset'], 'pointer': r['pointer'], 'qa': r['qa']}
                                          for r in catalog['translations'] if r.get('qa')])
    write_json(TOOLS / 'test_raporu.json', report)
    lines = ['FU TÜRKÇE — OTOMATİK GÜNCEL BUILD RAPORU',
             'Bu dosya build sonrası üretilir; geçmiş sürüm ölçümleri içermez.',
             f"source_commit: {evidence['source_commit']}",
             f"workflow_run_id: {evidence['workflow_run_id']}",
             f"pinned_upstream_commit: {evidence['upstream_commit']}",
             f"timestamp: {evidence['generated_at_utc']}"]
    lines += [f'{key}: {value}' for key, value in units.items()]
    lines += [f"ZIP bytes: {evidence['package']['bytes']}", f"ZIP SHA256: {evidence['package']['sha256']}",
              'static QA: PASS', 'pinned FU source validation: PASS', 'ZIP / root tree parity: PASS',
              'in_game_lqa: NOT TESTED', 'Görsel/font/taşma ve oynanış zinciri: docs/LQA_CHECKLIST.md', '']
    (TOOLS / 'GELISTIRME.txt').write_text('\n'.join(lines), encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--zip', dest='zip_path', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--translation-source-commit', required=True)
    parser.add_argument('--workflow-run-id', required=True)
    parser.add_argument('--build-report', type=Path, default=Path('build_output/validation.json'))
    parser.add_argument('--mod-dir', type=Path, default=Path('build_output/FU_Turkce'))
    parser.add_argument('--install-dir', type=Path, default=Path('FU_Turkce'))
    parser.add_argument('--create-zip', action='store_true')
    parser.add_argument('--refresh-tracked', action='store_true')
    args = parser.parse_args()
    evidence = build_evidence(args.zip_path, args.mod_dir, args.install_dir, args.build_report,
                              args.translation_source_commit, args.workflow_run_id, args.create_zip)
    write_json(args.output, evidence)
    if args.refresh_tracked:
        refresh_tracked(evidence)
    print(json.dumps(evidence, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
