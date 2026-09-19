#!/usr/bin/env python3
"""FU TÜRKÇE patch üretim ve statik doğrulama aracı.

Python 3.9+, yalnızca standart kütüphane.
Türkçe Unicode zorunludur; ASCII yedek sürüm bilinçli olarak desteklenmez.
"""
from __future__ import annotations
import argparse, copy, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

COLOR=re.compile(r'\^[^;\s]*;')
CONTROL=re.compile(r'\[[^\]]+\]|<[^>]+>')
NUMBER=re.compile(r'\d+(?:[.,]\d+)?')
ASCII_PAREN=re.compile(r'\([ -~]*[A-Za-z][ -~]*\)')

def tokens(p):
    if not p.startswith('/'): raise ValueError('Geçersiz JSON Pointer: '+p)
    return [x.replace('~1','/').replace('~0','~') for x in p[1:].split('/')]

def read_at(root,p):
    x=root
    for k in tokens(p): x=x[int(k)] if isinstance(x,list) else x[k]
    return x

def replace_at(root,p,v):
    a=tokens(p);x=root
    for k in a[:-1]: x=x[int(k)] if isinstance(x,list) else x[k]
    k=a[-1]
    if isinstance(x,list): x[int(k)]=v
    elif k in x: x[k]=v
    else: raise KeyError(p)

def seed(root,p,v):
    a=tokens(p);x=root
    for i,k in enumerate(a):
        last=i==len(a)-1
        if isinstance(x,list):
            n=int(k)
            while len(x)<=n:x.append(None)
            if last:x[n]=v;return
            if x[n] is None:x[n]=[] if a[i+1].isdigit() else {}
            x=x[n]
        else:
            if last:x[k]=v;return
            if k not in x:x[k]=[] if a[i+1].isdigit() else {}
            x=x[k]

def simulate(root,patch):
    r=copy.deepcopy(root)
    for op in patch:
        if op['op']=='test':
            if read_at(r,op['path'])!=op['value']: raise ValueError('Kaynak uyuşmazlığı: '+op['path'])
        elif op['op']=='replace': replace_at(r,op['path'],op['value'])
        else: raise ValueError('Desteklenmeyen patch işlemi')
    return r

def parse_jsonc(text):
    out=[];i=0;q=False;esc=False
    while i<len(text):
        c=text[i]
        if q:
            out.append(c)
            if esc:esc=False
            elif c=='\\':esc=True
            elif c=='"':q=False
            i+=1;continue
        if c=='"':q=True;out.append(c);i+=1;continue
        if text.startswith('//',i):
            j=text.find('\n',i+2)
            if j<0:break
            out.append('\n');i=j+1;continue
        if text.startswith('/*',i):
            j=text.find('*/',i+2)
            if j<0:raise ValueError('Kapanmamış JSON yorumu')
            out.append(' ');i=j+2;continue
        out.append(c);i+=1
    clean=''.join(out);out=[];i=0;q=False;esc=False
    while i<len(clean):
        c=clean[i]
        if q:
            out.append(c)
            if esc:esc=False
            elif c=='\\':esc=True
            elif c=='"':q=False
            i+=1;continue
        if c=='"':q=True;out.append(c);i+=1;continue
        if c==',':
            j=i+1
            while j<len(clean) and clean[j].isspace():j+=1
            if j<len(clean) and clean[j] in ']}':i+=1;continue
        out.append(c);i+=1
    return json.loads(''.join(out))

def nums(s):
    return Counter(x.replace(',','.') for x in NUMBER.findall(COLOR.sub('',s)))

def allowed(a,p):
    if a=='zb/researchTree/data.config':
        return bool(re.fullmatch(r'/strings/(info/[01]|currencies/(money|essence|fuscienceresource|fumadnessresource|fugeneticmaterial))',p))
    if a=='zb/researchTree/researchTree.config':
        return p in ('/gui/researchButton/caption','/gui/infoList/children/unlocksLabel/value')
    if a in ('zb/researchTree/fu_geology.config','zb/researchTree/fu_agriculture.config','zb/researchTree/fu_chemistry.config','zb/researchTree/fu_engineering.config'):
        tree=PurePosixPath(a).stem
        return p==f'/strings/trees/{tree}' or bool(re.fullmatch(r'/strings/research/[A-Za-z0-9_]+/[01]',p))
    if a.startswith('quests/fu_questlines/tutorial/') and a.endswith('.questtemplate'):
        return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription') or bool(re.fullmatch(r'/scriptConfig/descriptions/[A-Za-z0-9_]+',p))
    if a=='radiomessages/fu_quests.radiomessages':
        return bool(re.fullmatch(r'/[A-Za-z0-9_-]+/text',p))
    if a in ('objects/crafting/matterassembler/prototyper.object','objects/crafting/designlab/designlab.object','objects/crafting/chemlab/chemlab.object'):
        return p in ('/shortdescription','/description') or bool(re.fullmatch(r'/upgradeStages/[012]/(itemSpawnParameters/(description|shortdescription)|interactData/paneLayoutOverride/lbl(Title|SubTitle)/value)',p))
    if a=='objects/crafting/powerstation/powerstation.object':
        return p in ('/shortdescription','/description') or bool(re.fullmatch(r'/upgradeStages/[01]/(itemSpawnParameters/(description|shortdescription)|interactData/paneLayoutOverride/lbl(Title|SubTitle)/value)',p))
    if a=='objects/crafting/sproutingtable/sproutingtable.object':
        return p in ('/description','/subtitle','/shortdescription','/apexDescription','/avianDescription','/floranDescription','/glitchDescription','/humanDescription','/hylotlDescription')
    if a=='objects/crafting/xenostation/xenolab.object':
        return p in ('/description','/subtitle','/shortdescription')
    if a in ('objects/crafting/xenostationadvnew/xenostationadvnew.object','objects/crafting/fu_growingtray/fu_growingtray.object','objects/power/irongrowingtray/irongrowingtray.object','objects/power/isn_hydroponicstray/isn_hydroponicstray.object','objects/bees/beestation/beestation.object','objects/bees/beerefuge/beerefuge.object','items/generic/crafting/precursor/precursorfluid.item','items/generic/crafting/chemlab/aliencompound.item','items/liquids/shadowgasliquid.liqitem','items/generic/crafting/ff_plastic.item','items/generic/crafting/cellmateria.item','items/generic/crafting/chemlab/cell_spliced.item','items/generic/crafting/chemlab/unstableparticles.item','items/generic/crafting/fu_hydrogenmetallic.item','items/generic/crafting/quietusore.item','items/generic/crafting/ammoniumsulfate.item'):
        return p in ('/description','/shortdescription')
    if a=='objects/crafting/handmill/handmill.object':
        return p in ('/category','/description','/shortdescription','/subtitle')
    if a=='interface/windowconfig/beerefuge.config':
        return p in ('/paneLayout/lblTitle/value','/paneLayout/lblSubTitle/value','/paneLayout/lblProduct/value')
    if a in ('items/generic/crafting/matterassembler/ff_focusingarray.item','items/generic/crafting/matterassembler/powercore.item','items/generic/crafting/matterassembler/nuclearcore.item','items/generic/crafting/matterassembler/particlecore.item','objects/crafting/fu_shipcraftingtable/fu_shipcraftingtable.object'):
        return p in ('/description','/shortdescription')
    if a in ('objects/crafting/extractionlab/extractionlab.object','objects/crafting/extractionlabadv/extractionlabadv.object'):
        return p in ('/category','/description','/shortdescription','/subtitle')
    if a in ('objects/crafting/sciencelaptop/sciencelaptop0.object','objects/crafting/sciencelaptop/sciencelaptop1.object','objects/crafting/sciencelaptop/sciencelaptop2.object','objects/crafting/sciencelaptop/dataserver.object','objects/generic/labfurniture/fulargeterminal/fulargeterminal.object'):
        return p in ('/category','/description','/shortdescription')
    if a=='interface/windowconfig/fu_shipcraftingtable.config':
        return p in ('/paneLayout/windowtitle/title','/paneLayout/windowtitle/subtitle','/paneLayout/btnCraft/caption','/paneLayout/btnStopCraft/caption','/paneLayout/lblProduct/value','/paneLayout/filter/hint','/paneLayout/scrollArea/children/itemList/schema/listTemplate/itemName/value')
    if a=='objects/ship/fu_ftldrive/fu_stldrive.object':
        return p in ('/description','/shortdescription','/apexDescription','/avianDescription','/floranDescription','/glitchDescription','/humanDescription','/hylotlDescription','/novakidDescription')
    if a=='items/tools/mmgravgun2.beamaxe':
        return p in ('/description','/shortdescription','/category')
    return False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--catalog',type=Path,default=Path(__file__).with_name('ceviriler.json'))
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--source-dir',type=Path)
    args=ap.parse_args()
    if args.output.exists():ap.error('Çıktı klasörü zaten var.')

    ledger=json.loads(args.catalog.read_text(encoding='utf-8'))
    rows=ledger['translations'];groups=defaultdict(list);seen=set();colorfix=0
    for r in rows:
        a,p=r['asset'],r['pointer']
        if PurePosixPath(a).is_absolute() or '..' in PurePosixPath(a).parts or '\\' in a:raise ValueError('Güvensiz asset yolu: '+a)
        if (a,p) in seen:raise ValueError('Yinelenen alan: '+a+p)
        seen.add((a,p))
        if not allowed(a,p):raise ValueError('Oyuncu metni olmayan alan: '+a+p)
        if 'İngilizce adı:' in r['tr']:raise ValueError('İngilizce fallback/gloss: '+a+p)
        if Counter(COLOR.findall(r['en']))!=Counter(COLOR.findall(r['tr'])):
            if not r.get('qa',{}).get('allow_color_fix'):raise ValueError('Renk kodu uyuşmazlığı: '+a+p)
            colorfix+=1
        if Counter(CONTROL.findall(r['en']))!=Counter(CONTROL.findall(r['tr'])):raise ValueError('Kontrol kodu uyuşmazlığı: '+a+p)
        if nums(r['en'])!=nums(r['tr']):raise ValueError('Sayı uyuşmazlığı: '+a+p)
        groups[a].append(r)

    patches={}
    for a,rs in sorted(groups.items()):
        patch=[{'op':'test','path':r['pointer'],'value':r['en']} for r in rs]
        patch += [{'op':'replace','path':r['pointer'],'value':r['tr']} for r in rs]
        fixture={'__qa_sentinel__':{'id':'unchanged_internal_id','cost':12345,'script':'/unchanged.lua'}}
        for r in rs:seed(fixture,r['pointer'],r['en'])
        result=simulate(fixture,patch)
        for r in rs:
            if read_at(result,r['pointer'])!=r['tr']:raise AssertionError(a+r['pointer'])
        if args.source_dir:
            source=args.source_dir/a
            if not source.is_file():raise FileNotFoundError(source)
            simulate(parse_jsonc(source.read_text(encoding='utf-8-sig')),patch)
        patches[a]=patch

    args.output.mkdir(parents=True)
    mod=args.output/'FU_Turkce';mod.mkdir()
    metadata={'name':'FU_Turkce','friendlyName':'FU Türkçe - Başlangıç, Jeoloji, Tarım, Kimya ve Mühendislik (Beta)',
      'author':'FU TÜRKÇE topluluk yerelleştirmesi; FU: sayter ve katkıda bulunanlar',
      'version':ledger['translation_version'],
      'description':'Kısmi Türkçe yerelleştirme yaması. Tam çeviri değildir; oyun içi LQA, font ve taşma testleri sürüyor.',
      'requires':['FrackinUniverse'],'priority':9000}
    (mod/'_metadata').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a,p in patches.items():
        d=mod/(a+'.patch');d.parent.mkdir(parents=True,exist_ok=True)
        d.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'fields':len(rows),'assets':len(patches),'color_fixes':colorfix,'static_qa':'PASS','in_game_lqa':'NOT TESTED'},ensure_ascii=False))
    return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,KeyError,TypeError,IndexError,OSError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);raise SystemExit(1)
