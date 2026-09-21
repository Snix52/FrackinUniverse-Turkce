import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"


class RuntimeOverrideTests(unittest.TestCase):
    def test_text_typer_utf8_override_is_source_locked(self):
        manifest = json.loads((TOOLS / "raw_runtime_overrides.json").read_text(encoding="utf-8"))
        spec = next(x for x in manifest["assets"] if x["asset"] == "zb/zb_textTyper.lua")
        replacement = spec["replacements"][0]

        self.assertIn("utf8.char(159)", replacement["old"])
        self.assertIn("Preserve UTF-8 characters", replacement["new"])
        self.assertIn("byteCount = 2", replacement["new"])

        template = (TOOLS / "raw_overrides" / "zb" / "zb_textTyper.lua").read_text(encoding="utf-8")
        self.assertNotIn(replacement["old"], template)
        self.assertEqual(template.count(replacement["new"]), 1)
        for char in "çğıİöşü":
            self.assertIn(char, replacement["new"])


if __name__ == "__main__":
    unittest.main()
