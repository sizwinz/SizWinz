#!/usr/bin/env python3
"""Crop composed illustrations into independently clickable README cards.

SVG links inside an embedded image are not used; the README wraps each tile
in an HTML anchor. Crops retain the original connector coordinates.
"""
from pathlib import Path
import json
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
CARDS = {'main': [('pocketmc', 'PocketMC', 'https://github.com/PocketMC/pocket-mc-windows', 0, 0, 248, 350),
          ('msm',
           'MSM',
           'https://github.com/sizwinz/MSM-minecraft-server-manager-termux',
           248,
           0,
           248,
           350),
          ('studysage',
           'StudySage',
           'https://github.com/sizwinz/StudySage-Offline-Online-AI-Note-Assistant',
           496,
           0,
           248,
           350),
          ('ds-labs', 'DS Labs', 'https://github.com/DS-labs-33', 0, 350, 744, 115)],
 'gallery': [('gitfetch', 'GitFetch', 'https://github.com/sizwinz/GitFetch', 0, 0, 248, 275),
             ('skillwise', 'SkillWise', 'https://github.com/sizwinz/SkillWise', 248, 0, 248, 275),
             ('serverpulse', 'ServerPulse', 'https://github.com/sizwinz/ServerPulse', 496, 0, 248, 275),
             ('watchmark', 'WatchMark', 'https://github.com/sizwinz/WatchMark', 0, 275, 248, 115),
             ('campus',
              'Campus Assistant',
              'https://github.com/DS-Labs-33/Campus-Assistant',
              248,
              275,
              248,
              115),
             ('pocketmc-linux',
              'PocketMC on Linux',
              'https://github.com/PocketMC/pocket-mc-linux-mac',
              496,
              275,
              248,
              115),
             ('repositories',
              'More repositories',
              'https://github.com/sizwinz?tab=repositories',
              0,
              390,
              744,
              86)],
 'hackathon': [('schemesetu', 'SchemeSetu', 'https://github.com/sizwinz/SchemeSetu', 0, 0, 372, 300),
               ('ecospot', 'EcoSpot', 'https://ecospot-web.onrender.com', 372, 0, 372, 300),
               ('closing', 'Design · Engineer · Ship', None, 0, 300, 744, 65)]}

def star_badge(stars, x, y, theme, font_size=28):
    """The threshold is strictly greater than five; missing counts stay hidden."""
    if stars is None or stars <= 5:
        return ""
    orange = '#df6124' if theme == 'dark' else '#c34f1b'
    return (f'<g aria-label="{stars} GitHub stars"><title>{stars} GitHub stars</title>'
            f'<text x="{x}" y="{y}" text-anchor="end" '
            f'font-family="DejaVu Sans,Arial,sans-serif" font-size="{font_size}" '
            f'font-weight="600" fill="{orange}">★ {stars}</text></g>')


def title_row(original, title, stars, theme, align_name=True, crop=None):
    """Align the name and stars inside the card's own SVG coordinate system."""
    namespace = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', namespace)
    root = ET.fromstring(original)
    if crop is not None:
        x, y, width, height = crop
        # Retain only card subtrees intersecting this tile. Otherwise every
        # linked tile would redundantly carry all large cover bitmaps.
        for child in list(root):
            if child.tag != f'{{{namespace}}}svg':
                continue
            cx, cy = float(child.get('x', 0)), float(child.get('y', 0))
            cw, ch = float(child.get('width', 0)), float(child.get('height', 0))
            if cx >= x + width or cy >= y + height or cx + cw <= x or cy + ch <= y:
                root.remove(child)
    parents = {child: parent for parent in root.iter() for child in parent}
    for element in root.iter(f'{{{namespace}}}text'):
        if ''.join(element.itertext()).strip() != title:
            continue
        if align_name:
            element.set('text-anchor', 'start')
            element.set('x', '48')
        parent = parents[element]
        viewport = parent
        while viewport.tag != f'{{{namespace}}}svg':
            viewport = parents[viewport]
        view_box = [float(value) for value in viewport.get('viewBox').split()]
        badge = star_badge(stars, view_box[0] + view_box[2] - 48,
                           element.get('y'), theme)
        if badge:
            parent.append(ET.fromstring(badge))
        break
    else:
        if stars is not None and stars > 5:
            raise ValueError(f'No project-name row found for {title}')
    return ''.join(ET.tostring(child, encoding='unicode') for child in root)


def main():
    metrics = ROOT / 'assets' / 'github-metrics.json'
    repositories = json.loads(metrics.read_text(encoding='utf-8'))['repositories'] if metrics.exists() else {}
    for group, cards in CARDS.items():
        for theme in ("dark", "light"):
            original = (ROOT / "assets" / f"composed-{group}-{theme}.svg").read_text(encoding="utf-8")
            for slug, title, url, x, y, width, height in cards:
                repo = url.removeprefix('https://github.com/') if url else ''
                stars = repositories.get(repo)
                # Only illustration cards use a left-name/right-stars footer.
                # Compact info/navigation cards keep their centered text, and
                # hackathon cards retain their existing heading alignment.
                align_name = slug in ('pocketmc', 'msm', 'studysage', 'gitfetch', 'skillwise', 'serverpulse')
                inner = title_row(original, title, stars, theme, align_name,
                                  (x, y, width, height))
                svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * 2}" '
                       f'height="{height * 2}" viewBox="{x} {y} {width} {height}" overflow="hidden">'
                       f'<title>{escape(title)}</title>{inner}</svg>')
                ET.fromstring(svg)
                (ROOT / "assets" / f"card-{slug}-{theme}.svg").write_text(svg, encoding="utf-8")

if __name__ == "__main__":
    main()
