#!/usr/bin/env python3
"""Count the prose in chapter files and flag chapters under the target.

Counts only the text between "## Text" and "## Notes" when those headings
exist. Counts CJK characters when they are the majority, words otherwise.

Usage:
  python scripts/wordcount.py chapters/chapter-0001.md
  python scripts/wordcount.py --all novels/my-book/chapters
  python scripts/wordcount.py chapters/chapter-0001.md --min 2500
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CJK = re.compile(r"[㐀-䶿一-鿿豈-﫿぀-ヿ가-힯]")
WORD = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*", re.UNICODE)


def prose(text: str) -> str:
    match = re.search(r"(?m)^##\s+(Text|Texto|正文)\s*$", text)
    if match:
        text = text[match.end():]
        end = re.search(r"(?m)^##\s+(Notes|Notas|章节备注)\s*$", text)
        if end:
            text = text[: end.start()]
    # Drop markdown headings and markup characters.
    text = re.sub(r"(?m)^#{1,6}\s.*$", "", text)
    return re.sub(r"[*_`~]", "", text)


def count(text: str) -> tuple[int, str]:
    body = prose(text)
    cjk = len(CJK.findall(body))
    words = len(WORD.findall(CJK.sub(" ", body)))
    if cjk > words:
        return cjk, "characters"
    return words, "words"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", type=Path)
    parser.add_argument("--all", action="store_true", help="check every .md file in a folder")
    parser.add_argument("--min", type=int, default=None,
                        help="minimum (default 1800 words or 3000 characters)")
    args = parser.parse_args()

    files = sorted(args.path.glob("*.md")) if args.all else [args.path]
    if not files:
        print(f"No .md files found in {args.path}")
        return 1

    short = 0
    total = 0
    for file in files:
        try:
            n, unit = count(file.read_text(encoding="utf-8"))
        except OSError as error:
            print(f"{file}: cannot read ({error})")
            return 1
        minimum = args.min if args.min is not None else (3000 if unit == "characters" else 1800)
        flag = "OK" if n >= minimum else f"SHORT (minimum {minimum})"
        short += n < minimum
        total += n
        print(f"{file.name}: {n} {unit} {flag}")

    if len(files) > 1:
        print(f"Total: {total} across {len(files)} files, {short} short")
    return 2 if short else 0


if __name__ == "__main__":
    sys.exit(main())
