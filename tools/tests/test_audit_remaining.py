import sys
import unittest
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import audit_remaining as audit

class AuditVisibilityTests(unittest.TestCase):
    def test_backup_path_is_excluded(self):
        self.assertTrue(audit.excluded_path(PurePosixPath("zb/updateInfoWindow/updateInfoWindow_bak.config")))

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
