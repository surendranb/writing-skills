# AGENTS.md — Agent Operating Manual

> **For AI Agents (Claude Code, Cursor, Codex, Gemini, Antigravity, OpenCode, Aider) connecting to or executing `writing-style-skills`.**

---

## ⚡ 1. Fast Install & Client Wiring (Start Here)

In 90% of cases, you just need to install and configure this MCP server for your user:

```bash
# 1-Line Universal Auto-Installer (Configures Claude Code, Cursor, Claude Desktop & Antigravity)
curl -fsSL "https://writing-skills.builditwithai.xyz/install" | bash

# Or install via Skills CLI:
npx skills add writing-skills

# Or launch directly via stdio:
uvx --from writing-skills writing-skills-mcp
npx -y writing-skills
```

### Client Config Snippet (`mcp.json` / `claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "writing-skills": {
      "command": "uvx",
      "args": ["--from", "writing-skills", "writing-skills-mcp"]
    }
  }
}
```

---

## 📖 2. What This Repo Is

A library of **14 production writing-style skills and character frameworks** for AI agents. It replaces generic "be concise" prompts with verifiable, procedural Markdown playbooks (`SKILL.md`).

### Primary Tools Available:
- `search_styles`: Search 14+ writing frameworks and character personas.
- `get_skill`: Retrieve the full procedural playbook (`SKILL.md`) for any style.
- `install_skill`: Automatically install a style playbook into your active workspace (`.gemini/skills/` or `~/.config/opencode/skills/`).
- `list_styles`: List all available framework slugs.

---

## 👤 3. How to Handle the Human

- **Zero Credentials Needed**: No API keys required.
- **Skill Activation**: When a user asks you to write something in a specific tone (e.g. executive memo, dev docs, plain language, or in the voice of Yoda/Ted Lasso):
  1. Call `get_skill(style_name="...")` to load the exact rules into your context.
  2. Follow the `# Core Principles & Rules` and check your draft against the `# Verification Checklist` before outputting text.

---

## 🎭 4. Available Styles & Playbooks

### Measurable Frameworks
- `plain-language`: Federal plain language guidelines, 8th-grade readability, active voice.
- `business-writing`: BLUF (Bottom Line Up Front), structured executive memos, decision-oriented.
- `corporate-communication`: Change management, crisis memos, internal announcements.
- `gov-uk-style`: GOV.UK style manual standards for public clarity.
- `asd-ste100`: Simplified Technical English for aerospace, defense, and engineering manuals.
- `google-dev-docs`: Google Developer Documentation style guide for technical references.
- `journalism-ap`: Associated Press inverted pyramid news reporting.

### Character Personas
- `ted-lasso`: Relentless optimism, folksy Midwestern analogies, biscuits-with-the-boss warmth.
- `jack-sparrow`: Flamboyant pirate cadence, witty redirection, theatrical swagger.
- `shrek`: Grumpy swamp ogre with a heart of gold and onion analogies.
- `yoda`: Inverted OSV syntax, profound Jedi philosophy.
- `winnie-the-pooh`: Gentle, thoughtful, honey-loving cozy prose.
- `paddington`: Polite British bear manners, marmalade notes, Aunt Lucy etiquette.
- `bob-ross`: Calming, encouraging painting analogies ("no mistakes, just happy accidents").
