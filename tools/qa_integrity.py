"""Generic catalog, context, number, whitespace, glyph and LOCKED-term guards."""
from __future__ import annotations
import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from rule_data import TOOLS, render_terminology
from qa_raw import CONTROL, validate_raw, validate_manifest_pin

COLOR = re.compile(r'\^[^;\s]*;')
NUMBER = re.compile(r'\d+(?:[.,]\d+)?')
SIGNED = re.compile(r'[+-]\s*%?\s*\d+(?:[.,]\d+)?')
ESCAPED_TAB = re.compile(r'(?<!\\)(?:\\\\)*\\t')


def plain(value: str) -> str:
    return COLOR.sub('', value).strip()


def signed_numbers(value: str) -> Counter:
    return Counter(re.sub(r'\s|%', '', n).replace(',', '.')
                   for n in SIGNED.findall(COLOR.sub('', value)))


def tab_signature(value: str) -> tuple:
    # JSON "\t" is U+0009 after decoding; literal Lua-style escapes are separate.
    return tuple((tuple(map(len, re.findall('\t+', line))),
                  len(ESCAPED_TAB.findall(line))) for line in value.split('\n'))


def icon_signature(value: str, glyphs=()) -> Counter:
    # Corpus U+E024 and private-use UI glyphs; never classify Turkish letters as icons.
    return Counter(c for c in value if c in glyphs or unicodedata.category(c) == 'Co')


def bound_exception(row: dict, exception: dict) -> bool:
    return bool(exception.get('reason', '').strip()) and all(
        row.get(k) == exception.get(k) for k in ('asset', 'pointer', 'en', 'tr'))


def validate_format(row: dict, policy: dict) -> None:
    en, tr = row['en'], row['tr']
    if not isinstance(en, str) or not isinstance(tr, str) or not tr.strip():
        raise ValueError('Empty or non-text translation: ' + row['asset'] + row['pointer'])
    where = row['asset'] + row['pointer']
    for name, signature in (
        ('color', lambda s: Counter(COLOR.findall(s))),
        ('number', lambda s: Counter(n.replace(',', '.') for n in NUMBER.findall(COLOR.sub('', s)))),
    ):
        if signature(en) != signature(tr):
            if not any(bound_exception(row, x) for x in policy.get(name + '_exceptions', [])):
                raise ValueError(name.title() + ' mismatch without bound exception: ' + where)
    if signed_numbers(en) != signed_numbers(tr):
        raise ValueError('Signed number mismatch: ' + where)
    if tab_signature(en) != tab_signature(tr):
        if not any(bound_exception(row, x) for x in policy.get('tab_exceptions', [])):
            raise ValueError('TAB structure mismatch: ' + where)
    if Counter(CONTROL.findall(en)) != Counter(CONTROL.findall(tr)):
        if not any(bound_exception(row, x) for x in policy.get('control_exceptions', [])):
            raise ValueError('Control token mismatch: ' + where)
    glyphs = policy.get('ui_glyphs', [])
    if icon_signature(en, glyphs) != icon_signature(tr, glyphs):
        raise ValueError('UI glyph mismatch: ' + where)


def validate_translation_memory(rows: list[dict], policy: dict) -> None:
    by_source = defaultdict(list)
    for row in rows:
        by_source[row['en']].append(row)
    exceptions = policy.get('exceptions', [])
    for source, group in by_source.items():
        if len({r['tr'] for r in group}) <= 1:
            continue
        choices = [x for x in exceptions if x.get('en') == source and x.get('reason', '').strip()]
        allowed = {(v['asset'], v['pointer'], v['tr'])
                   for x in choices for v in x['variants']}
        if any((r['asset'], r['pointer'], r['tr']) not in allowed for r in group):
            raise ValueError('Translation memory drift: ' + repr(source))


class Terminology:
    def __init__(self, policy: dict):
        self.exact = defaultdict(set)
        self.phrases = []
        self.stems = []
        self.exceptions = policy.get('context_exceptions', [])
        self.forbidden = [(re.compile(x['pattern'], re.I if x.get('ignore_case') else 0),
                           x.get('message', 'Forbidden terminology'))
                          for x in policy.get('forbidden_regexes', [])]
        for term in policy['terms']:
            if term['status'] != 'LOCKED':
                continue
            forms = term.get('forms')
            if forms is None:
                aliases = term['source'].split(' / ')
                forms = [{'en': a, 'tr': a if term.get('mode') == 'preserve' else term['tr']}
                         for a in aliases]
            for form in forms:
                en, tr = form['en'], form['tr']
                self.exact[en].add(tr)
                if term.get('tr_stem'):
                    self.stems.append((re.compile(r'(?<!\w)' + re.escape(en) + r'(?!\w)', re.I),
                                       term['tr_stem'].casefold().replace('\u0307', '')))
                enforce_in_text = term.get('enforce_in_text', False)
                if len(en.split()) < 2 and not enforce_in_text:
                    continue
                banned = [s.strip() for s in term['forbidden'].split(',') if s.strip() not in ('', '-')]
                self.phrases.append((re.compile(r'(?<!\w)' + re.escape(en) + r'(?!\w)', re.I),
                                     tr.casefold(), [(b, re.compile(r'(?<!\w)' + re.escape(b) + r'(?!\w)', re.I))
                                                     for b in banned], enforce_in_text))

    def validate(self, row: dict) -> None:
        en, tr = plain(row['en']), plain(row['tr'])
        where = row['asset'] + row['pointer']
        for pattern, message in self.forbidden:
            if pattern.search(row['tr']):
                raise ValueError(message + ': ' + where)
        if any(bound_exception(row, x) for x in self.exceptions):
            return
        if en in self.exact:
            allowed = self.exact[en]
            if len(allowed) != 1 or tr not in allowed:
                raise ValueError('LOCKED terminology/context mismatch: ' + where + ' -> ' + repr(sorted(allowed)))
        for source_pattern, stem in self.stems:
            if source_pattern.search(en) and stem not in tr.casefold().replace('\u0307', ''):
                raise ValueError('LOCKED terminology missing stem ' + repr(stem) + ': ' + where)
        for source_pattern, canonical, banned, enforce_in_text in self.phrases:
            if not source_pattern.search(en):
                continue
            # A canonical phrase may contain a shorter forbidden word. Only
            # that overlapping occurrence is safe, never a separate occurrence.
            canonical_spans = [m.span() for m in re.finditer(
                r'(?<!\w)' + re.escape(canonical) + r'(?!\w)', tr, re.I)]
            for variant, pattern in banned:
                if any(not any(a <= m.start() and m.end() <= b
                               for a, b in canonical_spans)
                       for m in pattern.finditer(tr)):
                    raise ValueError('LOCKED forbidden variant ' + repr(variant) + ': ' + where)
            if enforce_in_text and not canonical_spans:
                raise ValueError('LOCKED terminology missing ' + repr(canonical) + ': ' + where)


def manifest_rows(primary: list[dict], tools: Path = TOOLS) -> list[dict]:
    index = {(r['asset'], r['pointer']): r for r in primary}
    if len(index) != len(primary):
        raise ValueError('Duplicate field in primary catalog')
    rows = list(primary)
    for path in sorted(tools.glob('*_translations.json')):
        if path.name == 'raw_text_translations.json':
            continue
        payload = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(payload, dict) and 'translations' in payload:
            manifest = payload['translations']
        elif isinstance(payload, list):
            manifest = payload
        elif isinstance(payload, dict):
            manifest = []
            for spec in payload.values():
                if not isinstance(spec, dict) or 'asset' not in spec:
                    raise ValueError('Unknown structured manifest schema: ' + path.name)
                for field, pointer in (('name', '/shortdescription'), ('description', '/description')):
                    if field not in spec:
                        continue
                    key = (spec['asset'], pointer)
                    if key not in index:
                        raise ValueError('Manifest field missing from primary catalog: ' + repr(key))
                    if spec[field] != index[key]['tr']:
                        raise ValueError('Manifest/catalog drift: ' + path.name + ' ' + repr(key))
                    manifest.append(dict(index[key], tr=spec[field]))
        else:
            raise ValueError('Unknown structured manifest schema: ' + path.name)
        seen = set()
        for row in manifest:
            key = (row['asset'], row['pointer'])
            if key in seen:
                raise ValueError('Duplicate manifest field: ' + path.name + ' ' + repr(key))
            seen.add(key)
            if key not in index:
                raise ValueError('Manifest field missing from primary catalog: ' + repr(key))
            if any(row[field] != index[key][field] for field in ('en', 'tr')):
                raise ValueError('Manifest/catalog drift: ' + path.name + ' ' + repr(key))
        rows.extend(manifest)
    return rows


def validate_project(rows: list[dict], tools: Path = TOOLS) -> dict:
    format_policy = json.loads((tools / 'rules/text_integrity.json').read_text(encoding='utf-8'))
    tm_policy = json.loads((tools / 'translation_memory_exceptions.json').read_text(encoding='utf-8'))
    term_policy = json.loads((tools / 'locked_terms.json').read_text(encoding='utf-8'))
    terminology = Terminology(term_policy)
    all_rows = manifest_rows(rows, tools)
    for row in all_rows:
        validate_format(row, format_policy)
        terminology.validate(row)
    raw_manifest = json.loads((tools / 'raw_text_translations.json').read_text(encoding='utf-8'))
    validate_manifest_pin(raw_manifest, tools)
    raw_rows = validate_raw(raw_manifest, format_policy, validate_format)
    for row in raw_rows:
        terminology.validate(row)
    validate_translation_memory(all_rows + raw_rows, tm_policy)
    doc = tools.parent / 'docs/TERMINOLOGY.md'
    if doc.read_text(encoding='utf-8') != render_terminology(term_policy):
        raise ValueError('Generated terminology document is stale; run qa_integrity.py --write-docs')
    return {'catalog_units_checked': len(all_rows),
            'raw_units_checked': len(raw_rows),
            'locked_terms': sum(x['status'] == 'LOCKED' for x in term_policy['terms'])}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-docs', action='store_true')
    args = parser.parse_args()
    if args.write_docs:
        policy = json.loads((TOOLS / 'locked_terms.json').read_text(encoding='utf-8'))
        (TOOLS.parent / 'docs/TERMINOLOGY.md').write_text(render_terminology(policy), encoding='utf-8')
    rows = json.loads((TOOLS / 'ceviriler.json').read_text(encoding='utf-8'))['translations']
    print(json.dumps(validate_project(rows), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
