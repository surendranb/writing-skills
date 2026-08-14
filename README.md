<p align="center">
  <img src="logo.svg" alt="Writing Skills Logo" width="120" />
</p>

# Writing Skills 🖋️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/writing-skills)](https://pypi.org/project/writing-skills/)
[![npm](https://img.shields.io/npm/v/writing-skills)](https://www.npmjs.com/package/writing-skills)

**Procedural writing-style skills for AI agents — official frameworks, not vibes.**

Ready-made `SKILL.md` packages: plain language, business writing, corporate
communication, GOV.UK, AP style, STE-100, dev docs — each with numbered mechanics
and a **verifiable checklist** the agent must pass. Compatible with any agent that
reads SKILL.md (opencode, Claude Code, Codex, Kiro, Gemini).

## Skills

### Frameworks

| Skill | What it enforces |
| :--- | :--- |
| `plain-language` | Plain Writing Act clarity. Sentences ≤25 words, passive ≤10%, jargon ban list. |
| `business-writing` | Executive comms. BLUF in the first line, explicit ask + deadline, buzzword ban list. |
| `corporate-communication` | Company announcements. News first, reader impact explicit, zero euphemism. |
| `gov-uk-style` | Public-sector readability. Keyword-first headings, ≤25-word sentences, ≤5-sentence paragraphs. |
| `asd-ste100` | Safety-critical technical prose. One instruction per sentence, controlled vocabulary, no idioms. |
| `google-dev-docs` | Developer documentation. Active voice, present tense, verb-first headings, runnable examples. |
| `journalism-ap` | Factual reporting. AP attribution and number rules, zero editorializing. |

### Voices

`ted-lasso` · `jack-sparrow` · `shrek` · `yoda` · `winnie-the-pooh` · `paddington` · `bob-ross`

## Install

| Harness | Command |
| :--- | :--- |
| **Any agent** (recommended) | `npx skills add writing-skills` — detects and installs into every agent on your machine |
| **Claude Code** (plugin) | `/plugin marketplace add surendranb/writing-skills` then `/plugin install writing-skills@writing-skills` |
| **Codex ≥ 0.147 / Kiro** | `git clone https://github.com/surendranb/writing-skills.git` — `plugin.json` is auto-discovered (Agent Plugins 1.0) |
| **npm** | `npm install writing-skills` |
| **Python** | `uv add writing-skills` or `pip install writing-skills` |

## Use

Ask for a style and the skill loads automatically:

> "rewrite this in plain language"
> "make this a BLUF business update"
> "write the press release in AP style"
> "say it like Ted Lasso"

Every framework skill ends with a `Verify` checklist (sentence caps, passive-voice
scans, ban lists, readability targets) the agent must pass before delivering.

## Contribute

Start from [template/SKILL.md](template/SKILL.md) and see [CONTRIBUTING.md](CONTRIBUTING.md).
Every skill must pass `python3 scripts/validate_skills.py` — frontmatter, verifiable
mechanics, a `Verify` checklist, and two transform examples are enforced by CI.

## License

MIT — [Surendran B](https://github.com/surendranb). See [LICENSE](LICENSE).