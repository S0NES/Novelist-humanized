#!/usr/bin/env python3
"""Build the release zip: dist/humanized-novelist-v<version>.zip.

The zip holds one folder, humanized-novelist/, with SKILL.md at its root, so it
can be uploaded as a skill to Claude.ai or MCP Market, or unzipped into any
agent's skills folder. Development files (.git, .github, dist) are left out.

Usage:
  python scripts/build-release.py
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".github", "dist", "__pycache__", "novels"}
SKIP_FILES = {".DS_Store"}


def main() -> int:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'(?m)^\s+version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', skill)
    if not match:
        print("SKILL.md has no metadata.version")
        return 1
    version = match.group(1)

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    target = dist / f"humanized-novelist-v{version}.zip"

    count = 0
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            relative = path.relative_to(ROOT)
            if path.is_dir() or relative.parts[0] in SKIP_DIRS:
                continue
            if any(part in SKIP_DIRS for part in relative.parts) or path.name in SKIP_FILES:
                continue
            archive.write(path, Path("humanized-novelist") / relative)
            count += 1

    print(f"Built {target.relative_to(ROOT)} with {count} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
