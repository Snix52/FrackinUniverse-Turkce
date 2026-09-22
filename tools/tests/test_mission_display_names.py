import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"

class MissionDisplayNameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog=json.loads((TOOLS/"ceviriler.json").read_text(encoding="utf-8"))
        cls.by={(r["asset"],r["pointer"]):r for r in catalog["translations"]}

    def test_localized_mission_names(self):
        expected={
            ("quests/ancienttemple.questtemplate","/title"):"^green;Kadim Tapınak",
            ("quests/avianhydro.questtemplate","/title"):"^green;Su Dağıtım Merkezi",
            ("quests/evernight.questtemplate","/title"):"^green;Evernight Tropik Ormanı",
            ("quests/forestoffae.questtemplate","/title"):"^green;Fae Ormanı",
            ("quests/grandarena.questtemplate","/title"):"^green;Büyük Arena",
            ("quests/japaneseruins.questtemplate","/title"):"^green;Gigant Dağı",
            ("quests/towerinvincible.questtemplate","/title"):"^green;Yenilmez Kule",
            ("quests/verdantruins.questtemplate","/title"):"^green;Yemyeşil Harabeler",
            ("ai/ancienttemple.aimission","/speciesText/default/buttonText"):"Kadim Tapınak (2)",
            ("ai/avianhydro.aimission","/speciesText/default/buttonText"):"Su Dağıtım Merkezi (6+)",
            ("ai/evernight.aimission","/speciesText/default/buttonText"):"Evernight Tropik Ormanı (5)",
            ("ai/forestoffae.aimission","/speciesText/default/buttonText"):"Fae Ormanı (5)",
            ("ai/grandarena.aimission","/speciesText/default/buttonText"):"Büyük Arena (5)",
            ("ai/japaneseruins.aimission","/speciesText/default/buttonText"):"Gigant Dağı (8)",
            ("ai/towerinvincible.aimission","/speciesText/default/buttonText"):"Yenilmez Kule (6)",
            ("ai/verdantruins.aimission","/speciesText/default/buttonText"):"Yemyeşil Harabeler (2)",
            ("ai/nightfort.aimission","/speciesText/default/buttonText"):"Gece Hisarı'nı Ziyaret Et",
            ("ai/nightfort.aimission","/speciesText/default/repeatButtonText"):"Gece Hisarı'nı Ziyaret Et",
        }
        for key,value in expected.items():
            with self.subTest(key=key):
                self.assertEqual(self.by[key]["tr"],value)

    def test_reference_titles_are_intentionally_preserved(self):
        expected={
            ("quests/alienjungle.questtemplate","/title"):"^green;Brine Star",
            ("quests/snowcrash.questtemplate","/title"):"^green;Snow Crash",
            ("quests/sunsetriders.questtemplate","/title"):"^green;Sunset Riders",
            ("quests/skytemple.questtemplate","/title"):"^green;Sky Boulevard",
            ("ai/shoggothmission.aimission","/speciesText/default/buttonText"):"^#7fac66;Delta Freya II^reset; (7+)",
        }
        for key,value in expected.items():
            with self.subTest(key=key):
                self.assertEqual(self.by[key]["tr"],value)

    def test_takeshi_reference_is_normalized(self):
        self.assertEqual(self.by[("quests/pavillion.questtemplate","/title")]["tr"],"^green;Takeshi's Castle")
        self.assertEqual(self.by[("ai/pavillion.aimission","/speciesText/default/buttonText")]["tr"],"Takeshi's Castle (3)")

if __name__ == "__main__":
    unittest.main()
