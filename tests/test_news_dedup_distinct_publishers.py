"""Regression test for news deduplication with distinct publishers and URLs.

Owner requirement:
- Add a news regression test with two articles that have the same headline,
  different publishers, and different URLs. Both must remain.
- Run the test against the existing Part 16 implementation first.
- Change production news code only if the test fails; preserve genuine duplicate-URL deduplication.
"""

from __future__ import annotations

from api.web.news import process_news_feed


def test_news_dedup_preserves_same_headline_different_publishers():
    """Verify two articles with identical headline but different publishers and URLs both remain."""
    headline = "Testco Reports Record Q3 Revenue and Margin Expansion"
    raw_articles = [
        {
            "title": headline,
            "publisher": "Financial Times Wire",
            "url": "https://example.com/ft/testco-record-q3",
            "published_at": "2026-10-15T08:00:00Z",
            "summary": "First publisher report on Testco earnings.",
        },
        {
            "title": headline,
            "publisher": "Bloomberg Desk",
            "url": "https://example.com/bbg/testco-record-q3-deepdive",
            "published_at": "2026-10-15T08:15:00Z",
            "summary": "Second publisher report analyzing Testco margins.",
        },
    ]

    feed = process_news_feed(raw_articles)

    assert feed.has_news is True
    assert len(feed.articles) == 2, f"Expected 2 articles, found {len(feed.articles)}"

    publishers = {a.publisher for a in feed.articles}
    assert publishers == {"Financial Times Wire", "Bloomberg Desk"}

    urls = {a.url for a in feed.articles}
    assert urls == {
        "https://example.com/ft/testco-record-q3",
        "https://example.com/bbg/testco-record-q3-deepdive",
    }


def test_genuine_duplicate_url_is_deduplicated():
    """Verify that articles sharing identical URL are still deduplicated."""
    raw_articles = [
        {
            "title": "Testco Expands Operations",
            "publisher": "Market Desk A",
            "url": "https://example.com/story/100",
            "published_at": "2026-10-15T09:00:00Z",
        },
        {
            "title": "Testco Expands Operations (Updated)",
            "publisher": "Market Desk B",
            "url": "https://example.com/story/100",
            "published_at": "2026-10-15T09:30:00Z",
        },
    ]

    feed = process_news_feed(raw_articles)
    assert len(feed.articles) == 1
