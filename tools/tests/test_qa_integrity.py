import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_validate as build
import qa_integrity as qa
from rule_data import TOOLS, render_terminology


def row(en, tr, asset='fixture.item', pointer='/description'):
    return dict(asset=asset, pointer=pointer, en=en, tr=tr)


class IntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = json.loads((TOOLS / 'ceviriler.json').read_text(encoding='utf-8'))['translations']
        cls.policy = json.loads((TOOLS / 'rules/text_integrity.json').read_text(encoding='utf-8'))
        cls.terms = json.loads((TOOLS / 'locked_terms.json').read_text(encoding='utf-8'))
        cls.tm = json.loads((TOOLS / 'translation_memory_exceptions.json').read_text(encoding='utf-8'))

    def test_current_corpus_and_versioned_manifests(self):
        result = qa.validate_project(self.rows)
        self.assertEqual(result['catalog_units_checked'], len(qa.manifest_rows(self.rows)))
        self.assertEqual(result['locked_terms'], sum(t['status'] == 'LOCKED' for t in self.terms['terms']))

    def test_signed_numbers_pass(self):
        for en, tr in [('+25%', '+25%'), ('-7', '-7'), ('+10', '+10'), ('-10', '-10'),
                       ('+1.5%', '+%1,5'), ('+^green;25^reset;%', '+%^green;25^reset;')]:
            with self.subTest(en=en, tr=tr):
                qa.validate_format(row(en, tr), self.policy)
                self.assertEqual(build.signed_nums(en), build.signed_nums(tr))

    def test_signed_numbers_fail(self):
        for en, tr in [('+25%', '-25%'), ('-7', '7'), ('+10', '-10'), ('-10', '+10'), ('+25', '25')]:
            with self.subTest(en=en, tr=tr), self.assertRaises(ValueError):
                qa.validate_format(row(en, tr), self.policy)

    def test_tabs_preserved_actual_and_escaped(self):
        for en, tr in [('a\tb', 'c\td'), (r'a\tb', r'c\td'), ('a\t\tb', 'c\t\td')]:
            qa.validate_format(row(en, tr), self.policy)
        parsed = json.loads('{"en":"a\\tb","tr":"c\\td"}')
        qa.validate_format(row(**parsed), self.policy)

    def test_tab_loss_and_structure_fail(self):
        for en, tr in [('a\tb', 'ab'), (r'a\tb', 'ab'), ('a\tb\tc', 'a\t\tbc'), ('a\tb', r'a\tb')]:
            with self.subTest(en=en, tr=tr), self.assertRaises(ValueError):
                qa.validate_format(row(en, tr), self.policy)

    def test_exact_tab_exceptions_and_no_blanket_bypass(self):
        self.assertEqual(len(self.policy['tab_exceptions']), 2)
        for exception in self.policy['tab_exceptions']:
            qa.validate_format(exception, self.policy)
            changed = dict(exception, tr=exception['tr'] + ' changed')
            with self.assertRaises(ValueError):
                qa.validate_format(changed, self.policy)
        with self.assertRaises(ValueError):
            qa.validate_format(dict(row('a\tb', 'ab'), qa={'allow_tab_fix': True}), self.policy)

    def test_icons_from_real_corpus(self):
        original = next(r for r in self.rows if '\ue024' in r['en'])
        qa.validate_format(original, self.policy)
        for bad in [original['tr'].replace('\ue024', ''), original['tr'].replace('\ue024', '\ue025'),
                    original['tr'] + '\ue024']:
            with self.assertRaises(ValueError):
                qa.validate_format(dict(original, tr=bad), self.policy)
        self.assertEqual(qa.icon_signature('Türkçe ğĞıİşŞöÖüÜçÇ'), {})

    def test_translation_memory_drift_fails(self):
        with self.assertRaises(ValueError):
            qa.validate_translation_memory([row('same', 'aynı'), row('same', 'başka', 'other.item')], {})

    def test_translation_memory_explicit_context_passes(self):
        qa.validate_translation_memory(self.rows, self.tm)
        modified = copy.deepcopy(self.rows)
        next(r for r in modified if r['en'] == 'Research')['tr'] = 'Yanlış üçüncü çeviri'
        with self.assertRaises(ValueError):
            qa.validate_translation_memory(modified, self.tm)

    def test_manifest_drift_cannot_return(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'v999_translations.json').write_text(json.dumps({'x': {'asset': 'fixture.item', 'name': 'Yanlış'}}))
            with self.assertRaises(ValueError):
                qa.manifest_rows([row('Name', 'Ad', pointer='/shortdescription')], root)

    def test_all_locked_canonical_forms(self):
        engine = qa.Terminology(self.terms)
        self.assertGreaterEqual(len(engine.exact), 507)
        for en, forms in engine.exact.items():
            if len(forms) != 1:
                continue
            with self.subTest(en=en):
                engine.validate(row(en, next(iter(forms))))

    def test_locked_wrong_variant_exact_and_in_sentence(self):
        engine = qa.Terminology(self.terms)
        for en, tr in [('Arc Smelter', 'Ark Eritici'), ('Build an Arc Smelter.', 'Bir Ark Eritici üret.'), ('Jungle', 'Cangıl'), ('Jungle', 'Cangil')]:
            with self.subTest(en=en), self.assertRaises(ValueError):
                engine.validate(row(en, tr))
        engine.validate(row('Build an Arc Smelter.', 'Bir Ark Ergitici üret.'))
        engine.validate(row('Jungle', 'Tropik Orman'))

    def test_precursor_locked_inside_names_and_sentences(self):
        engine = qa.Terminology(self.terms)
        engine.validate(row('Precursor Warbot', 'Precursor Savaş Botu'))
        engine.validate(row('Find the Precursor relic.', "Precursor'ın kalıntısını bul."))
        for en, tr in [
            ('Precursor Warbot', 'Öncül Savaş Botu'),
            ('Precursor Warbot', 'Savaş Botu'),
            ('Find the Precursor relic.', 'Öncül kalıntısını bul.'),
        ]:
            with self.subTest(en=en, tr=tr), self.assertRaisesRegex(ValueError, 'LOCKED'):
                engine.validate(row(en, tr))
        engine.validate(row('A forerunner', 'Bir öncül'))

    def test_food_terms_stay_locked_with_turkish_suffixes(self):
        engine = qa.Terminology(self.terms)
        for en, tr in [
            ('A dish with bacon.', 'Pastırmalı bir yemek.'),
            ('Jam made from pussplum.', 'İrin eriğinden yapılmış reçel.'),
            ('Cooked pearlpeas.', 'Pişmiş inci bezelyeleri.'),
        ]:
            with self.subTest(en=en):
                engine.validate(row(en, tr))
                with self.assertRaisesRegex(ValueError, 'LOCKED'):
                    engine.validate(row(en, 'Yanlış karşılık.'))

    def test_repeated_proper_names_are_locked_in_text(self):
        engine = qa.Terminology(self.terms)
        for en, tr in [
            ('Cthulhu Statue', 'Cthulhu Heykeli'),
            ('Erchius Converter', 'Erchius Dönüştürücü'),
            ('Charged Lunari', 'Yüklü Lunari'),
        ]:
            with self.subTest(en=en):
                engine.validate(row(en, tr))
                with self.assertRaisesRegex(ValueError, 'LOCKED'):
                    engine.validate(row(en, 'Yanlış karşılık'))

    def test_terminology_context_and_exception_binding(self):
        engine = qa.Terminology(self.terms)
        for exception in self.terms['context_exceptions']:
            engine.validate(exception)
            with self.assertRaises(ValueError):
                engine.validate(dict(exception, tr='Tamamen yanlış'))

    def test_terminology_generated_document_matches(self):
        self.assertEqual((TOOLS.parent / 'docs/TERMINOLOGY.md').read_text(encoding='utf-8'), render_terminology(self.terms))

    def test_core_cli_rejects_placeholder_and_format_mutations(self):
        from collections import Counter
        from unittest.mock import patch
        counts = Counter(r['en'] for r in self.rows)
        base = next(r for r in self.rows if counts[r['en']] == 1 and not r.get('qa')
                    and r['section'] != 'v0.30 Aktif araştırma ekipmanı kapanışı'
                    and r['pointer'] == '/description')
        for suffix in (' %s', ' {qa_probe}', ' $qa_probe', ' ^red;', '\n', ' 99999'):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as directory:
                catalog = json.loads((TOOLS / 'ceviriler.json').read_text(encoding='utf-8'))
                target = next(r for r in catalog['translations'] if r['asset'] == base['asset'] and r['pointer'] == base['pointer'])
                target['tr'] += suffix
                path = Path(directory) / 'catalog.json'
                path.write_text(json.dumps(catalog, ensure_ascii=False), encoding='utf-8')
                with patch.object(sys, 'argv', ['build_validate.py', '--catalog', str(path), '--output', str(Path(directory) / 'output')]):
                    with self.assertRaises(ValueError):
                        build.main()

    def test_empty_translation_fails(self):
        with self.assertRaises(ValueError):
            qa.validate_format(row('A sentence', '   '), self.policy)

    def test_source_mismatch_all_6016_fields(self):
        for r in self.rows:
            fixture = {}; build.seed(fixture, r['pointer'], r['en'])
            patch = [{'op': 'test', 'path': r['pointer'], 'value': r['en']},
                     {'op': 'replace', 'path': r['pointer'], 'value': r['tr']}]
            self.assertEqual(build.read_at(build.simulate(fixture, patch), r['pointer']), r['tr'])
            build.replace_at(fixture, r['pointer'], r['en'] + '__SOURCE_DRIFT__')
            with self.assertRaises(ValueError):
                build.simulate(fixture, patch)

    def test_technical_fields_and_dead_research_rejected(self):
        for r in self.rows:
            self.assertTrue(build.allowed(r['asset'], r['pointer']))
            self.assertFalse(build.allowed(r['asset'], '/price'))
            self.assertFalse(build.allowed(r['asset'], '/scripts/0'))
        for asset, nodes in build.NONVISIBLE_RESEARCH_IDS.items():
            for node in nodes:
                self.assertTrue(build.nonvisible_research_pointer(asset, '/strings/research/' + node + '/0'))

    def test_existing_placeholder_color_number_and_newline_contracts(self):
        for r in self.rows:
            en, tr = r['en'], r['tr']
            for pattern in (build.PRINTF, build.BRACE_PLACEHOLDER, build.DOLLAR_PLACEHOLDER):
                self.assertEqual(qa.Counter(pattern.findall(en)), qa.Counter(pattern.findall(tr)))
            self.assertEqual(en.count('\n'), tr.count('\n'))
            if not r.get('qa', {}).get('allow_number_fix'):
                self.assertEqual(build.nums(en), build.nums(tr))
        self.assertNotEqual(build.PRINTF.findall('%s'), build.PRINTF.findall('%d'))
        self.assertNotEqual(build.BRACE_PLACEHOLDER.findall('{item}'), build.BRACE_PLACEHOLDER.findall('{other}'))
        self.assertNotEqual(build.DOLLAR_PLACEHOLDER.findall('$item'), build.DOLLAR_PLACEHOLDER.findall('$other'))
        self.assertNotEqual(build.COLOR.findall('^red;'), build.COLOR.findall('^green;'))


if __name__ == '__main__':
    unittest.main()
