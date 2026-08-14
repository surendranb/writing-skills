# AGENTS.md — writing-skills

Repo map and contracts for agents working in this repository.

## What this is

14 writing-style skills as `SKILL.md` files: 7 **frameworks** (measurable standards
with hard checks) and 7 **voices** (character registers with mechanical rules).
Pure text — no code ships in the packages. The skills work in any harness that
reads SKILL.md.

## Layout

```
skills/<name>/SKILL.md      one skill per folder; frontmatter name == folder name
.claude-plugin/             Claude Code marketplace + plugin manifests
plugin.json                 Agent Plugins 1.0 manifest (Codex, Kiro, ...)
package.json / pyproject.toml   npm / PyPI packaging (files: plugin.json + skills/)
template/SKILL.md           skeleton for new skills
scripts/validate_skills.py  the CI gate — run it before any commit
```

## The skill anatomy contract (enforced by CI)

Every SKILL.md must have:

1. Frontmatter: `name` matching the folder; `description` >= 80 chars containing
   "Use when" with concrete trigger phrases.
2. `## The core rule` — one bolded sentence that IS the skill, plus a workflow line.
3. `## Mechanics` — numbered, each one verifiable (a cap, a ban list, a ratio —
   never a vibe).
4. `## Verify` — the checklist an agent must pass before delivering.
5. `## Do not` — the anti-patterns.
6. At least two `**Before:**/**After:**` (or `**Neutral:**/**Voice:**`) transforms.
7. Total length <= 120 lines. Skills load into context; economy is a feature.

## Working here

- Validate after any change: `python3 scripts/validate_skills.py`
- New skill: copy `template/SKILL.md` into `skills/<name>/`, fill it, add the
  path to `.claude-plugin/marketplace.json`, validate.
- Framework skills must cite the real standard (AP Stylebook, GOV.UK style guide,
  ASD-STE100, Plain Writing Act) — verify rules against the source, not memory.
  Fidelity errors are bugs.
- Voice skills: mechanics must prevent caricature (rate-limit the tics — see
  yoda's "every 3rd sentence" or jack-sparrow's "savvy? once, max").

## Releases

Every skill addition or plugin improvement = a release:

1. Bump the version in **all** of: `plugin.json`, `.claude-plugin/plugin.json`,
   `.claude-plugin/marketplace.json` (metadata.version), `package.json`,
   `pyproject.toml` (CI fails on mismatch).
2. Add a CHANGELOG.md entry.
3. Tag `vX.Y.Z` + GitHub release → PyPI publishes via trusted publishing
   (release.yml). npm: `npm publish` (manual).
