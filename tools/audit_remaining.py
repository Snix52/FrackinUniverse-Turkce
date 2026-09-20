#!/usr/bin/env python3
"""FU 6.5.8 içindeki çevrilebilir ve henüz çevrilmemiş metinleri sayar.

Bu araç çeviri üretmez. Sabit FU kaynağını tarar, oyuncuya görünmesi muhtemel
JSON/JSONC alanlarını mevcut ceviriler.json kataloğuyla karşılaştırır ve iki
havuz çıkarır:

* confirmed: Starbound/FU şemalarında doğrudan oyuncuya gösterilen alanlar
* review: arayüz/diyalog bağlamında görünür olabilen, elle doğrulanacak alanlar

Teknik kimlikler, dosya yolları, script adları ve devre dışı kaynaklar sayılmaz.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


PINNED_COMMIT = "329e714b3fe87571055c8ad7aa38135d199d3317"

BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".ogg", ".wav", ".ase", ".aseprite",
    ".xcf", ".pdn", ".ttf", ".zip", ".pak", ".dll", ".exe", ".so",
}

EXCLUDED_PARTS = {
    "a_notyetadded", "a_modders", "deprecated", "obsolete", "unused",
    "disabled", "attic", "archive", "backup", "backups", ".git", "tilesets",
}

EXPLICIT_VISIBLE_KEYS = {
    "shortdescription", "description", "title", "subtitle", "text",
    "completiontext", "turnindescription", "displayname", "friendlyname",
    "label", "caption", "tooltip", "tooltiptext", "hovertext", "helptext",
    "buttontext", "prompt", "question", "response", "message",
    "successmessage", "failuremessage", "errormessage", "statustext",
    "objectivetext", "chargentext", "charcreationtooltip", "speciesname",
    "sendername", "nameplate", "windowtitle", "maintitle", "hint", "category",
}

VISIBLE_CONTAINERS = {
    "strings", "contentpages", "chatoptions", "dialog", "dialogs",
    "scripteddialogs", "radiomessages", "messages", "greeting", "greetings",
    "converse", "chatter", "tenantdialog", "questdialog", "descriptions",
    "tooltips", "labels", "captions",
}

TECHNICAL_KEYS = {
    "type", "kind", "id", "messageid", "itemname", "objectname", "questid", "species",
    "rarity", "inventoryicon", "image", "icon", "portrait",
    "script", "scripts", "animation", "animationparts", "animationcustom",
    "config", "path", "file", "directory", "projectiletype", "statuseffect",
    "effect", "action", "command", "function", "parameters", "item",
    "object", "monster", "npc", "stagehand", "biome", "material", "liquid",
    "sound", "music", "asset", "recipe", "output", "input", "pool",
}

RESOURCE_SUFFIXES = (
    ".png", ".jpg", ".jpeg", ".gif", ".ogg", ".wav", ".lua", ".config",
    ".patch", ".frames", ".animation", ".object", ".item", ".activeitem",
    ".projectile", ".statuseffect", ".npctype", ".monsterpart", ".monstertype",
    ".recipe", ".matitem", ".material", ".cinematic", ".questtemplate",
)

VISIBLE_SUFFIX_RE = re.compile(
    r"(?:description|text|message|caption|label|tooltip|title)$", re.IGNORECASE
)
ALPHA_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĞğİıŞşÇçÜüÖö]")
POINTER_ESCAPE = str.maketrans({"~": "~0", "/": "~1"})


@dataclass(frozen=True)
class Candidate:
    asset: str
    pointer: str
    value: str
    confidence: str
    category: str
    origin: str
    key: str


def parse_jsonc(text: str) -> Any:
    out: list[str] = []
    i = 0
    quoted = False
    escaped = False
    while i < len(text):
        char = text[i]
        if quoted:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            i += 1
            continue
        if char == '"':
            quoted = True
            out.append(char)
            i += 1
            continue
        if text.startswith("//", i):
            end = text.find("\n", i + 2)
            if end < 0:
                break
            out.append("\n")
            i = end + 1
            continue
        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end < 0:
                raise ValueError("Unterminated JSON comment")
            out.append(" ")
            i = end + 2
            continue
        out.append(char)
        i += 1

    clean = "".join(out)
    out = []
    i = 0
    quoted = False
    escaped = False
    while i < len(clean):
        char = clean[i]
        if quoted:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            i += 1
            continue
        if char == '"':
            quoted = True
            out.append(char)
            i += 1
            continue
        if char == ",":
            look = i + 1
            while look < len(clean) and clean[look].isspace():
                look += 1
            if look < len(clean) and clean[look] in "]}":
                i += 1
                continue
        out.append(char)
        i += 1
    return json.loads("".join(out), strict=False)


def pointer(parts: Iterable[str]) -> str:
    return "".join("/" + str(part).translate(POINTER_ESCAPE) for part in parts)


def split_pointer(value: str) -> list[str]:
    if not value or value == "/":
        return []
    return [part.replace("~1", "/").replace("~0", "~") for part in value.lstrip("/").split("/")]


def looks_like_resource(value: str) -> bool:
    clean = re.sub(r"\^[^;\s]*;", "", value).strip()
    lower = clean.lower().split("?")[0].split(":")[-1]
    if lower.endswith(RESOURCE_SUFFIXES):
        return True
    if clean.startswith(("/", "./", "../")) and " " not in clean:
        return True
    if re.fullmatch(r"[A-Za-z0-9_./-]+:[A-Za-z0-9_./-]+", clean):
        return True
    return False


def visible_confidence(parts: list[str], value: str) -> str | None:
    if not isinstance(value, str) or not value.strip() or not ALPHA_RE.search(value):
        return None
    key = parts[-1].lower() if parts else ""
    ancestors = {part.lower() for part in parts[:-1]}
    if key.startswith("//"):
        # Tiled editörünün açıklama/metaveri alanları; oyunda gösterilmez.
        return None
    if key in TECHNICAL_KEYS:
        return None
    if looks_like_resource(value):
        return None
    if key in EXPLICIT_VISIBLE_KEYS:
        return "confirmed"
    if VISIBLE_SUFFIX_RE.search(key) and key not in TECHNICAL_KEYS:
        return "confirmed"
    if ancestors & VISIBLE_CONTAINERS:
        return "confirmed"
    if key == "value" and (
        ancestors & {
            "gui", "window", "windowconfig", "widget", "widgets", "button", "buttons",
            "title", "subtitle", "label", "labels", "caption", "textbox", "list",
        }
        or any("layout" in ancestor or ancestor.startswith(("lbl", "btn")) for ancestor in ancestors)
    ):
        return "confirmed"
    if ancestors & {"gui", "interface", "windowconfig", "scriptconfig"}:
        # Bu bağlamdaki key'lenmemiş değerlerin bir bölümü kullanıcı metnidir;
        # otomatik kesin sayıya katılmaz, elle gözden geçirme havuzunda tutulur.
        return "review"
    return None


def category_for(asset: str) -> str:
    path = asset.lower()
    if path.startswith(("zb/", "research/")):
        return "Araştırma ve görev arayüzü"
    if path.startswith("quests/"):
        return "Görevler"
    if path.startswith(("radiomessages/", "dialog/", "npcs/", "tenants/")):
        return "NPC, radyo ve diyalog"
    if path.startswith("codex/") or "/codex/" in path:
        return "Codex ve lore"
    if path.startswith(("interface/", "metagui/", "fu_metagui/")):
        return "Arayüz"
    if path.startswith(("items/active/", "items/armors/", "items/shields/")):
        return "Silah, zırh ve aktif ekipman"
    if path.startswith(("items/", "bees/bees/", "bees/combs/", "bees/frames/")):
        return "Malzeme, tüketilebilir ve diğer eşyalar"
    if path.startswith(("objects/crafting/", "objects/power/", "objects/bees/", "objects/scienceoutpost/", "bees/objects/")):
        return "Makineler, üretim ve dükkân nesneleri"
    if path.startswith("objects/"):
        return "Dünya, dekorasyon ve gemi nesneleri"
    if path.startswith(("species/", "ai/")):
        return "Irklar ve SAIL/AI"
    if path.startswith("monsters/"):
        return "Canavarlar"
    if path.startswith(("cinematics/", "cutscenes/")):
        return "Sinematikler"
    if path.startswith(("biomes/", "celestial/", "dungeons/", "liquids/", "materials/", "tiles/", "plants/")):
        return "Biyom, zindan ve dünya sistemleri"
    return "Diğer oyuncu metinleri"


def excluded_path(path: PurePosixPath) -> bool:
    lowered = {part.lower() for part in path.parts}
    if lowered & EXCLUDED_PARTS:
        return True
    name = path.name.lower()
    return any(token in name for token in (".disabled", ".unused", ".old", ".bak", "~"))


def walk_values(
    asset: str,
    node: Any,
    parts: list[str],
    origin: str,
) -> Iterable[Candidate]:
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk_values(asset, value, parts + [str(key)], origin)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_values(asset, value, parts + [str(index)], origin)
    elif isinstance(node, str):
        confidence = visible_confidence(parts, node)
        if confidence:
            yield Candidate(
                asset=asset,
                pointer=pointer(parts),
                value=node,
                confidence=confidence,
                category=category_for(asset),
                origin=origin,
                key=parts[-1] if parts else "",
            )


def candidates_from_data(source_path: str, data: Any) -> Iterable[Candidate]:
    if source_path.endswith(".patch"):
        asset = source_path[:-6]
        if isinstance(data, list):
            for index, operation in enumerate(data):
                if not isinstance(operation, dict) or "value" not in operation:
                    continue
                base = split_pointer(str(operation.get("path", "")))
                yield from walk_values(asset, operation["value"], base, f"{source_path}#{index}")
            return
        yield from walk_values(asset, data, [], source_path)
        return
    yield from walk_values(source_path, data, [], source_path)


def load_translations(catalog_path: Path) -> tuple[set[tuple[str, str]], int]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    rows = catalog.get("translations", [])
    keys = {
        (str(row["asset"]), str(row["pointer"]))
        for row in rows
        if isinstance(row, dict) and row.get("asset") and row.get("pointer")
    }
    return keys, len(rows)


def audit(source: Path, catalog_path: Path) -> dict[str, Any]:
    translated, catalog_rows = load_translations(catalog_path)
    candidates: dict[tuple[str, str], Candidate] = {}
    parse_failures: list[dict[str, str]] = []
    scanned_files = 0
    parsed_files = 0
    excluded_files = 0

    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel = PurePosixPath(path.relative_to(source).as_posix())
        if excluded_path(rel):
            excluded_files += 1
            continue
        if path.suffix.lower() in BINARY_SUFFIXES or path.stat().st_size > 8_000_000:
            continue
        scanned_files += 1
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, OSError):
            continue
        stripped = raw.lstrip()
        if not stripped.startswith(("{", "[")):
            continue
        try:
            data = parse_jsonc(raw)
        except Exception as exc:  # Kaynak kusurları ayrıca görünür kalsın.
            parse_failures.append({"path": rel.as_posix(), "error": str(exc)[:240]})
            continue
        parsed_files += 1
        for candidate in candidates_from_data(rel.as_posix(), data):
            key = (candidate.asset, candidate.pointer)
            previous = candidates.get(key)
            if previous is None or (previous.confidence == "review" and candidate.confidence == "confirmed"):
                candidates[key] = candidate

    confirmed = {key: row for key, row in candidates.items() if row.confidence == "confirmed"}
    review = {key: row for key, row in candidates.items() if row.confidence == "review"}
    remaining_confirmed = {key: row for key, row in confirmed.items() if key not in translated}
    remaining_review = {key: row for key, row in review.items() if key not in translated}
    translated_found = translated & set(candidates)
    translated_not_found = translated - set(candidates)

    def grouped(rows: dict[tuple[str, str], Candidate]) -> dict[str, dict[str, int]]:
        fields = Counter(row.category for row in rows.values())
        assets: defaultdict[str, set[str]] = defaultdict(set)
        for row in rows.values():
            assets[row.category].add(row.asset)
        return {
            name: {"assets": len(assets[name]), "fields": fields[name]}
            for name in sorted(fields)
        }

    def grouped_roots(rows: dict[tuple[str, str], Candidate]) -> dict[str, dict[str, int]]:
        fields: Counter[str] = Counter()
        assets: defaultdict[str, set[str]] = defaultdict(set)
        for row in rows.values():
            root = row.asset.split("/", 1)[0]
            fields[root] += 1
            assets[root].add(row.asset)
        return {
            root: {"assets": len(assets[root]), "fields": fields[root]}
            for root in sorted(fields, key=lambda item: (-fields[item], item))
        }

    samples: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in sorted(remaining_confirmed.values(), key=lambda item: (item.category, item.asset, item.pointer)):
        if len(samples[row.category]) < 20:
            samples[row.category].append({
                "asset": row.asset,
                "pointer": row.pointer,
                "source": row.value[:280],
            })

    key_frequency = Counter(row.key for row in remaining_confirmed.values())
    result = {
        "schema": 1,
        "pinned_fu_commit": PINNED_COMMIT,
        "rules": {
            "confirmed": "Known player-visible schema fields and visible text containers.",
            "review": "Possible UI/dialog values requiring manual context confirmation.",
            "excluded": "Technical IDs/resources plus deprecated, disabled, unused and not-yet-added paths.",
        },
        "inventory": {
            "scanned_text_files": scanned_files,
            "parsed_jsonc_files": parsed_files,
            "excluded_path_files": excluded_files,
            "parse_failures": len(parse_failures),
        },
        "catalog": {
            "rows": catalog_rows,
            "unique_structured_fields": len(translated),
            "matched_by_audit": len(translated_found),
            "not_in_audit_candidates": len(translated_not_found),
        },
        "source_visible_inventory": {
            "confirmed_fields": len(confirmed),
            "confirmed_assets": len({row.asset for row in confirmed.values()}),
            "review_fields": len(review),
            "review_assets": len({row.asset for row in review.values()}),
        },
        "remaining": {
            "confirmed_fields": len(remaining_confirmed),
            "confirmed_assets": len({row.asset for row in remaining_confirmed.values()}),
            "review_fields": len(remaining_review),
            "review_assets": len({row.asset for row in remaining_review.values()}),
            "confirmed_by_category": grouped(remaining_confirmed),
            "review_by_category": grouped(remaining_review),
            "confirmed_by_source_root": grouped_roots(remaining_confirmed),
            "review_by_source_root": grouped_roots(remaining_review),
        },
        "remaining_confirmed_key_frequency": dict(key_frequency.most_common()),
        "samples_by_category": dict(samples),
        "parse_failures": parse_failures,
        "translated_not_found": [
            {"asset": asset, "pointer": field_pointer}
            for asset, field_pointer in sorted(translated_not_found)
        ],
    }
    return result


def markdown_report(result: dict[str, Any]) -> str:
    remaining = result["remaining"]
    inventory = result["source_visible_inventory"]
    catalog = result["catalog"]
    lines = [
        "# FU Türkçe kalan kapsam denetimi",
        "",
        f"Kaynak: FrackinUniverse 6.5.8 / `{result['pinned_fu_commit']}`",
        "",
        "## Net tablo",
        "",
        "| Ölçü | Asset | Görünür alan |",
        "|---|---:|---:|",
        f"| Kaynaktaki doğrulanmış görünür envanter | {inventory['confirmed_assets']:,} | {inventory['confirmed_fields']:,} |",
        f"| Mevcut kataloğun benzersiz structured kapsamı | - | {catalog['unique_structured_fields']:,} |",
        f"| Kalan doğrulanmış kapsam | {remaining['confirmed_assets']:,} | {remaining['confirmed_fields']:,} |",
        f"| Elle bağlam kontrolü gereken ek havuz | {remaining['review_assets']:,} | {remaining['review_fields']:,} |",
        "",
        "## Kalan doğrulanmış kapsam",
        "",
        "| Kategori | Asset | Alan |",
        "|---|---:|---:|",
    ]
    for category, counts in remaining["confirmed_by_category"].items():
        lines.append(f"| {category} | {counts['assets']:,} | {counts['fields']:,} |")
    lines.extend([
        "",
        "## Denetim sağlığı",
        "",
        f"- JSON/JSONC parse edilen dosya: {result['inventory']['parsed_jsonc_files']:,}",
        f"- Yol kuralıyla dışlanan dosya: {result['inventory']['excluded_path_files']:,}",
        f"- Parse hatası: {result['inventory']['parse_failures']:,}",
        f"- Mevcut çevirilerden tarayıcıyla eşleşen alan: {catalog['matched_by_audit']:,}",
        f"- Tarayıcı adaylarında bulunmayan mevcut alan: {catalog['not_in_audit_candidates']:,}",
        "",
        "Not: Oyun içi font, taşma ve bağlam LQA'sı bu sayılara dahil değildir.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, default=Path("tools/ceviriler.json"))
    parser.add_argument("--json-output", type=Path, default=Path("audit_output/kalan_kapsam.json"))
    parser.add_argument("--md-output", type=Path, default=Path("audit_output/KALAN_KAPSAM.md"))
    args = parser.parse_args()

    result = audit(args.source.resolve(), args.catalog.resolve())
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.md_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.md_output.write_text(markdown_report(result), encoding="utf-8")
    print(markdown_report(result))


if __name__ == "__main__":
    main()
