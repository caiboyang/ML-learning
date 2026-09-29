#!/usr/bin/env python3
"""Offline bundle integrity tests; these do not replace a file:// browser check."""
import json
from html.parser import HTMLParser
from pathlib import Path
import runpy
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / '.agents/skills/company-research'
BUILD = runpy.run_path(str(SKILL / 'scripts/export-report.py'))['build_html']
DATA = SKILL / 'assets/research-dashboard/research.json'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.scripts = []
        self.resources = []
        self.in_data = False
        self.data = ''
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script':
            self.scripts.append(attrs)
            self.in_data = attrs.get('id') == 'research-data'
        if tag in ('img', 'iframe') or attrs.get('src') or (tag == 'link' and attrs.get('rel') == 'stylesheet'):
            self.resources.append((tag, attrs))

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_data = False

    def handle_data(self, text):
        if self.in_data:
            self.data += text


class ExportTests(unittest.TestCase):
    def test_bundle_is_self_contained_and_preserves_data(self):
        for source in [DATA, DATA.with_name('external-research.json')]:
            with self.subTest(source=source.name):
                page = Page(BUILD(source))
                self.assertEqual(page.resources, [])
                self.assertEqual(len(page.scripts), 2)
                self.assertEqual(json.loads(page.data), json.loads(source.read_text()))

    def test_supplied_text_cannot_escape_data_or_title(self):
        data = json.loads(DATA.read_text())
        payload = '</script><img src=x onerror=alert(1)><script>/* 中文 */'
        data['meta']['title'] = '</title>' + payload
        data['records'][0]['text'] = payload
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'input.json'
            source.write_text(json.dumps(data, ensure_ascii=False))
            page = Page(BUILD(source))
        self.assertEqual(page.resources, [])
        self.assertEqual(len(page.scripts), 2)
        self.assertEqual(json.loads(page.data), data)


if __name__ == '__main__':
    unittest.main()
