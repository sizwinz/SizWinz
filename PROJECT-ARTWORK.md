# Project cover artwork

The eight illustrated cards use bright product posters based on the actual
projects, replacing the former invented interface panels. Project names,
star counts, links, frames and connector paths remain native SVG elements.
Project logos and available application screenshots were supplied as generation
references alongside the user's four poster examples. Branding is included in
each poster, without a duplicate corner overlay. These are generated marketing
mockups, not unaltered application screenshots. ServerPulse, SchemeSetu and
EcoSpot previews are illustrative because no application capture was available.

Generation used the built-in imagegen tool. Full-resolution originals are in
`assets/project-art/`; the exact prompt set and reference paths are saved in
[`assets/project-art/poster-prompts.json`](./assets/project-art/poster-prompts.json).
The older `prompts.json` records the superseded editorial concept set.
Web thumbnails are in `assets/project-art/web/`, with original logos and their
delivery copies in `assets/project-logos/` and `assets/project-logos/web/`.

| Project | Repository evidence inspected | Cover subject |
| --- | --- | --- |
| [PocketMC](https://github.com/PocketMC/pocket-mc-windows) | README, `docs/assets/branding/logo.png`, `docs/assets/screenshots/screenshot-dashboard.png` | Green branding and a pale voxel landscape |
| [MSM](https://github.com/sizwinz/MSM-minecraft-server-manager-termux) | README, `assets/msm.png` (actual terminal capture) | Cyan branding with desktop and phone terminal previews |
| [StudySage](https://github.com/sizwinz/StudySage-Offline-Online-AI-Note-Assistant) | README, `assets/images/logo.png`, `assets/images/react_web_app_summary.png` | Mint and lavender branding with a dark summary app mockup |
| [GitFetch](https://github.com/sizwinz/GitFetch) | README, `public/screenshot dark.png`, `public/screenshot light.png` | GitHub branding and a light profile intelligence dashboard mockup |
| [SkillWise](https://github.com/sizwinz/SkillWise) | README, `SkillWise.png`, `screenshots/screenshot.png` | Book and learning path branding with a light resume upload app mockup |
| [ServerPulse](https://github.com/sizwinz/ServerPulse) | Public README retrieved from GitHub; no local checkout or logo found | Lavender community analytics poster with illustrative activity charts |
| [SchemeSetu](https://github.com/sizwinz/SchemeSetu) | Local `Hackathon/SchemeSetu1/README.md`, `public/logo.png` | Amber branding and illustrative eligibility, match and finance steps |
| [EcoSpot](https://ecospot-web.onrender.com) | Local `Hackathon/Hackout DAIICT/README.md`, `frontend/public/EcoSpot.png` | Mint branding and illustrative factory flow and emissions charts |

## Rebuilding

```sh
python scripts/build_art_assets.py
python scripts/build_composed.py
python scripts/build_cards.py
python scripts/make_readme.py
```

Project cards embed the original full-resolution PNGs without JPEG compression
or thumbnail resizing. The `-hq` card filenames avoid cached lower-quality artwork.
Thumbnail encoding for other uses requires Pillow and leaves original PNGs untouched.
Each linked tile contains only the card subtrees visible in its crop, keeping
bitmap payloads small. Compact text cards retain their original centered text.
The stats panel and automatic metrics workflow continue to use the same data.
