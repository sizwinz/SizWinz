#!/usr/bin/env python3
"""Encode web thumbnails; full-resolution generated art/logos stay untouched.

Only resize and encode delivery copies. Visual artwork is made with imagegen.
Input hashes prevent platform encoder differences from rewriting cached files.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'


def main():
    manifest = ASSETS / 'project-art' / 'web-manifest.json'
    previous = json.loads(manifest.read_text()) if manifest.exists() else {}
    hashes = {}
    inputs = list((ASSETS / 'project-art').glob('*.png')) + list((ASSETS / 'project-logos').glob('*.png'))
    for path in inputs:
        logo = path.parent.name == 'project-logos'
        key = path.relative_to(ASSETS).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes[key] = digest
        target = path.parent / 'web' / (path.stem + ('.png' if logo else '.jpg'))
        target.parent.mkdir(exist_ok=True)
        if previous.get(key) == digest and target.exists():
            continue
        with Image.open(path) as image:
            image.thumbnail((256, 256) if logo else (900, 900), Image.Resampling.LANCZOS)
            if logo:
                image.save(target, optimize=True)
            else:
                image.convert('RGB').save(target, quality=88, optimize=True)
    manifest.write_text(json.dumps(hashes, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
