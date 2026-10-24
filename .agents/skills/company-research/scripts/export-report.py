#!/usr/bin/env python3
"""Bundle the dashboard and research JSON into one offline, renameable HTML file."""
import argparse
import html
import json
from pathlib import Path


def build_html(data_path):
    assets = Path(__file__).resolve().parents[1] / 'assets/research-dashboard'
    data = json.loads(Path(data_path).read_text(encoding='utf-8'))
    # Escape '<' even inside JSON strings so supplied text cannot close the data script.
    embedded = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    page = (assets / 'index.html').read_text(encoding='utf-8')
    page = page.replace('<title>公司研究工作台 · 模板</title>',
                        f'<title>{html.escape(data["meta"]["title"])}</title>')
    page = page.replace('<link rel="stylesheet" href="styles.css">',
                        '<style>\n' + (assets / 'styles.css').read_text(encoding='utf-8') + '</style>')
    page = page.replace('  <script src="app.js" defer></script>\n', '')
    scripts = '<script type="application/json" id="research-data">' + embedded + '</script>\n'
    scripts += '<script>\n' + (assets / 'app.js').read_text(encoding='utf-8') + '</script>\n'
    return page.replace('</body>', scripts + '</body>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('data', type=Path, help='Research JSON; validate schema and references first')
    parser.add_argument('output', type=Path, help='Output .html file')
    args = parser.parse_args()
    if args.output.suffix.lower() != '.html':
        parser.error('Output must end in .html')
    page = build_html(args.data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(page, encoding='utf-8')
    print(f'Exported {args.output} (self-contained; no deployment)')


if __name__ == '__main__':
    main()
