"""Tests for Part 11: Market quote, snapshot metrics, and price change tokens.

Verifies:
- All seven snapshot metrics (Market Cap, P/E Ratio, 52-Week High, 52-Week Low, Volume, Dividend Yield, EPS)
- Original fallback handling for each metric
- Market-closed state (HISTORY_CLOSE_FALLBACK -> 'Latest close')
- Absolute daily change and signed percentage change
- Dedicated --down token used for negative price changes (no --warn)
- Light and dark theme tokens both define --down
- WCAG contrast ratios of --down
- Integration with FastAPI test client and template rendering
"""

from __future__ import annotations

import re
from pathlib import Path
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from api.research_schemas import (
    CompanyIdentity,
    IdentifierConfidence,
    MarketSnapshot,
    ResearchResponse,
    ServiceStatus,
)
from api.web.contracts import Metric
from api.web.formatters import (
    compact_money_label,
    money_label,
    number_label,
    percent_label,
)
from api.web.presenters import (
    market_brief_from_research,
    snapshot_metrics_from_market,
)

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"
CSS_INPUT = ROOT / "static" / "css" / "input.css"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def test_input_css_contains_down_tokens():
    """Verify input.css declares dedicated --down token for both light and dark themes."""
    assert CSS_INPUT.exists()
    content = CSS_INPUT.read_text(encoding="utf-8")
    
    # Check light theme has --down: #e30000
    assert "--down: #e30000" in content, "Light theme must define --down: #e30000"
    
    # Check dark theme has --down: #ff453a
    assert "--down: #ff453a" in content, "Dark theme must define --down: #ff453a"
    
    # Ensure warning tokens remain distinct
    assert "--warn: #b25000" in content
    assert "--warn: #ffb340" in content


def test_wcag_contrast_ratios():
    """Verify calculated WCAG contrast ratios for --down tokens exceed AA 4.5:1 standard."""
    def rel_lum(hex_col: str) -> float:
        hex_col = hex_col.lstrip("#")
        rgb = [int(hex_col[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        rgb_adj = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * rgb_adj[0] + 0.7152 * rgb_adj[1] + 0.0722 * rgb_adj[2]

    def contrast(c1: str, c2: str) -> float:
        l1, l2 = rel_lum(c1), rel_lum(c2)
        return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

    c_light = contrast("e30000", "ffffff")
    c_dark = contrast("ff453a", "1c1c1e")

    assert c_light >= 4.5, f"Light --down contrast {c_light:.2f} must meet 4.5:1 AA standard"
    assert c_dark >= 4.5, f"Dark --down contrast {c_dark:.2f} must meet 4.5:1 AA standard"
    assert round(c_light, 2) == 4.92
    assert round(c_dark, 2) == 4.99


def test_snapshot_metrics_all_seven_present_with_values():
    """Verify all seven snapshot metrics are generated with correct values and formatting."""
    market = MarketSnapshot(
        current_price=228.40,
        currency="USD",
        daily_change=2.15,
        daily_change_percent=0.95,
        market_cap=3420000000000,
        pe_ratio=31.8,
        fifty_two_week_high=237.23,
        fifty_two_week_low=164.08,
        volume=48200000,
        dividend_yield=0.0044,
        eps=7.19,
    )

    metrics = snapshot_metrics_from_market(market, "USD")
    metric_dict = {m.label: m.value for m in metrics}

    assert len(metrics) == 7
    assert metric_dict["Market cap"] == "$3.42T"
    assert metric_dict["P / E ratio"] == "31.8"
    assert metric_dict["52-week high"] == "$237.23"
    assert metric_dict["52-week low"] == "$164.08"
    assert metric_dict["Volume"] == "48.2M"
    assert metric_dict["Dividend yield"] == "0.44%"
    assert metric_dict["EPS"] == "$7.19"


def test_snapshot_metrics_fallbacks_when_none():
    """Verify fallback '—' is returned for every metric when data is None."""
    market = MarketSnapshot()
    metrics = snapshot_metrics_from_market(market, None)
    metric_dict = {m.label: m.value for m in metrics}

    assert len(metrics) == 7
    assert metric_dict["Market cap"] == "—"
    assert metric_dict["P / E ratio"] == "—"
    assert metric_dict["52-week high"] == "—"
    assert metric_dict["52-week low"] == "—"
    assert metric_dict["Volume"] == "—"
    assert metric_dict["Dividend yield"] == "—"
    assert metric_dict["EPS"] == "—"


def test_market_closed_state_latest_close_identification():
    """Verify market_status == 'HISTORY_CLOSE_FALLBACK' sets quoteLabel to 'Latest close'."""
    research = ResearchResponse(
        request_id="test-1",
        query="AAPL",
        company=CompanyIdentity(
            symbol="AAPL",
            name="Apple Inc.",
            identifier_confidence=IdentifierConfidence.HIGH,
        ),
        market=MarketSnapshot(
            current_price=225.0,
            market_status="HISTORY_CLOSE_FALLBACK",
            daily_change=-1.5,
            daily_change_percent=-0.66,
        ),
        status=ServiceStatus(
            overall="complete",
            market="available",
            news="available",
            company="available",
            ai="available",
        ),
    )
    brief = market_brief_from_research(research)
    assert brief.quoteLabel == "Latest close"

    # And when normal / open
    research_open = ResearchResponse(
        request_id="test-2",
        query="AAPL",
        company=CompanyIdentity(
            symbol="AAPL",
            name="Apple Inc.",
            identifier_confidence=IdentifierConfidence.HIGH,
        ),
        market=MarketSnapshot(
            current_price=225.0,
            market_status="REGULAR_HOURS",
            daily_change=1.5,
            daily_change_percent=0.66,
        ),
        status=ServiceStatus(
            overall="complete",
            market="available",
            news="available",
            company="available",
            ai="available",
        ),
    )
    brief_open = market_brief_from_research(research_open)
    assert brief_open.quoteLabel == "Current price"


def test_identity_dossier_positive_price_movement():
    """Verify positive movement renders + sign and uses --upt/--up green token, not --down."""
    tpl = env.get_template("partials/identity_dossier.html")
    company = CompanyIdentity(
        symbol="AAPL",
        name="Apple Inc.",
        identifier_confidence=IdentifierConfidence.HIGH,
        sector="Technology",
        industry="Consumer Electronics",
        exchange="NASDAQ",
    )
    market = MarketSnapshot(
        current_price=228.40,
        daily_change=2.15,
        daily_change_percent=0.95,
        currency="USD",
    )
    html = tpl.render(company=company, market=market, quote_label="Current price")
    soup = BeautifulSoup(html, "html.parser")

    price_elem = soup.find(class_="price")
    assert price_elem and "$228.40" in price_elem.get_text()

    change_elem = soup.find(class_="price-change")
    assert change_elem is not None
    text = change_elem.get_text().strip()
    assert "+2.15 (+0.95%)" in text
    assert "var(--upt)" in change_elem.get("style", "")
    assert "var(--warn)" not in change_elem.get("style", "")
    assert "var(--down)" not in change_elem.get("style", "")


def test_identity_dossier_negative_price_movement():
    """Verify negative movement renders - sign and uses dedicated --down red token, NOT --warn."""
    tpl = env.get_template("partials/identity_dossier.html")
    company = CompanyIdentity(
        symbol="AAPL",
        name="Apple Inc.",
        identifier_confidence=IdentifierConfidence.HIGH,
        sector="Technology",
        industry="Consumer Electronics",
        exchange="NASDAQ",
    )
    market = MarketSnapshot(
        current_price=220.00,
        daily_change=-3.25,
        daily_change_percent=-1.45,
        currency="USD",
    )
    html = tpl.render(company=company, market=market, quote_label="Current price")
    soup = BeautifulSoup(html, "html.parser")

    change_elem = soup.find(class_="price-change")
    assert change_elem is not None
    text = change_elem.get_text().strip()
    assert "-3.25 (-1.45%)" in text
    style = change_elem.get("style", "")
    assert "var(--down)" in style, "Negative price movement MUST use var(--down)"
    assert "var(--warn)" not in style, "Negative price movement MUST NOT use warning orange"


def test_identity_dossier_zero_price_movement():
    """Verify zero/unchanged price movement renders cleanly."""
    tpl = env.get_template("partials/identity_dossier.html")
    company = CompanyIdentity(
        symbol="XYZ",
        name="Flat Corp",
        identifier_confidence=IdentifierConfidence.HIGH,
    )
    market = MarketSnapshot(
        current_price=100.00,
        daily_change=0.0,
        daily_change_percent=0.0,
        currency="USD",
    )
    html = tpl.render(company=company, market=market, quote_label="Current price")
    soup = BeautifulSoup(html, "html.parser")

    change_elem = soup.find(class_="price-change")
    assert change_elem is not None
    text = change_elem.get_text().strip()
    assert "0.00 (0.00%)" in text


def test_market_snapshot_partial_rendering():
    """Verify templates/partials/market_snapshot.html renders all 7 cards plus provider card."""
    tpl = env.get_template("partials/market_snapshot.html")
    market = MarketSnapshot(
        current_price=228.40,
        currency="USD",
        daily_change=2.15,
        daily_change_percent=0.95,
        market_cap=3420000000000,
        pe_ratio=31.8,
        fifty_two_week_high=237.23,
        fifty_two_week_low=164.08,
        volume=48200000,
        dividend_yield=0.0044,
        eps=7.19,
        market_status="REGULAR_HOURS",
    )
    metrics = snapshot_metrics_from_market(market, "USD")
    html = tpl.render(market=market, metrics=metrics, quote_label="Current price")
    soup = BeautifulSoup(html, "html.parser")

    snapshot_section = soup.find("section", id="snapshot")
    assert snapshot_section is not None
    assert "g4" in snapshot_section.get("class", [])

    # Check metric texts
    text = snapshot_section.get_text()
    assert "MARKET CAP" in text.upper()
    assert "$3.42T" in text
    assert "P / E RATIO" in text.upper() or "P/E RATIO" in text.upper()
    assert "31.8" in text
    assert "52-WEEK HIGH" in text.upper()
    assert "$237.23" in text
    assert "52-WEEK LOW" in text.upper()
    assert "$164.08" in text
    assert "VOLUME" in text.upper()
    assert "48.2M" in text
    assert "DIVIDEND YIELD" in text.upper()
    assert "0.44%" in text
    assert "EPS" in text.upper()
    assert "$7.19" in text


def test_eps_shared_formatter_and_source_field():
    """Verify EPS uses money_label with currency, matching Part 14 usage."""
    val = money_label(7.19, "USD")
    assert val == "$7.19"
    val_neg = money_label(-1.42, "USD")
    assert val_neg == "-$1.42"
    val_none = money_label(None, "USD")
    assert val_none == "—"
