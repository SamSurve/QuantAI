"""Tests for Part 14: Financial Fundamentals presentation and null preservation.

Verifies:
- Primary metrics: EPS, Profit Margin, Total Cash, Total Debt, Operating Margin
- Fiscal period end date
- Expandable financial statements section: Revenue, Net Income, Free Cash Flow, Price-to-Sales, ROE, ROA
- Units and currency preservation (USD, EUR, etc.)
- Null preservation: null is NEVER shown as 0 or $0, but as "—"
- Legitimate 0 values (e.g. 0.0 debt) shown as 0
- Template rendering in templates/partials/fundamentals.html
- Clean unavailable state when financial data is missing
"""

from __future__ import annotations

from pathlib import Path
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from api.research_schemas import FinancialHealth
from api.web.fundamentals import format_financial_health

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def test_format_financial_health_all_fields_present():
    """Verify all required primary and statement fields are formatted with correct units."""
    fh = FinancialHealth(
        revenue=383_285_000_000,
        net_income=96_995_000_000,
        eps=7.19,
        profit_margin=0.253,
        operating_margin=0.301,
        free_cash_flow=99_600_000_000,
        total_cash=65_200_000_000,
        total_debt=101_000_000_000,
        price_to_sales=7.85,
        return_on_equity=1.512,
        return_on_assets=0.284,
        currency="USD",
        fiscal_period_end="2026-09-30",
    )

    data = format_financial_health(fh)
    primary = {m["label"]: m["value"] for m in data["primary"]}
    statements = {m["label"]: m["value"] for m in data["statements"]}

    # Primary metrics
    assert primary["EPS"] == "$7.19"
    assert primary["Profit margin"] == "25.30%"
    assert primary["Total cash"] == "$65.2B"
    assert primary["Total debt"] == "$101B"
    assert primary["Operating margin"] == "30.10%"
    assert data["fiscal_period_end"] == "2026-09-30"

    # Expandable statements
    assert statements["Revenue"] == "$383.29B" or statements["Revenue"] == "$383.28B"
    assert statements["Net income"] == "$97B" or statements["Net income"] == "$96.99B" or statements["Net income"] == "$97B"
    assert statements["Free cash flow"] == "$99.6B"
    assert statements["Price-to-Sales"] == "7.85"
    assert statements["ROE"] == "151.20%"
    assert statements["ROA"] == "28.40%"


def test_null_handling_never_shown_as_zero():
    """Verify null values produce '—' and are never coerced to 0, $0, or 0.0%."""
    fh = FinancialHealth(
        revenue=None,
        net_income=None,
        eps=None,
        profit_margin=None,
        operating_margin=None,
        free_cash_flow=None,
        total_cash=None,
        total_debt=None,
        price_to_sales=None,
        return_on_equity=None,
        return_on_assets=None,
        currency="USD",
        fiscal_period_end=None,
    )

    data = format_financial_health(fh)
    for m in data["primary"]:
        assert m["value"] == "—", f"{m['label']} must be '—', got {m['value']}"
        assert m["value"] != "0" and m["value"] != "$0"

    for m in data["statements"]:
        assert m["value"] == "—", f"{m['label']} must be '—', got {m['value']}"
        assert m["value"] != "0" and m["value"] != "$0"


def test_legitimate_zero_distinguished_from_null():
    """Verify explicit 0 is rendered as 0, not confused with null."""
    fh = FinancialHealth(
        total_debt=0,
        profit_margin=0.0,
        currency="USD",
    )
    data = format_financial_health(fh)
    primary = {m["label"]: m["value"] for m in data["primary"]}

    assert primary["Total debt"] == "$0"
    assert primary["Profit margin"] == "0.00%"


def test_currency_preservation_eur():
    """Verify non-USD currency codes are preserved in money formatting."""
    fh = FinancialHealth(
        eps=4.50,
        total_cash=10_000_000_000,
        currency="EUR",
    )
    data = format_financial_health(fh)
    primary = {m["label"]: m["value"] for m in data["primary"]}

    assert "€" in primary["EPS"] or "EUR" in primary["EPS"]
    assert "€" in primary["Total cash"] or "EUR" in primary["Total cash"]


def test_fundamentals_partial_rendering():
    """Verify templates/partials/fundamentals.html renders primary grid and expandable details."""
    tpl = env.get_template("partials/fundamentals.html")
    fh = FinancialHealth(
        revenue=383_000_000_000,
        net_income=96_000_000_000,
        eps=7.19,
        profit_margin=0.243,
        operating_margin=0.301,
        free_cash_flow=99_600_000_000,
        total_cash=65_200_000_000,
        total_debt=101_000_000_000,
        price_to_sales=7.8,
        return_on_equity=1.51,
        return_on_assets=0.28,
        currency="USD",
        fiscal_period_end="Sep 2026",
    )
    data = format_financial_health(fh)
    html = tpl.render(fundamentals=data)
    soup = BeautifulSoup(html, "html.parser")

    # Check primary labels
    for lbl in ["EPS", "Profit margin", "Total cash", "Total debt", "Operating margin"]:
        assert lbl in html

    # Check expandable details
    details = soup.find("details")
    assert details is not None
    summary = details.find("summary")
    assert summary is not None
    assert "Sep 2026" in summary.get_text()

    # Check statement metrics inside details
    for stmt_lbl in ["Revenue", "Net income", "Free cash flow", "Price-to-Sales", "ROE", "ROA"]:
        assert stmt_lbl in html


def test_fundamentals_partial_unavailable_state():
    """Verify templates/partials/fundamentals.html renders unavailable notice when data is None."""
    tpl = env.get_template("partials/fundamentals.html")
    html = tpl.render(fundamentals=None)
    assert "unavailable" in html.lower()
