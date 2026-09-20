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
CONTROL=re.compile(r'\[(?![^\]]*\^)[^\]]+\]|<[^>]+>')
NUMBER=re.compile(r'\d+(?:[.,]\d+)?')
ASCII_PAREN=re.compile(r'\([ -~]*[A-Za-z][ -~]*\)')
LOWERCASE_MECH=re.compile(r'\bmech\b')

# Geriye dönük LQA'da yakalanan ve tekrar projeye sızmaması gereken Türkçe hatalar.
BAD_TR_PATTERNS = (
    'Bilim Karakolundaki^reset; bana getir',
    'Dükkânına^reset;, ^orange;Bilim Karakoluna',
    'keskinlığ',
    'monokllü',
    'Et varlıklar'
)

# FU 6.5.8 pinned kaynağında strings.research altında dursa da aktif researchTree
# düğümüne bağlı olmayan metinler. Oyuncuya görünmedikleri için yamaya alınmaz.
NONVISIBLE_QUEST_ASSETS = {
    'quests/fu_questlines/tutorial/start_basics1.questtemplate',
    'quests/fu_questlines/science/chemistry/fuquest_dna.questtemplate',
    'quests/fu_questlines/science/chemistry/fuquest_mineral.questtemplate',
    'quests/fu_questlines/outpost/bees/13mites.questtemplate'
}

SCIENCE_EXTERNAL_QUEST_ASSETS = {
    'quests/fu_questlines/deprecated/fuquest_powerstation.questtemplate',
    'quests/fu_questlines/deprecated/fuquest_battery.questtemplate',
    'quests/fu_questlines/deprecated/fuquest_prototyper.questtemplate'
}

OUTPOST_SHOP_QUEST_ASSETS = {
    'quests/fu_questlines/outpost/scienceoutpost_floranShop.questtemplate',
    'quests/fu_questlines/outpost/scienceoutpost_foodShop.questtemplate',
    'quests/fu_questlines/outpost/scienceoutpost_gemShop.questtemplate',
    'quests/fu_questlines/outpost/scienceoutpost_kirhosShop.questtemplate',
    'quests/fu_questlines/outpost/scienceoutpost_radienShop.questtemplate',
    'quests/fu_questlines/outpost/scienceoutpost_shadowShop.questtemplate'
}

NONVISIBLE_RESEARCH_IDS = {
    'zb/researchTree/fu_geology.config': {'default','metals_tier7','metals_morphite','metals_nocxium','metals_plasmiccrystal','metals_diamond','metals_alloy5','metals_alloy6','isotopes6','terraforming1','terraforming2','terraforming3'},
    'zb/researchTree/fu_agriculture.config': {'default'},
    'zb/researchTree/fu_chemistry.config': {'default','elduucrystals'},
    'zb/researchTree/fu_engineering.config': {'default'},
    'zb/researchTree/fu_power.config': {'default','ansible'},
    'zb/researchTree/fu_craftsmanship.config': {'default','workbenchatechy'},
    'zb/researchTree/fu_warcraft.config': {'default'},
    'zb/researchTree/madness.config': {'default'}
}

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
        return p in ('/gui/researchButton/caption','/gui/infoList/children/unlocksLabel/value','/gui/title/value','/gui/consumptionText/value')
    if a=='zb/questList/data.config':
        return p in ('/strings/questlines/fu_sciences/title','/strings/questlines/fu_sciences/description') or bool(re.fullmatch(r'/strings/sublines/fu_(physics|chemistry|electronics|genetics|mechanical)',p))
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
    if a=='quests/fu_questlines/byos/fu_byosftldrive.questtemplate':
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
    science_chemistry_assets={
        'items/generic/crafting/chemlab/ff_fertilizer.item',
        'items/generic/crafting/iodine.item',
        'items/generic/crafting/chemlab/methyliodide.item',
        'items/liquids/liquidwastewater.liqitem',
        'items/generic/crafting/chemlab/fu_mulch.item',
        'items/materials/calichewall.matitem',
        'items/materials/bonemealmaterial.matitem',
        'items/generic/crafting/icecrystal.item'
    }
    if a in science_chemistry_assets:
        return p in ('/description','/shortdescription')
    science_electronics_assets={
        'items/generic/crafting/matterassembler/aichip.item',
        'items/generic/crafting/siliconboard.item',
        'objects/fu_watcher/fu_watcher.object'
    }
    if a in science_electronics_assets:
        return p in ('/description','/shortdescription')
    science_genetics_assets={
        'objects/farmables/miraclegrassseed/miraclegrassseed.object',
        'objects/farmables/brackentree/brackentreeseed.object',
        'objects/farmables/mutavisk/mutaviskseed.object',
        'objects/farmables/oonfortaseed/oonfortaseed.object',
        'objects/farmables/ignuschili/ignuschiliseed.object',
        'items/armors/tier3/mutaviskarmor/mutavisk.head',
        'items/generic/produce/guam.consumable',
        'objects/farmables/thornitoxplant/thornitoxseed.object'
    }
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
    outpost_bee_assets={
        'bees/objects/apiary/apiary.object',
        'bees/frames/basic.item',
        'bees/objects/beeexaminer/beeExaminer.object',
        'bees/bees/honey_queen.item',
        'bees/bees/honey_drone.item',
        'bees/combs/normalcomb.consumable',
        'items/generic/crafting/waxchunk.item',
        'bees/objects/apiarylarge/apiarylarge.object',
        'objects/bees/honeyjarrer/honeyjarrer.object',
        'bees/frames/tungsten.item',
        'items/materials/honey/goldenwood.matitem',
        'bees/bees/orchid_queen.item',
        'bees/bees/orchid_drone.item',
        'bees/bees/bumble_queen.item',
        'bees/bees/bumble_drone.item',
        'items/active/unsorted/bugnet/bugnet.activeitem',
        'objects/farmables/flowerred/flowerred.object',
        'items/generic/crafting/bottle.item'
    }
    if a in outpost_bee_assets:
        return p in ('/description','/shortdescription','/subtitle')
    outpost_shop_assets={
        'items/generic/loot/mission/greenfinger_trophy.item',
        'items/generic/loot/mission/luckycoin.item',
        'items/generic/loot/mission/temple_trophy.item',
        'items/generic/loot/mission/alien_trophy.item',
        'items/generic/loot/mission/radien_trophy.item',
        'items/generic/loot/mission/ancient_tech.item',
        'objects/scienceoutpost/fufoodshopfloran/fufoodshopfloran.object',
        'objects/scienceoutpost/fufoodshop/fufoodshop.object',
        'objects/scienceoutpost/fugemshop/fugemshop.object',
        'objects/scienceoutpost/kirhosshop/kirhosshop.object',
        'objects/scienceoutpost/radienshop/silene_shop.object',
        'objects/scienceoutpost/fushadowstore/fushadowstore.object'
    }
    if a in outpost_shop_assets:
        return p in ('/description','/shortdescription')
    power_assets={
        'objects/power/isn_solarpanel/isn_solarpanel.object',
        'objects/power/fu_solararray/fu_solararray.object',
        'objects/power/fu_solararrayadv/fu_solararrayadv.object',
        'objects/power/hydraulicdynamo/hydraulicdynamo.object',
        'objects/power/fu_windarray/isn_windarray.object',
        'objects/power/isn_thermalgenerator/isn_thermalgenerator.object',
        'objects/power/electricfurnace/electricfurnace.object',
        'objects/power/fu_blastfurnace/fu_blastfurnace.object',
        'objects/power/isn_arcsmelter/isn_arcsmelter.object',
        'objects/power/isn_fissionreactornew/isn_fissionreactornew.object',
        'objects/power/makeshiftreactor/makeshiftreactor.object',
        'objects/skath/skathfusionreactor/skathfusionreactor.object',
        'objects/power/fu_quantumgenerator/fu_quantumgenerator.object',
        'objects/power/quantumextractor/quantumextractor.object',
        'objects/bees/industrialcentrifuge/industrialcentrifuge.object',
        'objects/power/centrifuge/centrifuge.object',
        'objects/power/isn_powdersifter/isn_powdersifter.object',
        'objects/power/centrifuge2/centrifuge2.object',
        'objects/power/manufacturing/mfgstation.object',
        'objects/power/fu_liquidcondenser/fu_liquidcondenser.object',
        'objects/power/isn_battery_t1/isn_battery_t1.object',
        'objects/power/isn_battery_t2/isn_battery_t2.object',
        'objects/power/isn_battery_t3_ceru/isn_battery_t3_ceru.object',
        'objects/power/isn_battery_t3_fero/isn_battery_t3_fero.object',
        'objects/power/isn_battery_t4_fero/isn_battery_t4_fero.object',
        'objects/power/isn_atmoscondenser/isn_atmoscondenser.object',
        'objects/power/fu_liquidmixer/fu_liquidmixer.object',
        'objects/power/fu_atmosfilter/fu_atmosfilter.object',
        'objects/power/isn_atmosregulator/isn_atmosregulatornew.object',
        'objects/power/isn_atmosregulator/isn_atmosregulator.object',
        'objects/crafting/wiringstation/wiringstation.object',
        'objects/power/fu_alternatorgenerator/fu_alternatorgenerator.object'
    }
    if a in power_assets:
        if a=='objects/crafting/wiringstation/wiringstation.object' and p in ('/interactData/paneLayoutOverride/windowtitle/title','/interactData/paneLayoutOverride/windowtitle/subtitle'):
            return True
        return bool(re.fullmatch(r'/(description|shortdescription|subtitle|category|[A-Za-z]+Description)',p))
    layered_craftsmanship_assets={
        'objects/crafting/upgradeablecraftingobjects/craftingfurniture/craftingfurniture.object',
        'objects/crafting/upgradeablecraftingobjects/inventorstable/inventorstable.object',
        'objects/crafting/upgradeablecraftingobjects/craftingwheel/craftingwheel.object',
        'objects/crafting/woodencookingtable/woodencookingtable.object'
    }
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
    madness_simple_assets={
        'items/currency/fumadnessresource.currency',
        'items/active/weapons/other/brainharvester/brainharvester.activeitem',
        'items/active/weapons/ranged/unique/psiejector/psiejector.activeitem',
        'items/generic/crafting/darkmatter.item',
        'objects/crafting/instafreud/instafreud.object',
        'objects/crafting/psionicbench/psionicbench.object',
        'items/generic/crafting/matterconverter.item',
        'items/generic/crafting/psionicenergy.item',
        'items/generic/crafting/psionicenergy2.item',
        'items/generic/crafting/psionicenergy3.item',
        'items/generic/crafting/psionicenergy4.item',
        'objects/power/braingenerator/braingenerator.object',
        'objects/power/brainbattery/brainbattery.object'
    }
    if a in madness_simple_assets:
        return p in ('/description','/shortdescription')
    if a in ('objects/minibiome/elder/embalmingtable/embalmingtable.object','objects/power/psioniclab/psioniclab.object'):
        return p in ('/description','/shortdescription','/category')
    if a=='objects/crafting/psionicloader/psionicloader.object':
        return p in ('/description','/shortdescription','/subtitle')
    if a=='interface/windowconfig/psionicbench.config':
        return p in ('/paneLayout/lblProduct/value','/paneLayout/btnCraft/caption','/paneLayout/btnStopCraft/caption','/paneLayout/filter/hint','/paneLayout/scrollArea/children/itemList/schema/listTemplate/itemName/value')
    tutorial_target_simple_assets={
        'items/armors/backitems/lanternstick/lanternstick.back',
        'items/active/weapons/ranged/unique/miners/minertest/basicminertest.activeitem',
        'items/generic/crafting/methanol.item',
        'items/generic/crafting/fu_hydrogen.item',
        'items/generic/crafting/ff_silicon.item',
        'items/active/weapons/melee/spear/stonespear.activeitem',
        'items/generic/mechparts/legs/mechlegssimpleupgrade.item',
        'items/generic/mechparts/legs/mechlegssimpleupgrade2.item',
        'items/active/unsorted/mechTablet/mechtablet.activeitem',
        'items/active/unsorted/techtablet/techtablet.activeitem',
        'items/tools/wiretoolfu.wiretool',
        'objects/kheAA/kheAA_containerLink/kheAA_containerLink.object',
        'items/generic/crafting/paper.item',
        'items/generic/crafting/silverbar.item',
        'items/liquids/oil.liqitem',
        'objects/upgrade/techconsole/techconsole.object',
        'items/materials/sand.matitem',
        'items/materials/gravel.matitem'
    }
    if a in tutorial_target_simple_assets:
        return p in ('/description','/shortdescription')
    if a in ('objects/power/fu_rockbreaker/fu_rockbreaker.object','objects/bees/woodencentrifuge/woodencentrifuge.object','objects/crafting/fu_woodensifter/fu_woodensifter.object'):
        return p in ('/description','/shortdescription','/category')
    if a=='objects/crafting/armory/armory.object':
        return p in ('/description','/shortdescription') or bool(re.fullmatch(r'/upgradeStages/[012]/(itemSpawnParameters/(description|shortdescription)|interactData/paneLayoutOverride/lbl(Title|SubTitle)/value)',p))
    if a=='objects/crafting/upgradeablecraftingobjects/craftinganvil/craftinganvil.object':
        return p=='/shortdescription' or bool(re.fullmatch(r'/upgradeStages/[012]/itemSpawnParameters/shortdescription',p))
    if a=='items/armors/backitems/breathprotection/breathprotection.back':
        return p in ('/description','/shortdescription')
    craftsmanship_assets={
        'objects/colonysystem2/colonystation/colonystation.object',
        'objects/colonysystem2/colonycore/colonycore.object',
        'objects/colonysystem2/colonydeedmk2/colonydeedmk2.object',
        'objects/colonysystem2/colonydeedmk2/colonydeedmk2tiny.object',
        'objects/peglaci/snowpersongenerator/snowpersongenerator.object',
        'objects/crafting/lavalampstation/lavalampstation.object'
    }
    if a in craftsmanship_assets:
        if a=='objects/colonysystem2/colonystation/colonystation.object' and p in ('/interactData/paneLayoutOverride/windowtitle/title','/interactData/paneLayoutOverride/windowtitle/subtitle'):
            return True
        return bool(re.fullmatch(r'/(description|shortdescription|[A-Za-z]+Description)',p))
    booze_machine_assets={
        'objects/generic/boozekit/boozekit.object',
        'objects/crafting/starbooze/mashingtun/mashingtun.object',
        'objects/crafting/starbooze/fruitpress/fruitpress.object',
        'objects/crafting/starbooze/fermenter/fermenter.object',
        'objects/crafting/starbooze/rainbarrel/rainbarrel.object',
        'objects/crafting/starbooze/distillery/distillery.object'
    }
    if a in booze_machine_assets:
        return p in ('/description','/shortdescription') or (a=='objects/crafting/starbooze/rainbarrel/rainbarrel.object' and p=='/subtitle')
    booze_item_assets={
        'items/generic/crafting/starbooze/yeastwater.item',
        'items/generic/crafting/starbooze/grainwater.item',
        'items/generic/crafting/starbooze/grapemash.item',
        'items/generic/crafting/starbooze/wartwine.consumable',
        'items/generic/crafting/starbooze/hops.item',
        'items/generic/crafting/starbooze/malt.item',
        'items/generic/crafting/starbooze/wort.item',
        'items/generic/drinks/beer/beer.consumable',
        'items/generic/crafting/starbooze/applemash.item',
        'items/generic/crafting/starbooze/pearmash.item',
        'items/generic/crafting/starbooze/peachmash.item',
        'items/generic/drinks/vodka/spirits.consumable',
        'items/generic/crafting/starbooze/honeybucket.item',
        'items/generic/drinks/ciders/meadbottle.consumable',
        'items/generic/crafting/fu_carbondioxide.item',
        'items/liquids/fu_liquidhoney.liqitem'
    }
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
    rows=ledger['translations'];groups=defaultdict(list);seen=set();colorfix=0
    for r in rows:
        a,p=r['asset'],r['pointer']
        if PurePosixPath(a).is_absolute() or '..' in PurePosixPath(a).parts or '\\' in a:raise ValueError('Güvensiz asset yolu: '+a)
        if (a,p) in seen:raise ValueError('Yinelenen alan: '+a+p)
        seen.add((a,p))
        if not allowed(a,p):raise ValueError('Oyuncu metni olmayan alan: '+a+p)
        if nonvisible_research_pointer(a,p):raise ValueError('Aktif araştırma düğümüne bağlı olmayan metin: '+a+p)
        if a in NONVISIBLE_QUEST_ASSETS:raise ValueError('Aktif görev zincirine bağlı olmayan/kırık görev: '+a)
        if 'İngilizce adı:' in r['tr']:raise ValueError('İngilizce fallback/gloss: '+a+p)
        if r['en'].strip()=='Replace Me':raise ValueError('Runtime listTemplate dummy metni kataloğa alınamaz: '+a+p)
        if any(x in r['tr'] for x in BAD_TR_PATTERNS):raise ValueError('Bilinen Türkçe LQA hatası: '+a+p)
        if 'kraliçe arı' in r['tr'].casefold():raise ValueError('Kilitli arıcılık terimi ihlali (Ana Arı): '+a+p)
        if LOWERCASE_MECH.search(r['tr']):raise ValueError('Kilitli Mech yazımı ihlali (Mech büyük harfle): '+a+p)
        if a=='interface/windowconfig/beerefuge.config' and p=='/paneLayout/btnCraft/caption' and r['tr']!='Takas Et':raise ValueError('Arı Barınağı karma eylem etiketi Takas Et olmalı: '+a+p)
        if Counter(COLOR.findall(r['en']))!=Counter(COLOR.findall(r['tr'])):
            if not r.get('qa',{}).get('allow_color_fix'):raise ValueError('Renk kodu uyuşmazlığı: '+a+p)
            colorfix+=1
        if Counter(CONTROL.findall(r['en']))!=Counter(CONTROL.findall(r['tr'])):
            if not r.get('qa',{}).get('allow_control_fix'):raise ValueError('Kontrol kodu uyuşmazlığı: '+a+p)
        if nums(r['en'])!=nums(r['tr']) and not r.get('qa',{}).get('allow_number_fix'):raise ValueError('Sayı uyuşmazlığı: '+a+p)
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
            if source.is_file():
                if all(r.get('qa',{}).get('raw_source_value_guard') for r in rs):
                    source_text=source.read_text(encoding='utf-8-sig')
                    for r in rs:
                        if source_text.count(r['en'])<1:
                            raise ValueError('Ham JSON kaynak değeri bulunamadı: '+a+r['pointer'])
                else:
                    simulate(parse_jsonc(source.read_text(encoding='utf-8-sig')),patch)
            elif all(r.get('qa',{}).get('layered_source') for r in rs):
                # FU bazı vanilla assetleri yalnızca .patch katmanıyla değiştirir; hedef .object FU kaynak ağacında bulunmaz.
                # Bu alanların kaynak provenansı ledger qa.source_patch / external_base_verified ile ayrıca kilitlenir.
                pass
            else:
                raise FileNotFoundError(source)
        patches[a]=patch

    # Lua gibi JSON Patch uygulanamayan görünür metinler için kaynak-kilitli ham override.
    raw_assets={};raw_string_count=0
    raw_manifest_path=Path(__file__).with_name('raw_text_translations.json')
    if raw_manifest_path.is_file():
        raw_manifest=json.loads(raw_manifest_path.read_text(encoding='utf-8'))
        for spec in raw_manifest.get('assets',[]):
            a=spec['asset']
            if PurePosixPath(a).is_absolute() or '..' in PurePosixPath(a).parts or '\\' in a:raise ValueError('Güvensiz ham asset yolu: '+a)
            replacements=spec.get('replacements',[])
            if args.source_dir:
                source=args.source_dir/a
                if not source.is_file():raise FileNotFoundError(source)
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

    args.output.mkdir(parents=True)
    mod=args.output/'FU_Turkce';mod.mkdir()
    metadata={'name':'FU_Turkce','friendlyName':'FU Türkçe - Araştırma Sistemleri + Görevler (Beta)',
      'author':'FU TÜRKÇE topluluk yerelleştirmesi; FU: sayter ve katkıda bulunanlar',
      'version':ledger['translation_version'],
      'description':'Kısmi Türkçe yerelleştirme yaması. Ana araştırma sistemleri, Delilik/Metafizik, Tutorial ve Science görevleri ile Outpost İçki, Arıcılık ve Bilim Karakolu dükkân görevlerini kapsar; oyun içi LQA, font ve taşma testleri sürüyor.',
      'requires':['FrackinUniverse'],'priority':9000}
    (mod/'_metadata').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a,p in patches.items():
        d=mod/(a+'.patch');d.parent.mkdir(parents=True,exist_ok=True)
        d.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a,content in raw_assets.items():
        d=mod/a;d.parent.mkdir(parents=True,exist_ok=True)
        d.write_text(content,encoding='utf-8')
    print(json.dumps({'fields':len(rows),'patch_assets':len(patches),'raw_assets':len(raw_assets),'assets':len(patches)+len(raw_assets),'raw_strings':raw_string_count,'color_fixes':colorfix,'static_qa':'PASS','in_game_lqa':'NOT TESTED'},ensure_ascii=False))
    return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,KeyError,TypeError,IndexError,OSError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);raise SystemExit(1)
