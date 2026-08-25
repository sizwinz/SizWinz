import os
import urllib.request
import json
from datetime import datetime, timezone

# -------------------------------------------------------------
# 1. CONSTANTS & THEME
# -------------------------------------------------------------
PROJ_WIDTH = 420
PROJ_HEIGHT = 160

BG_COLOR = "#0d1117"
BORDER_COLOR = "#30363d"
TITLE_COLOR = "#58a6ff"
LABEL_COLOR = "#8b949e"
VALUE_COLOR = "#e6edf3"
PROJ_TEXT_COLOR = "#8b949e"
ACCENT_GREEN = "#3fb950"
STAR_GOLD = "#e3b341"
HIGHLIGHT_COLOR = "#7d8590"

now = datetime.now(timezone.utc)
timestamp_str = now.strftime("%Y-%m-%d %H:%M UTC")

featured_projects = [
    {
        "owner": "PocketMC",
        "repo": "pocket-mc-windows",
        "name": "PocketMC",
        "filename": "assets/project-pocketmc.svg",
        "desc": "Local-first Windows desktop app to host and manage Minecraft servers with automated tunneling and cloud backups.",
        "tags": [("C#", "#512BD4"), (".NET 8", "#512BD4"), ("WPF", "#5C2D91")],
        "highlights": "Windows-native · Velopack updates · Job isolation",
        "stars": 27,
        "forks": 4
    },
    {
        "owner": "sizwinz",
        "repo": "MSM-minecraft-server-manager-termux",
        "name": "MSM",
        "filename": "assets/project-msm.svg",
        "desc": "Terminal-native Minecraft server manager for Termux and Linux with crash protection and SQLite tracking.",
        "tags": [("Python", "#3572A5"), ("Termux", "#89e051"), ("SQLite", "#003B57")],
        "highlights": "POSIX-first · WAL-mode SQLite · Safe backups",
        "stars": 30,
        "forks": 6
    },
    {
        "owner": "sizwinz",
        "repo": "StudySage-Offline-Online-AI-Note-Assistant",
        "name": "StudySage",
        "filename": "assets/project-studysage.svg",
        "desc": "Privacy-first AI study assistant with offline Seq2Seq summarization, OCR, and multi-modal interfaces.",
        "tags": [("Python", "#3572A5"), ("React", "#61DAFB"), ("FastAPI", "#009688")],
        "highlights": "Offline-capable · Multi-modal · 5 UIs in 1 app",
        "stars": 9,
        "forks": 1
    },
    {
        "owner": "sizwinz",
        "repo": "SkillWise",
        "name": "SkillWise",
        "filename": "assets/project-skillwise.svg",
        "desc": "Career transition intelligence engine with LLM skill gap analysis and interactive 6-month roadmaps.",
        "tags": [("Python", "#3572A5"), ("Streamlit", "#FF4B4B"), ("Plotly", "#3F4F75")],
        "highlights": "Multi-provider LLM · Zero-shot gaps · Plotly viz",
        "stars": 6,
        "forks": 0
    },
    {
        "owner": "sizwinz",
        "repo": "GitFetch",
        "name": "GitFetch",
        "filename": "assets/project-gitfetch.svg",
        "desc": "Developer profile intelligence platform turning GitHub profiles into dashboards and AI-ready portfolio context.",
        "tags": [("TypeScript", "#3178c6"), ("React 19", "#61DAFB"), ("Vite", "#646CFF")],
        "highlights": "AI assistant proxy · Glassmorphism · Fast export",
        "stars": 2,
        "forks": 0
    },
    {
        "owner": "sizwinz",
        "repo": "ServerPulse",
        "name": "ServerPulse",
        "filename": "assets/project-serverpulse.svg",
        "desc": "Real-time Discord analytics bot with AI-generated Pulse Reports, engagement tracking, and multi-provider LLMs.",
        "tags": [("Python", "#3572A5"), ("MongoDB", "#47A248"), ("Redis", "#DC382D")],
        "highlights": "Docker-first · Redis leaderboards · Anomaly alerts",
        "stars": 2,
        "forks": 0
    }
]

headers = {"User-Agent": "Mozilla/5.0"}
github_token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
if github_token:
    headers["Authorization"] = f"token {github_token}"

# -------------------------------------------------------------
# 2. REAL-TIME DATA FETCHERS
# -------------------------------------------------------------
for proj in featured_projects:
    try:
        url = f"https://api.github.com/repos/{proj['owner']}/{proj['repo']}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            proj["stars"] = data.get("stargazers_count", proj["stars"])
            proj["forks"] = data.get("forks_count", proj["forks"])
            if data.get("description") and len(data["description"]) > 10:
                proj["desc"] = data["description"]
    except Exception as e:
        print(f"Project fetch notice for {proj['repo']}: {e}")

os.makedirs("assets", exist_ok=True)

# -------------------------------------------------------------
# 3. GENERATE FEATURED PROJECT CARDS (6 CARDS)
# -------------------------------------------------------------
def format_desc(text, max_chars=54):
    words = text.split()
    lines = []
    curr = []
    curr_len = 0
    for w in words:
        if curr_len + len(w) + 1 > max_chars and len(lines) < 2:
            lines.append(" ".join(curr))
            curr = [w]
            curr_len = len(w)
        else:
            curr.append(w)
            curr_len += len(w) + 1
    if curr and len(lines) < 2:
        lines.append(" ".join(curr))
    return lines

for p in featured_projects:
    desc_lines = format_desc(p["desc"], max_chars=56)
    desc_tspan = ""
    if len(desc_lines) >= 1:
        desc_tspan += f'<tspan x="20" y="86">{desc_lines[0]}</tspan>'
    if len(desc_lines) >= 2:
        desc_tspan += f'<tspan x="20" y="104">{desc_lines[1]}</tspan>'

    badges_svg = []
    tag_offset = 0
    for tag_name, tag_col in p.get("tags", []):
        tag_width = max(len(tag_name) * 7.0 + 26, 52)
        badges_svg.append(f'''
      <g transform="translate({tag_offset:.1f}, 0)">
        <rect width="{tag_width:.1f}" height="21" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1"/>
        <circle cx="10" cy="10.5" r="3.5" fill="{tag_col}"/>
        <text x="18" y="14.5" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="10.5" font-weight="600" fill="#c9d1d9">{tag_name}</text>
      </g>''')
        tag_offset += tag_width + 8
    badges_rendered = "".join(badges_svg)

    highlights_text = p.get("highlights", "")
    if len(highlights_text) > 52:
        highlights_text = highlights_text[:50] + "..."

    forks_svg = ""
    highlights_offset = 50
    if p["forks"] > 0:
        highlights_offset = 95
        forks_svg = f'''
    <g transform="translate(48, 0)">
      <svg x="0" y="0" width="14" height="14" viewBox="0 0 16 16" fill="{LABEL_COLOR}">
        <path d="M5 3.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm0 2.122a2.25 2.25 0 1 0-1.5 0v.878A2.25 2.25 0 0 0 5.75 8.5h1.5v2.128a2.251 2.251 0 1 0 1.5 0V8.5h1.5a2.25 2.25 0 0 0 2.25-2.25v-.878a2.25 2.25 0 1 0-1.5 0v.878a.75.75 0 0 1-.75.75h-4.5a.75.75 0 0 1-.75-.75v-.878Zm3.75 7.378a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm3-8.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"/>
      </svg>
      <text x="17" y="11" class="meta-val">{p["forks"]}</text>
    </g>'''

    proj_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PROJ_WIDTH} {PROJ_HEIGHT}" width="100%" height="{PROJ_HEIGHT}">
  <!-- Generated: {timestamp_str} -->
  <defs>
    <linearGradient id="cardBg_{p["name"]}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#121720"/>
    </linearGradient>
  </defs>

  <style>
    .proj-title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 15.5px; fill: {TITLE_COLOR}; }}
    .proj-desc {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 11.5px; fill: {PROJ_TEXT_COLOR}; line-height: 1.4; }}
    .meta-val {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 11.5px; fill: {VALUE_COLOR}; font-weight: 600; }}
    .highlights-text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 10.5px; fill: {HIGHLIGHT_COLOR}; }}
  </style>

  <rect x="0.5" y="0.5" width="{PROJ_WIDTH - 1}" height="{PROJ_HEIGHT - 1}" rx="8" fill="url(#cardBg_{p["name"]})" stroke="{BORDER_COLOR}" stroke-width="1"/>

  <!-- Title & Repo Book Icon -->
  <g transform="translate(20, 18)">
    <svg x="0" y="1" width="16" height="16" viewBox="0 0 16 16" fill="{ACCENT_GREEN}">
      <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 0-.75.75v1.25a.75.75 0 0 1-1.28.53L7.47 14.25a.75.75 0 0 0-.53-.22H4.5A2.5 2.5 0 0 1 2 11.5v-9Zm10.5 10V1.5H4.5a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h2.44a2.25 2.25 0 0 1 1.59.66l1.47 1.47V13.25a2.25 2.25 0 0 1 2-2.22V11H12.5v1.5ZM4.5 12h7a.75.75 0 0 0 .75-.75V11H4.5a1 1 0 0 0-1 1v-.25c.2.16.45.25.75.25Z"/>
    </svg>
    <text x="24" y="14" class="proj-title">{p["name"]}</text>
  </g>

  <!-- Badges Row -->
  <g transform="translate(20, 44)">
    {badges_rendered}
  </g>

  <!-- Description -->
  <text class="proj-desc">
    {desc_tspan}
  </text>

  <!-- Divider Line -->
  <line x1="20" y1="126" x2="{PROJ_WIDTH - 20}" y2="126" stroke="#21262d" stroke-width="1"/>

  <!-- Footer Row (Stars, Forks, Highlights) -->
  <g transform="translate(20, 137)">
    <!-- Stars -->
    <g transform="translate(0, 0)">
      <svg x="0" y="0" width="14" height="14" viewBox="0 0 16 16" fill="{STAR_GOLD}">
        <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.74a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.695Z"/>
      </svg>
      <text x="17" y="11" class="meta-val">{p["stars"]}</text>
    </g>
    {forks_svg}

    <!-- Highlights -->
    <g transform="translate({highlights_offset}, 0)">
      <text x="0" y="11" class="highlights-text">· {highlights_text}</text>
    </g>
  </g>
</svg>'''

    with open(p["filename"], "w", encoding="utf-8") as f:
        f.write(proj_svg)
    print(f"Generated {p['filename']}")

print("All 6 Featured Project cards generated successfully!")
