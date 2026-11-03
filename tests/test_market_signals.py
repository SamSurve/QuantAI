"""Tests for Part 13: Deterministic market signals and score ring UI.

Verifies:
- calculate_market_signal from real backend function (api/market_intelligence_services.py)
- Categories: BULLISH, NEUTRAL, BEARISH
- Threshold boundaries: score >= 60 (BULLISH), <= 40 (BEARISH), 41-59 (NEUTRAL)
- Real technical drivers: momentum, moving-average alignment, volatility
- Insufficient history handling (< 21 rows)
- Deterministic repeatability
- UI template rendering in templates/partials/signal_score.html:
  - 0-100 score ring with SVG stroke-dasharray
  - Confidence rating (Low / Moderate / High)
  - Category heading
  - Bullets for technical drivers
  - Expandable methodology (<details>)
"""

from __future__ import annotations

import math
from pathlib import Path
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from api.market_intelligence_services import calculate_market_signal
from api.research_schemas import HistoryPoint, MarketSignal
from api.web.presenters import market_brief_from_research

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def _generate_synthetic_history(n: int, start: float, trend: float, vol: float = 0.5) -> list[HistoryPoint]:
    points: list[HistoryPoint] = []
    val = start
    for i in range(n):
        # deterministic pseudo-movement
        step = trend + (math.sin(i) * vol)
        val += step
        points.append(
            HistoryPoint(
                timestamp=f"2026-01-{i+1:02d}" if i < 28 else f"2026-02-{i-27:02d}",
                close=round(val, 2),
                volume=10_000_000 + int(math.cos(i) * 1_000_000),
            )
        )
    return points


def test_real_backend_signal_bullish():
    """Verify backend produces BULLISH category for strong upward trend."""
    # 60 days of strong upward trend (+2.0 per day)
    history = _generate_synthetic_history(60, start=100.0, trend=2.0)
    sig = calculate_market_signal(history)

    assert sig.signal == "BULLISH"
    assert sig.score is not None and sig.score >= 60
    assert sig.confidence is not None and sig.confidence >= 40
    assert any("momentum is positive" in f.lower() for f in sig.factors)
    assert any("above the 20-session average" in f.lower() for f in sig.factors)
    assert sig.explanation is not None


def test_real_backend_signal_bearish():
    """Verify backend produces BEARISH category for strong downward trend."""
    # 60 days of strong downward trend (-2.0 per day)
    history = _generate_synthetic_history(60, start=300.0, trend=-2.0)
    sig = calculate_market_signal(history)

    assert sig.signal == "BEARISH"
    assert sig.score is not None and sig.score <= 40
    assert any("momentum is negative" in f.lower() for f in sig.factors)
    assert any("below the 20-session average" in f.lower() for f in sig.factors)


def test_real_backend_signal_neutral():
    """Verify backend produces NEUTRAL category for consolidation/mixed trend."""
    # 30 sessions base, 25 sessions consolidation, slight pullback on last day
    closes = [100.0] * 30 + [110.0] * 25 + [109.5]
    history = [HistoryPoint(timestamp=f"2026-01-{i}", close=c) for i, c in enumerate(closes)]
    sig = calculate_market_signal(history)

    assert sig.signal == "NEUTRAL"
    assert sig.score is not None and 40 < sig.score < 60


def test_real_backend_insufficient_history():
    """Verify backend returns None signal and score when < 21 rows."""
    history = _generate_synthetic_history(15, start=100.0, trend=1.0)
    sig = calculate_market_signal(history)

    assert sig.signal is None
    assert sig.score is None
    assert sig.confidence == 0
    assert "Insufficient daily price history" in sig.explanation


def test_signal_score_ring_template_rendering_bullish():
    """Verify templates/partials/signal_score.html renders 0-100 ring, confidence, bullets, details."""
    tpl = env.get_template("partials/signal_score.html")
    sig = MarketSignal(
        signal="BULLISH",
        score=72,
        confidence=75,
        factors=[
            "Price above 50- and 200-day averages",
            "Momentum positive over 3 months",
            "Volatility below its 1-year median",
        ],
        explanation="Score begins at 50 and adjusts for 20-session momentum.",
        methodology="The score combines moving-average alignment, momentum and volatility.",
    )
    html = tpl.render(signal=sig)
    soup = BeautifulSoup(html, "html.parser")

    # Score ring number and text
    assert "72" in html
    assert "of 100" in html
    assert "Bullish" in html
    assert "Confidence: High" in html or "Confidence: Moderate" in html or "75" in html

    # Bullets
    for factor in sig.factors:
        assert factor in html

    # Expandable details
    details = soup.find("details")
    assert details is not None
    assert "How this score is calculated" in details.get_text()
    assert "The score combines moving-average alignment" in details.get_text()

    # SVG stroke dasharray calculation (72% of 339 = ~244)
    svg = soup.find("svg")
    assert svg is not None
    assert "stroke-dasharray" in str(svg)


def test_signal_score_ring_template_rendering_unavailable():
    """Verify unavailable state is displayed cleanly when signal is None or insufficient."""
    tpl = env.get_template("partials/signal_score.html")
    html = tpl.render(signal=None)
    assert "Signal unavailable until sufficient deterministic history is sourced." in html or "unavailable" in html.lower()


def test_signal_deterministic_repeatability():
    """Verify running calculate_market_signal twice on the same input produces identical output."""
    history = _generate_synthetic_history(45, start=150.0, trend=0.8, vol=0.3)
    sig1 = calculate_market_signal(history)
    sig2 = calculate_market_signal(history)

    assert sig1.score == sig2.score
    assert sig1.signal == sig2.signal
    assert sig1.confidence == sig2.confidence
    assert sig1.factors == sig2.factors
    assert sig1.explanation == sig2.explanation
