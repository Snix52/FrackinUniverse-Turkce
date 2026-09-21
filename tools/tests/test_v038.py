import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];TOOLS=ROOT/"tools"
ASSET="interface/scripted/statWindow/extraStatsWindow.config"

class V038Tests(unittest.TestCase):
    def test_manifest_is_applied_exactly(self):
        m=json.loads((TOOLS/"v038_translations.json").read_text(encoding="utf-8"))
        c=json.loads((TOOLS/"ceviriler.json").read_text(encoding="utf-8"))
        rows=m["translations"]
        self.assertEqual(m["translation_version"],"0.38.0-beta")
        self.assertEqual(len(rows),22)
        self.assertEqual(len({r["en"] for r in rows}),22)
        self.assertEqual({r["asset"] for r in rows},{ASSET})
        idx={(r["asset"],r["pointer"]):r for r in c["translations"]}
        for r in rows:
            self.assertIn((r["asset"],r["pointer"]),idx)
            self.assertEqual(idx[(r["asset"],r["pointer"])]["tr"],r["tr"])
            self.assertEqual(r["section"],"v0.38 gelişmiş istatistikler arayüzü")

    def test_scope_is_title_tooltips_and_default_only(self):
        m=json.loads((TOOLS/"v038_translations.json").read_text(encoding="utf-8"))
        ps={r["pointer"] for r in m["translations"]}
        self.assertIn("/gui/title/value",ps)
        self.assertIn("/defaultTooltip",ps)
        self.assertEqual(sum(bool(re.fullmatch(r"/tooltipBoxes/(?:[0-9]|1[0-9])/tooltip",p)) for p in ps),20)
        self.assertFalse(any(p.startswith("/stats/") for p in ps))
        self.assertFalse(any(p.startswith("/gui/") and p!="/gui/title/value" for p in ps))

    def test_locked_stat_terms_are_preserved(self):
        m=json.loads((TOOLS/"v038_translations.json").read_text(encoding="utf-8"))
        by_en={r["en"]:r["tr"] for r in m["translations"]}
        self.assertEqual(by_en["Crit Chance"],"Kritik Şansı")
        self.assertEqual(by_en["Knockback Resist"],"Geri Tepme Direnci")
        self.assertEqual(by_en["Energy Regen"],"Enerji Yenilenmesi")
        self.assertEqual(by_en["Shield Bash Push"],"Kalkan Darbesi İtme Gücü")
        self.assertEqual(by_en["Energy Block Duration"],"Enerji Yenilenme Gecikmesi")

if __name__=="__main__":unittest.main()
