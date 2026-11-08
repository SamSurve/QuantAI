"""Financial fundamentals presenter mapping reported financial health into view models.

Preserves exact units, currency codes, and null-safety (null is never converted to 0).
"""

from __future__ import annotations

from typing import Any

from api.research_schemas import FinancialHealth
from api.web.formatters import (
    compact_money_label,
    money_label,
    number_label,
    percent_label,
)


def format_financial_health(fh: FinancialHealth | None) -> dict[str, Any]:
    """Transform FinancialHealth contract into primary cards and expandable statement metrics."""
    if fh is None:
        return {
            "available": False,
            "primary": [],
            "statements": [],
            "fiscal_period_end": None,
            "currency": None,
        }

    currency = fh.currency if fh else None

    primary = [
        {
            "label": "EPS",
            "value": money_label(fh.eps, currency),
        },
        {
            "label": "Profit margin",
            "value": percent_label(
                fh.profit_margin * 100 if fh.profit_margin is not None else None,
                include_sign=False,
            ),
        },
        {
            "label": "Total cash",
            "value": compact_money_label(fh.total_cash, currency),
        },
        {
            "label": "Total debt",
            "value": compact_money_label(fh.total_debt, currency),
        },
        {
            "label": "Operating margin",
            "value": percent_label(
                fh.operating_margin * 100 if fh.operating_margin is not None else None,
                include_sign=False,
            ),
        },
    ]

    statements = [
        {
            "label": "Revenue",
            "value": compact_money_label(fh.revenue, currency),
        },
        {
            "label": "Net income",
            "value": compact_money_label(fh.net_income, currency),
        },
        {
            "label": "Free cash flow",
            "value": compact_money_label(fh.free_cash_flow, currency),
        },
        {
            "label": "Price-to-Sales",
            "value": number_label(fh.price_to_sales),
        },
        {
            "label": "ROE",
            "value": percent_label(
                fh.return_on_equity * 100 if fh.return_on_equity is not None else None,
                include_sign=False,
            ),
        },
        {
            "label": "ROA",
            "value": percent_label(
                fh.return_on_assets * 100 if fh.return_on_assets is not None else None,
                include_sign=False,
            ),
        },
    ]

    return {
        "available": True,
        "primary": primary,
        "statements": statements,
        "fiscal_period_end": fh.fiscal_period_end,
        "currency": currency,
    }
