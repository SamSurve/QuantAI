"""Recent news feed presentation models, deduplication, safe URL validation, and formatting."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict

from api.web.formatters import MONTH_NAMES


def is_safe_news_url(url: str | None) -> bool:
    """Return True if URL is non-empty and uses an allowed web scheme (http/https)."""
    if not url:
        return False
    u = url.strip().lower()
    return u.startswith("http://") or u.startswith("https://")


def format_news_date(date_str: str | None) -> str | None:
    """Format an ISO date string into 'Mon D, YYYY' matching displayDate in Home.tsx."""
    if not date_str:
        return None
    stripped = date_str.strip()
    try:
        # Normalize ISO strings (e.g. 2026-08-25T12:00:00Z)
        clean = stripped.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean)
        month = MONTH_NAMES[dt.month - 1]
        return f"{month} {dt.day}, {dt.year}"
    except Exception:
        # Fallback to leading YYYY-MM-DD slice if unparseable
        if len(stripped) >= 10:
            return stripped[:10]
        return stripped


class NewsArticleView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str
    summary: str | None = None
    publisher: str | None = None
    url: str | None = None
    is_safe_url: bool = False
    published_at: str | None = None
    formatted_date: str | None = None
    meta_line: str = "Source metadata unavailable"
    sentiment: str | None = None


class NewsFeedView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    articles: list[NewsArticleView] = []
    has_news: bool = False
    is_unavailable: bool = False


def format_news_article(item: Any) -> NewsArticleView:
    """Format a raw news article (dict, Pydantic model, or BriefNewsItem) into a view model."""
    if isinstance(item, dict):
        title = str(item.get("title") or "").strip()
        summary = item.get("summary")
        publisher = item.get("publisher")
        raw_url = item.get("url")
        published_at = item.get("published_at") or item.get("publishedAt")
        sentiment = item.get("sentiment")
    else:
        title = str(getattr(item, "title", "") or "").strip()
        summary = getattr(item, "summary", None)
        publisher = getattr(item, "publisher", None)
        raw_url = getattr(item, "url", None)
        published_at = getattr(item, "published_at", None) or getattr(item, "publishedAt", None)
        sentiment = getattr(item, "sentiment", None)

    summary_str = summary.strip() if (summary and isinstance(summary, str) and summary.strip()) else None
    publisher_str = publisher.strip() if (publisher and isinstance(publisher, str) and publisher.strip()) else None

    safe_url = raw_url.strip() if (raw_url and is_safe_news_url(raw_url)) else None
    is_safe = safe_url is not None

    formatted_date = format_news_date(published_at)

    meta_parts = [p for p in [publisher_str, formatted_date] if p]
    meta_line = " · ".join(meta_parts) if meta_parts else "Source metadata unavailable"

    return NewsArticleView(
        title=title,
        summary=summary_str,
        publisher=publisher_str,
        url=safe_url,
        is_safe_url=is_safe,
        published_at=published_at,
        formatted_date=formatted_date,
        meta_line=meta_line,
        sentiment=sentiment,
    )


def process_news_feed(
    raw_articles: list[Any] | None,
    limit: int = 6,
    is_unavailable: bool = False,
) -> NewsFeedView:
    """Deduplicate, sort chronologically, and limit news articles to maximum 6."""
    if is_unavailable or not raw_articles:
        return NewsFeedView(
            articles=[],
            has_news=False,
            is_unavailable=is_unavailable,
        )

    # Deduplicate by URL (or title if no URL)
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    deduped: list[Any] = []

    for item in raw_articles:
        if isinstance(item, dict):
            url = (item.get("url") or "").strip().lower()
            title = (item.get("title") or "").strip().lower()
        else:
            url = (getattr(item, "url", None) or "").strip().lower()
            title = (getattr(item, "title", None) or "").strip().lower()

        if url:
            if url in seen_urls:
                continue
            seen_urls.add(url)
        else:
            if title and title in seen_titles:
                continue
            if title:
                seen_titles.add(title)

        deduped.append(item)

    # Chronological sort (newest first where published date is available)
    def sort_key(x: Any) -> str:
        if isinstance(x, dict):
            return str(x.get("published_at") or x.get("publishedAt") or "")
        return str(getattr(x, "published_at", None) or getattr(x, "publishedAt", None) or "")

    # Only sort if there are parseable date strings, otherwise preserve stable order
    has_dates = any(sort_key(x) for x in deduped)
    if has_dates:
        # Sort descending (newest first)
        deduped = sorted(deduped, key=sort_key, reverse=True)

    articles = [format_news_article(item) for item in deduped[:limit]]

    return NewsFeedView(
        articles=articles,
        has_news=len(articles) > 0,
        is_unavailable=False,
    )
