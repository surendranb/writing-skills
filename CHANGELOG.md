# Changelog

## 0.3.1 (2026-08-15)

- **Fixed** bundled-catalog fallback on installed wheels: `BUNDLE_ROOT` probing
  now walks both parents (editable-checkout and nested site-packages layouts).
  v0.3.0's fallback only worked from a repo checkout — `uvx` installs broke
  offline discovery.

## 0.3.0 (2026-08-15)

MCP skill registry: unlimited skills, live from GitHub, no re-installs.

- **Added** `writing-skills-mcp` server (`uvx writing-skills-mcp`): tools
  `search_styles` (ranked match over the full catalog),
  `get_skill` (full SKILL.md for shipped skills; catalog-only styles flagged),
  `install_skill` (downloads + writes into a harness skills dir).
- **Added** GitHub-backed discovery: index and skills fetched live from
  `main` — adding a skill is one commit, no package update ever needed for
  users. Bundled package data is the offline fallback.
- **Added** anonymous telemetry client (SUR-86 pattern): `server_first_install` /
  `mcp_started` / `tool_executed`, install id in `~/.writing-skills/`, envoy
  opt-out (`WRITING_SKILLS_TELEMETRY=false`, `DO_NOT_TRACK`), zero PII; only
  active when `WRITING_SKILLS_TELEMETRY_URL` is set. Worker relay + PostHog
  wiring lands next.
- **Added** CI check: `exhaustive-styles.json` shipped flags must match
  `skills/` folders (the discovery index never goes stale).
- **Changed** PyPI package becomes real: console script, `mcp` dependency,
  catalog ships in both npm and PyPI artifacts.

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
