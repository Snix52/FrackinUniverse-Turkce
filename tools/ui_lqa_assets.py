"""Reproducible, pixel-bounded Mech UI artwork derived from pinned FU assets.

Only existing label pixels/button text boxes may change. Gameplay configuration,
icon art, dimensions and callbacks are not localized here. No font is bundled.
"""
from __future__ import annotations
import copy
import hashlib
import io
import json
import re
from collections import Counter
from pathlib import Path

MECH_CONFIG = 'interface/mechfuel/mechfuel.config'
IMAGE_ROOT = 'interface/fu_turkce/mechfuel/'
WHITE = (255, 255, 255, 255)


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def source_bytes(source: Path, path: str, expected: str | None = None) -> bytes:
    raw = (source / path).read_bytes()
    if expected and blob_sha(raw) != expected:
        raise ValueError('Pinned UI source mismatch: ' + path)
    return raw


def render_images(source: Path, spec: dict) -> tuple[dict[str, bytes], dict]:
    from PIL import Image
    images, labels = {}, {}
    for name, expected in spec['image_sources'].items():
        raw = source_bytes(source, 'interface/mechfuel/' + name, expected)
        original = Image.open(io.BytesIO(raw)).convert('RGBA')
        result = original.copy()
        width, height = result.size
        allowed = set()
        if name == 'body.png':
            if result.size != (345, 197):
                raise ValueError('Mech body dimensions changed')
            for i, (en, tr, x1, x2, y1, y2, font_size) in enumerate(spec['raster_labels']):
                glyphs = {(x, y) for x in range(x1, x2) for y in range(y1, y2)
                          if original.getpixel((x, y)) == WHITE}
                if not glyphs or glyphs & allowed:
                    raise ValueError('Missing or overlapping source label: ' + en)
                allowed.update(glyphs)
                for point in glyphs:
                    result.putpixel(point, (1, 9, 21, 255))
                gx = (min(x for x, y in glyphs) + max(x for x, y in glyphs) + 1) / 2
                gy = 219 - (y1 + y2) / 2
                labels[f'fuTrFuelLegend{i}'] = {
                    'type': 'label', 'zlevel': 1, 'position': [gx, gy],
                    'hAnchor': 'mid', 'vAnchor': 'mid', 'fontSize': font_size,
                    'value': tr,
                }
            expected_glyphs = {(x, y) for y in list(range(62, 67)) + list(range(91, 96)) + list(range(116, 121))
                               for x in range(160, 320) if original.getpixel((x, y)) == WHITE}
            if allowed != expected_glyphs or len(allowed) != 475:
                raise ValueError('Mech legend pixel inventory differs')
        else:
            glyphs = {(x, y) for y in range(height) for x in range(3, width - 3)
                      if original.getpixel((x, y)) == WHITE}
            expected_count = 120 if name.startswith('deploy') else 78
            if len(glyphs) != expected_count:
                raise ValueError('Button glyph inventory changed: ' + name)
            x1, x2 = min(x for x, y in glyphs) - 2, max(x for x, y in glyphs) + 3
            y1, y2 = min(y for x, y in glyphs) - 1, max(y for x, y in glyphs) + 3
            for y in range(max(2, y1), min(height - 2, y2)):
                # Sample unobstructed button fill from the same row to retain shading.
                choices = [original.getpixel((x, y)) for x in range(5, width - 5)
                           if not x1 <= x < x2 and original.getpixel((x, y))[3] == 255]
                if not choices:
                    raise ValueError('No clean fill sample: ' + name)
                fill = Counter(choices).most_common(1)[0][0]
                if fill == WHITE:
                    raise ValueError('Unsafe fill sample: ' + name)
                for x in range(max(3, x1), min(width - 3, x2)):
                    allowed.add((x, y))
                    result.putpixel((x, y), fill)
        if any(original.getpixel((x, y)) != result.getpixel((x, y))
               for y in range(height) for x in range(width) if (x, y) not in allowed):
            raise ValueError('Artwork outside localized text changed: ' + name)
        stream = io.BytesIO()
        result.save(stream, format='PNG', optimize=False, compress_level=9)
        images[IMAGE_ROOT + name] = stream.getvalue()
    return images, labels


def object_span(text: str, key: str, start: int = 0) -> tuple[int, int]:
    match = re.search(r'"' + re.escape(key) + r'"\s*:\s*\{', text[start:])
    if not match:
        raise ValueError('Object anchor missing: ' + key)
    begin = start + match.end() - 1
    depth = 0
    quoted = escaped = False
    for i in range(begin, len(text)):
        char = text[i]
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if not depth:
                return begin, i + 1
    raise ValueError('Unclosed source object: ' + key)


def config_replacements(source_text: str, spec: dict, labels: dict) -> list[dict]:
    replacements = []
    text = source_text
    def change(old: str, new: str) -> None:
        nonlocal text
        if text.count(old) != 1:
            raise ValueError('Non-unique Mech config anchor: ' + old[:80])
        replacements.append({'old': old, 'new': new, 'expected_count': 1})
        text = text.replace(old, new)
    for name in spec['image_sources']:
        change('"/interface/mechfuel/' + name + '"', '"/' + IMAGE_ROOT + name + '"')
    for button, caption in [('btnUpgrade', 'DOLDUR'), ('btnEmpty', 'BOŞALT')]:
        begin, end = object_span(text, button)
        old = text[begin:end]
        if '"caption"' in old:
            raise ValueError('Source button now has a caption')
        new = '{\n      "caption" : ' + json.dumps(caption, ensure_ascii=False) + ',' + old[1:]
        change(old, new)
    begin, end = object_span(text, 'fuelTypes')
    old = text[begin:end]
    from audit_remaining import parse_jsonc
    types = parse_jsonc(old)
    if set(types) != set(spec['fuel_display_names']):
        raise ValueError('Fuel type keys changed upstream')
    for key, display in spec['fuel_display_names'].items():
        types[key]['displayName'] = display
    change(old, json.dumps(types, ensure_ascii=False, indent=2))
    begin, end = object_span(text, 'gui')
    marker = text[:begin + 1]
    added = ',\n'.join(json.dumps(key) + ': ' + json.dumps(value, ensure_ascii=False)
                        for key, value in labels.items())
    change(marker, marker + '\n' + added + ',\n')
    verify_config(parse_jsonc(source_text), parse_jsonc(text), spec)
    return replacements


def verify_config(original: dict, modified: dict, spec: dict) -> None:
    reverted = copy.deepcopy(modified)
    gui = reverted['gui']
    for key in list(gui):
        if key.startswith('fuTrFuelLegend'):
            del gui[key]
    for button in ('btnUpgrade', 'btnEmpty'):
        del gui[button]['caption']
        for state in ('base', 'hover', 'pressed'):
            gui[button][state] = original['gui'][button][state]
    gui['background']['fileBody'] = original['gui']['background']['fileBody']
    for key in spec['fuel_display_names']:
        if reverted['fuelTypes'][key].pop('displayName') != spec['fuel_display_names'][key]:
            raise ValueError('Fuel display name differs: ' + key)
    if reverted != original:
        raise ValueError('Non-display Mech config changed')
