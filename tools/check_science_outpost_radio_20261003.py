"""Verify every radio ID placed in the pinned Science Outpost map."""
from __future__ import annotations
import argparse
from collections import Counter
from pathlib import Path
import build_validate as build
from plan_translation import digest, read
from write_build_evidence import verify_source

TOOLS=Path(__file__).resolve().parent
MAP='dungeons/other/outpost/scienceoutpost.json'
APPROVED_ROWS_SHA256='a2d0503aeffc6967fa4e7f05096de9745d03c832c5ca4a0ff9423a5a27cb41bd'

def map_messages(data):
    result=Counter()
    def walk(layers):
        for layer in layers:
            walk(layer.get('layers',[]))
            for obj in layer.get('objects',[]):
                properties={p['name']:p['value'] for p in obj.get('properties',[])}
                if properties.get('stagehand')!='radiomessage':continue
                params=build.parse_jsonc(properties['parameters'])
                messages=params.get('radioMessages')
                if messages is None:messages=[params.get('radioMessage')]
                if not isinstance(messages,list) or not messages or any(not isinstance(m,str) or not m for m in messages):
                    raise ValueError('Unresolved outpost radio stagehand: '+str(obj.get('id')))
                result.update(messages)
    walk(data['layers'])
    if not result:raise ValueError('No outpost radio stagehands found')
    return result

def verify_coverage(messages,rows):
    ids={r['pointer'].split('/')[1] for r in rows}
    if ids!=set(messages):
        raise ValueError('Outpost radio coverage gap: '+str(sorted(set(messages)-ids)))

def validate_manifest(manifest,catalog,review):
    rows=manifest['translations']
    keys={(r['asset'],r['pointer']) for r in rows}
    if manifest['translation_version']!='0.71.1-beta' or len(rows)!=15 or len(keys)!=15 or len({r['asset'] for r in rows})!=3:
        raise ValueError('Outpost approved scope drift')
    core=sorted([{k:r[k] for k in ('asset','pointer','en','tr')} for r in rows],key=lambda r:(r['asset'],r['pointer']))
    if digest(core)!=APPROVED_ROWS_SHA256 or manifest['approved_rows_sha256']!=APPROVED_ROWS_SHA256:
        raise ValueError('Outpost approved translation drift')
    if review['status']!='APPROVED_LANGUAGE_AND_SOURCE_PREFLIGHT' or review['approved_rows_sha256']!=APPROVED_ROWS_SHA256:
        raise ValueError('Outpost language approval mismatch')
    if tuple(map(int,catalog['translation_version'].split('-')[0].split('.')))<(0,71,1):
        raise ValueError('Catalog behind outpost fix')
    index={(r['asset'],r['pointer']):r for r in catalog['translations']}
    if len(index)!=len(catalog['translations']):raise ValueError('Duplicate catalog pointer')
    for row in rows:
        expected={'layered_source':True,'source_patch':row['asset']+'.patch'} if row['asset']=='radiomessages/tutorial.radiomessages' else None
        if row.get('qa')!=expected:raise ValueError('Outpost source provenance mismatch')
        current=index.get((row['asset'],row['pointer']))
        if not current or any(current.get(k)!=row.get(k) for k in ('en','tr','qa')):
            raise ValueError('Outpost catalog mismatch')

def validate_source(rows,source):
    cache={}
    for row in rows:
        if row.get('qa',{}).get('layered_source'):
            build.verify_layered_row(row,source,cache)
        else:
            data=build.parse_jsonc((source/row['asset']).read_text(encoding='utf-8-sig'))
            if build.read_at(data,row['pointer'])!=row['en']:
                raise ValueError('Outpost direct source mismatch')
            touched,value=build.source_patch_value(row['asset'],row['pointer'],source,cache)
            if touched and value!=row['en']:raise ValueError('Outpost unreviewed overlay')

def check(source):
    verify_source(source)
    manifest=read(TOOLS/'v0711_translations.json');pin=read(TOOLS/'kaynaklar.json')
    if any(manifest[m]!=pin[p] for m,p in [('source_commit','commit'),('source_repository','repository'),('source_declared_version','declared_version')]):
        raise ValueError('Outpost source pin drift')
    validate_manifest(manifest,read(TOOLS/'ceviriler.json'),read(TOOLS.parent/'docs/reviews/science-outpost-radio-20261003.json'))
    data=build.parse_jsonc((source/MAP).read_text(encoding='utf-8-sig'))
    messages=map_messages(data)
    verify_coverage(messages,manifest['translations'])
    if len(messages)!=15 or sum(messages.values())!=16:raise ValueError('Outpost runtime inventory drift')
    validate_source(manifest['translations'],source)
    return {'message_ids':15,'map_placements':16,'translated_fields':15,'layered_fields':12,'direct_fields':3,'in_game_lqa':'NOT TESTED'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True)
    print('Science Outpost radio source gate PASS:',check(parser.parse_args().source.resolve()))
