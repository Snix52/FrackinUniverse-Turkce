import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import audit_remaining as audit
import plan_translation as planner


def candidate(asset, pointer='/description', en='Example text', pool='confirmed'):
    return dict(asset=asset, pointer=pointer, en=en, origin=asset, family=planner.family(asset),
                priority='P1', pool=pool)


class PlanningTests(unittest.TestCase):
    def test_context_does_not_merge_speakers_or_inspection_voices(self):
        rows = [candidate('objects/crafting/a/a.object'), candidate('objects/crafting/b/b.object'),
                candidate('objects/crafting/a/a.object', '/floranDescription'),
                candidate('objects/crafting/a/a.object', '/glitchDescription'),
                candidate('objects/ship/a/a.object', '/dialog/wakeUp/0/0'),
                candidate('objects/ship/b/b.object', '/dialog/wakeUp/0/0')]
        units = planner.units_for(rows, {})
        self.assertEqual(len(units), 5)
        self.assertEqual(sorted(len(u['occurrences']) for u in units), [1, 1, 1, 1, 2])

    def test_tm_exceptions_force_field_level_context(self):
        rows = [candidate('objects/crafting/a/a.object'), candidate('objects/crafting/b/b.object')]
        self.assertEqual(len(planner.units_for(rows, {'exceptions': [{'en': 'Example text'}]})), 2)

    def test_exact_source_keeps_newlines_and_case(self):
        rows = [candidate('objects/crafting/a/a.object', en='Read\nthis'),
                candidate('objects/crafting/b/b.object', en='Read this'),
                candidate('objects/crafting/c/c.object', en='read this')]
        self.assertEqual(len(planner.units_for(rows, {})), 3)

    def test_tm_conflicts_are_suggestions_and_keep_tr_blank(self):
        units = planner.units_for([candidate('objects/crafting/a/a.object')], {})
        planner.enrich(units, [dict(asset='x.item', pointer='/description', en='Example text', tr='A'),
                               dict(asset='y.item', pointer='/description', en='Example text', tr='B')], {'terms': []})
        self.assertTrue(units[0]['tm_conflict'])
        self.assertEqual(len(units[0]['tm_suggestions']), 2)
        self.assertIsNone(units[0]['tr'])
        self.assertFalse(units[0]['context_reviewed'])

    def test_priority_and_uncertain_pool_are_independent(self):
        policy = planner.read(planner.TOOLS / 'translation_priorities.json')
        self.assertEqual(planner.priority(candidate('quests/example.questtemplate'), policy)[0], 'P0')
        self.assertEqual(planner.priority(candidate('objects/ship/example.object', '/dialog/wakeUp/0/0'), policy)[0], 'P1')
        self.assertEqual(planner.priority(candidate('codex/example.codex'), policy)[0], 'P3')
        rows = [candidate('interface/test.config', pool='review'), candidate('objects/crafting/a/a.object')]
        fam, units, _, _ = planner.choose(rows, None, 500, 350, {})
        self.assertEqual(fam, 'objects/crafting')
        self.assertEqual(len(units), 1)

    def test_dialogue_first_keeps_critical_priority_and_review_pool(self):
        policy = planner.read(planner.TOOLS / 'translation_priorities.json')
        for asset, pointer in [('dialog/converse.config', '/converse/default/0'),
                               ('radiomessages/test.radiomessages', '/message/text'),
                               ('npcs/crew/test.npctype', '/scriptConfig/dialog/converse/0'),
                               ('objects/themed/example.object', '/chatOptions/0')]:
            with self.subTest(asset=asset):
                self.assertEqual(planner.priority(candidate(asset, pointer), policy)[0], 'P1')
        self.assertEqual(planner.priority(candidate('quests/test.questtemplate', '/text'), policy)[0], 'P0')
        self.assertEqual(planner.priority(candidate('objects/themed/example.object'), policy)[0], 'P3')
        raw = {'asset': 'npcs/crew/test.npctype', 'pointer': '/scriptConfig/dialog/converse/0',
               'value': 'Example speech', 'origin': 'npcs/crew/test.npctype', 'confidence': 'review'}
        queued = planner.queue_rows({'remaining_rows': [raw], 'lua_review': {'rows': []}}, policy)[0]
        self.assertEqual((queued['priority'], queued['pool']), ('P1', 'review'))

    def test_gameplay_keys_raise_machine_priority_outside_crafting_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'objects/themed/example.object.patch'
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps([{'op': 'add', 'path': '/interactAction',
                                         'value': 'OpenCraftingInterface'}]), encoding='utf-8')
            hints = planner.asset_role_hints(root, ['objects/themed/example.object'])
            raw = {'asset': 'objects/themed/example.object', 'pointer': '/description',
                   'origin': 'objects/themed/example.object.patch#0', 'value': 'Example',
                   'confidence': 'confirmed'}
            report = {'remaining_rows': [raw], 'lua_review': {'rows': []}}
            rows = planner.queue_rows(report, planner.read(planner.TOOLS / 'translation_priorities.json'), hints)
            self.assertEqual(rows[0]['priority'], 'P1')
            self.assertEqual(rows[0]['priority_rule'], 'interactive-system')
            self.assertEqual(rows[0]['gameplay_hints'][0]['pointer'], '/interactAction')
            raw['pointer'] = '/floranDescription'
            rows = planner.queue_rows(report, planner.read(planner.TOOLS / 'translation_priorities.json'), hints)
            self.assertEqual(rows[0]['priority'], 'P3')

    def test_limits_preserve_entire_groups_and_do_not_skip_oversized_first(self):
        rows = [candidate('objects/crafting/a/a.object'), candidate('objects/crafting/b/b.object')]
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            planner.choose(rows, None, 1, 350, {})
        self.assertEqual(len(planner.choose(rows, None, 2, 1, {})[1][0]['occurrences']), 2)

    def test_full_audit_export_does_not_change_existing_totals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source'
            source.mkdir()
            (source / 'example.object').write_text(json.dumps({'shortdescription': 'Object name',
                                                              'description': 'Object text'}), encoding='utf-8')
            catalog = root / 'catalog.json'
            catalog.write_text('{"translations": []}', encoding='utf-8')
            compact = audit.audit(source, catalog)
            expanded = audit.audit(source, catalog, include_rows=True)
            self.assertEqual(compact['remaining'], expanded['remaining'])
            self.assertEqual(len(expanded['remaining_rows']), 2)
            self.assertNotIn('remaining_rows', compact)

    def test_all_lua_review_rows_and_long_text_are_exported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text = 'Visible sentence ' + 'x' * 600
            (root / 'example.lua').write_text('\n'.join(
                'widget.setText("label", "' + text + str(i) + '")' for i in range(105)), encoding='utf-8')
            report = audit.audit_lua(root, root / 'missing.json', include_rows=True)
            self.assertEqual(len(report['rows']), 105)
            self.assertEqual(len(report['samples']), 100)
            self.assertEqual(report['rows'][0]['source'], text + '0')

    def test_hidden_ship_trackers_do_not_enter_translation_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source'
            path = source / 'frackinship/quests'
            path.mkdir(parents=True)
            data = {'title': 'Hidden tracker', 'text': 'Tracker text',
                    'completionText': 'Tracker completed', 'showInLog': False,
                    'showAcceptDialog': False, 'showCompleteDialog': False,
                    'showFailDialog': False, 'scriptConfig': {'portraits': {'default': 'sail'}}}
            for name in ('fu_byos', 'fu_shipupgrades'):
                (path / (name + '.questtemplate')).write_text(json.dumps(data), encoding='utf-8')
            # A visible neighbouring quest must remain in the audit.
            data.update(title='Visible quest', showInLog=True, showAcceptDialog=True)
            (path / 'visible.questtemplate').write_text(json.dumps(data), encoding='utf-8')
            catalog = root / 'catalog.json'
            catalog.write_text('{"translations": []}', encoding='utf-8')
            report = audit.audit(source, catalog, include_rows=True)
            rows = report['remaining_rows']
            self.assertTrue(rows)
            self.assertEqual({row['asset'] for row in rows},
                             {'frackinship/quests/visible.questtemplate'})

    def test_p0_quest_identifiers_and_gui_controls_stay_out_but_bookmark_name_is_visible(self):
        quest = 'quests/story/gaterepair.questtemplate'
        self.assertIsNone(audit.visible_confidence(quest,
            ['scriptConfig', 'portraits', 'questStarted'], 'questGiver'))
        self.assertIsNone(audit.visible_confidence(quest,
            ['scriptConfig', 'giveBlueprints', '0'], 'clawglove'))
        self.assertIsNone(audit.visible_confidence(quest,
            ['scriptConfig', 'outpostBookmark2', 'target', '1'], 'scienceoutpost'))
        self.assertEqual(audit.visible_confidence(quest,
            ['scriptConfig', 'outpostBookmark2', 'bookmarkName'], 'Science Outpost'), 'confirmed')
        self.assertEqual(audit.visible_confidence(quest, ['text'], 'Repair the gate.'), 'confirmed')
        self.assertIsNone(audit.visible_confidence('interface/mechfuel/mechfuel.config',
            ['gui', 'fuelLabel', 'vAnchor'], 'bottom'))
        self.assertIsNone(audit.visible_confidence('interface/mechfuel/mechfuel.config',
            ['gui', 'fuelLabel', 'callback'], 'insertFuel'))
        self.assertEqual(audit.visible_confidence('interface/mechfuel/mechfuel.config',
            ['gui', 'fuelLabel', 'value'], 'Fuel needed'), 'confirmed')

    def test_output_never_overwrites_started_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'packet.json').write_text('work in progress', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'overwrite'):
                planner.write_outputs(root, {}, [], {})
            self.assertEqual((root / 'packet.json').read_text(), 'work in progress')

    def make_packet(self):
        en = 'Planner fixture consumes 12 units.\nReady.'
        rows = [candidate('objects/crafting/plannerfixture/a.object', en=en),
                candidate('objects/crafting/plannerfixture/b.object', en=en)]
        packet = {'units': planner.units_for(rows, {}), 'inputs': {'catalog': 'hash'},
                  'runtime_review': {'reviewed': False, 'evidence': []}, 'measurements': {}}
        packet['basis_sha256'] = planner.digest(planner.immutable_packet(packet))
        expected = copy.deepcopy(packet)
        evidence = [{'source': 'fixture.recipe', 'note': 'Fixture runtime reference'}]
        packet['runtime_review'] = {'reviewed': True, 'evidence': evidence}
        unit = packet['units'][0]
        unit.update(tr='Hazırlık aracı 12 birim tüketir.\nHazır.', context_reviewed=True, runtime_evidence=evidence)
        return packet, expected

    def test_preflight_rejects_modified_source_missing_member_and_stale_inputs(self):
        for mutation in ('source', 'member', 'inputs'):
            packet, expected = self.make_packet()
            if mutation == 'source':
                packet['units'][0]['en'] += '!'
            elif mutation == 'member':
                packet['units'][0]['occurrences'].pop()
            else:
                packet['inputs']['catalog'] = 'new'
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, 'stale/modified'):
                planner.check_packet(packet, expected, [])

    def test_preflight_requires_runtime_and_group_context_review(self):
        packet, expected = self.make_packet()
        packet['units'][0]['context_reviewed'] = False
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            planner.check_packet(packet, expected, [])
        packet['units'][0]['context_reviewed'] = True
        packet['runtime_review']['evidence'] = []
        with self.assertRaisesRegex(ValueError, 'Runtime/context'):
            planner.check_packet(packet, expected, [])

    def test_preflight_checks_all_occurrences_and_real_project_integrity(self):
        packet, expected = self.make_packet()
        catalog = planner.read(planner.TOOLS / 'ceviriler.json')['translations']
        result = planner.check_packet(packet, expected, catalog)
        self.assertEqual(result['fields'], 2)
        packet['units'][0]['tr'] = 'Hazırlık aracı 120 birim tüketir.\nHazır.'
        with self.assertRaisesRegex(ValueError, 'Number mismatch'):
            planner.check_packet(packet, expected, catalog)

    def test_preflight_rejects_blank_english_and_lost_newline(self):
        for tr in ('', 'Planner fixture consumes 12 units.\nReady.', 'Hazırlık aracı 12 birim tüketir. Hazır.'):
            packet, expected = self.make_packet()
            packet['units'][0]['tr'] = tr
            with self.subTest(tr=tr), self.assertRaises(ValueError):
                planner.check_packet(packet, expected, [])

    def test_exact_locked_preserved_name_passes_but_unchanged_prose_does_not(self):
        packet, _ = self.make_packet()
        unit = packet['units'][0]
        unit.update(en='Kramil', tr='Kramil')
        for occurrence in unit['occurrences']:
            occurrence['pointer'] = '/shortdescription'
        packet['basis_sha256'] = planner.digest(planner.immutable_packet(packet))
        expected = copy.deepcopy(packet)
        catalog = planner.read(planner.TOOLS / 'ceviriler.json')['translations']
        self.assertEqual(planner.check_packet(packet, expected, catalog)['fields'], 2)
        for occurrence in unit['occurrences']:
            occurrence['pointer'] = '/description'
        packet['basis_sha256'] = planner.digest(planner.immutable_packet(packet))
        with self.assertRaisesRegex(ValueError, 'unchanged'):
            planner.check_packet(packet, copy.deepcopy(packet), catalog)

    def test_scripted_farmable_example_is_excluded_but_normal_wheat_remains(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = {'shortdescription': 'Wheat Seed', 'description': 'A staple crop.'}
            example = root / 'objects/farmables/fu_scriptedfarmableexample/fu_scriptedfarmableexample.object'
            example.parent.mkdir(parents=True)
            example.write_text(json.dumps(data), encoding='utf-8')
            normal = root / 'objects/farmables/wheat/wheatseed.object'
            normal.parent.mkdir(parents=True)
            normal.write_text(json.dumps(data), encoding='utf-8')
            catalog = root / 'catalog.json'
            catalog.write_text('{"translations": []}', encoding='utf-8')
            rows = audit.audit(root, catalog, include_rows=True)['remaining_rows']
            self.assertEqual({r['asset'] for r in rows}, {'objects/farmables/wheat/wheatseed.object'})


if __name__ == '__main__':
    unittest.main()
