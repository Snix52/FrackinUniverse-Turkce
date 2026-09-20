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
    "titaniumgear",
    "carbonarmorgear",
    "wastelandgear",
    "protocitegear",
    "penumbritegear",
    "zerchesiumgear",
)

# itemName: (shortdescription, description)
TR = {
    # Titanium
    "battlershield": ("Savaşçı Kalkanı", "^green;+10% Kalkan Darbesi^reset;"),
    "titaniumshield": ("Titanyum Kalkan", "^green;Asit Koruması, +5 Kalkan Darbesi İtme Gücü^reset;"),
    "titaniumboomerang": ("Titanyum Bumerang", "Bira partileri ve ölüm saçmak için harika."),
    "futitaniumchakram": ("Titanyum Çakram", "Yıkıcı enerjiyle çıtırdıyor."),
    "titaniumbroadsword": ("Titanyum Büyük Kılıç", "Büyük, ağır bir titanyum bıçak."),
    "flailtitanium": ("Titanyum Ezici", "Ağır, hantal ve muhteşem.\n^cyan;Blokları kırar^reset;"),
    "titaniumgreataxe": ("Titanyum Büyük Balta", "Son derece dayanıklı bir titanyum büyük balta."),
    "kelpsteelhatchet": ("Yosun Çekici", "Hylotl mühendisliği. Silaha dönüştürülmüş bir bitki. Tuhaf."),
    "titaniumkatana": ("Titanyum Katana", "Olağanüstü nitelikli bir kılıç.\n^yellow;4 vuruşluk kombo^reset;"),
    "titaniumlongsword": ("Titanyum Uzun Kılıç", "Hafif ama sağlam bir bıçak."),
    "ballmace": ("Çelik Gülleler", "İyi işlenmiş ama ağır. Tasarım: zimberzimber."),
    "titaniummace": ("Titanyum Topuz", "Pahalı ve acı verici!"),
    "goldquarterstaff": ("Altın Dövüş Asası", "Hantal ama hafif ve güzel."),
    "titaniumshortspear": ("Titanyum Kısa Mızrak", "Düşmanlara hiç de kısa gelmez.\n^cyan;Av silahı^reset;"),
    "fushroomsword": ("Mantar Bıçağı", "Bir şekilde silaha dönüştürülmüş mantar.\n^cyan;Floran^reset;"),
    "titaniumassaultrifle": ("Titanyum Taarruz Tüfeği", "Titanyum kasalı, tam otomatik bir tüfek."),
    "titaniumrevolver": ("Titanyum Revolver", "Ciddi darbe gücüne sahip büyük bir tabanca."),
    "titaniumshotgun": ("Titanyum Pompalı Tüfek", "Yakın mesafede ölümcül bir saçma yayılımıyla ateş eder."),
    "titaniumaxe": ("Titanyum Balta", "Bu balta hafif ama sağlamdır."),
    "titaniumhammer": ("Titanyum Çekiç", "Son derece dayanıklı bir titanyum çekiç."),
    "titaniumshortsword": ("Titanyum Kısa Kılıç", "Hafif bir titanyum kısa kılıç."),
    "fuspawngun": ("Floran Diken Fırlatıcı", "Rastgele üretilmiş silah. Zehir uçlu iğneler fırlatır."),
    "airstrike": ("Füze Salvosu", "Ölümcül bir havadan karaya füze bombardımanı çağırır."),
    "blizzardcannon": ("Tipi Topu", "Düşmanları kriyojenik roketlerle dondur!\n^cyan;Düşmanları dondurur^reset;\n^#e43774;Alan Temizleme^reset;"),
    "discrifle": ("Disk Tüfeği", "Sıra dışı zamanlar için sıra dışı bir silah.\n^yellow;Sekerek ilerleyen diskler fırlatır^reset;\n^green;Tuzak kurar^reset;"),
    "healingliquidgun": ("Şifalı Su Tabancası", "Bu tabanca şifalı su püskürtür. Hoş."),
    "funomadassaultrifle": ("Göçebe Savaş Tüfeği", "Çöl gezginlerinin gözde silahı.\n^yellow;Av silahı sayılır^reset;\n^green;Radyasyon Yanığına yol açar^reset;"),
    "funomadrifle": ("Göçebe Tüfeği", "Gezginler için son derece kullanışlı bir silah.\n^yellow;Av silahı sayılır^reset;\n^green;Radyasyon Yanığına yol açar^reset;"),
    "ionrifle": ("İyon Tüfeği", "Robotlara karşı savaşta güvenilir bir piyade silahı.\n^yellow;Elektriklenmeye yol açar^reset;\n^green;Alternatif atışla alanı kapatır^reset;"),
    "weaponminer": ("Fazer", "Güvenilir bir ışın silahı."),
    "murdermanipulator": ("Katliam Manipülatörü", "Başka amaca uyarlanmış bir manipülatör. Bu öldürüyor! Yaşasın!\n^cyan;Floran^reset;"),
    "mushroomgun": ("Mantar Tabancası", "Bu şeyden minik patlayıcı dostlar fışkırıyor.\n^yellow;Alan hasarı silahı, ^cyan;Floran^reset;^reset;"),
    "pistoltitaniumfu": ("Titanyum Magnum", "Yüksek kalibreli mermiler ateşler.\n^yellow;Yüksek hasarlı mermiler.^reset;"),
    "rifletitaniumfu": ("Titanyum Tüfek", "Güvenilir, isabetli ve üretimi ucuz."),
    "isn_flamethrower": ("Yakıcı", "Et pişirmekten daha büyük neşe var mı?\n^yellow;Yanma etkisi uygular^reset;"),
    "kineticrifle": ("Yönlendirici", "Gerçekten eşsiz bir silah!\n^yellow;Düşmanları etkisiz hâle getirir^reset;\n^green;Sıfır yerçekiminde yön değiştirir^reset;"),
    "snubber": ("Kısa Namlulu Tabanca", "Elmas uçlu mermileri 3'lü seri hâlinde ateşler.\n^cyan;Delici seri atış^reset;\n^#e43774;Av Silahı^reset;"),
    "fupoisonwand": ("Zehirli Değnek", "Düşmanlarını zehirler."),
    "teslastaff1": ("Tesla'nın Değneği", "Fırtınaların öfkesi avucunun içinde."),
    "corewhip": ("Alevli Kırbaç", "Çekirdek parçalarından yapılmış alevli bir kırbaç. Sıcacık!"),

    # Carbon
    "carbonbow": ("Karbon Av Yayı", "Karbon bir av yayı; yayla öldürülen canavarlar leziz et düşürür."),
    "carboncrossbow": ("Karbon Arbalet", "Ciddi bir darbe gücüne sahiptir."),
    "carbonstynger": ("Karbon Stynger", "Düşmanları iğne yastığına çevirmek için pompalı mekanizma."),
    "carbonaxe": ("Karbon Nacak", "Sağlamdır ve hayatta kalma uzmanları için idealdir.\n^cyan;Kanamaya yol açar^reset;"),
    "fucarbondagger": ("Karbon Bıçak", "Sağlamdır ve keskinliğini korur.\n^cyan;Kanamaya yol açar^reset;"),
    "fucarbonhammer": ("Karbon Çekiç Kazma", "Ağır ve güvenilir bir karbon çekiç."),
    "carbonkatana": ("Karbon Katana", "Ölümcül ağzı düşmanları derinden keser.\n^cyan;Kanamaya yol açar^reset;\n^yellow;6 vuruşluk kombo^reset;"),
    "carbonlongsword": ("Karbon Uzun Kılıç", "Ağır bir karbon uzun kılıç.\n^cyan;Kanamaya yol açar^reset;"),
    "carbonquarterstaff": ("Karbon Dövüş Asası", "Müthiş kaliteli. Tehlikeli."),
    "carbonshortspear": ("Karbon Kısa Mızrak", "Düşmanları delmek için yoğun metalden yapılmış bir mızrak.\n^cyan;Kanamaya yol açar^reset;\n^cyan;Av silahı^reset;"),
    "carbonblade": ("Karbon Kısa Kılıç", "İnce işçilikli.\n^cyan;Kanamaya yol açar^reset;"),
    "carbonspear": ("Karbon Mızrak", "Düşmanları delmek için yoğun metalden yapılmış bir mızrak.\n^cyan;Kanamaya yol açar^reset;\n^cyan;Av silahı^reset;"),
    "carbonshotgun": ("S-Mart Özel Yapımı", "S-Mart'ın en üst modeli.\n^cyan;Düşmanları sersemletir^reset;"),
    "carbonwhip": ("Karbon Kırbaç", "İnce dokunmuş karbon liflerinden yapılmış bir kırbaç.\n^cyan;Kanamaya yol açar^reset;"),

    # Wasteland
    "metalliccleaver": ("Hurda Satır", "Ölümcül bir silaha dönüştürülmüş hurda."),
    "metallicsword": ("Hurda Bıçak", "Hurdadan yapılmış ağır bir bıçak."),
    "metallichammer": ("Hurda Çekiç", "Sağlam. Bu hurda parçaları iyi bir silah olmuş."),
    "metallicspear": ("Hurda Mızrak", "Her tür hurdadan yapılmış.\n^cyan;Av silahı^reset;"),
    "crankgun": ("Kurmalı Top", "Keskin ve çirkin fleşetleri seri hâlinde ateşler.\n^yellow;Kanamaya yol açar^reset;"),
    "crankpistol": ("Kurmalı Tabanca", "Paslı çivi tabancası! Çok eğlenceli!\n^yellow;Kanamaya yol açar^reset;"),
    "crankrifle": ("Delici", "Delici mermileri yıkıcı yaralar açar.\n^yellow;Kanamaya yol açar^reset;"),

    # Protocite
    "protobow": ("Protocite Yayı", "Protocite ve başka yüksek kaliteli malzemelerden yapılmış."),
    "funeochakram": ("Proto Çakram", "Yıkıcı enerjiyle çıtırdıyor."),
    "coralkatana": ("Mercan Katana", "Bununla bıçaklanmak pek hoş olmasa gerek.\n^yellow;4 vuruşluk kombo^reset;"),
    "magnorbproto": ("Tauntra Küreleri", "Bu sıra dışı silah oldukça tehlikeli. ^cyan;\"Enerji\" silahı sayılır^reset;"),
    "chargepistol": ("Buzul Tabancası", "Düşmanlara dondurucu eğlence püskürtür.\n^yellow;Şarj, hasarı artırır^reset;"),
    "pistolprotofu": ("Protocite Revolver", "Yüksek kalibreli mermiler ateşler.\n^yellow;Yüksek hasarlı mermiler.^reset;\n^green;Set bonusu için \"enerji\" silahı sayılır.^reset;"),
    "protogun": ("Proto Tüfek", "Bu enerji pompalısıyla düşmanlarını neşeyle patlat.\n^yellow;Seken mermiler^reset;"),
    "protopistol": ("Proto Tabanca", "Alışılmadık olsa da kullanışlı bir tabanca.\n^yellow;Seken mermiler^reset;"),
    "protorifle": ("Proto Keskin Nişancı Tüfeği", "Seken mermi kullanan enerji tabanlı bir keskin nişancı tüfeği."),
    "protocitestaff": ("Protocite Asası", "Ham enerjiyle dolu."),
    "protocitewand": ("Protocite Değneği", "Yeterince Gelişmiş Teknoloji."),

    # Penumbrite
    "penumbriteshield": ("Penumbrite Kalkan", "^green;+12% Enerji Yenilenmesi^reset;"),
    "penumbriteboomerang": ("Penumbrite Bumerang", "Çıtırdayan, keskin bir ağız verilmiş."),
    "penumbrabow": ("Muamma Yayı", "Penumbrite ve öfkeden yapılmış."),
    "penumbritechakram": ("Penumbrite Çakram", "Hassas, güçlü ve parlak!"),
    "penumbritefist": ("Penumbrite Biçici", "Keskin, delici ağzıyla herkese eğlence sunar."),
    "penumbriteaxe": ("Penumbrite Balta", "Gölge enerjisiyle akıyor."),
    "penumbritebroadsword": ("Penumbra Büyük Kılıcı", "Her şeyi parçalara ayıracak keskin bir ağız."),
    "nightardagger": ("Nightar Bıçağı", "Kör ve neredeyse cansız ama hâlâ tehlikeli. Ölümcüllük için yükselt."),
    "penumbritedagger": ("Penumbra Hançeri", "Parlak Penumbritedan dövülmüş."),
    "flailpenumbrite": ("Penumbrite Ezici", "Ağır, hantal ve muhteşem."),
    "nightarwarblade": ("Nightar Savaş Satırı", "Nightar silahlarının açık ara en ağırı ve en değerlisi.\n^green;Büyük Balta veya Büyük Kılıç sayılır^reset;\n^cyan;Kanamaya yol açar^reset;"),
    "penumbritegreataxe": ("Penumbrite Büyük Balta", "İnanılmaz derecede şık."),
    "penumbritehammer": ("Penumbra Çekici", "Gölgeli darbeler, ölümcül eğlence."),
    "penumbritekatana": ("Penumbra Katana", "Parlak, bilenmiş ve ölümcül."),
    "penumbritelongsword": ("Penumbra Uzun Kılıcı", "Gölgeli bir amaçla keser."),
    "penumbramace": ("Penumbra Topuzu", "Güçlü ve ağır. Ciddi darbe hasarı."),
    "penumbritequarterstaff": ("Penumbra Dövüş Asası", "Ölümcül güç için gölgeyle işlenmiş metal."),
    "penumbriterapier": ("Penumbra Meç", "Gölgelerin vaadiyle hızla öldürür."),
    "penumbralscythe": ("Penumbra Tırpanı", "Karanlık bir vaatle zonkluyor."),
    "penumbriteshortspear": ("Penumbra Kısa Mızrağı", "Gölgelerin içinden sapla... hem de gölgeyle."),
    "nightarshortsword": ("Nightar Kısa Kılıcı", "Dengesi kötü ama ağzı keskin kalır. Ölümcüllük için yükselt."),
    "penumbriteshortsword": ("Penumbra Kısa Kılıcı", "Bu keskin ağız gölge gücüyle kaplı."),
    "penumbritespear": ("Penumbra Mızrağı", "Gölgeli ucu dürtmek için harikadır."),
    "siliconspear": ("Tek Kargısı", "Bu ağır mızrak, iyi zırhlanmış düşmanları bile deler.\n^cyan;Av silahı^reset;"),
    "wraithwind": ("Hayalet Örtüsü Mızrağı", "Çeşitli metallerle işlenmiş özel tasarım bir mızrak.\n^cyan;Zehirlenmeye yol açar^reset;.\n^cyan;Av silahı^reset;."),
    "magnorbpenumbrite": ("Penumbrite Magnorb", "Ayaz gibi tehlike küreleri düşmanı mahveder."),
    "biooozegun": ("Balçık Tabancası", "Zehirli balçık püskürtür. Eğlenceli!"),
    "liquidpoisongun": ("Zehir Tabancası", "Bu tabanca zehir püskürtür!"),
    "penumbriteassaultrifle": ("Penumbrite Taarruz Tüfeği", "Dengeli bir yaylım için özel işlenmiş mermiler."),
    "penumbritepistol": ("Penumbrite Revolver", "Özel bir gün için özel işlenmiş, yüksek kalibreli mermiler."),
    "penumbriterocketlauncher": ("Penumbrite Topu", "Uyumlanmış gücün hızlı patlamalarını ateşler."),
    "penumbriteshotgun": ("Penumbrite Pompalı Tüfek", "Özel işlenmiş mermiler; temizlik ekibi dâhil değildir."),
    "penumbritesmg": ("Penumbrite Makineli Tabanca", "Özel işlenmiş mermiler ve rahat bir bilek kayışı."),
    "penumbritesniperrifle": ("Penumbrite Keskin Nişancı Tüfeği", "Özel bir uğurlama için özel işlenmiş mermiler."),
    "silverslayer": ("Penumbrite Karabina", "Kullanışlı bir pakette özel işlenmiş mermiler."),
    "penumbrastaff": ("Penumbra Asası", "Penumbra Gücü."),
    "penumbrawand": ("Penumbra Değneği", "Yeterince Gelişmiş Teknoloji."),
    "penumbritewhip": ("Penumbrite Zincir Bıçağı", "Penumbritedan yapılmış bir zincir bıçak; harika bir ışıklı çubuk da olur."),

    # Zerchesium
    "gladiatorshield": ("Gladyatör Kalkanı", "^green;+4 Savunma^reset;"),
    "zerchesiumshield": ("Zerchesium Kalkan", "^green;Ateş Koruması, +7 Kalkan Darbesi İtme Gücü, 0.2 Yenilenme^reset;"),
    "zerchesiumboomerang": ("Zerchesium Bumerang", "Buz gibi soğuk, hızlı ve ölümcül."),
    "zerchesiumbow": ("Zerchesium Yayı", "Ayaz gibi bir tehditle dolu.\n^cyan;Düşmanları yavaşlatır^reset;"),
    "zerchesiumcrossbow": ("Zerchesium Arbalet", "Muhtemelen avlanmak için tasarlanmış bir arbalet."),
    "zerchesiumstynger": ("Zerchesium Stynger", "Donmuş oklarla tipi koparır."),
    "zerchesiumchakram": ("Zerchesium Çakram", "Kristalimsi yıkımın Zerchesium gücü."),
    "zerchesiumfist": ("Zerchesium Yumruk Bıçağı", "Ürpertici derecede etkili. Dondurup öldürür."),
    "zerchesiumaxe": ("Zerchesium Balta", "Neredeyse kırılmaz."),
    "hylotlgreatscion": ("Büyük Varis", "Geleneksel bir Hylotl savaş silahı.\n^cyan;Muazzam darbe gücü. Soğuk ağızlı^reset;.\n^green;Alternatif atış yavaşlatır^reset;"),
    "zerchesiumbroadsword": ("Zerchesium Büyük Kılıç", "Düşmanının düşeceğinden kesinlikle emin olarak saldır."),
    "zerchesiumdagger": ("Zerchesium Bıçak", "Jilet keskinliğindeki Zerchesium çeliğiyle sapla ve del."),
    "flailzerchesium": ("Zerchesium Ezici", "Dondurucu soğukta bir darbe çekici.\n^cyan;Blokları kırar^reset;"),
    "zerchesiumgreataxe": ("Zerchesium Büyük Balta", "Dondurucu ve tehlikeli bir ağız."),
    "zerchesiumhammer": ("Zerchesium Çekiç", "Parlak, tehlikeli ve eğlenceli!"),
    "zerchesiumkatana": ("Zerchesium Katana", "Ölümcül ağızlı, iki elli bir silah.\n^yellow;5 vuruşluk kombo^reset;"),
    "coraldullblade": ("Mercan Uzun Kılıcı", "Derinliklerden yapılmış. Bir de nefretten. Tonla nefretten.\n^cyan;Zehirlenmeye yol açar^reset;"),
    "kaicleaver": ("Kai Satırı", "Acımasız görünen bir Zerchesium satırı.\n^cyan;Uzun süreli kanamaya yol açar^reset;\n^green;Av silahı sayılır^reset;"),
    "zerchesiumlongsword": ("Zerchesium Uzun Kılıç", "Ağır ağızlı ve dondurucu soğukta.\n^cyan;Av silahı sayılır^reset;"),
    "zerchesiummace": ("Zerchesium Topuz", "İyi işlenmiş ama ağır."),
    "zerchesiumquarterstaff": ("Zerchesium Dövüş Asası", "Yoğun ve ölümcül."),
    "zerchesiumrapier": ("Zerchesium Meç", "Sağlam, ince işlenmiş ve dondurucu bir metal."),
    "zerchesiumscythe": ("Zerchesium Tırpan", "Ağır, dondurucu, metalik ölüm.\n^cyan;Donmuş Ağız^reset;"),
    "zerchesiumshortspear": ("Zerchesium Kısa Mızrak", "Soğuk ve hesapçı bir cinayet aleti.\n^cyan;Av silahı^reset;"),
    "hylotllesserscion": ("Varis Pençe Bıçağı", "Mercan ve çelik. Kan ve zafer."),
    "zerchesiumsword": ("Zerchesium Kısa Kılıç", "İnce bilenmiş Zerchesium çeliği."),
    "zerchesiumspear": ("Zerchesium Mızrak", "Harika işlenmiş bir savaş aracı.\n^cyan;Av silahı^reset;"),
    "magnorbzerchesium": ("Zerchesium Magnorb", "Ayaz gibi tehlike küreleri düşmanı mahveder."),
    "carvelle": ("Carvelle Keskin Nişancı Tüfeği", "Güçlü bir keskin nişancı tüfeği.\n^yellow;Güdümlü mermi^reset;"),
    "liquidacidgun": ("Asit Tabancası", "Bu tabanca sülfürik asit püskürtür! Eğlenceli!"),
    "fugrinder": ("Öğütücü", "Kinetik tüfek teknolojisinin zirvesi.\n^yellow;Aşırı Atış Hızı^reset;"),
    "k3rifle": ("K3 Çifte Atış", "İkinci atış düşünülerek yapılmış. Sportif.\n^yellow;Seri atış^reset;"),
    "longarm": ("Longarm Pompalı Tüfek", "Saçmaları çılgınca dağıtıp bunu yaparken harika görünmesi için özel üretilmiş bir pompalı tüfek."),
    "longarmpistol": ("Longarm Tabancası", "Tabancanın içine pompalı tüfek koymuşlar. Kesinlikle eğlenceli."),
    "minirocketlauncher": ("Mikro Roketatar", "Düşmanların kaçınmayı tercih ettiği ama kaçamadığı mini füzeler ateşler!\n^yellow;Güdümlü mermiler^reset;"),
    "napalmcannon": ("Napalm Fırlatıcı", "Bir marangozluk gösterisinde kapalı alanda ateşlenecek türden değil.\n^yellow;Yanma etkisi uygular^reset;"),
    "chargeshotgun": ("Fahrenheit 451", "Güçlü bir yangın çıkarıcı silah.\n^yellow;Yanma etkisi uygular^reset;"),
    "isn_napalmsprayer": ("Kavurucu Püskürtücü", "Devasa ve tehlikeli napalm akımları. Çocuklardan uzak tut.\n^yellow;Yanma etkisi uygular^reset;"),
    "teslagun": ("Tesla Silahı", "Keskin nişancılar için üstün bir uzun menzil seçeneği.\n^yellow;Elektriklenmeye yol açar^reset;\n^cyan;Müthiş kitle kontrolü^reset;"),
    "zerchesiumassaultrifle": ("Zerchesium Taarruz Tüfeği", "Düşmanlarını buz üstüne yatır.\n^cyan;Bombaatar^reset;"),
    "zerchesiumpistol": ("Zerchesium Tabanca", "Düşmanlarını buz üstüne yatır.\n^cyan;Düşmanları yavaşlatır^reset;"),
    "zerchesiumrocketlauncher": ("Zerchesium Roketatar", "Hızlı ateş eden bir buz roketatarı.\n^cyan;Düşmanları yavaşlatır^reset;"),
    "zerchesiumshotgun": ("Zerchesium Pompalı Tüfek", "Dondurucu misketler düşmanları kıyma eder.\n^cyan;Düşmanları yavaşlatır^reset;"),
    "zerchesiumsmg": ("Zerchesium Makineli Tabanca", "Düşmanlarını buz üstüne yatır.\n^cyan;Düşmanları yavaşlatır^reset;"),
    "zerchesiumsniper": ("Zerchesium Keskin Nişancı Tüfeği", "Düşmanlarını buz üstüne yatır.\n^green;Dron üretir^reset;\n^cyan;Düşmanları yavaşlatır^reset;"),
    "zerchesiumstaff": ("Zerchesium Asası", "Kullanışlı boyutta ayaz gibi ölüm."),
    "zerchesiumwhip": ("Zerchesium Kırbaç", "Buz gibi ucu olan bir kırbaç. Vınlayarak savrulur."),
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
    if len(selected) != 157:
        raise SystemExit(f"Beklenen 157 yeni combat asseti yerine {len(selected)} bulundu")

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
                    "section": "v0.22 Kademe 3 savaş ekipmanı",
                }
            )

    ledger["translation_version"] = "0.22.0-beta"
    ledger["note"] = (
        "v0.22 Kademe 3 savaş ekipmanı ve görev-eşya tutarlılığı: aktif Zırh ve "
        "Silahlar araştırma ağacındaki altı Kademe 3 düğümünün açtığı, gerçek üretim "
        "tarifi bulunan 158 combat asseti doğrulandı. Önceden kapsanan 1 silah korundu; "
        "157 yeni assette 314 görünür alan yerelleştirildi. Usta Manipülatör zincirinde "
        "2 asset/5 alan eşitlendi ve iki görev cümlesi düzeltildi. Toplam 3932 structured "
        "+ 15 Lua, 1044 patch asset + 1 raw override. Oyun içi LQA bekliyor."
    )
    CATALOG.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"new_assets": len(selected), "new_fields": len(selected) * 2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
