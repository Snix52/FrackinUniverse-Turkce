#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path, PurePosixPath
import audit_remaining as audit

CATEGORY = "Makineler, üretim ve dükkân nesneleri"
SECTION = "v0.32 makine, üretim ve dükkân arayüzü"
EXPECTED_FIELDS = 118
EXPECTED_ASSETS = 39
EXPECTED_UNIQUE = 87
TRANSLATIONS = json.loads(r'''{"Take all":"Tümünü Al","Take All":"Tümünü Al","Input":"Girdi","Output":"Çıktı","Search":"Ara","MATERIALS AVAILABLE":"MEVCUT MALZEMELER","^orange;Extraction Device^reset;":"^orange;Çıkarma Cihazı^reset;","FUEL SLOT":"YAKIT YUVASI","FUEL SLOTS":"YAKIT YUVALARI","Craft":"Üret","PRODUCT":"ÜRÜN","SCHEMATICS":"ŞEMALAR","Buy":"Satın Al","CAN AFFORD":"ALABİLİRSİN","PRODUCT DETAILS":"ÜRÜN BİLGİLERİ","GOODS":"ÜRÜNLER","A basic microscope designed to inspect queen bees. Works automatically.":"Ana arıları incelemek için tasarlanmış basit bir mikroskop. Otomatik çalışır.","^orange;Advanced^reset; Microscope":"^orange;Gelişmiş^reset; Mikroskop","Inspect Bees & Items":"Arıları ve Eşyaları İncele","Drag & Drop":"Sürükle ve Bırak","Centrifuge":"Santrifüj","Strictly speaking, I don't need to cook food to eat it, but it does reduce the energy necessary for digestion. Also, it just feels... right, somehow.":"Aslında yemek yiyebilmek için onu pişirmem gerekmiyor ama bu, sindirim için gereken enerjiyi azaltıyor. Üstelik bir şekilde daha... doğru hissettiriyor.","Insert Saplings":"Fidanları Yerleştir","Leaves on Right!":"Yapraklar Sağa!","^#b9b5b2;Place Pod in any slot.":"^#b9b5b2;Kapsülü herhangi bir yuvaya yerleştir.","Repair Image":"Görseli Onar","Hey you - yeah, you! C'mere a sec. You want in on some killer deals?":"Hey sen, evet sen! Bir gelsene. Kaçırılmayacak fırsatlar ister misin?","Pssst - hey kid! You interested in some... Furniture and furniture byproducts?":"Pssst, hey çocuk! Şey... mobilya ve mobilya yan ürünleriyle ilgilenir misin?","OKEA? ... Nope, uh, can't ever say I've heard of 'em. ... What's with that look?":"OKEA mı? ... Yok, hiç duymadım. ... O bakış ne?","Quality goods here, fallen right off the back of a truck! ... Er, not this one, though.":"Kaliteli mallar burada, kamyonun arkasından düşmüş gibi! ... Ee, ama bu kamyondan değil tabii.","Where do I get this stuff? I got a, er, supplier. Honest Dave. Swell guy, really.":"Bunları nereden mi buluyorum? Şey, bir tedarikçim var. Dürüst Dave. Harika adamdır, gerçekten.","I'm upset to hear about Earth, don't get me wrong, but I'd be lying if I said I'm not relieved to get the Protectorate off of my flippers.":"Dünya'ya olanlara üzüldüm, yanlış anlama; ama Protectorate'in artık tepemde olmamasından rahatladığımı inkâr edemem.","What, you think I can't drive this thing? Me and my booster seat would like to disagree.":"Ne, bunu süremeyeceğimi mi sanıyorsun? Ben ve yükseltici koltuğum aksini düşünüyoruz."," ^#dddddd;Create psionic weapons and gear.":" ^#dddddd;Psiyonik silah ve teçhizat üret."," ^#ffea00;Psionics Table":" ^#ffea00;Psiyonik Tezgâhı","^#b9b5b2;Place Servitor in the left slot.":"^#b9b5b2;Servitor'u soldaki yuvaya yerleştir.","Load Servitor":"Servitor'u Yükle"," Slowly works seeds":" Tohumları yavaşça işler"," SPROUTING TABLE":" FİLİZLENDİRME TEZGÂHI","Without the pain of the searing flame, the metal can never realize its potential.":"Yakıcı alevin acısı olmadan metal gerçek potansiyeline asla ulaşamaz."," ^#b9b5b2;Bars and ingredients":" ^#b9b5b2;Külçeler ve malzemeler"," Fission Furnace":" Fisyon Fırını","There is effectively nothing that this furnace cannot melt down.":"Bu fırının eritemeyeceği neredeyse hiçbir şey yok.","^orange;Fission Furnace^reset;":"^orange;Fisyon Fırını^reset;"," ^#b9b5b2;Health and well-being":" ^#b9b5b2;Sağlık ve bakım"," Health Center":" Sağlık Merkezi","A table with a bunch of medical tools.":"Bir sürü tıbbi alet bulunan bir masa.","A chance to display one's medical ability.":"Tıbbi becerilerimi sergilemek için bir fırsat.","A top-of-the-line medical station.":"Üst düzey bir tıbbi istasyon.","Floran ussse table. Patch ssself up.":"Floran masssayı kullanır. Kendini yamalar.","Inspired. Medical module activated.":"İlhamlı. Tıbbi modül etkinleştirildi.","I can use materials I've found here to create new healing items.":"Burada bulduğum malzemelerle yeni iyileştirme eşyaları üretebilirim.","This gives me the ability to heal and rejuvenate after incurring damage.":"Bu, hasar aldıktan sonra iyileşip kendimi toparlamamı sağlar.","This table looks good for treatin' wounds.":"Bu tezgâh yaraları sarmak için gayet iyi görünüyor.","^orange;Health Center^reset;":"^orange;Sağlık Merkezi^reset;"," ^#dddddd;Advanced textiles and more.":" ^#dddddd;Gelişmiş tekstiller ve daha fazlası."," ^9900ff;Clothing Fabricator^reset;":" ^9900ff;Giysi Üreticisi^reset;","A clothing fabricator. The Miniknog use these to enforce styles across the entire populace.":"Bir giysi üreticisi. Miniknog bunları tüm halka tek tip tarz dayatmak için kullanıyor.","A tool for working fabrics on an industrial scale.":"Kumaşları endüstriyel ölçekte işlemek için bir araç.","The best textile manipulator ever devised.":"Şimdiye kadar tasarlanmış en iyi tekstil işleme makinesi.","Machine sssew for Floran, work thread.":"Makine Floran için diker, ipliği işşşler.","Observant. A hyper-advanced tailoring tool.":"Gözlemci. Aşırı gelişmiş bir terzilik aracı.","A clothing fabricator. Maybe I can start my own fashion company.":"Bir giysi üreticisi. Belki kendi moda şirketimi kurabilirim.","It's not traditional in the least, but the clothes I can make with this will more than make up for it.":"Hiç geleneksel değil ama bununla yapabileceğim kıyafetler bu açığı fazlasıyla kapatır.","I could make myself a mighty fine new shirt with this.":"Bununla kendime pek şık yeni bir gömlek yapabilirim.","^orange;Clothing Fabricator^reset;":"^orange;Giysi Üreticisi^reset;"," Xenobiology Research":" Ksenobiyoloji Araştırmaları"," XENO RESEARCH LAB":" XENO ARAŞTIRMA LABORATUVARI","BRAIN JAR":"BEYİN KAVANOZU","Mix Two\nLiquids":"İki Sıvıyı\nKarıştır","WATER":"SU","WASTE SLOT":"ATIK YUVASI","  Never be sick again.":"  Bir daha asla hasta olma.","  PANACEA MEDICINES INC.":"  PANACEA MEDICINES INC.","Assemble":"Birleştir","Stop":"Durdur","Buy useful resources":"Yararlı kaynaklar satın al","ANSIBLE NETWORK":"ANSIBLE AĞI","  We'll grow on you!":"  Gönlünde filizleneceğiz!","  STARDEW ACRES":"  STARDEW ACRES","^shadow;No frequencies saved!":"^shadow;Kayıtlı frekans yok!","^shadow;Panacea Medicines Inc.":"^shadow;Panacea Medicines Inc.","^shadow;Accessing Ansible Network":"^shadow;Ansible Ağına erişiliyor","^shadow;Stardew Acres":"^shadow;Stardew Acres","^shadow;No power!":"^shadow;Güç yok!","^shadow;No signal currently set!":"^shadow;Ayarlanmış sinyal yok!","WASTE      COOLANT":"ATIK      SOĞUTUCU"}''')

def remaining_rows(source: Path):
    translated, _ = audit.load_translations(Path(__file__).with_name("ceviriler.json"))
    candidates = {}
    for path in sorted(source.rglob("*")):
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
            if row.asset in audit.V018_DEAD_OBJECT_ASSETS or row.asset in audit.AUDIT_EXCLUDED_PATHS:
                continue
            if audit.nonvisible_research_candidate(row.asset, row.pointer):
                continue
            key = (row.asset, row.pointer)
            prev = candidates.get(key)
            if prev is None or (prev.confidence == "review" and row.confidence == "confirmed"):
                candidates[key] = row
    return [
        row for key, row in sorted(candidates.items())
        if row.confidence == "confirmed" and row.category == CATEGORY and key not in translated
    ]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()
    rows = remaining_rows(args.source)
    if len(rows) != EXPECTED_FIELDS:
        raise ValueError(f"v0.32 alan sayısı değişti: {len(rows)} != {EXPECTED_FIELDS}")
    assets = {r.asset for r in rows}
    sources = {r.value for r in rows}
    if len(assets) != EXPECTED_ASSETS:
        raise ValueError(f"v0.32 asset sayısı değişti: {len(assets)} != {EXPECTED_ASSETS}")
    if len(sources) != EXPECTED_UNIQUE:
        raise ValueError(f"v0.32 kaynak metin sayısı değişti: {len(sources)} != {EXPECTED_UNIQUE}")
    catalog_path = Path(__file__).with_name("ceviriler.json")
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    existing_by_source = {}
    for current in catalog["translations"]:
        if current["en"] not in TRANSLATIONS:
            continue
        existing_by_source.setdefault(current["en"], set()).add(current["tr"])
    for source, choices in existing_by_source.items():
        if len(choices) != 1:
            raise ValueError(f"Mevcut çeviri belleği zaten tutarsız: {source!r} -> {sorted(choices)!r}")
        TRANSLATIONS[source] = next(iter(choices))

    missing = sorted(sources - TRANSLATIONS.keys())
    unused = sorted(TRANSLATIONS.keys() - sources)
    if missing or unused:
        raise ValueError(f"v0.32 çeviri haritası uyuşmuyor; missing={missing!r} unused={unused!r}")

    manifest = {
        "schema_version": 1,
        "translation_version": "0.32.0-beta",
        "scope": "Aktif makine, üretim ve dükkân arayüzleri; teknik kategori kimlikleri, devre dışı assetler ve şablon dummy metinleri hariç.",
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
    manifest_path = Path(__file__).with_name("v032_translations.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
    for row in manifest["translations"]:
        key = (row["asset"], row["pointer"])
        if key in index:
            raise ValueError(f"v0.32 alanı zaten katalogda: {key}")
        catalog["translations"].append(row)
        index[key] = row
    catalog["translation_version"] = manifest["translation_version"]
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"v0.32: {len(rows)} alan / {len(assets)} asset / {len(sources)} benzersiz metin")
    print(f"katalog: {len(catalog['translations'])} structured alan")

if __name__ == "__main__":
    main()
