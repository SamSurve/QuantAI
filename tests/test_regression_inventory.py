"""Tests for Part 30: AgentOS errors and unified regression inventory.

Formally inventories, catalogs, and verifies all five completed Python
regression suites that converted the original TypeScript regression cases:
1. tests/test_typed_research_backend.py (Phase 1–3 core typed research)
2. tests/test_market_intelligence.py (Phase 4 market intelligence)
3. tests/test_company_deep_analysis.py (Phase 5 company deep analysis)
4. tests/test_company_comparison.py (Phase 6 company comparison)
5. tests/test_agentos_client_errors.py (Phase 7 / Part 20 AgentOS client errors)

Also asserts AgentOS error handling matrix and normalization behavior.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.web.chat import friendly_agent_error
import tests.test_agentos_client_errors as t_agentos_errors
import tests.test_typed_research_backend as t_typed
import tests.test_market_intelligence as t_market
import tests.test_company_deep_analysis as t_deep
import tests.test_company_comparison as t_comparison


CONVERTED_REGRESSION_INVENTORY = [
    {
        "suite_id": "REG-01",
        "title": "Typed Research Backend Regression",
        "path": "tests/test_typed_research_backend.py",
        "phase": "Phase 1–3",
        "target": "Core typed research orchestrator, bounds, cache, adapters, ambiguity",
    },
    {
        "suite_id": "REG-02",
        "title": "Market Intelligence Regression",
        "path": "tests/test_market_intelligence.py",
        "phase": "Phase 4",
        "target": "Deterministic technical signals, history fallback, dividend yield normalization",
    },
    {
        "suite_id": "REG-03",
        "title": "Company Deep Analysis Regression",
        "path": "tests/test_company_deep_analysis.py",
        "phase": "Phase 5",
        "target": "Company profile, financial health, governance, numeric narrative guard",
    },
    {
        "suite_id": "REG-04",
        "title": "Company Comparison Regression",
        "path": "tests/test_company_comparison.py",
        "phase": "Phase 6",
        "target": "Multi-company comparison, FX rate provenance, currency & period protection",
    },
    {
        "suite_id": "REG-05",
        "title": "AgentOS Client Errors Regression",
        "path": "tests/test_agentos_client_errors.py",
        "phase": "Part 20",
        "target": "AgentOS client error normalization, friendly messages, quota/rate-limit detection",
    },
]


# ------------------------------------------------------------
# UNIFIED REGRESSION INVENTORY VERIFICATION
# ------------------------------------------------------------


def test_regression_inventory_completeness():
    """Verify all five converted regression suites exist on disk and are non-empty."""
    assert len(CONVERTED_REGRESSION_INVENTORY) == 5
    for item in CONVERTED_REGRESSION_INVENTORY:
        file_path = ROOT / item["path"]
        assert file_path.is_file(), f"Missing regression suite: {item['path']}"
        content = file_path.read_text(encoding="utf-8")
        assert len(content.strip()) > 100, f"Empty regression suite: {item['path']}"
        assert "from __future__ import annotations" in content


@pytest.mark.asyncio
async def test_regression_inventory_execution_coverage():
    """Verify key functions from all five suites execute without error."""
    # Suite 1: Typed research
    await t_typed.verify_orchestrator_partial_results()
    t_typed.verify_bounded_ai_context()

    # Suite 2: Market intelligence
    t_market.verify_signal_methodology()
    await t_market.verify_history_close_fallback()

    # Suite 3: Company deep analysis
    await t_deep.verify_complete_company_analysis()
    t_deep.verify_numeric_narrative_guard()

    # Suite 4: Company comparison
    await t_comparison.verify_complete_comparison()
    t_comparison.verify_currency_and_period_protection()

    # Suite 5: AgentOS errors
    t_agentos_errors.test_upstream_provider_500_error()
    t_agentos_errors.test_rate_limited_429_error()


# ------------------------------------------------------------
# AGENTOS CLIENT ERROR NORMALIZATION REGRESSIONS
# ------------------------------------------------------------


def test_agentos_errors_status_code_mapping():
    """Verify status code mapping for 401, 409, 429, 500, 503."""
    t_agentos_errors.test_upstream_provider_500_error()
    t_agentos_errors.test_unauthorized_401_error()
    t_agentos_errors.test_rate_limited_429_error()
    t_agentos_errors.test_temporarily_unavailable_in_message_200()
    t_agentos_errors.test_custom_conflict_message_409()
    t_agentos_errors.test_rate_limit_patterns()


def test_agentos_errors_edge_cases():
    """Verify edge cases: None message, empty message, unusual status codes."""
    # Empty / none message with 500
    assert "temporarily unavailable" in friendly_agent_error("", 500)
    assert "temporarily unavailable" in friendly_agent_error(None, 500)

    # Clean preservation of standard 400 validation error
    custom = "Invalid ticker symbol format."
    assert friendly_agent_error(custom, 400) == custom

    # Rate limit keywords detected case-insensitively
    assert "temporarily unavailable" in friendly_agent_error("RATE LIMIT EXCEEDED", 200).lower()
    assert "temporarily unavailable" in friendly_agent_error("Quota Exceeded for Token Bucket", 200).lower()
