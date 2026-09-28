#!/usr/bin/env python3
"""Generate the public demo from the portable skill assets; --check detects drift."""
import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true', help='Check without writing files')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
source = root / '.agents/skills/company-research/assets/research-dashboard'
target = root / 'company-research/demo'
files = ('index.html', 'styles.css', 'app.js', 'research.json', 'research.schema.json')
if args.check:
    changed = [name for name in files if not (target / name).is_file()
               or (target / name).read_bytes() != (source / name).read_bytes()]
    if changed:
        parser.exit(1, 'Demo needs regeneration: ' + ', '.join(changed) + '\n')
    print('Demo matches all five source files.')
else:
    target.mkdir(parents=True, exist_ok=True)
    for name in files:
        shutil.copyfile(source / name, target / name)
    print('Generated company-research/demo from skill assets.')
