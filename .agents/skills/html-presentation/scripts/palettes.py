"""Small author-selected palettes, semantic color roles, and text contrast checks."""
import re

PRESETS = {
    'forest': dict(zip(
        ['dark_surface', 'dark_text', 'dark_muted', 'dark_accent', 'light_surface',
         'light_text', 'light_muted', 'light_accent', 'highlight'],
        ['#101e19', '#f0ecdf', '#becbc0', '#c5edca', '#f0ecdf',
         '#173c2c', '#4b6555', '#376f48', '#f0a684'])),
    'blue': dict(zip(
        ['dark_surface', 'dark_text', 'dark_muted', 'dark_accent', 'light_surface',
         'light_text', 'light_muted', 'light_accent', 'highlight'],
        ['#101d32', '#f1f4fa', '#bcc9dd', '#b6d2ff', '#f1f4fa',
         '#182f50', '#4b607c', '#285da3', '#efa97b'])),
    'plum': dict(zip(
        ['dark_surface', 'dark_text', 'dark_muted', 'dark_accent', 'light_surface',
         'light_text', 'light_muted', 'light_accent', 'highlight'],
        ['#281b2c', '#f7f0f5', '#d2c0d0', '#ebc0e4', '#f7f0f5',
         '#432940', '#73566d', '#854476', '#e9b881']))
}


def contrast(a, b):
    def luminance(color):
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
        return sum(v * w for v, w in zip(linear, [.2126, .7152, .0722]))
    x, y = sorted([luminance(a), luminance(b)])
    return (y + .05) / (x + .05)


def resolve_palette(deck):
    name = deck.get('palette', 'forest')
    if not isinstance(name, str) or name not in PRESETS:
        raise ValueError('palette must be forest, blue or plum')
    overrides = deck.get('colors', {})
    if not isinstance(overrides, dict) or set(overrides) - PRESETS[name].keys():
        raise ValueError('colors must contain only documented semantic color roles')
    colors = dict(PRESETS[name], **overrides)
    for role, value in colors.items():
        if not isinstance(value, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
            raise ValueError(f'{role}: use an opaque #RRGGBB color')
    # All text roles can appear in small labels, so use the conservative 4.5 threshold.
    for mode in ['dark', 'light']:
        for role in ['text', 'muted', 'accent']:
            ratio = contrast(colors[f'{mode}_{role}'], colors[f'{mode}_surface'])
            if ratio < 4.5:
                raise ValueError(f'{mode}_{role} on {mode}_surface: {ratio:.2f}:1 contrast; need at least 4.5:1')
    return colors


def theme_css(deck):
    colors = resolve_palette(deck)
    declarations = ';'.join(f'--{key.replace("_", "-")}:{value}' for key, value in colors.items())
    css = ':root{' + declarations + '}\n'
    # Preserve the established speaker palette exactly for existing forest decks.
    if deck.get('palette', 'forest') == 'forest' and not deck.get('colors'):
        return css
    return css + ''':root{--illustration-soft:color-mix(in srgb,var(--light-accent) 10%,var(--light-surface));--illustration-mid:color-mix(in srgb,var(--light-accent) 22%,var(--light-surface));--illustration-shadow:color-mix(in srgb,var(--light-accent) 20%,transparent)}
@media screen {
body:has(.slide-note){background:var(--light-surface);color:var(--light-text)}
body.notes-deck{background:var(--light-surface)}
.notes-toolbar{background:var(--light-surface);color:var(--light-text);border-color:var(--light-muted)}
.notes-toolbar button{background:var(--light-surface);color:var(--light-text);border-color:var(--light-muted)}
.notes-toolbar .open-presentation{background:var(--light-accent);color:var(--light-surface)}
.notes-position,.note-heading h2{color:var(--light-text)}
.notes-keys,.sync-status,.sync-status[data-connected="true"],.eyebrow,.time,.purpose,
body.notes-deck .purpose,.quick span,.slide-thumbnail figcaption{color:var(--light-muted)}
body:has(.slide-note) a{color:var(--light-accent)}
.time,.notice,.quick li{background:var(--light-surface);border-color:var(--light-muted)}
.spoken,.speaker-timer{background:var(--dark-surface);color:var(--dark-text)}
.spoken .label,.timer-budget,.page-budget,.timer-help{color:var(--dark-muted)}
.timer-page,.speaker-timer,.speaker-timer button{border-color:var(--dark-muted)}
.speaker-timer .timer-toggle{background:var(--dark-accent);color:var(--dark-surface);border-color:var(--dark-accent)}
.timer-page[data-timing="over"] .page-elapsed,.timer-page[data-timing="over"] .page-budget{color:var(--dark-text);font-weight:700;text-decoration:underline}
.thumbnail-window{background:var(--dark-surface)}
body.notes-deck .script-scroll .script-content{scrollbar-color:var(--dark-muted) var(--dark-surface)}
/* Stage directions retain their yellow background and explicit brackets. */
}
'''
