#!/usr/bin/env python3
"""Generate the public demo from the portable skill assets; --check detects drift."""
import argparse
from pathlib import Path
import shutil
import runpy

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true', help='Check without writing files')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
source = root / '.agents/skills/company-research/assets/research-dashboard'
target = root / 'company-research/demo'
files = ('styles.css', 'app.js', 'research.json', 'external-research.json', 'research.schema.json')
exporter = runpy.run_path(str(root / '.agents/skills/company-research/scripts/export-report.py'))
standalone = {name: exporter['build_html'](source / data) for name, data in
              [('index.html', 'external-research.json'), ('report.html', 'research.json'), ('external.html', 'external-research.json')]}
if args.check:
    changed = [name for name in files if not (target / name).is_file()
               or (target / name).read_bytes() != (source / name).read_bytes()]
    for name, html in standalone.items():
        if not (target / name).is_file() or (target / name).read_text(encoding='utf-8') != html:
            changed.append(name)
    if changed:
        parser.exit(1, 'Demo needs regeneration: ' + ', '.join(changed) + '\n')
    print('Demo matches source assets and the single-file export.')
else:
    target.mkdir(parents=True, exist_ok=True)
    for name in files:
        shutil.copyfile(source / name, target / name)
    for name, html in standalone.items():
        (target / name).write_text(html, encoding='utf-8')
    print('Generated company-research/demo from skill assets.')
