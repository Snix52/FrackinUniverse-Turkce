#!/usr/bin/env python3
"""Build/validate a partial Frackin' Universe Turkish localization.

Python 3.9+, standard library only. No paid API, game launch, or installer.
This validates patch generation using an inspected-field ledger. It is NOT an
independent full-source or in-game test. --source-dir adds full local-source checks.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

COLOR = re.compile(r'\^[^;\s]*;')
CONTROL = re.compile(r'\[[^\]]+\]|<[^>]+>')
NUMBER = re.compile(r'\d+(?:\.\d+)?')


def ascii_text(text: str) -> str:
    replacements = str.maketrans({
        'ı':'i', 'İ':'I', 'ğ':'g', 'Ğ':'G', 'ş':'s', 'Ş':'S',
        'ç':'c', 'Ç':'C', 'ö':'o', 'Ö':'O', 'ü':'u', 'Ü':'U',
        '’':"'", '‘':"'", '“':'"', '”':'"', '…':'...',
        '–':'-', '—':'-', '\u00a0':' '
    })
    value = unicodedata.normalize('NFKD', text.translate(replacements))
    value = ''.join(c for c in value if not unicodedata.combining(c))
    if not value.isascii():
        raise ValueError('Unmapped non-ASCII character: '+repr(value))
    return value


def tokens(pointer: str) -> list[str]:
    if not pointer.startswith('/'):
        raise ValueError('Expected a non-root JSON Pointer: '+pointer)
    return [p.replace('~1', '/').replace('~0', '~') for p in pointer[1:].split('/')]


def read_at(root: object, pointer: str) -> object:
    obj = root
    for key in tokens(pointer):
        if isinstance(obj, list):
            obj = obj[int(key)]
        elif isinstance(obj, dict):
            obj = obj[key]
        else:
            raise ValueError('Non-container in pointer: '+pointer)
    return obj


def replace_at(root: object, pointer: str, value: object) -> None:
    parts = tokens(pointer)
    obj = root
    for key in parts[:-1]:
        obj = obj[int(key)] if isinstance(obj, list) else obj[key]
    last = parts[-1]
    if isinstance(obj, list):
        if not 0 <= int(last) < len(obj):
            raise IndexError(pointer)
        obj[int(last)] = value
    elif isinstance(obj, dict) and last in obj:
        obj[last] = value
    else:
        raise KeyError(pointer)


def seed_fixture(root: dict, pointer: str, value: str) -> None:
    """Construct ONLY the inspected leaf paths, not a claimed complete FU asset."""
    parts = tokens(pointer)
    obj = root
    for index, key in enumerate(parts):
        last = index == len(parts)-1
        if isinstance(obj, list):
            n = int(key)
            while len(obj) <= n:
                obj.append(None)
            if last:
                obj[n] = value
                return
            if obj[n] is None:
                obj[n] = [] if parts[index+1].isdigit() else {}
            obj = obj[n]
        else:
            if last:
                obj[key] = value
                return
            if key not in obj:
                obj[key] = [] if parts[index+1].isdigit() else {}
            obj = obj[key]


def simulate_patch(root: object, patch: list[dict]) -> object:
    """Small test/replace evaluator, NOT Starbound engine integration."""
    result = copy.deepcopy(root)
    for op in patch:
        if op['op'] == 'test':
            if read_at(result, op['path']) != op['value']:
                raise ValueError('Source mismatch: '+op['path'])
        elif op['op'] == 'replace':
            replace_at(result, op['path'], op['value'])
        else:
            raise ValueError('Unsupported operation: '+op['op'])
    return result


def allowed(asset: str, ptr: str) -> bool:
    if asset == 'zb/researchTree/data.config':
        return bool(re.fullmatch(r'/strings/(info/[01]|currencies/(money|essence|fuscienceresource|fumadnessresource|fugeneticmaterial))',ptr))
    if asset == 'zb/researchTree/researchTree.config':
        return ptr in ('/gui/researchButton/caption','/gui/infoList/children/unlocksLabel/value')
    if asset == 'zb/researchTree/fu_geology.config':
        return ptr == '/strings/trees/fu_geology' or bool(re.fullmatch(r'/strings/research/[A-Za-z0-9_]+/[01]',ptr))
    if asset.startswith('quests/fu_questlines/tutorial/') and asset.endswith('.questtemplate'):
        return ptr in ('/title','/text','/completionText','/scriptConfig/turnInDescription') or bool(re.fullmatch(r'/scriptConfig/descriptions/[A-Za-z0-9_]+',ptr))
    if asset == 'radiomessages/fu_quests.radiomessages':
        return bool(re.fullmatch(r'/[A-Za-z0-9_-]+/text',ptr))
    if asset == 'objects/crafting/matterassembler/prototyper.object':
        return ptr in ('/shortdescription','/description') or bool(re.fullmatch(r'/upgradeStages/[012]/(itemSpawnParameters/(description|shortdescription)|interactData/paneLayoutOverride/lbl(Title|SubTitle)/value)',ptr))
    return False


def parse_jsonc(text: str) -> object:
    """Strip JSON // and /* */ comments, and trailing commas outside strings."""
    out=[]; i=0; quoted=False; escaped=False
    while i < len(text):
        c=text[i]
        if quoted:
            out.append(c)
            if escaped: escaped=False
            elif c=='\\': escaped=True
            elif c=='"': quoted=False
            i+=1; continue
        if c=='"': quoted=True; out.append(c); i+=1; continue
        if text.startswith('//',i):
            end=text.find('\n',i+2)
            if end < 0: break
            out.append('\n'); i=end+1; continue
        if text.startswith('/*',i):
            end=text.find('*/',i+2)
            if end < 0: raise ValueError('Unterminated JSON comment')
            out.append(' '); i=end+2; continue
        out.append(c); i+=1
    clean=''.join(out); out=[]; i=0; quoted=False; escaped=False
    while i < len(clean):
        c=clean[i]
        if quoted:
            out.append(c)
            if escaped: escaped=False
            elif c=='\\': escaped=True
            elif c=='"': quoted=False
            i+=1; continue
        if c=='"': quoted=True; out.append(c); i+=1; continue
        if c==',':
            j=i+1
            while j<len(clean) and clean[j].isspace(): j+=1
            if j<len(clean) and clean[j] in ']}': i+=1; continue
        out.append(c); i+=1
    return json.loads(''.join(out))


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--catalog', type=Path, default=Path(__file__).with_name('ceviriler.json'))
    ap.add_argument('--output', type=Path, required=True, help='A NEW output folder; never point this at FU itself.')
    ap.add_argument('--ascii', action='store_true', help='Only target Turkish text is transliterated.')
    ap.add_argument('--source-dir',type=Path, help='Optional unpacked FU source directory. Does not modify source.')
    args=ap.parse_args()
    if args.output.exists():
        ap.error('Output already exists; choose a new directory. Nothing was overwritten.')
    if args.source_dir and (args.output.resolve()==args.source_dir.resolve() or args.source_dir.resolve() in args.output.resolve().parents):
        ap.error('Output must be separate from source-dir.')
    ledger=json.loads(args.catalog.read_text(encoding='utf-8'))
    rows=ledger['translations']; groups=defaultdict(list); seen=set()
    for r in rows:
        a,p=r['asset'],r['pointer']
        if PurePosixPath(a).is_absolute() or '..' in PurePosixPath(a).parts or '\\' in a:
            raise ValueError('Unsafe asset path: '+a)
        if (a,p) in seen: raise ValueError('Duplicate field: '+a+p)
        seen.add((a,p))
        if not allowed(a,p): raise ValueError('Non-display field: '+a+p)
        if not isinstance(r['en'],str) or not isinstance(r['tr'],str): raise TypeError(a+p)
        for pattern,name in ((COLOR,'color'),(CONTROL,'control')):
            if Counter(pattern.findall(r['en'])) != Counter(pattern.findall(r['tr'])):
                raise ValueError(name+' token mismatch: '+a+p)
        if Counter(NUMBER.findall(COLOR.sub('',r['en']))) != Counter(NUMBER.findall(COLOR.sub('',r['tr']))):
            raise ValueError('Numeric token mismatch: '+a+p)
        if r['en']==r['tr']: raise ValueError('Unchanged translation: '+a+p)
        groups[a].append(r)
    patches={}; details=[]; mismatches=[]
    for a,rs in sorted(groups.items()):
        targets=[ascii_text(r['tr']) if args.ascii else r['tr'] for r in rs]
        # Every guard precedes every replacement. A stale asset is not partly altered.
        patch=[{'op':'test','path':r['pointer'],'value':r['en']} for r in rs]
        patch += [{'op':'replace','path':r['pointer'],'value':tr} for r,tr in zip(rs,targets)]
        patch=json.loads(json.dumps(patch,ensure_ascii=False))
        fixture={'__qa_sentinel__':{'id':'unchanged_internal_id','cost':12345,'script':'/unchanged.lua'}}
        for r in rs: seed_fixture(fixture,r['pointer'],r['en'])
        result=simulate_patch(fixture,patch)
        for r,tr in zip(rs,targets):
            if read_at(result,r['pointer']) != tr: raise AssertionError(a+r['pointer'])
        if result['__qa_sentinel__'] != fixture['__qa_sentinel__']: raise AssertionError('Sentinel mutated')
        # Every possible one-field mismatch must fail, leaving the input untouched.
        for r in rs:
            mutated=copy.deepcopy(fixture)
            replace_at(mutated,r['pointer'],r['en']+' [SOURCE_CHANGED]')
            before=copy.deepcopy(mutated)
            try: simulate_patch(mutated,patch)
            except ValueError: pass
            else: raise AssertionError('Mismatch not rejected: '+a+r['pointer'])
            if mutated != before: raise AssertionError('Input mutated on failure')
        verified_local=False
        if args.source_dir:
            path=args.source_dir/a
            if not path.is_file(): mismatches.append({'asset':a,'reason':'Source file missing'})
            else:
                try:
                    original=parse_jsonc(path.read_text(encoding='utf-8-sig'))
                    simulate_patch(original,patch)
                    verified_local=True
                except (ValueError,KeyError,TypeError,IndexError) as exc:
                    mismatches.append({'asset':a,'reason':str(exc)})
        patches[a]=patch
        details.append({'asset':a,'translated_fields':len(rs),'guard_tests':len(rs),'fixture_check':'PASS',
                        'local_full_source_verified':verified_local})
    if mismatches:
        print(json.dumps({'source_check':'FAIL','mismatches':mismatches},ensure_ascii=False,indent=2),file=sys.stderr)
        return 2
    args.output.mkdir(parents=True)
    mod=args.output/'FU_Turkce'; mod.mkdir()
    metadata={
        'name':'FU_Turkce',
        'friendlyName':'FU Turkce - Baslangic ve Jeoloji (Beta)',
        'author':'ChatGPT destekli Turkce ceviri; FU: sayter ve katkida bulunanlar',
        'version':ledger['translation_version']+('-ascii' if args.ascii else ''),
        'description':'Partial Turkish text patch. NOT a full translation. Not tested in-game. No font included.',
        'requires':['FrackinUniverse'],
        'priority':9000
    }
    (mod/'_metadata').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a,patch in patches.items():
        dest=mod/(a+'.patch');dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(patch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={
        'translation_version':metadata['version'],
        'source_repository':ledger['source_repository'],
        'source_commit':ledger['source_commit'],
        'source_declared_version':ledger['source_declared_version'],
        'variant':'ASCII target text' if args.ascii else 'Turkish Unicode',
        'translated_display_fields':len(rows),'patched_assets':len(patches),
        'categories':dict(Counter(r['section'] for r in rows)),
        'checks':{'unique_paths':'PASS','display_field_allowlist':'PASS','valid_json':'PASS',
                  'color_token_multisets':'PASS','control_token_multisets':'PASS','numeric_token_multisets':'PASS',
                  'fixture_application':'PASS','unchanged_fixture_sentinel':'PASS',
                  'source_mismatch_rejection_cases':len(rows),'source_mismatch_rejection':'PASS'},
        'full_source_validation': 'PASS (local supplied files)' if args.source_dir else 'NOT PERFORMED; checked against inspected-field ledger only',
        'in_game_test':'NOT PERFORMED',
        'font_and_visual_layout_test':'NOT PERFORMED',
        'compatibility_with_user_workshop_build':'NOT VERIFIED',
        'important':'Per-asset guards: if ANY guarded English field differs, this entire asset patch is skipped. No promise of all future-version compatibility.',
        'assets':details,
        'catalog_sha256':hashlib.sha256(args.catalog.read_bytes()).hexdigest()
    }
    (args.output/'test_raporu.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'output':str(args.output),'fields':len(rows),'assets':len(patches),'static_checks':'PASS','in_game':'NOT TESTED'},ensure_ascii=False))
    return 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (ValueError,KeyError,TypeError,IndexError,OSError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
