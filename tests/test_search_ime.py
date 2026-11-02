"""Tests for IME composition and search client-side script behavior.

Verifies static/js/search.js contains compositionstart/end guards,
Enter-key suppression during IME composition, and query trimming.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCH_JS = ROOT / "static" / "js" / "search.js"


def test_search_js_exists():
    """Verify search.js exists in static/js/."""
    assert SEARCH_JS.exists(), "static/js/search.js must exist"


def test_search_js_ime_guards():
    """Verify search.js guards against premature submission during IME composition."""
    content = SEARCH_JS.read_text(encoding="utf-8")

    assert "compositionstart" in content
    assert "compositionend" in content
    assert "isComposing" in content or "composing" in content
    assert "keydown" in content
    assert "Enter" in content


def test_search_js_quick_search_and_trim():
    """Verify search.js binds quick-search shortcuts and trims input."""
    content = SEARCH_JS.read_text(encoding="utf-8")

    assert "data-quick-search" in content or "quick-search" in content
    assert "trim" in content
