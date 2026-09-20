#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_validate import parse_jsonc

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "fu_upstream"
CATALOG = Path(__file__).with_name("ceviriler.json")
NODES = ("advancealloygear", "durasteelgear")

# itemName: (shortdescription, description)
TR = {
    # Advanced Alloy
    "advalloycrossbow": ("Alaşım Arbalet", "Hantal bir arbalet. Ama aslında o kadar da ağır değil."),
    "advalloylongsword": ("Ustanın Uzun Kılıcı", "Karbondan dövülmüş. Öfkeyle sağlamlaştırılmış.\n^cyan;Kanamaya yol açar^reset;"),
    "advalloyshotgun": ("Alaşım Pompalı Tüfek", "Hassas tetikli, üstün kaliteli bir pompalı tüfek."),
    "advalloystynger": ("Alaşım Stynger", "Ek kütlesine rağmen inanılmaz derecede hafif."),
    "curvebroadsword": ("Breach Plazma Satırı", "Plazma ağızlı bir yakın dövüş satırı.\n^cyan;Set bonusları için plazma silahı sayılır^reset;\n^yellow;Yanma etkisi uygular^reset;"),
    "curvedagger": ("Breach Bıçağı", "Plazmayla yüklenmiş bir bıçak. Pek kullanışlı.\n^cyan;Yanma etkisi uygular^reset;"),
    "curvepistol": ("Breach Tabancası", "Uzay korsanlarına özgü bir plazma tabancası.\n^yellow;+Seker ve yakar^reset;"),
    "curvesmg": ("Breach Püskürtücü", "Uzay korsanlarının gözde plazma silahı.\n^yellow;+Seker ve yakar^reset;"),
    "curvestaff": ("Plazma Dövüş Asası", "Bir asa için epey kılıcımsı. Ziiiip zaaaap!\n^cyan;Set bonusları için plazma silahı sayılır^reset;"),
    "fucellgun": ("Hücresel Tüfek", "Hücresel maddeden ^cyan;dondurucu^reset; ve ^green;zehirli^reset; patlamalar ateşleyen, gerçekten eşsiz bir uzun menzil tüfeği."),
    "fugaussmachinegun": ("Gauss Makineli Tüfek", "Manyetik temelli, acımasız derecede etkili bir silah.\n^yellow;Alan hasarı^reset;\n^yellow;Av silahı^reset;"),
    "fugausspistol": ("Gauss Tabancası", "Manyetik temelli, acımasız derecede etkili bir silah.\n^yellow;Alan hasarı^reset;\n^yellow;Av silahı^reset;"),
    "fugaussrifle": ("Gauss Tüfeği", "Manyetik temelli, acımasız derecede etkili bir silah.\n^yellow;Alan hasarı^reset;\n^yellow;Av silahı^reset;"),
    "fugaussshotgun": ("Gauss Pompalı Tüfek", "Manyetik temelli, acımasız derecede etkili bir silah.\n^yellow;Alan hasarı^reset;\n^yellow;Av silahı^reset;"),
    "fugausssniper": ("Gauss Keskin Nişancı Tüfeği", "Çok kademeli bobinlere bağlı güçlü kapasitörler.\n^yellow;Alan hasarı^reset;\n^yellow;Av silahı^reset;\n^yellow;Yüksek hızlı mermi^reset;"),
    "isn_microwaveray": ("Sonik Top", "Gösterişli görünen ses dalgaları ateşler!\n^yellow;Sanırım fena değil^reset;\n^green;Belki seversin?^reset;"),
    "magnorbfrost": ("Ayaz Fırlatıcı", "Buz gibi soğuk."),
    "mobiuspistol": ("Nöbetçi Tabancası", "Kökeni sırlarla örtülü bir tabanca.\n^yellow;Donmuş ateşe yol açar^reset;"),
    "mobiusrailgun": ("Nöbetçi Raylı Tüfek", "Bu canavar düşmanı resmen katleder!\n^yellow;Donmuş ateşe yol açar^reset;\n^cyan;Taarruz Dronları çağırır^reset;"),
    "mobiusrifle": ("Nöbetçi Tüfeği", "Gelişmiş birliklerin vazgeçilmez silahı. Pek azı onunla boy ölçüşebilir.\n^yellow;Donmuş ateşe yol açar^reset;\n^cyan;Kalkan Dronları çağırır^reset;"),
    "nigtarbow": ("Parlak Çelik Yayı", "Özel üretilmiş okları tüm elementlere eşit hasar verir ama avlanmada da işe yarar."),

    # Durasteel
    "durasteelassaultrifle2": ("Durasteel Seri Atış Tüfeği", "Seri atış yapan, askerî sınıf otomatik bir tüfek."),
    "durasteelaxe": ("Durasteel Balta", "Bu şaheseri aşabilecek balta sayısı pek azdır."),
    "durasteelboomerang": ("Durasteel Bumerang", "Havalı ve tehlikeli."),
    "durasteeldagger": ("Durasteel Hançer", "Durasteel'den özenle işlenmiş bir hançer."),
    "durasteelgreataxe": ("Durasteel Büyük Balta", "Özenle işlenmiş bir Durasteel büyük balta."),
    "durasteelhammer": ("Durasteel Çekiç", "Heybetli bir Durasteel çekiç."),
    "durasteelkatana": ("Durasteel Katana", "Çoğu silahla boy ölçüşebilecek güçte.\n^yellow;5 vuruşluk kombo^reset;\n^cyan;Kanamaya yol açar^reset;"),
    "durasteelmace": ("Durasteel Topuz", "Kalın ve ağır. Tasarım: Sacre."),
    "durasteelmachinepistol": ("Durasteel Makineli Tabanca", "Ciddi tepme gücüne sahip büyük bir tabanca."),
    "durasteelshield": ("Durasteel Kalkan", "^green;Kritik Şansı +3%, Kritik Hasarı +5^reset;"),
    "durasteelshortspear": ("Durasteel Kısa Mızrak", "Düşmanlara hiç de kısa gelmez.\n^cyan;Av silahı^reset;"),
    "durasteelshotgun": ("Durasteel Pompalı Tüfek", "Yakın mesafede ölümcül bir saçma yayılımıyla ateş eder."),
    "durasteelsniperrifle": ("Durasteel Keskin Nişancı Tüfeği", "Uzun mesafeleri aşacak kadar güçlü."),
    "durasteelspear": ("Durasteel Mızrak", "En iyiler arasında yer alan bir Durasteel mızrak.\n^cyan;Av silahı^reset;"),
    "energyblade": ("Enerji Bıçağı", "Fife Krallığı'ndan bir silah."),
    "flaildurasteel": ("Durasteel Ezici", "Ağır, hantal ve muhteşem.\n^cyan;Blokları kırar^reset;"),
    "floatstaff": ("Yerçekimi Değneği", "^cyan;quiqksilver^reset; tarafından dövülmüş. Yerçekimini kontrol et!"),
    "friendmaker": ("Dost Yapan", "Muazzam hasar potansiyeli."),
    "fu_lasereyestaff": ("Göz Bastonu", "Oldukça ilginç bir teknolojik silah."),
    "fucarbonhandcannon": ("Patlama Çekici", "Acımasız derecede etkili bir tabanca.\n^cyan;Pompalı tarzı seri atışlar^reset;"),
    "fucoralcleaver": ("Mercan Satırı", "Keskin ve tehlikeli. Bir arkadaşına ver!"),
    "ionstrike": ("Yörünge Saldırısı", "Acımasız bir enerji patlaması salvosu.\n^cyan;Roket veya Enerji sayılır^reset;"),
    "moltenaxe": ("Erimiş Balta", "Ateş ve kükürt."),
    "pistoldurasteelfu": ("Durasteel Magnum", "Yüksek kalibreli mermiler ateşler.\n^yellow;Yüksek hasarlı mermiler.^reset;"),
    "rifledurasteelfu": ("Durasteel Tüfek", "Güvenilir, isabetli ve üretimi ucuz."),
    "shurikencannon": ("Shuriken Topu", "Bunun çabucak arkadaş edinmeye yarayacağına eminim."),
    "xenoshield": ("X10 Kalkan", "^green;+0.05 Can Yenilenmesi, -20% Düşme Hasarı^reset;"),
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


def active_combat_assets() -> dict[str, tuple[str, dict]]:
    assets: dict[str, tuple[str, dict]] = {}
    for pattern in ("*.activeitem", "*.beamaxe"):
        for path in SOURCE.rglob(pattern):
            try:
                data = parse_jsonc(path.read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            item_name = data.get("itemName")
            if isinstance(item_name, str):
                assets[item_name] = (path.relative_to(SOURCE).as_posix(), data)
    return assets


def main() -> None:
    ledger = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = ledger["translations"]
    existing = {(row["asset"], row["pointer"]) for row in rows}
    tree = parse_jsonc(
        (SOURCE / "zb/researchTree/fu_warcraft.config").read_text(encoding="utf-8-sig")
    )["researchTree"]["fu_warcraft"]
    unlocked = {item for node in NODES for item in tree[node]["unlocks"]}
    outputs = recipe_outputs()
    assets = active_combat_assets()

    selected: dict[str, tuple[str, dict]] = {}
    for item_name in sorted(unlocked):
        if item_name not in outputs or item_name not in assets:
            continue
        asset, data = assets[item_name]
        if (asset, "/shortdescription") in existing:
            continue
        selected[item_name] = (asset, data)

    missing = sorted(set(selected) - set(TR))
    extra = sorted(set(TR) - set(selected))
    if missing or extra:
        raise SystemExit(f"TR kapsamı uyuşmuyor. Eksik={missing!r}, fazla={extra!r}")
    if len(selected) != 48:
        raise SystemExit(f"Beklenen 48 yeni combat asseti yerine {len(selected)} bulundu")

    for item_name, (asset, data) in sorted(selected.items(), key=lambda pair: pair[1][0]):
        short_tr, description_tr = TR[item_name]
        for pointer, source_key, translated in (
            ("/shortdescription", "shortdescription", short_tr),
            ("/description", "description", description_tr),
        ):
            source_text = data.get(source_key)
            if not isinstance(source_text, str):
                raise SystemExit(f"Görünür alan eksik: {asset}{pointer}")
            rows.append(
                {
                    "asset": asset,
                    "pointer": pointer,
                    "en": source_text,
                    "tr": translated,
                    "section": "v0.23 Kademe 4 çekirdek savaş ekipmanı",
                }
            )

    ledger["translation_version"] = "0.23.0-beta"
    ledger["note"] = (
        "v0.23 Kademe 4 çekirdek savaş ekipmanı: aktif Zırh ve Silahlar araştırma "
        "ağacındaki advancealloygear ve durasteelgear düğümlerinin açtığı, gerçek üretim "
        "tarifi bulunan 48 savaş ekipmanında 96 görünür alan yerelleştirildi. Toplam "
        "4028 structured + 15 Lua, 1092 patch asset + 1 raw override. Oyun içi LQA bekliyor."
    )
    CATALOG.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"new_assets": len(selected), "new_fields": len(selected) * 2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
