#!/usr/bin/env python3
"""Check Humanized Novelist's package files. No external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def read(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except OSError as error:
        sys.exit(f"Cannot read {path}: {error}")


def load_json(path: str) -> dict:
    try:
        return json.loads(read(path))
    except json.JSONDecodeError as error:
        sys.exit(f"Fix the JSON in {path}: {error}")


SKILL = read("SKILL.md")
README = read("README.md")
CHANGELOG = read("CHANGELOG.md")
PLUGIN = load_json(".claude-plugin/plugin.json")
MARKET = load_json(".claude-plugin/marketplace.json")
CURSOR = load_json(".cursor-plugin/plugin.json")
PACKAGE = load_json("package.json")

meta = re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL)
if not meta:
    sys.exit("SKILL.md must begin with YAML metadata")
yaml = meta.group(1)

if not re.search(r"(?m)^name: humanized-novelist$", yaml):
    errors.append("SKILL.md name must be humanized-novelist")
for field in ("version:", "allowed-tools:"):
    if re.search(rf"(?m)^{field}", yaml):
        errors.append(f"Remove top-level YAML field {field[:-1]}")

version = re.search(r'(?m)^\s+version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', yaml)
changelog = re.search(r"(?m)^## ([0-9]+\.[0-9]+\.[0-9]+)$", CHANGELOG)
versions = {
    version.group(1) if version else "missing",
    changelog.group(1) if changelog else "missing",
    str(PLUGIN.get("version")),
    str(CURSOR.get("version")),
}
if len(versions) != 1:
    errors.append(f"Use one version everywhere: {sorted(versions)}")
if "version" in PACKAGE:
    errors.append("package.json must not have a version field")

block = re.search(r"(?m)^description: \|\n((?:  .*\n)+)", yaml + "\n")
if not block:
    errors.append("Write the SKILL.md description as an indented block")
else:
    description = " ".join(block.group(1).split())
    first = re.match(r"(.+?\.)(\s|$)", description).group(1)
    manifests = {
        "plugin.json": PLUGIN.get("description"),
        "cursor plugin.json": CURSOR.get("description"),
        "package.json": PACKAGE.get("description"),
        **{f"marketplace {p.get('name')}": p.get("description") for p in MARKET.get("plugins", [])},
    }
    for name, value in manifests.items():
        if value != first:
            errors.append(f"{name} description must be the first sentence of SKILL.md: {first!r}")

skills = [p.relative_to(ROOT) for p in ROOT.rglob("SKILL.md")]
if skills != [Path("SKILL.md")]:
    errors.append(f"Keep one SKILL.md at the repo root: {skills}")
if PLUGIN.get("skills") != ["./"]:
    errors.append("Point the Claude plugin skill loader at ./")
if "skills" in CURSOR:
    errors.append("Omit skills from the Cursor plugin")

for ref in sorted(set(re.findall(r"`((?:references|scripts)/[^`\s]+)`", SKILL))):
    if not (ROOT / ref).exists():
        errors.append(f"SKILL.md names a missing file: {ref}")

rules = [int(n) for n in re.findall(r"(?m)^(\d+)\. \*\*", SKILL.split("## 2.", 1)[-1].split("## 3.", 1)[0])]
rules += [int(n) for n in re.findall(r"(?m)^(\d+)\. (?!\*\*)", SKILL.split("### 2.2", 1)[-1].split("### 2.5", 1)[0])]
rules = sorted(set(rules))
if rules != list(range(1, len(rules) + 1)):
    errors.append(f"Number the word rules from 1 without gaps: {rules}")
table = sorted(int(n) for n in re.findall(r"(?m)^\| (\d+) \| ", README))
if table != rules:
    errors.append(f"README rule table {table} must match SKILL.md rules {rules}")

for path in [ROOT / "SKILL.md", *ROOT.glob("references/**/*.md"), ROOT / "README.md"]:
    text = path.read_text(encoding="utf-8")
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    prose = re.sub(r"`[^`]*`", "", prose)
    if re.search(r"[—–]", prose) and path.name != "README.md":
        errors.append(f"{path.relative_to(ROOT)} uses a dash outside code")

words = len(SKILL.split())
if words > 4000:
    errors.append(f"Keep SKILL.md under 4,000 words; it has {words}")

if errors:
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print(f"Humanized Novelist v{version.group(1)} is valid ({words} words in SKILL.md, {len(rules)} word rules)")
