"""Unit tests for the legacy markdown table and brief parser.

Verifies full parity with client/src/lib/market.ts parsing logic:
1. Cell cleaning (HTML tags, bold asterisks, backticks).
2. Table extraction with header and divider recognition.
3. Metric search in tables and fallback line extraction.
4. Chart coordinate parsing with currency and negative parenthetical handling.
5. News bullet point extraction and link sanitization.
6. Semantic tone classification.
7. Full MarketBrief view model assembly and empty fallback structure.
"""

import math
from api.web.legacy_parser import (
    clean_cell,
    display_value,
    empty_market_brief,
    extract_chart,
    extract_fallback_value,
    extract_news,
    find_table_value,
    find_value,
    normalize_term,
    number_from_cell,
    parse_market_brief,
    parse_tables,
    tone_for,
)


SAMPLE_MARKDOWN = """
# Apple Inc. (AAPL) Research Brief

| Metric | Value |
|---|---|
| Company Name | Apple Inc. |
| Ticker | AAPL |
| Exchange | NASDAQ |
| Sector | Technology |
| Industry | Consumer Electronics |
| Current Price | $185.50 |
| Day Change | +$2.30 (+1.25%) |
| Market Cap | $2.85T |
| P / E Ratio | 29.5 |
| 52-Week High | $199.62 |
| 52-Week Low | $164.08 |
| Volume | 54.2M |
| Dividend Yield | 0.52% |

### Historical Price
| Date | Close |
|---|---|
| 2026-01-02 | 182.10 |
| 2026-01-03 | 183.40 |
| 2026-01-04 | 185.50 |

### Recent News
- [Apple expands enterprise AI services across devices](https://example.com/news1)
* Supply chain partners report steady production throughput for Q1
1. Services segment hits new quarterly revenue milestone globally
"""


def test_clean_cell():
    """clean_cell removes HTML tags, bold asterisks, and backticks."""
    assert clean_cell("<b>$185.50</b>") == "$185.50"
    assert clean_cell("**AAPL**") == "AAPL"
    assert clean_cell("`29.5`") == "29.5"
    assert clean_cell("  <span class='bold'>**+1.2%**</span>  ") == "+1.2%"


def test_normalize_term():
    """normalize_term converts to lowercase alphanumeric words."""
    assert normalize_term("Market Cap (USD)") == "market cap usd"
    assert normalize_term("P/E Ratio") == "p e ratio"
    assert normalize_term("52-Week High") == "52 week high"


def test_parse_tables():
    """parse_tables extracts headers and row cells from markdown tables."""
    tables = parse_tables(SAMPLE_MARKDOWN)
    assert len(tables) == 2

    # First table: metrics
    metric_table = tables[0]
    assert metric_table.headers == ["metric", "value"]
    assert len(metric_table.rows) == 13
    assert metric_table.rows[0] == ["Company Name", "Apple Inc."]

    # Second table: prices
    price_table = tables[1]
    assert price_table.headers == ["date", "close"]
    assert len(price_table.rows) == 3
    assert price_table.rows[0] == ["2026-01-02", "182.10"]


def test_find_table_value():
    """find_table_value extracts cell content matching term aliases."""
    tables = parse_tables(SAMPLE_MARKDOWN)
    assert find_table_value(tables, ["market cap", "market capitalization"]) == "$2.85T"
    assert find_table_value(tables, ["pe ratio", "p/e"]) == "29.5"
    assert find_table_value(tables, ["nonexistent metric"]) == "—"


def test_extract_fallback_value():
    """extract_fallback_value scans lines for values matching currency/multiplier patterns."""
    text = "The estimated Market Capitalization for Microsoft is $3.15T currently.\nCurrent P/E is 35.4x."
    assert extract_fallback_value(text, ["market capitalization"]) == "$3.15T"
    assert extract_fallback_value(text, ["unknown"]) == "—"


def test_find_value_prefers_table_over_fallback():
    """find_value returns table match first, fallback second."""
    tables = parse_tables(SAMPLE_MARKDOWN)
    assert find_value(tables, SAMPLE_MARKDOWN, ["current price"]) == "$185.50"

    # When table does not have the term, it uses text fallback
    fallback_markdown = "Estimated Total Debt stands at $105.2B as of fiscal year end."
    assert find_value([], fallback_markdown, ["total debt"]) == "$105.2B"


def test_display_value():
    """display_value normalizes missing or unavailable values."""
    assert display_value("") == "—"
    assert display_value("—") == "—"
    assert display_value("unavailable") == "—"
    assert display_value("UNAVAILABLE") == "—"
    assert display_value("  $185.50  ") == "$185.50"


def test_number_from_cell():
    """number_from_cell parses positive, negative, and parenthetical currency."""
    assert number_from_cell("$185.50") == 185.50
    assert number_from_cell("€ 1,234.50") == 1234.50
    assert number_from_cell("-$25.10") == -25.10
    assert number_from_cell("($15.75)") == -15.75
    assert math.isnan(number_from_cell("no-digits-here"))


def test_extract_chart():
    """extract_chart extracts ordered ChartPoints from date/price tables."""
    tables = parse_tables(SAMPLE_MARKDOWN)
    points = extract_chart(tables)
    assert len(points) == 3
    assert points[0].label == "2026-01-02"
    assert points[0].value == 182.10
    assert points[2].label == "2026-01-04"
    assert points[2].value == 185.50


def test_extract_news():
    """extract_news extracts up to 3 news lines and strips markdown links."""
    news = extract_news(SAMPLE_MARKDOWN)
    assert len(news) == 3
    assert news[0] == "Apple expands enterprise AI services across devices"
    assert "https://" not in news[0]
    assert news[1] == "Supply chain partners report steady production throughput for Q1"
    assert news[2] == "Services segment hits new quarterly revenue milestone globally"


def test_tone_for():
    """tone_for classifies semantic tone accurately."""
    assert tone_for("+$2.30") == "positive"
    assert tone_for("up 4.5%") == "positive"
    assert tone_for("gain") == "positive"
    assert tone_for("-$1.15") == "negative"
    assert tone_for("down 2.1%") == "negative"
    assert tone_for("loss") == "negative"
    assert tone_for("$185.50") == "neutral"


def test_parse_market_brief_full_document():
    """parse_market_brief converts raw markdown into a populated MarketBrief."""
    brief = parse_market_brief(SAMPLE_MARKDOWN)
    assert brief.companyName == "Apple Inc."
    assert brief.ticker == "AAPL"
    assert brief.exchange == "NASDAQ"
    assert brief.sector == "Technology"
    assert brief.industry == "Consumer Electronics"
    assert brief.quote == "$185.50"
    assert brief.change == "+$2.30 (+1.25%)"
    assert len(brief.metrics) == 6
    assert brief.metrics[0].label == "Market cap"
    assert brief.metrics[0].value == "$2.85T"
    assert len(brief.news) == 3
    assert len(brief.chart) == 3
    assert brief.analysis == SAMPLE_MARKDOWN


def test_empty_market_brief():
    """empty_market_brief returns awaiting state placeholders."""
    brief = empty_market_brief()
    assert brief.companyName == "—"
    assert brief.ticker == "—"
    assert brief.change == "Awaiting AgentOS research"
    assert len(brief.metrics) == 6
    for m in brief.metrics:
        assert m.value == "—"
        assert m.tone == "neutral"
    assert len(brief.news) == 0
    assert len(brief.chart) == 0
