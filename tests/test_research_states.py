"""Tests for research status rendering, error guidance, and loading skeleton states.

Verifies idle, checking, success, partial, error states, and sanitized guidance.
"""

from __future__ import annotations

from pathlib import Path
import pytest
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def test_research_status_idle():
    """Verify idle state shows ready message."""
    template = env.get_template("partials/research_status.html")
    rendered = template.render(state="idle")
    assert "Ready for a company or ticker" in rendered or "Ready" in rendered


def test_research_status_loading():
    """Verify loading/checking state renders spinner/progress indication."""
    template = env.get_template("partials/research_status.html")
    rendered = template.render(state="loading", query="AAPL")
    assert "Building a sourced research record" in rendered or "Checking" in rendered


def test_research_status_ambiguous_guidance():
    """Verify ambiguous entity error displays recovery guidance."""
    template = env.get_template("partials/research_status.html")
    rendered = template.render(
        state="error",
        error_kind="ambiguous",
        error_message="Multiple companies match this query.",
    )
    assert "More than one company matched" in rendered
    assert "Traceback" not in rendered


def test_research_status_not_found_guidance():
    """Verify not-found entity error displays recovery guidance."""
    template = env.get_template("partials/research_status.html")
    rendered = template.render(
        state="error",
        error_kind="not_found",
        error_message="No supported listed company found.",
    )
    assert "No verified company record was found" in rendered
    assert "Traceback" not in rendered


def test_research_status_ai_unavailable_notice():
    """Verify AI unavailable notice keeps deterministic market data usable."""
    template = env.get_template("partials/research_status.html")
    rendered = template.render(
        state="partial",
        error_kind="ai_unavailable",
        error_message="AI analysis is temporarily unavailable.",
    )
    assert "optional AI interpretation is temporarily unavailable" in rendered
    assert "sourced research record remains useful" in rendered


def test_research_skeleton_structure():
    """Verify loading skeleton renders cards with shimmer animation."""
    template = env.get_template("partials/research_skeleton.html")
    rendered = template.render()
    assert "shimmer" in rendered
    assert "card" in rendered
    assert "role=\"status\"" in rendered or "aria-busy=\"true\"" in rendered
