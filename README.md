<p align="center">
  <img src="logo.svg" alt="writing-skills logo" width="96" />
</p>

# writing-skills

**15 writing-style skills for AI agents: 8 measurable frameworks, 7 character voices.**
Plain `SKILL.md` files. Works in any agent that reads skills
(Claude Code, opencode, Codex, Cursor, Kiro, Gemini).

[![npm](https://img.shields.io/npm/v/writing-skills)](https://www.npmjs.com/package/writing-skills)
[![PyPI](https://img.shields.io/pypi/v/writing-skills)](https://pypi.org/project/writing-skills/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Install

```bash
npx skills add writing-skills
```

One command, every agent on your machine.

<details>
<summary>Other install methods</summary>

| Harness | Command |
| :--- | :--- |
| Claude Code plugin | `/plugin marketplace add surendranb/writing-skills` then `/plugin install writing-skills@writing-skills` |
| Codex ≥ 0.147 / Kiro | `git clone https://github.com/surendranb/writing-skills.git` — `plugin.json` is auto-discovered |
| npm | `npm install writing-skills` |
| Python | `uv add writing-skills` or `pip install writing-skills` |

</details>

## Use

Ask for the style. The skill loads itself.

> "rewrite this in plain language" · "make this a BLUF business update" ·
> "press release in AP style" · "say it like Yoda"

Every skill ends with a `Verify` checklist the agent must pass before it delivers.

### Examples

| You say | Skill that fires | What you get |
| :--- | :--- | :--- |
| "Simplify this insurance letter so anyone can read it" | `plain-language` | Sentences ≤25 words, passive voice stripped, jargon replaced — checked against the Plain Writing Act rules |
| "Turn these notes into an update for my VP" | `business-writing` | BLUF first line, the ask and deadline explicit, buzzwords deleted |
| "Write the release notes for v2.0" | `google-dev-docs` | Active voice, present tense, verb-first headings |
| "Draft the outage announcement" | `corporate-communication` | News in line one, reader impact named, zero euphemism |
| "Make this maintenance manual usable by non-native speakers" | `asd-ste100` | Simplified Technical English: one instruction per sentence, no idioms |
| "Press release for the funding round, AP style" | `journalism-ap` | AP Stylebook attribution and number rules, no editorializing |
| "Explain recursion like Bob Ross" | `bob-ross` | A happy little explanation — calm, encouraging, and technically correct |
| "Rejection email, but make it Paddington" | `paddington` | Firm news delivered with unfailing politeness |

## The skills

### Frameworks — real standards, enforced

| Skill | Enforces |
| :--- | :--- |
| `plain-language` | Plain Writing Act. Sentences ≤25 words, passive ≤10%, jargon ban list. |
| `business-writing` | BLUF first line, explicit ask + deadline, buzzword ban list. |
| `corporate-communication` | News first, reader impact named, zero euphemism. |
| `gov-uk-style` | GOV.UK guide. Keyword-first headings, ≤5-sentence paragraphs. |
| `asd-ste100` | Simplified Technical English. One instruction per sentence, no idioms. |
| `google-dev-docs` | Google style. Active voice, present tense, verb-first headings. |
| `journalism-ap` | AP Stylebook. Attribution, number rules, zero editorializing. |
| `scott-adams` | Simplicity-is-persuasion. Curiosity-hook openers, ≤15-word sentences, prune "very/really". |

### Voices — characters, rate-limited against caricature

`ted-lasso` · `jack-sparrow` · `shrek` · `yoda` · `winnie-the-pooh` · `paddington` · `bob-ross`

## Contribute

Copy [template/SKILL.md](template/SKILL.md), fill it, run
`python3 scripts/validate_skills.py`. CI enforces the contract — see
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — [Surendran B](https://github.com/surendranb)
