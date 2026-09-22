#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import audit_remaining as audit

ASSET = "interface/cockpit/cockpit.config"
SECTION = "v0.33 cockpit ve navigasyon arayüzü"
EXPECTED_FIELDS = 281
EXPECTED_ASSETS = 1
EXPECTED_UNIQUE = 262
TRANSLATIONS = json.loads(r'''{"EDIT BOOKMARK":"YER İŞARETİNİ DÜZENLE","NEW BOOKMARK":"YENİ YER İŞARETİ","UNEXPLORED":"KEŞFEDİLMEDİ","VIEW":"GÖRÜNTÜLE","No orbiting bodies":"Yörüngede gökcismi yok","%s orbiting bodies":"Yörüngedeki gökcismi: %s","One orbiting body":"Yörüngede bir gökcismi","NAVIGATION OFFLINE":"NAVİGASYON ÇEVRİMDIŞI","SHIP DRIVE NOT INSTALLED":"FTL MOTORU KURULU DEĞİL","Unable to use FTL capabilities, please install a proper FTL drive":"FTL özellikleri kullanılamıyor. Uygun bir FTL Motoru kur.","ONLY USABLE ON YOUR OWN SHIP":"YALNIZCA KENDİ GEMİNDE KULLANILABİLİR","GO":"GİT","X":"X","Y":"Y","Cancel":"İptal","Enter bookmark name":"Yer işareti adı gir","Accept":"Kabul Et","Delete":"Sil","Jump":"Sıçra","Confirm FTL":"FTL'Yİ ONAYLA","Geological Analysis":"Jeolojik Analiz","Threat: ":"Tehdit: ","Weather":"Hava Durumu","UNMAPPED CELESTIAL OBJECTS UNAVAILABLE":"HARİTALANMAMIŞ GÖKCİSİMLERİ KULLANILAMAZ","REMOTE SYSTEM VIEW":"UZAK SİSTEM GÖRÜNÜMÜ","SHIP IN TRANSIT":"GEMİ SEYİR HÂLİNDE","^#b9b5b2; Select your destination":"^#b9b5b2; Hedefini seç"," Navigation Console":" Navigasyon Konsolu","FTL travel requires ^red;%i fuel^reset;.\n Not enough fuel to proceed.":"FTL yolculuğu için ^red;%i yakıt^reset; gerekiyor.\n Devam etmek için yeterli yakıt yok.","FTL travel will consume ^green;%i fuel^reset;.\nConfirm to proceed.":"FTL yolculuğu ^green;%i yakıt^reset; tüketecek.\nDevam etmek için onayla.","ADD BOOKMARK":"YER İŞARETİ EKLE","CANNOT BOOKMARK":"YER İŞARETİ EKLENEMEZ","REQUIRES MECH TO DEPLOY":"İNİŞ İÇİN MECH GEREKLİ","VISITED":"ZİYARET EDİLDİ","^reset;Threat: ^reset;":"^reset;Tehdit: ^reset;","View quest location":"Görev konumunu göster","View ship":"Gemiyi göster","Bookmarks":"Yer İşaretleri","Coordinates":"Koordinatlar","Aegisalt":"Aegisalt","Cinnabar":"Zinober","Narcotium":"Narkotium","Copper":"Bakır","Lasombrium":"Lasombrium","Crystal":"Kristal","Densinium":"Densinium","Durasteel":"Durasteel","Effigium":"Effigium","Crystal Erchius Fuel":"Kristal Erchius Yakıtı","Ferozium":"Ferozium","Plasmic Crystal":"Plazmik Kristal","Gold":"Altın","Iron":"Demir","Irradium":"Irradium","Isogen":"Isogen","Spare Parts":"Yedek Parçalar","Koanite":"Koanite","Lunari":"Lunari","Telebrium":"Telebrium","Neptunium":"Neptünyum","Nocxium":"Nocxium","Penumbrite":"Penumbrite","Plutonium":"Plütonyum","Prism Shard":"Prizma Parçası","Protocite":"Protocite","Pyreite":"Pyreite","Quietus":"Quietus","Silver":"Gümüş","Solarium":"Solarium","Thorium":"Toryum","Titanium":"Titanyum","Trianglium":"Trianglium","Tungsten":"Tungsten","Uranium":"Uranyum","Violium":"Violium","Xithricite":"Xithricite","Zerchesium":"Zerchesium","Acid Rain":"Asit Yağmuru","Ashfall":"Kül Yağışı","Ash Storm":"Kül Fırtınası","Bio Rain":"Biyo Yağmur","Blood Rain":"Kan Yağmuru","Cosmic Blasts":"Kozmik Patlamalar","Crystal Rain":"Kristal Yağmuru","Crystal Storm":"Kristal Fırtınası","Severe Crystal Storm":"Şiddetli Kristal Fırtınası","Dark Matter Blasts":"Karanlık Madde Patlamaları","Drizzle":"Çiseleme","Dust Storms":"Toz Fırtınaları","Cinder Showers":"Köz Sağanağı","Fire Storm":"Ateş Fırtınası","Fog":"Sis","Freeze Storm":"Dondurucu Fırtına","Lesser Freeze Storm":"Hafif Dondurucu Fırtına","Minor Freeze Storm":"Zayıf Dondurucu Fırtına","Smog":"Smog","Bubble Rain":"Baloncuk Yağmuru","Infested":"İstila Altında","Earthquakes":"Depremler","Minor Earthquakes":"Hafif Depremler","Severe Earthquakes":"Şiddetli Depremler","Heatwaves":"Sıcak Hava Dalgaları","Severe Heatwaves":"Şiddetli Sıcak Hava Dalgaları","Intense Heatwaves":"Aşırı Sıcak Hava Dalgaları","Rainy Lightning Storm":"Yağmurlu Yıldırım Fırtınası","Severe Rainy Lightning Storm":"Şiddetli Yağmurlu Yıldırım Fırtınası","Lightning Storm":"Yıldırım Fırtınası","Severe Lightning Storm":"Şiddetli Yıldırım Fırtınası","Butterfly Migration":"Kelebek Göçü","Sparklejoy":"Sparklejoy","Sudden Chill":"Ani Soğuk","Severe Chill":"Şiddetli Soğuk","Intense Chill":"Aşırı Soğuk","Dense Gas":"Yoğun Gaz","Super Dense Gas":"Aşırı Yoğun Gaz","Impossibly Dense Gas":"İmkânsız Derecede Yoğun Gaz","Luminous Rain":"Işıltılı Yağmur","Anti-Gravity Rain":"Anti-Yerçekimi Yağmuru","Light Anti-Gravity Rain":"Hafif Anti-Yerçekimi Yağmuru","Mist":"Pus","Hail":"Dolu","Healing Rain":"Şifalı Yağmur","Torrential Rain":"Sağanak Yağmur","Hurricane":"Kasırga","Electric Storm":"Elektrik Fırtınası","Ice Storms":"Buz Fırtınaları","Molten Iron Storm":"Erimiş Demir Fırtınası","Large Meteorites":"Büyük Meteorlar","Light Ashfall":"Hafif Kül Yağışı","Magma Storm":"Magma Fırtınası","Severe Magma Storm":"Şiddetli Magma Fırtınası","Small Meteorites":"Küçük Meteorlar","Misty Rain":"Puslu Yağmur","High-Mass Event":"Yüksek Kütle Olayı","Gravity Rain":"Yerçekimi Yağmuru","Light Gravity Rain":"Hafif Yerçekimi Yağmuru","Poison Gas":"Zehirli Gaz","Dense Poison Gas":"Yoğun Zehirli Gaz","Severe Poison Gas":"Ağır Zehirli Gaz","Organic Rain":"Organik Yağmur","Rain":"Yağmur","Sandstorms":"Kum Fırtınaları","Slime Storm":"Balçık Fırtınası","Weak Slime Storm":"Zayıf Balçık Fırtınası","Snow":"Kar","Blizzards":"Tipiler","Stardust":"Yıldız Tozu","Orbital Debris":"Yörünge Enkazı","Static Charge":"Statik Yük","Storms":"Fırtınalar","Sulphuric Rain":"Kükürtlü Yağmur","Sulphuric Fog":"Kükürtlü Sis","Sulphuric Storm":"Kükürtlü Fırtına","Slight Sulphuric Storm":"Hafif Kükürtlü Fırtına","Major Sulphuric Storm":"Şiddetli Kükürtlü Fırtına","Tar Rain":"Katran Yağmuru","Thunderstorms":"Gök Gürültülü Fırtınalar","Severe Thunder":"Şiddetli Gök Gürültüsü","Rolling Thunder":"Sürekli Gök Gürültüsü","Windstorms":"Rüzgâr Fırtınaları","Aether World":"Aether Gezegeni","Alien":"Yabancı","Gateway":"Geçit","Primeval Forest":"Kadim Orman","Volcanic Primeval":"Volkanik Kadim Dünya","Dark Primeval":"Karanlık Kadim Dünya","Arctic":"Kutup","Dark Arctic":"Karanlık Kutup","Asteroids":"Asteroitler","Atropus":"Atropus","Nightmare Atropus":"Kâbus Atropus","Barren":"Çorak","Bloodstone":"Kan Taşı","Atropus Sea":"Atropus Denizi","Bog":"Bataklık","Chromatic":"Kromatik","Crystalline":"Kristalli","Desert":"Çöl","Red Desert":"Kızıl Çöl","Dark Red Desert":"Karanlık Kızıl Çöl","Eden":"Eden","Unknown":"Bilinmiyor","Forest":"Orman","Frozen Volcanic":"Donmuş Volkanik","Gas Giant":"Gaz Devi","Fungal":"Mantar","Lush":"Yemyeşil","Frozen Moon":"Donmuş Ay","Ice Waste":"Buz Çorağı","Dark Ice Waste":"Karanlık Buz Çorağı","Infernus":"Infernus","Dark Infernus":"Karanlık Infernus","Irradiated":"Radyasyonlu","Jungle":"Tropik Orman","Lightless":"Işıksız","Lava":"Lav","Dark Magma":"Karanlık Magma","Cyber Sphere":"Siberküre","Midnight":"Gece Yarısı","Lunar":"Ay","Desert Moon":"Çöl Ayı","Metallic Moon":"Metalik Ay","Shadow Moon":"Gölge Ayı","Rocky Moon":"Kayalık Ay","Toxic Moon":"Zehirli Ay","Volcanic Moon":"Volkanik Ay","Mountainous":"Dağlık","Nitrogen Sea":"Azot Denizi","Oceanic":"Okyanus","Penumbra":"Penumbra","Proto World":"Proto Gezegen","Shadow Proto World":"Gölge Proto Gezegen","Savannah":"Savan","Scorched":"Kavrulmuş","Shadow":"Gölge","Gelatinous":"Jelatinimsi","Snowy":"Karlı","Dark Snow":"Karanlık Karlı Dünya","Strange Sea":"Tuhaf Deniz","Sulphuric":"Kükürtlü","Dark Sulphur":"Karanlık Kükürt","Sulphuric Sea":"Kükürtlü Deniz","Super Dense":"Aşırı Yoğun","Tabula Rasa":"Tabula Rasa","Tar Ball":"Katran Gezegeni","Rainforest":"Yağmur Ormanı","Tidewater":"Gelgit Suları","Toxic":"Zehirli","Tundra":"Tundra","Dark Tundra":"Karanlık Tundra","Wasteland":"Çorak Dünya","Volcanic":"Volkanik","Binary Star":"Çift Yıldız","Black Star":"Kara Yıldız","Frozen Star":"Donmuş Yıldız","Blue Star":"Mavi Yıldız","Mysterious Star":"Gizemli Yıldız","Dying Star":"Ölmekte Olan Yıldız","Temperate Star":"Ilıman Yıldız","Fiery Star":"Alevli Yıldız","Red Star":"Kızıl Yıldız","Gentle Star":"Sakin Yıldız","Radioactive Star":"Radyoaktif Yıldız","None":"Yok","Moderate":"Orta","Risky":"Riskli","Dangerous":"Tehlikeli","Extreme":"Aşırı","Lethal":"Ölümcül","Harmless (I)":"Zararsız (I)","Low (II)":"Düşük (II)","Moderate (III)":"Orta (III)","Risky (IV)":"Riskli (IV)","Dangerous (V)":"Tehlikeli (V)","Extreme (VI)":"Aşırı (VI)","Lethal (VII)":"Ölümcül (VII)","Impossible (VIII)":"İmkânsız (VIII)","Immeasurable (IX)":"Ölçülemez (IX)","Just No (X)":"Yok Artık (X)","A giant ball of gases intermingling with one another. There is simply nothing here to land on.":"Birbirine karışan gazlardan oluşan dev bir küre. Burada üzerine inilebilecek hiçbir yüzey yok.","A gas giant. There is no solid substance to this planet, just a collection of swirling gases.":"Bir gaz devi. Katı bir yüzeyi yok; yalnızca girdap gibi dönen gazlardan oluşuyor.","Can't land. The crushing pressure and tearing winds of this gas giant would kill you instantly.":"İniş yapılamaz. Bu gaz devinin ezici basıncı ve yırtıcı rüzgârları seni anında öldürür."}''')


def remaining_rows(source: Path):
    translated, _ = audit.load_translations(Path(__file__).with_name("ceviriler.json"))
    path = source / ASSET
    raw = path.read_text(encoding="utf-8-sig")
    data = audit.parse_jsonc(raw)
    rows = []
    for row in audit.candidates_from_data(ASSET, data):
        key = (row.asset, row.pointer)
        if row.confidence != "confirmed" or key in translated:
            continue
        if row.pointer.startswith("/visitableTypeDescription/"):
            continue
        rows.append(row)
    return sorted(rows, key=lambda r: r.pointer)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    args = ap.parse_args()
    rows = remaining_rows(args.source)
    if len(rows) != EXPECTED_FIELDS:
        raise ValueError(f"v0.33 alan sayısı değişti: {len(rows)} != {EXPECTED_FIELDS}")
    assets = {r.asset for r in rows}
    sources = {r.value for r in rows}
    if len(assets) != EXPECTED_ASSETS:
        raise ValueError(f"v0.33 asset sayısı değişti: {len(assets)} != {EXPECTED_ASSETS}")
    if len(sources) != EXPECTED_UNIQUE:
        raise ValueError(f"v0.33 kaynak metin sayısı değişti: {len(sources)} != {EXPECTED_UNIQUE}")

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
    unexplained_unused = [source for source in unused if source not in existing_by_source]
    if missing or unexplained_unused:
        raise ValueError(
            f"v0.33 çeviri haritası uyuşmuyor; missing={missing!r} "
            f"unexplained_unused={unexplained_unused!r}"
        )

    manifest = {
        "schema_version": 1,
        "translation_version": "0.33.0-beta",
        "scope": "Cockpit ana navigasyon arayüzü: yer işaretleri, cevher/hava göstergeleri, gezegen-yıldız türleri, tehdit etiketleri ve FTL kontrolleri; visitableTypeDescription açıklama bloğu sonraki pakete bırakıldı.",
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
    manifest_path = Path(__file__).with_name("v033_translations.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    index = {(r["asset"], r["pointer"]): r for r in catalog["translations"]}
    for row in manifest["translations"]:
        key = (row["asset"], row["pointer"])
        if key in index:
            raise ValueError(f"v0.33 alanı zaten katalogda: {key}")
        catalog["translations"].append(row)
        index[key] = row
    catalog["translation_version"] = manifest["translation_version"]
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"v0.33: {len(rows)} alan / {len(assets)} asset / {len(sources)} benzersiz metin")
    print(f"katalog: {len(catalog['translations'])} structured alan")


if __name__ == "__main__":
    main()
