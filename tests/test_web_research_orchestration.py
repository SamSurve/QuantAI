"""Tests for research orchestration and dual-mode execution.

Verifies concurrent execution of Market Intelligence and Company Deep Analysis,
partial result handling, and error classification.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch
import pytest

from api.research_schemas import (
    CompanyIdentity,
    IdentifierConfidence,
    ErrorCategory,
    MarketSnapshot,
    ResearchMode,
    ResearchRequest,
    ResearchResponse,
    ServiceStatus,
)
from api.research_errors import ResearchError
from api.web import research


def _mock_market_response(symbol="AAPL") -> ResearchResponse:
    return ResearchResponse(
        request_id="test-req-market",
        query=symbol,
        company=CompanyIdentity(
            symbol=symbol,
            name="Apple Inc.",
            exchange="NASDAQ",
            sector="Technology",
            industry="Consumer Electronics",
            identifier_confidence=IdentifierConfidence.HIGH,
        ),
        market=MarketSnapshot(current_price=228.40, daily_change=2.15, daily_change_percent=0.95),
        status=ServiceStatus(overall="complete", market="available", company="available", ai="available", news="available"),
    )


def _mock_deep_response(symbol="AAPL") -> ResearchResponse:
    return ResearchResponse(
        request_id="test-req-deep",
        query=symbol,
        company=CompanyIdentity(
            symbol=symbol,
            name="Apple Inc.",
            exchange="NASDAQ",
            sector="Technology",
            industry="Consumer Electronics",
            identifier_confidence=IdentifierConfidence.HIGH,
        ),
        market=MarketSnapshot(current_price=228.40),
        status=ServiceStatus(overall="complete", market="available", company="available", ai="available", news="available"),
    )


@pytest.mark.asyncio
async def test_dual_research_both_succeed():
    """Verify both operations succeed and results are merged."""
    mock_orchestrator = AsyncMock()
    mock_orchestrator.research.side_effect = [
        _mock_market_response("AAPL"),
        _mock_deep_response("AAPL"),
    ]

    result = await research.orchestrate_dual_research(
        query="AAPL",
        request_id="test-1",
        orchestrator=mock_orchestrator,
    )

    assert result.company is not None
    assert result.company.symbol == "AAPL"
    assert mock_orchestrator.research.call_count == 2

    # Check arguments
    calls = mock_orchestrator.research.call_args_list
    assert calls[0].args[1].mode == ResearchMode.MARKET_INTELLIGENCE
    assert calls[0].args[1].include_analysis is True
    assert calls[1].args[1].mode == ResearchMode.COMPANY_DEEP_ANALYSIS
    assert calls[1].args[1].include_analysis is False


@pytest.mark.asyncio
async def test_dual_research_market_succeeds_deep_fails():
    """Verify market intelligence survives when deep analysis fails."""
    mock_orchestrator = AsyncMock()
    mock_orchestrator.research.side_effect = [
        _mock_market_response("AAPL"),
        ResearchError(ErrorCategory.COMPANY_UNAVAILABLE, "Deep analysis unavailable"),
    ]

    result = await research.orchestrate_dual_research(
        query="AAPL",
        request_id="test-2",
        orchestrator=mock_orchestrator,
    )

    assert result.company is not None
    assert result.company.symbol == "AAPL"
    assert result.market is not None
    assert result.market.current_price == 228.40


@pytest.mark.asyncio
async def test_dual_research_deep_succeeds_market_fails():
    """Verify deep analysis survives when market intelligence fails."""
    mock_orchestrator = AsyncMock()
    mock_orchestrator.research.side_effect = [
        ResearchError(ErrorCategory.DATA_UNAVAILABLE, "Market data unavailable"),
        _mock_deep_response("AAPL"),
    ]

    result = await research.orchestrate_dual_research(
        query="AAPL",
        request_id="test-3",
        orchestrator=mock_orchestrator,
    )

    assert result.company is not None
    assert result.company.symbol == "AAPL"


@pytest.mark.asyncio
async def test_dual_research_both_fail_raises():
    """Verify ResearchError is raised when both operations fail."""
    mock_orchestrator = AsyncMock()
    mock_orchestrator.research.side_effect = [
        ResearchError(ErrorCategory.ENTITY_NOT_FOUND, "No supported listed company"),
        ResearchError(ErrorCategory.ENTITY_NOT_FOUND, "No supported listed company"),
    ]

    with pytest.raises(ResearchError) as exc_info:
        await research.orchestrate_dual_research(
            query="INVALID",
            request_id="test-4",
            orchestrator=mock_orchestrator,
        )
    assert exc_info.value.category == ErrorCategory.ENTITY_NOT_FOUND
