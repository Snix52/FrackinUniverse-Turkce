"""Prepare a source-bound gameplay queue and a reviewable packet; never edit catalogs."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import fnmatch
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

from audit_remaining import audit, parse_jsonc
from qa_integrity import validate_project
from write_build_evidence import verify_source

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def fingerprints():
    paths = [TOOLS / name for name in (
        'ceviriler.json', 'kaynaklar.json', 'locked_terms.json',
        'translation_memory_exceptions.json', 'raw_text_translations.json',
        'translation_priorities.json', 'plan_translation.py', 'audit_remaining.py',
        'qa_integrity.py', 'qa_raw.py', 'rule_data.py', 'write_build_evidence.py')]
    paths += sorted((TOOLS / 'rules').glob('*.json'))
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def priority(row, policy):
    matches = [rule for rule in policy['rules']
               if any(fnmatch.fnmatchcase(row['asset'], pat) for pat in rule['assets'])
               and (not rule.get('pointer') or re.search(rule['pointer'], row.get('pointer', '')))]
    if not matches:
        return 'P2', 'unclassified', 'Sınıflandırılmamış oyuncu metni; elle öncelik kontrolü gerekli.'
    chosen = min(matches, key=lambda rule: rule['priority'])
    return chosen['priority'], chosen['id'], chosen['reason']


def family(asset):
    parts = PurePosixPath(asset).parts
    depth = 3 if parts[:2] in [('items', 'generic'), ('objects', 'themed'),
                               ('quests', 'fu_questlines')] else 2
    return '/'.join(parts[:min(depth, len(parts) - 1)]) or parts[0]


def context(asset, pointer):
    """Conservative suggested groups; human confirmation remains mandatory."""
    parts = pointer.strip('/').split('/')
    lower = pointer.lower()
    if any(word in lower for word in ('dialog', 'chatter', 'converse', 'wake', 'contentpages')) or asset.startswith(('npcs/', 'dialog/', 'codex/')):
        # Keep each speaker/asset and dialogue branch distinct; only array indices collapse.
        role = '/'.join(p for p in parts if not p.isdigit())
        return [family(asset), asset, role]
    if len(parts) == 1 and (parts[0].lower().endswith('description') or parts[0] in ('title', 'subtitle')):
        # Floran/Glitch inspection voices remain distinct from ordinary descriptions.
        return [family(asset), '', parts[0]]
    return [family(asset), asset, '/'.join(p for p in parts if not p.isdigit())]


def asset_role_hints(source, assets):
    """Inspect gameplay keys as well as folders, including FU patch-only objects."""
    hints = defaultdict(list)
    for asset in sorted(set(assets)):
        if not asset.endswith('.object'):
            continue
        for path in (source / asset, source / (asset + '.patch')):
            if not path.is_file():
                continue
            data = parse_jsonc(path.read_text(encoding='utf-8-sig'))
            def visit(value, pointer=''):
                key = pointer.rsplit('/', 1)[-1]
                signal = None
                if key in ('offeredQuests', 'pickupQuestTemplates') and isinstance(value, list) and value:
                    signal = ('P1', 'quest-provider', 'Kaynakta görev sunma/başlatma bağlantısı var.')
                elif key == 'interactAction' and value in ('OpenCraftingInterface', 'ScriptPane', 'OpenTeleportDialog', 'OpenMerchantInterface'):
                    signal = ('P1', 'interactive-system', 'Kaynakta üretim, panel, ışınlanma veya dükkân arayüzü açılıyor.')
                elif key in ('inputNodes', 'outputNodes') and isinstance(value, list) and value:
                    signal = ('P1', 'wired-system', 'Kaynakta kablolu sistem bağlantısı var; işlevi incele.')
                if signal:
                    hints[asset].append({'priority': signal[0], 'rule': signal[1], 'reason': signal[2],
                                         'source': path.relative_to(source).as_posix(), 'pointer': pointer})
                if isinstance(value, dict):
                    # Patch values retain their destination pointer, not /N/value.
                    if value.get('op') in ('add', 'replace') and isinstance(value.get('path'), str):
                        visit(value.get('value'), value['path'])
                    else:
                        for k, child in value.items():
                            visit(child, pointer + '/' + k)
                elif isinstance(value, list):
                    for index, child in enumerate(value):
                        visit(child, pointer + '/' + str(index))
            visit(data)
    return hints


def queue_rows(report, policy, hints=None):
    hints = hints or {}
    rows = []
    for raw in report['remaining_rows']:
        row = dict(raw, en=raw['value'], pool=raw['confidence'])
        del row['value']
        row['priority'], row['priority_rule'], row['priority_reason'] = priority(row, policy)
        row['gameplay_hints'] = hints.get(row['asset'], [])
        if row['gameplay_hints']:
            hint = min(row['gameplay_hints'], key=lambda h: h['priority'])
            if hint['priority'] < row['priority']:
                row['priority'], row['priority_rule'], row['priority_reason'] = hint['priority'], hint['rule'], hint['reason']
        if (row['asset'].endswith('.object') and re.fullmatch(r'/[a-zA-Z]+Description', row['pointer'])
                and row['pointer'] not in ('/shortDescription', '/interactionDescription', '/turnInDescription')):
            row['priority'], row['priority_rule'], row['priority_reason'] = (
                'P3', 'inspection-voice', 'Nesneyi incelerken söylenen karakter repliği; mekanik yönlendirme varsa elle yükselt.')
        row['family'] = family(row['asset'])
        rows.append(row)
    for raw in report['lua_review']['rows']:
        row = dict(raw, en=raw['source'], pointer=f"line:{raw['line']}", pool='lua_review')
        row['priority'], row['priority_rule'], row['priority_reason'] = priority(row, policy)
        row['family'] = family(row['asset'])
        rows.append(row)
    return sorted(rows, key=lambda r: (r['priority'], r['family'], r['asset'], r['pointer']))


def units_for(rows, tm_policy):
    exceptions = {item['en'] for item in tm_policy.get('exceptions', [])}
    grouped = defaultdict(list)
    for row in rows:
        ctx = context(row['asset'], row['pointer'])
        key = [ctx, row['en']]
        if row['en'] in exceptions:
            key.append([row['asset'], row['pointer']])
        grouped[digest(key)].append(row)
    units = []
    for unit_id, members in grouped.items():
        first = members[0]
        units.append({'id': unit_id, 'en': first['en'], 'tr': None,
                      'context': context(first['asset'], first['pointer']),
                      'context_reviewed': False, 'runtime_evidence': [],
                      'priority': min(r['priority'] for r in members),
                      'occurrences': [{'asset': r['asset'], 'pointer': r['pointer'],
                                       'origin': r['origin']} for r in members]})
    return sorted(units, key=lambda u: (u['priority'], u['occurrences'][0]['asset'],
                                       u['occurrences'][0]['pointer'], u['id']))


def enrich(units, catalog, terms):
    by_source = defaultdict(list)
    for row in catalog:
        by_source[row['en']].append(row)
    for unit in units:
        variants = defaultdict(list)
        for row in by_source[unit['en']]:
            variants[row['tr']].append({'asset': row['asset'], 'pointer': row['pointer'],
                                       'same_context': context(row['asset'], row['pointer']) == unit['context']})
        unit['tm_suggestions'] = [{'tr': tr, 'occurrence_count': len(refs),
                                   'examples': sorted(refs, key=lambda r: not r['same_context'])[:5]}
                                  for tr, refs in sorted(variants.items())]
        unit['tm_conflict'] = len(variants) > 1
        unit['locked_terms'] = []
        for term in terms['terms']:
            if term.get('status') != 'LOCKED':
                continue
            aliases = term['source'].split(' / ') + [f['en'] for f in term.get('forms', [])]
            if any(re.search(r'(?<!\w)' + re.escape(alias) + r'(?!\w)', unit['en'], re.I)
                   for alias in aliases if alias):
                unit['locked_terms'].append(term)


def choose(rows, requested, max_fields, max_units, tm_policy):
    families = defaultdict(list)
    for row in rows:
        if row['pool'] == 'confirmed':
            families[row['family']].append(row)
    if not families:
        raise ValueError('No confirmed candidates')
    if requested and requested not in families:
        raise ValueError('Unknown confirmed family: ' + requested)
    selected_family = requested or min(families, key=lambda f: (
        min(r['priority'] for r in families[f]),
        -sum(r['priority'] == min(x['priority'] for x in families[f]) for r in families[f]), f))
    available = units_for(families[selected_family], tm_policy)
    selected, count = [], 0
    for unit in available:
        size = len(unit['occurrences'])
        if count + size > max_fields or len(selected) >= max_units:
            break  # Never silently jump over a higher-priority or oversized group.
        selected.append(unit)
        count += size
    if not selected:
        raise ValueError('First context group exceeds packet limit; choose another family or raise --max-fields')
    return selected_family, selected, len(families[selected_family]), len(available)


def dependencies(source, units):
    """Direct asset references are leads, not a claim of complete runtime closure."""
    results = []
    for asset in sorted({o['asset'] for u in units for o in u['occurrences']}):
        paths = [source / asset, source / (asset + '.patch')]
        for path in paths:
            if not path.is_file():
                continue
            data = parse_jsonc(path.read_text(encoding='utf-8-sig'))
            def walk(value):
                if isinstance(value, dict):
                    for child in value.values():
                        yield from walk(child)
                elif isinstance(value, list):
                    for child in value:
                        yield from walk(child)
                elif isinstance(value, str):
                    yield value
            for value in sorted(set(walk(data))):
                if not re.fullmatch(r'[^\s]+\.(lua|config|object|questtemplate|species)', value):
                    continue
                ref = (source / value.lstrip('/')) if value.startswith('/') else path.parent / value
                ref = ref.resolve()
                if not ref.is_relative_to(source.resolve()):
                    continue
                results.append({'from': asset, 'reference': value,
                                'asset': ref.relative_to(source.resolve()).as_posix(),
                                'exists_in_fu': ref.is_file()})
    return results


def prepare(source, requested=None, max_fields=500, max_units=350):
    validation = verify_source(source)
    report = audit(source, TOOLS / 'ceviriler.json', include_rows=True)
    if report['inventory']['parse_failures']:
        raise ValueError('Audit parse failures; inspect audit before preparing a packet')
    policy = read(TOOLS / 'translation_priorities.json')
    hints = asset_role_hints(source, (r['asset'] for r in report['remaining_rows']))
    rows = queue_rows(report, policy, hints)
    tm_policy = read(TOOLS / 'translation_memory_exceptions.json')
    fam, units, family_fields, family_units = choose(rows, requested, max_fields, max_units, tm_policy)
    catalog = read(TOOLS / 'ceviriler.json')
    enrich(units, catalog['translations'], read(TOOLS / 'locked_terms.json'))
    deps = dependencies(source, units)
    dep_assets = {r['asset'] for r in deps}
    related = [r for r in rows if r['pool'] != 'confirmed' and
               (r['family'] == fam or r['asset'] in dep_assets)]
    selection = {'family': fam, 'max_fields': max_fields, 'max_units': max_units}
    packet = {'schema': 1, 'status': 'DRAFT_CONTEXT_REVIEW_REQUIRED',
              'source_validation': validation, 'catalog_version': catalog['translation_version'],
              'inputs': fingerprints(), 'selection': selection,
              'family_fields': family_fields, 'family_context_units': family_units,
              'field_count': sum(len(u['occurrences']) for u in units),
              'context_unit_count': len(units), 'units': units,
              'direct_dependencies': deps, 'related_review_rows': related,
              'gameplay_hints': {asset: hints[asset] for asset in sorted(
                  {o['asset'] for u in units for o in u['occurrences']}) if asset in hints},
              'runtime_review': {'reviewed': False, 'evidence': [],
                                 'note': 'Check recipes/research/quests/shops/placements and referenced scripts/configs; record missing vanilla or external-mod dependencies.'},
              'measurements': {'translation_minutes': None, 'review_minutes': None,
                               'reviewed_units': None, 'corrected_units': None,
                               'lqa_status': 'NOT TESTED'}}
    # Only the documented editable fields may change before preflight.
    packet['basis_sha256'] = digest(immutable_packet(packet))
    return report, rows, packet


def immutable_packet(packet):
    result = {k: v for k, v in packet.items() if k not in ('basis_sha256', 'measurements', 'runtime_review')}
    result['units'] = [{k: v for k, v in unit.items()
                        if k not in ('tr', 'context_reviewed', 'runtime_evidence')}
                       for unit in packet['units']]
    return result


def check_packet(packet, expected, catalog, tools=TOOLS):
    if digest(immutable_packet(packet)) != expected['basis_sha256']:
        raise ValueError('Packet source, context, rules, TM or field membership is stale/modified; regenerate')
    if packet.get('basis_sha256') != expected['basis_sha256']:
        raise ValueError('Packet basis digest differs')
    runtime = packet.get('runtime_review', {})
    if runtime.get('reviewed') is not True or not valid_evidence(runtime.get('evidence')):
        raise ValueError('Runtime/context review and source references are required')
    added = []
    for unit in packet['units']:
        if unit.get('context_reviewed') is not True or not valid_evidence(unit.get('runtime_evidence')):
            raise ValueError('Unreviewed context/runtime evidence: ' + unit['id'])
        if not isinstance(unit.get('tr'), str) or not unit['tr'].strip() or unit['tr'] == unit['en']:
            raise ValueError('Missing or unchanged translation: ' + unit['id'])
        if unit['en'].count('\n') != unit['tr'].count('\n'):
            raise ValueError('Newline count mismatch: ' + unit['id'])
        for occurrence in unit['occurrences']:
            added.append({k: occurrence[k] for k in ('asset', 'pointer')} |
                         {'en': unit['en'], 'tr': unit['tr']})
    existing = {(r['asset'], r['pointer']) for r in catalog}
    if any((r['asset'], r['pointer']) in existing for r in added):
        raise ValueError('Packet overlaps current catalog')
    qa = validate_project(catalog + added, tools)
    return {'status': 'TECHNICAL_PREFLIGHT_PASS_LANGUAGE_REVIEW_REQUIRED',
            'fields': len(added), 'context_units': len(packet['units']), 'qa': qa,
            'note': 'Runtime evidence is human-attested, not automatically proven. Existing exact-source manifests, allowlists, build, CI and LQA remain required.'}


def valid_evidence(value):
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, dict) and isinstance(item.get('source'), str) and item['source'].strip()
        and isinstance(item.get('note'), str) and item['note'].strip() for item in value)


def write_outputs(output, report, rows, packet):
    output.mkdir(parents=True, exist_ok=True)
    for name in ('queue.json', 'packet.json', 'summary.md'):
        if (output / name).exists():
            raise ValueError('Refusing to overwrite existing work: ' + str(output / name))
    payload = {'schema': 1, 'inputs': packet['inputs'],
               'source_validation': packet['source_validation'], 'rows': rows}
    (output / 'queue.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    counts = Counter((r['pool'], r['priority']) for r in rows)
    lines = ['# Oynanış önceliği ve çeviri hazırlığı', '',
             'Öncelikler kural temelli ilk tahmindir; gerçek karşılaşma sıklığı ölçülmedi.', '',
             '| Havuz | P0 | P1 | P2 | P3 | Toplam |', '|---|---:|---:|---:|---:|---:|']
    for pool in ('confirmed', 'review', 'lua_review'):
        vals = [counts[pool, f'P{i}'] for i in range(4)]
        lines.append('| ' + pool + ' | ' + ' | '.join(map(str, vals + [sum(vals)])) + ' |')
    matching = sum(bool(u['tm_suggestions']) for u in packet['units'])
    lines += ['', f"Aday aile: `{packet['selection']['family']}`.",
              f"Paket: {packet['field_count']} alan / {packet['context_unit_count']} bağlam grubu; {matching} grupta birebir kaynak TM önerisi.",
              f"Ailenin tamamı: {packet['family_fields']} alan / {packet['family_context_units']} bağlam grubu.",
              f"İlişkili ek inceleme: {len(packet['related_review_rows'])}; doğrudan dosya bağlantısı: {len(packet['direct_dependencies'])}.",
              'Paket taslaktır. Bağlam, runtime erişimi, çeviri ve Sol dil incelemesi bekler.',
              'TM ve LOCKED listeleri öneri bağlamı taşır; çeviri otomatik kabul edilmez.',
              'İlk paket süreleri ölçülmeden hız kazancı yüzdesi verilmez.', '', '## Aile sırası', '',
              '| Öncelik | Aile | Alan |', '|---|---|---:|']
    families = defaultdict(list)
    for row in rows:
        if row['pool'] == 'confirmed':
            families[row['family']].append(row)
    for fam, members in sorted(families.items(), key=lambda x: (
            min(r['priority'] for r in x[1]),
            -sum(r['priority'] == min(y['priority'] for y in x[1]) for r in x[1]), x[0])):
        lines.append(f"| {min(r['priority'] for r in members)} | {fam} | {len(members)} |")
    (output / 'summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'planning_output')
    parser.add_argument('--family')
    parser.add_argument('--max-fields', type=int, default=500)
    parser.add_argument('--max-units', type=int, default=350)
    parser.add_argument('--check-packet', type=Path)
    args = parser.parse_args()
    if args.check_packet:
        packet = read(args.check_packet)
        if packet.get('inputs') != fingerprints():
            raise ValueError('Packet inputs changed; regenerate against current source/catalog/rules')
        selection = packet['selection']
        _, _, expected = prepare(args.source.resolve(), selection['family'],
                                 selection['max_fields'], selection['max_units'])
        result = check_packet(packet, expected, read(TOOLS / 'ceviriler.json')['translations'])
        print(json.dumps(result, ensure_ascii=False))
    else:
        if args.max_fields < 1 or args.max_units < 1:
            parser.error('Packet limits must be positive')
        if any(args.output.resolve().is_relative_to(p.resolve()) for p in
               (args.source, ROOT / 'FU_Turkce', ROOT / 'dist', TOOLS)):
            parser.error('Output must be outside source, tools and published package trees')
        if any((args.output / name).exists() for name in ('packet.json', 'queue.json', 'summary.md')):
            parser.error('Output already exists; choose a fresh --output to preserve work')
        report, rows, packet = prepare(args.source.resolve(), args.family, args.max_fields, args.max_units)
        write_outputs(args.output, report, rows, packet)
        print((args.output / 'summary.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    main()
