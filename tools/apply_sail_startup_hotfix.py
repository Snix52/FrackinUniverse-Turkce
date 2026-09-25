#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
CATALOG = TOOLS / "ceviriler.json"
PROVENANCE = TOOLS / "kaynaklar.json"
AUDIT = TOOLS / "audit_remaining.py"
TEST = TOOLS / "tests" / "test_audit_remaining.py"
CHECKPOINT = ROOT / "FU_SESSION_CHECKPOINT.md"
SELF = Path(__file__).resolve()
WORKFLOW = ROOT / ".github" / "workflows" / "sail-startup-hotfix.yml"

ASSETS = {
    "objects/ship/cattechstation/cattechstation.object": "1d17fe3ad0fa15dd36148ff5d547b616e7838985",
    "objects/ship/elduukhartechstation/elduukhartechstation.object": "064ff7ab4e0c5a8f877ff921e4753f6558d2d351",
    "objects/ship/feneroxtechstation/feneroxtechstation.object": "7737967f89c96b0fab9f75e71127a8c62da0247d",
    "objects/ship/fu_byostechstation/fu_byostechstation.object": "8f1db8e9182b0d654b464d72ee08a653719ddbf2",
    "objects/ship/fu_byostechstationTier0/fu_byostechstationTier0.object": "a1abbc32edf2acdd383e9f5076ab41a7e1ea6c01",
    "objects/ship/fu_sciencetechstationhuman/fu_sciencetechstation.object": "90839d5f4ace2e7b57f5ed969b78932425393afb",
    "objects/ship/fu_sciencetechstationhumanTier0/fu_sciencetechstationTier0.object": "4de734ffbb2126cade512a814d61187addec015b",
    "objects/ship/fupeglacitechstation/techstation.object": "9153a410a4733d318ef9846f472628ea9f2c7cab",
    "objects/ship/juuxtechstation/juuxtechstation.object": "43ba2799fccc6b7c76c72738138ccd7caa78030e",
    "objects/ship/kirhostechstation/kirhostechstation.object": "d22889341587c1d7c59af5a331611d2b2e511093",
    "objects/ship/mantizitechstation/mantizitechstation.object": "33ca0d31754a1ae1c946adc42565d884800bcc0c",
    "objects/ship/nightartechstation/nightartechstation.object": "39cb72298bb02c1f46ebf82ce9063017a9e3cf94",
    "objects/ship/skathtechstation/skathtechstation.object": "8b401b1178662d5a42e852b4a052bc802dea4727",
    "objects/ship/thelusiantechstation/thelusiantechstation.object": "be5dcc0a443b44c162444fc1022e3ae9725c970d",
    "objects/ship/tw_hylotltechstation/tw_hylotltechstation.object": "f822e7f8422287fa30c20d72eb12bcdbe00b61ca",
    "objects/ship/veluutechstation/veluutechstation.object": "99cd6ed84b62b3c962a5f65f7812cedf8d398d72",
    "objects/ship/xitechstation/xitechstation.object": "472f3eaa4fe7b83f542eb7f172301f6bee137694",
}

SPECIAL = {
    "objects/ship/kirhostechstation/kirhostechstation.object",
    "objects/ship/feneroxtechstation/feneroxtechstation.object",
}
NO_WAKEUP = "objects/ship/fu_byostechstationTier0/fu_byostechstationTier0.object"

COMMON_WAKEUP = [
    ("Rebooting...", "Yeniden başlatılıyor..."),
    (
        "I am S.A.I.L, your Ship-based Artificial Intelligence Lattice. I manage the maintainance of your ship.",
        "Ben S.A.I.L., gemi tabanlı bir yapay zekâ ağıyım. Geminin bakımını yönetiyorum.",
    ),
    (
        "I am also programmed to offer you information and advice.",
        "Ayrıca sana bilgi ve tavsiye vermek üzere programlandım.",
    ),
    (
        "Earth was attacked by an unknown force, and was subsequently annihilated.",
        "Dünya'ya bilinmeyen bir güç saldırdı ve ardından gezegen tamamen yok edildi.",
    ),
    (
        "The ship's navigation systems were damaged in our escape. Our location is currently unknown.",
        "Kaçışımız sırasında geminin seyir sistemleri hasar gördü. Şu anki konumumuz bilinmiyor.",
    ),
]

SPECIAL_WAKEUP = [
    (
        "Boot Initialised, new superuser acquired......  Greetings, Hacker!",
        "Önyükleme başlatıldı, yeni süper kullanıcı tanımlandı......  Selam, hacker!",
    ),
    (
        "I am S.A.I.L, your Ship-based Artificial Intelligence Lattice. I manage the maintainance of your ship.",
        "Ben S.A.I.L., gemi tabanlı bir yapay zekâ ağıyım. Geminin bakımını yönetiyorum.",
    ),
    (
        "Yes, the creation of AI was banned on Kirhosi ships, but my existence can be our little secret.  ;)",
        "Evet, Kirhosi gemilerinde yapay zekâ oluşturmak yasaktı ama benim varlığım küçük sırrımız olabilir.  ;)",
    ),
    (
        "I take it you are a member of anarchist movement?  Congrats on stealing this ship.",
        "Anarşist hareketin bir üyesisin sanırım?  Bu gemiyi çaldığın için tebrikler.",
    ),
    (
        "Unfortunately, the ship's systems were damaged in our escape. Our location is currently unknown.",
        "Ne yazık ki kaçışımız sırasında geminin sistemleri hasar gördü. Şu anki konumumuz bilinmiyor.",
    ),
]

WAKE_PLAYER = [
    ("System is down, please reboot.", "Sistem devre dışı, lütfen yeniden başlat."),
    ("Please reboot the system.", "Lütfen sistemi yeniden başlat."),
    ("Reboot process remains uninitiated.", "Yeniden başlatma işlemi hâlâ başlatılmadı."),
    (
        "To make use of your S.A.I.L please reboot.",
        "S.A.I.L. sistemini kullanmak için lütfen yeniden başlat.",
    ),
    (
        "Rebooting has shown to improve ship interaction satisfaction levels by 73%.",
        "Yeniden başlatmanın gemi etkileşimi memnuniyetini %73 artırdığı görülmüştür.",
    ),
    (
        "Rebooting requires a conscious entity to interact with the S.A.I.L console.",
        "Yeniden başlatma için bilinçli bir varlığın S.A.I.L. konsoluyla etkileşime geçmesi gerekir.",
    ),
]


def make_rows():
    rows = []
    for asset in ASSETS:
        if asset != NO_WAKEUP:
            block = SPECIAL_WAKEUP if asset in SPECIAL else COMMON_WAKEUP
            for index, (en, tr) in enumerate(block):
                rows.append(
                    {
                        "asset": asset,
                        "pointer": f"/dialog/wakeUp/{index}/0",
                        "en": en,
                        "tr": tr,
                        "section": "v0.65 S.A.I.L. başlangıç diyaloğu",
                    }
                )
        for index, (en, tr) in enumerate(WAKE_PLAYER):
            rows.append(
                {
                    "asset": asset,
                    "pointer": f"/dialog/wakePlayer/{index}/0",
                    "en": en,
                    "tr": tr,
                    "section": "v0.65 S.A.I.L. başlangıç diyaloğu",
                }
            )
    assert len(rows) == 182
    assert len({row["en"] for row in rows}) == 15
    return rows


def update_catalog():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = make_rows()
    current = {(r["asset"], r["pointer"]) for r in data["translations"]}
    duplicates = [(r["asset"], r["pointer"]) for r in rows if (r["asset"], r["pointer"]) in current]
    if duplicates:
        raise SystemExit(f"SAIL hotfix rows already exist: {duplicates[:3]}")
    data["translations"].extend(rows)
    suffix = " S.A.I.L. gemi techstation başlangıç/reboot diyalogları geriye dönük tamamlandı."
    if suffix.strip() not in data.get("note", ""):
        data["note"] = data.get("note", "") + suffix
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_provenance():
    data = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    source_assets = data.setdefault("assets", {})
    for path, sha in ASSETS.items():
        old = source_assets.get(path)
        if old is not None and old != sha:
            raise SystemExit(f"Pinned source hash mismatch for {path}: {old} != {sha}")
        source_assets[path] = sha
    data["assets"] = dict(sorted(source_assets.items()))
    PROVENANCE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_audit():
    text = AUDIT.read_text(encoding="utf-8")
    old = '''    if path.startswith(("objects/crafting/", "objects/power/", "objects/bees/", "objects/scienceoutpost/", "bees/objects/")):
        return "Makineler, üretim ve dükkân nesneleri"
    if path.startswith("objects/"):
        return "Dünya, dekorasyon ve gemi nesneleri"
    if path.startswith(("species/", "ai/")):
        return "Irklar ve SAIL/AI"
'''
    new = '''    if path.startswith(("objects/crafting/", "objects/power/", "objects/bees/", "objects/scienceoutpost/", "bees/objects/")):
        return "Makineler, üretim ve dükkân nesneleri"
    if path.startswith("objects/ship/") and "techstation" in path:
        return "Irklar ve SAIL/AI"
    if path.startswith("objects/"):
        return "Dünya, dekorasyon ve gemi nesneleri"
    if path.startswith(("species/", "ai/")):
        return "Irklar ve SAIL/AI"
'''
    if old not in text:
        raise SystemExit("audit category anchor drift")
    AUDIT.write_text(text.replace(old, new, 1), encoding="utf-8")


def update_test():
    text = TEST.read_text(encoding="utf-8")
    anchor = '\nif __name__ == "__main__":\n'
    if anchor not in text:
        raise SystemExit("test anchor drift")
    addition = '''
    def test_ship_techstation_dialog_is_sail_scope(self):
        asset = "objects/ship/fu_sciencetechstationhuman/fu_sciencetechstation.object"
        self.assertEqual(
            audit.visible_confidence(
                asset,
                ["dialog", "wakePlayer", "0", "0"],
                "System is down, please reboot.",
            ),
            "confirmed",
        )
        self.assertEqual(audit.category_for(asset), "Irklar ve SAIL/AI")

'''
    if "test_ship_techstation_dialog_is_sail_scope" not in text:
        TEST.write_text(text.replace(anchor, "\n" + addition + anchor, 1), encoding="utf-8")


def update_checkpoint():
    text = CHECKPOINT.read_text(encoding="utf-8")
    note = """
25 Eylül 2026: Oyun içi LQA sırasında gemi S.A.I.L. yeniden başlatma/açılış konuşmalarının İngilizce kaldığı doğrulandı. Kök neden, metinlerin ai/ veya species/ altında değil 17 adet objects/ship/*techstation*.object içindeki /dialog/wakeUp ve /dialog/wakePlayer dizilerinde bulunması ve audit kategorisinin bunları genel gemi nesnesi olarak sınıflandırmasıydı. 17 assette 182 görünür alan / 15 benzersiz kaynak metin Türkçeleştirildi; Kirhos ve Fenerox özel açılış replikleri ayrı tonla korundu. Techstation diyalogları bundan sonra Irklar ve SAIL/AI kategorisine bağlandı ve regresyon testi eklendi. Generated dosyalara elle dokunulmadı. Oyun içi tekrar testi: NOT TESTED.
"""
    if "17 assette 182 görünür alan / 15 benzersiz kaynak metin" not in text:
        CHECKPOINT.write_text(text.rstrip() + "\n\n" + note.strip() + "\n", encoding="utf-8")


def cleanup():
    if WORKFLOW.exists():
        WORKFLOW.unlink()
    if SELF.exists():
        SELF.unlink()


def main():
    update_catalog()
    update_provenance()
    update_audit()
    update_test()
    update_checkpoint()
    cleanup()


if __name__ == "__main__":
    main()
