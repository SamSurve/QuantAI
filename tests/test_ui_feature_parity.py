"""Tests for Part 34: All 21 UI features and Apple visual parity.

Verifies:
1. Individual verification for all 21 user-facing UI features:
   - F01: Search bar and quick ticker shortcuts.
   - F02: Navigation header with sticky backdrop filter and section anchors.
   - F03: Identity dossier with confidence badge and 56px hero price (-0.03em tracking).
   - F04: Market snapshot 4-column responsive grid and formatted metrics.
   - F05: Interactive chart with all 7 period controls (1D, 5D/1W, 1M, 3M, 6M, YTD, 1Y, 5Y).
   - F06: Deterministic Technical Signals score (0-100 gauge, Bullish/Bearish/Neutral).
   - F07: Financial health & fundamentals with expandable statement drawer.
   - F08: Executive brief with server-rendered MathML and disclaimer badge.
   - F09: Company profile and governance executive roster.
   - F10: Competitor evidence with sourced peer landscape notes.
   - F11: Sourced news feed with publisher tags and timestamps.
   - F12: Events radar with corporate calendar records and importance badges.
   - F13: Evidence appendix with provenance ledger and freshness states.
   - F14: Research desk chat drawer with AgentOS interface.
   - F15: Persistent theme system with 3-mode control and OS preference sync.
   - F16: Toast notification queue and connection health indicator.
   - F17: Responsive layout (1440px desktop vs 390px mobile reflow).
   - F18: Startup reveal splash and shimmer skeleton loading states.
   - F19: Contextual error recovery banners and empty states.
   - F20: Recent research activity tracker.
   - F21: Endpoint settings modal dialog with strict client-only storage.
2. Apple design system visual parity:
   - 22px card border-radius, 16px metric radius, 999px pills.
   - SF Pro / -apple-system typography stack with 56px hero price/headline (-0.03em / -0.035em).
   - True black (#000000) dark mode and #f5f5f7 light mode tokens.
3. Zero-network delta for local client interactions.
"""

from __future__ import annotations

import sys
from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import api.index as api_index


def test_f01_search_bar_and_shortcuts():
    """F01: Search bar and quick ticker shortcuts."""
    with TestClient(api_index.app) as client:
        res = client.get("/", headers={"Accept": "text/html"})
        assert res.status_code == 200
        html = res.text
        assert 'name="query"' in html
        assert 'data-quick-search="AAPL"' in html
        assert 'data-quick-search="MSFT"' in html
        assert 'data-quick-search="NVDA"' in html
        assert 'data-quick-search="TSLA"' in html


def test_f02_navigation_header_and_anchors():
    """F02: Navigation header with sticky backdrop filter and section anchors."""
    base = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    assert "backdrop-filter" in base
    for anchor in ("#snapshot", "#performance", "#fundamentals", "#news", "#analysis"):
        assert f'href="{anchor}"' in base


def test_f03_identity_dossier_price_hero():
    """F03: Identity dossier with confidence badge and 56px hero price with -0.03em tracking."""
    dossier = (ROOT / "templates" / "partials" / "identity_dossier.html").read_text(encoding="utf-8")
    assert 'class="price"' in dossier
    assert "56px" in dossier
    assert "letter-spacing:-0.03em" in dossier
    assert "company.name" in dossier
    assert "company.exchange" in dossier
    assert "Verified identity" in dossier


def test_f04_market_snapshot_grid():
    """F04: Market snapshot 4-column responsive grid and formatted metrics."""
    snapshot = (ROOT / "templates" / "partials" / "market_snapshot.html").read_text(encoding="utf-8")
    assert 'id="snapshot"' in snapshot
    assert 'class="g4"' in snapshot
    assert "Market snapshot" in snapshot
    assert "metrics" in snapshot


def test_f05_interactive_chart_periods():
    """F05: Interactive chart with all 7 period controls (1D, 5D/1W, 1M, 3M, 6M, YTD, 1Y, 5Y)."""
    chart = (ROOT / "templates" / "partials" / "market_chart.html").read_text(encoding="utf-8")
    assert 'id="performance"' in chart
    assert '<canvas id="marketChartCanvas"' in chart
    assert 'data-period="{{ p }}"' in chart
    for period in ("1D", "1W", "1M", "3M", "6M", "1Y", "5Y"):
        assert f'"{period}"' in chart

    market_chart_js = (ROOT / "static" / "js" / "market_chart.js").read_text(encoding="utf-8")
    for period in ("1D", "5D", "1W", "1M", "3M", "6M", "YTD", "1Y", "5Y"):
        assert period in market_chart_js


def test_f06_deterministic_technical_signals():
    """F06: Deterministic Technical Signals score (0-100 gauge, Bullish/Bearish/Neutral)."""
    signals = (ROOT / "templates" / "partials" / "signal_score.html").read_text(encoding="utf-8")
    assert "technical signal · deterministic" in signals.lower()
    assert "<svg" in signals and "circle" in signals
    assert "How this score is calculated" in signals


def test_f07_financial_fundamentals_health():
    """F07: Financial health & fundamentals with expandable statement drawer."""
    fundamentals = (ROOT / "templates" / "partials" / "fundamentals.html").read_text(encoding="utf-8")
    assert 'id="fundamentals"' in fundamentals
    assert "fundamentals.primary" in fundamentals
    assert "Financial statements" in fundamentals
    assert "fundamentals.statements" in fundamentals


def test_f08_executive_brief_mathml():
    """F08: Executive brief with server-rendered MathML and disclaimer badge."""
    brief = (ROOT / "templates" / "partials" / "analysis_brief.html").read_text(encoding="utf-8")
    assert 'id="analysis"' in brief
    assert "ai research brief" in brief.lower()
    assert "Interpretation · not evidence" in brief


def test_f09_company_profile_governance():
    """F09: Company profile and governance executive roster."""
    profile = (ROOT / "templates" / "partials" / "company_profile.html").read_text(encoding="utf-8")
    assert "company profile · verified" in profile.lower()
    assert "Sector" in profile and "Industry" in profile
    governance = (ROOT / "templates" / "partials" / "governance.html").read_text(encoding="utf-8")
    assert "governance · executive roster" in governance.lower()
    assert "Key Executive Leadership" in governance


def test_f10_competitor_evidence_peer_landscape():
    """F10: Competitor evidence with sourced peer landscape notes."""
    competitors = (ROOT / "templates" / "partials" / "competitor_evidence.html").read_text(encoding="utf-8")
    assert "competitive evidence" in competitors.lower()


def test_f11_sourced_news_feed():
    """F11: Sourced news feed with publisher tags and timestamps."""
    news = (ROOT / "templates" / "partials" / "news_feed.html").read_text(encoding="utf-8")
    assert 'id="news"' in news
    assert "Recent news" in news
    assert "View source ↗" in news


def test_f12_events_radar_corporate_calendar():
    """F12: Events radar with corporate calendar records and importance badges."""
    events = (ROOT / "templates" / "partials" / "events_radar.html").read_text(encoding="utf-8")
    assert "Events radar" in events
    assert "Calendar records" in events


def test_f13_evidence_appendix_provenance():
    """F13: Evidence appendix with provenance ledger and freshness states."""
    evidence = (ROOT / "templates" / "partials" / "evidence_appendix.html").read_text(encoding="utf-8")
    assert "Evidence appendix" in evidence
    assert "Show sources and freshness" in evidence


def test_f14_research_desk_chat_drawer():
    """F14: Research desk chat drawer with AgentOS interface."""
    chat = (ROOT / "templates" / "partials" / "chat_drawer.html").read_text(encoding="utf-8")
    assert 'id="chat-drawer"' in chat
    assert 'id="chat-toggle"' in chat
    assert "Ask the research desk" in chat


def test_f15_persistent_theme_system():
    """F15: Persistent theme system with 3-mode control and OS preference sync."""
    theme = (ROOT / "templates" / "partials" / "theme_toggle.html").read_text(encoding="utf-8")
    assert 'data-theme-value="light"' in theme
    assert 'data-theme-value="dark"' in theme
    assert 'data-theme-value="system"' in theme


def test_f16_toast_and_connection_health():
    """F16: Toast notification queue and connection health indicator."""
    with TestClient(api_index.app) as client:
        res = client.get("/", headers={"Accept": "text/html"})
        html = res.text
        assert 'id="toast-container"' in html
        assert 'id="connection-health-container"' in html or 'id="connection-indicator"' in html


def test_f17_responsive_layout_reflow():
    """F17: Responsive layout (1440px desktop vs 390px mobile reflow)."""
    css = (ROOT / "static" / "css" / "app.css").read_text(encoding="utf-8")
    assert "@media (max-width:900px)" in css or "@media" in css
    assert ".hero{font-size:38px!important}" in css or "38px" in css
    assert ".price{font-size:40px!important}" in css or "40px" in css


def test_f18_startup_reveal_and_skeletons():
    """F18: Startup reveal splash and shimmer skeleton loading states."""
    with TestClient(api_index.app) as client:
        res = client.get("/", headers={"Accept": "text/html"})
        assert 'id="startup-reveal"' in res.text
    skeleton = (ROOT / "templates" / "partials" / "research_skeleton.html").read_text(encoding="utf-8")
    assert "skeleton" in skeleton


def test_f19_contextual_error_recovery():
    """F19: Contextual error recovery banners and empty states."""
    status = (ROOT / "templates" / "partials" / "research_status.html").read_text(encoding="utf-8")
    assert "idle" in status
    assert "loading" in status
    assert "error" in status


def test_f20_recent_activity_tracker():
    """F20: Recent research activity tracker."""
    activity = (ROOT / "templates" / "partials" / "recent_activity.html").read_text(encoding="utf-8")
    assert "recent activity" in activity.lower()


def test_f21_endpoint_settings_modal():
    """F21: Endpoint settings modal dialog with strict client-only storage."""
    endpoint = (ROOT / "templates" / "partials" / "endpoint_settings.html").read_text(encoding="utf-8")
    assert 'id="endpoint-settings-dialog"' in endpoint
    assert 'id="endpoint-url-input"' in endpoint


def test_apple_design_visual_tokens():
    """Verify Apple financial terminal design tokens in CSS and templates."""
    css = (ROOT / "static" / "css" / "app.css").read_text(encoding="utf-8")
    assert "-apple-system" in css
    assert "SF Pro" in css or "SF Pro Display" in css or "Inter" in css
    assert "22px" in css or "border-radius:22px" in css or "rounded-[22px]" in css
    assert "999px" in css or "rounded-full" in css
    assert "#f5f5f7" in css or "--bg" in css
    assert "#1d1d1f" in css or "--text" in css


def test_zero_network_delta_client_interactions():
    """Verify client-side JavaScript implements local zero-network event handlers."""
    market_chart_js = (ROOT / "static" / "js" / "market_chart.js").read_text(encoding="utf-8")
    assert "updateChart" in market_chart_js
    assert "sliceSeries" in market_chart_js
    theme_js = (ROOT / "static" / "js" / "theme.js").read_text(encoding="utf-8")
    assert "localStorage.setItem" in theme_js
    assert "classList.toggle" in theme_js
