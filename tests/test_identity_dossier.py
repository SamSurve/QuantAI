"""Tests for company identity dossier and price/change display.

Verifies verified vs pending badges, company metadata line, price formatting,
positive/negative styling, and graceful missing field fallbacks.
"""

from __future__ import annotations

from pathlib import Path
import pytest
from jinja2 import Environment, FileSystemLoader

from api.research_schemas import CompanyIdentity, IdentifierConfidence, MarketSnapshot

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def _sample_company(
    symbol="MSFT",
    name="Microsoft Corporation",
    exchange="NASDAQ",
    sector="Technology",
    industry="Software—Infrastructure",
    confidence: IdentifierConfidence = IdentifierConfidence.HIGH,
) -> CompanyIdentity:
    return CompanyIdentity(
        symbol=symbol,
        name=name,
        exchange=exchange,
        sector=sector,
        industry=industry,
        identifier_confidence=confidence,
    )


def _sample_market(price=420.50, change=3.50, change_pct=0.84) -> MarketSnapshot:
    return MarketSnapshot(
        current_price=price,
        daily_change=change,
        daily_change_percent=change_pct,
    )


def test_verified_identity_rendering():
    """Verify verified company renders ticker badge, title, metadata line, and verified badge."""
    template = env.get_template("partials/identity_dossier.html")
    company = _sample_company(confidence=IdentifierConfidence.HIGH)
    market = _sample_market(price=420.50, change=3.50, change_pct=0.84)

    rendered = template.render(company=company, market=market)

    assert "MSFT" in rendered
    assert "Microsoft Corporation" in rendered
    assert "Technology · Software—Infrastructure · NASDAQ" in rendered
    assert "Verified identity" in rendered
    assert "$420.50" in rendered
    assert "+3.50 (+0.84%)" in rendered
    assert "var(--upt)" in rendered or "positive" in rendered


def test_pending_identity_rendering():
    """Verify pending company renders pending badge without claiming verified status."""
    template = env.get_template("partials/identity_dossier.html")
    company = _sample_company(confidence=IdentifierConfidence.LOW)
    market = _sample_market()

    rendered = template.render(company=company, market=market)

    assert "MSFT" in rendered
    assert "Pending verification" in rendered
    assert "Verified identity" not in rendered


def test_negative_price_change_display():
    """Verify negative price change renders in red/negative styling."""
    template = env.get_template("partials/identity_dossier.html")
    company = _sample_company()
    market = _sample_market(price=150.00, change=-2.50, change_pct=-1.64)

    rendered = template.render(company=company, market=market)

    assert "$150.00" in rendered
    assert "-2.50 (-1.64%)" in rendered
    assert "negative" in rendered or "var(--warn)" in rendered or "#d32f2f" in rendered or "red" in rendered or "var(--destructive)" in rendered or "var(--down)" in rendered


def test_missing_fields_fallbacks():
    """Verify missing sector, industry, or price renders gracefully without crashing."""
    template = env.get_template("partials/identity_dossier.html")
    company = CompanyIdentity(symbol="TEST", name=None, exchange=None, sector=None, industry=None, identifier_confidence=IdentifierConfidence.AMBIGUOUS)

    rendered = template.render(company=company, market=None)

    assert "TEST" in rendered
    assert "Ambiguous identity" in rendered
    assert "—" in rendered or "Quote unavailable" in rendered
