# Guide for agents

How to change Humanized Novelist without breaking it.

## Files

- `SKILL.md` is the prompt agents read on every use. It must stay the only `SKILL.md` in the repo, at the root.
- `references/` holds long material that `SKILL.md` loads on demand. Every file `SKILL.md` names must exist.
- `scripts/` holds Python scripts with no dependencies. They must run on Python 3.9 or newer on Windows, macOS and Linux.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` make the repo a Claude Code plugin and marketplace.
- `.cursor-plugin/plugin.json` describes the Cursor plugin.
- `package.json` makes the repo a pi package. Don't add a `version` field.
- `agents/openai.yaml` holds the display name and default prompt for OpenAI-compatible agents.
- `scripts/validate-package.py` checks all of the above.
- `scripts/build-release.py` builds `dist/humanized-novelist-v<version>.zip`. `.github/workflows/release.yml` runs it on every `v*` tag and publishes the release.

## Rules

- **Priority order.** Words, then story, then craft. A change must not let a craft or story rule reintroduce a word-level tell.
- **Word rules.** Number them from 1 without gaps. Keep the README table in sync; the validator checks it.
- **Version.** Keep one version in `SKILL.md` `metadata.version`, the first `CHANGELOG.md` heading and both plugin manifests.
- **Description.** Every manifest uses the first sentence of the `SKILL.md` description.
- **Length.** `SKILL.md` must stay under 4,000 words. Move detail to `references/`.
- **Style.** The repo's own prose follows its rules: no em dashes, no not-X-but-Y, plain words.
- **Checks.** Run `python3 scripts/validate-package.py` before publishing.
