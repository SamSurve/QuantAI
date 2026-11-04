"""Port of E:\\Quant-AI\\tests\\test_news_context_mapping.ts to pytest.

Verifies:
- Provider news summary preservation
- Missing provider summary kept None
- Returned article URL preservation
- Returned publisher preservation
- Returned publication timestamp preservation
"""

from __future__ import annotations

import pytest

from api.web.contracts import TypedResearchResponse
from api.web.presenters import market_brief_from_research


def test_news_context_mapping_regression():
    """Exact reproduction of E:\\Quant-AI\\tests\\test_news_context_mapping.ts."""
    response_dict = {
        "request_id": "news-context-regression",
        "query": "AAPL",
        "company": {"symbol": "AAPL", "name": "Apple Inc.", "currency": "USD", "identifier_confidence": "high"},
        "candidates": [],
        "market": None,
        "history": [],
        "news": [
            {
                "title": "Provider-supplied headline",
                "summary": "Provider-supplied factual article context.",
                "publisher": "Provider source",
                "url": "https://example.com/original-article",
                "published_at": "2026-08-25T12:00:00Z",
                "relevance": "medium",
                "sentiment": None,
            },
            {
                "title": "Headline without returned context",
                "summary": None,
                "publisher": "Provider source",
                "url": "https://example.com/second-original-article",
                "published_at": "2026-08-25T13:00:00Z",
                "relevance": "medium",
                "sentiment": None,
            },
        ],
        "analysis": None,
        "events": [],
        "sources": [],
        "status": {
            "overall": "partial",
            "market": "unavailable",
            "financials": "unavailable",
            "governance": "unavailable",
            "competitors": "unavailable",
            "history": "unavailable",
            "news": "available",
            "events": "unavailable",
            "company": "available",
            "ai": "unavailable",
        },
        "warnings": [],
    }

    res = TypedResearchResponse.model_validate(response_dict)
    brief = market_brief_from_research(res)

    assert brief.news[0].summary == "Provider-supplied factual article context.", (
        "Provider news summary was not preserved."
    )
    assert brief.news[1].summary is None, (
        "Missing provider summary was not kept empty."
    )
    assert brief.news[0].url == "https://example.com/original-article", (
        "Returned article URL was changed."
    )
    assert brief.news[0].publisher == "Provider source", (
        "Returned publisher was changed."
    )
    assert brief.news[0].publishedAt == "2026-08-25T12:00:00Z", (
        "Returned publication timestamp was changed."
    )
