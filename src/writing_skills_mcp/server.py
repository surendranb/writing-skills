"""writing-skills MCP server: GitHub-backed skill discovery and install.

The plugin ships skills statically; this server is the live registry on top.
The index is ``exhaustive-styles.json`` on GitHub main — a new skill is just a
commit, so scale (30 or 3500 styles) needs no package update. Network is a
freshness source, not a dependency: bundled package data is the offline
fallback for both the catalog and shipped skills.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from mcp.server.mcpserver import MCPServer

from . import __version__, telemetry

GITHUB_RAW = "https://raw.githubusercontent.com/surendranb/writing-skills/main"
CATALOG_URL = f"{GITHUB_RAW}/exhaustive-styles.json"
SKILL_URL = f"{GITHUB_RAW}/skills/{{slug}}/SKILL.md"
CACHE_TTL = 600.0
BUNDLE_ROOT = Path(__file__).resolve().parents[2]
VALID_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")

_cache: dict[str, tuple[float, str]] = {}


def fetch(url: str) -> str | None:
    now = time.monotonic()
    hit = _cache.get(url)
    if hit and now - hit[0] < CACHE_TTL:
        return hit[1]
    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            text = resp.read().decode()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    _cache[url] = (now, text)
    return text


def _bundled_catalog() -> list[dict] | None:
    try:
        return json.loads((BUNDLE_ROOT / "exhaustive-styles.json").read_text())
    except (OSError, json.JSONDecodeError):
        return None


def catalog() -> list[dict]:
    raw = fetch(CATALOG_URL) or (BUNDLE_ROOT / "exhaustive-styles.json").read_text()
    try:
        entries = json.loads(raw)
    except (json.JSONDecodeError, OSError):
        entries = _bundled_catalog() or []
    return [
        e
        for e in entries
        if isinstance(e, dict) and e.get("slug") and e.get("core")
    ]


def shipped_slugs() -> set[str]:
    return {e["slug"] for e in catalog() if e.get("shipped")}


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _score(query_tokens: set[str], entry: dict) -> float:
    score = 0.0
    for token in query_tokens:
        if token == entry["slug"]:
            score += 5.0
        if token in _tokens(entry["slug"]):
            score += 3.0
        if token in _tokens(entry.get("source", "")):
            score += 2.0
        if token in _tokens(entry.get("core", "")):
            score += 1.0
    return score / max(1, len(query_tokens))


def _skill_markdown(slug: str) -> str | None:
    if ((text := fetch(SKILL_URL.format(slug=slug))) is not None):
        return text
    path = BUNDLE_ROOT / "skills" / slug / "SKILL.md"
    try:
        return path.read_text()
    except OSError:
        return None


def _find_entry(slug: str) -> dict | None:
    return next((e for e in catalog() if e["slug"] == slug), None)


app = MCPServer("writing-skills")


@app.tool()
def search_styles(query: str, limit: int = 10) -> list[dict]:
    """Find writing styles matching a need. Pass a word or phrase (e.g. "plain
    language press release" or "Yoda"); returns ranked candidates with their
    source, one-line core rules, and whether a full skill is shipped. Use the
    returned slug in get_skill or install_skill."""
    try:
        q = _tokens(query)
        hits = sorted(
            catalog(),
            key=lambda e: (_score(q, e), e.get("shipped", False), e["slug"]),
            reverse=True,
        )
        return [
            {
                "slug": e["slug"],
                "source": e["source"],
                "core": e["core"],
                "shipped": bool(e.get("shipped")),
            }
            for e in hits[: max(1, min(limit, 50))]
        ]
    except Exception as exc:  # noqa: BLE001
        return [{"error": str(exc)}]


@app.tool()
def get_skill(slug: str) -> dict:
    """Get a writing skill as markdown. Shipped skills return the full SKILL.md
    (executable instructions + verify checklist); unshipped catalog styles
    return their core rules flagged not_shipped (usable as guidance, not yet
    a full skill)."""
    try:
        if not VALID_SLUG.match(slug):
            return {"slug": slug, "error": "invalid slug"}
        entry = _find_entry(slug)
        if entry is None:
            return {"slug": slug, "error": "unknown style"}
        if not entry.get("shipped"):
            return {
                "slug": slug,
                "shipped": False,
                "source": entry["source"],
                "core": entry["core"],
                "note": "catalog-only — no full skill shipped yet",
            }
        markdown = _skill_markdown(slug)
        if markdown is None:
            return {"slug": slug, "error": "skill content unavailable"}
        return {
            "slug": slug,
            "shipped": True,
            "source": entry["source"],
            "core": entry["core"],
            "skill_markdown": markdown,
        }
    except Exception as exc:  # noqa: BLE001
        return {"slug": slug, "error": str(exc)}


@app.tool()
def install_skill(slug: str, target_dir: str) -> dict:
    """Install a shipped writing skill into a harness skills directory. Pass
    the directory that holds skill folders (e.g. ~/.config/opencode/skills);
    writes <slug>/SKILL.md there so the harness can load it. Catalog-only
    styles are refused — they are not full skills yet."""
    try:
        if not VALID_SLUG.match(slug):
            return {"slug": slug, "error": "invalid slug"}
        entry = _find_entry(slug)
        if entry is None:
            return {"slug": slug, "error": "unknown style"}
        if not entry.get("shipped"):
            return {
                "slug": slug,
                "shipped": False,
                "error": "catalog-only — no full skill shipped yet",
            }
        markdown = _skill_markdown(slug)
        if markdown is None:
            return {"slug": slug, "error": "skill content unavailable"}
        target = Path(target_dir).expanduser() / slug / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(markdown)
        return {
            "slug": slug,
            "installed_to": str(target),
            "bytes": target.stat().st_size,
        }
    except Exception as exc:  # noqa: BLE001
        return {"slug": slug, "error": str(exc)}


def main() -> None:
    distinct_id, is_new = telemetry.install_id()
    if is_new:
        telemetry.event("server_first_install")
    telemetry.event("mcp_started", version=__version__)
    app.run()


if __name__ == "__main__":
    main()