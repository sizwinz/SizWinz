#!/usr/bin/env python3
"""Native SVG footer buttons and stack panel, matching the profile cards."""
import base64
from pathlib import Path
from xml.sax.saxutils import escape
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
STACK = [
    ('Languages', ['Python', 'TypeScript', 'C#', 'Go', 'Dart', 'JavaScript', 'HTML5', 'CSS3', 'SQL', 'Bash']),
    ('Frameworks & UI', ['React', 'Next.js', 'Vite', 'FastAPI', 'Flutter', '.NET 8', 'Streamlit', 'Tailwind CSS', 'WPF', 'Tauri']),
    ('AI / ML', ['Claude', 'Codex', 'Gemini', 'Hugging Face', 'PyTorch', 'Transformers', 'LangChain', 'OCR']),
    ('Databases', ['MongoDB', 'PostgreSQL', 'Redis', 'Supabase', 'SQLite']),
    ('Tools & platforms', ['Docker', 'Git', 'GitHub', 'Linux', 'VS Code', 'Vercel', 'GitHub Pages', 'Figma', 'Termux']),
    ('Utilities', ['ngrok', 'playit.gg', 'FFmpeg', 'yt-dlp', 'Tampermonkey', 'Minecraft server tools']),
]


def palette(theme):
    return (('#191c1e', '#353a3d', '#e8e3d9', '#bfc4c9', '#df6124', '#101213')
            if theme == 'dark' else
            ('#f3f2ef', '#b9c0c1', '#242b31', '#55616a', '#c34f1b', '#ecece9'))


def text(x, y, value, size=13, color='#e8e3d9', weight=500, anchor='start'):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans,Arial,sans-serif" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')


def document(body, width, height, title):
    attribute_title = escape(title, {'"': '&quot;'})
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * 2}" height="{height * 2}" '
           f'viewBox="0 0 {width} {height}" role="img" aria-label="{attribute_title}">'
           f'<title>{escape(title)}</title>{body}</svg>')
    ET.fromstring(svg)
    return svg


def stack_panel(theme):
    panel, border, ink, muted, accent, inset = palette(theme)
    body = f'<path d="M12 12H732V546L712 566H12Z" fill="{panel}" stroke="{border}"/>'
    body += text(32, 44, 'TECH STACK / EVER USED', 15, accent, 700)
    body += f'<path d="M32 62H712" stroke="{border}"/>'
    for index, (label, items) in enumerate(STACK):
        left = 32 + (index % 2) * 348
        top = 82 + (index // 2) * 160
        body += f'<rect x="{left}" y="{top}" width="332" height="148" rx="3" fill="{inset}" stroke="{border}"/>'
        body += f'<path d="M{left + 16} {top + 18}V{top + 30}" stroke="{accent}" stroke-width="2"/>'
        body += text(left + 26, top + 28, label, 13, ink, 700)
        x, cy = left + 16, top + 44
        for item in items:
            # A fixed-width font makes chip sizing deterministic on every runner.
            width = len(item) * 7.2 + 20
            if x + width > left + 316:
                x, cy = left + 16, cy + 33
            body += f'<rect x="{x}" y="{cy}" width="{width}" height="26" rx="2" fill="{panel}" stroke="{border}"/>'
            body += (f'<text x="{x + 10}" y="{cy + 17}" fill="{muted}" '
                     f'font-family="DejaVu Sans Mono,monospace" font-size="12">{escape(item)}</text>')
            x += width + 8
    return document(body, 744, 578, 'Tech Stack Ever Used: ' + '; '.join(label + ': ' + ', '.join(items) for label, items in STACK))


def footer_button(slug, label, theme):
    panel, border, ink, muted, accent, inset = palette(theme)
    body = f'<path d="M6 6H170V39L159 50H6Z" fill="{panel}" stroke="{border}"/>'
    if slug == 'pocketmc':
        logo = base64.b64encode((ROOT / 'assets/project-logos/web/pocketmc.png').read_bytes()).decode()
        body += f'<image x="18" y="15" width="26" height="26" href="data:image/png;base64,{logo}"/>'
    elif slug == 'website':
        body += (f'<g fill="none" stroke="{accent}" stroke-width="1.5">'
                 '<circle cx="31" cy="28" r="11"/><ellipse cx="31" cy="28" rx="5" ry="11"/>'
                 '<path d="M20 28H42M23 22H39M23 34H39"/></g>')
    else:
        body += text(18, 33, 'DS', 17, accent, 700)
    body += text(54, 33, label, 12, ink, 600)
    return document(body, 176, 56, label)


def main():
    for theme in ('dark', 'light'):
        (ROOT / f'assets/tech-stack-{theme}.svg').write_text(stack_panel(theme), encoding='utf-8')
        for slug, label in [('website', 'sahaj33.me'), ('pocketmc', 'PocketMC'), ('dslabs', 'DS Labs')]:
            (ROOT / f'assets/link-{slug}-{theme}.svg').write_text(footer_button(slug, label, theme), encoding='utf-8')


if __name__ == '__main__':
    main()
