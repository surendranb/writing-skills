#!/usr/bin/env python3
"""Validate every skill and manifest in this repo. Run: python3 scripts/validate_skills.py

Checks (CI runs this on every push/PR):
  - each skills/*/SKILL.md has parseable frontmatter with name + description
  - frontmatter name matches its folder name
  - description is trigger-rich: >= 80 chars and contains "Use when"
  - required sections present: The core rule, Mechanics, Verify, Do not,
    and at least two before/after transform examples
  - skill body stays context-tight (<= 120 lines)
  - plugin.json, .claude-plugin/plugin.json, .claude-plugin/marketplace.json
    parse, agree on version, and the marketplace skill list matches skills/
  - package.json and pyproject.toml versions match plugin.json
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
errors = []


def err(msg):
    errors.append(msg)


def frontmatter(text, path):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(f"{path}: missing frontmatter")
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


skill_dirs = sorted(d for d in (ROOT / "skills").iterdir() if d.is_dir())
for d in skill_dirs:
    path = d / "SKILL.md"
    if not path.exists():
        err(f"{d.name}: no SKILL.md")
        continue
    text = path.read_text()
    rel = f"skills/{d.name}/SKILL.md"

    fm = frontmatter(text, rel)
    if fm.get("name") != d.name:
        err(f"{rel}: frontmatter name '{fm.get('name')}' != folder '{d.name}'")
    desc = fm.get("description", "")
    if len(desc) < 80:
        err(f"{rel}: description too short ({len(desc)} chars, need >= 80)")
    if "Use when" not in desc:
        err(f"{rel}: description must contain 'Use when' trigger phrasing")

    for section in ["## The core rule", "## Mechanics", "## Verify", "## Do not"]:
        if section not in text:
            err(f"{rel}: missing section '{section}'")
    transforms = len(re.findall(r"\*\*(Before|Neutral)[:*]", text))
    if transforms < 2:
        err(f"{rel}: needs >= 2 transform examples, found {transforms}")
    lines = len(text.splitlines())
    if lines > 120:
        err(f"{rel}: {lines} lines — keep skills <= 120 lines (context economy)")

# Manifests parse and agree
manifests = {}
for f in ["plugin.json", ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
          "package.json"]:
    try:
        manifests[f] = json.loads((ROOT / f).read_text())
    except Exception as e:
        err(f"{f}: does not parse — {e}")

versions = {
    "plugin.json": manifests.get("plugin.json", {}).get("version"),
    ".claude-plugin/plugin.json": manifests.get(".claude-plugin/plugin.json", {}).get("version"),
    ".claude-plugin/marketplace.json": manifests.get(
        ".claude-plugin/marketplace.json", {}).get("metadata", {}).get("version"),
    "package.json": manifests.get("package.json", {}).get("version"),
}
pyproject = (ROOT / "pyproject.toml").read_text()
m = re.search(r'^version = "([^"]+)"', pyproject, re.M)
versions["pyproject.toml"] = m.group(1) if m else None
if len(set(versions.values())) != 1:
    err(f"version mismatch across manifests: {versions}")

mp = manifests.get(".claude-plugin/marketplace.json", {})
listed = {Path(s).name for p in mp.get("plugins", []) for s in p.get("skills", [])}
actual = {d.name for d in skill_dirs}
if listed and listed != actual:
    err(f"marketplace.json skills out of sync: missing {actual - listed}, stale {listed - actual}")

catalog_path = ROOT / "exhaustive-styles.json"
if catalog_path.exists():
    try:
        catalog = json.loads(catalog_path.read_text())
        shipped = {e["slug"] for e in catalog if isinstance(e, dict) and e.get("shipped")}
        if shipped != actual:
            err(f"exhaustive-styles.json shipped out of sync: "
                f"missing {actual - shipped}, stale {shipped - actual}")
    except json.JSONDecodeError:
        err("exhaustive-styles.json does not parse")

if errors:
    print(f"FAIL — {len(errors)} problem(s):")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
print(f"OK — {len(skill_dirs)} skills valid, manifests in sync (version {versions['plugin.json']})")
