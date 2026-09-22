from pathlib import Path
import json,sys
from collections import Counter
ROOT=Path(__file__).resolve().parents[2];TOOLS=ROOT/'tools';sys.path.insert(0,str(TOOLS))
from qa_raw import lua_parts,CONTROL

def replace(path,old,new,count=1):
 p=ROOT/path;s=p.read_text();assert s.count(old)==count,(path,s.count(old),old[:50]);p.write_text(s.replace(old,new))
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
replace('tools/qa_integrity.py','from rule_data import TOOLS, render_terminology','from rule_data import TOOLS, render_terminology\nfrom qa_raw import CONTROL, validate_raw, validate_manifest_pin')
replace('tools/qa_integrity.py',"    glyphs = policy.get('ui_glyphs', [])", "    if Counter(CONTROL.findall(en)) != Counter(CONTROL.findall(tr)):\n        if not any(bound_exception(row, x) for x in policy.get('control_exceptions', [])):\n            raise ValueError('Control token mismatch: ' + where)\n    glyphs = policy.get('ui_glyphs', [])")
replace('tools/qa_integrity.py',"            if not source_pattern.search(en) or canonical in tr.casefold():\n                continue\n            for variant, pattern in banned:\n                if pattern.search(tr):", "            if not source_pattern.search(en):\n                continue\n            # A canonical phrase may contain a shorter forbidden word. Only\n            # that overlapping occurrence is safe, never a separate occurrence.\n            canonical_spans = [m.span() for m in re.finditer(\n                r'(?<!\\w)' + re.escape(canonical) + r'(?!\\w)', tr, re.I)]\n            for variant, pattern in banned:\n                if any(not any(a <= m.start() and m.end() <= b\n                               for a, b in canonical_spans)\n                       for m in pattern.finditer(tr)):")
start="    validate_translation_memory(all_rows, tm_policy)\n    raw_rows = []\n"
s=(TOOLS/'qa_integrity.py').read_text();pos=s.index(start);end=s.index("    doc = tools.parent",pos)
s=s[:pos]+'''    raw_manifest = json.loads((tools / 'raw_text_translations.json').read_text(encoding='utf-8'))
    validate_manifest_pin(raw_manifest, tools)
    raw_rows = validate_raw(raw_manifest, format_policy, validate_format)
    for row in raw_rows:
        terminology.validate(row)
    validate_translation_memory(all_rows + raw_rows, tm_policy)
'''+s[end:];(TOOLS/'qa_integrity.py').write_text(s)
# Catalog and manifests: only localized strings/QA metadata; source fields stay exact.
cpath=TOOLS/'ceviriler.json';catalog=json.loads(cpath.read_text());rows=catalog['translations']
old_rows={(r['asset'],r['pointer']):dict(r) for r in rows}
for r in rows:
 if r['asset']=='interface/scripted/statWindow/statWindow.config' and '[Tile]' in r['en']:
  r['tr']=r['tr'].replace('[Tile]','[Zemin]')
  r['qa']={'allow_control_fix':True,'reason':'[Tile] görünür zemin etiketidir; Lua status kimliğini ayrı kullanır. Yalnız bu asset/pointer/en/tr eşleşmesi izinlidir.'}
 if r['asset']=='quests/story/gaterepair.questtemplate' and r['pointer']=='/completionText':
  r['tr']=r['tr'].replace('mekaniklerimizden birine','teknisyenlerimizden birine')
 if r['asset']=='quests/story/shiprepair.questtemplate':
  if r['pointer']=='/text':r['tr']=r['tr'].replace('bir şeylerden söyleniyor','bir şeylerden yakınıyor')
  if r['pointer']=='/scriptConfig/descriptions/repairShip':r['tr']='^orange;Erchius Kristali sevkiyatını^green; geri al^reset;.'
 # Existing source has no separating space; target need not inherit this typo.
 if r['asset']=='quests/outpost/shipupgrade/illegalshipupgrade3.questtemplate' and r['pointer']=='/text':
  r['tr']=r['tr'].replace('yasal.^green;', 'yasal. ^green;')
changed={(r['asset'],r['pointer']):r for r in rows if r!=old_rows[(r['asset'],r['pointer'])]}
# Minimal replacement of serialized affected rows, not reformatting the full catalog.
s=cpath.read_text()
for key,r in changed.items():
 old=json.dumps(old_rows[key],ensure_ascii=False,indent=2);new=json.dumps(r,ensure_ascii=False,indent=2)
 old='\n'.join('    '+l for l in old.splitlines());new='\n'.join('    '+l for l in new.splitlines())
 assert s.count(old)==1,(key,old);s=s.replace(old,new)
cpath.write_text(s)
for fn in ['v039_translations.json','v045_translations.json']:
 p=TOOLS/fn;d=json.loads(p.read_text());s=p.read_text()
 for old in d['translations']:
  key=(old['asset'],old['pointer'])
  if key not in changed:continue
  new=dict(old,tr=changed[key]['tr'])
  if '[Tile]' in old['en']:new['qa']=changed[key]['qa']
  a='\n'.join('    '+l for l in json.dumps(old,ensure_ascii=False,indent=2).splitlines());b='\n'.join('    '+l for l in json.dumps(new,ensure_ascii=False,indent=2).splitlines());assert s.count(a)==1;s=s.replace(a,b)
 p.write_text(s)
# Exact-bound exceptions: keep legacy visible decorations, never general bypass flags.
p=TOOLS/'rules/text_integrity.json';d=json.loads(p.read_text());d['control_exceptions']=[]
for r in rows:
 if Counter(CONTROL.findall(r['en']))!=Counter(CONTROL.findall(r['tr'])):
  reason=r.get('qa',{}).get('reason') or r.get('qa',{}).get('control_note') or 'Mevcut görünür açıklama/dekorasyon çevirisi; teknik placeholder değildir. Tam satıra bağlı istisna.'
  d['control_exceptions'].append({**{k:r[k] for k in ('asset','pointer','en','tr')},'reason':reason})
write(p,d)
# Explicit string slots for all existing source-locked replacements.
p=TOOLS/'raw_text_translations.json';d=json.loads(p.read_text())
for sp in d['assets']:
 for r in sp['replacements']:
  oc,ol=lua_parts(r['old']);nc,nl=lua_parts(r['new']);assert oc==nc and len(ol)==len(nl)
  r['text_literals']=[i for i,(a,b) in enumerate(zip(ol,nl)) if a!=b]
write(p,d)
replace('tools/tests/test_v039.py','test_tile_marker_control_code_is_preserved','test_visible_tile_labels_are_localized')
replace('tools/tests/test_v039.py','all("[Tile]" in r["tr"]','all("[Zemin]" in r["tr"]')
replace('tools/tests/test_v039.py','all("[Zemin]" not in r["tr"]','all("[Tile]" not in r["tr"]')
replace('tools/build_validate.py','from qa_integrity import validate_project','from qa_integrity import validate_project\nfrom qa_raw import verify_source_blob, validate_manifest_pin')
replace('tools/build_validate.py',"        for spec in raw_manifest.get('assets',[]):", "        validate_manifest_pin(raw_manifest, Path(__file__).parent)\n        for spec in raw_manifest.get('assets',[]):")
replace('tools/build_validate.py',"                content=source.read_text(encoding='utf-8-sig')", "                verify_source_blob(spec, source)\n                content=source.read_text(encoding='utf-8-sig')")
replace('tools/build_validate.py',"        for spec in runtime_manifest.get('assets',[]):", "        validate_manifest_pin(runtime_manifest, Path(__file__).parent)\n        for spec in runtime_manifest.get('assets',[]):")
replace('tools/build_validate.py',"                content=raw_assets.get(a, source.read_text(encoding='utf-8-sig'))", "                verify_source_blob(spec, source)\n                content=raw_assets.get(a, source.read_text(encoding='utf-8-sig'))")

assert len(changed)==9
# Add the two audited fuel warnings.
p=TOOLS/'raw_text_translations.json';d=json.loads(p.read_text())
pairs=[('The tank is full.','Depo dolu.'),('The tank has a different type of fuel, empty it first.','Depoda farklı türde yakıt var; önce depoyu boşalt.')]
replacements=[]
for en,tr in pairs:
 replacements.append({'old':f'widget.setText("lblEfficiency", "^red;{en}^white;")','display_en':en,'display_tr':tr,'expected_count':1,'new':f'widget.setText("lblEfficiency", "^red;{tr}^white;")','text_literals':[1]})
d['assets'].append({'asset':'interface/mechfuel/mechfuel.lua','source_blob_sha':'77d8f0b616e9c70e8b59ca9d2a991be3d8d4876f','replacements':replacements})
write(p,d)
# Bind the existing Research action context without changing a LOCKED term.
from qa_raw import replacement_rows,verify_source_blob
raw=[r for sp in d['assets'] for i,rp in enumerate(sp['replacements']) for r in replacement_rows(sp['asset'],i,rp)]
r=next(r for r in raw if r['en']=='Research')
p=TOOLS/'locked_terms.json';term=json.loads(p.read_text())
term['context_exceptions'].append(dict(r,reason='researchTree.lua researchButton runtime eylemi: Research -> Araştır. İsim bağlamından ayrıdır.'));write(p,term)
p=TOOLS/'translation_memory_exceptions.json';tm=json.loads(p.read_text())
for x in tm['exceptions']:
 if x['en']=='Research':x['variants'].append({k:r[k] for k in ('asset','pointer','tr')})
write(p,tm)
# Missing offline templates are reconstructed only from the verified FU source.
source=Path(sys.argv[1])
for name in ['interface/kheAA/kheAA_router/kheAA_routerGui.lua','interface/scripted/statWindow/statWindow.lua','interface/mechfuel/mechfuel.lua']:
 spec=next(sp for sp in d['assets'] if sp['asset']==name)
 verify_source_blob(spec,source/name)
 text=(source/name).read_text(encoding='utf-8-sig')
 for rp in spec['replacements']:
  assert text.count(rp['old'])==rp['expected_count'];text=text.replace(rp['old'],rp['new'])
 out=TOOLS/'raw_overrides'/name;assert not out.exists();out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text)
replace('tools/build_validate.py','    args.output.mkdir(parents=True)', "    if args.source_dir:\n        for asset, content in raw_assets.items():\n            template = Path(__file__).parent / 'raw_overrides' / asset\n            if not template.is_file() or template.read_text(encoding='utf-8-sig') != content:\n                raise ValueError('Raw template/pinned build drift: ' + asset)\n\n    args.output.mkdir(parents=True)")
replace('tools/ceviriler.json','"translation_version": "0.45.0-beta"','"translation_version": "0.45.1-beta"')
from pathlib import Path
R=ROOT
p=R/'README.md';s=p.read_text().replace('v0.45.0','v0.45.1').replace('**55** görünür','**57** görünür').replace('**8.079**','**8.081**').replace('**6** raw','**7** raw').replace('**2.282**','**2.283**')
a=s.index('Son doğrulanmış paket SHA-256:');b=s.index('## Neler Türkçe?',a)
s=s[:a]+'Paketin güncel SHA-256 değeri, kaynak commit kimliği, workflow run numarası ve doğrulama durumu yalnız [dist/build-evidence.json](dist/build-evidence.json) içinde tutulur. Bu bilgiler README’ye kopyalanmaz. Kaynak değişikliği ile paket yayını arasında, yayımlanmış son build için bu dosyadaki sürüm esas alınır.\n\n'+s[b:]
s=s.replace('## Sıradaki çalışma','## v0.45.1 bakım paketi\n\nLua görünür string güvenliği, LOCKED karma-varyant kontrolü, alan-bağlı kontrol kodu istisnaları, beş zemin etiketi, iki Mech yakıt uyarısı ve görev dili düzeltildi. PR QA salt okunur; generated çıktı değişiklikleri kaynak güncellemesi yerine kabul edilmez. Ayrıntılar: [bakım raporu](docs/QA_HARDENING_20260922.md).\n\n## Sıradaki çalışma')
p.write_text(s)
p=R/'FU_SESSION_CHECKPOINT.md';s=p.read_text();a=s.index('## Durum');b=s.index('Pinned FU:',a)
s=s[:a]+'''## Güncel çalışma
22 Eylül 2026: **v0.45.1 bakım paketi**, 22 Eylül ana kontrol bulgularının düzeltilmesi.
Kaynak sürüm: `tools/ceviriler.json`. Yayımlanmış son paketin gerçek sürümü, kaynak commit'i, CI run'ı, SHA-256 ve PASS durumu için tek referans: [`dist/build-evidence.json`](dist/build-evidence.json).
Bu checkpoint bir build kanıtı kopyası değildir; aşağıdaki v0.42-v0.45 sonuçları tarihsel kayıtlardır.

'''+s[b:]
s+='''
## v0.45.1 bakım checkpoint'i
- Hedef: F01-F08 ana kontrol bulguları; v0.46 yeni içerik kapsamına başlanmadı.
- Raw metinlerde gerçek Lua stringleri ayrıştırılır. Yalnız `text_literals` ile belirtilen stringler değişebilir; callback, widget adı, teknik string, kod ve yorum değişikliği reddedilir.
- Raw yer tutucuları, renkler, sayılar, kaçışlar, kontrol kodları ve görünür metinler ortak terminoloji/çeviri belleğiyle kontrol edilir.
- Research düğmesi için yalnız gerçek Lua eylem alanına bağlı bağlam istisnası eklendi. 506 LOCKED terimin karşılıkları değiştirilmedi.
- Beş `[Tile]` görünür etiketi `[Zemin]` yapıldı. Mevcut 10 dekorasyon istisnası ve bu beş etiket asset/pointer/en/tr/gerekçeye bağlandı; genel allow_control_fix artık tek başına geçiş sağlamaz.
- Mech yakıtının dolu/uyumsuz depo uyarıları çevrildi. Bu paneldeki diğer dinamik metinler ayrı kapsamdır; tam panel kapanışı iddia edilmez.
- Üç görev ifadesi ve bir görevde cümle arası boşluk düzeltildi. 8.024 mevcut alan korunur; yalnız 9 structured hedef metin değişti. 2 raw metin eklendi: 57 kullanım yeri / 7 raw asset.
- Eksik KheAA Router ve statWindow çevrimdışı kaynak şablonları tamamlandı. Pinned build ile bütün raw şablonların eşleşmesi zorunlu.
- Testler: 152 Python test yöntemi; bunların içinde 14 yazı animasyonu ve 8 Mech yakıt davranış senaryosu gerçek Lua 5.4 ile yürütülür. Bütün raw Lua dosyaları syntax kontrolünden geçer.
- Değişen ana kaynaklar: qa_integrity.py, qa_raw.py, build_validate.py, raw manifest/şablonları, v039/v045 manifestleri, katalog, text_integrity politikası, dar bağlam kayıtları, testler, PR/main workflowları ve dokümantasyon.
- Generated çıktı elle değiştirilmez. Güncel paket ve pinned-source sonuçları için üstteki build-evidence bağlantısı esas alınır.
- Açık dış ayar: `main` için zorunlu PR/status rule yapılandırması bu bağlantının yazma araçlarıyla değiştirilemedi. CI işleri eklendi; GitHub sunucusunda zorunlu merge kuralı yapılandırıldığı iddia edilmez. Yayın botunun generated commit akışı korunarak ayrıca ele alınmalıdır.
- Oyun içi LQA: **NOT TESTED**. Tricorder zemin etiketleri, Mech yakıt uyarıları, SAIL harfleri ve düzeltilen görev ekranları odaklı kontrol bekler.
- Sonraki başlangıç: bu bakım paketinin build-evidence sürümünü kontrol et; ardından mevcut v0.46 Irklar ve SAIL/AI planından devam et. Ana kontrolü yeniden başlatma.
'''
p.write_text(s)
p=R/'docs/QA_PIPELINE.md';s=p.read_text().replace('Generated commit `[skip ci]` kullanır ve çıktı yolları build trigger\'ında dışlanır.', 'Generated commit `[skip ci]` kullanır. İnsan eliyle generated-only değişikliklerin sessizce atlanmaması için main build trigger\'ında paths-ignore kullanılmaz. `check_generated_changes.py`, incoming diff içindeki generated değişikliğini çıktı ağacı yenilenmeden önce reddeder.')
s+='''
## v0.45.1 ek güvenlik sözleşmesi
`tools/qa_raw.py` Lua parçalarını çalıştırmadan string ve kod parçalarına ayırır. Raw manifestte her replacement için `text_literals` sıfır tabanlı görünür string indeksleridir. Diğer stringler ve bütün string-dışı kod/yorumlar exact kalır. `display_en/display_tr` açıklama metadata'sıdır; gerçek QA bu alanlara güvenmek yerine ayrıştırılan gerçek Lua stringleri üzerinde çalışır. Raw format düzeltmesi için genel bypass yoktur.

Gerçek raw stringler, `/replacements/<index>/literals/<slot>` bağlamıyla LOCKED ve ortak TM kontrolüne girer. Research eylemi yalnız tek gerçek widget bağlamında tanımlıdır. Doğru kanonik terim, aynı cümledeki ayrı yasaklı varyantı maskelemez; kanonik ifadenin içinde kalan kısa yasaklı alt-sözcük yanlış pozitif sayılmaz.

Kontrol-token farklılıkları `text_integrity.json/control_exceptions` içinde tam satıra bağlıdır. Kaynak/hedef/asset/pointer değişince istisna geçersizdir. `[Fire]`, `<item>` ve `[(pause)...]` korunur; görünür `[Tile]` etiketi yalnız beş belgeli stat adı için çevrilir.

Raw manifest pinleri merkezi FU piniyle karşılaştırılır. Full-source build, raw/runtime kaynak blob SHA'larını gerçek dosya baytlarıyla karşılaştırır; bütün raw şablonlar pinned build ile aynı metni üretmelidir.

`pr-qa.yml` tüm PR değişikliklerinde salt okunur çalışır; paket yayımlamaz, ref güncellemez ve credential saklamaz. PR'lar kaynak değişiklikleri taşır; `FU_Turkce/`, `dist/` ve generated raporlara doğrudan değişiklik kabul edilmez. Main build aynı kuralı çıktı yenilemeden önce uygular. Botun mevcut source-SHA yarış koruması korunur.

Test ortamı: Python 3.11 ve işletim sistemi Lua 5.4 kitaplığı. Ubuntu: `sudo apt-get install liblua5.4-0`. Lua kitaplığı yoksa davranış testleri atlanmaz, hata verir. Full-source build sonrasında `FU_TEST_MOD_DIR=build_output/FU_Turkce python -m unittest discover -s tools/tests -p 'test_lua_behavior.py' -v` komutu yeni üretilen Lua'yı da test eder. Bunlar Starbound API stub'larıyla yapılan testlerdir; gerçek oyun içi LQA değildir.

GitHub branch protection/required checks ayrı sunucu ayarıdır. Workflow eklemek tek başına zorunlu merge engeli oluşturmaz. Bu ayar, mevcut generated yayın botunun erişimi dikkate alınarak uygulanmalıdır.
''';p.write_text(s)
p=R/'docs/DECISIONS.md';p.write_text(p.read_text()+'''
## 2026-09-22: v0.45.1 ana kontrol bakım kararı
- Beş stat adındaki `[Tile]` teknik token değil görünür zemin etiketi: `[Zemin]`. Teknik status anahtarları değiştirilmedi. İstisnalar tam alan ve iki dildeki metne bağlıdır.
- Mech yakıtında iki uyarı: “Depo dolu.” ve “Depoda farklı türde yakıt var; önce depoyu boşalt.”; fuel callback'leri ve sayısal işlemler değişmez.
- `mechanics` görev bağlamında “teknisyenlerimiz”; “bir şeylerden yakınıyor”; görev hedefi “Erchius Kristali sevkiyatını geri al.”. Illegal ship upgrade 3 metnindeki nokta sonrası boşluk düzeltildi.
- LOCKED karşılıklar değişmedi. Raw Research düğmesi mevcut Araştır eylem bağlamına dar biçimde bağlandı.
- Geriye dönük QA tüm ana katalog ve sürüm manifestleriyle yürütülür; dilin tamamına insan LQA onayı verildiği anlamına gelmez.
''')
p=R/'docs/LQA_CHECKLIST.md';p.write_text(p.read_text()+'''
## v0.45.1 hedefli oyun içi kontrol (NOT TESTED)
- Tricorder: Cangıl, Çamur, Buz, Sulu Kar ve Kar `[Zemin]` etiketlerini aç; satır taşması ve stat gösterimini kontrol et.
- Mech yakıtı: dolu depoyu doldurmayı dene; başka yakıt türünü eklemeyi dene. Türkçe uyarı ve tüketim olmamasını kontrol et. Sonra uyumlu yakıtla normal doldurmayı dene.
- SAIL ve istasyon: Türkçe karakterleri yazı animasyonunda, atlamada ve renkli metinlerde kontrol et.
- Gate/ship repair görevleri: düzeltilen Türkçe ifadeleri ve renk sınırlarını kontrol et.
''')

replace('README.md','**Güncel sürüm:** v0.45.1 Beta  \n','**Güncel sürüm:** v0.45.1 Beta\n')

# The delivered source must equal the locally tested source byte-for-byte.
import hashlib
expected=json.loads(Path(__file__).with_name('expected.json').read_text())
for name,digest in expected.items():
 actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
 if actual!=digest:raise ValueError('Unexpected migration output: '+name+' '+actual)
print('Exact source migration: PASS; '+str(len(expected))+' source files verified')
