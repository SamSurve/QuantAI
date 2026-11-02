"""Ported regression test from E:\\Quant-AI\\tests\\test_research_error_guidance.ts.

Verifies classification of public error strings into recovery categories:
ambiguous, not_found, ai_unavailable, news_unavailable, other.
"""

from __future__ import annotations

import pytest
from api.web.research import classify_research_error, get_recovery_message

CASES: list[tuple[str, str]] = [
    ("Multiple companies match this query. Select a listed ticker to continue.", "ambiguous"),
    ("No supported listed company or ticker was found for this query.", "not_found"),
    ("AI analysis is temporarily unavailable. Please try again shortly.", "ai_unavailable"),
    ("Current news is temporarily unavailable. Other research data may still be available.", "news_unavailable"),
    ("Research is temporarily unavailable. Please try again shortly.", "other"),
]


@pytest.mark.parametrize("message, expected_kind", CASES)
def test_research_error_kind_regression(message: str, expected_kind: str):
    """Exact parity with test_research_error_guidance.ts assertions."""
    assert classify_research_error(message) == expected_kind


def test_recovery_messages():
    """Verify safe public guidance messages for each error kind."""
    assert (
        get_recovery_message("Multiple companies match this query. Select a listed ticker to continue.")
        == "More than one company matched. Try a ticker or a more specific company name."
    )
    assert (
        get_recovery_message("No supported listed company or ticker was found for this query.")
        == "No verified company record was found. Check the spelling or search by ticker."
    )
    assert (
        get_recovery_message("AI analysis is temporarily unavailable. Please try again shortly.")
        == "The sourced research record remains useful, but optional AI interpretation is temporarily unavailable."
    )
    assert (
        get_recovery_message("Current news is temporarily unavailable. Other research data may still be available.")
        == "The research record is available with a missing news source. Other sourced evidence remains visible."
    )
    assert (
        get_recovery_message("Research is temporarily unavailable. Please try again shortly.")
        == "The request could not complete. Check the research endpoint, then try again."
    )
