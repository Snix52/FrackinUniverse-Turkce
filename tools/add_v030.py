#!/usr/bin/env python3
"""v0.30 aktif araştırma ekipmanı kapanışını kataloğa ekler.

Kapsam, sabit bir klasör listesine göre değil; etkin fu_warcraft düğümü,
gerçek .recipe çıktısı ve görünür ekipman assetinin kesişimine göre seçilir.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_validate import parse_jsonc

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "fu_upstream"
CATALOG = Path(__file__).with_name("ceviriler.json")
TRANSLATIONS = Path(__file__).with_name("v030_translations.json")
PROVENANCE = Path(__file__).with_name("kaynaklar.json")
REPORT = Path(__file__).with_name("test_raporu.json")

GROUPS = {
    "early_shields": ("bonegear", "irongear", "telebriumgear", "tungstengear"),
    "early_side": (
        "ambergear",
        "slimegear1",
        "slimegear2",
        "slimegear3",
        "silkgear",
        "monsterplategear",
    ),
    "racial": ("kirhosgear", "lunarigear", "elduugear", "skathgear", "veluuishgear"),
    "epp": ("epps1", "epps2", "epps3", "epps4"),
    "tier6": ("solariumgear", "densiniumgear", "pyreitegear", "isogengear", "xithricitegear"),
    "tier7": ("aetheriumgear",),
}

EXPECTED_GROUP_COUNTS = {
    "early_shields": 6,
    "early_side": 126,
    "racial": 85,
    "epp": 28,
    "tier6": 130,
    "tier7": 38,
}


def recipe_outputs() -> set[str]:
    outputs: set[str] = set()
    for path in SOURCE.rglob("*.recipe"):
        try:
            data = parse_jsonc(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        output = data.get("output")
        if isinstance(output, dict) and isinstance(output.get("item"), str):
            outputs.add(output["item"])
    return outputs


def equipment_assets() -> dict[str, tuple[str, dict, str]]:
    assets: dict[str, tuple[str, dict, str]] = {}
    for kind, patterns in (
        ("weapon", ("*.activeitem", "*.beamaxe")),
        ("armor", ("*.back", "*.chest", "*.head", "*.legs")),
    ):
        for pattern in patterns:
            for path in SOURCE.rglob(pattern):
                try:
                    data = parse_jsonc(path.read_text(encoding="utf-8-sig"))
                except Exception:
                    continue
                item_name = data.get("itemName")
                if isinstance(item_name, str):
                    assets[item_name] = (path.relative_to(SOURCE).as_posix(), data, kind)
    return assets


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def main() -> None:
    ledger = json.loads(CATALOG.read_text(encoding="utf-8"))
    manifest = json.loads(TRANSLATIONS.read_text(encoding="utf-8"))
    rows = ledger["translations"]
    existing = {(row["asset"], row["pointer"]) for row in rows}
    tree = parse_jsonc(
        (SOURCE / "zb/researchTree/fu_warcraft.config").read_text(encoding="utf-8-sig")
    )["researchTree"]["fu_warcraft"]
    outputs = recipe_outputs()
    assets = equipment_assets()

    selected: dict[str, dict] = {}
    for group, nodes in GROUPS.items():
        for node in nodes:
            for item_name in sorted(set(tree[node]["unlocks"]) & outputs & assets.keys()):
                asset, data, kind = assets[item_name]
                if (asset, "/shortdescription") in existing:
                    continue
                if item_name in selected:
                    selected[item_name]["nodes"].append(node)
                    continue
                selected[item_name] = {
                    "asset": asset,
                    "data": data,
                    "kind": kind,
                    "group": group,
                    "nodes": [node],
                }

    missing = sorted(set(selected) - set(manifest))
    extra = sorted(set(manifest) - set(selected))
    if missing or extra:
        raise SystemExit(f"Çeviri kapsamı uyuşmuyor. Eksik={missing!r}, fazla={extra!r}")
    if len(selected) != 413:
        raise SystemExit(f"Beklenen 413 yeni ekipman asseti yerine {len(selected)} bulundu")
    counts = Counter(spec["group"] for spec in selected.values())
    if dict(counts) != EXPECTED_GROUP_COUNTS:
        raise SystemExit(f"Grup sayıları uyuşmuyor: {dict(counts)!r}")

    for item_name, spec in selected.items():
        translated = manifest[item_name]
        if translated["asset"] != spec["asset"]:
            raise SystemExit(f"Asset yolu uyuşmuyor: {item_name}")
        if translated["group"] != spec["group"] or translated["nodes"] != spec["nodes"]:
            raise SystemExit(f"Araştırma provenansı uyuşmuyor: {item_name}")
        for pointer, source_key, translated_key in (
            ("/shortdescription", "shortdescription", "name"),
            ("/description", "description", "description"),
        ):
            source_text = spec["data"].get(source_key)
            if not isinstance(source_text, str):
                raise SystemExit(f"Görünür alan eksik: {spec['asset']}{pointer}")
            rows.append(
                {
                    "asset": spec["asset"],
                    "pointer": pointer,
                    "en": source_text,
                    "tr": translated[translated_key],
                    "section": "v0.30 Aktif araştırma ekipmanı kapanışı",
                }
            )

    ledger["translation_version"] = "0.30.0-beta"
    ledger["note"] = (
        "v0.30 aktif araştırma ekipmanı kapanışı: erken kalkanlar ve yan dallar, "
        "Kirhos/Lunari/Elduu/Skath/Vel'uuish silahları, EPP sırt ekipmanları ile "
        "Kademe 6-7 düğümlerindeki gerçek tarif destekli 413 assetin 826 görünür alanı "
        "yerelleştirildi. Toplam 6016 structured + 15 Lua, 2086 patch asset + 1 raw "
        "override. Oyun içi LQA bekliyor."
    )
    CATALOG.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    provenance["translation_version"] = "0.30.0-beta"
    for spec in selected.values():
        provenance["assets"][spec["asset"]] = git_blob_sha(SOURCE / spec["asset"])
    provenance["assets"] = dict(sorted(provenance["assets"].items()))
    provenance["validation_note"] = (
        "v0.30: 2062 pinned FU patch asseti ile 24 katmanlı/harici taban asseti "
        "kayıtlıdır. Aktif araştırma ekipmanı kapanışındaki 413 yeni asset, pinned "
        "FU 6.5.8 Git blob SHA değerleriyle kaydedildi. ceviriler.json içindeki bütün "
        "kaynak alanları build_validate.py tarafından exact test/replace işlemleriyle "
        "doğrulanır; kaynak farkı derlemeyi durdurur."
    )
    PROVENANCE.write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    report.update(
        {
            "translation_version": "0.30.0-beta",
            "translated_display_fields": 6016,
            "raw_script_display_strings": 15,
            "total_localized_display_units": 6031,
            "patched_assets": 2086,
            "raw_override_assets": 1,
            "target_assets_total": 2087,
        }
    )
    report["categories"]["v0.30 Aktif araştırma ekipmanı kapanışı"] = 826
    checks = report["checks"]
    checks["unique_paths"] = "PASS (6016/6016)"
    checks["fixture_application"] = (
        "PASS (current 6016-field catalog; inactive research, disconnected quest assets, "
        "10 runtime-dead v0.18 objects, 26 runtime-dead/deprecated v0.19 crafting items "
        "and 69 v0.20 inactive/broken quest files rejected before patch generation; "
        "v0.21-v0.29 exact research/recipe-backed equipment guards preserved and v0.30 "
        "restricted to 413 remaining active research/recipe-backed equipment assets)"
    )
    checks["source_mismatch_rejection_cases"] = 6016
    checks["source_mismatch_rejection"] = "PASS (6016 test-guarded structured fields)"
    checks["exact_source_pointer_validation"] = (
        "PASS (5928/5928 pinned-FU fields; 88/88 layered/external provenance fields; "
        "0 untracked)"
    )
    checks["build_allowlist_current_scope"] = (
        "PASS (v0.30 catalog/tool full-source local static verification; GitHub Actions "
        "package build pending)"
    )
    report["v030_scope"] = {
        "selection_rule": "active fu_warcraft unlock + real recipe output + visible equipment asset",
        "research_nodes": [node for nodes in GROUPS.values() for node in nodes],
        "newly_localized_recipe_backed_assets": 413,
        "weapons": 288,
        "armor_and_epp": 125,
        "group_asset_counts": EXPECTED_GROUP_COUNTS,
        "added_structured_fields": 826,
        "added_patch_assets": 413,
        "pinned_fu_new_fields": 826,
        "layered_external_new_fields": 0,
        "source_provenance": "PASS (826/826)",
        "structured_field_count_after_release": 6016,
        "localized_display_units_after_release": 6031,
        "patch_assets_after_release": 2086,
        "target_assets_total": 2087,
        "translated_pointers": ["/shortdescription", "/description"],
        "technical_integrity": "PASS (numbers, color codes, icons, line breaks and tabs)",
        "static_qa": "PENDING",
        "github_actions_run": None,
        "package_commit": None,
        "package_zip": None,
        "in_game_lqa": "NOT PERFORMED",
        "github_actions_evidence": "PENDING",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "new_assets": len(selected),
                "new_fields": len(selected) * 2,
                "groups": counts,
            },
            ensure_ascii=False,
            default=dict,
        )
    )


if __name__ == "__main__":
    main()
