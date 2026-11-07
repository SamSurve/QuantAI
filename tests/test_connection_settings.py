"""Tests for connection settings, statuses (Ready, Checking, Offline), and browser-storage contract.

Step D acceptance criteria:
1. Ready, Checking and Offline connection statuses.
2. Refresh/re-check button.
3. Endpoint settings dialog.
4. Browser storage key analysts-ledger-agentos-url.
5. URL persistence in browser contract.
6. Browser chat and health logic isolated from server research.
"""

from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

from api.web.connection import (
    CONNECTION_STORAGE_KEY,
    ConnectionState,
    get_connection_status_label,
    normalize_endpoint_url,
)

ROOT = Path(__file__).resolve().parents[1]


def test_connection_status_semantic_labels():
    """Verify exact semantic labels Ready, Checking, and Offline."""
    assert get_connection_status_label("ready") == "Ready"
    assert get_connection_status_label("checking") == "Checking"
    assert get_connection_status_label("offline") == "Offline"
    assert get_connection_status_label(ConnectionState.READY) == "Ready"
    assert get_connection_status_label(ConnectionState.CHECKING) == "Checking"
    assert get_connection_status_label(ConnectionState.OFFLINE) == "Offline"


def test_browser_storage_key_constant():
    """Verify exact browser localStorage key analysts-ledger-agentos-url."""
    assert CONNECTION_STORAGE_KEY == "analysts-ledger-agentos-url"


def test_endpoint_url_normalization():
    """Verify endpoint URL normalization strips trailing slashes and whitespace."""
    assert normalize_endpoint_url("  /api/  ") == "/api"
    assert normalize_endpoint_url("http://localhost:8000/api///") == "http://localhost:8000/api"
    assert normalize_endpoint_url("/agentos") == "/api"  # Legacy /agentos mapped to /api
    assert normalize_endpoint_url("") == "/api"


def test_connection_health_template_structure():
    """Verify connection_health.html partial exists and contains status indicators and refresh button."""
    template_path = ROOT / "templates" / "partials" / "connection_health.html"
    assert template_path.exists(), "connection_health.html missing"
    html = template_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    indicator = soup.find(id="connection-indicator")
    assert indicator is not None, "#connection-indicator missing"

    refresh_btn = soup.find(id="connection-refresh-btn")
    assert refresh_btn is not None, "#connection-refresh-btn missing"
    assert "Check research endpoint" in (refresh_btn.get("aria-label", "") or refresh_btn.get("title", ""))


def test_endpoint_settings_dialog_template_structure():
    """Verify endpoint_settings.html partial exists and has correct modal attributes and inputs."""
    template_path = ROOT / "templates" / "partials" / "endpoint_settings.html"
    assert template_path.exists(), "endpoint_settings.html missing"
    html = template_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    dialog = soup.find(id="endpoint-settings-dialog")
    assert dialog is not None, "#endpoint-settings-dialog missing"
    assert dialog.get("role") == "dialog"
    assert dialog.get("aria-modal") == "true"
    assert "Research endpoint settings" in dialog.get("aria-label", "")

    input_el = soup.find(id="endpoint-url-input")
    assert input_el is not None, "#endpoint-url-input missing"

    save_btn = soup.find(id="endpoint-save-btn")
    assert save_btn is not None, "#endpoint-save-btn missing"
