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
    "irradiumgear",
    "triangliumgear",
    "prisilitegear",
    "quietusgear",
    "bioweaponsgear",
)

# itemName: (shortdescription, description)
TR = {
    # Irradium
    "banehammer": ("Irradium Çekiç", "Karbon ve Irradium kullanılarak dövülmüş. Oldukça tehlikeli.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "blastgun": ("Parçalayıcı", "Gerçekten tehlikeli bir pompalı tüfek türü."),
    "irradiumaxe": ("Irradium Balta", "Arıtılmış Irradium ile yapılmış bir silah.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiumblade": ("Irradium Savaş Bıçağı", "Fetih için üretildi.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiumbow": ("Irradium Yayı", "Radyoaktif avcılık için."),
    "irradiumdagger": ("Irradium Hançer", "Hızlı ve ölümcül.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiumgreataxe": ("Irradium Büyük Balta", "Bununla ikiye ayrılmak hiç eğlenceli değil.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiumkatana": ("Irradium Katana", "Radyoaktif bıçaklama keyfi. İki elle kullanılır.\n^cyan;Radyasyon Yanığına yol açar^reset;\n^yellow;5 vuruşluk kombo^reset;"),
    "irradiumlongsword": ("Irradium Uzun Kılıç", "Bilenmiş Irradium ağzı bunu oldukça... tepkili kılıyor.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiummace": ("Irradium Topuz", "Eğlenceyi artırmak için radyasyonla bezenmiş.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiumpistol": ("Irradium Tabanca", "Radyasyon hiç bu kadar sevimli ve ölümcül olmamıştı.\n^yellow;Radyasyon Yanığına yol açar^reset;"),
    "irradiumpistol2": ("Irradium Justicar", "Ölümcül radyoaktif enerji okları fırlatır."),
    "irradiumquarterstaff": ("Irradium Dövüş Asası", "Kemik kırmak için tasarlanmış radyoaktif bir asa.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiumrapier": ("Irradium Meç", "Hızlı ve tehlikeli, radyoaktif bir kılıç.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiumrifle": ("Irradium Enerji Tüfeği", "Sıyırıp geçse bile radyasyon yanığı ölümcüldür.\n^yellow;Radyasyon Yanığına yol açar^reset;"),
    "irradiumscythe": ("Irradium Tırpan", "Tarım için mi cinayet için mi, belli değil. Her iki türlü de eğlenceli.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiumshield": ("Irradium Kalkan", "^green;Bağışıklık: Aşırı Radyasyon, Yanma^reset;"),
    "irradiumshortspear": ("Irradium Kısa Mızrak", "Hafif ve acımasızca radyoaktif. Ölüm garantili.\n^cyan;Radyasyon Yanığına yol açar^reset;\n^cyan;Av silahı^reset;"),
    "irradiumshotgun": ("Irradium Seri Atış Tüfeği", "Radyoaktif mermi salvoları ateşler.\n^yellow;Radyasyon Yanığına yol açar^reset;"),
    "irradiumspear": ("Irradium Mızrak", "Zehirli Irradium radyasyonuyla güçlendirilmiş. Ne kadar düşünceli.\n^cyan;Radyasyon Yanığına yol açar^reset;\n^cyan;Av silahı^reset;"),
    "irradiumstaff": ("Irradium Asası", "Zehirli gazdan boğucu bir bulut oluşturur."),
    "irradiumsword": ("Irradium Kılıcı", "Irradium kullanılarak dövülmüş.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "irradiumwand": ("Irradium Değneği", "Yeterince Gelişmiş Teknoloji."),
    "irradiumwhip": ("Irradium Kırbaç", "Irradium kaplı bir kırbaç. Radyoaktif ve havalı.\n^cyan;Radyasyon Yanığına yol açar^reset;"),
    "isn_irradiator": ("Radyasyon Yayıcı", "Galaksiler arası silah yasalarına kesinlikle aykırı.\n^yellow;Alan etkili silah^reset;\n^green;Radyasyon Yanığına yol açar^reset;"),

    # Trianglium / Advanced Alloy
    "advalloyaxe": ("Ustanın Savaş Baltası", "Efsanevi bir Glitch şövalyesinin baltası örnek alınarak yapılmış. Densiniumu kolayca kestiği söylenir.\n^cyan;Kanamaya yol açar^reset;"),
    "advalloybroadsword": ("Ustanın Büyük Kılıcı", "Şehit düşen bir Apex isyancısının kılıcı örnek alınarak yapılmış. Masumları korumak için kalkan görevi de görür.\n^cyan;Kanamaya yol açar^reset;"),
    "advalloydagger": ("Ustanın Hançeri", "Zarif ve gölgeli. Dokununca serin.\n^cyan;Kanamaya yol açar^reset;"),
    "advalloyhammer": ("Ustanın Çekici", "Neredeyse yok edilemez bir alaşımdan yapılmış heybetli bir çekiç.\n^cyan;Kanamaya yol açar^reset;"),
    "advalloykatana": ("Ustanın Katanası", "Bu kılıçların açtığı yaraların asla iyileşmediği söylenir.\n^cyan;Kombo saldırıları hedefleri kanatır^reset;\n^yellow;8 vuruşluk kombo^reset;"),
    "advalloyrapier": ("Ustanın Meci", "Kusursuz biçimde bilenmiş."),
    "advalloyshortspear": ("Ustanın Kısa Mızrağı", "Düşmanlara hiç de kısa gelmez.\n^cyan;Av silahı^reset;"),
    "advalloyshortsword": ("Ustanın Kısa Kılıcı", "İnce işçilikli.\n^cyan;Kanamaya yol açar^reset;"),
    "advalloyspear": ("Ustanın Mızrağı", "Düşmanları delmek için ustalıkla yapılmış alaşım bir mızrak.\n^cyan;Av silahı^reset;\n^cyan;Kanamaya yol açar^reset;"),
    "coralspear": ("Mercan Mızrağı", "Tehlikeli derecede keskin mercan parçaları. Sapla gitsin!\n^cyan;Av silahı^reset;"),
    "coralstinger": ("Mercan Diken Kılıcı", "Tırtıklı ve hiç de dost canlısı değil.\n^cyan;Zehirlenmeye yol açar^reset;"),
    "coralsword": ("Mercan Büyük Kılıcı", "Son derece tehlikeli. Dokunma.\n^cyan;Zehirlenmeye yol açar^reset;"),
    "coralsword2": ("Mercan Kısa Kılıcı", "Keskin ve tırtıklı bir mercan kılıcı."),
    "crystallineblade": ("Kristal Kılıç", "Güzel, parlak ve ölümcül."),
    "curveblaster": ("Breach Tüfeği", "Gemi gövdelerini yarmak için özel tasarlanmış, eşsiz bir plazma faz silahı.\n^yellow;Hedefleri yakar^reset;"),
    "diamondshield": ("Gishinanki Kalkanı", "^green;Bağışıklık: Elektrik Şoku^reset;"),
    "energycutter": ("Breach Kesici", "Gemi gövdelerini kesmek için üretildi. Bir enerji silahıdır.\n^cyan;Kısa menzillidir. Hedefi yavaşlatır.^reset;\n^green;Alternatif atış kanama ve elektriklenmeye yol açar^reset;"),
    "fualienlaser": ("Uzaylı Lazeri", "Oldukça renkli bir uzaylı lazer silahı."),
    "fubiowand": ("Biyo-Değnek", "Organik madde sihirle buluşuyor."),
    "futriangliumpistol": ("Şovbozan", "Etkili ve ölümcül bir enerji silahı.\n^cyan;Zehirlenmeye yol açar^reset;\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "futriangliumsmg": ("Avare", "Zehirli Trianglium mermileriyle düşmanlarını ratatata diye indir.\n^cyan;Zehirlenmeye yol açar^reset;"),
    "manstopper": ("BK7 Manstopper", "Klasiklerden esinlenmiş, akıllı mühimmatla güncellenmiş.\n^cyan;Güdümlü mermiler^reset;"),
    "manstoppersmg": ("BK12 Manstopper", "Klasiklerden esinlenmiş, akıllı mühimmatla güncellenmiş.\n^cyan;Güdümlü mermiler^reset;"),
    "mineralblade": ("Parçacık Kılıcı", "Dayanıklı bir enerji kılıcı.\n^cyan;Yüksek hasarlı enerji silahı^reset;"),
    "mineralcannon": ("Parçacık Tüfeği", "Sakatlamak ve yok etmek için üretildi. Neşeli.\n^yellow;Blokları yok eder^reset;"),
    "mineralpistol": ("Parçacık Tabancası", "Büyük kuzenlerinin minik sürümü. Her zaman kullanışlı.\n^yellow;Blokları yok eder^reset;"),
    "mineralrapier": ("Parçacık Meci", "Bilimden yararlanmak bir şeyleri öldürmeyi kolaylaştırır! Yaşasın!\n^cyan;Set bonusları için Enerji sayılır^reset;"),
    "rifletriangliumfu": ("Trianglium Tüfek", "Güvenilir, isabetli ve üretimi ucuz."),
    "triangliumbroadsword": ("Trianglium Büyük Kılıç", "Üst üste dizilmiş Trianglium Piramitlerinden biçimlendirilmiş bir kılıç ağzı. Düşündüğünden daha etkili.\n^cyan;Radyoaktif, patlayan parçalar fırlatır^reset;"),
    "triangliumkatana": ("Trianglium Katana", "Hava kadar hafif, jilet kadar keskin.\n^cyan;Devasa 10 vuruşluk kombo!^reset;"),
    "triangliumlongsword": ("Trianglium Uzun Kılıç", "Tehlikeli derecede ışınlanmış. Üstelik keskin ve güzel."),
    "triwhip": ("Trianglium Kırbaç", "Trianglium parçaları yerçekimiyle bir kırbaç oluşturmuş. Sorma, kırbacı salla.\n^cyan;Radyoaktif, patlayan parçalar fırlatır^reset;"),

    # Prisilite / Prismatic
    "cutearmgun": ("Prizmatik Kol Püskürtücüsü", "Ön kola takılır. Ölümcül enerji patlamaları ateşler.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cuteaxe": ("Prizmatik Balta", "Düşmanları prizmatik güçle doğrar.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cuteboomerang": ("Prizmatik Bumerang", "Denizci Kelp'in asıl silahı bumerangdır, biliyorsun."),
    "cutebow": ("Sevimli Uzun Yay", "^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutebroadsword": ("Prizmatik Büyük Kılıç", "Sevimli büyük kılıçlar bugünlerde pek moda."),
    "cutecestus": ("Prizmatik Cestus", "Sevimli enerjiyle dolup taşıyor.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutechakram": ("Prizmatik Çakram", "^yellow;Duvarlardan seker^reset;\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutedagger": ("Prizmatik Hançer", "Renkli suikastçıların gözde silahı.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutegauntlet": ("Prizmatik Eldiven", "Sevginin sert yüzünü öğretir.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutegreataxe": ("Sevimli Büyük Balta", "Çok keskin, çok sevimli."),
    "cutehammer": ("Prizmatik Çekiç", "Düşmanlarını prizmatik enerjiyle savur.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutekatana": ("Prizmatik Katana", "Ölümcül bir kusursuzlukla bilenmiş.\n^yellow;Set bonusları için 'enerji' sayılır^reset;\n^yellow;6 vuruşluk kombo!^reset;"),
    "cutelongsword": ("Prizmatik Uzun Kılıç", "Renkli, keskin ve tek elli.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutemace": ("Prizmatik Topuz", "Kemikleri ezmeye ve renk saçmaya aç.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutemachinegun": ("Prizmatik Makineli Tüfek", "Odayı aydınlatır. Ölümle.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cuteorblauncher": ("Prizmatik Küre Fırlatıcı", "Yıkıcı enerji küreleri ateşler.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutepistol": ("Prizmatik Tabanca", "Prizma gücüyle atılan mermiler düşmanı paramparça eder.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutequarterstaff": ("Prizmatik Dövüş Asası", "İndir tepelerine.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cuterapier": ("Prizmatik Meç", "Parlak, gökkuşağı renkli bir meç.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cuterocketlauncher": ("Prizmatik Roketatar", "Rengârenk neşe patlamaları!\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutescythe": ("Prizmatik Tırpan", "Zayıfları biç.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cuteshield": ("Sevimli Kalkan", "^green;+5% Enerji Yenilenmesi, +2 Savunma, Bağışıklık: Delilik^reset;"),
    "cuteshortspear": ("Prizmatik Kısa Mızrak", "Göründüğünden çok daha tehlikeli.\n^yellow;Set bonusları için 'enerji' sayılır^reset;\n^cyan;Av silahı^reset;"),
    "cuteshortsword": ("Prizmatik Kısa Kılıç", "Bu sevimli ve keskin ağızdan güç akıyor.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cuteshotgun": ("Prizmatik Pompalı Tüfek", "Renkli patlamalar ateşler.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutesmg": ("Prizmatik Makineli Tabanca", "Enerji mermilerinle onları ölümüne kucakla!\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutesniperrifle": ("Prizmatik Tüfek", "Delip geçen tehlikeli mermiler.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "cutespear": ("Prizmatik Mızrak", "Prizmatik güçle delip geç!\n^yellow;Set bonusları için 'enerji' sayılır^reset;\n^cyan;Av silahı^reset;"),
    "cutestaff": ("Kalp Asası", "Nezaketinle öldür."),
    "cutewhip": ("Prizmatik Kırbaç", "Harika, rengârenk ve tehlikeli.\n^yellow;Set bonusları için 'enerji' sayılır^reset;"),
    "furainbowgun": ("Prizmatik Top", "Özel bir niteliğe sahip prizmatik patlamalar ateşler.\n^yellow;Alternatif atış isabet ettiğinde ek mermiler oluşturur^reset;"),
    "prismaticbow": ("Prizmatik Yay", "Kozmik enerjiyle titreşiyor."),
    "prismaticstaff": ("Kristal Parçası Asası", "Değişen renklerle parlar. ^red;Keskin^reset; ve ^yellow;Zayıflatıcıdır^reset;."),
    "prismaticwand": ("Prizmatik Değnek", "Yeterince Gelişmiş Teknoloji."),

    # Quietus
    "carnagebow": ("Kıyım Yayı", "Güdümlü oklar fırlatır."),
    "diamondblade": ("Elmas Kılıç", "Görkemle parlar ve olağanüstü değerlidir."),
    "diamondrapier": ("Elmas Meç", "Işıl ışıl bir elmas meç."),
    "futinydancer": ("Minik Dansçı", "Ufacık, sevimli cinayet araçları.\n^cyan;Enerji^reset;"),
    "goldmace": ("Altın Savaş Çekici", "Asil ve tehlikeli.\n^cyan;+10% Sersemletme^reset;"),
    "hellfiremace": ("Cehennem Ateşi Topuzu", "Öfkeyle yanıyor. Bir de ısıyla. Ve başka sıcak şeylerle. Tasarım: Gezbo."),
    "pistolquietusfu": ("Quietus Revolver", "Yüksek kalibreli mermiler ateşler.\n^yellow;Yüksek hasarlı mermiler^reset;"),
    "quietusassassin": ("Suikastçının Kılıcı", "Bir katil için Quietus kullanılarak dövülmüş bir kılıç."),
    "quietusassaultrifle": ("Quietus Taarruz Tüfeği", "Galaksiler arası silah yasalarını ihlal etmeyecek biçimde tasarlanmış, kendine özgü bir biyosilah.\n^cyan;Hedeflerin aldığı iyileştirmeyi %30 azaltır^reset; (10 sn)"),
    "quietusaxe": ("Quietus Balta", "Hızlı ve güvenilir; bu meret seni hayatta ve sapasağlam tutar."),
    "quietusboomerang": ("Quietus Bumerang", "Bu ağır bumerang nasıl düzgün çalışabiliyor?"),
    "quietusbow": ("Quietus Yayı", "Bol miktarda zehirli Quietus içerir."),
    "quietuscaptain": ("Kaptanın Kılıcı", "Bir lider için Quietus kullanılarak dövülmüş bir kılıç."),
    "quietuscrossbow": ("Quietus Arbalet", "Zehirli uçlu oklar kullanan hantal bir arbalet."),
    "quietusemperor": ("İmparator Kılıcı", "Ağır hizmet tipi bir Quietus silahı. Pekmez kadar yavaş ama acımasızca ölümcül."),
    "quietusgeneral": ("Generallerin Kılıcı", "Ciddi derecede keskin ağızlara sahip ağır hizmet tipi bir Quietus silahı."),
    "quietusgreataxe": ("Quietus Büyük Balta", "İğrenç bir biyosilah.\n^cyan;Zehirlenmeye yol açar^reset;"),
    "quietushammer": ("Quietus Çekiç", "Gerçek bir savaşçıya uygun, sağlam ve tehlikeli bir silah.\n^cyan;Zehirlenmeye yol açar^reset;"),
    "quietuskatana": ("Quietus Katana", "Rahatsız edici derecede kırmızı.\n^yellow;6 vuruşluk kombo^reset;"),
    "quietusknave": ("Serserinin Kılıcı", "İyi bir Quietus silahı."),
    "quietusknight": ("Şövalye Kılıcı", "Ağır hizmet tipi bir Quietus silahı."),
    "quietusmace": ("Quietus Topuz", "Ağır ve tehlikeli; Sersemletme şansı yüksektir."),
    "quietusmercenary": ("Paralı Askerin Kılıcı", "Bir savaşçı için Quietus kullanılarak dövülmüş bir kılıç."),
    "quietuspistol": ("Quietus Tabanca", "Galaksiler arası silah yasalarını ihlal etmeyecek biçimde tasarlanmış, kendine özgü bir biyosilah.\n^cyan;Hedeflerin aldığı iyileştirmeyi %30 azaltır^reset; (10 sn)"),
    "quietusquarterstaff": ("Quietus Dövüş Asası", "Parlak, can emen bir ölüm asası."),
    "quietusrapier": ("Kızıl İmparatoriçe", "Daha ağır bir meç türü. Her iki ağzı da fena hâlde keskin."),
    "quietusrocketlauncher": ("Quietus Roketatar", "Galaksiler arası silah yasalarını ihlal etmeyecek biçimde tasarlanmış, kendine özgü bir biyosilah.\n^cyan;Hedeflerin aldığı iyileştirmeyi %30 azaltır^reset; (10 sn)"),
    "quietusrogue": ("Haydutun Kılıcı", "İyi bir Quietus silahı."),
    "quietusscythe": ("Quellhound Tırpanı", "Parlak ve saf Quietus."),
    "quietusshield": ("Quietus Kalkan", "^green;Arı sokmalarına, çoğu radyasyon türüne ve deliliğe karşı bağışıklık sağlar.^reset;"),
    "quietusshortspear": ("Quietus Kısa Mızrak", "Düşmanları zehirlemeye hazır, keskin ve parlak bir ağız.\n^cyan;Zehirlenmeye yol açar^reset;\n^cyan;Av silahı^reset;"),
    "quietusshotgun": ("Quietus Pompalı Tüfek", "Galaksiler arası silah yasalarını ihlal etmeyecek biçimde tasarlanmış, kendine özgü bir biyosilah.\n^cyan;Hedeflerin aldığı iyileştirmeyi %30 azaltır^reset; (10 sn)"),
    "quietussmg": ("Quietus Makineli Tabanca", "Galaksiler arası silah yasalarını ihlal etmeyecek biçimde tasarlanmış, kendine özgü bir biyosilah.\n^cyan;Hedeflerin aldığı iyileştirmeyi %30 azaltır^reset; (10 sn)"),
    "quietussniper": ("Quietus Keskin Nişancı Tüfeği", "Galaksiler arası silah yasalarını ihlal etmeyecek biçimde tasarlanmış, kendine özgü bir biyosilah.\n^cyan;Hedeflerin aldığı iyileştirmeyi %30 azaltır^reset; (10 sn)"),
    "quietusspear": ("Quietus Mızrak", "Düşmanları delmek için harika.\n^cyan;Av silahı^reset;"),
    "quietusstaff": ("Quietus Asası", "Vay, ne güzel! ^red;Keskin^reset; bıçaklar fırlatır."),
    "quietuswand": ("Quietus Değneği", "Yeterince Gelişmiş Teknoloji."),
    "riflequietusfu": ("Toksin Tüfeği", "Güvenilir, isabetli ve üretimi ucuz."),

    # Biological weapons
    "atropusshield": ("Etçürüğü Kalkanı", "^green;+0.05% Can Yenilenmesi, Bağışıklık: Delilik^reset;"),
    "biogun": ("Biyo-Tüfek", "Kemikten biçimlendirilmiş biyolojik bir silah.\n^yellow;Biyo-balçık etkisi uygular^reset;\n^green;Nişan alınabilen sersemletici küreler^reset;"),
    "biopistol": ("Zehir Püskürtücü", "Zehirli bulutlar püskürtür. Eğlenceli.\n^yellow;Zehirlenmeye yol açar^reset;"),
    "corruptstaff": ("Yozlaşmış Asa", "Zehirli gazdan boğucu bir bulut oluşturur."),
    "corruptwand": ("Yozlaşmış Değnek", "Yeterince Gelişmiş Teknoloji."),
    "eyecannon": ("Ocu Topu", "Güçlü ve tuhaf bir biyolojik silah.\n^yellow;İrin etkisi uygular, blokları dönüştürür^reset;\n^green;Çoklu patlama, tuhaf fizik^reset;"),
    "fuatropusaxe": ("Et Örgüsü El Baltası", "İğrenç bir biyosilah.\n^cyan;Veba taşır^reset;"),
    "fuatropusbroadsword": ("Et Örgüsü Büyük Kılıcı", "İğrenç bir biyosilah.\n^cyan;Veba taşır^reset;"),
    "fuatropusdagger": ("Et Örgüsü Bıçağı", "İğrenç bir biyosilah.\n^cyan;Veba taşır^reset;"),
    "fuatropusgreataxe": ("Et Örgüsü Büyük Baltası", "İğrenç bir biyosilah.\n^cyan;Veba taşır^reset;"),
    "fuatropushammer": ("Et Örgüsü Çekici", "İğrenç bir biyosilah.\n^cyan;Veba taşır^reset;"),
    "fuatropusscythe": ("Et Örgüsü Tırpanı", "İğrenç ama ölümcül.\n^cyan;Veba taşır^reset;"),
    "fuatropusshortspear": ("Et Örgüsü Kısa Mızrağı", "İğrenç bir biyosilah.\n^cyan;Veba taşır^reset;\n^cyan;Av silahı^reset;"),
    "fuatropusshortsword": ("Et Örgüsü Kılıcı", "İğrenç bir biyosilah.\n^cyan;Veba taşır^reset;"),
    "fuatropusspear": ("Et Örgüsü Mızrağı", "İğrenç bir biyosilah.\n^cyan;Veba taşır^reset;\n^cyan;Av silahı^reset;"),
    "fumonsterclaw": ("Mutapençe", "Bunlar... kesilmiş canavar elleri mi? HARİKA!\n^cyan;Kanamaya yol açar^reset;"),
    "goregun": ("Kan Püskürtücü", "Kokuşmuş kan saçan iğrenç bir silah. Harika.\n^yellow;Alternatif atış kusmuk fırlatır! Eğlenceli!^reset;"),
    "lasherwhip": ("Lasher Kırbacı", "Bir Lasher bitkisinden yapılmış."),
    "magnorbatropus": ("Et Bolası", "Dehşet verici ama eğlenceli."),
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
    if len(selected) != 148:
        raise SystemExit(f"Beklenen 148 yeni combat asseti yerine {len(selected)} bulundu")

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
                    "section": "v0.24 Kademe 4 kalan savaş ekipmanı",
                }
            )

    ledger["translation_version"] = "0.24.0-beta"
    ledger["note"] = (
        "v0.24 Kademe 4 kalan savaş ekipmanı: aktif Zırh ve Silahlar araştırma "
        "ağacındaki irradiumgear, triangliumgear, prisilitegear, quietusgear ve "
        "bioweaponsgear düğümlerinin açtığı, gerçek üretim tarifi bulunan 148 savaş "
        "ekipmanında 296 görünür alan yerelleştirildi. Toplam 4324 structured + 15 Lua, "
        "1240 patch asset + 1 raw override. Oyun içi LQA bekliyor."
    )
    CATALOG.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"new_assets": len(selected), "new_fields": len(selected) * 2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
