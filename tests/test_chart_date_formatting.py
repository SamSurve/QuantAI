"""Port of tests/test_chart_date_formatting.ts to Python pytest.

Preserves exact date formatting, calendar boundary behavior, timezone preservation,
and invalid timestamp truncation.
"""

from __future__ import annotations

import pytest
from api.web.formatters import format_chart_date


def test_chart_date_formatting_regression():
    """Exact port of original test_chart_date_formatting.ts assertions."""
    # Chart date formatter changed the returned calendar date
    assert format_chart_date("2026-08-03T00:00:00+05:30") == "Aug 03"

    # Chart date formatter did not produce the requested readable label
    assert format_chart_date("2026-08-27T00:00:00Z") == "Aug 27"

    # Chart date formatter should avoid displaying a raw long invalid value
    assert format_chart_date("not-a-timestamp") == "not-a-time"


def test_chart_date_formatting_additional_cases():
    """Verify various months, days, leap years and short strings."""
    assert format_chart_date("2024-02-29T12:00:00Z") == "Feb 29"
    assert format_chart_date("2026-01-01T00:00:00Z") == "Jan 01"
    assert format_chart_date("2026-12-31T23:59:59-05:00") == "Dec 31"
    assert format_chart_date("short") == "short"
    assert format_chart_date("") == ""
