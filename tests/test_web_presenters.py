"""Tests for market brief and research presentation helpers."""

from __future__ import annotations

import pytest

from api.research_schemas import (
    CompanyIdentity,
    FreshnessRecord,
    FreshnessState,
    IdentifierConfidence,
    MarketIntelligenceFreshness,
    MarketIntelligenceReport,
    MarketSnapshot,
    OverallState,
    PriceHistoryBundle,
    ResearchResponse,
    ServiceState,
    ServiceStatus,
    StructuredAnalysis,
)
from api.web.presenters import (
    empty_market_brief,
    market_brief_from_research,
    typed_analysis_markdown,
)


def test_empty_market_brief():
    brief = empty_market_brief()
    assert brief.companyName == "—"
    assert brief.ticker == "—"
    assert brief.quote == "—"
    assert brief.change == "Awaiting AgentOS research"
    assert len(brief.metrics) == 6
    assert brief.metrics[0].label == "Market cap"


def test_market_brief_from_research():
    freshness = FreshnessRecord(state=FreshnessState.LIVE, as_of="2026-11-01T00:00:00Z")
    intelligence = MarketIntelligenceReport(
        market_pulse=MarketSnapshot(
            current_price=200.5,
            currency="USD",
            daily_change_percent=1.25,
            market_cap=3_000_000_000_000,
            pe_ratio=28.5,
            fifty_two_week_high=210.0,
            fifty_two_week_low=160.0,
            volume=50_000_000,
            dividend_yield=0.005,
            eps=6.5,
        ),
        price_history=PriceHistoryBundle(
            intraday=[],
            daily=[{"timestamp": "2026-11-01", "close": 200.5}],
            available_periods=["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"],
            default_period="1M",
            freshness=freshness,
        ),
        recent_news=[],
        event_radar=[],
        executive_brief=StructuredAnalysis(
            executive_summary="Strong revenue execution",
            bullish_factors=["Ecosystem momentum"],
            bearish_factors=["Macro headwinds"],
            risks=["Supply chain"],
            catalysts=["Product launch"],
        ),
        freshness=MarketIntelligenceFreshness(
            company=freshness,
            market=freshness,
            history=freshness,
            news=freshness,
            events=freshness,
            analysis=freshness,
        ),
    )

    research = ResearchResponse(
        request_id="test-req-1",
        query="AAPL",
        company=CompanyIdentity(
            symbol="AAPL",
            name="Apple Inc.",
            exchange="NMS",
            sector="Technology",
            industry="Consumer Electronics",
            currency="USD",
            identifier_confidence=IdentifierConfidence.HIGH,
        ),
        market=intelligence.market_pulse,
        market_intelligence=intelligence,
        status=ServiceStatus(
            overall=OverallState.COMPLETE,
            market=ServiceState.AVAILABLE,
            news=ServiceState.AVAILABLE,
            company=ServiceState.AVAILABLE,
            ai=ServiceState.AVAILABLE,
        ),
    )

    brief = market_brief_from_research(research)
    assert brief.companyName == "Apple Inc."
    assert brief.ticker == "AAPL"
    assert brief.quote == "$200.50"
    assert brief.change == "+1.25%"
    assert brief.quoteLabel == "Current price"

    # Check metrics
    labels = {m.label: m.value for m in brief.metrics}
    assert labels["Market cap"] == "$3T"
    assert labels["P / E ratio"] == "28.5"
    assert labels["Dividend yield"] == "0.50%"

    # Check analysis markdown
    assert "## Executive Summary" in brief.analysis
    assert "Strong revenue execution" in brief.analysis
    assert "Ecosystem momentum" in brief.analysis
