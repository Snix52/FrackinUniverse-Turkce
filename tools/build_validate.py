#!/usr/bin/env python3
"""FU TÜRKÇE patch üretim ve statik doğrulama aracı.

Python 3.11+, yalnızca standart kütüphane.
Türkçe Unicode zorunludur; ASCII yedek sürüm bilinçli olarak desteklenmez.
"""
from __future__ import annotations
import argparse, copy, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from rule_data import rule as load_rule
from qa_integrity import validate_project
from qa_raw import verify_source_blob, validate_manifest_pin
from write_build_evidence import verify_source, record_validation

COLOR=re.compile(r'\^[^;\s]*;')
CONTROL=re.compile(r'\[(?![^\]]*\^)[^\]]+\]|<[^>]+>')
NUMBER=re.compile(r'\d+(?:[.,]\d+)?')
SIGNED_NUMBER=re.compile(r'[+-]\s*%?\s*\d+(?:[.,]\d+)?')
ICON=re.compile(r'[\uE000-\uF8FF]')
PRINTF=re.compile(r'%(?:\d+\$)?[-+0#]*(?:\d+|\*)?(?:\.\d+|\.\*)?(?:hh|h|ll|l|L|z|j|t)?[diuoxXfFeEgGaAcspn%]')
BRACE_PLACEHOLDER=re.compile(r'\{(?:\d+|[A-Za-z_][A-Za-z0-9_.:-]*)\}')
DOLLAR_PLACEHOLDER=re.compile(r'\$(?:\{[A-Za-z_][A-Za-z0-9_.:-]*\}|[A-Za-z_][A-Za-z0-9_.:-]*)')
ASCII_PAREN=re.compile(r'\([ -~]*[A-Za-z][ -~]*\)')
LOWERCASE_MECH=re.compile(r'\bmech\b')

# Geriye dönük LQA'da yakalanan ve tekrar projeye sızmaması gereken Türkçe hatalar.
BAD_TR_PATTERNS = load_rule('BAD_TR_PATTERNS')

# FU 6.5.8 pinned kaynağında strings.research altında dursa da aktif researchTree
# düğümüne bağlı olmayan metinler. Oyuncuya görünmedikleri için yamaya alınmaz.
NONVISIBLE_QUEST_ASSETS = load_rule('NONVISIBLE_QUEST_ASSETS')

SCIENCE_EXTERNAL_QUEST_ASSETS = load_rule('SCIENCE_EXTERNAL_QUEST_ASSETS')

# v0.18: objects/power, objects/bees ve objects/scienceoutpost altındaki 57
# aday runtime tarifleri, araştırma düğümleri, dükkânlar ve Tiled yerleşimleriyle
# denetlendi. Aşağıdaki 47 asset gerçekten erişilebilir; kalan 10 asset bilinçli
# olarak dışarıda tutulur.
V018_OBJECT_ASSETS = load_rule('V018_OBJECT_ASSETS')

V018_DEAD_OBJECT_ASSETS = load_rule('V018_DEAD_OBJECT_ASSETS')

V018_CHAT_OPTION_ASSETS = load_rule('V018_CHAT_OPTION_ASSETS')

# v0.19: items/generic/crafting altındaki daha önce kapsanmayan 261 adayın
# runtime bağlantıları denetlendi. 235 etkin asset yalnızca envanter adı ve
# açıklama alanlarıyla kapsanır. Aşağıdaki 26 asset etkin tarif/ganimet/görev
# akışına bağlı değildir ya da yalnız deprecated kayıt temizliği içindir.
V019_DEAD_CRAFTING_ITEM_ASSETS = load_rule('V019_DEAD_CRAFTING_ITEM_ASSETS')

# v0.20: FU ana görev aileleri dışındaki 97 questtemplate adayı runtime
# başlangıçları, pickupQuestTemplates, NPC offeredQuests, SAIL görevleri,
# Tiled yerleşimleri ve görev ödülleri üzerinden denetlendi. Aşağıdaki 29
# görev oyuncuya gerçekten ulaşır; yalnızca görünür görev metni alanları
# yerelleştirilir.
V020_ACTIVE_QUEST_ASSETS = load_rule('V020_ACTIVE_QUEST_ASSETS')

# Kaynakta bulunmasına rağmen normal oyuncu akışına bağlı olmayan v0.20
# adayları. Optional Hardmode'un başlangıcı NPC dosyasında devre dışıdır;
# çoğu eski teknoloji görevi techshop tarafından başlatılmaz; görünmez
# takip/fix görevleri de oyuncu metni üretmez.
V020_INACTIVE_QUEST_ASSETS = load_rule('V020_INACTIVE_QUEST_ASSETS')

# Aktif fu_warcraft ağacındaki bonegear, irongear, telebriumgear ve
# tungstengear düğümlerinin açtığı; gerçek üretim tarifi bulunan v0.21
# erken oyun silahları. Önceden kapsanan 3 asset kendi eski allowlist'inde
# kalır; burada yalnız v0.21'de eklenen 121 asset bulunur.
V021_EARLY_WEAPON_ASSETS = load_rule('V021_EARLY_WEAPON_ASSETS')

# Aktif fu_warcraft ağacındaki Kademe 1-2 zırh kollarının açtığı,
# gerçek üretim tarifi bulunan v0.25 zırh parçaları. EPP düğümleri ayrı
# sistem olarak sonraki kapsama bırakılmıştır. Burada 114 yeni asset vardır.
V025_EARLY_ARMOR_ASSETS = load_rule('V025_EARLY_ARMOR_ASSETS')

# Aktif fu_warcraft ağacındaki yedi Kademe 5 kolunun açtığı ve gerçek
# üretim tarifi bulunan v0.29 zırh parçaları. Runtime araştırma/tarif
# zinciri esas olduğu için kaynak yolu tier4 veya tier6 olan parçalar da vardır.
V029_TIER5_ARMOR_ASSETS = load_rule('V029_TIER5_ARMOR_ASSETS')

# v0.30: etkin fu_warcraft düğümü + gerçek tarif çıktısı + görünür ekipman
# kesişiminde kalan 413 asset. Yol listesi çeviri manifestinde tek kaynak olarak
# tutulur; yalnız ad ve açıklama alanlarına izin verilir.
_V030_MANIFEST = json.loads(
    Path(__file__).with_name('v030_translations.json').read_text(encoding='utf-8')
)
V030_RESEARCH_GEAR_ASSETS = {spec['asset'] for spec in _V030_MANIFEST.values()}
if len(_V030_MANIFEST) != 413 or len(V030_RESEARCH_GEAR_ASSETS) != 413:
    raise ValueError('v0.30 ekipman manifesti 413 benzersiz asset içermeli')

_V031_MANIFEST = json.loads(
    Path(__file__).with_name('v031_translations.json').read_text(encoding='utf-8')
)
V031_SAIL_UI_FIELDS = {(row['asset'], row['pointer']) for row in _V031_MANIFEST['translations']}
if len(V031_SAIL_UI_FIELDS) != len(_V031_MANIFEST['translations']):
    raise ValueError('v0.31 SAIL manifestinde yinelenen alan var')

_V0311_MANIFEST = json.loads(
    Path(__file__).with_name('v0311_translations.json').read_text(encoding='utf-8')
)
V0311_QUEST_UI_FIELDS = {(row['asset'], row['pointer']) for row in _V0311_MANIFEST['translations']}
if len(V0311_QUEST_UI_FIELDS) != len(_V0311_MANIFEST['translations']):
    raise ValueError('v0.31.1 Görev Terminali manifestinde yinelenen alan var')

_V0312_MANIFEST = json.loads(
    Path(__file__).with_name('v0312_translations.json').read_text(encoding='utf-8')
)
V0312_RESEARCH_UI_FIELDS = {(row['asset'], row['pointer']) for row in _V0312_MANIFEST['translations']}
if len(V0312_RESEARCH_UI_FIELDS) != len(_V0312_MANIFEST['translations']):
    raise ValueError('v0.31.2 araştırma arayüzü manifestinde yinelenen alan var')

_V032_MANIFEST = json.loads(
    Path(__file__).with_name('v032_translations.json').read_text(encoding='utf-8')
)
V032_MACHINE_UI_FIELDS = {(row['asset'], row['pointer']) for row in _V032_MANIFEST['translations']}
if len(V032_MACHINE_UI_FIELDS) != len(_V032_MANIFEST['translations']):
    raise ValueError('v0.32 makine/üretim arayüzü manifestinde yinelenen alan var')

_V033_MANIFEST = json.loads(
    Path(__file__).with_name('v033_translations.json').read_text(encoding='utf-8')
)
V033_COCKPIT_UI_FIELDS = {(row['asset'], row['pointer']) for row in _V033_MANIFEST['translations']}
if len(V033_COCKPIT_UI_FIELDS) != len(_V033_MANIFEST['translations']):
    raise ValueError('v0.33 cockpit/navigasyon manifestinde yinelenen alan var')

_V034_MANIFEST = json.loads(
    Path(__file__).with_name('v034_translations.json').read_text(encoding='utf-8')
)
V034_COCKPIT_DESCRIPTION_FIELDS = {(row['asset'], row['pointer']) for row in _V034_MANIFEST['translations']}
if len(V034_COCKPIT_DESCRIPTION_FIELDS) != len(_V034_MANIFEST['translations']):
    raise ValueError('v0.34 cockpit açıklama manifestinde yinelenen alan var')

_V035_MANIFEST = json.loads(
    Path(__file__).with_name('v035_translations.json').read_text(encoding='utf-8')
)
V035_MATMOD_UI_FIELDS = {(row['asset'], row['pointer']) for row in _V035_MANIFEST['translations']}
if len(V035_MATMOD_UI_FIELDS) != len(_V035_MANIFEST['translations']):
    raise ValueError('v0.35 malzeme modu arayüzü manifestinde yinelenen alan var')

_V036_MANIFEST = json.loads(
    Path(__file__).with_name('v036_translations.json').read_text(encoding='utf-8')
)
V036_SHIP_NAMEPLATE_FIELDS = {(row['asset'], row['pointer']) for row in _V036_MANIFEST['translations']}
if len(V036_SHIP_NAMEPLATE_FIELDS) != len(_V036_MANIFEST['translations']):
    raise ValueError('v0.36 gemi isim plakası manifestinde yinelenen alan var')

_V037_MANIFEST = json.loads(
    Path(__file__).with_name('v037_translations.json').read_text(encoding='utf-8')
)
V037_KHEAA_ROUTER_FIELDS = {(row['asset'], row['pointer']) for row in _V037_MANIFEST['translations']}
if len(V037_KHEAA_ROUTER_FIELDS) != len(_V037_MANIFEST['translations']):
    raise ValueError('v0.37 KheAA yönlendirici manifestinde yinelenen alan var')

_V038_MANIFEST = json.loads(
    Path(__file__).with_name('v038_translations.json').read_text(encoding='utf-8')
)
V038_EXTRA_STATS_FIELDS = {(row['asset'], row['pointer']) for row in _V038_MANIFEST['translations']}
if len(V038_EXTRA_STATS_FIELDS) != len(_V038_MANIFEST['translations']):
    raise ValueError('v0.38 gelişmiş istatistikler manifestinde yinelenen alan var')

_V039_MANIFEST = json.loads(
    Path(__file__).with_name('v039_translations.json').read_text(encoding='utf-8')
)
V039_STAT_WINDOW_FIELDS = {(row['asset'], row['pointer']) for row in _V039_MANIFEST['translations']}
if len(V039_STAT_WINDOW_FIELDS) != len(_V039_MANIFEST['translations']):
    raise ValueError('v0.39 ana Tricorder manifestinde yinelenen alan var')

_V040_MANIFEST = json.loads(
    Path(__file__).with_name('v040_translations.json').read_text(encoding='utf-8')
)
V040_CHAR_CREATION_FIELDS = {(row['asset'], row['pointer']) for row in _V040_MANIFEST['translations']}
if len(V040_CHAR_CREATION_FIELDS) != len(_V040_MANIFEST['translations']):
    raise ValueError('v0.40 karakter oluşturma manifestinde yinelenen alan var')

_V041_MANIFEST = json.loads(
    Path(__file__).with_name('v041_translations.json').read_text(encoding='utf-8')
)
V041_SPACE_STATION_FIELDS = {(row['asset'], row['pointer']) for row in _V041_MANIFEST['translations']}
if len(V041_SPACE_STATION_FIELDS) != len(_V041_MANIFEST['translations']):
    raise ValueError('v0.41 Space Station manifestinde yinelenen alan var')

_V042_MANIFEST = json.loads(
    Path(__file__).with_name('v042_translations.json').read_text(encoding='utf-8')
)
V042_FUNCTIONAL_UI_FIELDS = {(row['asset'], row['pointer']) for row in _V042_MANIFEST['translations']}
if len(V042_FUNCTIONAL_UI_FIELDS) != len(_V042_MANIFEST['translations']):
    raise ValueError('v0.42 işlevsel arayüz manifestinde yinelenen alan var')

_V043_MANIFEST = json.loads(
    Path(__file__).with_name('v043_translations.json').read_text(encoding='utf-8')
)
V043_LIVE_UI_FIELDS = {(row['asset'], row['pointer']) for row in _V043_MANIFEST['translations']}
if len(V043_LIVE_UI_FIELDS) != len(_V043_MANIFEST['translations']):
    raise ValueError('v0.43 canlı arayüz manifestinde yinelenen alan var')

_V044_MANIFEST = json.loads(
    Path(__file__).with_name('v044_translations.json').read_text(encoding='utf-8')
)
V044_FINAL_UI_FIELDS = {(row['asset'], row['pointer']) for row in _V044_MANIFEST['translations']}
if len(V044_FINAL_UI_FIELDS) != len(_V044_MANIFEST['translations']):
    raise ValueError('v0.44 arayüz kapanış manifestinde yinelenen alan var')

_V045_MANIFEST = json.loads(
    Path(__file__).with_name('v045_translations.json').read_text(encoding='utf-8')
)
V045_QUEST_PATCH_FIELDS = {(row['asset'], row['pointer']) for row in _V045_MANIFEST['translations']}
if len(V045_QUEST_PATCH_FIELDS) != len(_V045_MANIFEST['translations']):
    raise ValueError('v0.45 görev kapanış manifestinde yinelenen alan var')

_V046_MANIFEST = json.loads(
    Path(__file__).with_name('v046_translations.json').read_text(encoding='utf-8')
)
V046_RACES_SAIL_FIELDS = {
    (row['asset'], row['pointer']) for row in _V046_MANIFEST['translations']
}
if len(V046_RACES_SAIL_FIELDS) != len(_V046_MANIFEST['translations']):
    raise ValueError('v0.46 Irklar/SAIL manifestinde yinelenen alan var')

_V047_MANIFEST = json.loads(
    Path(__file__).with_name('v047_translations.json').read_text(encoding='utf-8')
)
V047_PLANT_FIELDS = {
    (row['asset'], row['pointer']) for row in _V047_MANIFEST['translations']
}
if len(V047_PLANT_FIELDS) != len(_V047_MANIFEST['translations']):
    raise ValueError('v0.47 bitki manifestinde yinelenen alan var')

_V048_MANIFEST = json.loads(
    Path(__file__).with_name('v048_translations.json').read_text(encoding='utf-8')
)
V048_WOOD_TILE_FIELDS = {
    (row['asset'], row['pointer']) for row in _V048_MANIFEST['translations']
}
if len(V048_WOOD_TILE_FIELDS) != len(_V048_MANIFEST['translations']):
    raise ValueError('v0.48 ahşap yapı malzemesi manifestinde yinelenen alan var')

_V049_MANIFEST = json.loads(
    Path(__file__).with_name('v049_translations.json').read_text(encoding='utf-8')
)
V049_WOOD_MATERIAL_FIELDS = {
    (row['asset'], row['pointer']) for row in _V049_MANIFEST['translations']
}
if len(V049_WOOD_MATERIAL_FIELDS) != len(_V049_MANIFEST['translations']):
    raise ValueError('v0.49 ahşap malzeme manifestinde yinelenen alan var')

# Aktif fu_warcraft ağacındaki yedi Kademe 5 savaş ekipmanı kolunun
# gerçek üretim tarifi bulunan v0.28 assetleri. Ferozium Satırı önceki
# Battle paketinde çevrildiği için burada 96 yeni asset vardır.
V028_TIER5_COMBAT_ASSETS = load_rule('V028_TIER5_COMBAT_ASSETS')

# Aktif fu_warcraft ağacındaki yedi Kademe 4 zırh kolunun açtığı ve
# gerçek üretim tarifi bulunan v0.27 zırh parçaları. Dosya yolu tier5
# olsa da Cute seti bu Kademe 4 araştırma/tarif zincirinden açılır.
V027_TIER4_ARMOR_ASSETS = load_rule('V027_TIER4_ARMOR_ASSETS')

# Aktif fu_warcraft ağacındaki altı Kademe 3 zırh kolunun açtığı,
# gerçek üretim tarifi bulunan v0.26 zırh parçaları. Mutavisk miğferi
# önceki Science paketinde çevrildiği için burada 75 yeni asset vardır.
V026_TIER3_ARMOR_ASSETS = load_rule('V026_TIER3_ARMOR_ASSETS')

# Aktif fu_warcraft ağacındaki irradiumgear, triangliumgear, prisilitegear,
# quietusgear ve bioweaponsgear düğümlerinin açtığı, gerçek üretim tarifi
# bulunan v0.24 Kademe 4 savaş ekipmanı. Burada 148 yeni asset vardır.
V024_TIER4_REMAINING_COMBAT_ASSETS = load_rule('V024_TIER4_REMAINING_COMBAT_ASSETS')

# Aktif fu_warcraft ağacındaki advancealloygear ve durasteelgear
# düğümlerinin açtığı, gerçek üretim tarifi bulunan v0.23 Kademe 4
# çekirdek savaş ekipmanı. Burada 48 yeni asset vardır.
V023_TIER4_CORE_COMBAT_ASSETS = load_rule('V023_TIER4_CORE_COMBAT_ASSETS')

# Aktif fu_warcraft ağacındaki altı Kademe 3 düğümünün açtığı ve gerçek
# üretim tarifi bulunan v0.22 savaş ekipmanı. Daha önce çevrilen
# energyassault kendi eski allowlist'inde kalır; burada 157 yeni asset vardır.
V022_TIER3_COMBAT_ASSETS = load_rule('V022_TIER3_COMBAT_ASSETS')

# v0.22 görev metninde Usta Manipülatör olarak anılan iki erişilebilir
# eşyanın oyuncuya gösterilen alanları. Kırık augment Khe görevinden gelir;
# tamamlanmış araç da Nanoüretici tarifinin gerçek çıktısıdır.
V022_MASTER_MANIPULATOR_ASSETS = load_rule('V022_MASTER_MANIPULATOR_ASSETS')

def v021_weapon_pointer(p):
    return p in ('/shortdescription','/description')

def v020_quest_pointer(p):
    return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription')

def v019_crafting_item(a,p):
    return (a.startswith('items/generic/crafting/')
            and (a.endswith('.item') or a.endswith('.consumable'))
            and p in ('/shortdescription','/description'))

def v018_object_pointer(a,p):
    if p in ('/shortdescription','/description','/subtitle'):
        return True
    if re.fullmatch(r'/[A-Za-z0-9_]+Description',p):
        return True
    if re.fullmatch(r'/interactData/paneLayoutOverride/(windowtitle/(title|subtitle)|lbl(Title|SubTitle)/value)',p):
        return True
    if a=='objects/power/fu_rockcrusher/fu_rockcrusher.object' and p=='/category':
        return True
    if a=='objects/power/fu_rechargesensor/fu_rechargesensor.object':
        return bool(re.fullmatch(r'/chatStrings/(noBatteries|tooltip|statusOn|statusOff)',p))
    if a=='objects/power/fu_weatherbeacon/fu_weatherbeacon.object':
        return bool(re.fullmatch(r'/chatStrings/(solarPanel|solarArray|solarTower|nocturnArray|windTurbine)',p))
    if a in V018_CHAT_OPTION_ASSETS:
        return bool(re.fullmatch(r'/chatOptions/\d+',p))
    return False

OUTPOST_SHOP_QUEST_ASSETS = load_rule('OUTPOST_SHOP_QUEST_ASSETS')

NONVISIBLE_RESEARCH_IDS = load_rule('NONVISIBLE_RESEARCH_IDS')

# v0.17: objects/crafting ağacındaki daha önce çevrilmemiş etkin üretim nesneleri.
V017_CRAFTING_ASSETS = load_rule('V017_CRAFTING_ASSETS')

def v017_crafting_pointer(p):
    if p in ('/shortdescription','/description','/subtitle','/category'):
        return True
    if re.fullmatch(r'/[A-Za-z0-9_]+Description',p):
        return True
    if re.fullmatch(r'/interactData/paneLayoutOverride/(windowtitle/(title|subtitle)|lbl(Title|SubTitle)/value)',p):
        return True
    return bool(re.fullmatch(r'/upgradeStages/\d+/(itemSpawnParameters/(shortdescription|description|subtitle|[A-Za-z0-9_]+Description)|interactData/paneLayoutOverride/(windowtitle/(title|subtitle)|lbl(Title|SubTitle)/value))',p))

def nonvisible_research_pointer(a,p):
    m=re.fullmatch(r'/strings/research/([^/]+)/[01]',p)
    return bool(m and m.group(1) in NONVISIBLE_RESEARCH_IDS.get(a,set()))

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

def verify_layered_row(row, source_dir, cache):
    """Check every FU-owned patch value, including recorded vanilla array appends."""
    asset, pointer = row['asset'], row['pointer']
    source_patch = row.get('qa', {}).get('source_patch')
    if source_patch != asset + '.patch':
        raise ValueError('Invalid layered source patch: ' + asset + pointer)
    if source_patch not in cache:
        cache[source_patch] = parse_jsonc((source_dir/source_patch).read_text(encoding='utf-8-sig'))
    operations = cache[source_patch]
    if not isinstance(operations, list):
        raise ValueError('Unsupported layered source patch: ' + source_patch)
    missing = object()
    found = missing
    append_index = load_rule('AUDIT_PATCH_APPEND_INDEXES').get(asset)
    for op in operations:
        if not isinstance(op, dict):
            raise ValueError('Conditional layered source needs explicit verification: ' + source_patch)
        if op.get('op') == 'test':
            continue
        parts = tokens(op.get('path', ''))
        if '-' in parts and append_index is not None:
            parts = [str(append_index) if part == '-' else part for part in parts]
        target = tokens(pointer)
        if target[:len(parts)] != parts:
            continue
        found = missing  # A later parent replacement/removal invalidates earlier values.
        if op.get('op') in ('add', 'replace') and 'value' in op:
            try:
                found = op['value']
                for part in target[len(parts):]:
                    found = found[int(part)] if isinstance(found, list) else found[part]
            except (KeyError, IndexError, TypeError, ValueError):
                found = missing
    if found != row['en']:
        raise ValueError('Layered source mismatch: ' + asset + pointer)

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
    # Starbound bazı assetlerde alıntılı metinlerin içinde ham satır sonlarına
    # izin veriyor; strict=False bu motor-tarafı biçimi kaynak kilidiyle okur.
    return json.loads(''.join(out),strict=False)

def nums(s):
    return Counter(x.replace(',','.') for x in NUMBER.findall(COLOR.sub('',s)))

def signed_nums(s):
    return Counter(x.replace(' ','').replace('%','').replace(',','.') for x in SIGNED_NUMBER.findall(COLOR.sub('',s)))

def allowed(a,p):
    if (a,p) in V049_WOOD_MATERIAL_FIELDS:
        return True
    if (a,p) in V048_WOOD_TILE_FIELDS:
        return True
    if (a,p) in V047_PLANT_FIELDS:
        return True
    if (a,p) in V046_RACES_SAIL_FIELDS:
        return True
    if (a,p) in V045_QUEST_PATCH_FIELDS:
        return True
    if (a,p) in V044_FINAL_UI_FIELDS:
        return True
    if (a,p) in V043_LIVE_UI_FIELDS:
        return True
    if (a,p) in V042_FUNCTIONAL_UI_FIELDS:
        return True
    if (a,p) in V041_SPACE_STATION_FIELDS:
        return True
    if (a,p) in V040_CHAR_CREATION_FIELDS:
        return True
    if (a,p) in V039_STAT_WINDOW_FIELDS:
        return True
    if (a,p) in V038_EXTRA_STATS_FIELDS:
        return True
    if (a,p) in V037_KHEAA_ROUTER_FIELDS:
        return True
    if (a,p) in V036_SHIP_NAMEPLATE_FIELDS:
        return True
    if (a,p) in V035_MATMOD_UI_FIELDS:
        return True
    if (a,p) in V034_COCKPIT_DESCRIPTION_FIELDS:
        return True
    if (a,p) in V033_COCKPIT_UI_FIELDS:
        return True
    if (a,p) in V032_MACHINE_UI_FIELDS:
        return True
    if (a,p) in V0312_RESEARCH_UI_FIELDS:
        return True
    if (a,p) in V0311_QUEST_UI_FIELDS:
        return True
    if (a,p) in V031_SAIL_UI_FIELDS:
        return True
    if a in V030_RESEARCH_GEAR_ASSETS:
        return p in ('/shortdescription','/description')
    if a in V029_TIER5_ARMOR_ASSETS:
        return p in ('/shortdescription','/description')
    if a in V028_TIER5_COMBAT_ASSETS:
        return p in ('/shortdescription','/description')
    if a in V027_TIER4_ARMOR_ASSETS:
        return p in ('/shortdescription','/description')
    if a in V026_TIER3_ARMOR_ASSETS:
        return p in ('/shortdescription','/description')
    if a in V025_EARLY_ARMOR_ASSETS:
        return p in ('/shortdescription','/description')
    if a in V024_TIER4_REMAINING_COMBAT_ASSETS:
        return p in ('/shortdescription','/description')
    if a in V023_TIER4_CORE_COMBAT_ASSETS:
        return p in ('/shortdescription','/description')
    if a in V022_TIER3_COMBAT_ASSETS:
        return p in ('/shortdescription','/description')
    if a in V022_MASTER_MANIPULATOR_ASSETS:
        if a=='items/augments/quest/humanartifact.augment':
            return p in ('/shortdescription','/description','/augment/displayName')
        return p in ('/shortdescription','/description')
    if a in V021_EARLY_WEAPON_ASSETS:
        return v021_weapon_pointer(p)
    if a in V020_ACTIVE_QUEST_ASSETS:
        return v020_quest_pointer(p)
    if v019_crafting_item(a,p):
        return True
    if a in V018_OBJECT_ASSETS:
        return v018_object_pointer(a,p)
    if a in V017_CRAFTING_ASSETS:
        return v017_crafting_pointer(p)
    if a=='zb/researchTree/data.config':
        return bool(re.fullmatch(r'/strings/(info/[01]|currencies/(money|essence|fuscienceresource|fumadnessresource|fugeneticmaterial))',p))
    if a=='zb/researchTree/researchTree.config':
        return p in ('/gui/researchButton/caption','/gui/infoList/children/unlocksLabel/value','/gui/title/value','/gui/consumptionText/value')
    if a=='zb/questList/data.config':
        return p in ('/strings/questlines/fu_sciences/title','/strings/questlines/fu_sciences/description','/strings/questlines/fu_kevin_tasks/title','/strings/questlines/fu_kevin_tasks/description','/strings/sublines/fu_kevin','/strings/questlines/fu_battle/title','/strings/questlines/fu_battle/description','/strings/sublines/fu_monsters','/strings/sublines/fu_gear','/strings/questlines/fu_byos/title','/strings/questlines/fu_byos/description','/strings/sublines/fu_byosbasics') or bool(re.fullmatch(r'/strings/sublines/fu_(physics|chemistry|electronics|genetics|mechanical)',p))
    if a in ('zb/researchTree/fu_geology.config','zb/researchTree/fu_agriculture.config','zb/researchTree/fu_chemistry.config','zb/researchTree/fu_engineering.config','zb/researchTree/fu_power.config','zb/researchTree/fu_craftsmanship.config','zb/researchTree/fu_warcraft.config'):
        tree=PurePosixPath(a).stem
        return p==f'/strings/trees/{tree}' or bool(re.fullmatch(r'/strings/research/[A-Za-z0-9_]+/[01]',p))
    if a=='zb/researchTree/madness.config':
        return p=='/strings/trees/frackinuniversemadness' or bool(re.fullmatch(r'/strings/research/[A-Za-z0-9_]+/[01]',p))
    if a.startswith('quests/fu_questlines/tutorial/') and a.endswith('.questtemplate'):
        return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription') or bool(re.fullmatch(r'/scriptConfig/descriptions/[A-Za-z0-9_]+',p))
    if (a.startswith('quests/fu_questlines/science/') or a in SCIENCE_EXTERNAL_QUEST_ASSETS) and a.endswith('.questtemplate'):
        return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription') or bool(re.fullmatch(r'/scriptConfig/descriptions/[A-Za-z0-9_]+',p))
    if a.startswith('quests/fu_questlines/outpost/bees/') and a.endswith('.questtemplate'):
        return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription') or bool(re.fullmatch(r'/scriptConfig/descriptions/[A-Za-z0-9_]+',p))
    if a.startswith('quests/fu_questlines/outpost/booze/') and a.endswith('.questtemplate'):
        return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription') or bool(re.fullmatch(r'/scriptConfig/descriptions/[A-Za-z0-9_]+',p))
    if a in OUTPOST_SHOP_QUEST_ASSETS:
        return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription') or bool(re.fullmatch(r'/scriptConfig/descriptions/[A-Za-z0-9_]+',p))
    if (a.startswith('quests/fu_questlines/outpost/kevin_tasks/') or a.startswith('quests/fu_questlines/outpost/khe_stuff/')) and a.endswith('.questtemplate'):
        return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription') or bool(re.fullmatch(r'/scriptConfig/descriptions/[A-Za-z0-9_]+',p))
    if a.startswith('quests/fu_questlines/battle/') and a.endswith('.questtemplate'):
        return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription')
    if a.startswith('quests/fu_questlines/other/') and a.endswith('.questtemplate'):
        return p in ('/title','/text','/completionText','/scriptConfig/turnInDescription')
    if a.startswith('quests/fu_questlines/byos/') and a.endswith('.questtemplate'):
        return p in ('/title','/text','/completionText') or bool(re.fullmatch(r'/scriptConfig/descriptions/[A-Za-z0-9_]+',p))
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
    science_chemistry_assets=load_rule('science_chemistry_assets')
    if a in science_chemistry_assets:
        return p in ('/description','/shortdescription')
    science_electronics_assets=load_rule('science_electronics_assets')
    if a in science_electronics_assets:
        return p in ('/description','/shortdescription')
    science_genetics_assets=load_rule('science_genetics_assets')
    if a in science_genetics_assets:
        return p in ('/description','/shortdescription')
    if a=='objects/crafting/clonelab/clonelab.object':
        return p in ('/subtitle','/description','/shortdescription')
    if a=='items/generic/crafting/matterassembler/electromagnet.item':
        return p in ('/description','/shortdescription')
    if a=='items/augments/back/environment/acidimmunity.augment':
        return p in ('/description','/shortdescription','/augment/displayName')
    if a=='items/materials/blackglass.matitem':
        return p in ('/description','/shortdescription','/glitchdescription','/florandescription','/novakiddescription')
    if a in ('items/generic/crafting/fissionfurnace/protocitebar.item','items/generic/crafting/isotopes/tritium.item','items/generic/crafting/teleportercore.item'):
        return p in ('/description','/shortdescription')
    if a=='objects/crafting/handmill/handmill.object':
        return p in ('/category','/description','/shortdescription','/subtitle')
    if a=='interface/windowconfig/beerefuge.config':
        return p in ('/paneLayout/lblTitle/value','/paneLayout/lblSubTitle/value','/paneLayout/lblProduct/value','/paneLayout/btnCraft/caption','/paneLayout/btnStopCraft/caption','/paneLayout/filter/hint','/paneLayout/scrollArea/children/itemList/schema/listTemplate/itemName/value')
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
    if a=='objects/ship/fu_ftldrive/fu_ftldrivesmall.object':
        return p in ('/description','/shortdescription','/apexDescription','/avianDescription','/floranDescription','/glitchDescription','/humanDescription','/hylotlDescription','/novakidDescription')
    if a=='items/tools/mmgravgun2.beamaxe':
        return p in ('/description','/shortdescription','/category')
    outpost_bee_assets=load_rule('outpost_bee_assets')
    if a in outpost_bee_assets:
        return p in ('/description','/shortdescription','/subtitle')
    outpost_shop_assets=load_rule('outpost_shop_assets')
    if a in outpost_shop_assets:
        return p in ('/description','/shortdescription')
    outpost_kevin_khe_assets=load_rule('outpost_kevin_khe_assets')
    if a in outpost_kevin_khe_assets:
        return p in ('/description','/shortdescription') or (a=='items/throwables/beebriefcase/fu_beebriefcasekevin.activeitem' and p=='/notOnPlanetMessage')
    battle_target_assets=load_rule('battle_target_assets')
    if a in battle_target_assets:
        return p in ('/description','/shortdescription') or (a=='items/augments/quest/warbotartifact.augment' and p=='/augment/displayName')
    remaining_quest_target_assets=load_rule('remaining_quest_target_assets')
    if a in remaining_quest_target_assets:
        return p in ('/description','/shortdescription')
    power_assets=load_rule('power_assets')
    if a in power_assets:
        if a=='objects/crafting/wiringstation/wiringstation.object' and p in ('/interactData/paneLayoutOverride/windowtitle/title','/interactData/paneLayoutOverride/windowtitle/subtitle'):
            return True
        return bool(re.fullmatch(r'/(description|shortdescription|subtitle|category|[A-Za-z]+Description)',p))
    layered_craftsmanship_assets=load_rule('layered_craftsmanship_assets')
    if a=='objects/crafting/upgradeablecraftingobjects/craftingfurniture/craftingfurniture.object':
        return p=='/shortdescription' or bool(re.fullmatch(r'/upgradeStages/[01]/itemSpawnParameters/shortdescription',p))
    if a=='objects/crafting/upgradeablecraftingobjects/inventorstable/inventorstable.object':
        return p=='/shortdescription' or bool(re.fullmatch(r'/upgradeStages/[012]/itemSpawnParameters/shortdescription',p))
    if a=='objects/crafting/woodencookingtable/woodencookingtable.object':
        return bool(re.fullmatch(r'/upgradeStages/[01]/(itemSpawnParameters/(description|shortdescription|[A-Za-z]+Description)|interactData/paneLayoutOverride/windowtitle/(title|subtitle))',p))
    if a=='objects/crafting/upgradeablecraftingobjects/craftingwheel/craftingwheel.object':
        return p=='/shortdescription' or bool(re.fullmatch(r'/upgradeStages/[01]/itemSpawnParameters/shortdescription',p)) or bool(re.fullmatch(r'/upgradeStages/2/(itemSpawnParameters/(description|shortdescription|[A-Za-z]+Description)|interactData/paneLayoutOverride/lbl(Title|SubTitle)/value)',p))
    if a=='objects/crafting/upgradeablecraftingobject/slimecentrifuge/slimecentrifuge.object':
        return p in ('/description','/shortdescription') or bool(re.fullmatch(r'/upgradeStages/[012]/(itemSpawnParameters/(description|shortdescription|[A-Za-z]+Description)|interactData/paneLayoutOverride/windowtitle/(title|subtitle))',p))
    madness_simple_assets=load_rule('madness_simple_assets')
    if a in madness_simple_assets:
        return p in ('/description','/shortdescription')
    if a in ('objects/minibiome/elder/embalmingtable/embalmingtable.object','objects/power/psioniclab/psioniclab.object'):
        return p in ('/description','/shortdescription','/category')
    if a=='objects/crafting/psionicloader/psionicloader.object':
        return p in ('/description','/shortdescription','/subtitle')
    if a=='interface/windowconfig/psionicbench.config':
        return p in ('/paneLayout/lblProduct/value','/paneLayout/btnCraft/caption','/paneLayout/btnStopCraft/caption','/paneLayout/filter/hint','/paneLayout/scrollArea/children/itemList/schema/listTemplate/itemName/value')
    tutorial_target_simple_assets=load_rule('tutorial_target_simple_assets')
    if a in tutorial_target_simple_assets:
        return p in ('/description','/shortdescription')
    if a in ('objects/power/fu_rockbreaker/fu_rockbreaker.object','objects/bees/woodencentrifuge/woodencentrifuge.object','objects/crafting/fu_woodensifter/fu_woodensifter.object'):
        return p in ('/description','/shortdescription','/category')
    if a=='objects/bees/ironcentrifuge/ironcentrifuge.object':
        return p in ('/description','/shortdescription','/subtitle','/category')
    if a=='objects/crafting/armory/armory.object':
        return p in ('/description','/shortdescription') or bool(re.fullmatch(r'/upgradeStages/[012]/(itemSpawnParameters/(description|shortdescription)|interactData/paneLayoutOverride/lbl(Title|SubTitle)/value)',p))
    if a=='objects/crafting/upgradeablecraftingobjects/craftinganvil/craftinganvil.object':
        return p=='/shortdescription' or bool(re.fullmatch(r'/upgradeStages/[012]/itemSpawnParameters/shortdescription',p))
    if a=='items/armors/backitems/breathprotection/breathprotection.back':
        return p in ('/description','/shortdescription')
    craftsmanship_assets=load_rule('craftsmanship_assets')
    if a in craftsmanship_assets:
        if a=='objects/colonysystem2/colonystation/colonystation.object' and p in ('/interactData/paneLayoutOverride/windowtitle/title','/interactData/paneLayoutOverride/windowtitle/subtitle'):
            return True
        return bool(re.fullmatch(r'/(description|shortdescription|[A-Za-z]+Description)',p))
    booze_machine_assets=load_rule('booze_machine_assets')
    if a in booze_machine_assets:
        return p in ('/description','/shortdescription') or (a=='objects/crafting/starbooze/rainbarrel/rainbarrel.object' and p=='/subtitle')
    booze_item_assets=load_rule('booze_item_assets')
    if a in booze_item_assets:
        return p in ('/description','/shortdescription')
    return False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--catalog',type=Path,default=Path(__file__).with_name('ceviriler.json'))
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--source-dir',type=Path)
    args=ap.parse_args()
    if args.output.exists():ap.error('Çıktı klasörü zaten var.')

    ledger=json.loads(args.catalog.read_text(encoding='utf-8'))
    tm_policy=json.loads(Path(__file__).with_name('translation_memory_exceptions.json').read_text(encoding='utf-8'))
    tm_exceptions={x['en'] for x in tm_policy.get('exceptions',[])}
    locked_policy=json.loads(Path(__file__).with_name('locked_terms.json').read_text(encoding='utf-8'))
    locked_exact=locked_policy.get('exact_source_rules',{})
    locked_forbidden=locked_policy.get('forbidden_regexes',[])
    source_validation=verify_source(args.source_dir)
    integrity=validate_project(ledger['translations'])
    rows=ledger['translations'];groups=defaultdict(list);seen=set();colorfix=0;translation_memory=defaultdict(set)
    for r in rows:
        a,p=r['asset'],r['pointer']
        if PurePosixPath(a).is_absolute() or '..' in PurePosixPath(a).parts or '\\' in a:raise ValueError('Güvensiz asset yolu: '+a)
        if (a,p) in seen:raise ValueError('Yinelenen alan: '+a+p)
        seen.add((a,p))
        if a in V018_DEAD_OBJECT_ASSETS:raise ValueError('Runtime bağlantısı olmayan v0.18 nesnesi: '+a)
        if a in V019_DEAD_CRAFTING_ITEM_ASSETS:raise ValueError('Runtime bağlantısı olmayan/deprecated v0.19 üretim eşyası: '+a)
        if a in V020_INACTIVE_QUEST_ASSETS:raise ValueError('Oyuncuya görünmeyen/erişilemeyen v0.20 görevi: '+a)
        if not allowed(a,p):raise ValueError('Oyuncu metni olmayan alan: '+a+p)
        if nonvisible_research_pointer(a,p):raise ValueError('Aktif araştırma düğümüne bağlı olmayan metin: '+a+p)
        if a in NONVISIBLE_QUEST_ASSETS:raise ValueError('Aktif görev zincirine bağlı olmayan/kırık görev: '+a)
        if 'İngilizce adı:' in r['tr']:raise ValueError('İngilizce fallback/gloss: '+a+p)
        if r['en'].strip()=='Replace Me':raise ValueError('Runtime listTemplate dummy metni kataloğa alınamaz: '+a+p)
        if any(x in r['tr'] for x in BAD_TR_PATTERNS):raise ValueError('Bilinen Türkçe LQA hatası: '+a+p)
        plain_en=COLOR.sub('',r['en']).strip();plain_tr=COLOR.sub('',r['tr']).strip()
        if plain_en in locked_exact and plain_tr!=locked_exact[plain_en]:raise ValueError('LOCKED terminoloji ihlali: '+a+p+' -> '+locked_exact[plain_en])
        for rule in locked_forbidden:
            flags=re.IGNORECASE if rule.get('ignore_case') else 0
            if re.search(rule['pattern'],r['tr'],flags):raise ValueError(rule.get('message','Terminoloji ihlali')+' '+a+p)
        if 'kraliçe arı' in r['tr'].casefold():raise ValueError('Kilitli arıcılık terimi ihlali (Ana Arı): '+a+p)
        if LOWERCASE_MECH.search(r['tr']):raise ValueError('Kilitli Mech yazımı ihlali (Mech büyük harfle): '+a+p)
        if p=='/shortdescription' and re.search(r'\bGreaves\b', r['en']) and not re.search(r'Baldırl(?:ık|ığı)(?: Mk\. 2)?$', r['tr']):raise ValueError('Kilitli Greaves -> Baldırlık terminolojisi ihlali: '+a+p)
        if a=='items/armors/biome/garden/quiver/air/airback.back' and p=='/shortdescription' and r['tr']!='Beceri Sadağı':raise ValueError('Kilitli Skill Quiver -> Beceri Sadağı terminolojisi ihlali: '+a+p)
        if a=='items/active/weapons/ranged/unique/science/irradiator/isn_irradiator.activeitem' and p=='/shortdescription' and r['tr']!='Radyasyon Yayıcı':raise ValueError('Kilitli Irradiator -> Radyasyon Yayıcı terminolojisi ihlali: '+a+p)
        if a=='objects/crafting/pethealingstation/pethealingstationauto.object' and p=='/subtitle' and r['tr']!='Yaralı evcil hayvanlar için':raise ValueError('Pet Healing Station kaynak-anlam düzeltmesi korunmalı: '+a+p)
        if a=='interface/windowconfig/beerefuge.config' and p=='/paneLayout/btnCraft/caption' and r['tr']!='Takas Et':raise ValueError('Arı Barınağı karma eylem etiketi Takas Et olmalı: '+a+p)
        if Counter(COLOR.findall(r['en']))!=Counter(COLOR.findall(r['tr'])):
            if not r.get('qa',{}).get('allow_color_fix'):raise ValueError('Renk kodu uyuşmazlığı: '+a+p)
            colorfix+=1
        if Counter(CONTROL.findall(r['en']))!=Counter(CONTROL.findall(r['tr'])):
            if not r.get('qa',{}).get('allow_control_fix'):raise ValueError('Kontrol kodu uyuşmazlığı: '+a+p)
        if Counter(PRINTF.findall(r['en']))!=Counter(PRINTF.findall(r['tr'])):
            raise ValueError('Printf yer tutucusu uyuşmazlığı: '+a+p)
        if Counter(ICON.findall(r['en']))!=Counter(ICON.findall(r['tr'])):
            raise ValueError('Tooltip ikon uyuşmazlığı: '+a+p)
        if r['en'].count('\t')!=r['tr'].count('\t') and not r.get('qa',{}).get('allow_tab_fix'):
            raise ValueError('Sekme uyuşmazlığı: '+a+p)
        if signed_nums(r['en'])!=signed_nums(r['tr']):
            raise ValueError('İşaretli sayı uyuşmazlığı: '+a+p)
        if r['en'].count('%')!=r['tr'].count('%'):
            raise ValueError('Yüzde işareti uyuşmazlığı: '+a+p)
        if Counter(BRACE_PLACEHOLDER.findall(r['en']))!=Counter(BRACE_PLACEHOLDER.findall(r['tr'])):
            raise ValueError('Süslü parantez yer tutucusu uyuşmazlığı: '+a+p)
        if Counter(DOLLAR_PLACEHOLDER.findall(r['en']))!=Counter(DOLLAR_PLACEHOLDER.findall(r['tr'])):
            raise ValueError('Değişken yer tutucusu uyuşmazlığı: '+a+p)
        if r['en'].count('\n')!=r['tr'].count('\n'):
            raise ValueError('Satır sonu uyuşmazlığı: '+a+p)
        if nums(r['en'])!=nums(r['tr']) and not r.get('qa',{}).get('allow_number_fix'):raise ValueError('Sayı uyuşmazlığı: '+a+p)
        translation_memory[r['en']].add(r['tr'])
        groups[a].append(r)

    for source_text,translations in translation_memory.items():
        if len(translations)>1 and source_text not in tm_exceptions:
            raise ValueError('Çeviri belleği tutarsızlığı: '+source_text+' -> '+repr(sorted(translations)))

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
            direct_rows = [r for r in rs if not r.get('qa',{}).get('layered_source')]
            if direct_rows:
                if not source.is_file():
                    raise FileNotFoundError(source)
                data = parse_jsonc(source.read_text(encoding='utf-8-sig'))
                for row in direct_rows:
                    if read_at(data, row['pointer']) != row['en']:
                        raise ValueError('Direct source mismatch: ' + a + row['pointer'])
            patch_cache = {}
            for row in rs:
                qa = row.get('qa', {})
                if not qa.get('layered_source'):
                    continue
                if qa.get('source_patch'):
                    verify_layered_row(row, args.source_dir, patch_cache)
                elif not qa.get('external_base_verified'):
                    raise ValueError('Missing external source provenance: ' + a + row['pointer'])
        patches[a]=patch

    # Lua gibi JSON Patch uygulanamayan görünür metinler için kaynak-kilitli ham override.
    raw_assets={};raw_string_count=0
    raw_manifest_path=Path(__file__).with_name('raw_text_translations.json')
    if raw_manifest_path.is_file():
        raw_manifest=json.loads(raw_manifest_path.read_text(encoding='utf-8'))
        validate_manifest_pin(raw_manifest, Path(__file__).parent)
        for spec in raw_manifest.get('assets',[]):
            a=spec['asset']
            if PurePosixPath(a).is_absolute() or '..' in PurePosixPath(a).parts or '\\' in a:raise ValueError('Güvensiz ham asset yolu: '+a)
            replacements=spec.get('replacements',[])
            if args.source_dir:
                source=args.source_dir/a
                if not source.is_file():raise FileNotFoundError(source)
                verify_source_blob(spec, source)
                content=source.read_text(encoding='utf-8-sig')
                for r in replacements:
                    expected=int(r.get('expected_count',1))
                    if content.count(r['old'])!=expected:raise ValueError('Ham kaynak uyuşmazlığı: '+a+' | '+r.get('display_en',r['old']))
                    content=content.replace(r['old'],r['new'])
                    raw_string_count+=expected
            else:
                template=Path(__file__).parent/'raw_overrides'/a
                if not template.is_file():raise FileNotFoundError(template)
                content=template.read_text(encoding='utf-8-sig')
                for r in replacements:
                    expected=int(r.get('expected_count',1))
                    if content.count(r['old'])!=0 or content.count(r['new'])!=expected:raise ValueError('Ham override doğrulaması başarısız: '+a+' | '+r.get('display_tr',r['new']))
                    raw_string_count+=expected
            raw_assets[a]=content

    # Kaynak-kilitli Lua davranış düzeltmeleri. Bunlar çeviri birimi sayılmaz,
    # fakat pinned FU kodunda exact-match doğrulaması olmadan pakete giremez.
    runtime_manifest_path=Path(__file__).with_name('raw_runtime_overrides.json')
    if runtime_manifest_path.is_file():
        runtime_manifest=json.loads(runtime_manifest_path.read_text(encoding='utf-8'))
        validate_manifest_pin(runtime_manifest, Path(__file__).parent)
        for spec in runtime_manifest.get('assets',[]):
            a=spec['asset']
            if PurePosixPath(a).is_absolute() or '..' in PurePosixPath(a).parts or '\\' in a:
                raise ValueError('Güvensiz runtime override yolu: '+a)
            if args.source_dir:
                source=args.source_dir/a
                if not source.is_file():raise FileNotFoundError(source)
                verify_source_blob(spec, source)
                content=raw_assets.get(a, source.read_text(encoding='utf-8-sig'))
                for r in spec.get('replacements',[]):
                    expected=int(r.get('expected_count',1))
                    if content.count(r['old'])!=expected:
                        raise ValueError('Runtime override kaynak uyuşmazlığı: '+a)
                    content=content.replace(r['old'],r['new'])
            else:
                template=Path(__file__).parent/'raw_overrides'/a
                if not template.is_file():raise FileNotFoundError(template)
                content=raw_assets.get(a, template.read_text(encoding='utf-8-sig'))
                for r in spec.get('replacements',[]):
                    expected=int(r.get('expected_count',1))
                    if content.count(r['old'])!=0 or content.count(r['new'])!=expected:
                        raise ValueError('Runtime override şablon doğrulaması başarısız: '+a)
            raw_assets[a]=content

    if args.source_dir:
        for asset, content in raw_assets.items():
            template = Path(__file__).parent / 'raw_overrides' / asset
            if not template.is_file() or template.read_text(encoding='utf-8-sig') != content:
                raise ValueError('Raw template/pinned build drift: ' + asset)

    args.output.mkdir(parents=True)
    mod=args.output/'FU_Turkce';mod.mkdir()
    metadata={'name':'FU_Turkce','friendlyName':'FU Türkçe (Beta)',
      'author':'FU Türkçe',
      'version':ledger['translation_version'],
      'description':"Frackin' Universe için devam eden Türkçe yerelleştirme. Araştırma, görevler, üretim, temel makineler, işlevsel nesneler ve geniş ekipman kapsamını içerir.",
      'requires':['FrackinUniverse'],'priority':9000}
    (mod/'_metadata').write_bytes((json.dumps(metadata,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    for a,p in patches.items():
        d=mod/(a+'.patch');d.parent.mkdir(parents=True,exist_ok=True)
        d.write_bytes((json.dumps(p,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    for a,content in raw_assets.items():
        d=mod/a;d.parent.mkdir(parents=True,exist_ok=True)
        d.write_bytes(content.encode('utf-8'))
    stats={'fields':len(rows),'patch_assets':len(patches),'raw_assets':len(raw_assets),'assets':len(patches)+len(raw_assets),'raw_strings':raw_string_count,'color_fixes':colorfix,'static_qa':'PASS','in_game_lqa':'NOT TESTED',**integrity}
    if args.source_dir:
        stats['source_field_coverage'] = {
            'direct': sum(not r.get('qa', {}).get('layered_source') for r in rows),
            'fu_patch': sum(bool(r.get('qa', {}).get('source_patch')) for r in rows),
            'external_ledger_only': sum(bool(r.get('qa', {}).get('layered_source'))
                                        and not r.get('qa', {}).get('source_patch') for r in rows),
        }
    result=record_validation(args.output,stats,args.catalog,source_validation)
    print(json.dumps(result,ensure_ascii=False))
    return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,KeyError,TypeError,IndexError,OSError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);raise SystemExit(1)
