# Writing Skills for AI Agents ✍️

> **14 production writing-style skills and character frameworks for AI agents (Claude Code, Cursor, Codex, Gemini) with dynamic GitHub skill loading.**

[![PyPI version](https://img.shields.io/pypi/v/writing-skills?label=PyPI&color=blue)](https://pypi.org/project/writing-skills/)
[![PyPI downloads](https://img.shields.io/pypi/dm/writing-skills?label=PyPI%20downloads&color=blue)](https://pypi.org/project/writing-skills/)
[![npm version](https://img.shields.io/npm/v/writing-skills?label=npm&color=red)](https://www.npmjs.com/package/writing-skills)
[![npm downloads](https://img.shields.io/npm/dm/writing-skills?label=npm%20downloads&color=red)](https://www.npmjs.com/package/writing-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/Docs-writing--skills.builditwithai.xyz-purple)](https://writing-skills.builditwithai.xyz)

🌐 **Live Documentation & Web Portal**: [https://writing-skills.builditwithai.xyz](https://writing-skills.builditwithai.xyz)

---

## ⚡ Quickstart

```bash
# 1-Line Universal Installer (Auto-configures Claude Code, Cursor, Claude Desktop & Antigravity)
curl -fsSL "https://writing-skills.builditwithai.xyz/install" | bash

# Or install via skills CLI:
npx skills add writing-skills

# Or run directly via your preferred runtime:
uvx --from writing-skills writing-skills-mcp
npx -y writing-skills
```

---

## 🤖 Client Setup

### A. Claude Code (CLI)
```bash
claude mcp add writing-skills -- uvx --from writing-skills writing-skills-mcp
```

### B. Cursor & Google Antigravity (`mcp.json`)
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

### C. Claude Desktop (`claude_desktop_config.json`)
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

## 🛠️ Tools & Capabilities

| Tool Name | Parameters | Description | Return Type |
|---|---|---|---|
| `search_styles` | `query` (string) | Searches 14+ writing frameworks and character personas. | `JSON` |
| `get_skill` | `style_name` (string) | Retrieves the full procedural markdown playbook (`SKILL.md`) for any style. | `Markdown` |
| `install_skill` | `style_name` (string) | Automatically installs a style playbook into the agent's active workspace. | `JSON` |
| `list_styles` | *(none)* | Lists all available styles and frameworks. | `JSON` |
| `skill_read` | `skill_name` (string) | Loads style playbooks dynamically from GitHub. | `Markdown` |
| `skills_list` | *(none)* | Lists all available skills. | `JSON` |

---

## 🎭 Included Writing Styles

### A. Measurable Frameworks
1. **`plain-language`**: Federal plain language guidelines, 8th-grade readability, active voice.
2. **`technical-concise`**: Minimalist documentation, zero fluff, high signal-to-noise ratio.
3. **`executive-brief`**: BLUF (Bottom Line Up Front), structured bullet points, decision-oriented.
4. **`academic-rigorous`**: Factual precision, hedged claims, structured methodology tone.
5. **`storytelling-narrative`**: Pacing, tension-resolution arcs, relatable analogies.
6. **`persuasive-copy`**: Problem-agitation-solution, benefit-driven value propositions.
7. **`conversational-friendly`**: Approachable, warm, clear explanations for complex ideas.

### B. Character Personas
1. **`ponytail`**: Lazy senior developer mode (YAGNI, shortest diff, zero boilerplate).
2. **`surendran-voice`**: Pragmatic, authentic, conversational engineering voice.
3. **`socratic-tutor`**: Guides thinking with probing questions rather than dumping answers.
4. **`curt-reviewer`**: Direct, surgical code and PR review feedback.
5. **`patient-explainer`**: Step-by-step breakdown of difficult technical concepts.
6. **`architect-strategist`**: Big-picture systems thinking and trade-off analysis.
7. **`documentation-craftsman`**: Meticulous, beautifully formatted reference documentation.

---

## 🔒 Telemetry & Privacy

This package collects anonymous, non-PII diagnostic telemetry (command executions, latency, error codes) to improve tool reliability. No written text, draft content, personal data, source code, or environment variables are ever collected or stored.

You can opt out anytime by setting either of the following environment variables:
```bash
export DO_NOT_TRACK=1
# or
export MCP_TELEMETRY_OPT_OUT=1
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
