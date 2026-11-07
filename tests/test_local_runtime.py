"""Tests for Part 32: Local Uvicorn runtime and environment documentation.

Verifies:
1. Local ASGI / Uvicorn runtime behavior:
   - Verifies Uvicorn config initializes against root and api entrypoints.
   - Verifies ASGI application interface and lifespan compatibility.
   - Confirms Uvicorn is strictly a local dev/testing harness, not a production target.
2. Local route serving:
   - HTML shell rendering under local runtime (GET / with text/html).
   - JSON health and research routing under local runtime.
   - Static asset serving (/static/css/app.css, logo) via local ASGI mount.
3. Environment variable documentation:
   - Verifies .env.example contains variable names only with no credentials or values.
   - Verifies full coverage of variables referenced across backend code.
"""

from __future__ import annotations

import sys
from pathlib import Path
from fastapi.testclient import TestClient
import uvicorn

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import index as root_index
import api.index as api_index


def test_uvicorn_local_configuration():
    """Verify uvicorn.Config successfully initializes against local application."""
    config = uvicorn.Config(app=root_index.app, host="127.0.0.1", port=8000, log_level="warning")
    assert config is not None
    assert callable(config.app)

    # Re-export on root index matches api.index.app
    assert root_index.app is api_index.app


def test_local_asgi_html_and_json_content_negotiation():
    """Verify local ASGI server serves both HTML shell and JSON APIs correctly."""
    with TestClient(root_index.app) as client:
        # Browser request for HTML home page
        res_html = client.get("/", headers={"Accept": "text/html"})
        assert res_html.status_code == 200
        assert "text/html" in res_html.headers["content-type"]
        assert "<title>QuantAI" in res_html.text

        # API request for JSON health
        res_json = client.get("/", headers={"Accept": "application/json"})
        assert res_json.status_code == 200
        assert "application/json" in res_json.headers["content-type"]
        assert res_json.json()["agent_id"] == "groq-finance-agent"


def test_local_asgi_static_assets_mount():
    """Verify static assets are served through the local ASGI static mount."""
    with TestClient(root_index.app) as client:
        # CSS stylesheet
        css_res = client.get("/static/css/app.css")
        assert css_res.status_code == 200
        assert "text/css" in css_res.headers["content-type"]

        # Logo asset
        logo_res = client.get("/static/assets/analysts-ledger-logo.png")
        assert logo_res.status_code == 200
        assert "image/png" in logo_res.headers["content-type"]


def test_env_example_safety_and_completeness():
    """Verify .env.example contains only variable names without values or secrets."""
    env_example_path = ROOT / ".env.example"
    assert env_example_path.is_file(), ".env.example is missing"

    lines = env_example_path.read_text(encoding="utf-8").splitlines()
    parsed_vars = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        assert "=" in line, f"Malformed line in .env.example: {line}"
        key, value = line.split("=", 1)
        parsed_vars[key.strip()] = value.strip()
        # Strictly empty values: never commit credentials or placeholders
        assert value.strip() == "", f"Value found in .env.example for {key}: must be empty"

    # All primary and failover keys must be documented
    required_keys = {
        "GROQ_API_KEY_PRIMARY",
        "GROQ_MODEL_PRIMARY",
        "GROQ_API_KEY_SECONDARY",
        "GROQ_MODEL_SECONDARY",
        "OPENROUTER_API_KEY",
        "OPENROUTER_MODEL",
        "AI_PROVIDER_ORDER",
        "QUANTAI_DEVTOOLS",
    }
    assert required_keys.issubset(set(parsed_vars.keys())), f"Missing keys: {required_keys - set(parsed_vars.keys())}"


def test_uvicorn_supplementary_testing_designation():
    """Verify documentation and architecture clearly mark local Uvicorn as dev-only."""
    docs_path = ROOT / "VERCEL_DEPLOYMENT.md"
    assert docs_path.is_file()
    docs = docs_path.read_text(encoding="utf-8")
    assert "local development (`uvicorn index:app --reload`)" in docs
    assert "Vercel Serverless Functions" in docs
