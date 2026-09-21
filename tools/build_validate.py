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
PRINTF=re.compile(r'%(?:\d+\$)?[-+0#]*(?:\d+|\*)?(?:\.\d+|\.\*)?(?:hh|h|ll|l|L|z|j|t)?[diuoxXfFeEgGaAcspn%]')
BRACE_PLACEHOLDER=re.compile(r'\{(?:\d+|[A-Za-z_][A-Za-z0-9_.:-]*)\}')
DOLLAR_PLACEHOLDER=re.compile(r'\$(?:\{[A-Za-z_][A-Za-z0-9_.:-]*\}|[A-Za-z_][A-Za-z0-9_.:-]*)')
ASCII_PAREN=re.compile(r'\([ -~]*[A-Za-z][ -~]*\)')
LOWERCASE_MECH=re.compile(r'\bmech\b')

# Geriye dönük LQA'da yakalanan ve tekrar projeye sızmaması gereken Türkçe hatalar.
BAD_TR_PATTERNS = (
    'Bilim Karakolundaki^reset; bana getir',
    'Dükkânına^reset;, ^orange;Bilim Karakoluna',
    'keskinlığ',
    'monokllü',
    'Et varlıklar',
    "Vel'uuish arasında popüler bir keskin nişancı seçeneği",
    'Dirençlerine 5% katkı ile bir oksijen geri dönüştürücüsü sağlar',
    'Düşmanları hem de çok fazla hareket ettirir.'
)

# FU 6.5.8 pinned kaynağında strings.research altında dursa da aktif researchTree
# düğümüne bağlı olmayan metinler. Oyuncuya görünmedikleri için yamaya alınmaz.
NONVISIBLE_QUEST_ASSETS = {
    'quests/fu_questlines/tutorial/start_basics1.questtemplate',
    'quests/fu_questlines/science/chemistry/fuquest_dna.questtemplate',
    'quests/fu_questlines/science/chemistry/fuquest_mineral.questtemplate',
    'quests/fu_questlines/outpost/bees/13mites.questtemplate',
    'quests/fu_questlines/battle/monsters/fuquest_gorgolith.questtemplate',
    'quests/fu_questlines/battle/monsters/fuquest_gorillaking.questtemplate',
    'quests/fu_questlines/battle/monsters/fuquest_titan.questtemplate',
    'quests/fu_questlines/other/crucible_upgrades.questtemplate',
    'quests/fu_questlines/other/kevin_annoyance.questtemplate',
    'quests/fu_questlines/other/madness_reduction.questtemplate',
    'quests/fu_questlines/other/station_upgrades.questtemplate',
    'quests/fu_questlines/other/tricorder.questtemplate',
    'quests/fu_questlines/byos/fu_byosshipcraftingtable.questtemplate',
    'quests/fu_questlines/exploration/fuquest_explore1.questtemplate'
}

SCIENCE_EXTERNAL_QUEST_ASSETS = {
    'quests/fu_questlines/deprecated/fuquest_powerstation.questtemplate',
    'quests/fu_questlines/deprecated/fuquest_battery.questtemplate',
    'quests/fu_questlines/deprecated/fuquest_prototyper.questtemplate'
}

# v0.18: objects/power, objects/bees ve objects/scienceoutpost altındaki 57
# aday runtime tarifleri, araştırma düğümleri, dükkânlar ve Tiled yerleşimleriyle
# denetlendi. Aşağıdaki 47 asset gerçekten erişilebilir; kalan 10 asset bilinçli
# olarak dışarıda tutulur.
V018_OBJECT_ASSETS = {
    'objects/power/fu_conduit/fu_conduit.object',
    'objects/power/fu_fieldgenerator/fieldgen.object',
    'objects/power/fu_nocturnarray/fu_nocturnarray.object',
    'objects/power/fu_powersensorlarge/fu_powersensorlarge.object',
    'objects/power/fu_rechargesensor/fu_rechargesensor.object',
    'objects/power/fu_rockcrusher/fu_rockcrusher.object',
    'objects/power/fu_weatherbeacon/fu_weatherbeacon.object',
    'objects/power/gnomefactory/gnomefactory.object',
    'objects/power/isn_atmoscondenser/isn_atmoscondensermadness.object',
    'objects/power/isn_atmosregulator/isn_atmosregulatorwarped.object',
    'objects/power/isn_battery_t0/isn_battery_t0.object',
    'objects/power/isn_incinerator/isn_incinerator.object',
    'objects/power/isn_powersensor/isn_powersensor.object',
    'objects/power/isn_radiostation/isn_radiostationnew.object',
    'objects/power/massincinerator/massincinerator.object',
    'objects/bees/candle/bluecandle.object',
    'objects/bees/candle/bluecandledouble.object',
    'objects/bees/candle/bluecandletriple.object',
    'objects/bees/candle/flowercandle.object',
    'objects/bees/candle/flowercandledouble.object',
    'objects/bees/candle/flowercandletriple.object',
    'objects/bees/candle/ghostcandle.object',
    'objects/bees/candle/ghostcandledouble.object',
    'objects/bees/candle/ghostcandletriple.object',
    'objects/bees/candle/redcandle.object',
    'objects/bees/candle/redcandledouble.object',
    'objects/bees/candle/redcandletriple.object',
    'objects/bees/candle/waxcandle.object',
    'objects/bees/candle/waxcandledouble.object',
    'objects/bees/candle/waxcandletriple.object',
    'objects/bees/honeycooking/honeytable.object',
    'objects/bees/honeyextractor/honeyextractor.object',
    'objects/scienceoutpost/burgerfool/burgerfool.object',
    'objects/scienceoutpost/fupetshop/fupetshop.object',
    'objects/scienceoutpost/guidestorage/guidestorage.object',
    'objects/scienceoutpost/moonlit_comet/moonlitcomet.object',
    'objects/scienceoutpost/moonlit_comet/vina_plush.object',
    'objects/scienceoutpost/radienshopdrug/drugdealer.object',
    'objects/scienceoutpost/roses/rosebushlarge.object',
    'objects/scienceoutpost/roses/rosebushlarge_box.object',
    'objects/scienceoutpost/roses/rosebushmed.object',
    'objects/scienceoutpost/roses/rosebushmed_box.object',
    'objects/scienceoutpost/roses/rosebushsmall.object',
    'objects/scienceoutpost/roses/rosebushsmall_box.object',
    'objects/scienceoutpost/scienceinfobooth/scienceinfobooth.object',
    'objects/scienceoutpost/scienceoutpostbanner1/scienceoutpostbanner1.object',
    'objects/scienceoutpost/starbucks/fustarbucks.object',
}

V018_DEAD_OBJECT_ASSETS = {
    'objects/power/fu_solararrayscienceoutpost/fu_solararrayscienceoutpost.object',
    'objects/power/fu_upgrade/fu_upgrade.object',
    'objects/power/makeshiftreactor/makeshiftreactor2.object',
    'objects/bees/scentedalveary/scentedalveary.object',
    'objects/bees/scentedapiary/scentedapiary.object',
    'objects/scienceoutpost/game/deeponegame.object',
    'objects/scienceoutpost/moonlit_comet/moonlitcomet2.object',
    'objects/scienceoutpost/scienceoutpostbanner2/scienceoutpostbanner2.object',
    'objects/scienceoutpost/scienceoutpostbanner3/scienceoutpostbanner3.object',
    'objects/scienceoutpost/scienceoutpostbanner4/scienceoutpostbanner4.object',
}

V018_CHAT_OPTION_ASSETS = {
    'objects/scienceoutpost/moonlit_comet/moonlitcomet.object',
    'objects/scienceoutpost/scienceinfobooth/scienceinfobooth.object',
    'objects/scienceoutpost/starbucks/fustarbucks.object',
}

# v0.19: items/generic/crafting altındaki daha önce kapsanmayan 261 adayın
# runtime bağlantıları denetlendi. 235 etkin asset yalnızca envanter adı ve
# açıklama alanlarıyla kapsanır. Aşağıdaki 26 asset etkin tarif/ganimet/görev
# akışına bağlı değildir ya da yalnız deprecated kayıt temizliği içindir.
V019_DEAD_CRAFTING_ITEM_ASSETS = {
    'items/generic/crafting/chemlab/narcotics/fu_expiravittar.consumable',
    'items/generic/crafting/chemlab/narcotics/fu_malware.consumable',
    'items/generic/crafting/chemlab/narcotics/fu_prerolled.consumable',
    'items/generic/crafting/chemlab/narcotics/fu_radiant.consumable',
    'items/generic/crafting/chemlab/narcotics/fu_toxictop_blotter.consumable',
    'items/generic/crafting/chemlab/narcotics/fu_vexpill.consumable',
    'items/generic/crafting/chemlab/narcotics/fu_wubwub.consumable',
    'items/generic/crafting/circuitboard.item',
    'items/generic/crafting/ff_resin.item',
    'items/generic/crafting/fissionfurnace/ebonshard.item',
    'items/generic/crafting/fissionfurnace/morphitebar.item',
    'items/generic/crafting/fu_holodisc.item',
    'items/generic/crafting/fuguts.item',
    'items/generic/crafting/imperviumfurnitureplating.item',
    'items/generic/crafting/matterassembler/coil.item',
    'items/generic/crafting/matterassembler/kheWarpedRegulatorChip.item',
    'items/generic/crafting/matterassembler/magneticshielding.item',
    'items/generic/crafting/matterassembler/microchip.item',
    'items/generic/crafting/pelt.item',
    'items/generic/crafting/reactormagnet.item',
    'items/generic/crafting/servitorbehaviorchip.item',
    'items/generic/crafting/servitorchassis.item',
    'items/generic/crafting/servitorlaser.item',
    'items/generic/crafting/skathimpervium.item',
    'items/generic/crafting/starbooze/emptybottle2.item',
    'items/generic/crafting/tethydefurnitureplating.item',
}

# v0.20: FU ana görev aileleri dışındaki 97 questtemplate adayı runtime
# başlangıçları, pickupQuestTemplates, NPC offeredQuests, SAIL görevleri,
# Tiled yerleşimleri ve görev ödülleri üzerinden denetlendi. Aşağıdaki 29
# görev oyuncuya gerçekten ulaşır; yalnızca görünür görev metni alanları
# yerelleştirilir.
V020_ACTIVE_QUEST_ASSETS = {
    'quests/alienjungle.questtemplate',
    'quests/ancienttemple.questtemplate',
    'quests/avianhydro.questtemplate',
    'quests/challengelabs/extrachallengelabs1.questtemplate',
    'quests/challengelabs/extrachallengelabs2.questtemplate',
    'quests/challengelabs/extrachallengelabs3.questtemplate',
    'quests/challengelabs/extrachallengelabs4.questtemplate',
    'quests/evernight.questtemplate',
    'quests/forestoffae.questtemplate',
    'quests/grandarena.questtemplate',
    'quests/infiltration.questtemplate',
    'quests/japaneseruins.questtemplate',
    'quests/letheiafacility.questtemplate',
    'quests/letheiafleet.questtemplate',
    'quests/lethialabs.questtemplate',
    'quests/magickaforest.questtemplate',
    'quests/mmupgrade/mastermanipulator.questtemplate',
    'quests/mmupgrade/mastermanipulator2.questtemplate',
    'quests/pavillion.questtemplate',
    'quests/penguinhighway.questtemplate',
    'quests/skytemple.questtemplate',
    'quests/snowcrash.questtemplate',
    'quests/sunsetriders.questtemplate',
    'quests/tech/dash/combatmaneuvering1.questtemplate',
    'quests/tech/distortionsphere/distortionsphere.questtemplate',
    'quests/tech/distortionsphere/microsphereprecursor.questtemplate',
    'quests/tech/jump/longjump0.questtemplate',
    'quests/towerinvincible.questtemplate',
    'quests/verdantruins.questtemplate',
}

# Kaynakta bulunmasına rağmen normal oyuncu akışına bağlı olmayan v0.20
# adayları. Optional Hardmode'un başlangıcı NPC dosyasında devre dışıdır;
# çoğu eski teknoloji görevi techshop tarafından başlatılmaz; görünmez
# takip/fix görevleri de oyuncu metni üretmez.
V020_INACTIVE_QUEST_ASSETS = {
    'quests/ancientpowerconduit.questtemplate',
    'quests/bounty/fu_asraNoxSailFix.questtemplate',
    'quests/madness/madnessquest.questtemplate',
    'quests/mechfuel/fuelData.questtemplate',
    'quests/mmupgrade/mmgravgun.questtemplate',
    'quests/mmupgrade/mmgravgun2.questtemplate',
    'quests/mmupgrade/mmgravgun3.questtemplate',
    'quests/optionalhardmode/fu_t10_apex_mission2.questtemplate',
    'quests/optionalhardmode/fu_t10_avian_mission2.questtemplate',
    'quests/optionalhardmode/fu_t10_floran_mission2.questtemplate',
    'quests/optionalhardmode/fu_t10_floranarena1.questtemplate',
    'quests/optionalhardmode/fu_t10_floranarena2.questtemplate',
    'quests/optionalhardmode/fu_t10_floranarena3.questtemplate',
    'quests/optionalhardmode/fu_t10_gaterepair.questtemplate',
    'quests/optionalhardmode/fu_t10_glitch_mission2.questtemplate',
    'quests/optionalhardmode/fu_t10_human_mission1.questtemplate',
    'quests/optionalhardmode/fu_t10_hylotl_mission2.questtemplate',
    'quests/optionalhardmode/fu_t10_initial.questtemplate',
    'quests/optionalhardmode/fu_t10_precursor.questtemplate',
    'quests/story/protectorateapex.questtemplate',
    'quests/story/protectorateelunite.questtemplate',
    'quests/story/protectoratefu.questtemplate',
    'quests/story/protectoratehylotl.questtemplate',
    'quests/tech/dash/airdash2.questtemplate',
    'quests/tech/dash/blinkdash2.questtemplate',
    'quests/tech/dash/combatmaneuvering2.questtemplate',
    'quests/tech/dash/dashcombat.questtemplate',
    'quests/tech/dash/fadesprint.questtemplate',
    'quests/tech/dash/fadesprint2.questtemplate',
    'quests/tech/dash/fadesprint3.questtemplate',
    'quests/tech/dash/speedboots.questtemplate',
    'quests/tech/dash/speedboots2.questtemplate',
    'quests/tech/dash/speedboots3.questtemplate',
    'quests/tech/dash/speedbootsprecursor.questtemplate',
    'quests/tech/dash/speedbootsweak.questtemplate',
    'quests/tech/dash/teleportdash.questtemplate',
    'quests/tech/dash/zeroburst1.questtemplate',
    'quests/tech/dash/zeroburst2.questtemplate',
    'quests/tech/dash/zeroburst3.questtemplate',
    'quests/tech/dash/zeroburst4.questtemplate',
    'quests/tech/distortionsphere/armorsphere.questtemplate',
    'quests/tech/distortionsphere/bouncesphere.questtemplate',
    'quests/tech/distortionsphere/distortionsphere2.questtemplate',
    'quests/tech/distortionsphere/funball.questtemplate',
    'quests/tech/distortionsphere/microsphere.questtemplate',
    'quests/tech/distortionsphere/microspherebomb.questtemplate',
    'quests/tech/distortionsphere/microspherespider.questtemplate',
    'quests/tech/distortionsphere/powerboost.questtemplate',
    'quests/tech/jump/fuwallcling.questtemplate',
    'quests/tech/jump/fuwallcling2.questtemplate',
    'quests/tech/jump/fuwalljump.questtemplate',
    'quests/tech/jump/fuwalljump2.questtemplate',
    'quests/tech/jump/fuwalljump3.questtemplate',
    'quests/tech/jump/longjump.questtemplate',
    'quests/tech/jump/longjump2.questtemplate',
    'quests/tech/jump/longjump3.questtemplate',
    'quests/tech/jump/longjump4.questtemplate',
    'quests/tech/jump/quadjump.questtemplate',
    'quests/tech/jump/quintjump.questtemplate',
    'quests/tech/jump/rocketboots.questtemplate',
    'quests/tech/other/emergencybounce.questtemplate',
    'quests/tech/other/fuarmorboost.questtemplate',
    'quests/tech/other/fuarmorboost2.questtemplate',
    'quests/tech/other/fuarmorboost3.questtemplate',
    'quests/tech/other/fudevtech.questtemplate',
    'quests/tech/other/physicsfield.questtemplate',
    'quests/tech/other/physicsfield2.questtemplate',
    'quests/tech/other/physicsfield3.questtemplate',
    'quests/scripts/neb-damagetypekills.questtemplat',
}

# Aktif fu_warcraft ağacındaki bonegear, irongear, telebriumgear ve
# tungstengear düğümlerinin açtığı; gerçek üretim tarifi bulunan v0.21
# erken oyun silahları. Önceden kapsanan 3 asset kendi eski allowlist'inde
# kalır; burada yalnız v0.21'de eklenen 121 asset bulunur.
V021_EARLY_WEAPON_ASSETS = set('''
items/active/weapons/boomerang/bonespur.activeitem
items/active/weapons/boomerang/fufrisbee.activeitem
items/active/weapons/boomerang/ironboomerang.activeitem
items/active/weapons/boomerang/telebriumboomerang.activeitem
items/active/weapons/boomerang/tungstenboomerang.activeitem
items/active/weapons/boomerang/warspinner.activeitem
items/active/weapons/bow/bonebow/bonebow.activeitem
items/active/weapons/bow/ironcrossbow/ironcrossbow.activeitem
items/active/weapons/bow/ironstynger/ironstynger.activeitem
items/active/weapons/bow/telebriumbow/telebriumbow.activeitem
items/active/weapons/bow/telebriumcrossbow/telebriumcrossbow.activeitem
items/active/weapons/bow/telebriumstynger/telebriumstynger.activeitem
items/active/weapons/bow/tungstencrossbow/tungstencrossbow.activeitem
items/active/weapons/bow/tungstenstynger/tungstenstynger.activeitem
items/active/weapons/chakram/goldchakram.activeitem
items/active/weapons/chakram/telebriumchakram.activeitem
items/active/weapons/fist/boneclaws.activeitem
items/active/weapons/fist/hellclaw.activeitem
items/active/weapons/fist/stabfists.activeitem
items/active/weapons/fist/telebriumfist.activeitem
items/active/weapons/melee/axe/fuboneaxe.activeitem
items/active/weapons/melee/axe/fucultaxe.activeitem
items/active/weapons/melee/axe/telebriumaxe.activeitem
items/active/weapons/melee/broadsword/telebriumbroadsword.activeitem
items/active/weapons/melee/broadsword/tungstenbroadsword.activeitem
items/active/weapons/melee/dagger/feneroxdagger.activeitem
items/active/weapons/melee/dagger/fubonepickaxe.activeitem
items/active/weapons/melee/dagger/silverseablade.activeitem
items/active/weapons/melee/dagger/telebriumdagger.activeitem
items/active/weapons/melee/flail/flailiron.activeitem
items/active/weapons/melee/flail/flailtelebrium.activeitem
items/active/weapons/melee/flail/flailtungsten.activeitem
items/active/weapons/melee/greataxe/irongreataxe.activeitem
items/active/weapons/melee/greataxe/telebriumgreataxe.activeitem
items/active/weapons/melee/greataxe/tungstengreataxe.activeitem
items/active/weapons/melee/hammer/fishboneheadbasher.activeitem
items/active/weapons/melee/hammer/fubonehammer.activeitem
items/active/weapons/melee/hammer/telebriumhammer.activeitem
items/active/weapons/melee/katana/ironkatana.activeitem
items/active/weapons/melee/katana/telebriumkatana.activeitem
items/active/weapons/melee/katana/tungstenkatana.activeitem
items/active/weapons/melee/longsword/fubonesword.activeitem
items/active/weapons/melee/longsword/fucellsword.activeitem
items/active/weapons/melee/longsword/ironlongsword.activeitem
items/active/weapons/melee/longsword/silverlongsword.activeitem
items/active/weapons/melee/longsword/telebriumlongsword.activeitem
items/active/weapons/melee/longsword/tungstenlongsword.activeitem
items/active/weapons/melee/mace/bonemace.activeitem
items/active/weapons/melee/mace/fu_wrenchweapon.activeitem
items/active/weapons/melee/mace/ironmace.activeitem
items/active/weapons/melee/mace/telebriummace.activeitem
items/active/weapons/melee/mace/tungstenmace.activeitem
items/active/weapons/melee/quarterstaff/copperquarterstaff.activeitem
items/active/weapons/melee/quarterstaff/ironquarterstaff.activeitem
items/active/weapons/melee/quarterstaff/silverquarterstaff.activeitem
items/active/weapons/melee/quarterstaff/telebriumquarterstaff.activeitem
items/active/weapons/melee/quarterstaff/tungstenquarterstaff.activeitem
items/active/weapons/melee/rapier/goldrapier.activeitem
items/active/weapons/melee/rapier/ironrapier.activeitem
items/active/weapons/melee/rapier/silverrapier.activeitem
items/active/weapons/melee/rapier/telebriumrapier.activeitem
items/active/weapons/melee/rapier/tungstenrapier.activeitem
items/active/weapons/melee/scythe/fubonescythe.activeitem
items/active/weapons/melee/scythe/goldscythe.activeitem
items/active/weapons/melee/scythe/ironscythe.activeitem
items/active/weapons/melee/scythe/telebriumscythe.activeitem
items/active/weapons/melee/shortspear/coreshortspear.activeitem
items/active/weapons/melee/shortspear/ironshortspear.activeitem
items/active/weapons/melee/shortspear/telebriumshortspear.activeitem
items/active/weapons/melee/shortspear/tungstenshortspear.activeitem
items/active/weapons/melee/shortsword/boneblade.activeitem
items/active/weapons/melee/shortsword/goldenseascion.activeitem
items/active/weapons/melee/shortsword/telebriumshortsword.activeitem
items/active/weapons/melee/spear/bonespear.activeitem
items/active/weapons/melee/spear/lavaspear.activeitem
items/active/weapons/melee/spear/telebriumspear.activeitem
items/active/weapons/novakid/ironlmg.activeitem
items/active/weapons/novakid/ironmachinepistol.activeitem
items/active/weapons/novakid/ironshotgun.activeitem
items/active/weapons/novakid/ironsniperrifle.activeitem
items/active/weapons/novakid/tungstenassaultrifle.activeitem
items/active/weapons/novakid/tungstenmachinepistol.activeitem
items/active/weapons/novakid/tungstensniperrifle.activeitem
items/active/weapons/other/magnorbs/magnorbmoonstone/magnorbmoonstone.activeitem
items/active/weapons/protectorate/ironaxe.activeitem
items/active/weapons/protectorate/irondagger.activeitem
items/active/weapons/protectorate/ironhammer.activeitem
items/active/weapons/protectorate/ironspear.activeitem
items/active/weapons/protectorate/tungstendagger.activeitem
items/active/weapons/protectorate/tungstenshortsword.activeitem
items/active/weapons/protectorate/tungstenspear.activeitem
items/active/weapons/ranged/unique/aegisaltpistol3.activeitem
items/active/weapons/ranged/unique/artillery/crappy/crappyartillery.activeitem
items/active/weapons/ranged/unique/burster.activeitem
items/active/weapons/ranged/unique/bushmaster.activeitem
items/active/weapons/ranged/unique/corerifle.activeitem
items/active/weapons/ranged/unique/ff_bubblegun.activeitem
items/active/weapons/ranged/unique/ff_icechucker.activeitem
items/active/weapons/ranged/unique/fuprotectoraterifle.activeitem
items/active/weapons/ranged/unique/fuprotectoratesniper.activeitem
items/active/weapons/ranged/unique/lasrifle.activeitem
items/active/weapons/ranged/unique/pistolironfu.activeitem
items/active/weapons/ranged/unique/pistoltungstenfu.activeitem
items/active/weapons/ranged/unique/randomharpoongun.activeitem
items/active/weapons/ranged/unique/rifleironfu.activeitem
items/active/weapons/ranged/unique/rifletungstenfu.activeitem
items/active/weapons/ranged/unique/science/isn_flintlock/isn_flintlock.activeitem
items/active/weapons/ranged/unique/sniperknife.activeitem
items/active/weapons/ranged/unique/telebriummachinepistol.activeitem
items/active/weapons/ranged/unique/telebriumpistol.activeitem
items/active/weapons/ranged/unique/telebriumrifle.activeitem
items/active/weapons/ranged/unique/telebriumrocketlauncher.activeitem
items/active/weapons/ranged/unique/telebriumshotgun.activeitem
items/active/weapons/ranged/unique/telebriumsniperrifle.activeitem
items/active/weapons/staff/orestaffs/telebriumstaff.activeitem
items/active/weapons/wand/fuflamewand/fuflamewand.activeitem
items/active/weapons/wand/fuicewand/fuicewand.activeitem
items/active/weapons/wand/orewands/telebriumwand.activeitem
items/active/weapons/whip/silverwhip.activeitem
items/active/weapons/whip/stingwhip.activeitem
items/active/weapons/whip/telebriumwhip.activeitem
'''.split())

# Aktif fu_warcraft ağacındaki Kademe 1-2 zırh kollarının açtığı,
# gerçek üretim tarifi bulunan v0.25 zırh parçaları. EPP düğümleri ayrı
# sistem olarak sonraki kapsama bırakılmıştır. Burada 114 yeni asset vardır.
V025_EARLY_ARMOR_ASSETS = set('''
items/armors/backitems/noobpack/noobpack.back
items/armors/backitems/slimeinvisibleback/invisible.back
items/armors/bees/fubeesuit/fubeesuit.chest
items/armors/bees/fubeesuit/fubeesuit.head
items/armors/bees/fubeesuit/fubeesuit.legs
items/armors/biome/garden/quiver/quiver2/quiver2.back
items/armors/elduukhar/invis/inviselduu.chest
items/armors/elduukhar/invis/inviselduu.head
items/armors/elduukhar/invis/inviselduu.legs
items/armors/elduukhar/templeguard/templeguard.chest
items/armors/elduukhar/templeguard/templeguard.head
items/armors/elduukhar/templeguard/templeguard.legs
items/armors/elduukhar/worshipper/worshipper.chest
items/armors/elduukhar/worshipper/worshipper.head
items/armors/elduukhar/worshipper/worshipper.legs
items/armors/elduukhar/worshipper/worshipper2.head
items/armors/elduukhar/worshipper/worshipper3.head
items/armors/elduukhar/worshipper/worshipper4.head
items/armors/elduukhar/worshipper/worshipper5.head
items/armors/other/visors/snowgoggles/snowgoggles.head
items/armors/skath/skath-tier1/skathtier1.chest
items/armors/skath/skath-tier1/skathtier1.head
items/armors/skath/skath-tier1/skathtier1.legs
items/armors/skath/skath-tier2/skathtier2.chest
items/armors/skath/skath-tier2/skathtier2.head
items/armors/skath/skath-tier2/skathtier2.legs
items/armors/skath/skath-tier3accelerator/skathtier3accelerator.chest
items/armors/skath/skath-tier3accelerator/skathtier3accelerator.head
items/armors/skath/skath-tier3accelerator/skathtier3accelerator.legs
items/armors/skath/skath-tier3manipulator/skathtier3manipulator.chest
items/armors/skath/skath-tier3manipulator/skathtier3manipulator.head
items/armors/skath/skath-tier3manipulator/skathtier3manipulator.legs
items/armors/skath/skath-tier3separator/skathtier3separator.chest
items/armors/skath/skath-tier3separator/skathtier3separator.head
items/armors/skath/skath-tier3separator/skathtier3separator.legs
items/armors/slimeperson/slimeperson-invisible/invisible.chest
items/armors/slimeperson/slimeperson-invisible/invisible.head
items/armors/slimeperson/slimeperson-invisible/invisible.legs
items/armors/tier1/armoredsnowpants/armoredsnowpants.legs
items/armors/tier1/bloodhound/bloodhound.chest
items/armors/tier1/bloodhound/bloodhound.head
items/armors/tier1/bloodhound/bloodhound.legs
items/armors/tier1/fubonearmor/fubone.chest
items/armors/tier1/fubonearmor/fubone.head
items/armors/tier1/fubonearmor/fubone.legs
items/armors/tier1/leatherarmor/leatherarmor.chest
items/armors/tier1/leatherarmor/leatherarmor.head
items/armors/tier1/leatherarmor/leatherarmor.legs
items/armors/tier1/missionary/missionaryrobe.chest
items/armors/tier1/missionary/missionaryrobe.head
items/armors/tier1/missionary/missionaryrobe.legs
items/armors/tier1/plebeian/mantizitier1.chest
items/armors/tier1/plebeian/mantizitier1.legs
items/armors/tier1/spacediver/spacediver.chest
items/armors/tier1/spacediver/spacediver.head
items/armors/tier1/spacediver/spacediver.legs
items/armors/tier1/underworld/kirhostier1.chest
items/armors/tier1/underworld/kirhostier1.head
items/armors/tier1/underworld/kirhostier1.legs
items/armors/tier2/battletotem/beararmor.chest
items/armors/tier2/battletotem/beararmor.head
items/armors/tier2/battletotem/beararmor.legs
items/armors/tier2/fangshaman/wolf.chest
items/armors/tier2/fangshaman/wolf.head
items/armors/tier2/fangshaman/wolf.legs
items/armors/tier2/ff_slimearmor/ff_slimearmor.chest
items/armors/tier2/ff_slimearmor/ff_slimearmor.head
items/armors/tier2/ff_slimearmor/ff_slimearmor.legs
items/armors/tier2/fubonearmor2/fubone2.chest
items/armors/tier2/fubonearmor2/fubone2.head
items/armors/tier2/fubonearmor2/fubone2.legs
items/armors/tier2/furecon/furecon.chest
items/armors/tier2/furecon/furecon.head
items/armors/tier2/furecon/furecon.legs
items/armors/tier2/hacker/kirhostier2.chest
items/armors/tier2/hacker/kirhostier2.head
items/armors/tier2/hacker/kirhostier2.legs
items/armors/tier2/lunariarmor/lunari.chest
items/armors/tier2/lunariarmor/lunari.head
items/armors/tier2/lunariarmor/lunari.legs
items/armors/tier2/mantiziroyalguard/royalguard.chest
items/armors/tier2/mantiziroyalguard/royalguard.head
items/armors/tier2/mantiziroyalguard/royalguard.legs
items/armors/tier2/mantiziroyalguardornate/royalguardornate.chest
items/armors/tier2/mantiziroyalguardornate/royalguardornate.head
items/armors/tier2/mantiziroyalguardornate/royalguardornate.legs
items/armors/tier2/militia/mantizitier2.chest
items/armors/tier2/militia/mantizitier2.head
items/armors/tier2/militia/mantizitier2.legs
items/armors/tier2/nomad/fudesertwalker.chest
items/armors/tier2/nomad/fudesertwalker.head
items/armors/tier2/nomad/fudesertwalker.legs
items/armors/tier2/operative/fuoperative.chest
items/armors/tier2/operative/fuoperative.head
items/armors/tier2/operative/fuoperative.legs
items/armors/tier2/samurai/fusamuraiarmor.chest
items/armors/tier2/samurai/fusamuraiarmor.head
items/armors/tier2/samurai/fusamuraiarmor.legs
items/armors/tier2/sanguine/bloodgarb.chest
items/armors/tier2/sanguine/bloodgarb.head
items/armors/tier2/sanguine/bloodgarb.legs
items/armors/tier2/swashbuckler/cannoneer.chest
items/armors/tier2/swashbuckler/cannoneer.head
items/armors/tier2/swashbuckler/cannoneer.legs
items/armors/tier2/tw_spacesuit/tw_spacesuit.chest
items/armors/tier2/tw_spacesuit/tw_spacesuit.head
items/armors/tier2/tw_spacesuit/tw_spacesuit.legs
items/armors/tier2/vagabond/deckardchest.chest
items/armors/tier2/vagabond/deckardhead.head
items/armors/tier2/vagabond/deckardpants.legs
items/armors/tier3/stalkers/fudarkrobeschest.chest
items/armors/tier3/stalkers/fudarkrobeshelmet.head
items/armors/tier3/stalkers/fudarkrobespants.legs
items/armors/uniques/fuhoodedmask/fuhoodedmask.head
'''.split())

# Aktif fu_warcraft ağacındaki yedi Kademe 5 kolunun açtığı ve gerçek
# üretim tarifi bulunan v0.29 zırh parçaları. Runtime araştırma/tarif
# zinciri esas olduğu için kaynak yolu tier4 veya tier6 olan parçalar da vardır.
V029_TIER5_ARMOR_ASSETS = set('''
items/armors/biome/garden/quiver/air/airback.back
items/armors/biome/garden/quiver/quiver5/quiver5.back
items/armors/other/pandorasboxcapturenaut/pandorasboxcapturenaut.chest
items/armors/other/pandorasboxcapturenaut/pandorasboxcapturenaut.head
items/armors/other/pandorasboxcapturenaut/pandorasboxcapturenaut.legs
items/armors/other/pandorasboxcapturenaut/pandorasboxcapturenautpack.back
items/armors/tier4/kingslayer/test1.chest
items/armors/tier4/kingslayer/test1.head
items/armors/tier4/kingslayer/test1.legs
items/armors/tier5/arctic/sciencefu.chest
items/armors/tier5/arctic/sciencefu.head
items/armors/tier5/arctic/sciencefu.legs
items/armors/tier5/decker/kirhostier5manipulator.chest
items/armors/tier5/decker/kirhostier5manipulator.head
items/armors/tier5/decker/kirhostier5manipulator.legs
items/armors/tier5/ff_diamondarmor/ff_diamondarmor.chest
items/armors/tier5/ff_diamondarmor/ff_diamondarmor.head
items/armors/tier5/ff_diamondarmor/ff_diamondarmor.legs
items/armors/tier5/fudiver3/fudiver3.chest
items/armors/tier5/fudiver3/fudiver3.head
items/armors/tier5/fudiver3/fudiver3.legs
items/armors/tier5/fuwarphunter/fuwarphunter.chest
items/armors/tier5/fuwarphunter/fuwarphunter.head
items/armors/tier5/fuwarphunter/fuwarphunter.legs
items/armors/tier5/hellfire/hellfire.chest
items/armors/tier5/hellfire/hellfire.legs
items/armors/tier5/hellfire/hellfirehelm.head
items/armors/tier5/legionii/mantizitier5manipulator.chest
items/armors/tier5/legionii/mantizitier5manipulator.head
items/armors/tier5/legionii/mantizitier5manipulator.legs
items/armors/tier5/millenion/mantizitier5separator.chest
items/armors/tier5/millenion/mantizitier5separator.head
items/armors/tier5/millenion/mantizitier5separator.legs
items/armors/tier5/morphite/fuquantum.chest
items/armors/tier5/morphite/fuquantum.head
items/armors/tier5/morphite/fuquantum.legs
items/armors/tier5/rifter/kirhostier5separator.chest
items/armors/tier5/rifter/kirhostier5separator.head
items/armors/tier5/rifter/kirhostier5separator.legs
items/armors/tier5/sentryarmor/mobiusarmor.chest
items/armors/tier5/sentryarmor/mobiusarmor.head
items/armors/tier5/sentryarmor/mobiusarmor.legs
items/armors/tier5/valkyrie/althelm/kirhostier5accelerator2.head
items/armors/tier5/valkyrie/kirhostier5accelerator.chest
items/armors/tier5/valkyrie/kirhostier5accelerator.head
items/armors/tier5/valkyrie/kirhostier5accelerator.legs
items/armors/tier5/warframe/mantizitier5accelerator.chest
items/armors/tier5/warframe/mantizitier5accelerator.head
items/armors/tier5/warframe/mantizitier5accelerator.legs
items/armors/tier6/champion/mantizitier6separator.chest
items/armors/tier6/champion/mantizitier6separator.head
items/armors/tier6/champion/mantizitier6separator.legs
items/armors/tier6/fusunwalker/fusunwalker.chest
items/armors/tier6/fusunwalker/fusunwalker.head
items/armors/tier6/fusunwalker/fusunwalker.legs
items/armors/tier6/morphite2/fuquantumadv.chest
items/armors/tier6/morphite2/fuquantumadv.head
items/armors/tier6/morphite2/fuquantumadv.legs
items/armors/tier6/replicant/kirhostier6accelerator.chest
items/armors/tier6/replicant/kirhostier6accelerator.head
items/armors/tier6/replicant/kirhostier6accelerator.legs
'''.split())

# v0.30: etkin fu_warcraft düğümü + gerçek tarif çıktısı + görünür ekipman
# kesişiminde kalan 413 asset. Yol listesi çeviri manifestinde tek kaynak olarak
# tutulur; yalnız ad ve açıklama alanlarına izin verilir.
_V030_MANIFEST = json.loads(
    Path(__file__).with_name('v030_translations.json').read_text(encoding='utf-8')
)
V030_RESEARCH_GEAR_ASSETS = {spec['asset'] for spec in _V030_MANIFEST.values()}
if len(_V030_MANIFEST) != 413 or len(V030_RESEARCH_GEAR_ASSETS) != 413:
    raise ValueError('v0.30 ekipman manifesti 413 benzersiz asset içermeli')

# Aktif fu_warcraft ağacındaki yedi Kademe 5 savaş ekipmanı kolunun
# gerçek üretim tarifi bulunan v0.28 assetleri. Ferozium Satırı önceki
# Battle paketinde çevrildiği için burada 96 yeni asset vardır.
V028_TIER5_COMBAT_ASSETS = set('''
items/active/shields/bubbleshield.activeitem
items/active/shields/hellfireshield.activeitem
items/active/shields/nightar1.activeitem
items/active/shields/shadowshield.activeitem
items/active/shields/tritaniumshield.activeitem
items/active/weapons/bow/lightningcrossbow/lightningcrossbow.activeitem
items/active/weapons/bow/lightningstynger/lightningstynger.activeitem
items/active/weapons/bow/shadowstring/shadowstring.activeitem
items/active/weapons/melee/axe/effigiumaxe.activeitem
items/active/weapons/melee/axe/poweraxe.activeitem
items/active/weapons/melee/axe/uraniumaxe.activeitem
items/active/weapons/melee/broadsword/effigiumbroadsword.activeitem
items/active/weapons/melee/broadsword/uraniumbroadsword.activeitem
items/active/weapons/melee/dagger/effigiumdagger.activeitem
items/active/weapons/melee/dagger/fushadowdagger.activeitem
items/active/weapons/melee/dagger/uraniumdagger.activeitem
items/active/weapons/melee/flail/flailaegisalt.activeitem
items/active/weapons/melee/flail/flaileffigium.activeitem
items/active/weapons/melee/hammer/effigiumhammer.activeitem
items/active/weapons/melee/hammer/fuquantumhammer.activeitem
items/active/weapons/melee/hammer/uraniumhammer.activeitem
items/active/weapons/melee/katana/blooddiamondkatana.activeitem
items/active/weapons/melee/katana/diamondkatana.activeitem
items/active/weapons/melee/longsword/blooddiamondlongsword.activeitem
items/active/weapons/melee/longsword/effigiumlongsword.activeitem
items/active/weapons/melee/longsword/violiumlongsword.activeitem
items/active/weapons/melee/mace/aegisaltmace.activeitem
items/active/weapons/melee/mace/densealloymace.activeitem
items/active/weapons/melee/mace/effigiummace.activeitem
items/active/weapons/melee/mace/quantummace.activeitem
items/active/weapons/melee/mace/uraniummace.activeitem
items/active/weapons/melee/quarterstaff/diamondquarterstaff.activeitem
items/active/weapons/melee/rapier/effigiumrapier.activeitem
items/active/weapons/melee/shortspear/tritaniumshortspear.activeitem
items/active/weapons/melee/shortsword/effigiumshortsword.activeitem
items/active/weapons/melee/shortsword/heliosblade.activeitem
items/active/weapons/melee/shortsword/obsidianblade.activeitem
items/active/weapons/melee/shortsword/shadowburst.activeitem
items/active/weapons/melee/shortsword/uraniumshortsword.activeitem
items/active/weapons/melee/spear/banespear.activeitem
items/active/weapons/melee/spear/effigiumspear.activeitem
items/active/weapons/melee/spear/tritaniumspear.activeitem
items/active/weapons/melee/spear/uraniumspear.activeitem
items/active/weapons/other/magnorbs/magnorbhellfire/magnorbhellfire.activeitem
items/active/weapons/other/magnorbs/magnorbneutron/magnorbneutron.activeitem
items/active/weapons/other/magnorbs/magnorbshadow/magnorbshadow.activeitem
items/active/weapons/ranged/unique/artillery/violium/artillerygun1.activeitem
items/active/weapons/ranged/unique/bigdaddy.activeitem
items/active/weapons/ranged/unique/farsight.activeitem
items/active/weapons/ranged/unique/fucyclone.activeitem
items/active/weapons/ranged/unique/fuplasmacannon.activeitem
items/active/weapons/ranged/unique/fuplasmagun.activeitem
items/active/weapons/ranged/unique/futritaniumpistol.activeitem
items/active/weapons/ranged/unique/gravgun.activeitem
items/active/weapons/ranged/unique/gravitongun.activeitem
items/active/weapons/ranged/unique/gravitonpistol.activeitem
items/active/weapons/ranged/unique/mineralcannonadv.activeitem
items/active/weapons/ranged/unique/nitrogengun.activeitem
items/active/weapons/ranged/unique/nitrogenpistol.activeitem
items/active/weapons/ranged/unique/peglaci/chargecannon/chargecannon.activeitem
items/active/weapons/ranged/unique/peglaci/cripplermachinegun/chargemachinegun.activeitem
items/active/weapons/ranged/unique/peglaci/freezecannon/fufreezecannon.activeitem
items/active/weapons/ranged/unique/peglaci/frostcannonarm/frostcannonarm.activeitem
items/active/weapons/ranged/unique/peglaci/fubeamgun/fubeamgun.activeitem
items/active/weapons/ranged/unique/peglaci/fucloudgun/fucloudgun.activeitem
items/active/weapons/ranged/unique/peglaci/fuenergyblaster/fuenergyblaster.activeitem
items/active/weapons/ranged/unique/peglaci/fuenergymachinegun/fuenergymachinegun.activeitem
items/active/weapons/ranged/unique/peglaci/fuminelayer/fuminelayer.activeitem
items/active/weapons/ranged/unique/peglaci/furailgun/furailgun.activeitem
items/active/weapons/ranged/unique/peglaci/fushocklance/fushocklance.activeitem
items/active/weapons/ranged/unique/peglaci/imperius/chargemachinegun.activeitem
items/active/weapons/ranged/unique/peglaci/splittergun/splittergun.activeitem
items/active/weapons/ranged/unique/pistolaegisaltfu.activeitem
items/active/weapons/ranged/unique/pistoleffigiumfu.activeitem
items/active/weapons/ranged/unique/pistolferoziumfu.activeitem
items/active/weapons/ranged/unique/pistolirradiumfu.activeitem
items/active/weapons/ranged/unique/pistolvioliumfu.activeitem
items/active/weapons/ranged/unique/rifleaegisaltfu.activeitem
items/active/weapons/ranged/unique/rifleeffigiumfu.activeitem
items/active/weapons/ranged/unique/rifleferoziumfu.activeitem
items/active/weapons/ranged/unique/rifleirradiumfu.activeitem
items/active/weapons/ranged/unique/riflevioliumfu.activeitem
items/active/weapons/ranged/unique/science/annihilator/isn_annihilator.activeitem
items/active/weapons/ranged/unique/science/flamecannon/isn_flamethrower4.activeitem
items/active/weapons/ranged/unique/science/fusioncannon/isn_fusioncannon.activeitem
items/active/weapons/ranged/unique/science/plasmabeam/isn_plasmabeam.activeitem
items/active/weapons/ranged/unique/science/plasmapistol/isn_plasmapistol.activeitem
items/active/weapons/ranged/unique/science/terawattlaser/isn_terawattlaser.activeitem
items/active/weapons/ranged/unique/veilbreaker.activeitem
items/active/weapons/staff/gravitystaff/gravitystaff.activeitem
items/active/weapons/staff/orestaffs/effigiumstaff.activeitem
items/active/weapons/staff/orestaffs/tritaniumstaff.activeitem
items/active/weapons/staff/shadowstaff/shadowstaff.activeitem
items/active/weapons/wand/orewands/effigiumwand.activeitem
items/active/weapons/wand/orewands/tritaniumwand.activeitem
items/active/weapons/whip/effigiumwhip.activeitem
'''.split())

# Aktif fu_warcraft ağacındaki yedi Kademe 4 zırh kolunun açtığı ve
# gerçek üretim tarifi bulunan v0.27 zırh parçaları. Dosya yolu tier5
# olsa da Cute seti bu Kademe 4 araştırma/tarif zincirinden açılır.
V027_TIER4_ARMOR_ASSETS = set('''
items/armors/backitems/cutewings/cutewings.back
items/armors/backitems/shadowbonecape/shadowbonecape.back
items/armors/biome/garden/quiver/power/powerback.back
items/armors/biome/garden/quiver/quiver4/quiver4.back
items/armors/biome/garden/quiver/speed/speedback.back
items/armors/tier4/Ranger/quietus.chest
items/armors/tier4/Ranger/quietus.head
items/armors/tier4/Ranger/quietus.legs
items/armors/tier4/bearenhanced/beararmor2.chest
items/armors/tier4/bearenhanced/beararmor2.head
items/armors/tier4/bearenhanced/beararmor2.legs
items/armors/tier4/blisteralt/blisterarmoralt.chest
items/armors/tier4/blisteralt/blisterarmoralt.head
items/armors/tier4/blisteralt/blisterarmoralt.legs
items/armors/tier4/cellular/cellulararmor.chest
items/armors/tier4/cellular/cellulararmor.head
items/armors/tier4/cellular/cellulararmor.legs
items/armors/tier4/cultflesh/cultflesh.chest
items/armors/tier4/cultflesh/cultflesh.head
items/armors/tier4/cultflesh/cultflesh.legs
items/armors/tier4/enforcerarmor/enforcerarmor.chest
items/armors/tier4/enforcerarmor/enforcerarmor.head
items/armors/tier4/enforcerarmor/enforcerarmor.legs
items/armors/tier4/fieldscience/fieldscientist.chest
items/armors/tier4/fieldscience/fieldscientist.head
items/armors/tier4/fieldscience/fieldscientist.legs
items/armors/tier4/fuarmoredcultist/fuarmoredcultist.back
items/armors/tier4/fuarmoredcultist/fuarmoredcultist.chest
items/armors/tier4/fuarmoredcultist/fuarmoredcultist.head
items/armors/tier4/fuarmoredcultist/fuarmoredcultist.legs
items/armors/tier4/fudiver2/fudiver2.chest
items/armors/tier4/fudiver2/fudiver2.head
items/armors/tier4/fudiver2/fudiver2.legs
items/armors/tier4/fuguardian/fuguardian.chest
items/armors/tier4/fuguardian/fuguardian.head
items/armors/tier4/fuguardian/fuguardian.legs
items/armors/tier4/fuinferno/fuinferno.chest
items/armors/tier4/fuinferno/fuinferno.head
items/armors/tier4/fuinferno/fuinferno.legs
items/armors/tier4/fuinvader/fuinvader.chest
items/armors/tier4/fuinvader/fuinvader.head
items/armors/tier4/fuinvader/fuinvader.legs
items/armors/tier4/fuprotector/fuprotector.chest
items/armors/tier4/fuprotector/fuprotector.head
items/armors/tier4/fuprotector/fuprotector.legs
items/armors/tier4/furavager/furavager.chest
items/armors/tier4/furavager/furavager.head
items/armors/tier4/furavager/furavager.legs
items/armors/tier4/fustarkiller/fustarkiller.chest
items/armors/tier4/fustarkiller/fustarkiller.head
items/armors/tier4/fustarkiller/fustarkiller.legs
items/armors/tier4/graphene/graphene.chest
items/armors/tier4/graphene/graphene.head
items/armors/tier4/graphene/graphene.legs
items/armors/tier4/hunter/wasteland2.chest
items/armors/tier4/hunter/wasteland2.head
items/armors/tier4/hunter/wasteland2.legs
items/armors/tier4/intersec/kirhostier4.chest
items/armors/tier4/intersec/kirhostier4.head
items/armors/tier4/intersec/kirhostier4.legs
items/armors/tier4/irradiumarmor/irradiumarmor.chest
items/armors/tier4/irradiumarmor/irradiumarmor.head
items/armors/tier4/irradiumarmor/irradiumarmor.legs
items/armors/tier4/maverickhunter/maverickhunter.chest
items/armors/tier4/maverickhunter/maverickhunter.head
items/armors/tier4/maverickhunter/maverickhunter.legs
items/armors/tier4/primus/mantizitier4.chest
items/armors/tier4/primus/mantizitier4.head
items/armors/tier4/primus/mantizitier4.legs
items/armors/tier4/scoutarmor_melee/ff_scoutarmor_melee.chest
items/armors/tier4/scoutarmor_melee/ff_scoutarmor_melee.head
items/armors/tier4/scoutarmor_melee/ff_scoutarmor_melee.legs
items/armors/tier4/shadowbonearmor/shadowbonearmor.chest
items/armors/tier4/shadowbonearmor/shadowbonearmor.head
items/armors/tier4/shadowbonearmor/shadowbonearmor.legs
items/armors/tier4/spacefareradv/spacefareradv.chest
items/armors/tier4/spacefareradv/spacefareradv.head
items/armors/tier4/spacefareradv/spacefareradv.legs
items/armors/tier4/survivors/wasteland.chest
items/armors/tier4/survivors/wasteland.head
items/armors/tier4/survivors/wasteland.legs
items/armors/tier4/x10/xeno.chest
items/armors/tier4/x10/xeno.head
items/armors/tier4/x10/xeno.legs
items/armors/tier5/cute/cute.chest
items/armors/tier5/cute/cute.head
items/armors/tier5/cute/cute.legs
'''.split())

# Aktif fu_warcraft ağacındaki altı Kademe 3 zırh kolunun açtığı,
# gerçek üretim tarifi bulunan v0.26 zırh parçaları. Mutavisk miğferi
# önceki Science paketinde çevrildiği için burada 75 yeni asset vardır.
V026_TIER3_ARMOR_ASSETS = set('''
items/armors/biome/garden/quiver/energy/energyback.back
items/armors/biome/garden/quiver/quiver3/quiver3.back
items/armors/nightar/daywalker/daywalker.chest
items/armors/nightar/daywalker/daywalker.head
items/armors/nightar/daywalker/daywalker.legs
items/armors/other/visors/bmcglowscoutvisor/bmcglowscoutvisor.head
items/armors/other/visors/bmcjumpscoutvisor/bmcjumpscoutvisor.head
items/armors/other/visors/bmcspeedscoutvisor/bmcspeedscoutvisor.head
items/armors/tier3/assaultarmor/fuexplorer.chest
items/armors/tier3/assaultarmor/fuexplorer.head
items/armors/tier3/assaultarmor/fuexplorer.legs
items/armors/tier3/battleborn/test1.chest
items/armors/tier3/battleborn/test1.head
items/armors/tier3/battleborn/test1.legs
items/armors/tier3/corsair/kirhostier3.chest
items/armors/tier3/corsair/kirhostier3.head
items/armors/tier3/corsair/kirhostier3.legs
items/armors/tier3/evaarmor/eva.chest
items/armors/tier3/evaarmor/eva.head
items/armors/tier3/evaarmor/eva.legs
items/armors/tier3/evader/fuplatinumarmor.chest
items/armors/tier3/evader/fuplatinumarmor.head
items/armors/tier3/evader/fuplatinumarmor.legs
items/armors/tier3/fuhoplite/fuhoplite.chest
items/armors/tier3/fuhoplite/fuhoplite.head
items/armors/tier3/fuhoplite/fuhoplite.legs
items/armors/tier3/fuintrepid/fuintrepid.chest
items/armors/tier3/fuintrepid/fuintrepid.head
items/armors/tier3/fuintrepid/fuintrepid.legs
items/armors/tier3/fujunker/fujunker.chest
items/armors/tier3/fujunker/fujunker.head
items/armors/tier3/fujunker/fujunker.legs
items/armors/tier3/gendarme/furusted.chest
items/armors/tier3/gendarme/furusted.head
items/armors/tier3/gendarme/furusted.legs
items/armors/tier3/masquerade/test1.chest
items/armors/tier3/masquerade/test1.head
items/armors/tier3/masquerade/test1.legs
items/armors/tier3/mutaviskarmor/mutavisk.chest
items/armors/tier3/mutaviskarmor/mutavisk.legs
items/armors/tier3/nautilus/fudiver.chest
items/armors/tier3/nautilus/fudiver.head
items/armors/tier3/nautilus/fudiver.legs
items/armors/tier3/samurai2/samurai2.chest
items/armors/tier3/samurai2/samurai2.head
items/armors/tier3/samurai2/samurai2.legs
items/armors/tier3/scoutarmor/ff_scoutarmor.chest
items/armors/tier3/scoutarmor/ff_scoutarmor.head
items/armors/tier3/scoutarmor/ff_scoutarmor.legs
items/armors/tier3/shielded/rust2.chest
items/armors/tier3/shielded/rust2.head
items/armors/tier3/shielded/rust2.legs
items/armors/tier3/slayer/mantizitier3.chest
items/armors/tier3/slayer/mantizitier3.head
items/armors/tier3/slayer/mantizitier3.legs
items/armors/tier3/spacefarer/spacefarer.chest
items/armors/tier3/spacefarer/spacefarer.head
items/armors/tier3/spacefarer/spacefarer.legs
items/armors/tier3/steampunk/fusteampunk.chest
items/armors/tier3/steampunk/fusteampunk.head
items/armors/tier3/steampunk/fusteampunk.legs
items/armors/tier3/tw_fieldresearch/alts/1/researchalt1.head
items/armors/tier3/tw_fieldresearch/alts/2/researchalt2.head
items/armors/tier3/tw_fieldresearch/tw_fieldresearch.chest
items/armors/tier3/tw_fieldresearch/tw_fieldresearch.head
items/armors/tier3/tw_fieldresearch/tw_fieldresearch.legs
items/armors/tier3/tw_spacepunk/tw_spacepunk.chest
items/armors/tier3/tw_spacepunk/tw_spacepunk.head
items/armors/tier3/tw_spacepunk/tw_spacepunk.legs
items/armors/tier3/wanderer/fupioneer.chest
items/armors/tier3/wanderer/fupioneer.head
items/armors/tier3/wanderer/fupioneer.legs
items/armors/tier4/fubountyhunter/fubountyhunter.chest
items/armors/tier4/fubountyhunter/fubountyhunter.head
items/armors/tier4/fubountyhunter/fubountyhunter.legs
'''.split())

# Aktif fu_warcraft ağacındaki irradiumgear, triangliumgear, prisilitegear,
# quietusgear ve bioweaponsgear düğümlerinin açtığı, gerçek üretim tarifi
# bulunan v0.24 Kademe 4 savaş ekipmanı. Burada 148 yeni asset vardır.
V024_TIER4_REMAINING_COMBAT_ASSETS = set('''
items/active/shields/atropusshield.activeitem
items/active/shields/cuteshield.activeitem
items/active/shields/diamondshield.activeitem
items/active/shields/irradiumshield.activeitem
items/active/shields/quietusshield.activeitem
items/active/weapons/boomerang/cuteboomerang.activeitem
items/active/weapons/boomerang/quietusboomerang.activeitem
items/active/weapons/bow/carnagebow/carnagebow.activeitem
items/active/weapons/bow/cutebow/cutebow.activeitem
items/active/weapons/bow/irradiumbow/irradiumbow.activeitem
items/active/weapons/bow/prismaticbow/prismaticbow.activeitem
items/active/weapons/bow/quietusbow/quietusbow.activeitem
items/active/weapons/bow/quietuscrossbow/quietuscrossbow.activeitem
items/active/weapons/chakram/cutechakram.activeitem
items/active/weapons/fist/cutecestus.activeitem
items/active/weapons/fist/cutegauntlet.activeitem
items/active/weapons/fist/monsterclaw.activeitem
items/active/weapons/melee/axe/advalloyaxe.activeitem
items/active/weapons/melee/axe/cuteaxe.activeitem
items/active/weapons/melee/axe/fuatropusaxe.activeitem
items/active/weapons/melee/axe/irradiumaxe.activeitem
items/active/weapons/melee/axe/quietusaxe.activeitem
items/active/weapons/melee/broadsword/advalloybroadsword.activeitem
items/active/weapons/melee/broadsword/coralstinger.activeitem
items/active/weapons/melee/broadsword/coralsword.activeitem
items/active/weapons/melee/broadsword/cutebroadsword.activeitem
items/active/weapons/melee/broadsword/fuatropusbroadsword.activeitem
items/active/weapons/melee/broadsword/irradiumsword.activeitem
items/active/weapons/melee/broadsword/mineralblade.activeitem
items/active/weapons/melee/broadsword/quietusemperor.activeitem
items/active/weapons/melee/broadsword/quietusknight.activeitem
items/active/weapons/melee/broadsword/triangliumbroadsword.activeitem
items/active/weapons/melee/dagger/advalloydagger.activeitem
items/active/weapons/melee/dagger/cutedagger.activeitem
items/active/weapons/melee/dagger/fuatropusdagger.activeitem
items/active/weapons/melee/dagger/irradiumdagger.activeitem
items/active/weapons/melee/dagger/quietusknave.activeitem
items/active/weapons/melee/dagger/quietusrogue.activeitem
items/active/weapons/melee/greataxe/cutegreataxe.activeitem
items/active/weapons/melee/greataxe/fuatropusgreataxe.activeitem
items/active/weapons/melee/greataxe/irradiumgreataxe.activeitem
items/active/weapons/melee/greataxe/quietusgreataxe.activeitem
items/active/weapons/melee/hammer/advalloyhammer.activeitem
items/active/weapons/melee/hammer/cutehammer.activeitem
items/active/weapons/melee/hammer/fuatropushammer.activeitem
items/active/weapons/melee/hammer/irradiumhammer.activeitem
items/active/weapons/melee/hammer/quietushammer.activeitem
items/active/weapons/melee/katana/advalloykatana.activeitem
items/active/weapons/melee/katana/cutekatana.activeitem
items/active/weapons/melee/katana/irradiumkatana.activeitem
items/active/weapons/melee/katana/quietuskatana.activeitem
items/active/weapons/melee/katana/triangliumkatana.activeitem
items/active/weapons/melee/longsword/crystallineblade.activeitem
items/active/weapons/melee/longsword/cutelongsword.activeitem
items/active/weapons/melee/longsword/irradiumlongsword.activeitem
items/active/weapons/melee/longsword/quietusgeneral.activeitem
items/active/weapons/melee/longsword/triangliumlongsword.activeitem
items/active/weapons/melee/mace/cutemace.activeitem
items/active/weapons/melee/mace/goldmace.activeitem
items/active/weapons/melee/mace/hellfiremace.activeitem
items/active/weapons/melee/mace/irradiummace.activeitem
items/active/weapons/melee/mace/quietusmace.activeitem
items/active/weapons/melee/quarterstaff/cutequarterstaff.activeitem
items/active/weapons/melee/quarterstaff/irradiumquarterstaff.activeitem
items/active/weapons/melee/quarterstaff/quietusquarterstaff.activeitem
items/active/weapons/melee/rapier/advalloyrapier.activeitem
items/active/weapons/melee/rapier/cuterapier.activeitem
items/active/weapons/melee/rapier/diamondrapier.activeitem
items/active/weapons/melee/rapier/irradiumrapier.activeitem
items/active/weapons/melee/rapier/mineralrapier.activeitem
items/active/weapons/melee/rapier/quietusrapier.activeitem
items/active/weapons/melee/scythe/cutescythe.activeitem
items/active/weapons/melee/scythe/fuatropusscythe.activeitem
items/active/weapons/melee/scythe/irradiumscythe.activeitem
items/active/weapons/melee/scythe/quietusscythe.activeitem
items/active/weapons/melee/shortspear/advalloyshortspear.activeitem
items/active/weapons/melee/shortspear/cuteshortspear.activeitem
items/active/weapons/melee/shortspear/fuatropusshortspear.activeitem
items/active/weapons/melee/shortspear/irradiumshortspear.activeitem
items/active/weapons/melee/shortspear/quietusshortspear.activeitem
items/active/weapons/melee/shortsword/advalloyshortsword.activeitem
items/active/weapons/melee/shortsword/coralsword2.activeitem
items/active/weapons/melee/shortsword/cuteshortsword.activeitem
items/active/weapons/melee/shortsword/diamondblade.activeitem
items/active/weapons/melee/shortsword/fuatropusshortsword.activeitem
items/active/weapons/melee/shortsword/irradiumblade.activeitem
items/active/weapons/melee/shortsword/quietusassassin.activeitem
items/active/weapons/melee/shortsword/quietuscaptain.activeitem
items/active/weapons/melee/shortsword/quietusmercenary.activeitem
items/active/weapons/melee/spear/advalloyspear.activeitem
items/active/weapons/melee/spear/coralspear.activeitem
items/active/weapons/melee/spear/cutespear.activeitem
items/active/weapons/melee/spear/fuatropusspear.activeitem
items/active/weapons/melee/spear/irradiumspear.activeitem
items/active/weapons/melee/spear/quietusspear.activeitem
items/active/weapons/other/magnorbs/magnorbatropus/magnorbatropus.activeitem
items/active/weapons/ranged/unique/biogun.activeitem
items/active/weapons/ranged/unique/biopistol.activeitem
items/active/weapons/ranged/unique/blastgun.activeitem
items/active/weapons/ranged/unique/curveblaster.activeitem
items/active/weapons/ranged/unique/cutearmgun.activeitem
items/active/weapons/ranged/unique/cutemachinegun.activeitem
items/active/weapons/ranged/unique/cuteorblauncher.activeitem
items/active/weapons/ranged/unique/cutepistol.activeitem
items/active/weapons/ranged/unique/cuterocketlauncher.activeitem
items/active/weapons/ranged/unique/cuteshotgun.activeitem
items/active/weapons/ranged/unique/cutesmg.activeitem
items/active/weapons/ranged/unique/cutesniperrifle.activeitem
items/active/weapons/ranged/unique/energycutter.activeitem
items/active/weapons/ranged/unique/eyecannon.activeitem
items/active/weapons/ranged/unique/fualienlaser.activeitem
items/active/weapons/ranged/unique/furainbowgun.activeitem
items/active/weapons/ranged/unique/futriangliumpistol.activeitem
items/active/weapons/ranged/unique/futriangliumsmg.activeitem
items/active/weapons/ranged/unique/goregun.activeitem
items/active/weapons/ranged/unique/irradiumpistol2.activeitem
items/active/weapons/ranged/unique/irradiumrifle.activeitem
items/active/weapons/ranged/unique/manstopper.activeitem
items/active/weapons/ranged/unique/manstoppersmg.activeitem
items/active/weapons/ranged/unique/mineralcannon.activeitem
items/active/weapons/ranged/unique/mineralpistol.activeitem
items/active/weapons/ranged/unique/peglaci/irradiumpistol/irradiumpistol.activeitem
items/active/weapons/ranged/unique/peglaci/irradiumshotgun/irradiumshotgun.activeitem
items/active/weapons/ranged/unique/pistolquietusfu.activeitem
items/active/weapons/ranged/unique/quietusassaultrifle.activeitem
items/active/weapons/ranged/unique/quietuspistol.activeitem
items/active/weapons/ranged/unique/quietusrocketlauncher.activeitem
items/active/weapons/ranged/unique/quietusshotgun.activeitem
items/active/weapons/ranged/unique/quietussmg.activeitem
items/active/weapons/ranged/unique/quietussniper.activeitem
items/active/weapons/ranged/unique/riflequietusfu.activeitem
items/active/weapons/ranged/unique/rifletriangliumfu.activeitem
items/active/weapons/ranged/unique/science/irradiator/isn_irradiator.activeitem
items/active/weapons/ranged/unique/tinydancer.activeitem
items/active/weapons/staff/cutestaff/cutestaff.activeitem
items/active/weapons/staff/orestaffs/corruptstaff.activeitem
items/active/weapons/staff/orestaffs/irradiumstaff.activeitem
items/active/weapons/staff/orestaffs/prismaticstaff.activeitem
items/active/weapons/staff/orestaffs/quietusstaff.activeitem
items/active/weapons/wand/fubiowand/fubiowand.activeitem
items/active/weapons/wand/orewands/corruptwand.activeitem
items/active/weapons/wand/orewands/irradiumwand.activeitem
items/active/weapons/wand/orewands/prismaticwand.activeitem
items/active/weapons/wand/orewands/quietuswand.activeitem
items/active/weapons/whip/cutewhip.activeitem
items/active/weapons/whip/irradiumwhip.activeitem
items/active/weapons/whip/lasherwhip.activeitem
items/active/weapons/whip/triwhip.activeitem
'''.split())

# Aktif fu_warcraft ağacındaki advancealloygear ve durasteelgear
# düğümlerinin açtığı, gerçek üretim tarifi bulunan v0.23 Kademe 4
# çekirdek savaş ekipmanı. Burada 48 yeni asset vardır.
V023_TIER4_CORE_COMBAT_ASSETS = set('''
items/active/shields/durasteelshield.activeitem
items/active/shields/xenoshield.activeitem
items/active/weapons/boomerang/durasteelboomerang.activeitem
items/active/weapons/bow/advalloycrossbow/advalloycrossbow.activeitem
items/active/weapons/bow/advalloystynger/advalloystynger.activeitem
items/active/weapons/bow/nigtarbow/nigtarbow.activeitem
items/active/weapons/melee/axe/fucoralcleaver.activeitem
items/active/weapons/melee/axe/moltenaxe.activeitem
items/active/weapons/melee/broadsword/curvebroadsword.activeitem
items/active/weapons/melee/broadsword/energyblade.activeitem
items/active/weapons/melee/dagger/curvedagger.activeitem
items/active/weapons/melee/flail/flaildurasteel.activeitem
items/active/weapons/melee/greataxe/durasteelgreataxe.activeitem
items/active/weapons/melee/katana/durasteelkatana.activeitem
items/active/weapons/melee/longsword/advalloylongsword.activeitem
items/active/weapons/melee/mace/durasteelmace.activeitem
items/active/weapons/melee/quarterstaff/curvestaff.activeitem
items/active/weapons/melee/shortspear/durasteelshortspear.activeitem
items/active/weapons/novakid/durasteelassaultrifle2.activeitem
items/active/weapons/novakid/durasteelmachinepistol.activeitem
items/active/weapons/novakid/durasteelshotgun.activeitem
items/active/weapons/novakid/durasteelsniperrifle.activeitem
items/active/weapons/other/magnorbs/magnorbfrost/magnorbfrost.activeitem
items/active/weapons/protectorate/durasteelaxe.activeitem
items/active/weapons/protectorate/durasteeldagger.activeitem
items/active/weapons/protectorate/durasteelhammer.activeitem
items/active/weapons/protectorate/durasteelspear.activeitem
items/active/weapons/ranged/unique/advalloyshotgun.activeitem
items/active/weapons/ranged/unique/artillery/ionstrike/ionstrike.activeitem
items/active/weapons/ranged/unique/curvepistol.activeitem
items/active/weapons/ranged/unique/curvesmg.activeitem
items/active/weapons/ranged/unique/friendmaker.activeitem
items/active/weapons/ranged/unique/fucarbonhandcannon.activeitem
items/active/weapons/ranged/unique/fucellgun.activeitem
items/active/weapons/ranged/unique/fugaussmachinegun.activeitem
items/active/weapons/ranged/unique/fugausspistol.activeitem
items/active/weapons/ranged/unique/fugaussrifle.activeitem
items/active/weapons/ranged/unique/fugaussshotgun.activeitem
items/active/weapons/ranged/unique/fugausssniper.activeitem
items/active/weapons/ranged/unique/pistoldurasteelfu.activeitem
items/active/weapons/ranged/unique/rifledurasteelfu.activeitem
items/active/weapons/ranged/unique/science/microwavegun/isn_microwaveray.activeitem
items/active/weapons/ranged/unique/shurikencannon.activeitem
items/active/weapons/ranged/unique/theblackmarket/sentryguns/mobiuspistol.activeitem
items/active/weapons/ranged/unique/theblackmarket/sentryguns/mobiusrifle.activeitem
items/active/weapons/ranged/unique/theblackmarket/sentryguns/railgun/mobiusrailgun.activeitem
items/active/weapons/staff/lasereyestaff/fu_lasereyestaff.activeitem
items/active/weapons/wand/floatwand/floatstaff.activeitem
'''.split())

# Aktif fu_warcraft ağacındaki altı Kademe 3 düğümünün açtığı ve gerçek
# üretim tarifi bulunan v0.22 savaş ekipmanı. Daha önce çevrilen
# energyassault kendi eski allowlist'inde kalır; burada 157 yeni asset vardır.
V022_TIER3_COMBAT_ASSETS = set('''
items/active/shields/gladiatorshield.activeitem
items/active/shields/nightar2.activeitem
items/active/shields/penumbriteshield.activeitem
items/active/shields/titaniumshield.activeitem
items/active/shields/zerchesiumshield.activeitem
items/active/weapons/boomerang/penumbriteboomerang.activeitem
items/active/weapons/boomerang/titaniumboomerang.activeitem
items/active/weapons/boomerang/zerchesiumboomerang.activeitem
items/active/weapons/bow/carbonbow/carbonbow.activeitem
items/active/weapons/bow/carboncrossbow/carboncrossbow.activeitem
items/active/weapons/bow/carbonstynger/carbonstynger.activeitem
items/active/weapons/bow/penumbrabow/penumbrabow.activeitem
items/active/weapons/bow/protobow/protobow.activeitem
items/active/weapons/bow/zerchesiumbow/zerchesiumbow.activeitem
items/active/weapons/bow/zerchesiumcrossbow/zerchesiumcrossbow.activeitem
items/active/weapons/bow/zerchesiumstynger/zerchesiumstynger.activeitem
items/active/weapons/chakram/funeochakram.activeitem
items/active/weapons/chakram/penumbritechakram.activeitem
items/active/weapons/chakram/titaniumchakram.activeitem
items/active/weapons/chakram/zerchesiumchakram.activeitem
items/active/weapons/fist/penumbritefist.activeitem
items/active/weapons/fist/zerchesiumfist.activeitem
items/active/weapons/melee/axe/carbonaxe.activeitem
items/active/weapons/melee/axe/penumbriteaxe.activeitem
items/active/weapons/melee/axe/zerchesiumaxe.activeitem
items/active/weapons/melee/broadsword/hylotlgreatscion.activeitem
items/active/weapons/melee/broadsword/metalliccleaver.activeitem
items/active/weapons/melee/broadsword/metallicsword.activeitem
items/active/weapons/melee/broadsword/penumbritebroadsword.activeitem
items/active/weapons/melee/broadsword/titaniumbroadsword.activeitem
items/active/weapons/melee/broadsword/zerchesiumbroadsword.activeitem
items/active/weapons/melee/dagger/carbondagger.activeitem
items/active/weapons/melee/dagger/nightardagger.activeitem
items/active/weapons/melee/dagger/penumbriredagger.activeitem
items/active/weapons/melee/dagger/zerchesiumknife.activeitem
items/active/weapons/melee/flail/flailpenumbrite.activeitem
items/active/weapons/melee/flail/flailtitanium.activeitem
items/active/weapons/melee/flail/flailzerchesium.activeitem
items/active/weapons/melee/greataxe/nightarwarblade.activeitem
items/active/weapons/melee/greataxe/penumbritegreataxe.activeitem
items/active/weapons/melee/greataxe/titaniumgreataxe.activeitem
items/active/weapons/melee/greataxe/zerchesiumgreataxe.activeitem
items/active/weapons/melee/hammer/fucarbonhammer.activeitem
items/active/weapons/melee/hammer/kelpsteelhatchet.activeitem
items/active/weapons/melee/hammer/metallichammer.activeitem
items/active/weapons/melee/hammer/penumbritehammer.activeitem
items/active/weapons/melee/hammer/zerchesiumhammer.activeitem
items/active/weapons/melee/katana/carbonkatana.activeitem
items/active/weapons/melee/katana/coralkatana.activeitem
items/active/weapons/melee/katana/penumbritekatana.activeitem
items/active/weapons/melee/katana/titaniumkatana.activeitem
items/active/weapons/melee/katana/zerchesiumkatana.activeitem
items/active/weapons/melee/longsword/carbonlongsword.activeitem
items/active/weapons/melee/longsword/coraldullblade.activeitem
items/active/weapons/melee/longsword/kaicleaver.activeitem
items/active/weapons/melee/longsword/penumbritelongsword.activeitem
items/active/weapons/melee/longsword/titaniumlongsword.activeitem
items/active/weapons/melee/longsword/zerchesiumlongsword.activeitem
items/active/weapons/melee/mace/ballmace.activeitem
items/active/weapons/melee/mace/penumbramace.activeitem
items/active/weapons/melee/mace/titaniummace.activeitem
items/active/weapons/melee/mace/zerchesiummace.activeitem
items/active/weapons/melee/quarterstaff/carbonquarterstaff.activeitem
items/active/weapons/melee/quarterstaff/goldquarterstaff.activeitem
items/active/weapons/melee/quarterstaff/penumbritestaff.activeitem
items/active/weapons/melee/quarterstaff/zerchesiumquarterstaff.activeitem
items/active/weapons/melee/rapier/penumbriterapier.activeitem
items/active/weapons/melee/rapier/zerchesiumrapier.activeitem
items/active/weapons/melee/scythe/penumbralscythe.activeitem
items/active/weapons/melee/scythe/zerchesiumscythe.activeitem
items/active/weapons/melee/shortspear/carbonshortspear.activeitem
items/active/weapons/melee/shortspear/penumbriteshortspear.activeitem
items/active/weapons/melee/shortspear/titaniumshortspear.activeitem
items/active/weapons/melee/shortspear/zerchesiumshortspear.activeitem
items/active/weapons/melee/shortsword/carbonblade.activeitem
items/active/weapons/melee/shortsword/fushroomsword.activeitem
items/active/weapons/melee/shortsword/hylotllesserscion.activeitem
items/active/weapons/melee/shortsword/nightarshortsword.activeitem
items/active/weapons/melee/shortsword/penumbriteshortsword.activeitem
items/active/weapons/melee/shortsword/zerchesiumsword.activeitem
items/active/weapons/melee/spear/carbonspear.activeitem
items/active/weapons/melee/spear/metallicspear.activeitem
items/active/weapons/melee/spear/penumbritespear.activeitem
items/active/weapons/melee/spear/siliconspear.activeitem
items/active/weapons/melee/spear/wraithwind.activeitem
items/active/weapons/melee/spear/zerchesiumspear.activeitem
items/active/weapons/novakid/titaniumassaultrifle.activeitem
items/active/weapons/novakid/titaniumrevolver.activeitem
items/active/weapons/novakid/titaniumshotgun.activeitem
items/active/weapons/other/magnorbs/magnorbpenumbrite/magnorbpenumbrite.activeitem
items/active/weapons/other/magnorbs/magnorbproto/magnorbproto.activeitem
items/active/weapons/other/magnorbs/magnorbzerchesium/magnorbzerchesium.activeitem
items/active/weapons/protectorate/titaniumaxe.activeitem
items/active/weapons/protectorate/titaniumhammer.activeitem
items/active/weapons/protectorate/titaniumshortsword.activeitem
items/active/weapons/ranged/assaultrifle/floranneedler.activeitem
items/active/weapons/ranged/unique/artillery/airstrike/airstrike.activeitem
items/active/weapons/ranged/unique/blizzardcannon.activeitem
items/active/weapons/ranged/unique/carbonshotgun.activeitem
items/active/weapons/ranged/unique/carvelle.activeitem
items/active/weapons/ranged/unique/crankgun.activeitem
items/active/weapons/ranged/unique/crankpistol.activeitem
items/active/weapons/ranged/unique/crankrifle.activeitem
items/active/weapons/ranged/unique/discrifle.activeitem
items/active/weapons/ranged/unique/fu_liquidguns/biooozegun.activeitem
items/active/weapons/ranged/unique/fu_liquidguns/healingliquidgun.activeitem
items/active/weapons/ranged/unique/fu_liquidguns/liquidacidgun.activeitem
items/active/weapons/ranged/unique/fu_liquidguns/liquidpoisongun.activeitem
items/active/weapons/ranged/unique/fugrinder.activeitem
items/active/weapons/ranged/unique/funomadassaultrifle.activeitem
items/active/weapons/ranged/unique/funomadrifle.activeitem
items/active/weapons/ranged/unique/ionrifle.activeitem
items/active/weapons/ranged/unique/k3rifle.activeitem
items/active/weapons/ranged/unique/longarm.activeitem
items/active/weapons/ranged/unique/longarmpistol.activeitem
items/active/weapons/ranged/unique/miners/weaponminer/weaponminer.activeitem
items/active/weapons/ranged/unique/minirocketlauncher.activeitem
items/active/weapons/ranged/unique/murdermanipulator.activeitem
items/active/weapons/ranged/unique/mushroomgun.activeitem
items/active/weapons/ranged/unique/napalmcannon.activeitem
items/active/weapons/ranged/unique/peglaci/burstgun/chargeshotgun.activeitem
items/active/weapons/ranged/unique/peglaci/glacialpistol/chargepistol.activeitem
items/active/weapons/ranged/unique/penumbriteassaultrifle.activeitem
items/active/weapons/ranged/unique/penumbritepistol.activeitem
items/active/weapons/ranged/unique/penumbriterocketlauncher.activeitem
items/active/weapons/ranged/unique/penumbriteshotgun.activeitem
items/active/weapons/ranged/unique/penumbritesmg.activeitem
items/active/weapons/ranged/unique/penumbritesniperrifle.activeitem
items/active/weapons/ranged/unique/pistolprotofu.activeitem
items/active/weapons/ranged/unique/pistoltitaniumfu.activeitem
items/active/weapons/ranged/unique/protogun.activeitem
items/active/weapons/ranged/unique/protopistol.activeitem
items/active/weapons/ranged/unique/protorifle.activeitem
items/active/weapons/ranged/unique/rifletitaniumfu.activeitem
items/active/weapons/ranged/unique/science/flamepistol/isn_flamethrower.activeitem
items/active/weapons/ranged/unique/science/kineticrifle/kineticrifle.activeitem
items/active/weapons/ranged/unique/science/napalmsprayer/isn_napalmsprayer.activeitem
items/active/weapons/ranged/unique/silverslayer.activeitem
items/active/weapons/ranged/unique/snubber.activeitem
items/active/weapons/ranged/unique/teslagun.activeitem
items/active/weapons/ranged/unique/zerchesiumassaultrifle.activeitem
items/active/weapons/ranged/unique/zerchesiumpistol.activeitem
items/active/weapons/ranged/unique/zerchesiumrocketlauncher.activeitem
items/active/weapons/ranged/unique/zerchesiumshotgun.activeitem
items/active/weapons/ranged/unique/zerchesiumsmg.activeitem
items/active/weapons/ranged/unique/zerchesiumsniper.activeitem
items/active/weapons/staff/orestaffs/penumbrastaff.activeitem
items/active/weapons/staff/orestaffs/protocitestaff.activeitem
items/active/weapons/staff/orestaffs/zerchesiumstaff.activeitem
items/active/weapons/wand/fupoisonwand/fupoisonwand.activeitem
items/active/weapons/wand/orewands/penumbrawand.activeitem
items/active/weapons/wand/orewands/protocitewand.activeitem
items/active/weapons/wand/teslawand/teslastaff1.activeitem
items/active/weapons/whip/carbonwhip.activeitem
items/active/weapons/whip/corewhip.activeitem
items/active/weapons/whip/penumbritewhip.activeitem
items/active/weapons/whip/zerchesiumwhip.activeitem
'''.split())

# v0.22 görev metninde Usta Manipülatör olarak anılan iki erişilebilir
# eşyanın oyuncuya gösterilen alanları. Kırık augment Khe görevinden gelir;
# tamamlanmış araç da Nanoüretici tarifinin gerçek çıktısıdır.
V022_MASTER_MANIPULATOR_ASSETS = {
    'items/augments/quest/humanartifact.augment',
    'items/tools/fumastermanipulator.beamaxe',
}

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

# v0.17: objects/crafting ağacındaki daha önce çevrilmemiş etkin üretim nesneleri.
V017_CRAFTING_ASSETS = {
    'objects/crafting/armory/armoryoutpost.object',
    'objects/crafting/bothealingstation/pethealingstation.object',
    'objects/crafting/bothealingstation/pethealingstationauto.object',
    'objects/crafting/catalystfuelrefinery/catalystfuelrefinery.object',
    'objects/crafting/chemlab/chemlaboutpost.object',
    'objects/crafting/clothingfabricator/clothingfabricator.object',
    'objects/crafting/designlab/designlaboutpost.object',
    'objects/crafting/eggstra/chickennest/chickennest.object',
    'objects/crafting/eggstra/cowbell/cowbell.object',
    'objects/crafting/eggstra/eggincubator/eggincubator.object',
    'objects/crafting/eggstra/farmclock/farmclock.object',
    'objects/crafting/eggstra/largetrough/irontrough.object',
    'objects/crafting/eggstra/largetrough/largetrough.object',
    'objects/crafting/elderhealingstation/elderhealingstation.object',
    'objects/crafting/elderhealingstation/pethealingstationauto.object',
    'objects/crafting/elduu/crystalloom/crystalloom.object',
    'objects/crafting/elduu/furniturestation/furniturestation.object',
    'objects/crafting/elduu/gemstation/gemstation.object',
    'objects/crafting/extraavianaugments/extraavianaugments.object',
    'objects/crafting/extraweaponupgradeanvil/extraweaponupgradeanvil.object',
    'objects/crafting/farmwell/farmwell.object',
    'objects/crafting/fissionfurnacenew/fissionfurnacenew.object',
    'objects/crafting/fu_petrenamer/fu_petrenamer.object',
    'objects/crafting/fu_racialiser/fu_racialiser.object',
    'objects/crafting/fu_racializer/fu_racializer.object',
    'objects/crafting/fu_upgradetable/fu_upgradetable.object',
    'objects/crafting/fuincubator/fuincubator.object',
    'objects/crafting/fuwaterbarrel/fuwaterbarrel.object',
    'objects/crafting/genesequencer/genesequencer.object',
    'objects/crafting/liquidpumpwell/liquidpumpwell.object',
    'objects/crafting/lobstertrap/lobstertrap.object',
    'objects/crafting/madnesscodex/madnesscodex.object',
    'objects/crafting/matterassembler/prototyperoutpost.object',
    'objects/crafting/mechfuelrefinery/fuelrefinery.object',
    'objects/crafting/medievalworkstation/medievalworkstation.object',
    'objects/crafting/miningbench/miningbench.object',
    'objects/crafting/miningbench/weaponshuffler.object',
    'objects/crafting/nanofabricator/nanofabricator.object',
    'objects/crafting/nanofabricator/nanofabricatoroutpost.object',
    'objects/crafting/pesttrap/pesttrap.object',
    'objects/crafting/pethealingstation/pethealingstationauto.object',
    'objects/crafting/petpicrepair/petpicrepair.object',
    'objects/crafting/pixelcompressor/hypercompressor.object',
    'objects/crafting/platingtable/platingtable.object',
    'objects/crafting/powerstation/powerstatiooutpost.object',
    'objects/crafting/ppshopmini/ppshopmini.object',
    'objects/crafting/ppshoptruck/ppshoptruck.object',
    'objects/crafting/radiencrafting/radiencrafting.object',
    'objects/crafting/servitorloader/servitorloader.object',
    'objects/crafting/shrineofsouls/shrineofsouls.object',
    'objects/crafting/slimecookingtable/slimecookingtable.object',
    'objects/crafting/slimefire/slimefire.object',
    'objects/crafting/weaponupgradeanvil2/fuweaponupgradeanvil.object',
    'objects/crafting/xiwell/xiwell.object',
}

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

def allowed(a,p):
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
    outpost_kevin_khe_assets={
        'items/armors/tier1/booster/kirhosbooster.chest',
        'items/generic/crafting/algaegreen.item',
        'items/generic/crafting/chemlab/biofuelcannister.item',
        'items/generic/loot/babyheadonastick.consumable',
        'items/generic/crafting/blooddiamond.item',
        'items/generic/crafting/brain.item',
        'items/generic/crafting/isotopes/antineutronium.item',
        'items/generic/crafting/isotopes/neutronium.item',
        'items/generic/crafting/pureerchius.item',
        'items/active/flashlights/lanterror/lanterror.activeitem',
        'items/generic/other/killpod.consumable',
        'items/throwables/neutronbomb.thrownitem',
        'items/throwables/beebriefcase/fu_beebriefcasekevin.activeitem',
        'items/generic/loot/mission/luckycoin_khe.item',
        'items/generic/loot/mission/temple_trophy_khe.item',
        'items/generic/produce/orange.consumable',
        'items/generic/crafting/goldbar.item',
        'items/generic/crafting/diamond.item',
        'items/generic/crafting/crystal.item',
        'items/generic/crafting/corefragmentore.item'
    }
    if a in outpost_kevin_khe_assets:
        return p in ('/description','/shortdescription') or (a=='items/throwables/beebriefcase/fu_beebriefcasekevin.activeitem' and p=='/notOnPlanetMessage')
    battle_target_assets={
        'items/active/weapons/ranged/unique/theblackmarket/armcannon/armcannon.activeitem',
        'items/active/weapons/ranged/unique/energyassault.activeitem',
        'items/active/weapons/ranged/unique/laspistol.activeitem',
        'items/active/weapons/melee/shortsword/hardenedsteelblade.activeitem',
        'items/active/weapons/melee/broadsword/warcleaver.activeitem',
        'items/armors/tier1/plebeian/mantizitier1.head',
        'items/active/shields/furelicshield.activeitem',
        'items/active/weapons/melee/axe/poptopclaw.activeitem',
        'items/active/grapplinghooks/websnapper/websnapper.activeitem',
        'items/augments/quest/warbotartifact.augment'
    }
    if a in battle_target_assets:
        return p in ('/description','/shortdescription') or (a=='items/augments/quest/warbotartifact.augment' and p=='/augment/displayName')
    remaining_quest_target_assets={
        'items/armors/tier6/densiniumarmor/densinium.head',
        'objects/minibiome/elder/elderstatue.object',
        'items/generic/crafting/moltencore.item',
        'items/generic/crafting/shoggothflesh.item',
        'items/generic/mission/wagneridcard.item',
        'items/generic/crafting/mythos/fugrimoire.item',
        'items/active/unsorted/precursorkey/sciencebrochure2.activeitem',
        'objects/ship/fu_crewbed0/fu_crewbed0.object',
        'objects/ship/fu_crewdeed/fu_crewdeed.object',
        'objects/questturnins/elderturnin.object',
        'objects/questturnins/precursorturnin.object'
    }
    if a in remaining_quest_target_assets:
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
    if a=='objects/bees/ironcentrifuge/ironcentrifuge.object':
        return p in ('/description','/shortdescription','/subtitle','/category')
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
        if a in V018_DEAD_OBJECT_ASSETS:raise ValueError('Runtime bağlantısı olmayan v0.18 nesnesi: '+a)
        if a in V019_DEAD_CRAFTING_ITEM_ASSETS:raise ValueError('Runtime bağlantısı olmayan/deprecated v0.19 üretim eşyası: '+a)
        if a in V020_INACTIVE_QUEST_ASSETS:raise ValueError('Oyuncuya görünmeyen/erişilemeyen v0.20 görevi: '+a)
        if not allowed(a,p):raise ValueError('Oyuncu metni olmayan alan: '+a+p)
        if nonvisible_research_pointer(a,p):raise ValueError('Aktif araştırma düğümüne bağlı olmayan metin: '+a+p)
        if a in NONVISIBLE_QUEST_ASSETS:raise ValueError('Aktif görev zincirine bağlı olmayan/kırık görev: '+a)
        if 'İngilizce adı:' in r['tr']:raise ValueError('İngilizce fallback/gloss: '+a+p)
        if r['en'].strip()=='Replace Me':raise ValueError('Runtime listTemplate dummy metni kataloğa alınamaz: '+a+p)
        if any(x in r['tr'] for x in BAD_TR_PATTERNS):raise ValueError('Bilinen Türkçe LQA hatası: '+a+p)
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
        if Counter(BRACE_PLACEHOLDER.findall(r['en']))!=Counter(BRACE_PLACEHOLDER.findall(r['tr'])):
            raise ValueError('Süslü parantez yer tutucusu uyuşmazlığı: '+a+p)
        if Counter(DOLLAR_PLACEHOLDER.findall(r['en']))!=Counter(DOLLAR_PLACEHOLDER.findall(r['tr'])):
            raise ValueError('Değişken yer tutucusu uyuşmazlığı: '+a+p)
        if r['en'].count('\n')!=r['tr'].count('\n'):
            raise ValueError('Satır sonu uyuşmazlığı: '+a+p)
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
    metadata={'name':'FU_Turkce','friendlyName':'FU Türkçe (Beta)',
      'author':'FU Türkçe',
      'version':ledger['translation_version'],
      'description':"Frackin' Universe için devam eden Türkçe yerelleştirme. Araştırma, görevler, üretim, temel makineler, işlevsel nesneler ve geniş ekipman kapsamını içerir.",
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
