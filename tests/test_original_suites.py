"""Executes each of the seven original Python regression suites in a separate subprocess.

Verifies that all original suites run directly with sys.executable and exit with code 0.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]

ORIGINAL_SUITES = [
    "tests/test_agentos_entity_resolution.py",
    "tests/test_company_comparison.py",
    "tests/test_company_deep_analysis.py",
    "tests/test_market_intelligence.py",
    "tests/test_production_readiness.py",
    "tests/test_provider_failover.py",
    "tests/test_typed_research_backend.py",
]


@pytest.mark.parametrize("suite_relpath", ORIGINAL_SUITES)
def test_original_suite_subprocess(suite_relpath: str):
    """Run an original suite as a subprocess and assert exit code 0."""
    suite_path = ROOT / suite_relpath
    assert suite_path.exists(), f"Suite file missing: {suite_relpath}"

    env = dict(os.environ)
    env["OPENBLAS_NUM_THREADS"] = "1"
    env["OMP_NUM_THREADS"] = "1"

    result = subprocess.run(
        [sys.executable, str(suite_path)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, (
        f"Suite {suite_relpath} failed with exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )
