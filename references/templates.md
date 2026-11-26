# Templates

Write file content in the book's language. Headings may stay in English so the scripts can find them.

## 00-outline.md

```markdown
STATUS: AWAITING APPROVAL

# <Book title>

## Settings
- Language:
- Genre and tone:
- Genre pack: none | litrpg-cyberpunk
- POV characters:
- Chapter length: 2,000 to 3,500 words
- Mature content: violence <level>; sex implicit
- Dialogue punctuation: straight double quotes

## Core conflict
What the protagonists want, and what stops them.

## TODO
### To write
- [ ] Chapter 0001: <title> - <core event>
### In progress
### Done
- [x] Chapter 0000: <title> - <core event> (<words> words)

## Chapter table
| Chapter | Title | POV | Core event | Closing hook | Words | Status |
|---|---|---|---|---|---|---|

## Suspense threads
- Main:
- Side:
- Final answer (hidden from readers):

## Totals
- Chapters done: 0
- Words: 0

## Chapter summaries
### Chapter 0001: <title>
150 to 300 words: what happened, what changed, what question is open.
```

When the author approves, replace the first line with `STATUS: APPROVED`.

## 01-characters.md

```markdown
# Characters

## Protagonists
### <Name>
- Age and role:
- Distinctive traits (2 or 3):
- Core value:
- Biggest fear:
- Fatal flaw:
- Inner desire:
- Background:
- Secret:
- Way of speaking:
- Body language:
- Under stress:

## Antagonists
### <Name>
(same fields, plus what they believe they are fighting for)

## Supporting cast
### <Name>
- Role and job in the story:
- Way of speaking:
```

## 02-ledger.md

```markdown
# Continuity ledger

## Current state (after chapter NNNN)
| Character | Location | Wounds and condition | Possessions, implants, money | Knows | Relations |
|---|---|---|---|---|---|

## World rules established
- Rule (chapter where it appeared)

## Planted clues
| Clue | Planted in | Payoff planned | Paid off in |
|---|---|---|---|

## Exceptions the author approved
- Rule bent, chapter, reason
```

## chapters/chapter-NNNN.md

```markdown
# Chapter N: <title>

## Working notes
- Core event:
- Answers the previous hook:
- Closing hook:
- POV:

## Text

Prose only. Every sentence follows section 2 of SKILL.md.

## Notes
- Clues planted:
- Next chapter (1 or 2 lines):
```

The scripts count and scan only the part between `## Text` and `## Notes`.
