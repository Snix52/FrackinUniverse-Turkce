"""Load typed validation data; the Python engine contains no asset inventories."""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path

TOOLS = Path(__file__).resolve().parent

@lru_cache(maxsize=None)
def rule(name: str):
    for path in sorted((TOOLS / 'rules').glob('*.json')):
        payload = json.loads(path.read_text(encoding='utf-8'))
        if name not in payload.get('rules', {}):
            continue
        spec = payload['rules'][name]
        kind, value = spec['type'], spec['value']
        if kind == 'set':
            return frozenset(value)
        if kind == 'tuple':
            return tuple(value)
        if kind == 'dict_of_sets':
            return {key: frozenset(items) for key, items in value.items()}
        if kind == 'dict':
            return value
        raise ValueError('Unknown rule type: ' + kind)
    raise ValueError('Missing validation rule: ' + name)


def render_terminology(policy: dict) -> str:
    lines = ['# FU TÜRKÇE Terminoloji Sözlüğü', '',
             '<!-- GENERATED: tools/locked_terms.json; python tools/qa_integrity.py --write-docs -->',
             'Tek kaynak `tools/locked_terms.json` dosyasıdır. Bu tablo doğrudan düzenlenmez.', '',
             'Durumlar: PROPOSED, APPROVED, REVIEW, LOCKED.', '',
             '| Kaynak | Bağlam | Tür | Onaylı Türkçe | Kullanılmayacak | Durum | Not |',
             '|---|---|---|---|---|---|---|']
    for term in policy['terms']:
        lines.append('| ' + ' | '.join(term[k] for k in
                     ('source', 'context', 'type', 'tr', 'forbidden', 'status', 'note')) + ' |')
    lines.extend(['', '## Kural', '',
                  'Oyuncuya gösterilen metinde Türkçe adın yanına İngilizce açıklama eklenmez.',
                  'Belirsiz terimler REVIEW olarak tutulur; kesin karar verilmeden yayılmaz.',
                  'LOCKED kayıtların tam kaynak adları denetlenir. Çok sözcüklü terimlerin bilinen yanlış karşılıkları metin içinde de denetlenir.',
                  '`tr_stem` tanımlı malzeme adlarının Türkçe kökü çekimli cümlelerde de aranır.',
                  'Çekimli serbest metinlerin eksiksiz anlamsal denetimi statik QA kapsamı dışındadır.', ''])
    return '\n'.join(lines)
