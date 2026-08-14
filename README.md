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

```bash
npx skills add writing-skills      # installs into every detected agent (Claude Code, opencode, Codex, ...)
npm install writing-skills         # or pip/uv: uv add writing-skills
```

`writing-skills` is also an Agent Plugins 1.0.0 package — Claude Code, Codex ≥ 0.147
and Kiro discover `plugin.json` when you point them at the repo:

```bash
git clone https://github.com/surendranb/writing-skills.git
```

## Use

Ask for a style and the skill loads automatically:

> "rewrite this in plain language"
> "make this a BLUF business update"
> "write the press release in AP style"
> "say it like Ted Lasso"

Every framework skill ends with a `Verify` checklist (sentence caps, passive-voice
scans, ban lists, readability targets) the agent must pass before delivering.

## Contribute

Add a skill as a folder under `skills/` with a `SKILL.md`:

- `name` in frontmatter matching the folder; trigger-rich `description` starting with "Use when"
- `## The core rule`, `## Mechanics` (numbered, verifiable), `## Do not`, and at least two before/after `## Transform example`s

## License

MIT — [Surendran B](https://github.com/surendranb). See [LICENSE](LICENSE).