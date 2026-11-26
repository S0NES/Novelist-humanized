# Humanized Novelist

[![Check package](https://github.com/S0NES/Novelist-humanized/actions/workflows/validate.yml/badge.svg)](https://github.com/S0NES/Novelist-humanized/actions/workflows/validate.yml)

An agent skill for writing long serialized novels, one chapter at a time, with prose that reads like a person wrote it. It works in Claude, Claude Code, Codex, Cursor and any agent that loads `SKILL.md` skills.

Most AI fiction is easy to spot. Characters answer "You're cruel" with "I'm not cruel, I'm precise." Every scene closes on "And she knew it." Hearts pound, blood runs cold, silences are deafening, and dashes are everywhere. Humanized Novelist writes so those patterns don't appear, then checks the chapter again before saving it.

**Before:**
> It wasn't fear — it was calculation. Kael's heart pounded as a deafening silence filled the corridor, a testament to everything they had lost. "You're reckless," Mira said. "I'm not reckless. I'm decisive." He knew, in that moment, that everything had changed.

**After:**
> Kael counted the doors instead of breathing. Four on the left, three on the right, and the fourth on the left had a fresh scratch near the lock. "You're reckless," Mira said. He was already kneeling at the lock. "Hold the light still."

## What it combines

| Layer | What it controls | Built from |
|---|---|---|
| Words | Every sentence: 19 drafting rules and dialogue rules | [humanizer](https://github.com/blader/humanizer) by Siqi Chen (MIT) |
| Story | POV, one scene per chapter, register changes, exposition, continuity ledger | Story rules by Vinicius Scarabelli |
| Craft | First-20% openings, 10 opening techniques, 10 closing hooks, suspense, outline and summary workflow | chinese-novelist, adapted |

When they conflict, the author's request wins, then the word rules, then the story rules, then craft.

## Features

- Plans a book with you, then writes chapter after chapter without asking again.
- Keeps an outline with a TODO list, a chapter table and a summary for every chapter, so long serials stay consistent.
- Keeps a continuity ledger: locations, wounds, possessions, what each character knows, rules and planted clues.
- Revises each chapter in a second pass against the same rules.
- Works in any language. Notes for Portuguese, Spanish and Chinese are included.
- Runs unattended on a schedule: a planning run stops for your approval, and writing runs continue from where the last one stopped.
- Optional genre pack for LitRPG and cyberpunk (system grammar, costs for every upgrade, no magic words).
- Two scripts with no dependencies: a chapter length counter and a scanner for surface AI tells.

## Installation

### Claude Code

```text
/plugin marketplace add S0NES/Novelist-humanized
/plugin install humanized-novelist@humanized-novelist
```

### Skills CLI (Claude Code, Codex, Cursor, Gemini CLI and others)

```bash
npx skills add S0NES/Novelist-humanized --global --agent '*'
```

Leave off `--global` to install it only in the current project.

### Claude.ai and the Claude desktop app

Download `humanized-novelist-v<version>.zip` from the [latest release](https://github.com/S0NES/Novelist-humanized/releases/latest) and upload it as a skill in Settings.

### MCP Market

Install it from its MCP Market listing, or add the GitHub repo to your MCP Market Hub library.

## Usage

Start a book:

```text
/humanized-novelist start a new novel in novels/glass-city
```

Write the next chapter:

```text
/humanized-novelist write the next chapter of novels/glass-city
```

Write several:

```text
/humanized-novelist write chapters 4 to 6 of novels/glass-city
```

Revise existing chapters:

```text
/humanized-novelist revise novels/glass-city/chapters/chapter-0003.md
```

Clean a pasted passage:

```text
/humanized-novelist humanize this scene: [paste]
```

### Scheduled runs

Point a scheduled task at the project folder with a prompt such as:

```text
Use the humanized-novelist skill on <folder>. If the outline is approved, write the next chapter and revise it. If there is no outline, run unattended planning and stop for approval.
```

The first scheduled run creates `00-outline.md` with `STATUS: AWAITING APPROVAL`. Change that line to `STATUS: APPROVED` and the next run starts writing.

## Project layout

```text
novels/<book>/
  00-outline.md      settings, TODO, chapter table, suspense threads, summaries
  01-characters.md   character sheets
  02-ledger.md       continuity ledger
  world.md           optional world rules
  chapters/chapter-0001.md ...
```

## Scripts

```bash
python scripts/wordcount.py --all novels/glass-city/chapters
python scripts/check_tells.py --all novels/glass-city/chapters
```

`wordcount.py` counts words, or characters for Chinese and Japanese, and flags short chapters. `check_tells.py` lists dashes, separator lines, banned words, stock idioms and common not-X-but-Y shapes in English, Portuguese and Spanish. Both exit with code 2 when they find a problem, so you can use them in CI. The scanner sees only surface patterns; the skill still reads each chapter for rhythm and subtext.

## The word rules

| # | Rule |
|---|---|
| 1 | Not X but Y |
| 2 | One-line closers and dramatic fragments |
| 3 | Sayings that sound deep |
| 4 | Staged run-ups |
| 5 | Arguing with no one |
| 6 | No forced triads |
| 7 | No repeated openings |
| 8 | No em dashes or en dashes |
| 9 | Qualifiers only where the doubt is real |
| 10 | Vary sentence length on purpose |
| 11 | Banned words |
| 12 | No inflated significance |
| 13 | No shallow -ing tails |
| 14 | No sales language |
| 15 | Plain verbs |
| 16 | No adjective piles or abstract emotion |
| 17 | No stock idioms |
| 18 | A chapter file holds only the chapter |
| 19 | Never describe the text |

Plus the dialogue rules in [`references/dialogue.md`](references/dialogue.md), led by the ban on the mirrored rebuttal.

## Limits

This skill edits for human readers. It does not promise to get past AI detectors. A rule list can't replace an author with something to say, so use it to remove the default choices and keep your own.

## Releasing

1. Bump `metadata.version` in `SKILL.md`, both plugin manifests and `CHANGELOG.md`.
2. Run `python scripts/validate-package.py`.
3. Tag and push: `git tag v1.0.1 && git push origin v1.0.1`.

The Release workflow checks the package, builds `dist/humanized-novelist-v<version>.zip` with `scripts/build-release.py`, and publishes a GitHub Release with the zip attached. Build the zip locally with `python scripts/build-release.py`.

## Credits and license

MIT. See [LICENSE](LICENSE) and [CREDITS.md](CREDITS.md).
