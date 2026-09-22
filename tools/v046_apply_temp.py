from pathlib import Path
import base64
import json
import shutil
import zlib

ROOT = Path(".")
TOOLS = ROOT / "tools"
SECTION = "v0.46 Irklar ve SAIL/AI"

CORE_SPECIES = {
    "apex", "avian", "floran", "glitch", "human", "hylotl", "novakid",
    "fenerox", "shadow", "skath", "fupeglaci", "thelusian", "fukirhos",
    "radien", "fumantizi", "nightar", "elduukhar", "slimeperson",
    "veluu", "juux",
}
CORE_ASSETS = {f"species/{name}.species" for name in CORE_SPECIES}

rows = []
for part in sorted((TOOLS / ".v046_parts").glob("part*.b64")):
    payload = json.loads(zlib.decompress(base64.b64decode(part.read_text(encoding="utf-8"))))
    rows.extend(payload["translations"])

if len(rows) != 129:
    raise ValueError(f"v0.46 staged field count: {len(rows)}")
if len({(r["asset"], r["pointer"]) for r in rows}) != 129:
    raise ValueError("v0.46 duplicate field")
if len({r["asset"] for r in rows}) != 53:
    raise ValueError("v0.46 asset count mismatch")
if len({r["en"] for r in rows}) != 127:
    raise ValueError("v0.46 unique source count mismatch")
if sum(r["asset"].startswith("ai/") for r in rows) != 89:
    raise ValueError("v0.46 AI field count mismatch")
if sum(r["asset"].startswith("species/") for r in rows) != 40:
    raise ValueError("v0.46 species field count mismatch")

by = {(r["asset"], r["pointer"]): r for r in rows}
fixes = {
    ("species/juux.species", "/charCreationTooltip/description"): [
        ("Psiyonik Fırlatıcı", "Psiyonik Odak"),
    ],
    ("species/fenerox.species", "/charCreationTooltip/description"): [
        ("Avcı Pençesi", "Avcı Pençeleri"),
    ],
    ("species/floran.species", "/charCreationTooltip/description"): [
        ("İğneli Silahlar/Floran Silahları/Fırlatılanlar",
         "İğneleyici/Floran Silahları/Fırlatılanlar"),
    ],
    ("species/slimeperson.species", "/charCreationTooltip/description"): [
        ("Jelatinimsi, Bataklık ve Bataklık biyomları",
         "Jelatinimsi, Bataklık ve Sulaklık biyomları"),
    ],
    ("species/hylotl.species", "/charCreationTooltip/description"): [
        ("Barışçıl Hylotllar", "Barışçıl Hylotl'lar"),
    ],
    ("species/fukirhos.species", "/charCreationTooltip/description"): [
        ("-^red;5^reset;%Fiziksel", "-^red;5^reset;% Fiziksel"),
    ],
    ("species/veluu.species", "/charCreationTooltip/description"): [
        ("+^green;13^reset;% Zıplama ve +^green;6^reset;% Koşu Hızı",
         "^green;13^reset;% Zıplama ve ^green;6^reset;% Koşu Hızı"),
    ],
}
for key, replacements in fixes.items():
    row = by[key]
    for old, new in replacements:
        if old not in row["tr"]:
            raise ValueError(f"v0.46 final wording source missing: {key} {old}")
        row["tr"] = row["tr"].replace(old, new)

manifest = {
    "schema_version": 1,
    "translation_version": "0.46.0-beta",
    "scope": (
        "Çekirdek FU/Starbound karakter oluşturma ırk açıklamaları ile canlı "
        "SAIL/AI görev metinleri; üçüncü taraf ırk uyumluluk patchleri review "
        "havuzunda tutulur."
    ),
    "translations": rows,
}
(TOOLS / "v046_translations.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

catalog_path = TOOLS / "ceviriler.json"
catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
if catalog["translation_version"] != "0.45.1-beta":
    raise ValueError("Unexpected base catalog version: " + catalog["translation_version"])
existing = {(r["asset"], r["pointer"]) for r in catalog["translations"]}
for row in rows:
    key = (row["asset"], row["pointer"])
    if key in existing:
        raise ValueError("v0.46 field already exists: " + repr(key))
    catalog["translations"].append(row)
    existing.add(key)
catalog["translation_version"] = "0.46.0-beta"
catalog_path.write_text(
    json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

rule_payload = {
    "schema_version": 1,
    "description": "v0.46 Irklar ve SAIL/AI runtime visibility classification.",
    "rules": {
        "AUDIT_CORE_PLAYABLE_SPECIES_ASSETS": {
            "type": "set",
            "value": sorted(CORE_ASSETS),
        },
        "V046_TECHNICAL_FALSE_POSITIVE_FIELDS": {
            "type": "dict_of_sets",
            "value": {
                "species/irken.raceeffect": [
                    "/envEffects/0/scripts/0/args/label"
                ],
                "species/skelekin.raceeffect": [
                    "/liquidEffects/0/scripts/0/args/label"
                ],
            },
        },
    },
}
(TOOLS / "rules" / "v046.json").write_text(
    json.dumps(rule_payload, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

audit_path = TOOLS / "audit_remaining.py"
s = audit_path.read_text(encoding="utf-8")
if "from dataclasses import dataclass, replace" not in s:
    s = s.replace(
        "from dataclasses import dataclass\n",
        "from dataclasses import dataclass, replace\n",
        1,
    )
rule_needle = "AUDIT_PATCH_APPEND_INDEXES = load_rule('AUDIT_PATCH_APPEND_INDEXES')\n"
rule_insert = (
    rule_needle
    + "AUDIT_CORE_PLAYABLE_SPECIES_ASSETS = load_rule('AUDIT_CORE_PLAYABLE_SPECIES_ASSETS')\n"
    + "V046_TECHNICAL_FALSE_POSITIVE_FIELDS = load_rule('V046_TECHNICAL_FALSE_POSITIVE_FIELDS')\n"
)
if "AUDIT_CORE_PLAYABLE_SPECIES_ASSETS = load_rule" not in s:
    if rule_needle not in s:
        raise ValueError("audit rule insertion point missing")
    s = s.replace(rule_needle, rule_insert, 1)

helper_needle = "def load_translations(catalog_path: Path) -> tuple[set[tuple[str, str]], int]:\n"
helper = '''def v046_candidate_visibility(candidate: Candidate) -> Candidate | None:
    if candidate.pointer in V046_TECHNICAL_FALSE_POSITIVE_FIELDS.get(
        candidate.asset, frozenset()
    ):
        return None
    if (
        candidate.asset.startswith("species/")
        and candidate.asset.endswith(".species")
        and candidate.asset not in AUDIT_CORE_PLAYABLE_SPECIES_ASSETS
        and candidate.confidence == "confirmed"
    ):
        return replace(candidate, confidence="review")
    return candidate


'''
if "def v046_candidate_visibility" not in s:
    if helper_needle not in s:
        raise ValueError("audit helper insertion point missing")
    s = s.replace(helper_needle, helper + helper_needle, 1)

loop_needle = '''        for candidate in candidates_from_data(rel.as_posix(), data):
            if candidate.asset in V018_DEAD_OBJECT_ASSETS'''
loop_replace = '''        for candidate in candidates_from_data(rel.as_posix(), data):
            candidate = v046_candidate_visibility(candidate)
            if candidate is None:
                continue
            if candidate.asset in V018_DEAD_OBJECT_ASSETS'''
if "candidate = v046_candidate_visibility(candidate)" not in s:
    if loop_needle not in s:
        raise ValueError("audit loop insertion point missing")
    s = s.replace(loop_needle, loop_replace, 1)
audit_path.write_text(s, encoding="utf-8")

build_path = TOOLS / "build_validate.py"
s = build_path.read_text(encoding="utf-8")
manifest_needle = """if len(V045_QUEST_PATCH_FIELDS) != len(_V045_MANIFEST['translations']):
    raise ValueError('v0.45 görev kapanış manifestinde yinelenen alan var')
"""
manifest_insert = manifest_needle + """
_V046_MANIFEST = json.loads(
    Path(__file__).with_name('v046_translations.json').read_text(encoding='utf-8')
)
V046_RACES_SAIL_FIELDS = {
    (row['asset'], row['pointer']) for row in _V046_MANIFEST['translations']
}
if len(V046_RACES_SAIL_FIELDS) != len(_V046_MANIFEST['translations']):
    raise ValueError('v0.46 Irklar/SAIL manifestinde yinelenen alan var')
"""
if "_V046_MANIFEST" not in s:
    if manifest_needle not in s:
        raise ValueError("build manifest insertion point missing")
    s = s.replace(manifest_needle, manifest_insert, 1)

allowed_needle = """def allowed(a,p):
    if (a,p) in V045_QUEST_PATCH_FIELDS:
"""
allowed_replace = """def allowed(a,p):
    if (a,p) in V046_RACES_SAIL_FIELDS:
        return True
    if (a,p) in V045_QUEST_PATCH_FIELDS:
"""
if "if (a,p) in V046_RACES_SAIL_FIELDS" not in s:
    if allowed_needle not in s:
        raise ValueError("build allowed insertion point missing")
    s = s.replace(allowed_needle, allowed_replace, 1)

source_block = """        if args.source_dir:
            source=args.source_dir/a
            if source.is_file():
                simulate(parse_jsonc(source.read_text(encoding='utf-8-sig')),patch)
            elif all(r.get('qa',{}).get('layered_source') for r in rs):
                # FU bazı vanilla assetleri yalnızca .patch katmanıyla değiştirir; hedef .object FU kaynak ağacında bulunmaz.
                # Bu alanların kaynak provenansı ledger qa.source_patch / external_base_verified ile ayrıca kilitlenir.
                pass
            else:
                raise FileNotFoundError(source)
"""
source_replacement = """        if args.source_dir:
            source=args.source_dir/a
            v046_layered = all(
                (a, r['pointer']) in V046_RACES_SAIL_FIELDS
                and r.get('qa',{}).get('layered_source')
                for r in rs
            )
            if v046_layered:
                # v0.46'da bazı vanilla/FU hedeflerinin hem base asseti hem de
                # runtime'da onu değiştiren .patch katmanı bulunur. Görünür
                # kaynak metin patch'ten geliyorsa base dosyaya karşı test
                # etmek yanlış negatif üretir; exact source_patch değeri burada
                # doğrudan doğrulanır.
                patch_cache = {}
                for r in rs:
                    source_patch = r.get('qa',{}).get('source_patch')
                    if not source_patch:
                        raise ValueError('v0.46 layered source patch eksik: '+a+r['pointer'])
                    patch_path = args.source_dir/source_patch
                    if not patch_path.is_file():
                        raise FileNotFoundError(patch_path)
                    if source_patch not in patch_cache:
                        patch_cache[source_patch] = parse_jsonc(
                            patch_path.read_text(encoding='utf-8-sig')
                        )
                    found = None
                    for source_op in patch_cache[source_patch]:
                        if not isinstance(source_op,dict) or 'value' not in source_op:
                            continue
                        source_path = str(source_op.get('path',''))
                        if source_path == r['pointer']:
                            found = source_op['value']
                            continue
                        if source_path and r['pointer'].startswith(source_path+'/'):
                            try:
                                found = read_at(
                                    source_op['value'],
                                    r['pointer'][len(source_path):]
                                )
                            except (KeyError,IndexError,TypeError,ValueError):
                                pass
                    if found != r['en']:
                        raise ValueError(
                            'v0.46 layered kaynak uyuşmazlığı: '+a+r['pointer']
                        )
            elif source.is_file():
                simulate(parse_jsonc(source.read_text(encoding='utf-8-sig')),patch)
            elif all(r.get('qa',{}).get('layered_source') for r in rs):
                # Eski katmanlı kapsamların kendi sürüm provenance testleri korunur.
                pass
            else:
                raise FileNotFoundError(source)
"""
if "v046_layered = all(" not in s:
    if source_block not in s:
        raise ValueError("build layered-source block missing")
    s = s.replace(source_block, source_replacement, 1)
build_path.write_text(s, encoding="utf-8")

generator = r'''#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
import audit_remaining as audit

TOOLS = Path(__file__).resolve().parent
MANIFEST = TOOLS / "v046_translations.json"
CATALOG = TOOLS / "ceviriler.json"
CORE = __CORE__

def value_at(data, pointer):
    cur = data
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur

def patch_value(ops, pointer):
    found = None
    for op in ops:
        if not isinstance(op, dict):
            continue
        path = str(op.get("path", ""))
        if path == pointer and "value" in op:
            found = op["value"]
            continue
        if path and pointer.startswith(path + "/") and "value" in op:
            try:
                found = value_at(op["value"], pointer[len(path):])
            except (KeyError, IndexError, TypeError, ValueError):
                pass
    return found

def version_tuple(value):
    return tuple(map(int, value.split("-", 1)[0].split(".")))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = m["translations"]
    if m["translation_version"] != "0.46.0-beta":
        raise ValueError("v0.46 sürüm bilgisi bozuk")
    if len(rows) != 129 or len({(r["asset"], r["pointer"]) for r in rows}) != 129:
        raise ValueError("v0.46 alan kapsamı bozuk")
    if len({r["asset"] for r in rows}) != 53 or len({r["en"] for r in rows}) != 127:
        raise ValueError("v0.46 asset/kaynak kapsamı bozuk")
    if sum(r["asset"].startswith("ai/") for r in rows) != 89:
        raise ValueError("v0.46 SAIL/AI alan sayısı bozuk")
    species = [r for r in rows if r["asset"].startswith("species/")]
    if len(species) != 40 or {r["asset"] for r in species} != set(CORE):
        raise ValueError("v0.46 çekirdek ırk kapsamı bozuk")
    if set(CORE) != set(audit.AUDIT_CORE_PLAYABLE_SPECIES_ASSETS):
        raise ValueError("v0.46 audit çekirdek ırk listesi bozuk")

    cache = {}
    for row in rows:
        qa = row.get("qa", {})
        asset = row["asset"]
        pointer = row["pointer"]
        if qa.get("layered_source"):
            src = qa.get("source_patch")
            if not src or not src.endswith(".patch"):
                raise ValueError("v0.46 layered source eksik: " + asset + pointer)
            if src not in cache:
                path = args.source / src
                if not path.is_file():
                    raise FileNotFoundError(path)
                cache[src] = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
            actual = patch_value(cache[src], pointer)
        else:
            if asset not in cache:
                path = args.source / asset
                if not path.is_file():
                    raise FileNotFoundError(path)
                cache[asset] = audit.parse_jsonc(path.read_text(encoding="utf-8-sig"))
            actual = value_at(cache[asset], pointer)
        if actual != row["en"]:
            raise ValueError("v0.46 pinned kaynak uyuşmazlığı: " + asset + pointer)

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if version_tuple(catalog["translation_version"]) < (0, 46, 0):
        raise ValueError("Ana katalog v0.46 öncesinde")
    idx = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
    for row in rows:
        got = idx.get((row["asset"], row["pointer"]))
        if not got or got["en"] != row["en"] or got["tr"] != row["tr"]:
            raise ValueError("v0.46 katalog eşleşmesi eksik: " + row["asset"] + row["pointer"])
    print(json.dumps({
        "fields": 129,
        "assets": 53,
        "unique_source": 127,
        "ai_fields": 89,
        "species_fields": 40,
        "source_documents": len(cache),
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
'''
generator = generator.replace("__CORE__", repr(sorted(CORE_ASSETS)))
(TOOLS / "generate_v046.py").write_text(generator, encoding="utf-8")

test_text = r'''import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import audit_remaining as audit

SECTION = "v0.46 Irklar ve SAIL/AI"

class V046Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads((TOOLS / "v046_translations.json").read_text(encoding="utf-8"))
        cls.rows = cls.m["translations"]
        cls.by = {(r["asset"], r["pointer"]): r for r in cls.rows}

    def test_scope_is_exact(self):
        self.assertEqual(self.m["translation_version"], "0.46.0-beta")
        self.assertEqual(len(self.rows), 129)
        self.assertEqual(len({(r["asset"], r["pointer"]) for r in self.rows}), 129)
        self.assertEqual(len({r["asset"] for r in self.rows}), 53)
        self.assertEqual(len({r["en"] for r in self.rows}), 127)
        self.assertEqual(sum(r["asset"].startswith("ai/") for r in self.rows), 89)
        self.assertEqual(sum(r["asset"].startswith("species/") for r in self.rows), 40)
        self.assertTrue(all(r["section"] == SECTION for r in self.rows))

    def test_catalog_contains_exact_manifest(self):
        c = json.loads((TOOLS / "ceviriler.json").read_text(encoding="utf-8"))
        self.assertEqual(c["translation_version"], "0.46.0-beta")
        idx = {(r["asset"], r["pointer"]): r for r in c["translations"]}
        for r in self.rows:
            self.assertEqual(idx[(r["asset"], r["pointer"])]["en"], r["en"])
            self.assertEqual(idx[(r["asset"], r["pointer"])]["tr"], r["tr"])

    def test_species_runtime_scope(self):
        assets = {r["asset"] for r in self.rows if r["asset"].startswith("species/")}
        self.assertEqual(assets, set(audit.AUDIT_CORE_PLAYABLE_SPECIES_ASSETS))
        self.assertEqual(len(assets), 20)
        optional = audit.Candidate(
            "species/avali.species", "/charCreationTooltip/title", "Avali",
            "confirmed", "Irklar ve SAIL/AI", "species/avali.species", "title"
        )
        self.assertEqual(audit.v046_candidate_visibility(optional).confidence, "review")
        core = audit.Candidate(
            "species/fukirhos.species", "/charCreationTooltip/title", "Kirhos",
            "confirmed", "Irklar ve SAIL/AI", "species/fukirhos.species", "title"
        )
        self.assertEqual(audit.v046_candidate_visibility(core).confidence, "confirmed")

    def test_technical_raceeffect_labels_are_excluded(self):
        for asset, pointer in (
            ("species/irken.raceeffect", "/envEffects/0/scripts/0/args/label"),
            ("species/skelekin.raceeffect", "/liquidEffects/0/scripts/0/args/label"),
        ):
            row = audit.Candidate(
                asset, pointer, "env1", "confirmed", "Irklar ve SAIL/AI", asset, "label"
            )
            self.assertIsNone(audit.v046_candidate_visibility(row))

    def test_layered_sources_are_explicit(self):
        layered = [r for r in self.rows if r.get("qa", {}).get("layered_source")]
        self.assertEqual(len(layered), 30)
        for r in layered:
            self.assertTrue(r["qa"]["source_patch"].endswith(".patch"))

    def test_format_contracts(self):
        color = re.compile(r"\^[^;\s]*;")
        control = re.compile(r"\[(?![^\]]*\^)[^\]]+\]|<[^>]+>")
        number = re.compile(r"\d+(?:[.,]\d+)?")
        signed = re.compile(r"[+-]\s*%?\s*\d+(?:[.,]\d+)?")
        norm = lambda xs: sorted(
            x.replace(" ", "").replace("%", "").replace(",", ".") for x in xs
        )
        for r in self.rows:
            self.assertEqual(sorted(color.findall(r["en"])), sorted(color.findall(r["tr"])))
            self.assertEqual(sorted(control.findall(r["en"])), sorted(control.findall(r["tr"])))
            self.assertEqual(
                sorted(x.replace(",", ".") for x in number.findall(color.sub("", r["en"]))),
                sorted(x.replace(",", ".") for x in number.findall(color.sub("", r["tr"]))),
            )
            self.assertEqual(norm(signed.findall(r["en"])), norm(signed.findall(r["tr"])))
            self.assertEqual(r["en"].count("\n"), r["tr"].count("\n"))

    def test_reference_consistency_choices(self):
        juux = self.by[("species/juux.species", "/charCreationTooltip/description")]["tr"]
        self.assertIn("Psiyonik Odak", juux)
        self.assertNotIn("Psiyonik Fırlatıcı", juux)
        fenerox = self.by[("species/fenerox.species", "/charCreationTooltip/description")]["tr"]
        self.assertIn("Avcı Pençeleri", fenerox)
        floran = self.by[("species/floran.species", "/charCreationTooltip/description")]["tr"]
        self.assertIn("İğneleyici/Floran Silahları/Fırlatılanlar", floran)
        hylotl = self.by[("species/hylotl.species", "/charCreationTooltip/description")]["tr"]
        self.assertIn("Hylotl'lar", hylotl)

if __name__ == "__main__":
    unittest.main()
'''
(TOOLS / "tests" / "test_v046.py").write_text(test_text, encoding="utf-8")

build_workflow = ROOT / ".github" / "workflows" / "build-package.yml"
s = build_workflow.read_text(encoding="utf-8")
old = """      - name: Verify v0.45 layered quest sources
        run: python tools/generate_v045.py --source fu_source
"""
new = """      - name: Verify v0.45-v0.46 pinned translation sources
        run: |
          python tools/generate_v045.py --source fu_source
          python tools/generate_v046.py --source fu_source
"""
if "generate_v046.py" not in s:
    if old not in s:
        raise ValueError("build workflow v0.45 gate missing")
    s = s.replace(old, new, 1)
build_workflow.write_text(s, encoding="utf-8")

pr_workflow = ROOT / ".github" / "workflows" / "pr-qa.yml"
s = pr_workflow.read_text(encoding="utf-8")
old = """          python tools/generate_v045.py --source fu_source
          python tools/build_validate.py --source-dir fu_source --output build_output
"""
new = """          python tools/generate_v045.py --source fu_source
          python tools/generate_v046.py --source fu_source
          python tools/build_validate.py --source-dir fu_source --output build_output
"""
if "generate_v046.py" not in s:
    if old not in s:
        raise ValueError("PR workflow v0.45 gate missing")
    s = s.replace(old, new, 1)
pr_workflow.write_text(s, encoding="utf-8")

# Remove every temporary staging/workflow file before the tested source commit.
for path in (
    ROOT / ".github" / "workflows" / "v046-candidate-dump.yml",
    ROOT / ".github" / "workflows" / "v046-context-dump.yml",
    ROOT / ".github" / "workflows" / "v046-apply.yml",
    ROOT / ".github" / "workflows" / "v046-diagnose.yml",
    TOOLS / "v046_apply_temp.py",
):
    path.unlink(missing_ok=True)
shutil.rmtree(TOOLS / ".v046_parts", ignore_errors=True)
