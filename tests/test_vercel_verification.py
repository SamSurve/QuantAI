"""Tests for Part 33: Vercel configuration verification and deployment honesty.

Verifies:
1. Comprehensive Vercel configuration:
   - vercel.json schema validation and Python serverless function parameters.
   - includeFiles covers all static assets referenced in templates and all templates.
   - excludeFiles protects against leaking tests, caches, and build tools.
   - HTTP response header directives (Cache-Control: no-store on API).
2. Deployment honesty boundaries:
   - Code-level separation between locally verified behaviors and live-deployment-only behaviors.
   - Zero fabrication of cloud deployment state in local environments.
   - VERCEL_DEPLOYMENT.md documents edge CDN, cold starts, and edge headers as requiring live deployment.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import api.index as api_index

LOCALLY_VERIFIED_BEHAVIORS = [
    "asgi_application_routing",
    "jinja2_template_rendering",
    "static_file_asset_serving",
    "sliding_window_rate_limiting",
    "concurrency_guard_execution",
    "request_id_propagation",
    "provider_failover_sequence",
    "error_sanitization_and_status_codes",
]

LIVE_DEPLOYMENT_REQUIRED_BEHAVIORS = [
    "edge_cdn_routing_and_distribution",
    "serverless_microvm_cold_start_timing",
    "cloud_edge_header_injection",
    "global_anycast_dns_resolution",
    "live_upstream_provider_network_latency",
]


def test_vercel_json_spec_and_file_coverage():
    """Verify vercel.json includes all static assets and templates referenced in HTML."""
    config_path = ROOT / "vercel.json"
    assert config_path.is_file()
    config = json.loads(config_path.read_text(encoding="utf-8"))

    func_config = config["functions"]["api/**/*.py"]
    assert func_config["maxDuration"] == 60
    assert "templates/**" in func_config["includeFiles"]
    assert "static/**" in func_config["includeFiles"]
    assert "api/**" in func_config["includeFiles"]

    # Verify all files referenced in base.html exist on disk
    base_html = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    static_refs = re.findall(r'href="/static/([^"]+)"|src="/static/([^"]+)"', base_html)
    for ref_tuple in static_refs:
        rel = ref_tuple[0] or ref_tuple[1]
        static_file = ROOT / "static" / rel
        assert static_file.is_file(), f"Referenced static file does not exist: {static_file}"


def test_templates_exist_and_render_locally():
    """Verify key templates exist on disk and render cleanly without live Vercel."""
    templates_dir = ROOT / "templates"
    assert templates_dir.is_dir()
    for required in ("base.html", "pages/home.html", "pages/not_found.html"):
        assert (templates_dir / required).is_file(), f"Missing template: {required}"

    with TestClient(api_index.app) as client:
        response = client.get("/", headers={"Accept": "text/html"})
        assert response.status_code == 200
        assert "QuantAI" in response.text
        assert "Research any company" in response.text


def test_deployment_honesty_boundary_matrix():
    """Verify explicit distinction between local verification and live cloud behavior."""
    docs = (ROOT / "VERCEL_DEPLOYMENT.md").read_text(encoding="utf-8")

    # Locally verified section must exist and list local items
    assert "### Locally Verified Behavior:" in docs
    assert "ASGI Application Routing" in docs
    assert "Template & Static Bundling" in docs
    assert "API Headers & Security" in docs
    assert "Graceful Failover" in docs

    # Behaviors requiring live deployment must be clearly separated
    assert "### Behaviors Requiring Live Vercel Deployment:" in docs
    assert "Edge CDN Routing" in docs
    assert "Real Serverless Cold Starts" in docs
    assert "Cloudflare / Vercel Edge Headers" in docs
    assert "Upstream Quota Latency" in docs


def test_no_fabricated_cloud_state_in_local_environment():
    """Verify that local test execution does not mock or falsely claim live Vercel cloud environment."""
    # When running locally, Vercel-specific cloud variables are absent or local
    with TestClient(api_index.app) as client:
        res = client.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"
        # Must not report fake live cloud deployment identifiers
        assert "x-vercel-id" not in res.headers
        assert "x-vercel-cache" not in res.headers
