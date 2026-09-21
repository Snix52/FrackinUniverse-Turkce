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
NODES = (
    "tritaniumgear",
    "enrichedgear",
    "violiumgear",
    "feroziumgear",
    "aegisaltgear",
    "densealloygear",
    "effigiumgear",
)

# itemName: (shortdescription, description)
TR = {
    # Kalkanlar
    "bubbleshield": ("Su Kalkanı", "^green;+0.1% Can Yenilenmesi, +20% Enerji^reset;"),
    "hellfireshield": ("Cehennem Ateşi Kalkanı", "^green;+9% Enerji Yenilenmesi, Bağışıklık: Lav, Yanma^reset;"),
    "warswornshield": ("Savaş Yeminlisi Kalkanı", "^green;-20% Düşme Hasarı, +10 Kalkan Darbesi^reset;"),
    "shadowshield": ("Gölge Kalkanı", "^green;+3 Savunma^reset;\n^cyan;Bağışıklık: Asit^reset;"),
    "tritaniumshield": ("Tritanium Kalkanı", "^green;-30% Düşme Hasarı^reset;"),

    # Yaylar ve arbaletler
    "lightningcrossbow": ("Yıldırım Arbaleti", "Elektrik saçıyor!"),
    "lightningstynger": ("Yıldırım Stynger", "Yıldırım fırtınası gibi oklar yağdırır."),
    "shadowstring": ("Gölge Kirişi", "Piyasadaki en karanlık yay."),

    # Baltalar
    "effigiumaxe": ("Hayalet Balta", "Bir ruh kadar hayaletimsi."),
    "poweraxe": ("Tritanium Balta", "Kuş çıkacak, gülümse!\n^cyan;Elektriklenmeye ve Sekmeye yol açar^reset;"),
    "uraniumaxe": ("Uranyum Balta", "Zenginleştirilmiş uranyumdan yapılmış."),

    # Büyük kılıçlar
    "effigiumbroadsword": ("Hayalet Büyük Kılıç", "Bir ruh kadar hayaletimsi.\n^cyan;Caliginous Gazına yol açar^reset;"),
    "uraniumbroadsword": ("Uranyum Kılıcı", "Bu kesinlikle iyi bir fikre benziyor!"),

    # Hançerler
    "effigiumdagger": ("Hayalet Bıçak", "Bir ruh kadar hayaletimsi."),
    "fushadowdagger": ("Gölgepençe", "Gölgede dövülmüş bir hançer.\n^cyan;Gölge Hasarı^reset;"),
    "uraniumdagger": ("Uranyum Bıçak", "Hızlı ve radyoaktif."),

    # Eziciler
    "flailaegisalt": ("Aegisalt Ezici", "Ağır, hantal ve muhteşem.\n^cyan;Blokları kırar^reset;"),
    "flaileffigium": ("Effigium Ezici", "Yoğun gölge maddesi yayar.\n^cyan;Blokları kırar^reset;"),

    # Çekiçler
    "effigiumhammer": ("Hayalet Çekiç", "Bir ruh kadar hayaletimsi."),
    "fuquantumhammer": ("Kuantum Çekici", "İki evrenin arasında duruyor. İnanılmaz.\n^red;Fiziksel Hasar verir^reset;"),
    "uraniumhammer": ("Uranyum Çekiç", "Uranyum ve gelişmiş alaşımdan dövülmüş. Oldukça radyoaktif."),

    # Katanalar ve uzun kılıçlar
    "blooddiamondkatana": ("Plazmik Kristal Katana", "Ölümcül bir vaatle parıldıyor.\n^yellow;6 vuruşluk kombo^reset;\n^green;Kombolar kanamaya yol açar^reset;"),
    "diamondkatana": ("Elmas Katana", "İki elle kullanılan, ışıl ışıl bir elmas. Olağanüstü güzel ve ölümcül.\n^yellow;8 vuruşluk kombo^reset;"),
    "blooddiamondlongsword": ("Plazmik Kristal Uzun Kılıç", "Kristalimsi bir nefretle parlıyor."),
    "effigiumlongsword": ("Hayalet Kılıç", "Bir ruh kadar hayaletimsi.\n^cyan;Caliginous Gazına yol açar^reset;"),
    "violiumlongsword": ("Violium Uzun Kılıç", "Yıldız kökenli Violium parçacıkları ve karbondan dövülmüş."),

    # Topuzlar
    "aegisaltmace": ("Aegisalt Topuz", "Yoğun bir külçe dolusu ezme eğlencesi."),
    "densealloymace": ("Yoğun Alaşım Topuzu", "İyi işlenmiş ama ağır. Tasarım: Gezbo."),
    "effigiummace": ("Hayalet Topuz", "Hayaletlerin umurunda olmaz. Seni yine de öldürürler. Tasarım: Gezbo."),
    "quantummace": ("Kuantum Topuzu", "Sorma, çünkü Bilim."),
    "uraniummace": ("Uranyum Topuzu", "Kesinlikle zehirsiz."),

    # Dövüş asaları ve meçler
    "diamondquarterstaff": ("Elmas Dövüş Asası", "Son derece değerli bir silah."),
    "effigiumrapier": ("Hayalet Meç", "Bir ruh kadar hayaletimsi."),

    # Kısa mızraklar
    "tritaniumshortspear": ("Tritanium Kısa Mızrak", "Şahane bir saplama aleti.\n^cyan;Elektriklenmeye yol açar^reset;\n^cyan;Av silahı^reset;"),

    # Kısa kılıçlar
    "effigiumshortsword": ("Hayalet Savaş Bıçağı", "Bir ruh kadar hayaletimsi."),
    "heliosblade": ("Helios", "Morphite, tehlikeli bir kusursuzlukla bilenmiş."),
    "obsidianblade": ("Obsidyen Kılıç", "Volkanik cam ne kadar güzel ve keskin."),
    "shadowburst": ("Gölge Biçici", "Kadim ve bilinmeyen malzemelerden yapılmış bir ruh parçalayıcı.\n^red;Kanamaya yol açar^reset;"),
    "uraniumshortsword": ("Uranyum Savaş Bıçağı", "Aslında oldukça ölümcül."),

    # Mızraklar
    "banespear": ("Felaket Mızrağı", "Son derece şık ve incelikli bir delici silah.\n^cyan;Av silahı^reset;"),
    "effigiumspear": ("Hayalet Mızrak", "Bir ruh kadar hayaletimsi.\n^cyan;Av silahı^reset;"),
    "tritaniumspear": ("Tritanium Mızrağı", "Bunu bilim uğruna bir düşmana saplamalısın!\n^cyan;Elektriklenmeye yol açar^reset;\n^cyan;Av silahı^reset;"),
    "uraniumspear": ("Uranyum Kargısı", "Ölümcül zenginleştirilmiş uranyumla doldurulmuş. Ne kadar düşüncelisin.\n^cyan;Av silahı^reset;"),

    # Magnorb'lar
    "magnorbhellfire": ("Cehennem Ateşi Küreleri", "Yakıp kavuran eğlenceyle dolu."),
    "magnorbneutron": ("Nötron Yıldızı Küreleri", "Üstün yerçekimi küreleri. ^cyan;Set bonusları için 'enerji' silahı sayılır^reset;"),
    "magnorbshadow": ("Gölge Küreleri", "Düşmanlara katılaşmış gölge fırlatır."),

    # Özel menzilli silahlar
    "artillerygun": ("Kararsız Füze Salvosu", "Yıkıcı bir füze saldırısı çağırır. Blokları yok eder.\n^cyan;Alternatif atış hasarı artırır^reset;"),
    "bigdaddy": ("Kışkırtıcı", "Devasa bir enerji keskin nişancı tüfeği. Büyük darbe.\n^yellow;Birincil atış alanı engeller^reset;"),
    "farsight": ("FarSight XR-20", "Acımasız bir uzun menzil tüfeği.\n^yellow;Kanamaya yol açar^reset;"),
    "fucyclone": ("Siklon", "Minik ölüm saçmaları fırlatır. Hem de çok, çok hızlı."),
    "fuplasmacannon": ("Plazma Püskürtücü", "En yüksek hasar çıktısı için enerjiyi odaklar.\n^cyan;Set bonusları için plazma silahı sayılır^reset;\n^yellow;Blokları yok eder^reset;"),
    "fuplasmagun": ("Plazma Tüfeği", "En yüksek hasar çıktısı için enerjiyi odaklar.\n^cyan;Set bonusları için plazma silahı sayılır^reset;\n^yellow;Blokları yok eder^reset;"),
    "futritaniumpistol": ("Azgın Ateş", "Deli mermilerle olağanüstü bir atış hızı sunar."),
    "gravgun": ("Yerçekimi Silahı", "Yerçekimini odaklanmış patlamalara yoğunlaştırır.\n^cyan;Düşmanları çok güçlü biçimde savurur.^reset;\n^yellow;Aşırı Geri Tepme (Alternatif)^reset;"),
    "gravitongun": ("Graviton Tüfeği", "Mikro yerçekimi silaha dönüştürülmüş.\n^yellow;Birincil atış dalga patlamasıdır^reset;\nAlternatif: ^green;Güçlü geri tepme, Büyük Savunmasızlık^reset;"),
    "gravitonpistol": ("Graviton Tabancası", "Mikro yerçekimi silaha dönüştürülmüş.\n^yellow;Kısa menzilli^reset;\n^green;Muazzam geri tepme^reset;"),
    "mineralcannonadv": ("Parçacık Tüfeği", "Muazzam bir patlama potansiyeli.\n^yellow;Blokları yok eder^reset;"),
    "nitrogengun": ("Azot Topu", "Biraz dondurucu olsa da çoğu durumda etkilidir.\n^yellow;Donma etkisi uygular^reset;"),
    "nitrogenpistol": ("Azot Makineli Tabanca", "Biraz dondurucu olsa da çoğu durumda etkilidir.\n^yellow;Donma etkisi uygular^reset;"),

    # Peglaci silahları
    "chargecannon": ("Radyasyon Yükleyici", "Radyoaktif-elektrik patlamalarını doldurup serbest bırakır.\n^yellow;Dolduruldukça hasarı artar^reset;"),
    "chargemachinegun": ("Sakatlayıcı Makineli Tüfek", "Seri atışlı radyoaktif eğlence!\n^yellow;Radyasyon Yanığına yol açar^reset;"),
    "fufreezecannon": ("Ani Soğuk", "Buz bulutları bırakan bir silah.\n^yellow;Patlamalar hedefleri kaydırır^reset;\n^cyan;Alternatif atış düşmanları dondurur^reset;"),
    "frostcannonarm": ("Mistral Buz Püskürtücü", "Dondurucu sisler keyfin için silaha dönüştürülmüş.\n^yellow;Donma etkisi uygular^reset;\n^green;Çoklu atış^reset;"),
    "fubeamgun": ("Işın Tüfeği", "Düşmanlarını kavurması garanti, yoğun bir ışın."),
    "fucloudgun": ("Patlama Topu", "Patlayıcı gaz bulutları ateşler.\n^yellow;Aşırı gürültülü^reset;\n^green;Devasa patlama alanı^reset;"),
    "fuenergyblaster": ("Enerji Atıcı", "Denetimli enerji kullanan son derece yararlı bir silah.\n^yellow;Olağanüstü işlevsellik^reset;\n^cyan;Elektriklenmeye yol açar^reset;"),
    "fuenergymachinegun": ("Biçici", "Violium kökenli acımasız patlamalar düşmanları parçalar.\n^yellow;Elektriklenmeye yol açar^reset;\n^cyan;Yavaşlatma etkisi uygular^reset;"),
    "fuminelayer": ("Mayın Fırlatıcı", "Mayın tarlalarıyla düşmanlarını kıymaya çevir.\n^yellow;Yanma etkisi uygular^reset;\n^green;Geniş bir alanı mahveder^reset;"),
    "furailgun": ("Raylı Tüfek", "Yıkıcı bir uzun menzil tüfeği.\n^yellow;Blokları deler, menzille birlikte hasarı artar^reset;\n^cyan;Verimli alternatif atış^reset;"),
    "fushocklance": ("Şok Kargısı", "Şok edici derecede ölümcül.\n^yellow;Yıkıcı alternatif atış^reset;\n^cyan;Birincil atış ek fiziksel hasar verir^reset;"),
    "fuaegisaltminigun": ("Imperius Döner Makineli Tüfeği", "Olağanüstü güçlü.\n^yellow;Alternatif atış düşmanları yavaşlatır^reset;\n^green;+Kesintisiz Atış^reset;\n^red;-Yavaşlatılmış^reset;"),
    "splittergun": ("Fissure Ayrık Tüfek", "Peglaci onları geliştirdi, sen ise kusursuzlaştırdın. Yıkıcı bir silah."),

    # Cevher tabancaları ve tüfekleri
    "pistolaegisaltfu": ("Aegisalt Revolver", "Yüksek kalibreli mermiler ateşler.\n^yellow;Yüksek hasarlı mermiler^reset;"),
    "pistoleffigiumfu": ("Effigium Revolver", "Yüksek kalibreli mermiler ateşler.\n^yellow;Yüksek hasarlı mermiler.^reset;"),
    "pistolferoziumfu": ("Ferozium Revolver", "Yüksek kalibreli mermiler ateşler.\n^yellow;Yüksek hasarlı mermiler^reset;"),
    "pistolirradiumfu": ("Irradium Revolver", "Yüksek kalibreli mermiler ateşler.\n^yellow;Yüksek hasarlı mermiler.^reset;"),
    "pistolvioliumfu": ("Violium Revolver", "Yüksek kalibreli mermiler ateşler.\n^yellow;Yüksek hasarlı mermiler^reset;"),
    "rifleaegisaltfu": ("Aegisalt Tüfek", "Güvenilir, isabetli ve üretimi ucuz."),
    "rifleeffigiumfu": ("Effigium Tüfek", "Güvenilir, isabetli ve üretimi ucuz."),
    "rifleferoziumfu": ("Ferozium Tüfek", "Güvenilir, isabetli ve üretimi ucuz."),
    "rifleirradiumfu": ("Irradium Tüfek", "Güvenilir, isabetli ve üretimi ucuz."),
    "riflevioliumfu": ("Violium Tüfek", "Güvenilir, isabetli ve üretimi ucuz."),

    # Bilim silahları
    "isn_annihilator": ("Dalga Tüfeği", "Fizik kurallarını yok sayan sıra dışı patlamalar ateşler.\n^yellow;Duvarları yok sayar^reset;"),
    "isn_flamethrower4": ("İnferno", "Oldukça büyük bir alev silahı.\n^yellow;Yanma etkisi uygular^reset;"),
    "isn_fusioncannon": ("Füzyon Topu", "Süper ağır bir füzyon roketatarı.\n^yellow;Devasa etki alanı^reset;\n^green;Blokları yok eder^reset;"),
    "isn_plasmabeam": ("Plazma Işın Topu", "Yavaş ama yıkıcı. Helyn Sektöründe yasaktır.\n^cyan;Set bonusları için plazma silahı sayılır^reset;\n^yellow;Aşırı güçlü patlama^reset;\n^red;Ağır^reset;"),
    "isn_plasmapistol": ("Plazma Tabancası", "Sıra dışı bir çağ için sıra dışı bir tabanca.\n^cyan;Set bonusları için plazma silahı sayılır^reset;\n^yellow;Seken mermiler^reset;"),
    "isn_terawattlaser": ("XT Lazer Tekrarlayıcı", "Atış hızı mı istedin? Al sana!\n^yellow;Seken mermiler^reset;"),
    "veilbreaker": ("Perdekıran", "Acımasız ve verimli bir silah."),

    # Asalar ve değnekler
    "gravitystaff": ("Madde Asası", "^orange;Birincil^reset;: Ön Plan, ^orange;İkincil^reset;: Arka Plan."),
    "effigiumstaff": ("Effigium Asası", "Bir Caliginous Gazı bulutu oluşturur."),
    "tritaniumstaff": ("Tritanium Asası", "Fırtına bulutları oluşturur."),
    "shadowstaff": ("Gölge Asası", "Bu güçlü asa, ölümcül bir gölge yılanı çağırır."),
    "effigiumwand": ("Effigium Değneği", "Yeterince Gelişmiş Teknoloji."),
    "tritaniumwand": ("Tritanium Değneği", "Yeterince Gelişmiş Teknoloji."),

    # Kırbaçlar
    "effigiumwhip": ("Effigium Kırbacı", "Hayaletimsi bir kamçı. Oldukça kısa ama hızlı savrulur.\n^cyan;Caliginous Gazına yol açar^reset;"),
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
                if item_name in assets:
                    raise SystemExit(f"Yinelenen savaş ekipmanı itemName: {item_name}")
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

    all_selected: dict[str, tuple[str, dict]] = {}
    selected: dict[str, tuple[str, dict]] = {}
    for item_name in sorted(unlocked):
        if item_name not in outputs or item_name not in assets:
            continue
        asset, data = assets[item_name]
        all_selected[item_name] = (asset, data)
        if (asset, "/shortdescription") in existing:
            continue
        selected[item_name] = (asset, data)

    missing = sorted(set(selected) - set(TR))
    extra = sorted(set(TR) - set(selected))
    if missing or extra:
        raise SystemExit(f"TR kapsamı uyuşmuyor. Eksik={missing!r}, fazla={extra!r}")
    if len(all_selected) != 97 or len(selected) != 96:
        raise SystemExit(
            f"Beklenen 97 tarifli / 96 yeni Kademe 5 savaş ekipmanı yerine "
            f"{len(all_selected)} / {len(selected)} bulundu"
        )

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
                    "section": "v0.28 Kademe 5 savaş ekipmanı",
                }
            )

    ledger["translation_version"] = "0.28.0-beta"
    ledger["note"] = (
        "v0.28 Kademe 5 savaş ekipmanı: Zırh ve Silahlar araştırma ağacındaki "
        "tritaniumgear, enrichedgear, violiumgear, feroziumgear, aegisaltgear, "
        "densealloygear ve effigiumgear düğümlerinin açtığı, gerçek üretim tarifi "
        "bulunan 97 savaş ekipmanı doğrulandı. Önceden çevrilmiş Ferozium Satırı "
        "korunarak kalan 96 assette 192 görünür alan yerelleştirildi. Toplam 5068 "
        "structured + 15 Lua, 1612 patch asset + 1 raw override. Oyun içi LQA bekliyor."
    )
    CATALOG.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "recipe_backed_assets": len(all_selected),
                "preserved_assets": len(all_selected) - len(selected),
                "new_assets": len(selected),
                "new_fields": len(selected) * 2,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
