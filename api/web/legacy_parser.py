"""Legacy markdown table and brief parser for QuantAI.

Pure-Python implementation of the legacy AgentOS conversational response parser
from client/src/lib/market.ts. Extracts financial metrics, price history charts,
and news bullet points from unstructured or semi-structured markdown responses.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Literal

from api.web.contracts import (
    BriefNewsItem,
    ChartPoint,
    MarketBrief,
    MarketBriefPriceHistory,
    Metric,
)


@dataclass
class MarkdownTable:
    headers: list[str]
    rows: list[list[str]]


METRIC_KEYS: list[tuple[str, list[str]]] = [
    ("Market cap", ["market cap", "market capitalization"]),
    ("P / E ratio", ["p/e", "p/e ratio", "pe ratio", "price to earnings"]),
    ("52-week high", ["52 week high", "52-week high"]),
    ("52-week low", ["52 week low", "52-week low"]),
    ("Volume", ["volume", "avg volume", "average volume"]),
    ("Dividend yield", ["dividend yield"]),
]


def clean_cell(value: str) -> str:
    """Strip HTML tags, bold formatting, backticks, and outer whitespace."""
    no_html = re.sub(r"<[^>]+>", "", value)
    no_bold = no_html.replace("**", "")
    no_code = no_bold.replace("`", "")
    return no_code.strip()


def parse_tables(markdown: str) -> list[MarkdownTable]:
    """Parse Markdown tables with headers and divider rows."""
    lines = markdown.split("\n")
    tables: list[MarkdownTable] = []
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        separator = lines[index + 1].strip() if index + 1 < len(lines) else ""
        if not line.startswith("|") or not separator.startswith("|") or not re.search(r"[-:]{3,}", separator):
            index += 1
            continue

        headers = [clean_cell(cell).lower() for cell in line.split("|")[1:-1]]
        rows: list[list[str]] = []
        index += 2
        while index < len(lines) and lines[index].strip().startswith("|"):
            row_cells = [clean_cell(cell) for cell in lines[index].strip().split("|")[1:-1]]
            rows.append(row_cells)
            index += 1
        tables.append(MarkdownTable(headers=headers, rows=rows))

    return tables


def normalize_term(value: str) -> str:
    """Normalize text to alphanumeric lower-case words for fuzzy comparison."""
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def find_table_value(tables: list[MarkdownTable], terms: list[str]) -> str:
    """Search tables for matching label header/column or raw row cells."""
    normalized_terms = [normalize_term(term) for term in terms]

    for table in tables:
        label_index = -1
        value_index = -1
        for idx, header in enumerate(table.headers):
            if re.search(r"metric|measure|item|indicator|field", header):
                label_index = idx
            if re.search(r"value|amount|data|latest|current", header):
                value_index = idx

        for row in table.rows:
            label_col = label_index if label_index >= 0 and label_index < len(row) else 0
            label = normalize_term(row[label_col]) if label_col < len(row) else ""
            if any(re.search(rf"\b{re.escape(term)}\b", label) for term in normalized_terms):
                val_col = value_index if value_index >= 0 and value_index < len(row) else (1 if len(row) > 1 else 0)
                return row[val_col] if val_col < len(row) and row[val_col] else "—"

    # Flat row fallback search for currency or digits
    for table in tables:
        for row in table.rows:
            joined = normalize_term(" ".join(row))
            if any(re.search(rf"\b{re.escape(term)}\b", joined) for term in normalized_terms):
                for cell in row:
                    if re.search(r"[$€£₹¥]|\d", cell):
                        return cell
    return "—"


def extract_fallback_value(markdown: str, terms: list[str]) -> str:
    """Extract numeric or currency values from raw lines when absent in tables."""
    normalized_terms = [normalize_term(term) for term in terms]
    lines = markdown.split("\n")
    for line in lines:
        normalized_line = normalize_term(line)
        if any(re.search(rf"\b{re.escape(term)}\b", normalized_line) for term in normalized_terms):
            match = re.search(r"([$€£₹¥]\s?[\d,.]+(?:[BMKT])?|[\d,.]+%?|[\d,.]+\s?[BMKT])", line, re.IGNORECASE)
            if match:
                return match.group(0).strip()
    return "—"


def find_value(tables: list[MarkdownTable], markdown: str, terms: list[str]) -> str:
    """Find value in parsed tables, falling back to line pattern matching."""
    from_table = find_table_value(tables, terms)
    return from_table if from_table != "—" else extract_fallback_value(markdown, terms)


def display_value(value: str) -> str:
    """Normalize empty or unavailable tokens to em-dash."""
    if not value or value == "—" or re.fullmatch(r"unavailable", value.strip(), re.IGNORECASE):
        return "—"
    return value.strip()


def number_from_cell(value: str) -> float:
    """Parse numeric values from currency or parenthesized negative strings."""
    cleaned = re.sub(r"[$€£₹¥,\s]", "", value)
    cleaned = re.sub(r"\((.*)\)", r"-\1", cleaned)
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    return float(match.group(0)) if match else math.nan


def extract_chart(tables: list[MarkdownTable]) -> list[ChartPoint]:
    """Extract numeric chart points from date and price columns in tables."""
    for table in tables:
        date_index = -1
        price_index = -1
        for idx, header in enumerate(table.headers):
            if re.search(r"date|day|period|time", header):
                date_index = idx
            if re.search(r"close|price|value|last", header):
                price_index = idx

        if date_index < 0 or price_index < 0:
            continue

        points: list[ChartPoint] = []
        for row in table.rows:
            if date_index < len(row) and price_index < len(row):
                label = row[date_index]
                val = number_from_cell(row[price_index])
                if label and math.isfinite(val):
                    points.append(ChartPoint(label=label, value=val))

        if len(points) >= 2:
            return points[-40:]

    return []


def extract_news(markdown: str) -> list[str]:
    """Extract news bullet points from news sections or bulleted lines."""
    lines = markdown.split("\n")
    section_start = -1
    for idx, line in enumerate(lines):
        if re.search(r"recent news|news (?:highlights|summary)|latest news", line, re.IGNORECASE):
            section_start = idx
            break

    candidates = lines[section_start + 1 : section_start + 12] if section_start >= 0 else lines
    news_items: list[str] = []
    for line in candidates:
        if re.search(r"^\s*(?:[-*•]|\d+\.)\s+", line):
            cleaned = re.sub(r"^\s*(?:[-*•]|\d+\.)\s+", "", line)
            cleaned = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cleaned).strip()
            if len(cleaned) > 12:
                news_items.append(cleaned)
                if len(news_items) >= 3:
                    break
    return news_items


def tone_for(value: str) -> Literal["neutral", "positive", "negative"]:
    """Determine semantic tone from signs or directional keywords."""
    if re.search(r"^\+|up|gain|positive", value, re.IGNORECASE):
        return "positive"
    if re.search(r"^-|down|loss|negative", value, re.IGNORECASE):
        return "negative"
    return "neutral"


def parse_market_brief(markdown: str) -> MarketBrief:
    """Parse unstructured conversational AgentOS response into MarketBrief."""
    tables = parse_tables(markdown)

    quote = display_value(find_value(tables, markdown, ["current price", "stock price", "last price", "price"]))
    change = display_value(find_value(tables, markdown, ["day change", "change", "daily change", "percent change"]))

    metrics = [
        Metric(
            label=label,
            value=display_value(find_value(tables, markdown, matches)),
            tone=tone_for(display_value(find_value(tables, markdown, matches))),
        )
        for label, matches in METRIC_KEYS
    ]

    chart_points = extract_chart(tables)
    raw_news = extract_news(markdown)
    news_items = [
        BriefNewsItem(
            title=title,
            summary=None,
            publisher=None,
            publishedAt=None,
            url=None,
            sentiment=None,
        )
        for title in raw_news
    ]

    return MarketBrief(
        companyName=display_value(find_value(tables, markdown, ["company name", "company"])),
        ticker=display_value(find_value(tables, markdown, ["ticker", "symbol"])),
        exchange=display_value(find_value(tables, markdown, ["exchange"])),
        sector=display_value(find_value(tables, markdown, ["sector"])),
        industry=display_value(find_value(tables, markdown, ["industry"])),
        quoteLabel="Current price",
        quote=quote,
        change=change,
        metrics=metrics,
        news=news_items,
        chart=chart_points,
        priceHistory=MarketBriefPriceHistory(
            intraday=[],
            daily=chart_points,
            availablePeriods=[],
            defaultPeriod="1M",
        ),
        analysis=markdown,
        aiInterpretationNotice=None,
        signal=None,
        events=[],
        sources=[],
        warnings=[],
        freshness=[],
        deepAnalysis=None,
    )


def empty_market_brief() -> MarketBrief:
    """Return fallback empty MarketBrief awaiting research."""
    return MarketBrief(
        companyName="—",
        ticker="—",
        exchange="—",
        sector="—",
        industry="—",
        quoteLabel="Current price",
        quote="—",
        change="Awaiting AgentOS research",
        metrics=[Metric(label=label, value="—", tone="neutral") for label, _ in METRIC_KEYS],
        news=[],
        chart=[],
        priceHistory=MarketBriefPriceHistory(
            intraday=[],
            daily=[],
            availablePeriods=[],
            defaultPeriod="1M",
        ),
        analysis="",
        aiInterpretationNotice=None,
        signal=None,
        events=[],
        sources=[],
        warnings=[],
        freshness=[],
        deepAnalysis=None,
    )
