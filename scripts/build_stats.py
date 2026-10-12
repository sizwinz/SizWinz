#!/usr/bin/env python3
"""Render cached GitHub data in the profile's chamfered orange/slate theme."""
import json
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]


def streaks(days, today):
    counts = {date.fromisoformat(d['date']): d['contributionCount'] for d in days}
    longest = run = 0
    previous = None
    for day in sorted(counts):
        if previous is not None and day != previous + timedelta(days=1):
            run = 0
        run = run + 1 if counts[day] > 0 else 0
        longest = max(longest, run)
        previous = day
    end = today if counts.get(today, 0) else today - timedelta(days=1)
    current = 0
    while counts.get(end, 0) > 0:
        current += 1
        end -= timedelta(days=1)
    return current, longest


def render(data, theme):
    dark = theme == 'dark'
    panel, border, ink, muted, orange, inset = (
        ('#191c1e', '#353a3d', '#e8e3d9', '#bfc4c9', '#df6124', '#101213') if dark
        else ('#f3f2ef', '#b9c0c1', '#242b31', '#55616a', '#c34f1b', '#ecece9'))
    parts = []
    def text(x, y, value, size=13, color=None, weight=500, anchor='start'):
        parts.append(f'<text x="{x}" y="{y}" fill="{color or ink}" '
                     f'font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" '
                     f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')
    parts.append(f'<path d="M12 12H732V380L712 400H12Z" fill="{panel}" stroke="{border}"/>')
    parts.append(f'<path d="M24 24H720V61H24Z" fill="{inset}"/>')
    text(38, 48, 'GITHUB / SIZWINZ', 12, orange, 700)
    text(704, 48, 'BUILD · SHARE · REPEAT', 10, muted, anchor='end')
    text(38, 94, 'By the numbers', 19, weight=700)
    text(398, 94, 'Languages I build with', 17, weight=700)
    collection = data['contributions']
    calendar = collection['contributionCalendar']
    days = [day for week in calendar['weeks'] for day in week['contributionDays']]
    today = date.fromisoformat(collection['endedAt'][:10])
    current, longest = streaks(days, today)
    rows = [('Project stars', data['project_stars']),
            ('Commits · past year', collection['totalCommitContributions']),
            ('Pull requests · past year', collection['totalPullRequestContributions']),
            ('Issues · past year', collection['totalIssueContributions']),
            ('Repos committed to · past year', collection['totalRepositoriesWithContributedCommits'])]
    for i, (label, value) in enumerate(rows):
        y = 128 + i * 26
        text(38, y, label, 12, muted)
        text(342, y, f'{value:,}', 14, orange if i == 0 else ink, 700, 'end')
    languages = data['languages']
    total = sum(item['bytes'] for item in languages)
    top = languages[:6]
    x = 398
    for i, item in enumerate(top):
        percentage = item['bytes'] / total if total else 0
        color = item['color'] or orange
        parts.append(f'<rect x="{x}" y="111" width="{percentage * 306}" height="8" fill="{color}"/>')
        x += percentage * 306
        col, row = i % 2, i // 2
        lx, ly = 398 + col * 160, 143 + row * 27
        parts.append(f'<rect x="{lx}" y="{ly - 8}" width="6" height="6" fill="{color}"/>')
        text(lx + 12, ly, item['name'], 11, muted)
        text(lx + 146, ly, f'{percentage * 100:.1f}%', 11, anchor='end')
    if x < 704:
        parts.append(f'<rect x="{x}" y="111" width="{704 - x}" height="8" fill="{border}"/>')
    text(398, 236, 'Public owned repos · non-forks · code bytes', 10, muted)
    parts.append(f'<path d="M38 262H706M372 110V243" stroke="{border}" fill="none"/>')
    for x, value, label in [(145, calendar['totalContributions'], 'CONTRIBUTIONS'),
                            (372, current, 'CURRENT STREAK'), (599, longest, 'LONGEST STREAK')]:
        text(x, 311, f'{value:,}', 29, orange if x == 372 else ink, 700, 'middle')
        text(x, 337, label, 10, muted, 600, 'middle')
    text(372, 363, 'Contribution calendar · past year · streaks in days', 10, muted, anchor='middle')
    text(38, 386, 'Stars: public owned + featured org repos', 9, muted)
    text(704, 386, 'Updated ' + data['updated_at'][:10] + ' UTC', 9, muted, anchor='end')
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1488" height="824" '
           'viewBox="0 0 744 412" role="img" aria-label="SizWinz GitHub statistics">'
           '<title>SizWinz GitHub statistics</title>' + ''.join(parts) + '</svg>')
    ET.fromstring(svg)
    return svg


def main():
    data = json.loads((ROOT / 'assets/github-metrics.json').read_text(encoding='utf-8'))
    for theme in ('dark', 'light'):
        (ROOT / 'assets' / f'github-stats-{theme}.svg').write_text(render(data, theme), encoding='utf-8')


if __name__ == '__main__':
    main()
