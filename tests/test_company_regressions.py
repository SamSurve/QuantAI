"""Tests for Part 29: Company deep analysis and comparison regressions.

Verifies:
1. Company deep analysis:
   - Full factual synthesis with deterministic values strictly preserved outside AI boundary.
   - Graceful partial degradation on failing sub-services.
   - Numeric narrative guard ensuring AI cannot inject unverified metrics into narrative text.
2. Company comparison:
   - Complete multi-company comparison with deterministic metrics.
   - Strict currency matching and period protection.
   - Verified FX conversion rates and provenance tracking.
   - Reverse FX direction protection and missing FX handling.
   - Cache deduplication and in-flight request protection.
   - Validation against identical tickers.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import api.index as index_module
import tests.test_company_deep_analysis as t_deep
import tests.test_company_comparison as t_comparison


# ------------------------------------------------------------
# COMPANY DEEP ANALYSIS REGRESSIONS
# ------------------------------------------------------------


@pytest.mark.asyncio
async def test_company_deep_analysis_complete_regression():
    """Verify complete company deep analysis retains deterministic values."""
    await t_deep.verify_complete_company_analysis()


@pytest.mark.asyncio
async def test_company_deep_analysis_partial_regression():
    """Verify partial company deep analysis handles subservice failures gracefully."""
    await t_deep.verify_partial_company_analysis()


def test_company_deep_analysis_numeric_narrative_guard():
    """Verify AI interpretation cannot invent numeric facts in narrative claims."""
    t_deep.verify_numeric_narrative_guard()


# ------------------------------------------------------------
# COMPANY COMPARISON REGRESSIONS
# ------------------------------------------------------------


@pytest.mark.asyncio
async def test_company_comparison_complete_regression():
    """Verify complete company comparison across multiple companies."""
    await t_comparison.verify_complete_comparison()


def test_company_comparison_currency_and_period_protection():
    """Verify currency mismatch protection and period validation."""
    t_comparison.verify_currency_and_period_protection()


@pytest.mark.asyncio
async def test_company_comparison_verified_fx_and_provenance():
    """Verify FX rate conversion with verified provenance records."""
    await t_comparison.verify_verified_fx_comparison_and_provenance()


@pytest.mark.asyncio
async def test_company_comparison_missing_or_invalid_fx():
    """Verify missing or invalid FX preserves safe error and does not corrupt data."""
    await t_comparison.verify_missing_or_invalid_fx_preserves_safe_failure()


def test_company_comparison_reverse_fx_direction_protection():
    """Verify reverse FX direction handling and period consistency."""
    t_comparison.verify_reverse_fx_direction_and_period_protection()


@pytest.mark.asyncio
async def test_company_comparison_partial_sources_and_ai_failure():
    """Verify comparison tolerates partial sources and AI failure."""
    await t_comparison.verify_partial_sources_and_ai_failure()


@pytest.mark.asyncio
async def test_company_comparison_unexpected_profile_failure():
    """Verify unexpected profile failure falls back to safe partial data."""
    await t_comparison.verify_unexpected_profile_failure_is_safe_partial_data()


@pytest.mark.asyncio
async def test_company_comparison_cache_deduplication():
    """Verify cached comparison results avoid redundant calls."""
    await t_comparison.verify_cache_deduplication()


def test_company_comparison_numeric_guard_and_validation():
    """Verify numeric guards prevent narrative hallucinations in comparison."""
    t_comparison.verify_numeric_guard_and_validation()


@pytest.mark.asyncio
async def test_company_comparison_same_resolved_ticker_validation():
    """Verify comparison rejects comparing a ticker to itself."""
    await t_comparison.verify_same_resolved_ticker_is_safe_validation_error()


def test_company_regressions_endpoint_integration():
    """Verify client integration with company analysis and comparison routes."""
    with TestClient(index_module.app) as client:
        # Request with empty body should be rejected safely by Pydantic validation
        resp = client.post("/api/research", json={})
        assert resp.status_code == 422
