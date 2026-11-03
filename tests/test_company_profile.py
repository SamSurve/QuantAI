"""Tests for company profile presentation, URL sanitization, and missing-data handling."""

from __future__ import annotations

import pytest
from fastapi.templating import Jinja2Templates

from api.research_schemas import CompanyIdentity, CompanyOverview
from api.web.company_profile import (
    CompanyProfileView,
    format_company_profile,
    is_safe_website_url,
)


def test_is_safe_website_url():
    """Verify website URL security: only http and https are allowed."""
    assert is_safe_website_url("https://www.apple.com") is True
    assert is_safe_website_url("http://example.com/investors") is True
    assert is_safe_website_url("HTTPS://SECURE.ORG") is True

    # Unsafe schemes rejected
    assert is_safe_website_url("javascript:alert(1)") is False
    assert is_safe_website_url("data:text/html,bad") is False
    assert is_safe_website_url("ftp://ftp.example.com") is False
    assert is_safe_website_url("file:///etc/passwd") is False
    assert is_safe_website_url("") is False
    assert is_safe_website_url(None) is False


def test_company_profile_full_mapping():
    """Verify full company profile maps all fields correctly."""
    overview = CompanyOverview(
        company_name="Apple Inc.",
        ticker="AAPL",
        exchange="NASDAQ",
        sector="Technology",
        industry="Consumer Electronics",
        country="United States",
        headquarters="Cupertino, California",
        website="https://www.apple.com",
        business_description="Designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories.",
        employees=161000,
    )
    identity = CompanyIdentity(
        symbol="AAPL",
        name="Apple Inc.",
        exchange="NASDAQ",
        sector="Technology",
        industry="Consumer Electronics",
        identifier_confidence="high",
    )

    profile = format_company_profile(overview, identity)

    assert profile.company_name == "Apple Inc."
    assert profile.ticker == "AAPL"
    assert profile.exchange == "NASDAQ"
    assert profile.sector == "Technology"
    assert profile.industry == "Consumer Electronics"
    assert profile.country == "United States"
    assert profile.headquarters == "Cupertino, California"
    assert profile.website == "https://www.apple.com"
    assert profile.is_safe_website is True
    assert profile.employees == "161,000"
    assert "smartphones" in (profile.description or "")
    assert profile.has_profile is True


def test_company_profile_missing_data_never_invented():
    """Verify missing fields remain unavailable, never fabricated."""
    overview = CompanyOverview(
        ticker="AAPL",
        business_description="Minimal description.",
    )
    identity = CompanyIdentity(symbol="AAPL", name="Apple Inc.", identifier_confidence="high")

    profile = format_company_profile(overview, identity)

    assert profile.company_name == "Apple Inc."
    assert profile.ticker == "AAPL"
    assert profile.country is None
    assert profile.headquarters is None
    assert profile.website is None
    assert profile.is_safe_website is False
    assert profile.employees is None
    assert profile.description == "Minimal description."


def test_company_profile_unsafe_website_neutralized():
    """Verify unsafe website URLs are neutralized."""
    overview = CompanyOverview(
        ticker="XYZ",
        website="javascript:stealTokens()",
    )
    profile = format_company_profile(overview, None)
    assert profile.is_safe_website is False


def test_company_profile_template_rendering():
    """Verify template renders safe links with rel=noopener noreferrer."""
    templates = Jinja2Templates(directory="templates")

    overview = CompanyOverview(
        company_name="Tesla, Inc.",
        ticker="TSLA",
        country="United States",
        headquarters="Austin, Texas",
        website="https://www.tesla.com",
        employees=140473,
        business_description="Designs and manufactures electric vehicles and energy systems.",
    )
    identity = CompanyIdentity(
        symbol="TSLA",
        name="Tesla, Inc.",
        exchange="NASDAQ",
        sector="Consumer Cyclical",
        industry="Auto Manufacturers",
        identifier_confidence="high",
    )
    profile = format_company_profile(overview, identity)

    html = templates.get_template("partials/company_profile.html").render({"profile": profile})

    assert "Company profile" in html
    assert "United States" in html
    assert "140,473" in html
    assert 'href="https://www.tesla.com"' in html
    assert 'rel="noopener noreferrer"' in html
    assert 'target="_blank"' in html
