# Contributing

Add a skill as a folder under `skills/` with a single `SKILL.md`. Start from
[template/SKILL.md](template/SKILL.md).

## The bar

- **Frameworks** teach a real, citable standard (a style guide, a law, a spec) —
  not personal taste. Verify every rule against the source; getting the standard
  wrong is a bug, not an opinion.
- **Voices** capture a character mechanically: rules that produce the voice and
  rate-limits that prevent caricature.
- Every mechanic must be checkable: a word cap, a ban list, a ratio, a required
  shape. If an agent can't verify it, rewrite it until it can.

## Checklist (CI enforces this — run it yourself first)

```bash
python3 scripts/validate_skills.py
```

- [ ] Folder name matches frontmatter `name`
- [ ] `description` >= 80 chars, contains "Use when" + concrete trigger phrases
- [ ] `## The core rule` — one bolded sentence + a workflow line
- [ ] `## Mechanics` — numbered and verifiable
- [ ] `## Verify` — the pass/fail checklist
- [ ] `## Do not` — the anti-patterns
- [ ] Two or more before/after transform examples
- [ ] <= 120 lines total
- [ ] Added to `.claude-plugin/marketplace.json` skills list

## Style of the skills themselves

Write the skill the way the skill says to write: plain, front-loaded, verifiable.
A wordy skill about concision refutes itself.
