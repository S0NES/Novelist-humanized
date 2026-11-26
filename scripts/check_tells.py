#!/usr/bin/env python3
"""Scan chapter prose for surface AI tells and print each hit with its line.

This finds patterns a regex can see: dashes, separator lines, banned words,
stock idioms and common not-X-but-Y shapes in English, Portuguese and
Spanish. It cannot judge rhythm, triads or subtext, so a clean result does
not mean the chapter is clean. Read it too.

Usage:
  python scripts/check_tells.py chapters/chapter-0001.md
  python scripts/check_tells.py --all novels/my-book/chapters
  python scripts/check_tells.py chapter.md --allow-dashes
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

I = re.IGNORECASE

CHECKS: list[tuple[str, re.Pattern[str]]] = [
    ("dash (rule 8)", re.compile(r"[—–]|\s--\s")),
    ("separator line (rule 8)", re.compile(r"^\s*([-*_=~#])\1{2,}\s*$")),
    ("not X but Y (rule 1)", re.compile(
        r"\b(it|this|that|he|she|they) (was|is|were)n['’]?t (just |only |merely )?\w+[^.!?]{0,40}([.,;]|\s[—–-]) *(it|this|that|he|she|they) (was|is|were)\b"
        r"|\b(that|this|it)['’]s not [^.!?]{1,40}[.,;] *(that|this|it)['’]s\b"
        r"|\bi['’]m not [^.!?]{1,30}[.,;] *i['’]m\b"
        r"|\bnot (just|only|merely) [^.!?]{1,60}\bbut\b"
        r"|\bn[ãa]o (era|é|foi|eram|são) (s[óo] |apenas |somente )?[^.!?]{1,40}([,;.]|\s[—–-]) *(era|é|foi|eram|são)\b"
        r"|\bn[ãa]o sou [^.!?]{1,30}[,;.] *sou\b"
        r"|\bno (era|es|fue) (solo |solamente )?[^.!?]{1,40}[,;.] *(era|es|fue)\b", I)),
    ("staged run-up (rule 4)", re.compile(
        r"^\s*(here['’]s the thing|the truth is|honestly\?|look,|a verdade é que|sinceramente\?|olha,)", I)),
    ("arguing with no one (rule 5)", re.compile(
        r"\b(not that (he|she|they|i) (was|were)|n[ãa]o que (ele|ela|eles) (fosse|estivesse|tivesse)|it wasn['’]t about|n[ãa]o era sobre)\b", I)),
    ("banned word (rule 11)", re.compile(
        r"\b(crucial|intricate|intricad[oa]s?|meticulous(ly)?|meticulos[oa]s?|vibrant|vibrantes?|tapestry|tapeçaria|testament|testemunho de"
        r"|delve[sd]?|delving|mergulhar fundo|underscor\w+|foster(s|ed|ing)?|fomentar|pivotal|a mix of|um misto de|a dance of|uma dança de)\b", I)),
    ("inflated significance (rule 12)", re.compile(
        r"\b(change[sd]? everything|everything (had )?changed|tudo (tinha )?mudado|tudo mudou|mudaria tudo|mudava tudo|indelible|indelével|a new era|uma nova era|lo cambiaba todo)\b", I)),
    ("stock idiom (rule 17)", re.compile(
        r"\b(heart (was )?pound\w*|blood ran cold|deafening silence|time stood still|tears streamed"
        r"|cora[çc][ãa]o disparad[oa]|sangue gelou|sil[êe]ncio ensurdecedor|o tempo parou|l[áa]grimas rolaram"
        r"|se le hel[óo] la sangre|silencio ensordecedor|el tiempo se detuvo)\b", I)),
    ("sales language (rule 14)", re.compile(
        r"\b(nestled|breathtaking|in the heart of|aninhad[oa]|de tirar o f[ôo]lego|no cora[çc][ãa]o d[aoe])\b", I)),
    ("chat leftover (rule 18)", re.compile(
        r"\b(here is (the )?chapter|i hope (you enjoy|this)|aqui est[áa] o cap[íi]tulo|espero que goste|as we saw|como vimos)\b", I)),
    ("all-caps or spaced emphasis (rule 2)", re.compile(r"\b[A-ZÀ-Ý]{4,}\b(?![^\n]*[a-z])|\b(\w+\. ){2,}\w+\.(?=\s|$)")),
]


def prose_lines(text: str) -> list[tuple[int, str]]:
    lines = text.splitlines()
    start, end = 0, len(lines)
    for i, line in enumerate(lines):
        if re.match(r"^##\s+(Text|Texto|正文)\s*$", line):
            start = i + 1
        elif start and re.match(r"^##\s+(Notes|Notas|章节备注)\s*$", line):
            end = i
            break
    return [(i + 1, lines[i]) for i in range(start, end)]


def scan(path: Path, allow_dashes: bool) -> int:
    hits = 0
    for number, line in prose_lines(path.read_text(encoding="utf-8")):
        for name, pattern in CHECKS:
            if allow_dashes and name.startswith("dash"):
                continue
            for match in pattern.finditer(line):
                hits += 1
                snippet = line.strip()
                if len(snippet) > 110:
                    snippet = snippet[:107] + "..."
                print(f"{path.name}:{number}: {name}: \"{match.group(0).strip()}\" | {snippet}")
    return hits


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", type=Path)
    parser.add_argument("--all", action="store_true", help="scan every .md file in a folder")
    parser.add_argument("--allow-dashes", action="store_true",
                        help="skip the dash check when the author's sample uses dashes")
    args = parser.parse_args()

    files = sorted(args.path.glob("*.md")) if args.all else [args.path]
    total = 0
    for file in files:
        try:
            total += scan(file, args.allow_dashes)
        except OSError as error:
            print(f"{file}: cannot read ({error})")
            return 1
    print(f"{total} surface tell(s) found in {len(files)} file(s). Read the text for the rest.")
    return 2 if total else 0


if __name__ == "__main__":
    sys.exit(main())
