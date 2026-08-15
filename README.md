<p align="center">
  <img src="logo.svg" alt="writing-skills logo" width="96" />
</p>

# writing-skills

**14 writing-style skills for AI agents: 7 measurable frameworks, 7 character voices.**
Plain `SKILL.md` files — no code, no server. Works in any agent that reads skills
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

### Voices — characters, rate-limited against caricature

`ted-lasso` · `jack-sparrow` · `shrek` · `yoda` · `winnie-the-pooh` · `paddington` · `bob-ross`

## MCP server — unlimited skills, live from GitHub

```bash
uvx writing-skills-mcp
```

The plugin ships 14 skills statically. The MCP server is the living registry
on top: it discovers styles from the full catalog on GitHub (`search_styles`),
returns any skill's full `SKILL.md` (`get_skill`), and installs it into a
harness skills directory (`install_skill`). A new skill is just a commit —
no package update, no re-install, at any scale.

```bash
uvx --from writing-skills writing-skills-mcp
```

## Contribute

Copy [template/SKILL.md](template/SKILL.md), fill it, run
`python3 scripts/validate_skills.py`. CI enforces the contract — see
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — [Surendran B](https://github.com/surendranb)
