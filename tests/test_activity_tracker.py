"""Tests for recent activity tracking, 5-item limit, ordering, and presentation.

Step D acceptance criteria:
1. Five recent searches.
2. Query label, mode, completion and confidence.
3. Activity ordering (newest first).
4. Five-item limit.
"""

from __future__ import annotations

from api.web.activity import (
    ResearchActivityItem,
    add_research_activity,
    format_activity_entry,
)


def test_activity_ordering_newest_first():
    """Verify that successive activities are prepended so the newest appears first."""
    history: list[dict] = []

    history = add_research_activity(history, query="AAPL", mode="market_intelligence", status="completed", confidence="high")
    history = add_research_activity(history, query="MSFT", mode="company_deep_analysis", status="completed", confidence="medium")
    history = add_research_activity(history, query="GOOGL", mode="market_intelligence", status="completed", confidence="high")

    assert len(history) == 3
    assert history[0]["query"] == "GOOGL"
    assert history[1]["query"] == "MSFT"
    assert history[2]["query"] == "AAPL"


def test_five_item_limit_strictly_enforced():
    """Verify that adding more than 5 activities strictly caps the list at the 5 most recent."""
    history: list[dict] = []
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"]

    for ticker in tickers:
        history = add_research_activity(
            history,
            query=ticker,
            mode="market_intelligence",
            status="completed",
            confidence="high",
        )

    assert len(history) == 5
    # Most recent 5 in reverse order of addition: META, TSLA, NVDA, AMZN, GOOGL
    assert [item["query"] for item in history] == ["META", "TSLA", "NVDA", "AMZN", "GOOGL"]


def test_activity_fields_and_formatting():
    """Verify query label, mode, completion status, and confidence are preserved."""
    item = ResearchActivityItem(
        id="act-1",
        query="NVDA",
        type="market_intelligence",
        status="completed",
        confidence="high",
    )
    formatted = format_activity_entry(item)
    assert formatted["query"] == "NVDA"
    assert formatted["type"] == "Market Intelligence"
    assert formatted["status"] == "completed"
    assert formatted["confidence"] == "high"
    assert "subtitle" in formatted
    assert "Market Intelligence · completed · high" in formatted["subtitle"]


def test_activity_optional_confidence():
    """Verify activity entry when confidence is omitted or None."""
    item = ResearchActivityItem(
        id="act-2",
        query="TST",
        type="company_deep_analysis",
        status="partial",
        confidence=None,
    )
    formatted = format_activity_entry(item)
    assert formatted["confidence"] is None
    assert formatted["subtitle"] == "Company Deep Analysis · partial"
