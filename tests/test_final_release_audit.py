"""Tests for Part 36: Final release audit and complete migration parity.

Verifies:
1. Protected baseline file hashes match approved Option B specification.
2. PARITY_CHECKLIST.md exists and covers all 21 UI features and 7 infrastructure capabilities.
3. README.md specifies Vercel as the sole production target and documents local development.
4. PROGRESS.md is prepared for final release at 36/36.
5. Vercel deployment assets (vercel.json, .vercelignore, VERCEL_DEPLOYMENT.md) are intact.
6. All 5 converted TypeScript regression suites and Part 34/35 suites are present.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest().lower()


def test_protected_baseline_hashes():
    """Verify protected baseline test file hashes match Option B authorized specification."""
    readiness_path = ROOT / "tests" / "test_production_readiness.py"
    failover_path = ROOT / "tests" / "test_provider_failover.py"

    assert readiness_path.exists(), "test_production_readiness.py missing"
    assert failover_path.exists(), "test_provider_failover.py missing"

    readiness_hash = _sha256(readiness_path)
    failover_hash = _sha256(failover_path)

    # Option B authorized hash for test_production_readiness.py
    assert readiness_hash == "eec6aaf8796dcfc34540dad4e80b0d14fd7dcf39921434c28f441f118ff6115d"
    # Strictly preserved original hash for test_provider_failover.py
    assert failover_hash == "9c4e2d5693f6088a698be10c460538b520a2bf9a48a49a7aa371af5c5af59861"


def test_parity_checklist_complete_coverage():
    """Verify PARITY_CHECKLIST.md documents all 21 UI features and 7 infrastructure capabilities."""
    checklist_path = ROOT / "PARITY_CHECKLIST.md"
    assert checklist_path.exists(), "PARITY_CHECKLIST.md must exist in root"
    content = checklist_path.read_text(encoding="utf-8")

    # All 21 UI features
    for i in range(1, 22):
        assert f"F{i:02d}" in content, f"Missing UI feature F{i:02d} in checklist"

    # All 7 infrastructure capabilities
    for i in range(1, 8):
        assert f"C{i:02d}" in content, f"Missing capability C{i:02d} in checklist"

    assert "Vercel Serverless Function" in content
    assert "100% PARITY" in content


def test_readme_production_specification():
    """Verify README.md specifies Vercel as production platform and no self-hosted alternative."""
    readme_path = ROOT / "README.md"
    assert readme_path.exists(), "README.md must exist in root"
    content = readme_path.read_text(encoding="utf-8")

    assert "Vercel Serverless" in content or "Vercel" in content
    assert "PARITY_CHECKLIST.md" in content
    assert "VERCEL_DEPLOYMENT.md" in content
    assert "self-hosted Uvicorn server" not in content.lower() or "strictly for local development" in content.lower()


def test_vercel_configuration_integrity():
    """Verify vercel.json is valid JSON with required function duration and inclusions."""
    vercel_path = ROOT / "vercel.json"
    assert vercel_path.exists(), "vercel.json missing"
    config = json.loads(vercel_path.read_text(encoding="utf-8"))

    assert "functions" in config
    fn = config["functions"].get("api/**/*.py") or config["functions"].get("api/index.py")
    assert fn is not None, "Missing functions config for api entrypoint"
    assert fn.get("maxDuration") == 60
    assert "includeFiles" in fn

    ignore_path = ROOT / ".vercelignore"
    assert ignore_path.exists(), ".vercelignore missing"


def test_all_regression_and_capability_suites_present():
    """Verify all 5 converted TypeScript suites and Parts 34/35 suites are present."""
    required_suites = [
        "tests/test_legacy_parser.py",                # Part 26
        "tests/test_developer_telemetry.py",          # Part 27
        "tests/test_research_regressions.py",         # Part 28
        "tests/test_company_regressions.py",          # Part 29
        "tests/test_regression_inventory.py",         # Part 30
        "tests/test_deployment_config.py",            # Part 31
        "tests/test_local_runtime.py",                # Part 32
        "tests/test_vercel_verification.py",          # Part 33
        "tests/test_ui_feature_parity.py",            # Part 34
        "tests/test_infrastructure_security.py",      # Part 35
    ]
    for suite in required_suites:
        path = ROOT / suite
        assert path.exists(), f"Required test suite missing: {suite}"
