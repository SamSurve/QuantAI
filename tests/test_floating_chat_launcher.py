"""Tests for floating research desk chat launcher, drawer header, and empty state."""

from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient

from api.index import app

ROOT = Path(__file__).resolve().parents[1]
DRAWER_HTML_PATH = ROOT / "templates" / "partials" / "chat_drawer.html"


def test_floating_launcher_button_markup():
    """Verify floating launcher button has compact circular markup, tooltip, and accessible labels."""
    html = DRAWER_HTML_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    toggle = soup.find(id="chat-toggle")
    assert toggle is not None, "#chat-toggle button missing"
    assert "chat-floating-btn" in toggle.get("class", [])
    assert toggle.get("title") == "Ask QuantAI"
    assert toggle.get("aria-label") == "Ask QuantAI"

    # Tooltip element
    tooltip = toggle.find(class_="chat-launcher-tooltip")
    assert tooltip is not None, ".chat-launcher-tooltip missing"
    assert tooltip.get_text(strip=True) == "Ask QuantAI"

    # Accessible text for screen readers and parity
    sr_text = toggle.find(class_="sr-only")
    assert sr_text is not None, ".sr-only element missing"
    assert "Ask the research desk" in sr_text.get_text()

    # SVG chat icon
    svg = toggle.find("svg")
    assert svg is not None, "Chat icon SVG missing inside toggle button"


def test_chat_drawer_header_controls():
    """Verify drawer header contains branding, title, connection status, minimize and close controls."""
    html = DRAWER_HTML_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    drawer = soup.find(id="chat-drawer")
    assert drawer is not None, "#chat-drawer missing"

    # Header controls
    minimize_btn = drawer.find(id="chat-minimize")
    assert minimize_btn is not None, "#chat-minimize button missing"
    assert minimize_btn.get("aria-label") == "Minimize chat"

    close_btn = drawer.find(id="chat-close")
    assert close_btn is not None, "#chat-close button missing"
    assert close_btn.get("aria-label") == "Close chat"

    # Connection health indicator
    conn_dot = drawer.find(id="chat-connection-dot")
    assert conn_dot is not None, "#chat-connection-dot missing"

    conn_text = drawer.find(id="chat-connection-text")
    assert conn_text is not None, "#chat-connection-text missing"
    assert "Ready" in conn_text.get_text()

    # Branding and title
    assert "Research Desk" in drawer.get_text()
    assert "Groq Finance Agent" in drawer.get_text()


def test_chat_empty_state_welcoming_interface():
    """Verify welcoming empty state with title, explanation, and 4 example prompt chips."""
    html = DRAWER_HTML_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    empty_state = soup.find(id="chat-empty-state")
    assert empty_state is not None, "#chat-empty-state missing"

    text = empty_state.get_text()
    assert "Your Research Desk" in text
    assert "Ask questions about companies, market movements, financial metrics and research findings." in text

    # Verify all 4 example prompt chips
    chips = empty_state.find_all("button", class_="chat-example-chip")
    assert len(chips) == 4, f"Expected 4 example prompt chips, found {len(chips)}"

    expected_prompts = [
        "Explain Reliance's latest performance.",
        "What are the key risks for NVIDIA?",
        "Compare TCS and Infosys.",
        "Explain the latest market signals.",
    ]

    observed_prompts = [chip.get("data-prompt") for chip in chips]
    assert observed_prompts == expected_prompts


def test_multiline_input_textarea():
    """Verify chat input form uses multiline textarea with submit button."""
    html = DRAWER_HTML_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    form = soup.find(id="chat-form")
    assert form is not None, "#chat-form missing"

    textarea = form.find("textarea", id="chat-input")
    assert textarea is not None, "#chat-input must be a textarea for multiline support"
    assert textarea.get("placeholder") == "Ask a financial question..."

    submit = form.find(id="chat-submit")
    assert submit is not None, "#chat-submit button missing"
    assert submit.get("type") == "submit"


def test_home_page_renders_floating_chat():
    """Verify home page HTML includes the floating launcher and chat drawer."""
    client = TestClient(app)
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.status_code == 200
    html = response.text

    assert 'id="chat-toggle"' in html
    assert 'class="chat-floating-btn"' in html
    assert 'id="chat-drawer"' in html
    assert "Your Research Desk" in html
    assert 'id="chat-minimize"' in html
    assert 'id="chat-close"' in html
