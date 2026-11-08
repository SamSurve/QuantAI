"""Integration and formatting tests for unified INR and international currency display."""

from __future__ import annotations

from pathlib import Path
import pytest
from jinja2 import Environment, FileSystemLoader

from api.comparison_services import comparison_metric
from api.research_schemas import (
    CompanyIdentity,
    CompanyOverview,
    ComparisonWinner,
    FinancialHealth,
    IdentifierConfidence,
    MarketSnapshot,
    ResearchResponse,
    ServiceState,
    ServiceStatus,
)
from api.web.contracts import ChartPoint, MarketBrief, MarketBriefPriceHistory, Metric
from api.web.formatters import (
    compact_money_label,
    format_indian_compact,
    format_indian_number,
    money_label,
    number_label,
    percent_label,
)
from api.web.fundamentals import format_financial_health
from api.web.presenters import market_brief_from_research, snapshot_metrics_from_market

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def test_inr_formatting_rules():
    """Verify Indian rupee rules: symbol ₹, en-IN grouping, and Cr compact notation."""
    # Stock price formatting
    assert money_label(2845.50, "INR") == "₹2,845.50"
    assert money_label(125000.00, "INR") == "₹1,25,000.00"
    assert money_label(10000000.00, "INR") == "₹1,00,00,000.00"

    # Compact notation
    assert compact_money_label(125_000_000, "INR") == "₹12.50 Cr"
    assert compact_money_label(17_916_992_946_176, "INR") == "₹17.92 Lakh Cr"
    assert compact_money_label(250_000, "INR") == "₹2.50 L"


def test_international_currencies_retained():
    """Verify US ($), UK (£), EUR (€), and JPY (¥) are properly formatted."""
    assert money_label(228.40, "USD") == "$228.40"
    assert compact_money_label(3_420_000_000_000, "USD") == "$3.42T"

    assert money_label(2550.00, "GBP") == "£2,550.00"
    assert compact_money_label(180_000_000_000, "GBP") == "£180B"

    assert money_label(175.25, "EUR") == "€175.25"
    assert compact_money_label(210_000_000_000, "EUR") == "€210B"

    assert money_label(15420, "JPY") == "¥15,420"


def test_missing_currency_safe_fallback():
    """Verify missing currency metadata outputs a clean safe numeric string without inventing USD."""
    assert money_label(2845.50, None) == "2,845.50"
    assert money_label(125.0, "") == "125.00"
    assert compact_money_label(50_000_000, None) == "50M"


def test_identity_dossier_renders_inr_for_nse_company():
    """Verify identity_dossier.html renders ₹ for Reliance NSE listing."""
    template = env.get_template("partials/identity_dossier.html")
    company = CompanyIdentity(
        symbol="RELIANCE.NS",
        name="Reliance Industries Limited",
        exchange="NSI",
        currency="INR",
        identifier_confidence=IdentifierConfidence.HIGH,
    )
    market = MarketSnapshot(
        current_price=2845.50,
        currency="INR",
        daily_change=25.50,
        daily_change_percent=0.90,
    )
    rendered = template.render(company=company, market=market)
    assert "₹2845.50" in rendered or "₹2,845.50" in rendered
    assert "$" not in rendered


def test_identity_dossier_renders_inr_for_bse_company():
    """Verify identity_dossier.html renders ₹ for BSE listing."""
    template = env.get_template("partials/identity_dossier.html")
    company = CompanyIdentity(
        symbol="500325.BO",
        name="Reliance Industries Limited",
        exchange="BSE",
        currency="INR",
        identifier_confidence=IdentifierConfidence.HIGH,
    )
    market = MarketSnapshot(
        current_price=2846.00,
        currency="INR",
        daily_change=26.00,
        daily_change_percent=0.92,
    )
    rendered = template.render(company=company, market=market)
    assert "₹2846.00" in rendered or "₹2,846.00" in rendered
    assert "$" not in rendered


def test_identity_dossier_renders_usd_for_us_company():
    """Verify identity_dossier.html renders $ for Apple."""
    template = env.get_template("partials/identity_dossier.html")
    company = CompanyIdentity(
        symbol="AAPL",
        name="Apple Inc.",
        exchange="NASDAQ",
        currency="USD",
        identifier_confidence=IdentifierConfidence.HIGH,
    )
    market = MarketSnapshot(
        current_price=228.40,
        currency="USD",
        daily_change=2.15,
        daily_change_percent=0.95,
    )
    rendered = template.render(company=company, market=market)
    assert "$228.40" in rendered
    assert "₹" not in rendered


def test_market_snapshot_metrics_currency_inr():
    """Verify 52-week high, low, EPS and Market Cap format with ₹ and INR units."""
    market = MarketSnapshot(
        current_price=2845.50,
        currency="INR",
        market_cap=19000000000000,
        fifty_two_week_high=3000.0,
        fifty_two_week_low=2200.0,
        eps=120.50,
        pe_ratio=23.6,
        volume=5000000,
        dividend_yield=0.004,
    )
    metrics = snapshot_metrics_from_market(market, currency="INR")
    metrics_by_label = {m.label: m.value for m in metrics}

    assert "₹19.00 Lakh Cr" in metrics_by_label["Market cap"] or "₹" in metrics_by_label["Market cap"]
    assert metrics_by_label["52-week high"] == "₹3,000.00"
    assert metrics_by_label["52-week low"] == "₹2,200.00"
    assert metrics_by_label["EPS"] == "₹120.50"
    # Ratios, percentages and volume remain separate from currency
    assert metrics_by_label["P / E ratio"] == "23.6"
    assert metrics_by_label["Volume"] == "5M"
    assert metrics_by_label["Dividend yield"] == "0.40%"


def test_fundamentals_currency_formatting_inr():
    """Verify fundamentals reporting displays INR for Indian financials."""
    fh = FinancialHealth(
        revenue=9000000000000.0,
        net_income=700000000000.0,
        eps=105.20,
        total_cash=2600000000000.0,
        total_debt=5020000000000.0,
        profit_margin=0.078,
        operating_margin=0.125,
        currency="INR",
    )
    data = format_financial_health(fh)
    assert data["available"] is True
    assert data["currency"] == "INR"

    primary_by_label = {item["label"]: item["value"] for item in data["primary"]}
    assert primary_by_label["EPS"] == "₹105.20"
    assert "₹" in primary_by_label["Total cash"]
    assert "₹" in primary_by_label["Total debt"]
    assert primary_by_label["Profit margin"] == "7.80%"


def test_company_comparison_cross_currency_integrity():
    """Verify company comparison tracks original currencies and flags unconverted monetary amounts."""
    metric = comparison_metric(
        "market_cap",
        19000000000000,
        3400000000000,
        unit="currency",
        currency_a="INR",
        currency_b="USD",
        higher_is_better=True,
    )
    assert metric.currency_a == "INR"
    assert metric.currency_b == "USD"
    # Cannot directly compare nominal monetary values across different currencies without verified FX
    assert metric.currency_comparable is False
    assert metric.winner == ComparisonWinner.INSUFFICIENT_DATA
    assert "CURRENCY_COMPARISON_UNAVAILABLE" in (metric.note or "")
