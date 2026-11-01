"""Regression test baseline verifying all seven original suites under pytest."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tests.test_agentos_entity_resolution as t_agentos
import tests.test_company_comparison as t_comparison
import tests.test_company_deep_analysis as t_deep
import tests.test_market_intelligence as t_market
import tests.test_production_readiness as t_prod
import tests.test_provider_failover as t_failover
import tests.test_typed_research_backend as t_typed


def test_agentos_entity_resolution_baseline():
    """Verify entity resolution behavior from original suite."""
    t_agentos.verify_clear_company_names()
    t_agentos.verify_terminal_ticker()
    t_agentos.verify_ambiguous_never_fetches_ticker()


@pytest.mark.asyncio
async def test_company_comparison_baseline():
    """Verify company comparison functions and validations."""
    await t_comparison.verify_complete_comparison()
    t_comparison.verify_currency_and_period_protection()
    await t_comparison.verify_verified_fx_comparison_and_provenance()
    await t_comparison.verify_missing_or_invalid_fx_preserves_safe_failure()
    t_comparison.verify_reverse_fx_direction_and_period_protection()
    await t_comparison.verify_partial_sources_and_ai_failure()
    await t_comparison.verify_unexpected_profile_failure_is_safe_partial_data()
    await t_comparison.verify_cache_deduplication()
    t_comparison.verify_numeric_guard_and_validation()
    await t_comparison.verify_same_resolved_ticker_is_safe_validation_error()


@pytest.mark.asyncio
async def test_company_deep_analysis_baseline():
    """Verify deep analysis functions and protections."""
    await t_deep.verify_complete_company_analysis()
    await t_deep.verify_partial_company_analysis()
    t_deep.verify_numeric_narrative_guard()


@pytest.mark.asyncio
async def test_market_intelligence_baseline():
    """Verify market intelligence calculations and fallback rules."""
    t_market.verify_signal_methodology()
    await t_market.verify_complete_market_intelligence()
    await t_market.verify_partial_failures()
    await t_market.verify_history_close_fallback()
    await t_market.verify_dividend_yield_unit_normalization()


def test_production_readiness_baseline():
    """Verify production readiness routes and guardrails."""
    t_prod.check_agentos_routes()
    t_prod.check_missing_provider_behavior()
    t_prod.check_agentos_run_protection()
    t_prod.check_configured_provider_agentos_setup()


@pytest.mark.asyncio
async def test_provider_failover_baseline():
    """Verify provider fallback timeout and structured engine failover."""
    await t_failover.verify_async_timeout_fallback()
    await t_failover.verify_structured_engine_matrix()


@pytest.mark.asyncio
async def test_typed_research_backend_baseline():
    """Verify orchestrator, bounds, cache, and protection."""
    await t_typed.verify_orchestrator_partial_results()
    await t_typed.verify_malformed_ai_is_partial_not_failure()
    t_typed.verify_bounded_ai_context()
    await t_typed.verify_cache_and_inflight_deduplication()
    await t_typed.verify_entity_validation_and_ambiguity()
    await t_typed.verify_market_and_news_adapters()
    await t_typed.verify_request_protection()
