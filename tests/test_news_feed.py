"""Tests for news feed processing, deduplication, safe URL validation, and template rendering."""

from __future__ import annotations

import pytest
from fastapi.templating import Jinja2Templates

from api.web.news import (
    NewsArticleView,
    NewsFeedView,
    format_news_article,
    is_safe_news_url,
    process_news_feed,
)


def test_is_safe_news_url():
    """Verify URL validation allows only http and https schemes."""
    assert is_safe_news_url("https://news.example.com/article1") is True
    assert is_safe_news_url("http://example.org/test") is True
    assert is_safe_news_url("HTTPS://EXAMPLE.COM/CAPS") is True

    # Disallowed/unsafe schemes
    assert is_safe_news_url("javascript:alert(1)") is False
    assert is_safe_news_url("data:text/html,<script>bad()</script>") is False
    assert is_safe_news_url("file:///C:/secrets.txt") is False
    assert is_safe_news_url("vbscript:run()") is False
    assert is_safe_news_url("//protocol-relative.com") is False
    assert is_safe_news_url("") is False
    assert is_safe_news_url(None) is False


def test_six_article_maximum():
    """Verify feed caps output at 6 articles even when 8 articles are provided."""
    raw_articles = [
        {
            "title": f"Testco fictional update {i}",
            "summary": f"Fictional test context number {i}",
            "publisher": "Testco Dispatch",
            "url": f"https://example.com/news/{i}",
            "published_at": f"2026-09-0{i+1}T10:00:00Z",
        }
        for i in range(8)
    ]

    feed = process_news_feed(raw_articles, limit=6)
    assert len(feed.articles) == 6
    assert feed.has_news is True


def test_duplicate_url_removal():
    """Verify articles with identical URLs are deduplicated while distinct articles are preserved."""
    raw_articles = [
        {
            "title": "Testco opens new testing facility",
            "summary": "First release context.",
            "publisher": "Newswire Alpha",
            "url": "https://example.com/testco-facility",
            "published_at": "2026-09-01T10:00:00Z",
        },
        {
            "title": "Testco opens new testing facility (reprint)",
            "summary": "Duplicate wire context.",
            "publisher": "Newswire Beta",
            "url": "https://example.com/testco-facility",  # duplicate URL
            "published_at": "2026-09-01T10:05:00Z",
        },
        {
            "title": "Testco reports steady fictional operations",
            "summary": "Different story context.",
            "publisher": "Newswire Alpha",
            "url": "https://example.com/testco-operations",
            "published_at": "2026-09-02T10:00:00Z",
        },
    ]

    feed = process_news_feed(raw_articles)
    assert len(feed.articles) == 2
    # Chronological sort places Sep 02 before Sep 01
    assert feed.articles[0].url == "https://example.com/testco-operations"
    assert feed.articles[1].url == "https://example.com/testco-facility"


def test_chronological_ordering():
    """Verify articles are sorted in chronological order (newest first)."""
    raw_articles = [
        {
            "title": "Oldest fictional report",
            "published_at": "2026-09-01T08:00:00Z",
            "url": "https://example.com/1",
        },
        {
            "title": "Newest fictional report",
            "published_at": "2026-09-03T08:00:00Z",
            "url": "https://example.com/3",
        },
        {
            "title": "Middle fictional report",
            "published_at": "2026-09-02T08:00:00Z",
            "url": "https://example.com/2",
        },
    ]

    feed = process_news_feed(raw_articles)
    assert len(feed.articles) == 3
    assert feed.articles[0].title == "Newest fictional report"
    assert feed.articles[1].title == "Middle fictional report"
    assert feed.articles[2].title == "Oldest fictional report"


def test_missing_optional_fields_safely_handled():
    """Verify articles missing summary, publisher, date, or URL render cleanly."""
    raw = {
        "title": "Testco headline with minimal fields",
        "summary": None,
        "publisher": None,
        "url": None,
        "published_at": None,
    }

    view = format_news_article(raw)
    assert view.title == "Testco headline with minimal fields"
    assert view.summary is None
    assert view.publisher is None
    assert view.url is None
    assert view.is_safe_url is False
    assert view.formatted_date is None
    assert view.meta_line == "Source metadata unavailable"


def test_unsafe_url_neutralized():
    """Verify javascript: and unsafe URLs are marked not safe."""
    raw = {
        "title": "Malicious payload link",
        "url": "javascript:alert('xss')",
    }
    view = format_news_article(raw)
    assert view.is_safe_url is False
    assert view.url is None  # neutralized


def test_empty_news_state():
    """Verify empty article list produces empty feed state."""
    feed = process_news_feed([])
    assert len(feed.articles) == 0
    assert feed.has_news is False
    assert feed.is_unavailable is False


def test_unavailable_news_state():
    """Verify unavailable state sets flag correctly."""
    feed = process_news_feed([], is_unavailable=True)
    assert len(feed.articles) == 0
    assert feed.has_news is False
    assert feed.is_unavailable is True


def test_news_template_rendering_security():
    """Verify rendered HTML includes rel=noopener noreferrer on safe links and no link on unsafe ones."""
    templates = Jinja2Templates(directory="templates")

    feed = NewsFeedView(
        articles=[
            NewsArticleView(
                title="Testco expands renewable research",
                summary="Fictional test company announces renewable energy initiative.",
                publisher="Global Energy Gazette",
                url="https://example.com/renewable-news",
                is_safe_url=True,
                formatted_date="Sep 5, 2026",
                meta_line="Global Energy Gazette · Sep 5, 2026",
            ),
            NewsArticleView(
                title="Unlinked brief report",
                summary=None,
                publisher="Local Wire",
                url=None,
                is_safe_url=False,
                formatted_date="Sep 4, 2026",
                meta_line="Local Wire · Sep 4, 2026",
            ),
        ],
        has_news=True,
    )

    html = templates.get_template("partials/news_feed.html").render({"news_feed": feed})

    assert "Recent news" in html
    assert "Testco expands renewable research" in html
    assert 'href="https://example.com/renewable-news"' in html
    assert 'rel="noopener noreferrer"' in html
    assert 'target="_blank"' in html
    # Second article has no URL, so title should be plain text and no href
    assert "Unlinked brief report" in html
    assert 'href="None"' not in html
