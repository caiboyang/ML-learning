#!/usr/bin/env python3
"""Build two linked presentation pages from one trusted, locally authored deck."""
import argparse
import html
import json
import math
import re
import shutil
from pathlib import Path

from palettes import resolve_palette, theme_css

TEMPLATE = Path(__file__).resolve().parents[1] / 'assets' / 'template'


def clock(seconds):
    return f'{int(seconds) // 60:02d}:{int(seconds) % 60:02d}'


def validate(deck):
    resolve_palette(deck)
    if not re.fullmatch(r'[a-z0-9-]+', deck['id']):
        raise ValueError('deck.id must use lowercase letters, digits and hyphens')
    slides = deck['slides']
    if not slides:
        raise ValueError('A deck needs at least one slide')
    ids = [s['id'] for s in slides]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r'[a-z][a-z0-9-]*', x) for x in ids):
        raise ValueError('Slide IDs must be unique lowercase HTML identifiers')
    if 'top' in ids:
        raise ValueError('The ID top is reserved for the notes overview')
    for s in slides:
        for name in ['budget_seconds', 'media_seconds']:
            value = s.get(name)
            if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or value < 0 or value % 1):
                raise ValueError(f'{s["id"]}: {name} must be whole nonnegative seconds or null')
        if not s.get('title') or not s.get('html') or not s.get('notes'):
            raise ValueError(f'{s["id"]}: title, html and notes are required')
        if s.get('theme', 'dark') not in ['dark', 'paper']:
            raise ValueError('theme must be dark or paper')
        for note in s['notes']:
            if len(note) != 1 or next(iter(note)) not in ['say', 'cue'] or not isinstance(next(iter(note.values())), str):
                raise ValueError('Each note must contain exactly one string: say or cue')


def build(deck, output, asset_dir=None):
    validate(deck)
    output = Path(output)
    if output.resolve() == TEMPLATE.resolve():
        raise ValueError('Build into a separate output directory')
    escape = html.escape
    scenes, articles, links, timing = [], [], [], []
    elapsed = 0
    for number, slide in enumerate(deck['slides'], 1):
        ident, title = slide['id'], slide['title']
        total = len(deck['slides'])
        budget = slide.get('budget_seconds')
        theme = ' paper' if slide.get('theme') == 'paper' else ''
        scene = (f'<section class="scene{theme}" id="{ident}" data-title="{escape(title)}" '
                 f'aria-label="{number}. {escape(title)}"><div class="scene-label">{escape(slide.get("label", ""))}</div>'
                 f'<div class="scene-content">{slide["html"]}</div><div class="scene-number">{number:02d} / {total}</div></section>')
        scenes.append(scene)
        preview = '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="theme.css"></head><body>' + scene + '</body></html>'
        # Cues are escaped and excluded from speech estimates; say is plain text too.
        spoken = ''.join(f'<p class="delivery-cue" lang="zh-CN">【{escape(n["cue"])}】</p>' if 'cue' in n
                         else f'<p>{escape(n["say"])}</p>' for n in slide['notes'])
        words = len(re.findall(r"[A-Za-z]+(?:[’'-][A-Za-z]+)*", ' '.join(n['say'] for n in slide['notes'] if 'say' in n)))
        media = slide.get('media_seconds', 0) or 0
        low, high = math.ceil(words / 120 * 60 + media), math.ceil(words / 100 * 60 + media)
        timing.append({'id': ident, 'words': words, 'budget_seconds': budget, 'media_seconds': media,
                       'estimate_seconds': [low, high], 'kind': slide.get('kind', 'talk')})
        time_label = '未设预算' if budget is None else f'预算 {clock(budget)} · {clock(elapsed)}–{clock(elapsed + budget)}'
        if budget is not None:
            elapsed += budget
        time_label += f' · 英文口播+媒体估算 {clock(low)}–{clock(high)}'
        links.append(f'<li><a href="#{ident}"><span>{number:02d}</span>{escape(title)}</a></li>')
        articles.append(
            f'<article class="slide-note" id="{ident}" data-budget-seconds="{budget if budget is not None else ""}">'
            f'<div class="note-top"><p class="eyebrow">SLIDE {number:02d} / {total}</p><span class="time">{time_label}</span></div>'
            f'<div class="note-heading"><div><h2>{escape(title)}</h2><p class="purpose">{escape(slide.get("purpose", ""))}</p></div>'
            f'<figure class="slide-thumbnail"><div class="thumbnail-window"><iframe srcdoc="{escape(preview)}" title="第 {number} 屏缩略图" loading="lazy" tabindex="-1" aria-hidden="true"></iframe></div><figcaption>第 {number} 屏</figcaption></figure></div>'
            f'<div class="spoken" lang="{escape(deck.get("language", "en"))}"><span class="label">只读正文 · 黄色【提示】不读</span>{spoken}</div></article>')
    common = f'data-deck-id="{escape(deck["id"])}" data-speaker="{escape(deck["speaker"])}"'
    title = escape(deck['title'])
    index = f'<!doctype html><html lang="{escape(deck.get("language", "en"))}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="theme.css"><script src="app.js" defer></script></head><body {common}><main id="presentation">' + '\n'.join(scenes) + '</main><div class="reading-progress"><span id="progressFill"></span></div></body></html>'
    media_guide = '视频页 V 播放/暂停、R 重播。' if any(s['id'] == 'video' for s in deck['slides']) else ''
    guide = ('同一台电脑、同一个浏览器的两个窗口，系统设为扩展屏。点击“打开演示窗口”，拖到投影屏后点击“准备投影”。'
             '回到讲稿，↑ ↓ 或 Page Up / Page Down 翻页，Home / End 到首尾。T 同时开始或暂停两个计时器；换页只重置本页用时。'
             + media_guide + '深底大字区域是口播，黄色提示不读。两栏先读左栏再读右栏。'
             '时间预算不是必须讲满的时间；估算按英文 100–120 词/分钟加媒体时长，不包含临场展开和停顿，以彩排实测为准。')
    notes = (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · 讲稿</title><link rel="stylesheet" href="speaker.css"><link rel="stylesheet" href="theme.css"><script src="notes.js" defer></script></head><body {common} data-budget-label="{escape(deck.get("budget_label", "预算与估算见每页；以彩排为准"))}"><main><header id="top"><p class="eyebrow">SPEAKER GUIDE</p><h1>{title}</h1><div class="notice">{guide}</div><a href="index.html" target="_blank" rel="noopener">独立打开演示（不联动）</a></header><section class="quick"><h2>逐屏速查</h2><ol>'
             + ''.join(links) + '</ol></section>' + '\n'.join(articles) + '</main></body></html>')
    output.mkdir(parents=True, exist_ok=True)
    for name in ['style.css', 'speaker.css', 'app.js', 'notes.js']:
        shutil.copyfile(TEMPLATE / name, output / name)
    if asset_dir and Path(asset_dir).is_dir():
        shutil.copytree(asset_dir, output / 'assets', dirs_exist_ok=True)
    (output / 'theme.css').write_text(theme_css(deck), encoding='utf-8')
    (output / 'index.html').write_text(index, encoding='utf-8')
    (output / 'notes.html').write_text(notes, encoding='utf-8')
    (output / 'timing.json').write_text(json.dumps(timing, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return timing


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('deck', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    report = build(json.loads(args.deck.read_text(encoding='utf-8')), args.output, args.deck.parent / 'assets')
    talk = [x for x in report if x['kind'] != 'qa']
    print(f'Built {len(report)} slides; talk estimate excluding pauses: '
          f'{clock(sum(x["estimate_seconds"][0] for x in talk))}–{clock(sum(x["estimate_seconds"][1] for x in talk))}. Rehearse to calibrate.')
