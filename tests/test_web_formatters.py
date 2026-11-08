"""Tests for web formatting helpers."""

from __future__ import annotations

import math
import pytest

from api.web.formatters import (
    compact_money_label,
    format_date,
    format_indian_compact,
    format_indian_number,
    money_label,
    number_label,
    percent_label,
    tone_for,
)


def test_number_label():
    assert number_label(None) == "—"
    assert number_label(float("nan")) == "—"
    assert number_label(float("inf")) == "—"
    assert number_label(1234567) == "1,234,567"
    assert number_label(1234.5678, max_fraction_digits=2) == "1,234.57"
    assert number_label(0) == "0"
    assert number_label(50_000_000, notation="compact") == "50M"
    assert number_label(1_500_000_000, notation="compact") == "1.5B"


def test_indian_number_formatting():
    """Verify Indian numbering system (en-IN): last 3 digits, then pairs."""
    assert format_indian_number(2845.50) == "2,845.50"
    assert format_indian_number(125000.00) == "1,25,000.00"
    assert format_indian_number(10000000.00) == "1,00,00,000.00"
    assert format_indian_number(500.0) == "500.00"
    assert format_indian_number(0.0) == "0.00"


def test_indian_compact_formatting():
    """Verify Indian compact units (Lakh Cr, Cr, L, K)."""
    assert format_indian_compact(125_000_000) == "12.50 Cr"
    assert format_indian_compact(17_916_992_946_176) == "17.92 Lakh Cr"
    assert format_indian_compact(250_000) == "2.50 L"
    assert format_indian_compact(1_500) == "1.50 K"


def test_money_label():
    assert money_label(None) == "—"
    # Safe fallback when currency is unavailable (never invent an ungrounded currency)
    assert money_label(200.5) == "200.50"
    assert money_label(200.5, currency="USD") == "$200.50"
    assert money_label(200.5, currency="EUR") == "€200.50"
    assert money_label(200.5, currency="GBP") == "£200.50"
    assert money_label(200.5, currency="INR") == "₹200.50"
    assert money_label(2845.50, currency="INR") == "₹2,845.50"
    assert money_label(125000.00, currency="INR") == "₹1,25,000.00"
    assert money_label(200.5, currency="JPY") == "¥200"
    assert money_label(-5.2, currency="USD") == "-$5.20"
    assert money_label(-2845.50, currency="INR") == "-₹2,845.50"


def test_compact_money_label():
    assert compact_money_label(None) == "—"
    assert compact_money_label(3_000_000_000_000, currency="USD") == "$3T"
    assert compact_money_label(500_500_000, currency="USD") == "$500.5M"
    assert compact_money_label(10_200_000_000, currency="USD") == "$10.2B"
    assert compact_money_label(1_500, currency="USD") == "$1.5K"
    assert compact_money_label(500, currency="USD") == "$500"
    # Indian compact currency
    assert compact_money_label(125_000_000, currency="INR") == "₹12.50 Cr"
    assert compact_money_label(17_916_992_946_176, currency="INR") == "₹17.92 Lakh Cr"
    # Fallback without currency
    assert compact_money_label(500_500_000) == "500.5M"


def test_percent_label():
    assert percent_label(None) == "—"
    assert percent_label(1.25) == "+1.25%"
    assert percent_label(-0.5) == "-0.50%"
    assert percent_label(0) == "0.00%"
    assert percent_label(1.25, include_sign=False) == "1.25%"


def test_tone_for():
    assert tone_for("+1.25%") == "positive"
    assert tone_for("gain") == "positive"
    assert tone_for("up") == "positive"
    assert tone_for("-0.50%") == "negative"
    assert tone_for("loss") == "negative"
    assert tone_for("down") == "negative"
    assert tone_for("0.00%") == "neutral"
    assert tone_for("—") == "neutral"


def test_format_date():
    assert format_date(None) == "Date unavailable"
    assert format_date("") == "Date unavailable"
    assert format_date("2026-11-01T15:30:00Z") == "2026-11-01"
    assert format_date("2026-11-01") == "2026-11-01"
