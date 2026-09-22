import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
SECTION = "v0.41 Space Station arayüzü"
CONFIG = "interface/scripted/spaceStation/spaceStation.config"
TEXTS = "interface/scripted/spaceStation/texts.config"
DATA = "interface/scripted/spaceStation/spaceStationData.config"
LUA = "interface/scripted/spaceStation/spaceStation.lua"

class V041Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((TOOLS / "v041_translations.json").read_text(encoding="utf-8"))
        cls.rows = cls.manifest["translations"]

    def test_manifest_scope_is_exact(self):
        self.assertEqual(self.manifest["translation_version"], "0.41.0-beta")
        self.assertEqual(len(self.rows), 250)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in self.rows}), 250)
        self.assertEqual(Counter(r["asset"] for r in self.rows), {
            CONFIG: 14,
            TEXTS: 188,
            DATA: 48,
        })
        self.assertTrue(all(r["section"] == SECTION for r in self.rows))

    def test_unreachable_and_manual_review_fields_stay_out(self):
        keys = {(r["asset"], r["pointer"]) for r in self.rows}
        self.assertNotIn((TEXTS, "/generic/chat4"), keys)
        self.assertNotIn((TEXTS, "/generic/chat5"), keys)
        self.assertFalse(any("/quests/" in r["pointer"] for r in self.rows))
        self.assertIn((TEXTS, "/defaultButtonStates/0"), keys)
        self.assertIn((TEXTS, "/defaultButtonStates/5"), keys)

    def test_placeholders_and_format_codes_are_preserved(self):
        token = re.compile(r"\{[A-Za-z0-9_.:-]+\}|\[\([^)]+\)[^\]]*\]|\^[^;\s]*;")
        for row in self.rows:
            self.assertEqual(
                sorted(token.findall(row["en"])),
                sorted(token.findall(row["tr"])),
                row["asset"] + row["pointer"],
            )
        control = re.compile(r"\\[(?![^\\]]*\\^)[^\\]]+\\]|<[^>]+>")
        for row in self.rows:
            source_codes = sorted(control.findall(row["en"]))
            target_codes = sorted(control.findall(row["tr"]))
            if source_codes != target_codes:
                self.assertTrue(
                    row.get("qa", {}).get("allow_control_fix"),
                    row["asset"] + row["pointer"],
                )
                self.assertTrue(row.get("qa", {}).get("reason", "").strip())

        hylotl = next(
            r for r in self.rows
            if r["asset"] == TEXTS and r["pointer"] == "/hylotl/chat2"
        )
        self.assertEqual(
            hylotl["tr"],
            "Şunu izledin mi [ne dediğini pek anlayamıyorsun]?? Gelmiş geçmiş en iyi dizi!",
        )
        self.assertTrue(hylotl["qa"]["allow_control_fix"])
        self.assertTrue(hylotl["qa"]["reason"].strip())

    def test_lua_replacements_are_source_locked(self):
        raw = json.loads((TOOLS / "raw_text_translations.json").read_text(encoding="utf-8"))
        spec = next(x for x in raw["assets"] if x["asset"] == LUA)
        self.assertEqual(spec["source_blob_sha"], "18c0a56b26c7278d559fa7d38f222754d55560c5")
        self.assertEqual(len(spec["replacements"]), 11)
        self.assertEqual(sum(int(r.get("expected_count", 1)) for r in spec["replacements"]), 16)
        self.assertEqual(len({r["old"] for r in spec["replacements"]}), 11)
        self.assertTrue(all(r["old"] != r["new"] for r in spec["replacements"]))
        trs = {r["display_tr"] for r in spec["replacements"]}
        self.assertIn("Pikselin:", trs)
        self.assertIn("İstasyon stoğu:", trs)
        self.assertIn("Tamamen yükseltildi!", trs)

    def test_ui_and_stat_terminology(self):
        by = {(r["asset"], r["pointer"]): r["tr"] for r in self.rows}
        self.assertEqual(by[(CONFIG, "/gui/investButton/caption")], "Yatır")
        self.assertEqual(by[(TEXTS, "/defaultButtonStates/3")], "Ticaret Malları")
        descriptions = "\n".join(
            r["tr"] for r in self.rows
            if r["asset"] == DATA and r["pointer"].endswith("/4")
        )
        for term in (
            "Geri Tepme Direnci",
            "Koruma",
            "Enerji Yenilenmesi",
            "Enerji Yenilenme Gecikmesi",
            "Açlık Tüketimi",
        ):
            self.assertIn(term, descriptions)

if __name__ == "__main__":
    unittest.main()
