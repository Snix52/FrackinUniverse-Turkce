"""Negative controls for the 2026-09-22 audit; no known-bad mutation may pass."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qa_integrity as qa
import qa_raw as raw
from rule_data import TOOLS, render_terminology


def replacement(en='Science Outpost', tr='Bilim Karakolu'):
    return dict(old='widget.setText("label", ' + json.dumps(en) + ')',
                new='widget.setText("label", ' + json.dumps(tr, ensure_ascii=False) + ')',
                text_literals=[1], expected_count=1,
                display_en=en, display_tr=tr)


def manifest(*replacements):
    return dict(source_repository='fixture/repo', source_commit='a'*40,
                assets=[dict(asset='test.lua', source_blob_sha='b'*40,
                             replacements=list(replacements))])


def row(en, tr):
    return dict(asset='test.item', pointer='/description', en=en, tr=tr)


class RawHardeningTests(unittest.TestCase):
    def check(self, rep):
        return raw.validate_raw(manifest(rep), {}, qa.validate_format)

    def test_valid_translation_and_literal_slot(self):
        rows = self.check(replacement())
        self.assertEqual(rows[0]['tr'], 'Bilim Karakolu')
        self.assertEqual(rows[0]['pointer'], '/replacements/0/literals/1')

    def test_code_and_technical_string_mutations_fail(self):
        rep = replacement()
        bads = [rep['new'].replace('widget.setText', 'widget.wrongFunction'),
                rep['new'].replace('"label"', '"otherLabel"'),
                rep['new']+'; player.consumeCurrency("money", 100)',
                rep['new']+' -- changed code comment']
        for bad in bads:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.check(dict(rep, new=bad))

    def test_placeholder_color_number_and_escape_mutations_fail(self):
        pairs = [('%s', ''), ('%s', '%d'), ('%s %d', '%d'), ('%s %d', '%d %s'), ('{item}', '{other}'),
                 ('$item', '$other'), ('<fuelName>', '<other>'), ('[Fire]', '[Ateş]'),
                 ('[(pause)2]', '[(pause)3]'), ('^red;Text^reset;', 'Metin'),
                 ('100', '200'), ('+10%', '-10%'), ('a\nb', 'ab'), ('a\tb', 'ab')]
        for en, tr in pairs:
            with self.subTest(en=en, tr=tr), self.assertRaises(ValueError):
                self.check(replacement('Value: '+en, 'Değer: '+tr))

    def test_valid_tokens_and_turkish_inflections_pass(self):
        self.check(replacement('Get %s at ^red;100^reset; {item} $n <fuelName> [Fire]\n',
                               '%s al: ^red;100^reset; {item} $n <fuelName> [Fire]\n'))

    def test_slot_declarations_and_counts_fail_closed(self):
        for slots in [None, [], [0], [0, 1], [1, 1], [True], [-1], [99]]:
            with self.subTest(slots=slots), self.assertRaises(ValueError):
                self.check(dict(replacement(), text_literals=slots))
        for count in [0, -1, True, '1', 1.5]:
            with self.subTest(count=count), self.assertRaises(ValueError):
                self.check(dict(replacement(), expected_count=count))

    def test_informational_display_fields_cannot_hide_actual_errors(self):
        rep=replacement('Count %s', 'Sayı %s')
        rep['new']=rep['new'].replace('%s','')
        with self.assertRaises(ValueError): self.check(rep)

    def test_lexer_quotes_comments_long_strings_and_incomplete_calls(self):
        code, strings=raw.lua_parts('canvas:drawText("a\\n\\\"b",')
        self.assertEqual(strings, ['a\n"b'])
        self.assertEqual(code,['canvas:drawText(', ','])
        self.assertEqual(raw.lua_parts('x=[=[\nTürkçe]=] -- "not a string"')[1],['Türkçe'])
        self.assertEqual(raw.lua_parts('--[=[ "not a string" ]=]\nx="İ"')[1],['İ'])
        for broken in ['x="unterminated', 'x=[=[abc', 'x="\\q"', 'x="\\999"']:
            with self.subTest(broken=broken), self.assertRaises(ValueError): raw.lua_parts(broken)

    def test_duplicate_assets_replacements_and_missing_hash_fail(self):
        m=manifest(replacement());m['assets']*=2
        with self.assertRaises(ValueError):raw.validate_raw(m,{},qa.validate_format)
        with self.assertRaises(ValueError):raw.validate_raw(manifest(replacement(),replacement()),{},qa.validate_format)
        m=manifest(replacement());m['assets'][0]['source_blob_sha']=''
        with self.assertRaises(ValueError):raw.validate_raw(m,{},qa.validate_format)

    def test_source_blob_is_checked_against_bytes(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'test.lua';p.write_bytes(b'hello\r\n')
            digest=hashlib.sha1(b'blob 7\0hello\r\n').hexdigest()
            spec=dict(asset='test.lua',source_blob_sha=digest)
            raw.verify_source_blob(spec,p)
            p.write_bytes(b'hello\n')
            with self.assertRaises(ValueError):raw.verify_source_blob(spec,p)

    def test_source_manifest_pin_is_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            t=Path(directory);(t/'kaynaklar.json').write_text(json.dumps(dict(repository='fixture/repo',commit='a'*40)))
            raw.validate_manifest_pin(manifest(),t)
            with self.assertRaises(ValueError):raw.validate_manifest_pin(dict(manifest(),source_commit='c'*40),t)

    def test_project_checks_raw_terms_and_cross_surface_memory(self):
        terms=json.loads((TOOLS/'locked_terms.json').read_text())
        # Real terms, empty TM policy; only the fixture corpus is replaced.
        with tempfile.TemporaryDirectory() as directory:
            t=Path(directory)/'tools';t.mkdir();(t/'rules').mkdir();(t.parent/'docs').mkdir()
            (t/'locked_terms.json').write_text(json.dumps(terms))
            (t.parent/'docs/TERMINOLOGY.md').write_text(render_terminology(terms))
            (t/'rules/text_integrity.json').write_text('{}')
            (t/'translation_memory_exceptions.json').write_text('{}')
            (t/'kaynaklar.json').write_text(json.dumps(dict(repository='fixture/repo',commit='a'*40)))
            p=t/'raw_text_translations.json'
            p.write_text(json.dumps(manifest(replacement('Science Outpost','Science Outpost!'))))
            with self.assertRaisesRegex(ValueError,'LOCKED'):qa.validate_project([],t)
            p.write_text(json.dumps(manifest(replacement('Neutral source','Birinci çeviri'))))
            with self.assertRaisesRegex(ValueError,'memory drift'):
                qa.validate_project([row('Neutral source','İkinci çeviri')],t)


class LockedAndControlTests(unittest.TestCase):
    def setUp(self):
        self.policy=json.loads((TOOLS/'rules/text_integrity.json').read_text())
        self.terms=json.loads((TOOLS/'locked_terms.json').read_text())
        self.engine=qa.Terminology(self.terms)

    def test_canonical_does_not_hide_separate_forbidden_variant(self):
        with self.assertRaisesRegex(ValueError,'forbidden variant'):
            self.engine.validate(row('Visit the Science Outpost.', 'Bilim Karakolu / Science Outpost noktasına git.'))

    def test_canonical_and_inflected_phrase_pass(self):
        self.engine.validate(row('Visit the Science Outpost.', "Bilim Karakolu'na git."))
        self.engine.validate(row('Build an Arc Smelter.', 'Bir Ark Ergitici üret.'))

    def test_canonical_subphrase_overlap_is_not_blanket_bypass(self):
        term=dict(source='Test Object',tr='Uzun Kılıç',forbidden='Kılıç',status='LOCKED')
        engine=qa.Terminology({'terms':[term]})
        engine.validate(row('Test Object', 'Uzun Kılıç'))
        with self.assertRaises(ValueError):engine.validate(row('Use Test Object', 'Uzun Kılıç veya Kılıç kullan.'))

    def test_tile_exceptions_are_exactly_bound(self):
        exceptions=[x for x in self.policy['control_exceptions'] if '[Tile]' in x['en']]
        self.assertEqual(len(exceptions),5)
        for e in exceptions:
            qa.validate_format(e,self.policy)
            for key,value in [('asset','other.config'),('pointer','/other'),('tr',e['tr']+' [Ateş]')]:
                with self.subTest(key=key),self.assertRaises(ValueError):qa.validate_format(dict(e,**{key:value}),self.policy)

    def test_blanket_control_fix_cannot_drop_runtime_token(self):
        for en,tr in [('[Fire]','[Ateş]'),('[(pause)3]',''),('<item>','<eşya>')]:
            with self.subTest(en=en),self.assertRaises(ValueError):
                qa.validate_format(dict(row(en,tr+' metin'),qa={'allow_control_fix':True}),self.policy)

    def test_existing_control_exceptions_still_pass(self):
        for e in self.policy['control_exceptions']:qa.validate_format(e,self.policy)

    def test_raw_research_action_is_explicit_not_general(self):
        exceptions=[x for x in self.terms['context_exceptions'] if x['asset'].endswith('/researchTree.lua')]
        self.assertEqual(len(exceptions),1)
        self.engine.validate(exceptions[0])
        with self.assertRaises(ValueError):self.engine.validate(dict(exceptions[0],tr='İncele'))

class GeneratedGuardTests(unittest.TestCase):
    def test_source_edits_pass(self):
        from check_generated_changes import validate_paths
        validate_paths(['tools/ceviriler.json','tools/raw_overrides/test.lua','docs/DECISIONS.md'])

    def test_generated_only_and_mixed_edits_fail(self):
        from check_generated_changes import validate_paths
        for path in ['FU_Turkce/a.patch','dist/package.zip','dist/build-evidence.json',
                     'tools/test_raporu.json','tools/GELISTIRME.txt']:
            for paths in [[path], ['tools/ceviriler.json',path]]:
                with self.subTest(paths=paths),self.assertRaises(ValueError):validate_paths(paths)

    def test_pr_workflow_is_read_only_and_has_no_path_bypass(self):
        source=(TOOLS.parent/'.github/workflows/pr-qa.yml').read_text()
        self.assertIn('pull_request:',source)
        self.assertIn('contents: read',source)
        self.assertIn('persist-credentials: false',source)
        self.assertIn('check_generated_changes.py',source)
        for forbidden in ['contents: write','pull_request_target','paths-ignore:','git push','publish_generated.py']:
            self.assertNotIn(forbidden,source)

    def test_main_guard_precedes_output_refresh(self):
        source=(TOOLS.parent/'.github/workflows/build-package.yml').read_text()
        self.assertNotIn('paths-ignore:',source)
        self.assertLess(source.index('check_generated_changes.py'),source.index('rm -rf FU_Turkce'))
        self.assertIn('liblua5.4-0',source)
        self.assertIn('FU_TEST_MOD_DIR: build_output/FU_Turkce',source)

if __name__=='__main__':unittest.main()
