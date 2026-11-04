"""Tests for AI research brief presentation, non-blocking fallback, and template rendering."""

from __future__ import annotations

import pytest
from fastapi.templating import Jinja2Templates

from api.web.analysis import AnalysisBriefView, process_analysis_brief


def test_analysis_brief_processing_with_markdown_and_lead():
    """Verify analysis brief extracts editorial lead and renders sanitized HTML."""
    raw = (
        "# Executive Assessment\n"
        "A services-led margin story, priced for perfection and exposed to regulatory changes in key jurisdictions.\n\n"
        "Here is formula $E = mc^2$ and key risks:\n"
        "- Supply chain volatility\n"
        "- Regulatory compliance\n"
    )

    view = process_analysis_brief(raw)
    assert view.has_analysis is True
    assert view.is_unavailable is False
    assert view.lead == "A services-led margin story, priced for perfection and exposed to regulatory changes in key jurisdictions."
    assert "<math" in view.rendered_html
    assert "Supply chain volatility" in view.rendered_html


def test_analysis_brief_unavailable_non_blocking():
    """Verify unavailable state sets friendly notice without crashing or inventing text."""
    view = process_analysis_brief(None, is_unavailable=True, notice="AI service busy")
    assert view.has_analysis is False
    assert view.is_unavailable is True
    assert "AI service busy" in (view.unavailable_notice or "")


def test_analysis_brief_empty():
    """Verify empty or None analysis returns clean empty view."""
    view = process_analysis_brief(None)
    assert view.has_analysis is False
    assert view.lead is None
    assert view.rendered_html == ""


def test_analysis_brief_template_rendering():
    """Verify partials/analysis_brief.html renders correctly."""
    templates = Jinja2Templates(directory="templates")

    view = AnalysisBriefView(
        has_analysis=True,
        is_unavailable=False,
        lead="A services-led margin story, priced for perfection and exposed to regulation.",
        rendered_html="<p>Detailed analysis body with <math display='inline'><mi>x</mi></math></p>",
    )

    html = templates.get_template("partials/analysis_brief.html").render({"analysis_brief": view})

    assert 'id="analysis"' in html
    assert "AI research brief" in html
    assert "Interpretation · not evidence" in html
    assert "A services-led margin story" in html
    assert "<math" in html


def test_analysis_brief_unavailable_template_rendering():
    """Verify partials/analysis_brief.html renders non-blocking unavailable notice."""
    templates = Jinja2Templates(directory="templates")

    view = AnalysisBriefView(
        has_analysis=False,
        is_unavailable=True,
        unavailable_notice="AI interpretation is temporarily unavailable.",
    )

    html = templates.get_template("partials/analysis_brief.html").render({"analysis_brief": view})

    assert 'id="analysis"' in html
    assert "Interpretation · not evidence" in html
    assert "AI interpretation is temporarily unavailable" in html
    assert "The sourced market record remains visible" in html
