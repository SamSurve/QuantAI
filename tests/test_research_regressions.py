"""Tests for Part 28: Research regressions and push wrapper upgrade.

Verifies:
1. Converted research regressions:
   - Typed research backend (bounds, partials, inflight deduplication, ambiguity).
   - Market intelligence (deterministic signals, history fallback, dividend yield unit normalization).
2. Push wrapper upgrade:
   - TOTAL_PARTS extended to 36.
   - Batch and Day boundaries updated.
   - Argument validation up to 36.
   - Commit message structure enforcement.
   - Safe staging filters and protected path isolation.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import migration.push_part as push_wrapper
import tests.test_typed_research_backend as t_typed
import tests.test_market_intelligence as t_market


# ------------------------------------------------------------
# RESEARCH REGRESSION VERIFICATION
# ------------------------------------------------------------


@pytest.mark.asyncio
async def test_typed_research_orchestrator_regressions():
    """Verify typed research orchestrator handles partial results and malformed AI."""
    await t_typed.verify_orchestrator_partial_results()
    await t_typed.verify_malformed_ai_is_partial_not_failure()


def test_typed_research_bounds_and_protection():
    """Verify typed research bounds AI context and request size."""
    t_typed.verify_bounded_ai_context()


@pytest.mark.asyncio
async def test_typed_research_cache_and_ambiguity():
    """Verify cache deduplication, entity validation, and adapters."""
    await t_typed.verify_cache_and_inflight_deduplication()
    await t_typed.verify_entity_validation_and_ambiguity()
    await t_typed.verify_market_and_news_adapters()
    await t_typed.verify_request_protection()


def test_market_intelligence_signals_regression():
    """Verify market intelligence deterministic signal calculations."""
    t_market.verify_signal_methodology()


@pytest.mark.asyncio
async def test_market_intelligence_pipeline_regressions():
    """Verify complete flow, partial failure, fallback, and yield normalization."""
    await t_market.verify_complete_market_intelligence()
    await t_market.verify_partial_failures()
    await t_market.verify_history_close_fallback()
    await t_market.verify_dividend_yield_unit_normalization()


# ------------------------------------------------------------
# PUSH WRAPPER UPGRADE VERIFICATION
# ------------------------------------------------------------


def test_push_wrapper_extended_part_limits():
    """Verify push wrapper is configured for 36 parts."""
    assert push_wrapper.TOTAL_PARTS == 36
    assert 36 in push_wrapper.BATCH_ENDS
    assert 36 in push_wrapper.DAY_ENDS


def test_push_wrapper_argument_validation():
    """Verify argument validation accepts parts 1-36 and rejects out-of-range."""
    # Valid parts
    push_wrapper.validate_arguments(1, "part 01: valid message")
    push_wrapper.validate_arguments(28, "part 28: research regressions and push wrapper upgrade")
    push_wrapper.validate_arguments(36, "part 36: final release audit")

    # Out of range parts
    with pytest.raises(push_wrapper.PushError, match="part_no must be between 1 and 36"):
        push_wrapper.validate_arguments(0, "part 00: invalid")

    with pytest.raises(push_wrapper.PushError, match="part_no must be between 1 and 36"):
        push_wrapper.validate_arguments(37, "part 37: out of range")


def test_push_wrapper_message_format_validation():
    """Verify commit message formatting requires single line and correct prefix."""
    with pytest.raises(push_wrapper.PushError, match="must be a single line"):
        push_wrapper.validate_arguments(28, "part 28: first line\nsecond line")

    with pytest.raises(push_wrapper.PushError, match='must start with "part 28:"'):
        push_wrapper.validate_arguments(28, "wrong prefix message")

    with pytest.raises(push_wrapper.PushError, match="needs a description"):
        push_wrapper.validate_arguments(28, "part 28:")


def test_push_wrapper_safe_staging_filter():
    """Verify push wrapper safe staging rejects sensitive files and accepts safe code."""
    assert push_wrapper.is_safe_to_stage("api/web/routes.py") is True
    assert push_wrapper.is_safe_to_stage("tests/test_research_regressions.py") is True
    assert push_wrapper.is_safe_to_stage(".env.example") is True

    # Sensitive or protected files
    assert push_wrapper.is_safe_to_stage(".env") is False
    assert push_wrapper.is_safe_to_stage(".env.production") is False
    assert push_wrapper.is_safe_to_stage("secret_key.pem") is False
    assert push_wrapper.is_safe_to_stage("credentials.json") is False
    assert push_wrapper.is_safe_to_stage(".venv/bin/python") is False
    assert push_wrapper.is_safe_to_stage("tools/tailwind.exe") is False
