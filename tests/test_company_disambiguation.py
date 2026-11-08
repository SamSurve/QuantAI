"""Regression and integration tests for interactive company disambiguation.

Tests:
1. Unique company name search resolves directly.
2. Ambiguous query (e.g. 'Mahindra') returns candidates and disambiguation UI.
3. Candidate cards contain ticker, name, exchange, and selection action.
4. Dedicated /api/companies/search endpoint returns structured validated data.
5. Direct ticker search regression (AAPL, MSFT, M&M.NS) bypasses disambiguation.
6. Safety rule: No arbitrary selection of first candidate on ambiguous search.
7. Empty candidate query handling.
8. Provider timeout and error degradation.
9. Indian company selection (.NS, .BO) preserves INR currency formatting.
10. International company selection preserves USD / native currency.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

from bs4 import BeautifulSoup
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.index import app
from api.research_schemas import CompanyCandidate
from api.research_services import EntityResolutionService

client = TestClient(app)


def test_dedicated_company_search_endpoint_with_results():
    """Verify /api/companies/search returns structured candidates for ambiguous search."""
    response = client.get("/api/companies/search?query=mahindra")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "mahindra"
    assert data["count"] > 0
    assert len(data["candidates"]) == data["count"]

    symbols = [c["symbol"] for c in data["candidates"]]
    assert any("M&M" in s for s in symbols)
    for c in data["candidates"]:
        assert "symbol" in c
        assert "name" in c
        assert "exchange" in c
        assert "quote_type" in c


def test_dedicated_company_search_endpoint_empty():
    """Verify /api/companies/search with blank query returns empty list."""
    response = client.get("/api/companies/search?query=")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == ""
    assert data["count"] == 0
    assert data["candidates"] == []


def test_dedicated_company_search_endpoint_prefix_stripped():
    """Verify /companies/search fallback route works identically."""
    response = client.get("/companies/search?query=mahindra")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0


def test_ambiguous_company_search_renders_disambiguation_ui():
    """Verify ambiguous query 'mahindra' renders interactive disambiguation cards without error banners."""
    response = client.get("/research?query=mahindra", headers={"Accept": "text/html"})
    assert response.status_code == 200
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Verify disambiguation section
    section = soup.find(id="company-disambiguation")
    assert section is not None, "#company-disambiguation section missing in HTML"
    assert "Which company are you looking for?" in section.get_text()

    # Verify no error warning banner
    assert "Research request needs attention" not in html
    assert "More than one company matched. Try a ticker" not in html

    # Verify candidate cards
    cards = section.find_all(class_="disambiguation-card")
    assert len(cards) >= 2, f"Expected multiple candidate cards, found {len(cards)}"

    # Check first card structure
    first_card = cards[0]
    ticker = first_card.find(class_="disambiguation-ticker")
    assert ticker is not None
    assert ticker.get_text(strip=True) != ""

    name = first_card.find(class_="disambiguation-name")
    assert name is not None
    assert name.get_text(strip=True) != ""

    # Check selection action
    select_btn = first_card.find(class_="disambiguation-select-btn")
    assert select_btn is not None
    assert "Research this company" in select_btn.get_text()
    assert select_btn.get("data-select-ticker") is not None


def test_candidate_selection_launches_research_with_inr():
    """Verify searching chosen candidate 'M&M.NS' loads dashboard with INR formatting."""
    response = client.get("/research?query=M%26M.NS", headers={"Accept": "text/html"})
    assert response.status_code == 200
    html = response.text

    # No disambiguation for exact symbol
    assert "Which company are you looking for?" not in html
    # Ticker present (HTML entity &amp; or direct &)
    assert "M&amp;M.NS" in html or "M&M.NS" in html
    # INR currency symbol (₹) present in dossier / pricing
    assert "₹" in html or "INR" in html


def test_direct_ticker_search_preserves_usd():
    """Verify direct ticker AAPL loads dashboard without disambiguation and with USD."""
    response = client.get("/research?query=AAPL", headers={"Accept": "text/html"})
    assert response.status_code == 200
    html = response.text

    assert "Which company are you looking for?" not in html
    assert "AAPL" in html
    assert "$" in html or "USD" in html


def test_no_arbitrary_first_result_selection():
    """Verify EntityResolutionService still rejects picking the first result silently when ambiguous."""
    service = EntityResolutionService()
    candidates = [
        CompanyCandidate(symbol="M&M.NS", name="Mahindra & Mahindra Limited", exchange="NSI", quote_type="EQUITY"),
        CompanyCandidate(symbol="M&MFIN.NS", name="Mahindra & Mahindra Financial Services", exchange="NSI", quote_type="EQUITY"),
    ]
    selected = service._select_candidate("mahindra", candidates)
    assert selected is None, "Resolver must not arbitrarily select first candidate for ambiguous query"


def test_provider_timeout_graceful_handling():
    """Verify candidate search gracefully handles provider timeout."""
    service = EntityResolutionService()
    with patch.object(service, "_search_candidates", side_effect=TimeoutError("Provider timeout")):
        # search_candidates should return empty list rather than crashing
        import asyncio
        results = asyncio.run(service.search_candidates("timeout_test"))
        assert results == []


def test_nonexistent_company_shows_polite_not_found():
    """Verify search for a non-existent company shows clean not-found guidance."""
    response = client.get("/research?query=XYZNONEXISTENT9999", headers={"Accept": "text/html"})
    assert response.status_code == 200
    html = response.text
    assert "Which company are you looking for?" not in html
    assert "No verified company record was found" in html or "needs attention" in html
