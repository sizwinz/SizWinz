# Artwork credits and reuse

This GitHub profile redesign uses HANCORE's MIT-licensed visual asset design system, especially its original chamfered card-frame geometry, SVG shadow/filter definitions, orange and slate palette, typography settings, connected line-route paths, and responsive card layout.

- Original repository: [HANCORE-linux/HANCORE-linux](https://github.com/HANCORE-linux/HANCORE-linux)
- Original source directory: [`folio/`](https://github.com/HANCORE-linux/HANCORE-linux/tree/main/folio)
- Original license: [MIT](./LICENSE-HANCORE)
- Original author: Copyright (c) 2025 HANCORE

The exact original image files `social-discord-{dark,light}.png` and `social-acknowledgements-{dark,light}.png` are bundled unmodified from the original SVG sources (converted to PNG for GitHub rendering). **SizWinz's logo, textual content and interface illustrations are different from HANCORE's original imagery**, and do not imply HANCORE or Omarchy endorsement. The project covers use original project branding and generated artwork grounded in repository descriptions. See [project artwork sources](./PROJECT-ARTWORK.md).

To regenerate: `python scripts/build.py && python scripts/build_art_assets.py && python scripts/build_composed.py && python scripts/build_cards.py && python scripts/build_stats.py && python scripts/make_readme.py`. Requires `cairosvg` and `Pillow`. Original MIT notice is retained in `LICENSE-HANCORE`.
