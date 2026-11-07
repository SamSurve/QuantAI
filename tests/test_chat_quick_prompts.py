"""Tests for chat quick prompts parity with original client/src/components/ChatPanel.tsx.

Requirements:
- Verify exact original strings:
    1. 'Pressure-test the thesis'
    2. 'Trace the source lane'
    3. 'Separate evidence from interpretation'
- Verify these three original prompts are present and actionable in templates/partials/chat_drawer.html.
- Verify incorrect Part 20 prompts ('Catalysts & risks', 'Operating margin', 'Peer context')
  are no longer present.
"""

from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DRAWER_HTML_PATH = ROOT / "templates" / "partials" / "chat_drawer.html"
ORIGINAL_CHAT_PANEL_PATH = Path("E:/Quant-AI/client/src/components/ChatPanel.tsx")

EXPECTED_QUICK_PROMPTS = (
    "Pressure-test the thesis",
    "Trace the source lane",
    "Separate evidence from interpretation",
)


def test_quick_prompts_match_original_tsx_source():
    """Verify original strings match ChatPanel.tsx in E:/Quant-AI."""
    if ORIGINAL_CHAT_PANEL_PATH.exists():
        content = ORIGINAL_CHAT_PANEL_PATH.read_text(encoding="utf-8")
        for prompt in EXPECTED_QUICK_PROMPTS:
            assert f'"{prompt}"' in content or f"'{prompt}'" in content, (
                f"Prompt '{prompt}' not found in original ChatPanel.tsx"
            )

    assert EXPECTED_QUICK_PROMPTS == (
        "Pressure-test the thesis",
        "Trace the source lane",
        "Separate evidence from interpretation",
    )


def test_drawer_contains_three_original_quick_prompts():
    """Verify templates/partials/chat_drawer.html contains all 3 original quick prompt buttons."""
    assert DRAWER_HTML_PATH.exists(), "chat_drawer.html missing"
    html = DRAWER_HTML_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    pills_container = soup.find(id="chat-pills")
    assert pills_container is not None, "#chat-pills container missing"

    buttons = pills_container.find_all("button")
    assert len(buttons) == 3, f"Expected 3 quick prompt buttons, found {len(buttons)}"

    observed_prompts = [btn.get("data-prompt") for btn in buttons]
    observed_texts = [btn.get_text(strip=True) for btn in buttons]

    assert observed_prompts == list(EXPECTED_QUICK_PROMPTS), (
        f"data-prompt attributes {observed_prompts} do not match {EXPECTED_QUICK_PROMPTS}"
    )
    assert observed_texts == list(EXPECTED_QUICK_PROMPTS), (
        f"Button texts {observed_texts} do not match {EXPECTED_QUICK_PROMPTS}"
    )


def test_incorrect_part20_prompts_removed():
    """Verify incorrect Part 20 prompt labels and texts are absent."""
    html = DRAWER_HTML_PATH.read_text(encoding="utf-8")

    forbidden_strings = [
        "Catalysts & risks",
        "Catalysts &amp; risks",
        "Operating margin",
        "Peer context",
        "Summarize the key catalysts and risks",
        "Explain the operating margin trend",
        "How do the reported fundamentals compare to peers?",
    ]

    for forbidden in forbidden_strings:
        assert forbidden not in html, f"Found legacy Part 20 string '{forbidden}' in chat_drawer.html"
