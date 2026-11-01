"""Tests for Pydantic contracts parity with TypeScript research, market, and AgentOS interfaces."""

from __future__ import annotations

import json
from typing import get_args

import pytest
from pydantic import ValidationError

from api.research_schemas import (
    ComparisonWinner,
    CompanyIdentity,
    ErrorCategory,
    IdentifierConfidence,
    MarketSnapshot,
    ResearchResponse,
    ServiceState,
    ServiceStatus,
    OverallState,
)
from api.web.contracts import (
    AgentInfo,
    AgentRunResponse,
    BriefNewsItem,
    ChartPoint,
    MarketBrief,
    Metric,
    ResearchErrorKind,
    TypedResearchResponse,
    friendly_agent_error,
    research_error_kind,
)


def test_research_response_parity_and_aliases():
    """Verify TypedResearchResponse compatibility with backend ResearchResponse."""
    assert TypedResearchResponse is ResearchResponse

    data = {
        "request_id": "req-123",
        "query": "AAPL",
        "company": {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "exchange": "NMS",
            "sector": "Technology",
            "identifier_confidence": "high",
        },
        "candidates": [],
        "market": {
            "current_price": 200.5,
            "currency": "USD",
            "daily_change": 2.5,
            "daily_change_percent": 1.25,
        },
        "history": [
            {"timestamp": "2026-11-01T00:00:00Z", "close": 200.5}
        ],
        "news": [],
        "events": [],
        "sources": [
            {
                "source": "Yahoo Finance",
                "retrieved_at": "2026-11-01T00:00:00Z",
                "data_type": "market",
            }
        ],
        "status": {
            "overall": "complete",
            "market": "available",
            "news": "available",
            "company": "available",
            "ai": "not_requested",
        },
        "warnings": [],
    }
    response = TypedResearchResponse.model_validate(data)
    assert response.request_id == "req-123"
    assert response.company.symbol == "AAPL"
    assert response.market.current_price == 200.5


def test_comparison_winner_literal_values():
    """Verify all comparison winner values including TIE and INSUFFICIENT_DATA."""
    assert set(item.value for item in ComparisonWinner) == {"A", "B", "TIE", "INSUFFICIENT_DATA"}


def test_market_presentation_contracts():
    """Verify Metric, ChartPoint, BriefNewsItem, and MarketBrief Pydantic models."""
    metric = Metric(label="P/E Ratio", value="28.5", tone="positive")
    assert metric.label == "P/E Ratio"
    assert metric.tone == "positive"

    # Default tone is neutral
    default_metric = Metric(label="Volume", value="50M")
    assert default_metric.tone == "neutral"

    chart_point = ChartPoint(label="10:00", value=195.4)
    assert chart_point.label == "10:00"
    assert chart_point.value == 195.4

    news = BriefNewsItem(
        title="Quarterly results",
        summary="Positive earnings beat",
        publisher="Reuters",
        publishedAt="2026-11-01T12:00:00Z",
        url="https://example.test/news",
        sentiment="positive",
    )
    assert news.title == "Quarterly results"
    assert news.publishedAt == "2026-11-01T12:00:00Z"


def test_market_brief_serialization_and_defaults():
    """Verify MarketBrief contract with nested models and null handling."""
    brief = MarketBrief(
        companyName="Apple Inc.",
        ticker="AAPL",
        exchange="NMS",
        sector="Technology",
        industry="Consumer Electronics",
        quoteLabel="Current price",
        quote="$200.50",
        change="+1.25%",
        metrics=[Metric(label="Market cap", value="$3.0T", tone="positive")],
        news=[],
        chart=[ChartPoint(label="10:00", value=200.5)],
        priceHistory={
            "intraday": [],
            "daily": [{"label": "2026-11-01", "value": 200.5}],
            "availablePeriods": ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"],
            "defaultPeriod": "1M",
        },
        analysis="Executive summary",
        aiInterpretationNotice=None,
        signal=None,
        events=[],
        sources=[],
        warnings=[],
        freshness=[],
        deepAnalysis=None,
    )
    dumped = brief.model_dump(by_alias=True)
    assert dumped["companyName"] == "Apple Inc."
    assert dumped["quote"] == "$200.50"
    assert dumped["metrics"][0]["label"] == "Market cap"
    assert dumped["priceHistory"]["defaultPeriod"] == "1M"


def test_agentos_contracts():
    """Verify AgentRunResponse and AgentInfo models."""
    run = AgentRunResponse(
        run_id="run-001",
        session_id="sess-001",
        content="Research response",
        status="SUCCESS",
    )
    assert run.run_id == "run-001"
    assert run.status == "SUCCESS"

    agent = AgentInfo(
        id="groq-finance-agent",
        name="Finance Research Agent",
        model={"model": "gpt-oss-120b", "provider": "Groq"},
    )
    assert agent.id == "groq-finance-agent"
    assert agent.model["provider"] == "Groq"


def test_research_error_kind_mapping():
    """Verify safe public research error classification helper."""
    assert research_error_kind("Multiple companies match query") == "ambiguous"
    assert research_error_kind("Entity not found for XYZ") == "not_found"
    assert research_error_kind("AI analysis is temporarily unavailable") == "ai_unavailable"
    assert research_error_kind("Failed to fetch news feed") == "news_unavailable"
    assert research_error_kind("Unexpected socket reset") == "other"


def test_friendly_agent_error_mapping():
    """Verify AgentOS friendly error mapping helper."""
    assert "temporarily unavailable" in friendly_agent_error("Rate limit exceeded", status=429)
    assert "temporarily unavailable" in friendly_agent_error("Service unavailable", status=503)
    assert "temporarily unavailable" in friendly_agent_error("Internal server error", status=500)
    assert "unavailable for this session" in friendly_agent_error("Unauthorized", status=401)
    assert friendly_agent_error("Custom error") == "Custom error."
