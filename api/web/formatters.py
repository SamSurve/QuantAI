"""Market and financial data formatters matching TypeScript Intl behavior."""

from __future__ import annotations

import math
import re
from typing import Literal

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "INR": "₹",
    "JPY": "¥",
    "CAD": "CA$",
    "AUD": "A$",
    "CHF": "CHF ",
    "CNY": "¥",
}


def number_label(
    value: float | int | None,
    max_fraction_digits: int = 2,
    notation: str | None = None,
) -> str:
    """Format numeric values with thousand separators or compact notation."""
    if value is None:
        return "—"
    try:
        val = float(value)
        if not math.isfinite(val):
            return "—"
    except (ValueError, TypeError):
        return "—"

    if notation == "compact":
        return _format_compact(val, max_fraction_digits)

    # Standard format with grouping
    if val.is_integer() and max_fraction_digits == 0:
        return f"{int(val):,}"

    formatted = f"{val:,.{max_fraction_digits}f}"
    # Strip unnecessary trailing zeroes if integer-like float
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted if formatted else "0"


def _format_compact(val: float, max_fraction_digits: int = 2) -> str:
    abs_val = abs(val)
    sign = "-" if val < 0 else ""

    if abs_val >= 1e12:
        unit = "T"
        scaled = abs_val / 1e12
    elif abs_val >= 1e9:
        unit = "B"
        scaled = abs_val / 1e9
    elif abs_val >= 1e6:
        unit = "M"
        scaled = abs_val / 1e6
    elif abs_val >= 1e3:
        unit = "K"
        scaled = abs_val / 1e3
    else:
        unit = ""
        scaled = abs_val

    formatted = f"{scaled:.{max_fraction_digits}f}".rstrip("0").rstrip(".")
    if not formatted:
        formatted = "0"
    return f"{sign}{formatted}{unit}"


def money_label(
    value: float | int | None,
    currency: str | None = None,
    max_fraction_digits: int = 2,
) -> str:
    """Format currency values with appropriate symbol and decimals."""
    if value is None:
        return "—"
    try:
        val = float(value)
        if not math.isfinite(val):
            return "—"
    except (ValueError, TypeError):
        return "—"

    curr_code = (currency or "USD").upper()
    symbol = CURRENCY_SYMBOLS.get(curr_code, f"{curr_code} ")

    if curr_code == "JPY":
        # JPY typically has no fractional decimals
        abs_int = abs(int(round(val)))
        sign = "-" if val < 0 else ""
        return f"{sign}{symbol}{abs_int:,}"

    sign = "-" if val < 0 else ""
    abs_val = abs(val)
    formatted_num = f"{abs_val:,.{max_fraction_digits}f}"
    return f"{sign}{symbol}{formatted_num}"


def compact_money_label(
    value: float | int | None,
    currency: str | None = None,
    max_fraction_digits: int = 2,
) -> str:
    """Format compact money strings like $3T or €500.5M."""
    if value is None:
        return "—"
    try:
        val = float(value)
        if not math.isfinite(val):
            return "—"
    except (ValueError, TypeError):
        return "—"

    curr_code = (currency or "USD").upper()
    symbol = CURRENCY_SYMBOLS.get(curr_code, f"{curr_code} ")

    compact_str = _format_compact(abs(val), max_fraction_digits)
    sign = "-" if val < 0 else ""
    return f"{sign}{symbol}{compact_str}"


def percent_label(
    value: float | int | None,
    max_fraction_digits: int = 2,
    include_sign: bool = True,
) -> str:
    """Format percentages with optional positive sign and decimal precision."""
    if value is None:
        return "—"
    try:
        val = float(value)
        if not math.isfinite(val):
            return "—"
    except (ValueError, TypeError):
        return "—"

    sign = ""
    if include_sign:
        sign = "+" if val > 0 else ("-" if val < 0 else "")
    formatted_num = f"{abs(val):.{max_fraction_digits}f}"
    return f"{sign}{formatted_num}%"


def tone_for(value: str) -> Literal["positive", "negative", "neutral"]:
    """Determine visual metric tone based on value sign/sentiment."""
    val = value.strip().lower()
    if val.startswith("+") or any(word in val for word in ("up", "gain", "positive")):
        return "positive"
    if val.startswith("-") or any(word in val for word in ("down", "loss", "negative")):
        return "negative"
    return "neutral"


def format_date(date_str: str | None, fallback: str = "Date unavailable") -> str:
    """Extract YYYY-MM-DD from an ISO timestamp without shifting time zones."""
    if not date_str:
        return fallback
    stripped = date_str.strip()
    if len(stripped) >= 10 and stripped[:10].replace("-", "").isdigit():
        return stripped[:10]
    return fallback


MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def format_chart_date(value: str | int | float) -> str:
    """Format calendar date for chart axis/tooltip (e.g. 'Aug 03').

    Matches original MarketChart.tsx formatChartDate contract.
    """
    raw = str(value)
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", raw)
    if m:
        try:
            month_idx = int(m.group(2)) - 1
            day_str = m.group(3)
            if 0 <= month_idx < 12:
                return f"{MONTH_NAMES[month_idx]} {day_str}"
        except Exception:
            pass
    return raw[:10]
