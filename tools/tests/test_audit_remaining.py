import sys
import unittest
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import audit_remaining as audit

class AuditVisibilityTests(unittest.TestCase):
    def test_backup_path_is_excluded(self):
        self.assertTrue(audit.excluded_path(PurePosixPath("zb/updateInfoWindow/updateInfoWindow_bak.config")))

    def test_formatting_only_numeric_label_is_not_player_text(self):
        self.assertIsNone(audit.visible_confidence(
            "interface/mechfuel/mechfuel.config",
            ["paneLayout", "lblFuelAmount", "value"],
            "^yellow;0 / 0^white;",
        ))
        self.assertEqual(
            audit.visible_confidence(
                "interface/mechfuel/mechfuel.config",
                ["paneLayout", "lblFuelType", "value"],
                "^yellow;Fuel^reset;",
            ),
            "confirmed",
        )

    def test_technical_sail_breadcrumb_is_not_player_text(self):
        self.assertIsNone(audit.visible_confidence(
            "zb/newSail/newSail.config", ["gui", "path", "value"], "root/sail/ui/intro"
        ))

    def test_fully_invisible_handler_quest_is_excluded(self):
        data = {
            "title": "Invisible handler",
            "text": "Technical text",
            "invisible": True,
            "logOnly": True,
            "showInLog": False,
            "showAcceptDialog": False,
        }
        self.assertEqual(list(audit.candidates_from_data("zb/handler.questtemplate", data)), [])

    def test_optional_mmupgrade_fallback_is_audit_excluded(self):
        self.assertIn(
            "interface/scripted/mmupgrade/mmupgradegui.original.config",
            audit.AUDIT_EXCLUDED_PATHS,
        )

    def test_unreachable_deep_one_vn_is_audit_excluded(self):
        self.assertIn(
            "interface/scripted/sbvn/games/cthululove/deepone.sbvn",
            audit.AUDIT_EXCLUDED_PATHS,
        )

    def test_unreachable_pandora_field_guide_is_audit_excluded(self):
        self.assertIn(
            "interface/scripted/sbvn/games/pandorasboxmonsterfieldguide/pandorasboxmonsterfieldguide.sbvn",
            audit.AUDIT_EXCLUDED_PATHS,
        )

    def test_cockpit_runtime_config_text_is_visible_by_prefix(self):
        asset = "interface/cockpit/cockpit.config"
        self.assertEqual(
            audit.visible_confidence(asset, ["clusterMoons", "plural"], "%s orbiting bodies"),
            "confirmed",
        )
        self.assertEqual(
            audit.visible_confidence(asset, ["planetTypeNames", "metallicmoon"], "Cyber Sphere"),
            "confirmed",
        )
        self.assertEqual(
            audit.visible_confidence(
                asset,
                ["visitableTypeDescription", "garden", "0"],
                "^#76fe68;Lush ^reset;foothills mark this landing location.",
            ),
            "confirmed",
        )
        self.assertIsNone(audit.visible_confidence(
            asset, ["starTypeColors", "default"], "white"
        ))
        self.assertIsNone(audit.visible_confidence(
            asset, ["systemTooltipConfig", "name", "value"], "Placeholder"
        ))

    def test_cockpit_runtime_templates_are_excluded_by_pointer(self):
        asset = "interface/cockpit/cockpit.config"
        excluded = audit.AUDIT_EXCLUDED_FIELDS[asset]
        self.assertEqual(len(excluded), 21)
        self.assertIn("/gui/jumpDialog/children/text/value", excluded)
        self.assertIn("/gui/systeminfo/children/inner/children/view/caption", excluded)
        self.assertTrue(audit.audit_excluded_candidate(
            asset, "/gui/bookmarksFrame/children/bookmarkList/children/bookmarkItemList/schema/listTemplate/name/value"
        ))
        self.assertFalse(audit.audit_excluded_candidate(asset, "/gui/windowtitle/title"))
        self.assertFalse(audit.audit_excluded_candidate(asset, "/displayOres/copper/displayName"))

    def test_sbvn_option_labels_are_visible_but_scene_targets_are_not(self):
        data = {
            "scenes": {
                "choice": {
                    "text": "Choose.",
                    "options": [
                        ["BACK", "previousScene"],
                        ["^green;NEXT^reset;", "nextScene", ["flag=1"]],
                    ],
                }
            }
        }
        rows = list(audit.candidates_from_data(
            "interface/scripted/sbvn/games/test/test.sbvn", data
        ))
        by_pointer = {row.pointer: row for row in rows}
        self.assertEqual(
            by_pointer["/scenes/choice/options/0/0"].value,
            "BACK",
        )
        self.assertEqual(
            by_pointer["/scenes/choice/options/1/0"].value,
            "^green;NEXT^reset;",
        )
        self.assertNotIn("/scenes/choice/options/0/1", by_pointer)
        self.assertNotIn("/scenes/choice/options/1/1", by_pointer)
        self.assertNotIn("/scenes/choice/options/1/2/0", by_pointer)

    def test_title_from_entity_hides_only_windowtitle_fallback_text(self):
        data = {
            "titleFromEntity": True,
            "paneLayout": {
                "windowtitle": {
                    "title": "FALLBACK TITLE",
                    "subtitle": "Fallback subtitle",
                },
                "btnCraft": {"caption": "Craft"},
            },
        }
        rows = list(audit.candidates_from_data("interface/windowconfig/beestation.config", data))
        by_pointer = {row.pointer: row for row in rows}
        self.assertNotIn("/paneLayout/windowtitle/title", by_pointer)
        self.assertNotIn("/paneLayout/windowtitle/subtitle", by_pointer)
        self.assertEqual(by_pointer["/paneLayout/btnCraft/caption"].value, "Craft")

        rows = list(audit.candidates_from_data("interface/windowconfig/tomedais.config", data))
        by_pointer = {row.pointer: row for row in rows}
        self.assertIn("/paneLayout/windowtitle/title", by_pointer)
        self.assertIn("/paneLayout/windowtitle/subtitle", by_pointer)

        data["titleFromEntity"] = False
        rows = list(audit.candidates_from_data("interface/windowconfig/beestation.config", data))
        by_pointer = {row.pointer: row for row in rows}
        self.assertIn("/paneLayout/windowtitle/title", by_pointer)
        self.assertIn("/paneLayout/windowtitle/subtitle", by_pointer)

    def test_team_bar_template_name_is_excluded(self):
        self.assertTrue(audit.audit_excluded_candidate(
            "interface/windowconfig/teambar.config", "/paneLayout/name/value"
        ))

    def test_cockpit_runtime_text_containers_are_visible(self):
        asset = "interface/cockpit/cockpit.config"
        self.assertEqual(
            audit.visible_confidence(asset, ["planetTypeNames", "garden"], "Lush"),
            "confirmed",
        )
        self.assertEqual(
            audit.visible_confidence(asset, ["visitableTypeDescription", "garden", "0"], "A lush world."),
            "confirmed",
        )
        self.assertEqual(
            audit.visible_confidence(asset, ["threatTextPrefix"], "^reset;Threat: ^reset;"),
            "confirmed",
        )
        self.assertIsNone(audit.visible_confidence(
            asset, ["clusterInfoBox", "iconImage"], "/interface/bookmarks/icons/%s.png"
        ))

    def test_matmod_runtime_names_are_visible_without_global_name_rule(self):
        asset = "interface/scripted/fu_matmodplacer/fu_matmodplacer.config"
        self.assertEqual(
            audit.visible_confidence(asset, ["matMods", "0", "name"], "Weather Protection"),
            "confirmed",
        )
        self.assertIsNone(audit.visible_confidence(
            "interface/other.config", ["matMods", "0", "name"], "Weather Protection"
        ))

    def test_dead_research_ids_follow_build_policy(self):
        self.assertTrue(audit.nonvisible_research_candidate(
            "zb/researchTree/fu_geology.config", "/strings/research/default/0"
        ))
        self.assertTrue(audit.nonvisible_research_candidate(
            "zb/researchTree/fu_power.config", "/strings/research/ansible/1"
        ))
        self.assertFalse(audit.nonvisible_research_candidate(
            "zb/researchTree/fu_geology.config", "/strings/research/metals_tungsten/0"
        ))

if __name__ == "__main__":
    unittest.main()
