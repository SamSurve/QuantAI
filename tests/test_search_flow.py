"""Tests for company search flow and quick-search shortcuts.

Verifies normalization, starter tickers, absence of user mode picker,
and template rendering for search form and quick chips.
"""

from __future__ import annotations

import pytest
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from api.web import search

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def test_normalize_search_query():
    """Verify search normalization trims whitespace and preserves case."""
    assert search.normalize_search_query("  AAPL  ") == "AAPL"
    assert search.normalize_search_query("Microsoft Corporation") == "Microsoft Corporation"
    assert search.normalize_search_query("   ") == ""
    assert search.normalize_search_query("") == ""


def test_starter_tickers_list():
    """Verify original four starter tickers are present in exact order."""
    assert search.STARTER_TICKERS == ["AAPL", "MSFT", "NVDA", "TSLA"]


def test_search_form_template_rendering():
    """Verify search_form partial renders pill input, button, and quick chips."""
    template = env.get_template("partials/search_form.html")
    rendered = template.render(starter_tickers=search.STARTER_TICKERS)

    assert 'action="/research"' in rendered
    assert 'name="query"' in rendered
    assert 'placeholder="Search a company or ticker"' in rendered
    assert "Research" in rendered
    assert "AAPL" in rendered
    assert "MSFT" in rendered
    assert "NVDA" in rendered
    assert "TSLA" in rendered
    assert "chip" in rendered


def test_no_mode_picker_in_search():
    """Confirm there is NO user-selectable research mode dropdown or toggle in search UI."""
    template = env.get_template("partials/search_form.html")
    rendered = template.render(starter_tickers=search.STARTER_TICKERS)

    # Must NOT have mode picker
    assert "market_intelligence" not in rendered
    assert "company_deep_analysis" not in rendered
    assert "select mode" not in rendered.lower()
    assert "choose mode" not in rendered.lower()


def test_home_page_includes_search_form():
    """Verify home.html includes search partial."""
    template = env.get_template("pages/home.html")
    rendered = template.render(starter_tickers=search.STARTER_TICKERS)

    assert "Research any company." in rendered
    assert "Know what is evidence." in rendered
    assert "AAPL" in rendered
    assert "search-input" in rendered
