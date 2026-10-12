#!/usr/bin/env python3
"""Render aggregate WakaTime snapshots without exposing project or machine names."""
import json
from pathlib import Path
from build_profile_extras import palette, text, document

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'assets/wakatime-metrics.json'


def duration(seconds):
    minutes = round(max(0, seconds) / 60)
    return f'{minutes // 60}h {minutes % 60:02d}m'


def render(data, theme):
    panel, border, ink, muted, accent, inset = palette(theme)
    # Never present a cached weekly total as all-time during migration.
    valid = data and data.get('range') == 'all_time'
    value = duration(data['total_seconds']) if valid else 'Unavailable'
    body = f'<path d="M4 4H356V30L346 40H4Z" fill="{panel}" stroke="{border}"/>'
    body += f'<path d="M192 5V39" stroke="{border}"/>'
    body += (f'<g fill="none" stroke="{accent}" stroke-width="1.5">'
             '<circle cx="22" cy="22" r="7"/><path d="M22 18V22L26 24"/></g>')
    body += text(38, 26, 'WAKATIME · ALL TIME', 11, ink, 600)
    body += text(274, 27, value, 14, accent, 700, 'middle')
    title = 'WakaTime all-time tracked time: ' + value
    if valid:
        title += ' · updated ' + data['updated_at'][:16].replace('T', ' ') + ' UTC'
    return document(body, 360, 44, title)


def main():
    data = json.loads(SNAPSHOT.read_text(encoding='utf-8')) if SNAPSHOT.exists() else None
    for theme in ('dark', 'light'):
        (ROOT / f'assets/wakatime-{theme}.svg').write_text(render(data, theme), encoding='utf-8')


if __name__ == '__main__':
    main()
