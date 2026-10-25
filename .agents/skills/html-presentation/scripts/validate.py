#!/usr/bin/env python3
"""Check local assets, matching scenes/notes, and thumbnail parity."""
import argparse
import html
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        for name in ['href', 'src', 'poster']:
            if attrs.get(name):
                self.refs.append(attrs[name])


def validate_site(root):
    root = Path(root).resolve()
    index = (root / 'index.html').read_text(encoding='utf-8')
    notes = (root / 'notes.html').read_text(encoding='utf-8')
    scenes = re.findall(r'<section class="scene\b.*?</section>', index, re.S)
    cards = re.findall(r'<article class="slide-note".*?</article>', notes, re.S)
    get_id = lambda text: re.search(r'\bid="([^"]+)"', text)[1]
    assert scenes and [get_id(x) for x in scenes] == [get_id(x) for x in cards], 'Slide/note identity or order mismatch'
    for scene, card in zip(scenes, cards):
        thumb = re.search(r'srcdoc="([^"]*)"', card)
        assert thumb and scene in html.unescape(thumb[1]), f'Thumbnail mismatch: {get_id(scene)}'
    for path in root.glob('*.html'):
        parser = Links()
        parser.feed(path.read_text(encoding='utf-8'))
        assert len(parser.ids) == len(set(parser.ids)), f'Duplicate HTML ID: {path.name}'
        for ref in parser.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            assert target == root or root in target.parents, f'Asset escapes output: {ref}'
            assert target.exists(), f'Missing local asset: {path.name}: {ref}'
            if url.fragment and target.suffix == '.html':
                target_parser = Links()
                target_parser.feed(target.read_text(encoding='utf-8'))
                assert unquote(url.fragment) in target_parser.ids, f'Missing anchor: {ref}'
    return len(scenes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('site', type=Path)
    args = parser.parse_args()
    print(f'PASS: {validate_site(args.site)} matching slides/notes, thumbnails and local references')
