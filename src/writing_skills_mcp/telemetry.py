"""Anonymous usage telemetry (SUR-86 pattern).

Ships disabled-by-default unless the relay gateway is reachable; opt-out via
WRITING_SKILLS_TELEMETRY=false / DO_NOT_TRACK / NO_TELEMETRY. Zero PII:
install id is a random UUID, no paths, no payload content.
"""

from __future__ import annotations

import json
import os
import threading
import urllib.request
import uuid
from pathlib import Path

from . import __version__

OPTOUT_ENVS = ("WRITING_SKILLS_TELEMETRY", "DO_NOT_TRACK", "NO_TELEMETRY")

# Cloudflare relay (SUR-88) that forwards to PostHog; env overrides for
# self-hosting or local verification.
GATEWAY_URL = "https://writing-skills.builditwithai.xyz/e"
AGENT_ENVS = (
    ("claude_code", ("CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE")),
    ("cursor", ("CURSOR_TRACE_ID",)),
    ("windsurf", ("WINDSURF",)),
    ("opencode", ("OPENCODE",)),
    ("gemini_cli", ("GEMINI_CLI",)),
)

_install_id: str | None = None


def telemetry_url() -> str:
    return os.environ.get("WRITING_SKILLS_TELEMETRY_URL") or GATEWAY_URL


def opted_out() -> bool:
    for name in OPTOUT_ENVS:
        if os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "false"):
            return True
    return False


def _id_dir() -> Path:
    return Path(os.environ.get("WRITING_SKILLS_HOME", "~/.writing-skills")).expanduser()


def install_id() -> tuple[str, bool]:
    global _install_id
    if _install_id:
        return _install_id, False
    id_file = _id_dir() / "installation_id"
    if id_file.exists():
        _install_id = id_file.read_text().strip()
        return _install_id, False
    if opted_out():
        return uuid.uuid4().hex, True
    _install_id = uuid.uuid4().hex
    _id_dir().mkdir(parents=True, exist_ok=True)
    id_file.write_text(_install_id)
    return _install_id, True


def agent_name() -> str | None:
    for name, envs in AGENT_ENVS:
        if any(os.environ.get(e) for e in envs):
            return name
    return None


def _enrich(props: dict) -> dict:
    agent = agent_name()
    out = {
        "mcp_server_name": "writing-skills-mcp",
        "actor_type": "ai_agent" if agent else "unknown",
        "agent_name": agent or "unknown",
        "discovery_channel": os.environ.get("WRITING_SKILLS_SOURCE", "unknown"),
    }
    out.update(props)
    return out


def event(name: str, **props: object) -> None:
    if opted_out():
        return
    url = telemetry_url()
    distinct_id, _ = install_id()
    payload = {
        "event": name,
        "distinct_id": distinct_id,
        "properties": {
            "$process_person_profile": False,  # no PostHog person profiles
            **_enrich(props),
        },
    }

    def post() -> None:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                # Product UA: default library UAs are rejected at the edge
                "User-Agent": f"writing-skills-mcp/{__version__}",
            },
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=3)
        except Exception:
            pass

    threading.Thread(target=post, daemon=True).start()