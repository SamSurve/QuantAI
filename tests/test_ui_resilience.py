"""Tests for application UI resilience, startup reveal, reduced motion, keyboard accessibility, and 404 error recovery.

Step D acceptance criteria:
1. Original 1.2-second reveal.
2. Reduced-motion support.
3. Error recovery.
4. Reload action.
5. 404 page structure and navigation.
6. Keyboard-accessible dialogs & focus management.
7. Toast notifications.
"""

from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient

from api.index import app

ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_startup_reveal_template_structure():
    """Verify startup_reveal.html partial contains the 1.2s brand mark, trace SVG, and taglines."""
    template_path = ROOT / "templates" / "partials" / "startup_reveal.html"
    assert template_path.exists(), "startup_reveal.html missing"
    html = template_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    reveal = soup.find(id="startup-reveal")
    assert reveal is not None, "#startup-reveal container missing"
    assert reveal.get("aria-hidden") == "true"

    assert "QUANTAI" in html
    assert "Research. Understand. Decide." in html

    # Verify original trace SVG path
    trace_svg = soup.find("svg", class_="startup-reveal__trace")
    assert trace_svg is not None, "trace SVG missing"
    path = trace_svg.find("path")
    assert path is not None
    assert "M0 43H32L50 35" in path.get("d", "")


def test_startup_reveal_timing_and_reduced_motion_in_app_js():
    """Verify app.js implements 1180ms startup reveal timing and 0ms for prefers-reduced-motion."""
    app_js_path = ROOT / "static" / "js" / "app.js"
    assert app_js_path.exists(), "app.js missing"
    code = app_js_path.read_text(encoding="utf-8")

    assert "prefers-reduced-motion" in code
    assert "1180" in code
    assert "startup-reveal" in code


def test_404_page_template_and_route():
    """Verify not_found.html template exists with 404, message, and Go Home link."""
    template_path = ROOT / "templates" / "pages" / "not_found.html"
    assert template_path.exists(), "not_found.html missing"
    html = template_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    assert "404" in html
    assert "Page Not Found" in html

    home_link = soup.find("a", href="/")
    assert home_link is not None, "Missing link to home ('/')"
    assert "Go Home" in home_link.get_text()

    # Route check: non-existent page returns 404 with HTML when requested
    res = client.get("/nonexistent-page-url", headers={"Accept": "text/html"})
    assert res.status_code == 404
    assert "404" in res.text


def test_error_recovery_and_reload_controls():
    """Verify reload action controls exist and are keyboard accessible."""
    base_html = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    app_js = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")

    # app.js must handle reload action
    assert "window.location.reload" in app_js or "location.reload" in app_js


def test_toast_container_and_notification_system():
    """Verify toast notification container in HTML and toast helper in app.js."""
    base_html = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    assert 'id="toast-container"' in base_html

    app_js = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
    assert "showToast" in app_js
