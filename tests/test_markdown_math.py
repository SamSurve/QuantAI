"""Tests for pure-python LaTeX to MathML rendering and editorial lead extraction."""

from __future__ import annotations

import pytest
from api.web.markdown import extract_editorial_lead, render_markdown


def test_inline_math_rendering():
    """Verify inline LaTeX $x^2 + y^2 = z^2$ converts to MathML."""
    raw = "The Pythagorean formula is $x^2 + y^2 = z^2$ in Cartesian space."
    html = render_markdown(raw)
    assert "<math" in html
    assert 'xmlns="http://www.w3.org/1998/Math/MathML"' in html
    assert "<msup>" in html
    assert "<mi>x</mi>" in html


def test_display_math_rendering():
    """Verify block display LaTeX $$\\frac{a}{b} = c$$ converts to block MathML."""
    raw = "The equation is:\n\n$$\\frac{a}{b} = c$$\n"
    html = render_markdown(raw)
    assert "<math" in html
    assert 'display="block"' in html
    assert "<mfrac>" in html


def test_malformed_math_graceful_fallback():
    """Verify broken LaTeX does not crash the renderer and renders safe escaped fallback."""
    raw = "Broken formula: $\\frac{unclosed$ still renders without crashing."
    html = render_markdown(raw)
    assert "Broken formula" in html
    assert "still renders" in html


def test_editorial_lead_extraction():
    """Verify extraction of the first meaningful paragraph line for the editorial pull quote."""
    markdown = (
        "# Morning Briefing\n"
        "## Key Points\n"
        "- Bullet 1\n"
        "- Bullet 2\n"
        "A services-led margin story, priced for perfection and exposed to regulatory changes in key jurisdictions.\n"
        "\n"
        "Further detailed paragraphs follow here."
    )
    lead = extract_editorial_lead(markdown)
    assert lead == "A services-led margin story, priced for perfection and exposed to regulatory changes in key jurisdictions."


def test_editorial_lead_fallback():
    """Verify short or empty markdown returns None for lead."""
    assert extract_editorial_lead(None) is None
    assert extract_editorial_lead("") is None
    assert extract_editorial_lead("Short line.") is None
