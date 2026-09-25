import json
import struct
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from custom_assets import load_custom_assets


class EbrarAssetTests(unittest.TestCase):
    def test_object_art_recipe_and_deployment_are_consistent(self):
        assets = load_custom_assets(TOOLS)
        base = 'objects/decorative/futrebrarstar/'
        obj = json.loads(assets[base + 'futrebrarstar.object'])
        self.assertEqual(obj['objectName'], 'futrebrarstar')
        self.assertIn('Ebrar', obj['shortdescription'])
        self.assertIn('sevgilisi', obj['description'])
        self.assertIn('Ebrar, bu evrendeki en güzel keşfim sensin.', obj['humanDescription'])
        self.assertEqual(obj['orientations'][0]['anchors'], ['background'])
        for image in ('ebrarstar.png', 'ebrarstarlit.png', 'ebrarstaricon.png'):
            data = assets[base + image]
            self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II', data[16:24]), (16, 16))
        self.assertEqual(obj['inventoryIcon'], 'ebrarstaricon.png')
        for layer in obj['orientations'][0]['imageLayers']:
            self.assertIn(base + layer['image'], assets)
        recipe = json.loads(assets['recipes/emptyhands/futrebrarstar.recipe'])
        self.assertEqual(recipe['output']['item'], obj['objectName'])
        self.assertIn('plain', recipe['groups'])
        deployment = json.loads(assets['player.config.patch'])
        self.assertEqual(deployment, [
            [{'op': 'add', 'path': '/deploymentConfig/scripts/-',
              'value': '/scripts/fu_tr_ebrar_ship.lua'}],
            [{'op': 'add', 'path': '/defaultBlueprints/tier1/-',
              'value': {'item': obj['objectName']}}],
        ])
        fixture = {'deploymentConfig': {'scripts': ['/scripts/existing.lua']},
                   'defaultBlueprints': {'tier1': [{'item': 'existing'}]}}
        for batch in deployment:
            self.assertEqual(len(batch), 1)
            operation = batch[0]
            parent = fixture
            for component in operation['path'].strip('/').split('/')[:-1]:
                parent = parent[component]
            parent.append(operation['value'])
        self.assertEqual(fixture['deploymentConfig']['scripts'],
                         ['/scripts/existing.lua', '/scripts/fu_tr_ebrar_ship.lua'])
        self.assertEqual(fixture['defaultBlueprints']['tier1'][-1]['item'], obj['objectName'])
        self.assertIn('scripts/fu_tr_ebrar_ship.lua', assets)


if __name__ == '__main__':
    unittest.main()
