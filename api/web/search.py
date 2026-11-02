"""Search utilities and normalization for QuantAI research interface.

Preserves starter tickers, query trimming, and entity search rules.
"""

from __future__ import annotations

STARTER_TICKERS: list[str] = ["AAPL", "MSFT", "NVDA", "TSLA"]


def normalize_search_query(query: str | None) -> str:
    """Normalize user-entered company name or ticker query.

    Trims leading/trailing whitespace and preserves case.
    Returns empty string for whitespace-only or None inputs.
    """
    if not query:
        return ""
    return query.strip()
