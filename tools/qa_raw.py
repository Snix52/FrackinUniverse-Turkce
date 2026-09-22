"""Fail-closed contracts for visible Lua string replacements, not Lua rewrites.

The lexer accepts incomplete snippets but never executes them. Only explicitly
listed string slots may differ; code, comments and other strings stay exact.
Runtime behavior overrides remain a separate, source-locked manifest.
"""
from __future__ import annotations
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

COLOR = re.compile(r'\^[^;\s]*;')
CONTROL = re.compile(r'\[(?![^\]]*\^)[^\]]+\]|<[^>]+>')
PRINTF = re.compile(r'%(?:\d+\$)?[-+0#]*(?:\d+|\*)?(?:\.\d+|\.\*)?(?:hh|h|ll|l|L|z|j|t)?[diuoxXfFeEgGaAcspn%]')
BRACE = re.compile(r'\{(?:\d+|[A-Za-z_][A-Za-z0-9_.:-]*)\}')
DOLLAR = re.compile(r'\$(?:\{[A-Za-z_][A-Za-z0-9_.:-]*\}|[A-Za-z_][A-Za-z0-9_.:-]*)')
NUMBER = re.compile(r'\d+(?:[.,]\d+)?')
LONG = re.compile(r'\[(=*)\[')
ESCAPES = {'a':'\a', 'b':'\b', 'f':'\f', 'n':'\n', 'r':'\r', 't':'\t', 'v':'\v', '\\':'\\', '"':'"', "'":"'"}


def lua_parts(code: str) -> tuple[list[str], list[str]]:
    """Return exact non-string segments and decoded Lua string literals."""
    if not isinstance(code, str) or not code:
        raise ValueError('Empty Lua snippet')
    segments, literals = [], []
    i = start = 0
    while i < len(code):
        if code.startswith('--', i):
            match = LONG.match(code, i + 2)
            if match:
                end = code.find(']' + match[1] + ']', match.end())
                if end < 0:
                    raise ValueError('Unterminated Lua comment')
                i = end + len(match[1]) + 2
            else:
                end = code.find('\n', i)
                i = len(code) if end < 0 else end + 1
            continue
        match = LONG.match(code, i)
        if match:
            end = code.find(']' + match[1] + ']', match.end())
            if end < 0:
                raise ValueError('Unterminated Lua long string')
            value = code[match.end():end]
            if value.startswith('\r\n'):
                value = value[2:]
            elif value.startswith('\n'):
                value = value[1:]
            stop = end + len(match[1]) + 2
        elif code[i] in ('"', "'"):
            quote = code[i]
            j = i + 1
            out = []
            while j < len(code) and code[j] != quote:
                char = code[j]
                if char in '\n\r':
                    raise ValueError('Unescaped newline in Lua string')
                if char != '\\':
                    out.append(char); j += 1; continue
                j += 1
                if j == len(code):
                    raise ValueError('Incomplete Lua escape')
                char = code[j]
                if char in ESCAPES:
                    out.append(ESCAPES[char]); j += 1
                elif char == '\n':
                    out.append('\n'); j += 1
                elif char == 'z':
                    j += 1
                    while j < len(code) and code[j].isspace():
                        j += 1
                elif char.isascii() and char.isdigit():
                    m = re.match(r'\d{1,3}', code[j:])
                    number = int(m[0])
                    if number > 255:
                        raise ValueError('Lua byte escape outside 0..255')
                    out.append(chr(number)); j += len(m[0])
                elif char == 'x' and re.match(r'[0-9a-fA-F]{2}', code[j+1:j+3]):
                    out.append(chr(int(code[j+1:j+3], 16))); j += 3
                elif char == 'u':
                    m = re.match(r'u\{([0-9a-fA-F]+)\}', code[j:])
                    if not m:
                        raise ValueError('Invalid Lua Unicode escape')
                    out.append(chr(int(m[1], 16))); j += len(m[0])
                else:
                    raise ValueError('Unsupported Lua escape: ' + char)
            if j >= len(code):
                raise ValueError('Unterminated Lua string')
            value, stop = ''.join(out), j + 1
        else:
            i += 1; continue
        segments.append(code[start:i])
        literals.append(value)
        i = start = stop
    segments.append(code[start:])
    return segments, literals


def validate_tokens(row: dict) -> None:
    en, tr = row['en'], row['tr']
    where = row['asset'] + row['pointer']
    for name, pattern in [('color', COLOR), ('control', CONTROL), ('printf', PRINTF),
                          ('brace', BRACE), ('dollar', DOLLAR)]:
        if Counter(pattern.findall(en)) != Counter(pattern.findall(tr)):
            raise ValueError('Raw ' + name + ' mismatch: ' + where)
    if PRINTF.findall(en) != PRINTF.findall(tr):
        raise ValueError('Raw printf argument order mismatch: ' + where)
    nums = lambda value: Counter(n.replace(',', '.') for n in NUMBER.findall(COLOR.sub('', value)))
    if nums(en) != nums(tr):
        raise ValueError('Raw number mismatch: ' + where)
    for char in ('%', '\n', '\r'):
        if en.count(char) != tr.count(char):
            raise ValueError('Raw formatting mismatch: ' + where)


def replacement_rows(asset: str, index: int, replacement: dict) -> list[dict]:
    old_code, old = lua_parts(replacement['old'])
    new_code, new = lua_parts(replacement['new'])
    if old_code != new_code or len(old) != len(new):
        raise ValueError('Lua technical code changed: ' + asset)
    slots = replacement.get('text_literals')
    changed = [i for i, (en, tr) in enumerate(zip(old, new)) if en != tr]
    if (not isinstance(slots, list) or not slots or
            any(type(i) is not int for i in slots) or slots != sorted(set(slots)) or
            any(i < 0 or i >= len(old) for i in slots) or changed != slots):
        raise ValueError('Lua visible string slots mismatch: ' + asset)
    if type(replacement.get('expected_count')) is not int or replacement['expected_count'] < 1:
        raise ValueError('Invalid raw expected_count: ' + asset)
    return [dict(asset=asset, pointer=f'/replacements/{index}/literals/{i}', en=old[i], tr=new[i]) for i in slots]


def validate_raw(manifest: dict, format_policy: dict, validate_format) -> list[dict]:
    rows, assets = [], set()
    for spec in manifest['assets']:
        asset = spec['asset']
        if asset in assets:
            raise ValueError('Duplicate raw asset: ' + asset)
        assets.add(asset)
        if not re.fullmatch(r'[0-9a-f]{40}', spec.get('source_blob_sha', '')):
            raise ValueError('Missing raw source blob: ' + asset)
        seen = set()
        for i, replacement in enumerate(spec['replacements']):
            if replacement['old'] in seen:
                raise ValueError('Duplicate raw replacement: ' + asset)
            seen.add(replacement['old'])
            for row in replacement_rows(asset, i, replacement):
                validate_format(row, format_policy)
                validate_tokens(row)
                rows.append(row)
    return rows


def verify_source_blob(spec: dict, path: Path) -> None:
    data = path.read_bytes()
    actual = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    if actual != spec.get('source_blob_sha'):
        raise ValueError('Raw source blob mismatch: ' + spec['asset'])


def validate_manifest_pin(manifest: dict, tools: Path) -> None:
    source = json.loads((tools / 'kaynaklar.json').read_text(encoding='utf-8'))
    if (manifest.get('source_commit') != source['commit'] or
            manifest.get('source_repository') != source['repository']):
        raise ValueError('Raw manifest FU pin mismatch')
