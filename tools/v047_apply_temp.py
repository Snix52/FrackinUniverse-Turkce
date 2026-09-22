#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit

SECTION = "v0.47 bitkiler"
VERSION = "0.47.0-beta"
EXPECTED_FIELDS = 170
EXPECTED_ASSETS = 66
EXPECTED_UNIQUE = 110

TRANSLATIONS = {
    "A ball flower": "Küre biçimli bir çiçek.",
    "A beautiful flower.": "Güzel bir çiçek.",
    "A bizarre plant with no need for sunlight. What does it eat?": "Güneş ışığına ihtiyaç duymayan tuhaf bir bitki. Neyle besleniyor?",
    "A bloodstone sprout": "Kan Taşı Filizi",
    "A bunch of curling roots.": "Kıvrılmış köklerden oluşan bir demet.",
    "A chromatic flower.": "Kromatik bir çiçek.",
    "A cloudy spiral flower.": "Bulutumsu, sarmal bir çiçek.",
    "A crispy shrub.": "Çıtır bir çalı.",
    "A dry shrub.": "Kuru bir çalı.",
    "A forest plant": "Bir orman bitkisi.",
    "A gelatinous bush.": "Jelatinimsi bir çalı.",
    "A gore-sprout": "Kanlı Filiz",
    "A long, sinewy weed.": "Uzun, lifli bir yabani ot.",
    "A mushroom of some sort.": "Bir tür mantar.",
    "A mushroom.": "Mantar.",
    "A pile of mossy stones.": "Yosunlu taş yığını.",
    "A sea anemone": "Bir deniz şakayığı.",
    "A shrub.": "Çalı.",
    "A small metallic hive.": "Küçük metalik bir kovan.",
    "A spiralling spiky plant.": "Sarmal ve dikenli bir bitki.",
    "A stone": "Bir taş.",
    "A strange alien pod.": "Tuhaf bir uzaylı kapsülü.",
    "A swampy plant.": "Bataklık bitkisi.",
    "A thorn bush.": "Dikenli çalı.",
    "A vibrant chromatic flower.": "Canlı renklerde kromatik bir çiçek.",
    "A vine-covered stone.": "Sarmaşıklarla kaplı bir taş.",
    "A weird protrusion.": "Tuhaf bir çıkıntı.",
    "A yellowed shrub.": "Sararmış bir çalı.",
    "Aetherweed": "Aether Yosunu",
    "An anemone.": "Deniz şakayığı.",
    "An unusual aquatic seaweed": "Sıra dışı bir su yosunu.",
    "An unusual bug-like structure.": "Böceği andıran sıra dışı bir yapı.",
    "Analysis. This pod appears to be organic.": "Analiz. Bu kapsül organik görünüyor.",
    "Arboreal Plant": "Ağaçsı Bitki",
    "Ball flower": "Küre Çiçeği",
    "Biggy rocks.": "Kocaman kayalar.",
    "Blood sea flora and fauna. Interesting.": "Kan denizindeki bitki ve hayvan yaşamı. İlginç.",
    "Bloodstone Sprout": "Kan Taşı Filizi",
    "Bloodstone sprout": "Kan Taşı Filizi",
    "Ceiling plants": "Tavan Bitkileri",
    "Claw Fern": "Pençe Eğreltisi",
    "Cone bush.": "Koni çalısı.",
    "Coral": "Mercan",
    "Coral.": "Mercan.",
    "Creepy crawly thingsss.": "Ürkütücü, sürünen şşşeyler.",
    "Creepy ssshape.": "Ürkütücü şşşekil.",
    "Crissspy.": "Çıtır sss.",
    "Curiosity. An unusual bug-like structure.": "Merak. Böceği andıran sıra dışı bir yapı.",
    "Eldergrass": "Kadim Çim",
    "Frozen Plantlife": "Donmuş Bitki Örtüsü",
    "Funny sssquishy pod.": "Komik, yumuşşşak kapsül.",
    "Gelatinous plants": "Jelatinimsi Bitkiler",
    "Goresprout": "Kanlı Filiz",
    "Large rocks.": "Büyük kayalar.",
    "Lightless plants": "Işıksız Bitkiler",
    "Little obsidian pebbles.": "Küçük obsidyen çakılları.",
    "Little sulphuric pebbles.": "Küçük kükürtlü çakıllar.",
    "Long grass": "Uzun Çim",
    "Metallic Hive": "Metalik Kovan",
    "Mushrooms": "Mantarlar",
    "Obsidian pebbles.": "Obsidyen çakılları.",
    "Ocean plants": "Okyanus Bitkileri",
    "Pepper Grass": "Biber Otu",
    "Pretty flower.": "Güzel çiçek.",
    "Pretty.": "Güzel.",
    "Proto-grass": "Proto Çim",
    "Pulsating Plant": "Nabız Atan Bitki",
    "Rainforest grasses": "Yağmur Ormanı Çimleri",
    "Rainforest plants": "Yağmur Ormanı Bitkileri",
    "Rootssss.": "Kökler sss.",
    "Seagrass": "Deniz Otu",
    "Seagrass.": "Deniz otu.",
    "Some curling roots.": "Kıvrılmış kökler.",
    "Some frozen plantlife.": "Donmuş bitki örtüsü.",
    "Spicy grass. That's new.": "Acılı ot. Bu da yeni.",
    "Sssharp coral.": "Sssivri mercan.",
    "Ssshrub.": "Sssçalı.",
    "Ssslimy weeds.": "Sssümüksü otlar.",
    "Ssspiky bush.": "Sssdikenli çalı.",
    "Ssspinny and ssspiky.": "Sssdönen ve sssdikenli.",
    "Ssstones.": "Ssskayalar.",
    "Sswampy.": "Sssbataklık.",
    "Statement. A cloudy spiral flower.": "Bildirim. Bulutumsu, sarmal bir çiçek.",
    "Statement. A crispy shrub.": "Bildirim. Çıtır bir çalı.",
    "Statement. A pile of mossy stones.": "Bildirim. Yosunlu taş yığını.",
    "Statement. A shrub.": "Bildirim. Bir çalı.",
    "Statement. A swampy plant.": "Bildirim. Bataklık bitkisi.",
    "Statement. A thorn bush.": "Bildirim. Dikenli çalı.",
    "Statement. A twisted spike plant.": "Bildirim. Bükülmüş dikenli bir bitki.",
    "Statement. An attractive flower.": "Bildirim. Hoş görünümlü bir çiçek.",
    "Statement. An unusual protrusion.": "Bildirim. Sıra dışı bir çıkıntı.",
    "Statement. Coral.": "Bildirim. Mercan.",
    "Statement. Large rocks.": "Bildirim. Büyük kayalar.",
    "Statement. Sea bush.": "Bildirim. Deniz çalısı.",
    "Statement. These look like roots.": "Bildirim. Bunlar köke benziyor.",
    "Stone": "Taş",
    "Strange fleshy stuff.": "Tuhaf, etsi bir doku.",
    "Strange flora of a tidewater world": "Gelgit Suları dünyasına özgü tuhaf bitki örtüsü.",
    "Strange grass": "Tuhaf Çim",
    "Strange looking grass.": "Tuhaf görünümlü çim.",
    "Strange undersea flora and fauna.": "Tuhaf denizaltı bitki ve hayvan yaşamı.",
    "Sulphuric pebbles.": "Kükürtlü çakıllar.",
    "Sulphuric rocks.": "Kükürtlü kayalar.",
    "Tall, lush grass": "Uzun, gür çim.",
    "This is an interesting plant...": "İlginç bir bitki...",
    "Undersea plants": "Denizaltı Bitkileri",
    "Vine Grass": "Sarmaşık Otu",
    "Viney Stone": "Sarmaşıklı Taş",
    "What in the...just being near this is uncomfortable.": "Bu da ne... Yakınında durmak bile huzursuz ediyor.",
    "Yellowed grass.": "Sararmış çim.",
}

def remaining_plant_rows(source: Path):
    translated, _ = audit.load_translations(TOOLS / "ceviriler.json")
    candidates = {}
    base = source / "plants"
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        rel = PurePosixPath(path.relative_to(source).as_posix())
        if audit.excluded_path(rel):
            continue
        if path.suffix.lower() in audit.BINARY_SUFFIXES or path.stat().st_size > 8_000_000:
            continue
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, OSError):
            continue
        if not raw.lstrip().startswith(("{", "[")):
            continue
        try:
            data = audit.parse_jsonc(raw)
        except Exception:
            continue
        for row in audit.candidates_from_data(rel.as_posix(), data):
            row = audit.v046_candidate_visibility(row)
            if row is None:
                continue
            key = (row.asset, row.pointer)
            if key in translated or audit.audit_excluded_candidate(row.asset, row.pointer):
                continue
            if row.confidence != "confirmed" or row.category != "Biyom, zindan ve dünya sistemleri":
                continue
            prev = candidates.get(key)
            if prev is None or (prev.confidence == "review" and row.confidence == "confirmed"):
                candidates[key] = row
    return [candidates[k] for k in sorted(candidates)]

def write_manifest(source: Path):
    rows = remaining_plant_rows(source)
    assets = {r.asset for r in rows}
    sources = {r.value for r in rows}
    if len(rows) != EXPECTED_FIELDS:
        raise ValueError(f"v0.47 plant field drift: {len(rows)} != {EXPECTED_FIELDS}")
    if len(assets) != EXPECTED_ASSETS:
        raise ValueError(f"v0.47 plant asset drift: {len(assets)} != {EXPECTED_ASSETS}")
    if len(sources) != EXPECTED_UNIQUE:
        raise ValueError(f"v0.47 plant source drift: {len(sources)} != {EXPECTED_UNIQUE}")
    if set(TRANSLATIONS) != sources:
        raise ValueError(
            f"v0.47 translation map mismatch; missing={sorted(sources-set(TRANSLATIONS))!r} "
            f"unused={sorted(set(TRANSLATIONS)-sources)!r}"
        )
    allowed = {"/description", "/shortdescription", "/floranDescription", "/glitchDescription"}
    if {r.pointer for r in rows} - allowed:
        raise ValueError("Unexpected plant pointer: " + repr(sorted({r.pointer for r in rows} - allowed)))
    manifest = {
        "schema_version": 1,
        "translation_version": VERSION,
        "scope": "Oyuncuya görünen FU bitki adları, açıklamaları ve Floran/Glitch inceleme replikleri. Teknik plant ID'leri ile .liquid config description metadata alanları kapsam dışıdır.",
        "translations": [
            {
                "asset": r.asset,
                "pointer": r.pointer,
                "en": r.value,
                "tr": TRANSLATIONS[r.value],
                "section": SECTION,
            }
            for r in rows
        ],
    }
    (TOOLS / "v047_translations.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest

def update_catalog(manifest):
    path = TOOLS / "ceviriler.json"
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if catalog["translation_version"] != "0.46.3-beta":
        raise ValueError("Unexpected catalog base version: " + catalog["translation_version"])
    existing = {(r["asset"], r["pointer"]) for r in catalog["translations"]}
    for row in manifest["translations"]:
        key = (row["asset"], row["pointer"])
        if key in existing:
            raise ValueError("v0.47 row already exists: " + repr(key))
        catalog["translations"].append(row)
        existing.add(key)
    catalog["translation_version"] = VERSION
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def update_audit_rules():
    path = TOOLS / "rules" / "dead_assets.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    fields = data["rules"]["AUDIT_EXCLUDED_FIELDS"]["value"]
    fields["liquids/"] = ["/description"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    test_path = TOOLS / "tests" / "test_audit_remaining.py"
    text = test_path.read_text(encoding="utf-8")
    needle = "    def test_sbvn_option_labels_are_visible_but_scene_targets_are_not(self):\n"
    test = '''    def test_liquid_description_metadata_is_prefix_excluded(self):
        self.assertIn("liquids/", audit.AUDIT_EXCLUDED_FIELDS)
        self.assertIn("/description", audit.AUDIT_EXCLUDED_FIELDS["liquids/"])
        self.assertTrue(audit.audit_excluded_candidate(
            "liquids/blood.liquid", "/description"
        ))
        self.assertTrue(audit.audit_excluded_candidate(
            "liquids/liquidnitrogen.liquid", "/description"
        ))
        self.assertFalse(audit.audit_excluded_candidate(
            "items/liquids/liquidblood.liqitem", "/description"
        ))
        self.assertFalse(audit.audit_excluded_candidate(
            "liquids/blood.liquid", "/name"
        ))

'''
    if "test_liquid_description_metadata_is_prefix_excluded" not in text:
        if needle not in text:
            raise ValueError("audit test insertion point missing")
        text = text.replace(needle, test + needle, 1)
    test_path.write_text(text, encoding="utf-8")

def write_generator():
    content = r'''#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit
from write_build_evidence import verify_source

MANIFEST = TOOLS / "v047_translations.json"
CATALOG = TOOLS / "ceviriler.json"
EXPECTED_FIELDS = 170
EXPECTED_ASSETS = 66
EXPECTED_UNIQUE = 110
ALLOWED_POINTERS = {"/description", "/shortdescription", "/floranDescription", "/glitchDescription"}

def version_tuple(value):
    return tuple(map(int, value.split("-", 1)[0].split(".")))

def read_at(root, pointer):
    cur = root
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()
    verify_source(args.source)

    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = m["translations"]
    if m["translation_version"] != "0.47.0-beta":
        raise ValueError("v0.47 manifest version drift")
    if len(rows) != EXPECTED_FIELDS:
        raise ValueError(f"v0.47 field drift: {len(rows)}")
    if len({(r["asset"], r["pointer"]) for r in rows}) != EXPECTED_FIELDS:
        raise ValueError("v0.47 duplicate field")
    if len({r["asset"] for r in rows}) != EXPECTED_ASSETS:
        raise ValueError("v0.47 asset drift")
    if len({r["en"] for r in rows}) != EXPECTED_UNIQUE:
        raise ValueError("v0.47 source drift")
    if any(not r["asset"].startswith("plants/") for r in rows):
        raise ValueError("v0.47 non-plant asset")
    if {r["pointer"] for r in rows} - ALLOWED_POINTERS:
        raise ValueError("v0.47 pointer drift")
    if "/description" not in audit.AUDIT_EXCLUDED_FIELDS.get("liquids/", frozenset()):
        raise ValueError("liquid description audit exclusion missing")

    cache = {}
    for r in rows:
        path = args.source / r["asset"]
        if not path.is_file():
            raise FileNotFoundError(path)
        if r["asset"] not in cache:
            cache[r["asset"]] = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
        if read_at(cache[r["asset"]], r["pointer"]) != r["en"]:
            raise ValueError("v0.47 pinned source mismatch: " + r["asset"] + r["pointer"])

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if version_tuple(catalog["translation_version"]) < (0, 47, 0):
        raise ValueError("catalog version behind v0.47")
    idx = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
    for r in rows:
        cur = idx.get((r["asset"], r["pointer"]))
        if not cur or cur["en"] != r["en"] or cur["tr"] != r["tr"]:
            raise ValueError("v0.47 catalog mismatch: " + r["asset"] + r["pointer"])

    print(f"v0.47 source gate PASS: {len(rows)} alan / {len({r['asset'] for r in rows})} asset / {len({r['en'] for r in rows})} kaynak")

if __name__ == "__main__":
    main()
'''
    path = TOOLS / "generate_v047.py"
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)

def write_tests():
    content = r'''import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit

SECTION = "v0.47 bitkiler"

class V047Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads((TOOLS / "v047_translations.json").read_text(encoding="utf-8"))
        cls.rows = cls.m["translations"]
        cls.by = {(r["asset"], r["pointer"]): r for r in cls.rows}

    def test_scope_is_exact(self):
        self.assertEqual(self.m["translation_version"], "0.47.0-beta")
        self.assertEqual(len(self.rows), 170)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in self.rows}), 170)
        self.assertEqual(len({r["asset"] for r in self.rows}), 66)
        self.assertEqual(len({r["en"] for r in self.rows}), 110)
        self.assertTrue(all(r["asset"].startswith("plants/") for r in self.rows))
        self.assertEqual(
            {r["pointer"] for r in self.rows},
            {"/description", "/shortdescription", "/floranDescription", "/glitchDescription"},
        )
        self.assertTrue(all(r["section"] == SECTION for r in self.rows))

    def test_catalog_contains_exact_manifest(self):
        c = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(
            tuple(map(int, c["translation_version"].split("-")[0].split("."))),
            (0, 47, 0),
        )
        idx = {(r["asset"], r["pointer"]): r for r in c["translations"]}
        for r in self.rows:
            self.assertEqual(idx[(r["asset"], r["pointer"])]["en"], r["en"])
            self.assertEqual(idx[(r["asset"], r["pointer"])]["tr"], r["tr"])

    def test_liquid_config_descriptions_are_not_translation_debt(self):
        self.assertIn("/description", audit.AUDIT_EXCLUDED_FIELDS["liquids/"])
        self.assertTrue(audit.audit_excluded_candidate("liquids/blood.liquid", "/description"))
        self.assertFalse(audit.audit_excluded_candidate(
            "items/liquids/liquidblood.liqitem", "/description"
        ))
        self.assertFalse(any(r["asset"].startswith("liquids/") for r in self.rows))

    def test_project_terminology_and_character_tone(self):
        self.assertEqual(
            self.by[("plants/grass/ground/decorative/aethersea/aethergrass.grass", "/shortdescription")]["tr"],
            "Aether Yosunu",
        )
        self.assertEqual(
            self.by[("plants/grass/ground/decorative/bloodstoneplant/bloodstoneplant.grass", "/shortdescription")]["tr"],
            "Kan Taşı Filizi",
        )
        self.assertEqual(
            self.by[("plants/grass/ground/decorative/rainforestgrasses/rainforestgrasses.grass", "/shortdescription")]["tr"],
            "Yağmur Ormanı Çimleri",
        )
        self.assertEqual(
            self.by[("plants/grass/ground/decorative/sulphurpebbles/sulphurpebbles.grass", "/shortdescription")]["tr"],
            "Kükürtlü çakıllar.",
        )
        self.assertIn(
            "Gelgit Suları",
            self.by[("plants/grass/ground/decorative/tidewatergrass/tidewatergrass.grass", "/description")]["tr"],
        )
        self.assertTrue(
            self.by[("plants/bushes/ground/buglike/buglike.bush", "/floranDescription")]["tr"].count("ş") >= 3
        )
        self.assertTrue(
            self.by[("plants/bushes/ground/buglike/buglike.bush", "/glitchDescription")]["tr"].startswith("Merak.")
        )

    def test_format_contracts(self):
        color = re.compile(r"\^[^;\s]*;")
        control = re.compile(r"\[(?![^\]]*\^)[^\]]+\]|<[^>]+>")
        number = re.compile(r"\d+(?:[.,]\d+)?")
        for r in self.rows:
            self.assertEqual(sorted(color.findall(r["en"])), sorted(color.findall(r["tr"])))
            self.assertEqual(sorted(control.findall(r["en"])), sorted(control.findall(r["tr"])))
            self.assertEqual(
                sorted(x.replace(",", ".") for x in number.findall(color.sub("", r["en"]))),
                sorted(x.replace(",", ".") for x in number.findall(color.sub("", r["tr"]))),
            )
            self.assertEqual(r["en"].count("\n"), r["tr"].count("\n"))

if __name__ == "__main__":
    unittest.main()
'''
    (TOOLS / "tests" / "test_v047.py").write_text(content, encoding="utf-8")

def update_build_validator():
    path = TOOLS / "build_validate.py"
    text = path.read_text(encoding="utf-8")
    load_needle = '''if len(V046_RACES_SAIL_FIELDS) != len(_V046_MANIFEST['translations']):
    raise ValueError('v0.46 Irklar/SAIL manifestinde yinelenen alan var')
'''
    load_block = load_needle + '''
_V047_MANIFEST = json.loads(
    Path(__file__).with_name('v047_translations.json').read_text(encoding='utf-8')
)
V047_PLANT_FIELDS = {
    (row['asset'], row['pointer']) for row in _V047_MANIFEST['translations']
}
if len(V047_PLANT_FIELDS) != len(_V047_MANIFEST['translations']):
    raise ValueError('v0.47 bitki manifestinde yinelenen alan var')
'''
    if "V047_PLANT_FIELDS" not in text:
        if load_needle not in text:
            raise ValueError("build_validate v047 manifest insertion point missing")
        text = text.replace(load_needle, load_block, 1)

    allowed_needle = '''def allowed(a,p):
    if (a,p) in V046_RACES_SAIL_FIELDS:
'''
    allowed_replace = '''def allowed(a,p):
    if (a,p) in V047_PLANT_FIELDS:
        return True
    if (a,p) in V046_RACES_SAIL_FIELDS:
'''
    if "if (a,p) in V047_PLANT_FIELDS:" not in text:
        if allowed_needle not in text:
            raise ValueError("build_validate allowed insertion point missing")
        text = text.replace(allowed_needle, allowed_replace, 1)
    path.write_text(text, encoding="utf-8")

def update_workflows():
    for rel in (".github/workflows/build-package.yml", ".github/workflows/pr-qa.yml"):
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        text = text.replace("Verify v0.45-v0.46 pinned translation sources", "Verify v0.45-v0.47 pinned translation sources")
        if "python tools/generate_v047.py --source fu_source" not in text:
            text = text.replace(
                "python tools/generate_v046.py --source fu_source",
                "python tools/generate_v046.py --source fu_source\n          python tools/generate_v047.py --source fu_source",
                1,
            )
        path.write_text(text, encoding="utf-8")

def update_old_test_version_gate():
    path = TOOLS / "tests" / "test_v046.py"
    text = path.read_text(encoding="utf-8")
    old = '        self.assertEqual(c["translation_version"], "0.46.3-beta")\n'
    new = '''        self.assertGreaterEqual(
            tuple(map(int, c["translation_version"].split("-")[0].split("."))),
            (0, 46, 3),
        )
'''
    if old in text:
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")

def update_docs():
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    replacements = {
        "**Güncel sürüm:** v0.46.3 Beta": "**Güncel sürüm:** v0.47.0 Beta",
        "v0.46.3 Beta itibarıyla:": "v0.47.0 Beta itibarıyla:",
        "- **8.153** yapılandırılmış oyuncu metni": "- **8.323** yapılandırılmış oyuncu metni",
        "- **8.210** toplam yerelleştirilmiş görünür birim": "- **8.380** toplam yerelleştirilmiş görünür birim",
        "- **2.329** patch asset": "- **2.395** patch asset",
        "- **2.336** toplam hedef asset": "- **2.402** toplam hedef asset",
        "dist/FU_Turkce_v0.46.3_Beta.zip": "dist/FU_Turkce_v0.47.0_Beta.zip",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    old_para = "v0.46.1 bakımında generic Jungle terminolojisi Tropik Orman olarak kilitlendi. v0.46.2 bakımında eski toplu görev/konum özel-ad kararı yeniden denetlendi. v0.46.3 bakımında Nightfort oyuncuya görünen ad olarak **Gece Hisarı** biçiminde yerelleştirildi; teknik `nightfort` kimlikleri korundu. Sonraki paket güncel Remaining Scope Audit sıralamasından seçilecektir."
    new_para = "v0.46.1-v0.46.3 bakımında Jungle ve görev/konum görünen adları geriye dönük denetlendi. **v0.47.0** ile 66 bitki assetindeki **170** oyuncu-yüzü ad, açıklama ve Floran/Glitch inceleme metni Türkçeleştirildi. `.biome/friendlyName` ve `.liquid/description` gibi runtime görünürlüğü doğrulanmayan metadata alanları çeviri borcundan çıkarıldı."
    text = text.replace(old_para, new_para)
    readme.write_text(text.rstrip() + "\n", encoding="utf-8")

    decisions = ROOT / "docs" / "DECISIONS.md"
    text = decisions.read_text(encoding="utf-8")
    note = '''### v0.47.0 - Bitkiler ve liquid metadata denetimi

- `plants/` kökündeki 66 canlı assette 170 oyuncuya gösterilen alan yerelleştirildi: `description`, `shortdescription`, `floranDescription`, `glitchDescription`.
- Bitki teknik adları, dosya yolları ve worldgen kimlikleri değiştirilmedi.
- Proje terminolojisi yeniden kullanıldı: **Aether**, **Kan Taşı**, **Yağmur Ormanı**, **Kükürtlü**, **Gelgit Suları**, **Jelatinimsi**.
- Floran inceleme repliklerinde tıslama ve kısa/ilkel söyleyiş; Glitch repliklerinde robotik duygu/işlev önekleri korunur.
- `liquids/*.liquid /description` alanları normal oyuncu envanter açıklaması değildir. Görünür sıvı eşya metinleri `items/liquids/*.liqitem` üzerinden gelir; FU runtime taramasında liquid-config description alanını ekrana basan bir bağ bulunmadı.
- Bu nedenle yalnız `liquids/` asset ailesindeki `/description` pointerı audit confirmed kapsamından çıkarılır. `.liqitem` açıklamaları bu kuraldan etkilenmez.
'''
    if "### v0.47.0 - Bitkiler ve liquid metadata denetimi" not in text:
        text = text.rstrip() + "\n\n" + note.strip() + "\n"
    decisions.write_text(text, encoding="utf-8")

    checkpoint = ROOT / "FU_SESSION_CHECKPOINT.md"
    text = checkpoint.read_text(encoding="utf-8")
    note = '''## v0.47.0 bitkiler checkpoint
- İlk Plants + Liquids audit havuzu: **102 asset / 206 confirmed alan**.
- Runtime sınıflandırması:
  - **Plants:** 66 asset / 170 gerçek oyuncu metni
  - **Liquids:** 36 asset / 36 `/description` metadata false positive
- v0.47 manifesti: **170 alan / 66 asset / 110 benzersiz kaynak**.
- Bitki kapsamı: ad, açıklama, Floran ve Glitch inceleme replikleri.
- Liquid config açıklamaları audit confirmed kapsamından çıkarıldı; `items/liquids/*.liqitem` görünür metinleri ayrı ve etkilenmiyor.
- Katalog sürümü: **0.47.0-beta**.
- Beklenen structured toplam: **8.323**; patch asset: **2.395**.
- Beklenen audit sonrası Biyom/Zindan/Dünya confirmed borcu: **638 asset / 1.746 alan**.
- Beklenen genel confirmed borç: **12.350 asset / 50.092 alan**.
- Oyun içi LQA: **NOT TESTED**.
'''
    if "## v0.47.0 bitkiler checkpoint" not in text:
        text = text.rstrip() + "\n\n" + note.strip() + "\n"
    checkpoint.write_text(text, encoding="utf-8")

def cleanup_temp():
    for path in (
        ROOT / ".github" / "workflows" / "v047-plants-liquids-dump.yml",
        ROOT / ".github" / "workflows" / "v047-apply.yml",
        TOOLS / "v047_apply_temp.py",
    ):
        if path.exists():
            path.unlink()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()
    manifest = write_manifest(args.source)
    update_catalog(manifest)
    update_audit_rules()
    write_generator()
    write_tests()
    update_build_validator()
    update_workflows()
    update_old_test_version_gate()
    update_docs()
    cleanup_temp()
    print(f"v0.47 migration prepared: {len(manifest['translations'])} fields / {len({r['asset'] for r in manifest['translations']})} assets")

if __name__ == "__main__":
    main()
