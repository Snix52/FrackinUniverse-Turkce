"""Screenshot-linked source regressions. Host stubs are not in-game LQA."""
import json
import os
import struct
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit
import build_validate as build
import test_lua_behavior as lua_host


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


class UiLqaSourceTests(unittest.TestCase):
    def test_manifest_and_short_labels_match_catalog(self):
        spec = read(TOOLS / 'ui_lqa_20260925.json')
        rows = read(TOOLS / 'v0651_translations.json')['translations']
        catalog = read(TOOLS / 'ceviriler.json')
        index = {(r['asset'], r['pointer']): r for r in catalog['translations']}
        self.assertEqual(len(rows), 11)
        for row in rows:
            self.assertEqual(index[row['asset'], row['pointer']], row)
            self.assertTrue(build.allowed(row['asset'], row['pointer']))
            self.assertFalse(build.allowed(row['asset'], '/scriptDelta'))
        for asset, pointer, en, old, tr, limit in spec['ui_edits']:
            self.assertEqual(index[asset, pointer]['tr'], tr)
            self.assertLessEqual(len(tr), limit)
        self.assertEqual(audit.visible_confidence('_FUversioning.config', ['welcome'], 'Welcome!'), 'confirmed')
        self.assertEqual(audit.category_for('_FUversioning.config'), 'Arayüz')

    def test_native_mech_labels_keep_fuel_identifiers_and_callbacks(self):
        path = 'interface/mechfuel/mechfuel.config'
        config = audit.parse_jsonc((TOOLS / 'raw_overrides' / path).read_text(encoding='utf-8'))
        spec = read(TOOLS / 'ui_lqa_20260925.json')
        self.assertEqual(set(config['fuelTypes']), set(spec['fuel_display_names']))
        for code, tr in spec['fuel_display_names'].items():
            self.assertEqual(config['fuelTypes'][code]['displayName'], tr)
        for fuel in config['fuels'].values():
            self.assertIn(fuel['fuelType'], config['fuelTypes'])
        self.assertEqual(config['gui']['btnUpgrade']['callback'], 'fuel')
        self.assertEqual(config['gui']['btnEmpty']['callback'], 'emptyfuel')
        self.assertEqual(config['gui']['btnUpgrade']['caption'], 'DOLDUR')
        self.assertEqual(config['gui']['btnEmpty']['caption'], 'BOŞALT')
        self.assertEqual(config['scriptWidgetCallbacks'], ['insertFuel', 'fuel', 'emptyfuel'])
        self.assertEqual(len([key for key in config['gui'] if key.startswith('fuTrFuelLegend')]), 8)
        rows = [r for r in read(TOOLS / 'ceviriler.json')['translations'] if r['asset'] == path]
        patched = build.simulate(config, build.translation_patch(path, rows))
        for row in rows:
            self.assertEqual(build.read_at(patched, row['pointer']), row['tr'])

    def test_source_derived_images_have_safe_inventory_and_original_dimensions(self):
        spec = read(TOOLS / 'ui_lqa_20260925.json')
        inventory = read(TOOLS / 'custom_assets.json')['assets']
        self.assertEqual(len(spec['image_sources']), 7)
        for name in spec['image_sources']:
            asset = 'interface/fu_turkce/mechfuel/' + name
            self.assertIn(asset, inventory)
            data = (TOOLS / 'custom_assets' / asset).read_bytes()
            self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
            expected = (345, 197) if name == 'body.png' else ((86, 18) if name.startswith('deploy') else (52, 18))
            self.assertEqual(struct.unpack('>II', data[16:24]), expected)

    def test_welcome_keeps_newlines_and_explicit_source_variant(self):
        row = next(r for r in read(TOOLS / 'v0651_translations.json')['translations'] if r['pointer'] == '/welcome')
        self.assertEqual(row['en'].count('\n'), row['tr'].count('\n'))
        self.assertEqual(len(row['qa']['source_newline_pattern']), row['en'].count('\n'))
        self.assertNotIn('\r', row['en'])
        self.assertTrue(set(row['qa']['source_newline_pattern']) <= {'L', 'C'})
        self.assertFalse(build.allowed('_FUversioning.config', '/version'))


class UiLqaLuaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lua_host.LuaBehaviorTests.setUpClass.__func__(cls)

    execute = lua_host.LuaBehaviorTests.execute
    string_at = lua_host.LuaBehaviorTests.string_at

    def source(self, asset):
        directory = Path(os.environ.get('FU_TEST_MOD_DIR', str(TOOLS / 'raw_overrides')))
        return 'require = function(...) end\n' + (directory / asset).read_text(encoding='utf-8') + '\n'

    def test_mech_display_names_loading_and_empty_preserve_codes(self):
        self.execute(self.source('interface/mechfuel/mechfuel.lua') + '''
local shown = {}
widget = {setText = function(key, value) shown[key] = value end}
self = {fuelTypes = {Oil = {textColor = 'gray', displayName = 'Yağ'}, Addon = {textColor = 'blue'}}, currentFuelType = 'Oil'}
setFuelTypeText('Oil')
assert(shown.lblFuelType == 'YAKIT: ^gray;Yağ')
assert(self.currentFuelType == 'Oil')
setFuelTypeText('Addon')
assert(shown.lblFuelType == 'YAKIT: ^blue;Addon')
setFuelTypeText(nil)
assert(shown.lblFuelType == 'YAKIT: ^red;BOŞ^reset;')
fuelCountPreview({name = 'liquidoil', count = 1})
assert(shown.lblModuleCount == '^red;Yükleniyor^reset;')
AUDIT_OUTPUT = 'PASS'
''')

    def test_gps_ship_modes_preserve_stats_and_properties(self):
        self.execute(self.source('interface/kukagps/kukagps.lua') + '''
local rows, props = {}, {fu_byos = true}
widget = {
 clearListItems = function() rows = {} end,
 addListItem = function() return tostring(#rows + 1) end,
 setText = function(key, text) table.insert(rows, text) end
}
local upgrades = {fuelEfficiency = 0.1, maxFuel = 10000, shipSpeed = 71, shipLevel = 8, capabilities = {'systemTravel'}}
player = {worldId = function() return 'ClientShipWorld:test' end, shipUpgrades = function() return upgrades end}
world = {getProperty = function(key) return props[key] end}
contains = function(values, expected) for _, v in pairs(values) do if v == expected then return true end end return false end
local function output() populateMaterialsList() return table.concat(rows, '\\n') end
local text = output()
assert(text:find('Şu anda gemidesin', 1, true))
assert(text:find('Küçük FTL Motoru', 1, true))
assert(text:find('10000', 1, true) and text:find('71', 1, true))
assert(text:find('10%', 1, true))
props['fu_byos.planetTravel'] = 1
assert(output():find('STL Motoru', 1, true))
props['fu_byos.systemTravel'] = 1
assert(output():find('her yere yolculuk', 1, true))
props.fu_byos = false
assert(output():find('Ana oyun gemisi', 1, true))
upgrades.capabilities = {}
assert(output():find('Esther Bright', 1, true))
assert(upgrades.maxFuel == 10000 and upgrades.shipSpeed == 71)
AUDIT_OUTPUT = 'PASS'
''')

    def test_sail_atmosphere_text_does_not_change_toggle_logic(self):
        self.execute(self.source('zb/newSail/fu_customFunctions.lua') + '''
local props = {['ship.level'] = 0}
local text
player = {worldId = function() return 'own' end, ownShipWorldId = function() return 'own' end}
world = {getProperty = function(k) return props[k] end, setProperty = function(k,v) props[k] = v end}
resetGUI = function() end
cfg = {TextData = {}}
textTyper = {init = function(_, value) text = value end}
fu_toggleAtmosphereMode()
assert(props['fu_byos.newAtmosphereSystem'] == true)
assert(text:find('kapalı bir odada', 1, true))
fu_toggleAtmosphereMode()
assert(props['fu_byos.newAtmosphereSystem'] == false)
assert(text:find('arka plan duvarı', 1, true))
player.worldId = function() return 'other' end
fu_toggleAtmosphereMode()
assert(text:find('geminin sahibi', 1, true))
assert(props['fu_byos.newAtmosphereSystem'] == false)
AUDIT_OUTPUT = 'PASS'
''')


if __name__ == '__main__':
    unittest.main()
