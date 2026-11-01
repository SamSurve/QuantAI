"""Tests for web formatting helpers."""

from __future__ import annotations

import math
import pytest

from api.web.formatters import (
    compact_money_label,
    format_date,
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


def test_money_label():
    assert money_label(None) == "—"
    assert money_label(200.5) == "$200.50"
    assert money_label(200.5, currency="USD") == "$200.50"
    assert money_label(200.5, currency="EUR") == "€200.50"
    assert money_label(200.5, currency="GBP") == "£200.50"
    assert money_label(200.5, currency="INR") == "₹200.50"
    assert money_label(200.5, currency="JPY") == "¥200"
    assert money_label(-5.2, currency="USD") == "-$5.20"


def test_compact_money_label():
    assert compact_money_label(None) == "—"
    assert compact_money_label(3_000_000_000_000, currency="USD") == "$3T"
    assert compact_money_label(500_500_000, currency="USD") == "$500.5M"
    assert compact_money_label(10_200_000_000, currency="USD") == "$10.2B"
    assert compact_money_label(1_500, currency="USD") == "$1.5K"
    assert compact_money_label(500, currency="USD") == "$500"


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
