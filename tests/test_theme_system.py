"""Tests for the persistent three-mode theme system (Light/Dark/System).

Verifies template rendering, anti-flicker script in base.html,
segmented theme toggle markup, and JavaScript client behavior contract.
"""

from __future__ import annotations

import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"
THEME_JS = ROOT / "static" / "js" / "theme.js"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def test_theme_toggle_template_structure():
    """Verify theme toggle partial has segmented control with Light, Dark, System."""
    template = env.get_template("partials/theme_toggle.html")
    rendered = template.render()

    assert 'role="group"' in rendered
    assert 'aria-label="Theme"' in rendered
    assert "Light" in rendered
    assert "Dark" in rendered
    assert "System" in rendered
    assert 'class="segs' in rendered
    assert 'data-theme-value="light"' in rendered
    assert 'data-theme-value="dark"' in rendered
    assert 'data-theme-value="system"' in rendered


def test_base_template_anti_flicker_script():
    """Verify base.html contains the inline anti-flicker script executing in head."""
    base_html = (TEMPLATES_DIR / "base.html").read_text(encoding="utf-8")
    assert "quantai-theme" in base_html
    assert "prefers-color-scheme: dark" in base_html
    assert "document.documentElement.dataset.theme" in base_html
    assert "document.documentElement.classList.toggle" in base_html
    assert "document.documentElement.style.colorScheme" in base_html


def test_theme_js_exists_and_contract():
    """Verify theme.js implements pure client-side theme switching without network requests."""
    assert THEME_JS.exists(), "static/js/theme.js must exist"
    content = THEME_JS.read_text(encoding="utf-8")

    # LocalStorage key
    assert "quantai-theme" in content

    # System media query
    assert "prefers-color-scheme: dark" in content

    # Theme options handled
    assert '"light"' in content or "'light'" in content
    assert '"dark"' in content or "'dark'" in content
    assert '"system"' in content or "'system'" in content

    # DOM updates
    assert "dataset.theme" in content
    assert "classList.toggle" in content or "classList.add" in content
    assert "colorScheme" in content

    # Zero server requests
    assert "fetch(" not in content
    assert "XMLHttpRequest" not in content
    assert "htmx" not in content.lower()
