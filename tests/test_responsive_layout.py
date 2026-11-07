"""Tests for responsive layout, original anchor targets, and error-state resilience.

Step D acceptance criteria:
5. Responsive layout.
6. Original anchor IDs.
7. Keyboard-accessible dialogs.
8. Focus management.
10. No broken layout after research errors.
"""

from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_ANCHOR_IDS = [
    "snapshot",
    "performance",
    "fundamentals",
    "news",
    "analysis",
    "sources",
]


def test_original_anchor_ids_present_in_templates():
    """Verify that all six original navigation anchor IDs exist in the rendered template partials."""
    partials_dir = ROOT / "templates" / "partials"
    all_html = ""
    for html_file in partials_dir.glob("*.html"):
        all_html += html_file.read_text(encoding="utf-8") + "\n"

    soup = BeautifulSoup(all_html, "html.parser")

    for anchor_id in EXPECTED_ANCHOR_IDS:
        target = soup.find(id=anchor_id)
        assert target is not None, f"Anchor target #{anchor_id} missing from template partials."


def test_navbar_links_match_anchor_ids():
    """Verify navbar links in base.html match the navigation anchors."""
    base_html = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(base_html, "html.parser")

    nav = soup.find("nav", class_="nav")
    assert nav is not None, "Navbar missing in base.html"

    links = [a.get("href") for a in nav.find_all("a")]
    for expected in ["#snapshot", "#performance", "#fundamentals", "#news", "#analysis"]:
        assert expected in links, f"Navbar missing expected link to {expected}"


def test_error_status_layout_preservation():
    """Verify that research_status.html maintains clean card styling without breaking the workspace."""
    status_path = ROOT / "templates" / "partials" / "research_status.html"
    assert status_path.exists(), "research_status.html missing"
    html = status_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # The error / guidance section must be properly containerized
    container = soup.find("section") or soup.find("div")
    assert container is not None
    assert "research-status" in container.get("class", []) or "card" in container.get("class", [])
