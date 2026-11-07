"""Tests for Part 31: Vercel deployment configuration and ASGI routing.

Verifies:
1. vercel.json structure:
   - JSON schema definition.
   - Serverless functions maxDuration=60.
   - includeFiles bundling templates/**, static/**, api/**.
   - excludeFiles stripping tests, pycache, venv.
   - Cache-Control: no-store header for all /api/(.*) routes.
   - Rewrites forwarding all routes to ASGI entrypoint /api/index.py.
2. .vercelignore patterns:
   - tests/, __pycache__/, *.pyc, .vercel/, dist/, node_modules/.
3. VERCEL_DEPLOYMENT.md environment variable documentation:
   - GROQ_API_KEY_PRIMARY, GROQ_MODEL_PRIMARY, GROQ_API_KEY_SECONDARY,
     GROQ_MODEL_SECONDARY, OPENROUTER_API_KEY, OPENROUTER_MODEL.
4. Python 3.12 runtime pinning.
5. All 4 modular Vercel entrypoint files import and re-export canonical app.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_vercel_json_schema_and_functions():
    """Verify vercel.json exists, parses, and defines 60s maxDuration for functions."""
    config_path = ROOT / "vercel.json"
    assert config_path.is_file(), "vercel.json missing"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    assert config.get("$schema") == "https://openapi.vercel.sh/vercel.json"
    functions = config.get("functions", {})
    api_func = functions.get("api/**/*.py")
    assert api_func is not None, "Missing api/**/*.py function definition"
    assert api_func.get("maxDuration") == 60

    include_files = api_func.get("includeFiles", "")
    assert "templates/**" in include_files
    assert "static/**" in include_files
    assert "api/**" in include_files

    exclude_files = api_func.get("excludeFiles", "")
    assert "tests/**" in exclude_files
    assert "__pycache__" in exclude_files


def test_vercel_headers_and_rewrites():
    """Verify Cache-Control: no-store header on API routes and ASGI rewrites."""
    config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))

    headers = config.get("headers", [])
    api_header = next((h for h in headers if h.get("source") in ("/api/(.*)", "/api/:path*")), None)
    assert api_header is not None, "Missing API header rule"
    assert any(
        kv.get("key") == "Cache-Control" and "no-store" in kv.get("value", "")
        for kv in api_header.get("headers", [])
    )

    rewrites = config.get("rewrites", [])
    assert any(
        r.get("destination") == "/api/index.py"
        for r in rewrites
    ), "Missing rewrite to /api/index.py"


def test_vercelignore_patterns():
    """Verify .vercelignore contains all required patterns for lean bundles."""
    ignore_path = ROOT / ".vercelignore"
    assert ignore_path.is_file(), ".vercelignore missing"
    content = ignore_path.read_text(encoding="utf-8")

    required = ("tests/", "__pycache__/", "*.pyc", ".vercel/", "dist/", "node_modules/")
    for pattern in required:
        assert pattern in content, f"Missing {pattern} in .vercelignore"


def test_vercel_deployment_docs_and_variables():
    """Verify VERCEL_DEPLOYMENT.md documents all primary and secondary provider keys."""
    docs_path = ROOT / "VERCEL_DEPLOYMENT.md"
    assert docs_path.is_file(), "VERCEL_DEPLOYMENT.md missing"
    content = docs_path.read_text(encoding="utf-8")

    required_vars = (
        "GROQ_API_KEY_PRIMARY",
        "GROQ_MODEL_PRIMARY",
        "GROQ_API_KEY_SECONDARY",
        "GROQ_MODEL_SECONDARY",
        "OPENROUTER_API_KEY",
        "OPENROUTER_MODEL",
    )
    for var_name in required_vars:
        assert var_name in content, f"Missing documentation for {var_name}"


def test_python_runtime_version():
    """Verify Python runtime is pinned to 3.12."""
    py_version_path = ROOT / ".python-version"
    assert py_version_path.is_file()
    assert py_version_path.read_text(encoding="utf-8").strip() == "3.12"


def test_modular_entrypoints_export_canonical_app():
    """Verify all 4 modular entrypoints and root index.py re-export canonical app."""
    entrypoints = (
        "api/health.py",
        "api/agents.py",
        "api/research.py",
        "api/agents/groq-finance-agent/runs.py",
        "index.py",
    )
    for ep in entrypoints:
        ep_path = ROOT / ep
        assert ep_path.is_file(), f"Missing entrypoint {ep}"
        text = ep_path.read_text(encoding="utf-8")
        assert "app" in text
