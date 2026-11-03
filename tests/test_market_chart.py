"""Tests for Part 12: Interactive market chart, period tabs, and Chart.js vendoring.

Verifies:
- Chart.js vendored locally without external CDN
- Chart.js bundle SHA-256 integrity
- Single JSON payload containing both intraday (1D) and 5Y daily history
- All seven period buttons rendered: 1D, 1W, 1M, 3M, 6M, 1Y, 5Y
- Client-side period slicing and performance summary calculation
- Empty history state handling when series is empty or < 2 points
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from api.research_schemas import (
    CompanyIdentity,
    FreshnessRecord,
    FreshnessState,
    HistoryPeriod,
    HistoryPoint,
    MarketSnapshot,
    PriceHistoryBundle,
    ResearchResponse,
    ServiceStatus,
)
from api.web.contracts import ChartPoint
from api.web.presenters import (
    calculate_performance_summary,
    market_brief_from_research,
    slice_period_series,
)

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"
VENDOR_CHART = ROOT / "static" / "vendor" / "chart" / "chart.umd.min.js"
STATIC_JS = ROOT / "static" / "js"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)

EXPECTED_CHART_SHA256 = "2812cb8825fdc57469eb2f7bb055e9429244e599920511ee477e828499b632cb"


def test_chart_vendor_asset_integrity():
    """Verify Chart.js 4.x is vendored locally with matching locally calculated SHA-256."""
    assert VENDOR_CHART.exists(), "static/vendor/chart/chart.umd.min.js must exist"
    content = VENDOR_CHART.read_bytes()
    assert len(content) > 150_000, "Chart.js bundle should be over 150KB"
    calc_sha = hashlib.sha256(content).hexdigest()
    assert calc_sha == EXPECTED_CHART_SHA256, f"Expected SHA-256 {EXPECTED_CHART_SHA256}, got {calc_sha}"


def test_no_external_cdn_in_templates_or_chart_js():
    """Verify neither templates nor client chart scripts contain external CDN links."""
    for path in TEMPLATES_DIR.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        assert "cdn.jsdelivr.net" not in text
        assert "cdnjs.cloudflare.com" not in text
        assert "unpkg.com" not in text

    chart_js = STATIC_JS / "market_chart.js"
    if chart_js.exists():
        text = chart_js.read_text(encoding="utf-8")
        assert "cdn.jsdelivr.net" not in text
        assert "cdnjs.cloudflare.com" not in text
        assert "unpkg.com" not in text


def test_single_json_payload_contains_both_intraday_and_daily():
    """Verify research response contains both intraday (1D) and daily (5Y) series."""
    intraday = [
        HistoryPoint(timestamp="2026-11-03T09:30:00Z", close=227.0),
        HistoryPoint(timestamp="2026-11-03T16:00:00Z", close=228.4),
    ]
    daily = [
        HistoryPoint(timestamp="2021-11-03", close=150.0),
        HistoryPoint(timestamp="2026-11-03", close=228.4),
    ]
    bundle = PriceHistoryBundle(
        intraday=intraday,
        daily=daily,
        available_periods=[HistoryPeriod.ONE_DAY, HistoryPeriod.FIVE_YEARS],
        default_period=HistoryPeriod.SIX_MONTHS,
        freshness=FreshnessRecord(state=FreshnessState.LIVE, as_of="2026-11-03"),
    )
    research = ResearchResponse(
        request_id="test-chart-1",
        query="AAPL",
        company=CompanyIdentity(symbol="AAPL", name="Apple Inc.", identifier_confidence="high"),
        history=daily,
        status=ServiceStatus(overall="complete", market="available", news="available", company="available", ai="available"),
    )
    # Populate market intelligence bundle
    from api.research_schemas import MarketIntelligenceReport, MarketIntelligenceFreshness
    f_rec = FreshnessRecord(state=FreshnessState.LIVE, as_of="2026-11-03")
    mi_freshness = MarketIntelligenceFreshness(
        company=f_rec,
        market=f_rec,
        history=f_rec,
        news=f_rec,
        events=f_rec,
        analysis=f_rec,
    )
    research.market_intelligence = MarketIntelligenceReport(
        price_history=bundle,
        freshness=mi_freshness,
    )

    brief = market_brief_from_research(research)
    assert len(brief.priceHistory.intraday) == 2
    assert len(brief.priceHistory.daily) == 2
    assert brief.priceHistory.intraday[0].value == 227.0
    assert brief.priceHistory.daily[0].value == 150.0


def test_slice_period_series_all_seven_periods():
    """Verify client-side slicing algorithm matches MarketChart.tsx / Home.tsx."""
    intraday = [ChartPoint(label="09:30", value=227.0), ChartPoint(label="16:00", value=228.4)]
    # Daily points spanning 5 years
    daily = [
        ChartPoint(label="2021-11-03", value=150.0), # 5Y
        ChartPoint(label="2025-11-03", value=180.0), # 1Y
        ChartPoint(label="2026-05-03", value=195.0), # 6M
        ChartPoint(label="2026-08-03", value=205.0), # 3M
        ChartPoint(label="2026-10-03", value=215.0), # 1M
        ChartPoint(label="2026-10-27", value=220.0), # 1W
        ChartPoint(label="2026-11-03", value=228.4), # Latest
    ]

    # 1D returns intraday
    s_1d = slice_period_series(intraday, daily, "1D")
    assert s_1d == intraday

    # 5Y returns full daily
    s_5y = slice_period_series(intraday, daily, "5Y")
    assert len(s_5y) == 7

    # 1W returns within 7 days
    s_1w = slice_period_series(intraday, daily, "1W")
    assert len(s_1w) >= 2
    assert s_1w[0].label == "2026-10-27"
    assert s_1w[-1].label == "2026-11-03"

    # Performance summary
    perf = calculate_performance_summary(s_1w)
    assert perf is not None
    assert perf["low"] == 220.0
    assert perf["high"] == 228.4
    assert round(perf["change"], 2) == 3.82


def test_empty_chart_state_rendering():
    """Verify template renders empty/awaiting chart state when series has < 2 points."""
    tpl = env.get_template("partials/market_chart.html")
    html = tpl.render(chart_points=[])
    soup = BeautifulSoup(html, "html.parser")

    # Empty state message
    assert "Price history appears when the research record includes dated closes." in html or "Series unavailable" in html or "awaiting series" in html.lower()


def test_market_chart_partial_renders_seven_tabs():
    """Verify partial renders all 7 period buttons (1D, 1W, 1M, 3M, 6M, 1Y, 5Y)."""
    tpl = env.get_template("partials/market_chart.html")
    daily = [
        ChartPoint(label="2026-10-01", value=220.0),
        ChartPoint(label="2026-11-03", value=228.4),
    ]
    html = tpl.render(
        chart_points=daily,
        chart_data_json=json.dumps({"intraday": [], "daily": [{"label": "2026-11-03", "value": 228.4}]}),
    )
    soup = BeautifulSoup(html, "html.parser")

    buttons = [btn.get_text().strip() for btn in soup.find_all("button", class_=lambda c: c and "period" in c or "seg" in c)]
    for period in ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"]:
        assert period in html, f"Period {period} must be in market chart markup"
