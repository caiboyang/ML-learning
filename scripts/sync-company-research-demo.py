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
files = ('index.html', 'styles.css', 'app.js', 'research.json', 'research.schema.json')
exporter = runpy.run_path(str(root / '.agents/skills/company-research/scripts/export-report.py'))
standalone = exporter['build_html'](source / 'research.json')
if args.check:
    changed = [name for name in files if not (target / name).is_file()
               or (target / name).read_bytes() != (source / name).read_bytes()]
    if not (target / 'report.html').is_file() or (target / 'report.html').read_text(encoding='utf-8') != standalone:
        changed.append('report.html')
    if changed:
        parser.exit(1, 'Demo needs regeneration: ' + ', '.join(changed) + '\n')
    print('Demo matches source assets and the single-file export.')
else:
    target.mkdir(parents=True, exist_ok=True)
    for name in files:
        shutil.copyfile(source / name, target / name)
    (target / 'report.html').write_text(standalone, encoding='utf-8')
    print('Generated company-research/demo from skill assets.')
