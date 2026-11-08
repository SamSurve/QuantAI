"""Tests for backend currency resolution and propagation across services."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, patch

from api.company_analysis_services import (
    CompanyProfileResult,
    FinancialHealthResult,
    market_snapshot_from_profile,
)
from api.market_intelligence_services import MarketPulseResult, MarketPulseService
from api.research_schemas import (
    CompanyIdentity,
    CompanyOverview,
    FinancialHealth,
    HistoryPoint,
    IdentifierConfidence,
    MarketSnapshot,
    ResearchResponse,
    ServiceState,
    ServiceStatus,
    SourceRecord,
)
from api.research_services import (
    MarketDataResult,
    MarketDataService,
    resolve_source_currency,
)
from api.web.research import merge_research_records


def test_resolve_source_currency_nse_listing():
    """NSE listing ending in .NS resolves to INR when source confirms INR or by exchange qualification."""
    # Source info confirms INR
    assert resolve_source_currency("RELIANCE.NS", "NSI", info={"currency": "INR"}) == "INR"
    # Source financialCurrency confirms INR
    assert resolve_source_currency("TCS.NS", "NSI", info={"financialCurrency": "INR"}) == "INR"
    # Suffix and exchange fallback
    assert resolve_source_currency("INFY.NS", "NSI", info={}) == "INR"
    assert resolve_source_currency("TATAMOTORS.NS", "NSE") == "INR"


def test_resolve_source_currency_bse_listing():
    """BSE listing ending in .BO resolves to INR when source confirms INR or by exchange qualification."""
    assert resolve_source_currency("500325.BO", "BSE", info={"currency": "INR"}) == "INR"
    assert resolve_source_currency("RELIANCE.BO", "BSE", info={}) == "INR"
    assert resolve_source_currency("TCS.BO", "BSE") == "INR"


def test_resolve_source_currency_us_listing():
    """US listed stocks retain USD."""
    assert resolve_source_currency("AAPL", "NASDAQ", info={"currency": "USD"}) == "USD"
    assert resolve_source_currency("MSFT", "NMS", info={}) == "USD"
    assert resolve_source_currency("JPM", "NYQ", info={"currency": "USD"}) == "USD"


def test_resolve_source_currency_gbp_listing():
    """UK listed stocks use GBP."""
    assert resolve_source_currency("SHEL.L", "LSE", info={"currency": "GBP"}) == "GBP"
    assert resolve_source_currency("AZN.L", "LSE", info={}) == "GBP"


def test_resolve_source_currency_eur_listing():
    """European listed stocks use EUR."""
    assert resolve_source_currency("SAP.DE", "FRA", info={"currency": "EUR"}) == "EUR"
    assert resolve_source_currency("MC.PA", "EPA", info={}) == "EUR"


def test_resolve_source_currency_missing_metadata_fallback():
    """When currency metadata and exchange are unavailable, safe fallback is None (never invent USD)."""
    assert resolve_source_currency("UNKNOWN", exchange=None, info=None) is None
    assert resolve_source_currency("TEST", exchange="", info={}) is None


def test_resolve_source_currency_preserves_explicit_source_currency():
    """Authoritative source info currency takes precedence over exchange assumptions."""
    assert resolve_source_currency("DUAL", "NASDAQ", info={"currency": "CAD"}) == "CAD"
    assert resolve_source_currency("GLOBAL", "LSE", info={"currency": "USD"}) == "USD"


@pytest.mark.asyncio
async def test_market_data_service_currency_propagation():
    """MarketDataService sets currency on both CompanyIdentity and MarketSnapshot without mutating numbers."""
    entity = CompanyIdentity(
        symbol="RELIANCE.NS",
        name="Reliance Industries Limited",
        exchange="NSI",
        identifier_confidence=IdentifierConfidence.HIGH,
    )
    service = MarketDataService()

    fake_info = {
        "longName": "Reliance Industries Limited",
        "exchange": "NSI",
        "currency": "INR",
        "currentPrice": 2845.50,
        "marketCap": 19000000000000,
        "fiftyTwoWeekHigh": 3000.0,
        "fiftyTwoWeekLow": 2200.0,
    }
    fake_history = [
        HistoryPoint(timestamp="2026-11-07T00:00:00Z", close=2820.0),
        HistoryPoint(timestamp="2026-11-08T00:00:00Z", close=2845.50),
    ]

    with patch.object(service, "_get_info", AsyncMock(return_value=fake_info)), \
         patch.object(service, "_get_history", AsyncMock(return_value=fake_history)):
        result = await service.fetch(entity)

    assert result.company.currency == "INR"
    assert result.market is not None
    assert result.market.currency == "INR"
    assert result.market.current_price == 2845.50
    assert result.market.daily_change == pytest.approx(25.50, rel=1e-3)


@pytest.mark.asyncio
async def test_market_pulse_service_currency_propagation():
    """MarketPulseService propagates currency to pulse company and market pulse."""
    entity = CompanyIdentity(
        symbol="TCS.NS",
        name="Tata Consultancy Services",
        exchange="NSI",
        identifier_confidence=IdentifierConfidence.HIGH,
    )
    service = MarketPulseService()

    fake_info = {
        "longName": "Tata Consultancy Services Limited",
        "exchange": "NSI",
        "currency": "INR",
        "currentPrice": 3950.0,
        "regularMarketPrice": 3950.0,
        "marketCap": 14000000000000,
    }

    with patch.object(service, "_info", AsyncMock(return_value=fake_info)):
        result, _ = await service.fetch(entity)

    assert result.company.currency == "INR"
    assert result.market is not None
    assert result.market.currency == "INR"
    assert result.market.current_price == 3950.0


def test_market_snapshot_from_profile_currency():
    """market_snapshot_from_profile resolves source currency from profile info dictionary."""
    info = {
        "symbol": "RELIANCE.NS",
        "exchange": "NSI",
        "currency": "INR",
        "regularMarketPrice": 2845.50,
        "marketCap": 19000000000000,
    }
    snapshot = market_snapshot_from_profile(info, currency="INR", as_of="2026-11-08T00:00:00Z")
    assert snapshot is not None
    assert snapshot.currency == "INR"
    assert snapshot.current_price == 2845.50


def test_merge_research_records_currency_propagation():
    """merge_research_records ensures market snapshot inherits company currency if snapshot currency was missing."""
    company = CompanyIdentity(
        symbol="RELIANCE.NS",
        name="Reliance Industries Limited",
        currency="INR",
        identifier_confidence=IdentifierConfidence.HIGH,
    )
    market_snap_without_currency = MarketSnapshot(
        current_price=2845.50,
        currency=None,
    )
    status = ServiceStatus(
        overall="complete",
        company=ServiceState.AVAILABLE,
        market=ServiceState.AVAILABLE,
        news=ServiceState.AVAILABLE,
        ai=ServiceState.AVAILABLE,
    )
    market_resp = ResearchResponse(
        request_id="req-1",
        query="RELIANCE.NS",
        company=company,
        market=market_snap_without_currency,
        status=status,
    )
    deep_resp = ResearchResponse(
        request_id="req-1",
        query="RELIANCE.NS",
        company=company,
        status=status,
    )

    merged = merge_research_records(market_resp, deep_resp)
    assert merged.market is not None
    assert merged.market.currency == "INR"
