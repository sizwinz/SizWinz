#!/usr/bin/env python3
"""Build connected GitHub README section illustrations.

All connector routes are drawn in the SAME SVG coordinate space as their cards.
No dependent multi-image spacing, no inline image seams and no runtime assets.
Uses HANCORE-inspired MIT-licensed source card frames from this repository.
"""
from __future__ import annotations

import re
import base64
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets"
DEST.mkdir(exist_ok=True)
SRC = {
    "main": [
        "source/feature-pocketmc", "source/feature-msm", "source/feature-studysage",
        "source/info-0",
    ],
    "gallery": [
        "source/gallery-gitfetch", "source/gallery-skillwise",
        "source/gallery-serverpulse", "source/info-small-0",
        "assets/connected-info-campus", "source/info-small-2", "source/archive",
    ],
    "hackathon": [
        "assets/hackathon-schemesetu", "assets/hackathon-ecospot", "source/closing",
    ],
}
THEMES = {
    "dark": ("#48525b", "#df6124"),
    "light": ("#8d969b", "#c34f1b"),
}
XML_NS = "http://www.w3.org/2000/svg"

PROJECT_ART = {
    'feature-pocketmc': 'pocketmc', 'feature-msm': 'msm',
    'feature-studysage': 'studysage', 'gallery-gitfetch': 'gitfetch',
    'gallery-skillwise': 'skillwise', 'gallery-serverpulse': 'serverpulse',
    'hackathon-schemesetu': 'schemesetu', 'hackathon-ecospot': 'ecospot',
}


def bitmap(path: Path, x, y, width, height, fit='slice') -> str:
    data = base64.b64encode(path.read_bytes()).decode('ascii')
    # Inline data keeps the illustration self-contained when GitHub loads it
    # as an image; nested network requests are not required.
    mime = 'image/jpeg' if path.suffix == '.jpg' else 'image/png'
    return (f'<image x="{x}" y="{y}" width="{width}" height="{height}" '
            f'preserveAspectRatio="xMidYMid {fit}" href="data:{mime};base64,{data}"/>')


def project_cover(raw: str, name: str) -> str:
    slug = PROJECT_ART.get(name.split('/')[-1])
    if not slug:
        return raw
    path = DEST / 'project-art' / 'web' / f'{slug}.jpg'
    if not path.exists():
        raise FileNotFoundError(f'Missing project cover: {path}')
    root = ET.fromstring(f'<svg xmlns="{XML_NS}">{raw}</svg>')
    ET.register_namespace('', XML_NS)
    # Preserve the original chamfered frame and its shadow; replace only
    # the invented interface art inside the card.
    defs = [e for e in root if e.tag.endswith('defs')]
    frames = [e for e in root if e.tag.endswith('path')][:2]
    labels = []
    if name.split('/')[-1].startswith('feature-'):
        bounds = (32, 35, 560, 548)
        labels = [e for e in root if e.tag.endswith('text') and e.get('y') == '636']
    elif name.split('/')[-1].startswith('gallery-'):
        bounds = (32, 24, 560, 325)
        labels = [e for e in root if e.tag.endswith('text') and e.get('y') in ('402', '444')]
    else:
        bounds = (33, 92, 678, 296)
        for e in root:
            if not e.tag.endswith('text'):
                continue
            if e.get('y') == '126':
                e.set('x', '48'); e.set('y', '413'); labels.append(e)
            elif e.get('y') == '425':
                e.set('y', '443'); labels.append(e)
            elif e.get('y') == '462':
                e.set('y', '469'); labels.append(e)
    result = ''.join(ET.tostring(e, encoding='unicode') for e in defs + frames)
    result += bitmap(path, *bounds)
    # Poster artwork already contains prominent project branding.
    result += ''.join(ET.tostring(e, encoding='unicode') for e in labels)
    return result


def route(d: str, color: str) -> str:
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>'


def node(x: int, y: int, color: str) -> str:
    return f'<rect x="{x - 3}" y="{y - 3}" width="6" height="6" fill="{color}"/>'


def connection_details(group: str, theme: str) -> str:
    """Bright signals and small terminal caps, scaled to the displayed cards.

    Adapted from HANCORE's folio_connections.py: 3.5-unit signals and
    3-unit terminals on a 624-unit card displayed at 248 pixels.
    Draw after the cards so terminal caps stay visible on their borders.
    """
    ink = '#e8e3d9' if theme == 'dark' else '#41474d'
    scale = 248 / 624
    caps = []

    def cap(x, y):
        caps.append(f'M{x - 11 * scale:.3f} {y:.3f}H{x + 11 * scale:.3f}')

    if group == 'main':
        signals = 'M186 30H208M536 30H558M372 39V47'
        for x in (124, 372, 620):
            cap(x, 45 + 16 * scale)
            cap(x, 45 + 668 * scale)
        cap(372, 366 + 16 * scale)
        cap(372, 366 + 160 * scale)
    elif group == 'gallery':
        signals = ('M186 30H208M536 30H558M372 35V42'
                   'M124 241V249M372 241V249M620 241V249'
                   'M186 262H208M536 262H558M372 382V390')
        for x in (124, 372, 620):
            cap(x, 42 + 16 * scale)
            cap(x, 42 + 460 * scale)
        for x in (124, 372, 620):
            cap(x, 281 + 16 * scale)
            cap(x, 281 + 160 * scale)
        cap(372, 397 + 16 * scale)
    else:
        signals = 'M186 35V49M558 35V49M248 285H270M474 285H496M372 294V301'
        for x in (186, 558):
            cap(x, 20 + 83 * .5)
            cap(x, 20 + 483 * .5)
        cap(372, 307 + 16 * scale)
    return (
        f'<g aria-label="Decorative connector signals and terminals">'
        f'<path d="{signals}" fill="none" stroke="{ink}" stroke-width="{3.5 * scale:.3f}"/>'
        f'<path d="{"".join(caps)}" fill="none" stroke="{ink}" stroke-width="{3 * scale:.3f}"/>'
        '</g>'
    )


def embed(name: str, theme: str, x: int, y: int,
          width: float, height: float, view_box: str,
          strip_hack_routes: bool = False) -> str:
    path = ROOT / f"{name}-{theme}.svg"
    raw = path.read_text(encoding="utf-8")
    raw = raw[raw.index(">") + 1:].rstrip()
    raw = raw.rsplit("</svg>", 1)[0]
    if name == 'assets/connected-info-campus':
        # Use the same compact frame geometry as its new row companions.
        raw = (ROOT / f'source/info-0-{theme}.svg').read_text(encoding='utf-8')
        raw = raw[raw.index('>') + 1:].rsplit('</svg>', 1)[0]
        raw = raw.replace('DS Labs', 'Campus Assistant').replace(
            'Products made to be used.', 'Multilingual campus helper.')
    if name in ('source/info-0', 'source/archive', 'source/closing'):
        root = ET.fromstring(f'<svg xmlns="{XML_NS}">{raw}</svg>')
        accent = THEMES[theme][1]
        for text in root:
            if not text.tag.endswith('text'):
                continue
            if text.text == 'DS Labs':
                text.set('font-family', 'IBM Plex Mono, DejaVu Sans Mono, monospace')
                text.set('font-size', '50'); text.set('font-weight', '700')
                text.set('letter-spacing', '2'); text.set('fill', accent)
                text.set('y', '78')
            elif text.text == 'More repositories':
                text.set('fill', accent)
            elif name == 'source/closing':
                text.set('y', '53')
                text.set('dominant-baseline', 'middle')
        if name == 'source/info-0':
            frame = [e for e in root if e.tag.endswith('path')][1]
            frame.set('stroke', accent); frame.set('stroke-width', '2.5')
            frame.set('fill', '#211c18' if theme == 'dark' else '#fff4e9')
        raw = ''.join(ET.tostring(e, encoding='unicode') for e in root)
    if strip_hack_routes:
        # Reuse artwork only: the new parent owns the complete network.
        raw = raw[raw.index("<defs>"):]
    raw = project_cover(raw, name)
    ident = name.split("/")[-1] + str(x)
    for old, new in [("float", f"float-{ident}"), ("shadow", f"shadow-{ident}")]:
        raw = raw.replace(f'id="{old}"', f'id="{new}"')
        raw = raw.replace(f'url(#{old})', f'url(#{new})')
    return (
        f'<svg x="{x}" y="{y}" width="{width}" height="{height}" '
        f'viewBox="{view_box}">{raw}</svg>'
    )


def compose(group: str, theme: str) -> str:
    wire, orange = THEMES[theme]
    art = SRC[group]

    if group == "main":
        height = 465
        body = (
            route("M372 10V30M124 30H620M124 30V52M372 30V52M620 30V52", wire)
            + route("M124 311V341M372 311V373M620 311V341M124 341H620M372 430V452", wire)
            + node(372, 10, orange) + node(372, 452, orange)
        )
        for i in range(3):
            body += embed(art[i], theme, i * 248, 45, 248, 278, "0 0 624 700")
        body += embed(art[3], theme, 248, 366, 248, 76.308, "0 0 624 192")

    elif group == "gallery":
        height = 476
        body = (
            route("M372 10V30M124 30H620M124 30V48M372 30V48M620 30V48", wire)
            + route("M124 225V288M372 225V288M620 225V288M124 262H620", wire)
            + route("M124 345V369M372 345V404M620 345V369M124 369H620", wire)
            + node(372, 10, orange)
        )
        for i in range(3):
            body += embed(art[i], theme, i * 248, 42, 248, 195.54, "0 0 624 492")
        for i in range(3):
            body += embed(art[3 + i], theme, i * 248, 281, 248, 76.308, "0 0 624 192")
        body += embed(art[6], theme, 248, 397, 248, 76.308, "0 0 624 192")

    else:
        height = 365
        body = (
            route("M372 7V23M186 23H558M186 23V63M558 23V63", wire)
            + route("M186 262V285M558 262V285M186 285H558M372 285V315", wire)
            + node(372, 7, orange) + node(372, 285, orange)
        )
        body += embed(art[0], theme, 0, 20, 372, 274, "0 0 744 548", True)
        body += embed(art[1], theme, 372, 20, 372, 274, "0 0 744 548", True)
        body += embed(art[2], theme, 248, 307, 248, 48.487, "0 0 624 122")

    body += connection_details(group, theme)
    result = (
        f'<svg xmlns="{XML_NS}" width="1488" height="{height * 2}" '
        f'viewBox="0 0 744 {height}" role="img" '
        f'aria-label="{group.title()} software project illustration">'
        f'<title>{group.title()} projects</title>{body}</svg>'
    )
    ET.fromstring(result)  # catches invalid XML entities before committing
    return result


def main() -> None:
    for theme in THEMES:
        for group in SRC:
            target = DEST / f"composed-{group}-{theme}.svg"
            target.write_text(compose(group, theme), encoding="utf-8")
            print("Wrote", target.relative_to(ROOT))


if __name__ == "__main__":
    main()
