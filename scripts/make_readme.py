#!/usr/bin/env python3
"""Generate the GitHub profile README. Edit CONTENT to update profile copy."""
from pathlib import Path

CONTENT = """<!--
SizWinz portfolio · connected project cards with individual links.
Graphics adapted from HANCORE's MIT-licensed assets. See LICENSE-HANCORE.
Project covers use original branding and generated artwork based on repository details.
Rebuild: python scripts/build.py && python scripts/build_art_assets.py && python scripts/build_composed.py && python scripts/build_cards.py && python scripts/build_stats.py && python scripts/build_profile_extras.py && python scripts/build_wakatime.py
Regenerate README: python scripts/make_readme.py
-->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/sahaj-signature-dark.svg" />
    <img src="./assets/sahaj-signature-light.svg" width="220" alt="Sahaj Italiya signature" align="top" />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(min-width: 1280px) and (prefers-color-scheme: dark)" srcset="./assets/bio-wide-dark.png" width="744" height="76" />
    <source media="(min-width: 1280px) and (prefers-color-scheme: light)" srcset="./assets/bio-wide-light.png" width="744" height="76" />
    <source media="(prefers-color-scheme: dark)" srcset="./assets/bio-narrow-dark.png" />
    <img src="./assets/bio-narrow-light.png" width="280" height="161" alt="Sahaj Italiya — Computer Engineering student and software builder" />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/label-main-dark.png" />
    <img src="./assets/label-main-light.png" width="248" alt="Desktop apps and systems" />
  </picture>
</p>

<p align="center">
<a href="https://github.com/PocketMC/pocket-mc-windows" title="PocketMC"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-pocketmc-hq-dark.svg" /><img src="./assets/card-pocketmc-hq-light.svg" width="248" height="350" alt="PocketMC" align="top" /></picture></a><a href="https://github.com/sizwinz/MSM-minecraft-server-manager-termux" title="MSM"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-msm-hq-dark.svg" /><img src="./assets/card-msm-hq-light.svg" width="248" height="350" alt="MSM" align="top" /></picture></a><a href="https://github.com/sizwinz/StudySage-Offline-Online-AI-Note-Assistant" title="StudySage"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-studysage-hq-dark.svg" /><img src="./assets/card-studysage-hq-light.svg" width="248" height="350" alt="StudySage" align="top" /></picture></a><br />
<a href="https://github.com/DS-labs-33" title="DS Labs"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-ds-labs-dark.svg" /><img src="./assets/card-ds-labs-light.svg" width="744" height="115" alt="DS Labs" align="top" /></picture></a>

</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/label-gallery-dark.png" />
    <img src="./assets/label-gallery-light.png" width="248" alt="More things I build" />
  </picture>
</p>

<p align="center">
<a href="https://github.com/sizwinz/GitFetch" title="GitFetch"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-gitfetch-hq-dark.svg" /><img src="./assets/card-gitfetch-hq-light.svg" width="248" height="275" alt="GitFetch" align="top" /></picture></a><a href="https://github.com/sizwinz/SkillWise" title="SkillWise"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-skillwise-hq-dark.svg" /><img src="./assets/card-skillwise-hq-light.svg" width="248" height="275" alt="SkillWise" align="top" /></picture></a><a href="https://github.com/sizwinz/ServerPulse" title="ServerPulse"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-serverpulse-hq-dark.svg" /><img src="./assets/card-serverpulse-hq-light.svg" width="248" height="275" alt="ServerPulse" align="top" /></picture></a><br />
<a href="https://github.com/sizwinz/WatchMark" title="WatchMark"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-watchmark-dark.svg" /><img src="./assets/card-watchmark-light.svg" width="248" height="115" alt="WatchMark" align="top" /></picture></a><a href="https://github.com/DS-Labs-33/Campus-Assistant" title="Campus Assistant"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-campus-dark.svg" /><img src="./assets/card-campus-light.svg" width="248" height="115" alt="Campus Assistant" align="top" /></picture></a><a href="https://github.com/PocketMC/pocket-mc-linux-mac" title="PocketMC on Linux"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-pocketmc-linux-dark.svg" /><img src="./assets/card-pocketmc-linux-light.svg" width="248" height="115" alt="PocketMC on Linux" align="top" /></picture></a><br />
<a href="https://github.com/sizwinz?tab=repositories" title="More repositories"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-repositories-dark.svg" /><img src="./assets/card-repositories-light.svg" width="744" height="86" alt="More repositories" align="top" /></picture></a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/label-hackathons-dark.svg" />
    <img src="./assets/label-hackathons-light.svg" width="248" alt="Hackathon projects" />
  </picture>
</p>

<p align="center">
<a href="https://github.com/sizwinz/SchemeSetu" title="SchemeSetu"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-schemesetu-hq-dark.svg" /><img src="./assets/card-schemesetu-hq-light.svg" width="372" height="300" alt="SchemeSetu" align="top" /></picture></a><a href="https://github.com/sizwinz/EcoSpot" title="EcoSpot"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-ecospot-hq-dark.svg" /><img src="./assets/card-ecospot-hq-light.svg" width="372" height="300" alt="EcoSpot" align="top" /></picture></a><br />
<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/card-closing-dark.svg" /><img src="./assets/card-closing-light.svg" width="744" height="65" alt="Design · Engineer · Ship" align="top" /></picture>
</p>

<p align="center">
  <a href="https://github.com/sizwinz" title="GitHub statistics"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/github-stats-dark.svg" /><img src="./assets/github-stats-light.svg" width="744" height="412" alt="SizWinz GitHub statistics: project stars, contributions, languages and streaks" /></picture></a>
</p>

<p align="center">
  <a href="https://wakatime.com/@sizwinz" title="WakaTime all-time tracked time"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/wakatime-dark.svg" /><img src="./assets/wakatime-light.svg" width="360" height="44" alt="WakaTime all-time tracked time" align="top" /></picture></a>
</p>

<p align="center">
  <a href="https://sahaj33.me" title="sahaj33.me"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/link-website-dark.svg" /><img src="./assets/link-website-light.svg" width="176" height="56" alt="sahaj33.me" align="top" /></picture></a><a href="https://github.com/PocketMC" title="PocketMC"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/link-pocketmc-dark.svg" /><img src="./assets/link-pocketmc-light.svg" width="176" height="56" alt="PocketMC" align="top" /></picture></a><a href="https://github.com/DS-labs-33" title="DS Labs"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/link-dslabs-dark.svg" /><img src="./assets/link-dslabs-light.svg" width="176" height="56" alt="DS Labs" align="top" /></picture></a>
</p>

<p align="center">
  <a href="https://discord.com/users/775329619259162654" title="Discord"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/social-discord-dark.png" /><img src="./assets/social-discord-light.png" width="44" height="44" alt="Discord" /></picture></a>
  <a href="https://www.buymeacoffee.com/sahaj33" title="Buy Me a Coffee"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/social-coffee-dark.svg" /><img src="./assets/social-coffee-light.svg" width="44" height="44" alt="Buy Me a Coffee" /></picture></a>
  <a href="./ASSET-CREDITS.md" title="Artwork credits and licenses"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/social-acknowledgements-dark.png" /><img src="./assets/social-acknowledgements-light.png" width="44" height="44" alt="Credits" /></picture></a>
</p>

<details>
<summary>About me</summary>

I am a computer engineering student at Gujarat, India, trying to turn ideas into products that people might enjoy using.

I enjoy coding software and experimenting with new technology and approaches to create better products; My interests vary from AI to desktop applications, developer tools, and product development. I started **PocketMC**, a product I envisioned to redefine server management software for Minecraft.

I currently lead **DS Labs**, an organization in which I engage in idea and product development, as well as research to learn and experience the processes needed to evolve ideas into functional products, learning about the intricacies and real-life implementation details of software design and development.

Outside of coding, I'm fascinated by human psychology, gaming, entrepreneurship, and how people think and make decisions. I enjoy understanding not just how something works, but why it works.

I want to achieve ambitious goals for the products I am involved with, but I also understand that time is a critical factor, and I enjoy learning and experimenting with new concepts and approaches to evolve my skills as an engineer and software architect. I aspire to launch products with an impact worldwide and eventually turn them into successful businesses.

</details>

<details>
<summary>Setup & current activity</summary>

<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/setup-dark.svg" /><img src="./assets/setup-light.svg" width="744" height="272" alt="My setup: laptop, phone, mouse and earbuds" /></picture>

<p align="center">
  <a href="https://discord.com/users/775329619259162654" title="Live Discord presence"><picture><source media="(prefers-color-scheme: dark)" srcset="https://discord-rp-for-github.vercel.app/api/775329619259162654?layout=readme&amp;theme=dark&amp;showDisplayName=true&amp;idleMessage=Hey%2C+wsp%21+I%27m+Sahaj+AKA+SizWinz.+If+I%27m+doing+something%2C+then+you+will+get+to+see+it+here." /><img src="https://discord-rp-for-github.vercel.app/api/775329619259162654?layout=readme&amp;theme=light&amp;showDisplayName=true&amp;idleMessage=Hey%2C+wsp%21+I%27m+Sahaj+AKA+SizWinz.+If+I%27m+doing+something%2C+then+you+will+get+to+see+it+here." width="744" alt="Sahaj’s live Discord presence and current activity" /></picture></a>
</p>

</details>

<details>
<summary>Tech stack</summary>

<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/tech-stack-grid-dark.svg" /><img src="./assets/tech-stack-grid-light.svg" width="744" height="578" alt="Tech Stack Ever Used: languages, frameworks and UI, AI and ML, databases, tools and platforms, utilities" /></picture>

</details>

<details>
<summary>Quotes I live by</summary>

| Quote | Author |
| --- | --- |
| Become an expert in one thing and then build multiple income streams out of that one thing. | Raj Shamani |
| Give people wonderful tools and they'll do wonderful things. | Apple |
| Ever tried? Ever failed? No matter. Try again. Fail again. Fail better. | Samuel Beckett |
| I think it's very important to have a feedback loop, where you're constantly thinking about what you've done and how you could be doing it better. | Elon Musk |

</details>
"""

if __name__ == "__main__":
    path = Path(__file__).resolve().parents[1] / "README.md"
    path.write_text(CONTENT, encoding="utf-8")
    print("Updated", path)
