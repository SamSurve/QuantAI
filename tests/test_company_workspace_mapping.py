"""Port of original tests/test_company_workspace_mapping.ts to pytest.

Verifies:
- Price history available periods preservation
- Intraday and daily point count preservation
- Default period preservation
- Company profile description preservation
- Financials revenue and net income missing-data preservation
- Market cap fallback preservation
- Compact Financial Health metrics preservation
- Partial research response handling
- Company association integrity
"""

from __future__ import annotations

import pytest

from api.web.contracts import TypedResearchResponse
from api.web.presenters import market_brief_from_research


def test_company_workspace_mapping_regression():
    """Exact reproduction of E:\\Quant-AI\\tests\\test_company_workspace_mapping.ts."""
    response_dict = {
        "request_id": "workspace-mapping-regression",
        "query": "AAPL",
        "company": {"symbol": "AAPL", "name": "Apple Inc.", "currency": "USD", "identifier_confidence": "high"},
        "candidates": [],
        "market": {"market_cap": 2345000000, "currency": "USD"},
        "history": [],
        "news": [],
        "analysis": None,
        "events": [],
        "sources": [],
        "market_intelligence": {
            "market_pulse": {"current_price": 100, "market_cap": None, "currency": "USD"},
            "price_history": {
                "intraday": [
                    {"timestamp": "2026-08-26T10:00:00Z", "close": 99},
                    {"timestamp": "2026-08-26T10:30:00Z", "close": 100},
                ],
                "daily": [
                    {"timestamp": "2026-08-20T00:00:00Z", "close": 95},
                    {"timestamp": "2026-08-26T00:00:00Z", "close": 100},
                ],
                "available_periods": ["1D", "1W", "1M", "1Y", "5Y"],
                "default_period": "1M",
                "freshness": {"state": "live", "cache_scope": "none"},
            },
            "market_signal": None,
            "recent_news": [],
            "event_radar": [],
            "executive_brief": None,
            "freshness": {
                "company": {"state": "live", "cache_scope": "none"},
                "market": {"state": "live", "cache_scope": "none"},
                "history": {"state": "live", "cache_scope": "none"},
                "news": {"state": "unavailable", "cache_scope": "none"},
                "events": {"state": "unavailable", "cache_scope": "none"},
                "analysis": {"state": "not_requested", "cache_scope": "none"},
            },
        },
        "company_deep_analysis": {
            "company_overview": {
                "ticker": "AAPL",
                "market_cap": 1234000000,
                "currency": "USD",
                "business_description": "Returned profile text only.",
            },
            "financial_health": {
                "revenue": 123,
                "net_income": None,
                "eps": 2.5,
                "profit_margin": 0.2,
                "operating_margin": 0.25,
                "total_cash": 75,
                "total_debt": 45,
                "currency": "USD",
                "fiscal_period_end": "2026-06-30",
            },
            "governance": None,
            "competitive_evidence": {
                "status": "unavailable",
                "competitors": [],
                "note": "Insufficient verified competitor data.",
            },
            "market_context": None,
            "recent_news": [],
            "events": [],
            "analyst_interpretation": None,
            "freshness": {
                "company": {"state": "live", "cache_scope": "none"},
                "financials": {"state": "live", "cache_scope": "none"},
                "governance": {"state": "unavailable", "cache_scope": "none"},
                "competitors": {"state": "unavailable", "cache_scope": "none"},
                "market": {"state": "live", "cache_scope": "none"},
                "news": {"state": "unavailable", "cache_scope": "none"},
                "events": {"state": "unavailable", "cache_scope": "none"},
                "analysis": {"state": "not_requested", "cache_scope": "none"},
            },
        },
        "status": {
            "overall": "partial",
            "market": "available",
            "financials": "available",
            "governance": "unavailable",
            "competitors": "unavailable",
            "history": "available",
            "news": "unavailable",
            "events": "unavailable",
            "company": "available",
            "ai": "not_requested",
        },
        "warnings": [],
    }

    res = TypedResearchResponse.model_validate(response_dict)
    brief = market_brief_from_research(res)

    assert ",".join(brief.priceHistory.availablePeriods) == "1D,1W,1M,1Y,5Y", (
        "Workspace added or removed returned history periods."
    )
    assert len(brief.priceHistory.daily) == 2 and len(brief.priceHistory.intraday) == 2, (
        "Workspace did not preserve returned history points."
    )
    assert brief.priceHistory.defaultPeriod == "1M", (
        "Workspace changed the returned default history period."
    )
    assert brief.deepAnalysis is not None and brief.deepAnalysis.profile.description == "Returned profile text only.", (
        "Workspace changed returned company profile text."
    )
    assert any(metric.label == "Revenue" and metric.value != "—" for metric in brief.deepAnalysis.financials), (
        "Workspace omitted returned revenue."
    )
    assert any(metric.label == "Net income" and metric.value == "—" for metric in brief.deepAnalysis.financials), (
        "Workspace did not retain missing financial data as unavailable."
    )
    market_cap_metric = next((m for m in brief.metrics if m.label == "Market cap"), None)
    assert market_cap_metric is not None and market_cap_metric.value != "—", (
        "Workspace did not use an existing returned market-cap fallback."
    )
    assert any(metric.label == "Operating margin" and metric.value != "—" for metric in brief.deepAnalysis.financials), (
        "Workspace omitted a returned compact Financial Health metric."
    )


def test_partial_research_mapping_integrity():
    """Verify mapping handles null deep analysis gracefully."""
    response_dict = {
        "request_id": "workspace-partial-regression",
        "query": "MSFT",
        "company": {"symbol": "MSFT", "name": "Microsoft Corp.", "currency": "USD", "identifier_confidence": "high"},
        "status": {
            "overall": "partial",
            "market": "unavailable",
            "financials": "unavailable",
            "governance": "unavailable",
            "competitors": "unavailable",
            "history": "unavailable",
            "news": "unavailable",
            "events": "unavailable",
            "company": "available",
            "ai": "not_requested",
        },
    }
    res = TypedResearchResponse.model_validate(response_dict)
    brief = market_brief_from_research(res)
    assert brief.ticker == "MSFT"
    assert brief.companyName == "Microsoft Corp."
    assert brief.deepAnalysis is None


def test_company_association_protection():
    """Verify ticker mismatch between overview and company identity does not contaminate identity."""
    response_dict = {
        "request_id": "workspace-isolation-regression",
        "query": "AAPL",
        "company": {"symbol": "AAPL", "name": "Apple Inc.", "currency": "USD", "identifier_confidence": "high"},
        "market": {"market_cap": 3000000000000, "currency": "USD"},
        "company_deep_analysis": {
            "company_overview": {
                "ticker": "AAPL",
                "business_description": "Apple profile.",
            },
            "financial_health": None,
            "governance": None,
            "competitive_evidence": {
                "status": "available",
                "competitors": ["MSFT", "GOOGL"],
                "note": "Primary competitors in technology platforms.",
            },
            "market_context": None,
            "recent_news": [],
            "events": [],
            "analyst_interpretation": None,
            "freshness": {
                "company": {"state": "live", "cache_scope": "none"},
                "financials": {"state": "unavailable", "cache_scope": "none"},
                "governance": {"state": "unavailable", "cache_scope": "none"},
                "competitors": {"state": "live", "cache_scope": "none"},
                "market": {"state": "live", "cache_scope": "none"},
                "news": {"state": "unavailable", "cache_scope": "none"},
                "events": {"state": "unavailable", "cache_scope": "none"},
                "analysis": {"state": "not_requested", "cache_scope": "none"},
            },
        },
        "status": {
            "overall": "partial",
            "market": "available",
            "financials": "unavailable",
            "governance": "unavailable",
            "competitors": "available",
            "history": "unavailable",
            "news": "unavailable",
            "events": "unavailable",
            "company": "available",
            "ai": "not_requested",
        },
    }
    res = TypedResearchResponse.model_validate(response_dict)
    brief = market_brief_from_research(res)
    assert brief.ticker == "AAPL"
    assert brief.deepAnalysis is not None
    assert brief.deepAnalysis.competitors.items == ["MSFT", "GOOGL"]
