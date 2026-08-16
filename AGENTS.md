# AGENTS.md — Codebase Operational Guide for AI Agents

> **Context, architecture, file map, and execution commands for AI coding agents (Claude Code, Cursor, Codex, Gemini, Antigravity, OpenCode, Aider) working on `writing-style-skills`.**

---

## 1. Codebase Overview

- **Language & Runtime**: Python 3.10+ (`mcp` FastMCP) + Markdown Skills Catalog + NPM distribution wrapper.
- **Package Name**: `writing-skills` (PyPI) / `writing-skills` (NPM).
- **Core Function**: Serves 14 production writing-style skills (7 measurable frameworks + 7 character voices) to AI agents via dynamic MCP tools (`search_styles`, `get_skill`, `install_skill`, `skill_read`) and the Skills CLI.

---

## 2. Directory & File Map

```
writing-style-skills/
├── src/writing_skills_mcp/
│   ├── server.py              # FastMCP server, tool implementations (get_skill, install_skill, search_styles)
│   └── telemetry.py           # Edge Schema v2 telemetry client
├── skills/                    # 14 Production SKILL.md procedural playbooks
│   ├── plain-language/SKILL.md         # Federal plain language guidelines (8th-grade reading level)
│   ├── business-writing/SKILL.md       # BLUF (Bottom Line Up Front) executive memos
│   ├── corporate-communication/SKILL.md# Stakeholder comms, change management, crisis memos
│   ├── gov-uk-style/SKILL.md           # GOV.UK style manual standards
│   ├── asd-ste100/SKILL.md             # Simplified Technical English standard
│   ├── google-dev-docs/SKILL.md        # Google Developer Documentation style guide
│   ├── journalism-ap/SKILL.md          # Associated Press inverted pyramid journalism
│   ├── ted-lasso/SKILL.md              # Relentless optimism & folksy Midwestern analogies
│   ├── jack-sparrow/SKILL.md           # Flamboyant pirate cadence & witty redirection
│   ├── shrek/SKILL.md                  # Grumpy swamp ogre with heart of gold
│   ├── yoda/SKILL.md                   # Inverted OSV syntax & profound Jedi wisdom
│   ├── winnie-the-pooh/SKILL.md        # Gentle, thoughtful, honey-loving prose
│   ├── paddington/SKILL.md             # Polite British bear manners & marmalade notes
│   └── bob-ross/SKILL.md               # Calming, encouraging painting analogies ("happy accidents")
├── scripts/
│   └── validate_skills.py     # Linter & validator verifying frontmatter, headers, and rules across all skills
├── exhaustive-styles.json     # Comprehensive catalog of writing styles and personas
├── pyproject.toml             # Python packaging metadata (writing-skills)
├── package.json               # NPM packaging metadata (writing-skills)
├── smithery.yaml              # Smithery.ai marketplace configuration
├── server.json                # Official MCP registry specification
├── gemini-extension.json      # Google Gemini / Antigravity extension manifest
├── .claude-plugin/            # Claude Code plugin manifests (plugin.json, marketplace.json)
└── .well-known/ai-plugin.json # OpenAI / ChatGPT Actions manifest
```

---

## 3. Development & Testing Commands

```bash
# Install dependencies in editable mode
uv sync || pip install -e ".[dev]"

# Run the MCP server locally in stdio mode
uv run python -m writing_skills_mcp.server

# Validate and lint all SKILL.md files
python3 scripts/validate_skills.py

# Run the test suite
uv run pytest tests/ -v
```

---

## 4. Skill Authoring Invariants & Gotchas

1. **SKILL.md Standard Structure**:
   - Every skill inside `skills/<slug>/SKILL.md` MUST contain:
     - YAML frontmatter with `name`, `description`, `version`, `author`, `tags`.
     - `# Context & Purpose`
     - `# Core Principles & Rules` (with exact measurable rules).
     - `# Examples` (Before vs. After).
     - `# Verification Checklist` (Self-auditing criteria for the agent).
2. **Validation Script (`scripts/validate_skills.py`)**:
   - Always run `python3 scripts/validate_skills.py` after creating or editing any `SKILL.md`. CI enforces 100% passing validation before publishing.
3. **Workspace Skill Installation (`install_skill`)**:
   - `install_skill(style_name)` writes the procedural markdown file directly into the target agent harness directory (e.g. `~/.config/opencode/skills/` or `.gemini/skills/`).
