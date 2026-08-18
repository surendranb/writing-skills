# AGENTS.md — writing-skills

Repo map and contracts for agents working in this repository.

## What this is

15 writing-style skills as `SKILL.md` files: 8 **frameworks** (measurable
standards with hard checks) and 7 **voices** (character registers with
mechanical rules). Pure text — this repo contains skills and their packaging,
nothing else.

## Layout

```
skills/<name>/SKILL.md      one skill per folder; frontmatter name == folder name
.claude-plugin/             Claude Code marketplace + plugin manifests
plugin.json                 Agent Plugins 1.0 manifest (Codex, Kiro, ...)
package.json / pyproject.toml   npm / PyPI packaging (plugin.json + skills/ only)
template/SKILL.md           skeleton for new skills
scripts/validate_skills.py  the CI gate — run it before any commit
```

## The skill anatomy contract (enforced by CI)

1. Frontmatter: `name` matching the folder; `description` >= 80 chars containing
   "Use when" with concrete trigger phrases.
2. `## The core rule` — one bolded sentence that IS the skill, plus a workflow line.
3. `## Mechanics` — numbered, each one verifiable (a cap, a ban list, a ratio).
4. `## Verify` — the checklist an agent must pass before delivering.
5. `## Do not` — the anti-patterns.
6. At least two before/after transform examples.
7. Total length <= 120 lines.

Framework skills must cite the real standard and match it — verify rules
against the source, not memory. Fidelity errors are bugs.

## Working here

- Validate after any change: `python3 scripts/validate_skills.py`
- New skill: copy `template/SKILL.md` into `skills/<name>/`, fill it, add the
  path to `.claude-plugin/marketplace.json`, validate.
- Keep this repo skills-only: no servers, no scripts beyond the validator,
  no config that runs anything on install.

## Releases

Every skill addition or plugin improvement = a release: bump the version in
plugin.json, .claude-plugin/plugin.json, .claude-plugin/marketplace.json
(metadata.version), package.json, pyproject.toml (CI fails on mismatch);
add a CHANGELOG entry; tag vX.Y.Z + GitHub release; `npm publish` manually.
