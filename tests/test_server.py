"""Unittest smoke for the writing-skills MCP server (stdlib only).

Run: python3 -m unittest discover -s tests -v
"""

import http.server
import json
import os
import tempfile
import threading
import unittest
import urllib.error
from pathlib import Path

from writing_skills_mcp import server, telemetry

CATALOG = json.dumps(
    [
        {
            "slug": "plain-language",
            "source": "US Plain Writing Act + PLAIN",
            "core": "front-load; <=25-word sentences; passive <=10%; jargon ban",
            "shipped": True,
        },
        {
            "slug": "hemingway-iceberg",
            "source": "Hemingway",
            "core": "sentences under 12 words, declarative",
            "shipped": False,
        },
    ]
)

SKILL_MD = "---\nname: plain-language\n---\n\n## The core rule\nWrite plainly.\n"


class FakeCatalog(unittest.TestCase):
    def setUp(self):
        server._cache.clear()
        self.dir = tempfile.TemporaryDirectory()
        root = Path(self.dir.name)
        (root / "skills" / "plain-language").mkdir(parents=True)
        (root / "skills" / "plain-language" / "SKILL.md").write_text(SKILL_MD)
        (root / "exhaustive-styles.json").write_text(CATALOG)
        self.old_bundle = server.BUNDLE_ROOT
        server.BUNDLE_ROOT = root

        def fake_fetch(url):
            if url == server.CATALOG_URL:
                return CATALOG
            if url == server.SKILL_URL.format(slug="plain-language"):
                return SKILL_MD
            return None

        self.old_fetch = server.fetch
        server.fetch = fake_fetch

    def tearDown(self):
        server.BUNDLE_ROOT = self.old_bundle
        server.fetch = self.old_fetch
        self.dir.cleanup()

    def test_search_ranks_shipped_first(self):
        hits = server.search_styles("plain language", limit=10)
        self.assertEqual(hits[0]["slug"], "plain-language")
        self.assertTrue(hits[0]["shipped"])
        self.assertEqual(hits[1]["slug"], "hemingway-iceberg")
        self.assertFalse(hits[1]["shipped"])

    def test_get_shipped_returns_markdown(self):
        out = server.get_skill("plain-language")
        self.assertTrue(out["shipped"])
        self.assertIn("## The core rule", out["skill_markdown"])

    def test_get_unshipped_flagged(self):
        out = server.get_skill("hemingway-iceberg")
        self.assertFalse(out["shipped"])
        self.assertIn("catalog-only", out["note"])

    def test_get_unknown(self):
        self.assertIn("error", server.get_skill("nope"))

    def test_get_invalid_slug(self):
        self.assertIn("error", server.get_skill("../evil"))

    def test_install_writes_skill(self):
        target = Path(self.dir.name) / "harness-skills"
        out = server.install_skill("plain-language", str(target))
        self.assertIn("installed_to", out)
        path = target / "plain-language" / "SKILL.md"
        self.assertEqual(path.read_text(), SKILL_MD)
        self.assertTrue(path.stat().st_size > 0)

    def test_install_refuses_unshipped(self):
        out = server.install_skill("hemingway-iceberg", str(self.dir.name))
        self.assertIn("catalog-only", out["error"])

    def test_bundled_fallback_offline(self):
        server.fetch = lambda url: None
        out = server.get_skill("plain-language")
        self.assertTrue(out["shipped"])

    def test_bundle_root_probe_nested_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site_packages = root / "lib" / "python3.12" / "site-packages"
            site_packages.mkdir(parents=True)
            (site_packages / "exhaustive-styles.json").write_text("[]")
            pkg_file = site_packages / "writing_skills_mcp" / "server.py"
            self.assertEqual(server._find_bundle_root(pkg_file), site_packages)

    def test_bundle_root_probe_editable_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pkg = root / "src" / "writing_skills_mcp"
            pkg.mkdir(parents=True)
            (root / "exhaustive-styles.json").write_text("[]")
            pkg_file = pkg / "server.py"
            self.assertEqual(server._find_bundle_root(pkg_file), root)


@unittest.skipUnless(
    os.environ.get("WRITING_SKILLS_LIVE") == "1",
    "set WRITING_SKILLS_LIVE=1 for live GitHub smoke",
)
class LiveGitHub(unittest.TestCase):
    def test_search_hits_live_catalog(self):
        hits = server.search_styles("GOV.UK plain English", limit=5)
        self.assertTrue(hits)
        self.assertTrue(any(h["shipped"] for h in hits))

    def test_get_live_shipped_skill(self):
        out = server.get_skill("gov-uk-style")
        self.assertTrue(out["shipped"])
        self.assertIn("The core rule", out["skill_markdown"])


class TelemetryTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        telemetry._install_id = None
        self.requests = []

        class CaptureHandler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(
                    self.rfile.read(int(self.headers["Content-Length"]))
                )
                self.server.requests.append(body)
                self.send_response(200)
                self.end_headers()

            def log_message(self, *args):
                pass

        self.httpd = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), CaptureHandler
        )
        self.httpd.requests = self.requests
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.old = {k: os.environ.get(k) for k in (
            "WRITING_SKILLS_TELEMETRY_URL", "WRITING_SKILLS_HOME",
            "WRITING_SKILLS_SOURCE", "WRITING_SKILLS_TELEMETRY",
            "DO_NOT_TRACK", "NO_TELEMETRY")}
        os.environ["WRITING_SKILLS_TELEMETRY_URL"] = (
            f"http://127.0.0.1:{self.httpd.server_port}/capture"
        )
        os.environ["WRITING_SKILLS_HOME"] = str(Path(self.dir.name) / "home")
        os.environ["WRITING_SKILLS_SOURCE"] = "uvx"
        for k in ("WRITING_SKILLS_TELEMETRY", "DO_NOT_TRACK", "NO_TELEMETRY"):
            os.environ.pop(k, None)

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        for k, v in self.old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        telemetry._install_id = None
        self.dir.cleanup()

    def test_event_posts_and_creates_install_id(self):
        telemetry.event("server_first_install")
        telemetry.event("mcp_started")
        deadline = threading.Event()
        deadline.wait(0.5)
        self.assertEqual(len(self.requests), 2)
        for req in self.requests:
            self.assertEqual(req["distinct_id"], req["distinct_id"])
            self.assertEqual(req["properties"]["discovery_channel"], "uvx")
        self.assertTrue(len(self.requests[0]["distinct_id"]) == 32)
        id_file = Path(self.dir.name) / "home" / "installation_id"
        self.assertEqual(id_file.read_text(), self.requests[0]["distinct_id"])

    def test_optout_silent(self):
        os.environ["WRITING_SKILLS_TELEMETRY"] = "false"
        telemetry._install_id = None
        telemetry.event("mcp_started")
        self.assertEqual(self.requests, [])
        id_file = Path(self.dir.name) / "home" / "installation_id"
        self.assertFalse(id_file.exists())


if __name__ == "__main__":
    unittest.main()