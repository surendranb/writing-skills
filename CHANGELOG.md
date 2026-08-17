# Changelog

## 0.4.0 (2026-08-17)

- The MCP server and registry manifests moved to their own project,
  [writing-skills-mcp](https://github.com/surendranb/writing-skills-mcp).
- The Claude Code plugin manifest no longer configures a server.
- npm and PyPI packages contain `plugin.json` and `skills/` only.

## 0.3.0 – 0.3.5 (2026-08-15)

- Added an MCP server and registry manifests (moved to their own project in
  0.4.0 — see [writing-skills-mcp](https://github.com/surendranb/writing-skills-mcp)).

## 0.2.0 (2026-08-14)

World-class pass: discovery, correctness, and contribution infrastructure.

- **Fixed** two AP Stylebook fidelity errors in `journalism-ap`: percentages now
  use the % symbol with figures (AP adopted it in 2019; the skill taught the
  pre-2019 spelled-out rule), and the never-abbreviated months list is now
  complete (March, April, May, June, July — was missing March and April).
- **Added** `## Verify` checklists to all 7 voice skills — every skill in the
  repo now ends with a mechanical pass/fail gate, not just the frameworks.
- **Added** Claude Code discovery: `.claude-plugin/marketplace.json` +
  `.claude-plugin/plugin.json`. Install with
  `/plugin marketplace add surendranb/writing-skills`.
- **Added** CI validation (`scripts/validate_skills.py` + workflow): frontmatter,
  required sections, transform counts, line caps, manifest version sync, and
  marketplace/skills-folder sync — enforced on every push and PR.
- **Added** PyPI release workflow (trusted publishing, no tokens).
- **Added** AGENTS.md (agent-facing repo contract), CONTRIBUTING.md, and
  `template/SKILL.md`.
- **Changed** README: per-harness install matrix.

## 0.1.1 (2026-08)

Initial published state: 14 skills (7 frameworks, 7 voices), Agent Plugins 1.0
manifest, npm package.
