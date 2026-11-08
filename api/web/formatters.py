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


def format_indian_number(val: float | int, max_fraction_digits: int = 2) -> str:
    """Format a positive number using the Indian grouping system (en-IN).

    Group the lowest 3 digits together, then group preceding digits by pairs.
    """
    abs_val = abs(float(val))
    parts = f"{abs_val:.{max_fraction_digits}f}".split(".")
    int_part = parts[0]
    dec_part = "." + parts[1] if len(parts) > 1 and max_fraction_digits > 0 else ""
    if len(int_part) <= 3:
        return int_part + dec_part
    last3 = int_part[-3:]
    remaining = int_part[:-3]
    chunks: list[str] = []
    while len(remaining) > 2:
        chunks.append(remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        chunks.append(remaining)
    chunks.reverse()
    return ",".join(chunks) + "," + last3 + dec_part


def format_indian_compact(val: float | int, max_fraction_digits: int = 2) -> str:
    """Format compact amounts using standard Indian financial units (Lakh Cr, Cr, L, K)."""
    abs_val = abs(float(val))
    if abs_val >= 1e12:
        scaled = abs_val / 1e12
        unit = " Lakh Cr"
    elif abs_val >= 1e7:
        scaled = abs_val / 1e7
        unit = " Cr"
    elif abs_val >= 1e5:
        scaled = abs_val / 1e5
        unit = " L"
    elif abs_val >= 1e3:
        scaled = abs_val / 1e3
        unit = " K"
    else:
        scaled = abs_val
        unit = ""

    if unit:
        formatted = f"{scaled:.{max_fraction_digits}f}"
        return f"{formatted}{unit}"
    return format_indian_number(scaled, max_fraction_digits)


def money_label(
    value: float | int | None,
    currency: str | None = None,
    max_fraction_digits: int = 2,
) -> str:
    """Format currency values with appropriate symbol and decimals.

    Uses en-IN locale grouping for INR, whole units for JPY, and clean safe fallback
    when currency metadata is unavailable without inventing an ungrounded currency.
    """
    if value is None:
        return "—"
    try:
        val = float(value)
        if not math.isfinite(val):
            return "—"
    except (ValueError, TypeError):
        return "—"

    sign = "-" if val < 0 else ""
    abs_val = abs(val)

    if currency:
        curr_code = currency.strip().upper()
        symbol = CURRENCY_SYMBOLS.get(curr_code, f"{curr_code} ")
        if curr_code == "INR":
            formatted_num = format_indian_number(abs_val, max_fraction_digits)
            return f"{sign}{symbol}{formatted_num}"
        if curr_code == "JPY":
            abs_int = abs(int(round(val)))
            return f"{sign}{symbol}{abs_int:,}"
        formatted_num = f"{abs_val:,.{max_fraction_digits}f}"
        return f"{sign}{symbol}{formatted_num}"

    # Missing currency metadata -> safe fallback without inventing a currency
    formatted_num = f"{abs_val:,.{max_fraction_digits}f}"
    return f"{sign}{formatted_num}"


def compact_money_label(
    value: float | int | None,
    currency: str | None = None,
    max_fraction_digits: int = 2,
) -> str:
    """Format compact money strings like $3T or ₹12.50 Cr."""
    if value is None:
        return "—"
    try:
        val = float(value)
        if not math.isfinite(val):
            return "—"
    except (ValueError, TypeError):
        return "—"

    sign = "-" if val < 0 else ""
    abs_val = abs(val)

    if currency:
        curr_code = currency.strip().upper()
        symbol = CURRENCY_SYMBOLS.get(curr_code, f"{curr_code} ")
        if curr_code == "INR":
            compact_str = format_indian_compact(abs_val, max_fraction_digits)
            return f"{sign}{symbol}{compact_str}"
        compact_str = _format_compact(abs_val, max_fraction_digits)
        return f"{sign}{symbol}{compact_str}"

    compact_str = _format_compact(abs_val, max_fraction_digits)
    return f"{sign}{compact_str}"


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
