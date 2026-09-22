import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TOOLS=ROOT/"tools"
SECTION="v0.45 görev kapanışı"

class V045Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=json.loads((TOOLS/"v045_translations.json").read_text(encoding="utf-8"))
        cls.rows=cls.m["translations"]
        cls.by={(r["asset"],r["pointer"]):r for r in cls.rows}

    def test_scope_is_exact(self):
        self.assertEqual(self.m["translation_version"],"0.45.0-beta")
        self.assertEqual(len(self.rows),29)
        self.assertEqual(len({(r["asset"],r["pointer"]) for r in self.rows}),29)
        self.assertEqual(len({r["asset"] for r in self.rows}),18)
        self.assertEqual(len({r["en"] for r in self.rows}),29)
        self.assertTrue(all(r["section"]==SECTION for r in self.rows))

    def test_catalog_contains_manifest(self):
        c=json.loads((TOOLS/"ceviriler.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(tuple(map(int,c["translation_version"].split("-")[0].split("."))),(0,45,0))
        idx={(r["asset"],r["pointer"]):r for r in c["translations"]}
        for r in self.rows:
            self.assertEqual(idx[(r["asset"],r["pointer"])]["tr"],r["tr"])

    def test_every_row_is_pinned_layered_quest_source(self):
        for r in self.rows:
            qa=r.get("qa",{})
            self.assertTrue(qa.get("layered_source"),r["asset"]+r["pointer"])
            self.assertEqual(qa.get("source_patch"),r["asset"]+".patch")
            self.assertTrue(qa["source_patch"].endswith(".questtemplate.patch"))

    def test_format_tokens_numbers_and_newlines_are_preserved(self):
        color=re.compile(r"\^[^;\s]*;")
        control=re.compile(r"\[(?![^\]]*\^)[^\]]+\]|<[^>]+>")
        number=re.compile(r"\d+(?:[.,]\d+)?")
        signed=re.compile(r"[+-]\s*%?\s*\d+(?:[.,]\d+)?")
        norm=lambda xs: sorted(x.replace(" ","").replace("%","").replace(",",".") for x in xs)
        for r in self.rows:
            self.assertEqual(sorted(color.findall(r["en"])),sorted(color.findall(r["tr"])),r["asset"]+r["pointer"])
            self.assertEqual(sorted(control.findall(r["en"])),sorted(control.findall(r["tr"])),r["asset"]+r["pointer"])
            self.assertEqual(sorted(x.replace(",",".") for x in number.findall(color.sub("",r["en"]))),sorted(x.replace(",",".") for x in number.findall(color.sub("",r["tr"]))),r["asset"]+r["pointer"])
            self.assertEqual(norm(signed.findall(r["en"])),norm(signed.findall(r["tr"])),r["asset"]+r["pointer"])
            self.assertEqual(r["en"].count("\n"),r["tr"].count("\n"),r["asset"]+r["pointer"])

    def test_project_terminology_and_context_choices(self):
        expected={
            ("quests/story/gaterepair.questtemplate","/scriptConfig/BYOSCompletionText"):"^orange;Protectorate'e^reset; yeniden hoş geldin, Ajan. Senin yardımınla başaracağımızı biliyorum. Ama önce o ^red;bozuk FTL motorunu^reset; onarman gerek! ^cyan;Mühendislik ağacında gerekli araştırmayı aç^reset; ve ^orange;İmalat Tezgâhında^reset; bir ^green;STL Motoru üret^reset;.",
            ("quests/outpost/techscientist5.questtemplate","/text"):"Çarpıtma Küreni ^orange;yükseltmemi^reset; ister misin? Böylece ^red;[Fire]^reset; tuşuna basarak bomba bırakıp engelleri patlatabilirsin! Tamamlamak için birkaç son parçaya ihtiyacım var. ^green;Bana 10 ^orange;Altın Külçe^reset; getirebilir misin?",
            ("quests/outpost/shipupgrade/shipupgrade2.questtemplate","/text"):"Dört mürettebat üyen var! Bu büyüklükte bir mürettebatla artık Kestrel Lisansına hak kazandın. Tebrikler! ^green;Penguin Pete'e git^reset; ve gemini yükseltmek için ^orange;2 Yükseltme Modülü^reset; götür.",
            ("quests/story/shiprepair.questtemplate","/title"):"İtibarı Yeniden Kazanmak",
        }
        for key,value in expected.items():
            self.assertEqual(self.by[key]["tr"],value)

    def test_mech_spelling_stays_locked(self):
        for r in self.rows:
            self.assertIsNone(re.search(r"\bmech\b",r["tr"]))

if __name__=="__main__":
    unittest.main()