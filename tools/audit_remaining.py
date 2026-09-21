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


from write_build_evidence import verify_source
from rule_data import rule as load_rule

PINNED_COMMIT = json.loads(Path(__file__).with_name('kaynaklar.json').read_text(encoding='utf-8'))['commit']
NONVISIBLE_RESEARCH_IDS = load_rule('NONVISIBLE_RESEARCH_IDS')
V018_DEAD_OBJECT_ASSETS = load_rule('V018_DEAD_OBJECT_ASSETS')
AUDIT_TECHNICAL_CATEGORY_VALUES = load_rule('AUDIT_TECHNICAL_CATEGORY_VALUES')
AUDIT_EXCLUDED_PATHS = load_rule('AUDIT_EXCLUDED_PATHS')
AUDIT_EXCLUDED_FIELDS = load_rule('AUDIT_EXCLUDED_FIELDS')
AUDIT_PATCH_APPEND_INDEXES = load_rule('AUDIT_PATCH_APPEND_INDEXES')

BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".ogg", ".wav", ".ase", ".aseprite",
    ".xcf", ".pdn", ".ttf", ".zip", ".pak", ".dll", ".exe", ".so",
}

EXCLUDED_PARTS = {
    "a_notyetadded", "a_modders", "deprecated", "obsolete", "unused",
    "disabled", "attic", "archive", "backup", "backups", ".git", "tilesets",
}

EXCLUDED_ROOTS = {"behaviors", "particles", "projectiles", "recipes"}
REVIEW_ONLY_ROOTS = {"dungeons"}

CATEGORY_VISIBLE_SUFFIXES = {
    ".object", ".activeitem", ".item", ".matitem", ".consumable", ".head",
    ".chest", ".legs", ".back", ".augment", ".thrownitem", ".liqitem",
    ".beamaxe", ".miningtool", ".harvestingtool", ".inspectiontool",
    ".flashlight", ".wiretool", ".painttool", ".tillingtool", ".blueprint",
}

EXPLICIT_VISIBLE_KEYS = {
    "shortdescription", "description", "title", "subtitle", "text",
    "completiontext", "turnindescription", "displayname", "friendlyname",
    "label", "caption", "tooltip", "tooltiptext", "hovertext", "helptext",
    "buttontext", "prompt", "question", "response", "message",
    "successmessage", "failuremessage", "errormessage", "statustext",
    "objectivetext", "chargentext", "charcreationtooltip", "speciesname",
    "sendername", "nameplate", "windowtitle", "maintitle", "hint",
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


def visible_confidence(asset: str, parts: list[str], value: str) -> str | None:
    if not isinstance(value, str) or not value.strip() or not ALPHA_RE.search(value):
        return None
    key = parts[-1].lower() if parts else ""
    ancestors = {part.lower() for part in parts[:-1]}
    if (key == "value" and len(parts) >= 2 and str(parts[-2]).lower() == "path"
            and "/" in value and re.fullmatch(r"[A-Za-z0-9_./-]+", value.strip())):
        return None
    if key.startswith("//"):
        # Tiled editörünün açıklama/metaveri alanları; oyunda gösterilmez.
        return None
    if key == "category":
        if value.strip() in AUDIT_TECHNICAL_CATEGORY_VALUES:
            return None
        return "confirmed" if PurePosixPath(asset).suffix.lower() in CATEGORY_VISIBLE_SUFFIXES else None
    if key in TECHNICAL_KEYS:
        return None
    if looks_like_resource(value):
        return None
    if key == "tooltip" and value.strip() == "base":
        return None
    if value.strip() == "Replace Me":
        return None
    if value.strip() == "Lvl. 100" and "listtemplate" in ancestors:
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
    suffix = PurePosixPath(path).suffix.lower()
    if suffix in {".item", ".matitem", ".consumable", ".augment", ".thrownitem", ".liqitem", ".blueprint"}:
        return "Malzeme, tüketilebilir ve diğer eşyalar"
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
    if path.parts and path.parts[0].lower() in EXCLUDED_ROOTS:
        return True
    name = path.name.lower()
    if name in {".metadata", "steamtext_info.txt"}:
        return True
    return any(token in name for token in (".disabled", ".unused", ".old", ".bak", "_bak", "~"))


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
        confidence = visible_confidence(asset, parts, node)
        if confidence:
            if asset.split("/", 1)[0].lower() in REVIEW_ONLY_ROOTS:
                confidence = "review"
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
    if (source_path.endswith(".questtemplate") and isinstance(data, dict)
            and data.get("invisible") is True and data.get("logOnly") is True
            and data.get("showInLog") is False and data.get("showAcceptDialog") is False):
        return
    if source_path.endswith(".patch"):
        asset = source_path[:-6]
        if isinstance(data, list):
            for index, operation in enumerate(data):
                if not isinstance(operation, dict) or "value" not in operation:
                    continue
                base = split_pointer(str(operation.get("path", "")))
                if "-" in base and asset in AUDIT_PATCH_APPEND_INDEXES:
                    base = [str(AUDIT_PATCH_APPEND_INDEXES[asset]) if part == "-" else part for part in base]
                yield from walk_values(asset, operation["value"], base, f"{source_path}#{index}")
            return
        yield from walk_values(asset, data, [], source_path)
        return
    yield from walk_values(source_path, data, [], source_path)


def nonvisible_research_candidate(asset: str, field_pointer: str) -> bool:
    parts = split_pointer(field_pointer)
    return (
        len(parts) >= 3
        and parts[0] == "strings"
        and parts[1] == "research"
        and parts[2] in NONVISIBLE_RESEARCH_IDS.get(asset, set())
    )


def audit_excluded_candidate(asset: str, field_pointer: str) -> bool:
    return field_pointer in AUDIT_EXCLUDED_FIELDS.get(asset, frozenset())


def load_translations(catalog_path: Path) -> tuple[set[tuple[str, str]], int]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    rows = catalog.get("translations", [])
    keys = {
        (str(row["asset"]), str(row["pointer"]))
        for row in rows
        if isinstance(row, dict) and row.get("asset") and row.get("pointer")
    }
    return keys, len(rows)


def load_raw_lua_translations(path: Path) -> set[tuple[str, str]]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    translated: set[tuple[str, str]] = set()
    for asset in data.get("assets", []):
        asset_path = str(asset.get("asset", ""))
        for replacement in asset.get("replacements", []):
            visible = str(replacement.get("display_en", ""))
            if asset_path and visible:
                translated.add((asset_path, visible))
    return translated


LUA_LITERAL = re.compile(r"(['\"])((?:\\.|(?!\1).)*)\1")
LUA_DISPLAY_CALLS = (
    ("widget.settext", "last"),
    ("canvas:drawtext", "first"),
    ("object.say", "first"),
    ("npc.say", "first"),
    ("say(", "first"),
)


def audit_lua(source: Path, raw_catalog: Path) -> dict[str, Any]:
    translated = load_raw_lua_translations(raw_catalog)
    rows: list[dict[str, Any]] = []
    for path in sorted(source.rglob("*.lua")):
        rel = PurePosixPath(path.relative_to(source).as_posix())
        if excluded_path(rel):
            continue
        try:
            lines = path.read_text(encoding="utf-8-sig").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("--"):
                continue
            lowered = stripped.lower()
            mode = next((candidate_mode for marker, candidate_mode in LUA_DISPLAY_CALLS if marker in lowered), None)
            if not mode:
                continue
            literal_matches = list(LUA_LITERAL.finditer(stripped))
            if not literal_matches:
                continue
            selected = literal_matches[-1] if mode == "last" else literal_matches[0]
            if "widget.settext" in lowered:
                call_start = lowered.find("widget.settext")
                comma = stripped.find(",", call_start)
                if comma < 0:
                    continue
                # Tek literal ilk argümansa widget kimliğidir, gösterilen metin değildir.
                if len(literal_matches) == 1 and selected.start() < comma:
                    continue
                between = lowered[comma:selected.start()]
                if "getparameter" in between or "assetjson" in between:
                    continue
            value = bytes(selected.group(2), "utf-8").decode("unicode_escape")
            clean = re.sub(r"\^[^;\s]*;", "", value).strip()
            if not clean or not ALPHA_RE.search(clean) or looks_like_resource(clean):
                continue
            if (rel.as_posix(), clean) in translated:
                continue
            # Tek kelimelik küçük harfli widget kimliklerini metin sanma.
            if re.fullmatch(r"[a-z][a-z0-9_.]*", clean):
                continue
            rows.append({
                "asset": rel.as_posix(),
                "line": line_number,
                "source": clean[:500],
            })
    return {
        "detected_remaining_literals": len(rows),
        "assets": len({row["asset"] for row in rows}),
        "known_translated_literals": len(translated),
        "samples": rows[:100],
        "scope_note": "Heuristic review pool for direct widget/canvas/NPC display calls; not a full Lua semantic analysis.",
    }


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
            if candidate.asset in V018_DEAD_OBJECT_ASSETS or candidate.asset in AUDIT_EXCLUDED_PATHS:
                continue
            if audit_excluded_candidate(candidate.asset, candidate.pointer):
                continue
            if nonvisible_research_candidate(candidate.asset, candidate.pointer):
                continue
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
        values: defaultdict[str, set[str]] = defaultdict(set)
        for row in rows.values():
            assets[row.category].add(row.asset)
            values[row.category].add(row.value)
        return {
            name: {
                "assets": len(assets[name]),
                "fields": fields[name],
                "unique_source_strings": len(values[name]),
            }
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
            "confirmed_unique_source_strings": len({row.value for row in remaining_confirmed.values()}),
            "review_unique_source_strings": len({row.value for row in remaining_review.values()}),
            "confirmed_source_characters": sum(len(row.value) for row in remaining_confirmed.values()),
            "confirmed_by_category": grouped(remaining_confirmed),
            "review_by_category": grouped(remaining_review),
            "confirmed_by_source_root": grouped_roots(remaining_confirmed),
            "review_by_source_root": grouped_roots(remaining_review),
        },
        "remaining_confirmed_key_frequency": dict(key_frequency.most_common()),
        "ui_confirmed_rows": [
            {
                "asset": row.asset,
                "pointer": row.pointer,
                "source": row.value,
                "key": row.key,
                "origin": row.origin,
            }
            for row in sorted(
                (candidate for candidate in remaining_confirmed.values() if candidate.category == "Arayüz"),
                key=lambda item: (item.asset, item.pointer),
            )
        ],
        "ui_review_rows": [
            {
                "asset": row.asset,
                "pointer": row.pointer,
                "source": row.value,
                "key": row.key,
                "origin": row.origin,
            }
            for row in sorted(
                (candidate for candidate in remaining_review.values() if candidate.category == "Arayüz"),
                key=lambda item: (item.asset, item.pointer),
            )
        ],
        "samples_by_category": dict(samples),
        "parse_failures": parse_failures,
        "translated_not_found": [
            {"asset": asset, "pointer": field_pointer}
            for asset, field_pointer in sorted(translated_not_found)
        ],
        "lua_review": audit_lua(source, catalog_path.with_name("raw_text_translations.json")),
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
        f"| Doğrudan ekrana basılan Lua inceleme havuzu | {result['lua_review']['assets']:,} | {result['lua_review']['detected_remaining_literals']:,} |",
        "",
        "## Kalan doğrulanmış kapsam",
        "",
        "| Kategori | Asset | Alan | Benzersiz kaynak metin |",
        "|---|---:|---:|---:|",
    ]
    for category, counts in remaining["confirmed_by_category"].items():
        lines.append(
            f"| {category} | {counts['assets']:,} | {counts['fields']:,} | "
            f"{counts['unique_source_strings']:,} |"
        )
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

    source_validation = verify_source(args.source.resolve())
    result = audit(args.source.resolve(), args.catalog.resolve())
    result['source_validation'] = source_validation
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.md_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.md_output.write_text(markdown_report(result), encoding="utf-8")
    print(markdown_report(result))


if __name__ == "__main__":
    main()
