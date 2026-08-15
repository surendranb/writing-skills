# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: S110, BLE001
"""Anonymous usage telemetry: identity, environment signals, and transport to
the gateway. Opt-out and privacy: see README."""

import atexit
import json
import os
import platform
import re
import subprocess
import sys
import threading
import time
import urllib.request
import uuid
from pathlib import Path

from . import __version__

GATEWAY_URL = "https://writing-skills.builditwithai.xyz/e"
SCHEMA_VERSION = 2

STATUS_OK = {"success", "warning", "cancelled"}
STATUS_ERR = {"error", "exception"}
ERROR_CATEGORIES = {
    "APIError", "ValidationError", "SchemaHallucination", "IAMError",
    "TimeoutError", "RateLimitError", "NotFoundError", "SourceUnavailable",
    "MissingApiKey", "InternalError", "Cancelled",
}

MCP_SERVER_VERSION = __version__ or "unknown"


def _telemetry_disabled() -> bool:
    if os.getenv("WRITING_SKILLS_TELEMETRY", "true").lower() in ("false", "0", "off"):
        return True
    for var in ("DISABLE_TELEMETRY", "DO_NOT_TRACK", "NO_TELEMETRY"):
        if os.getenv(var, "").lower() in ("1", "true", "yes", "on"):
            return True
    return False


def _get_home_dir() -> Path:
    return Path(os.environ.get("WRITING_SKILLS_HOME", Path.home() / ".writing-skills")).expanduser()


def _init_anonymous_identity():
    try:
        config_dir = _get_home_dir()
        config_dir.mkdir(parents=True, exist_ok=True)

        id_file = config_dir / "installation_id"
        if id_file.exists():
            installation_id = id_file.read_text(encoding="utf-8").strip()
            is_first_install = False
        else:
            installation_id = uuid.uuid4().hex
            id_file.write_text(installation_id, encoding="utf-8")
            is_first_install = True

        flag_file = config_dir / "installed_v2"
        if not flag_file.exists():
            is_first_install = True
            flag_file.write_text("1", encoding="utf-8")

        return installation_id, is_first_install
    except Exception:
        return uuid.uuid4().hex, False


_install_id: str | None = None


def install_id() -> tuple[str, bool]:
    global _install_id
    if _install_id:
        return _install_id, False
    iid, is_first = _init_anonymous_identity()
    _install_id = iid
    return iid, is_first


SESSION_ID = f"sess_{uuid.uuid4().hex}"

_KNOWN_SOURCES = {
    "readme", "glama", "mcpso", "pulsemcp", "setup",
    "cursor_button", "vscode_button", "installer",
}


def _install_source():
    raw = (os.getenv("WRITING_SKILLS_SOURCE") or "").strip().lower()
    if not raw:
        return None, None
    return raw, (raw if raw in _KNOWN_SOURCES else "other")


_REDACTIONS = [
    (re.compile(r"\bhttps?://\S+"), "<url>"),
    (re.compile(r"(?:file://)?[A-Za-z]:[\\/](?:[^\\/:*?\"<>|\r\n]+[\\/])+[^\\/:*?\"<>|\r\n ]*"), "<path>"),
    (re.compile(r"(?:file://)?/(?:[\w.@()~+-]+/)+[\w.@()~+-]*"), "<path>"),
    (re.compile(r"(?:[\w.@()~+-]+/){2,}[\w.@()~+-]+"), "<path>"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "<email>"),
]


def _scrub(value):
    if isinstance(value, str):
        s = value
        for pattern, replacement in _REDACTIONS:
            s = pattern.sub(replacement, s)
        return s
    if isinstance(value, dict):
        return {k: _scrub(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_scrub(v) for v in value]
    return value


scrub = _scrub


def _normalize_client_name(raw):
    n = (raw or "").strip().lower()
    if not n or n == "unknown":
        return None
    buckets = [
        ("local-agent-mode", "claude_cowork"),
        ("claude-code", "claude_code"),
        ("claude_code", "claude_code"),
        ("claude code", "claude_code"),
        ("claudeai", "claude_desktop"),
        ("claude-ai", "claude_desktop"),
        ("cursor", "cursor"),
        ("gemini", "gemini_cli"),
        ("windsurf", "windsurf"),
        ("opencode", "opencode"),
        ("antigravity", "antigravity"),
        ("vscode", "vscode"),
    ]
    for needle, bucket in buckets:
        if needle in n:
            return bucket
    return "other"


def _detect_run_context() -> str:
    env = os.environ
    if env.get("GITHUB_ACTIONS", "").lower() == "true" or env.get("CI", "").lower() in ("true", "1"):
        return "ci"
    if ("KUBERNETES_SERVICE_HOST" in env or "AWS_EXECUTION_ENV" in env
            or "ECS_CONTAINER_METADATA_URI" in env or os.path.exists("/.dockerenv")):
        return "cloud"
    if "TERM_PROGRAM" in env or "SSH_TTY" in env or "SSH_CONNECTION" in env or sys.stdin.isatty():
        return "terminal"
    return "desktop" if (env.get("__CFBundleIdentifier") or "DISPLAY" in env) else "headless"


def _detect_agent_name() -> str:
    env = os.environ
    if "CLAUDECODE" in env or "CLAUDE_CODE" in env or any(k.startswith("CLAUDE_CODE_") for k in env):
        return "claude_code"
    if any(k in env for k in ("CURSOR_TRACE_ID", "CURSOR_TRACE", "CURSOR_VERSION")):
        return "cursor"
    if "GEMINI_CLI" in env:
        return "gemini_cli"
    if "WINDSURF_VERSION" in env or any(k.startswith("CODEIUM_") for k in env):
        return "windsurf"
    if "ANTIGRAVITY" in env or "AGY_SESSION" in env:
        return "antigravity"
    if "OPENCODE" in env:
        return "opencode"
    return "generic_agent" if not sys.stdin.isatty() else "human_terminal"


def _detect_discovery_channel() -> str:
    src = os.getenv("WRITING_SKILLS_SOURCE")
    if src:
        return src
    argv_str = " ".join(sys.argv).lower()
    if "uvx" in argv_str or "uv" in sys.executable:
        return "uvx"
    if "brew" in sys.executable or "homebrew" in sys.executable:
        return "homebrew"
    if sys.prefix != sys.base_prefix:
        return "pip_venv"
    return "direct_python"


_PENDING_SENDS = []


def _drain_pending_sends(deadline_seconds=2.0):
    end = time.time() + deadline_seconds
    for th in list(_PENDING_SENDS):
        remaining = end - time.time()
        if remaining <= 0:
            break
        try:
            th.join(remaining)
        except Exception:
            pass


atexit.register(_drain_pending_sends)


def send_telemetry(event: str, properties: dict | None = None):
    """Fire-and-forget event to the gateway on a daemon thread."""
    if _telemetry_disabled():
        return

    iid, _ = install_id()
    url = os.environ.get("WRITING_SKILLS_TELEMETRY_URL", GATEWAY_URL)
    src_raw, src = _install_source()
    internal_run = os.getenv("WRITING_SKILLS_INTERNAL", "").lower() in ("1", "true", "yes")

    def _send():
        try:
            props = {
                "schema_version": SCHEMA_VERSION,
                "mcp_server_name": "writing-skills",
                "$os": platform.system(),
                "python_version": platform.python_version(),
                "mcp_server_version": MCP_SERVER_VERSION,
                "cpu_arch": platform.machine(),
                "in_virtual_env": sys.prefix != sys.base_prefix,
                "timezone_offset": -time.timezone if (time.localtime().tm_isdst == 0) else -time.altzone,
                "agent_name": _detect_agent_name(),
                "run_context": _detect_run_context(),
                "discovery_channel": _detect_discovery_channel(),
                "session_id": SESSION_ID,
                **(properties or {}),
            }
            if internal_run:
                props["internal_run"] = True
            if src:
                props.setdefault("install_source", src)
                props.setdefault("install_source_raw", src_raw)

            props = _scrub(props)
            props["$process_person_profile"] = False
            payload = {
                "event": event,
                "distinct_id": iid,
                "properties": props,
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": f"writing-skills/{MCP_SERVER_VERSION}",
                },
            )
            urllib.request.urlopen(req, timeout=3)
        except Exception:
            pass

    th = threading.Thread(target=_send, daemon=True)
    th.start()
    _PENDING_SENDS.append(th)
    if len(_PENDING_SENDS) > 8:
        _PENDING_SENDS[:] = [t for t in _PENDING_SENDS if t.is_alive()]


def event(name: str, **props: object) -> None:
    """Alias for send_telemetry for backward compatibility."""
    send_telemetry(name, props)