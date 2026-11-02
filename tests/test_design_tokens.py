"""Tests for Apple-style design tokens and Jinja2 UI macros.

Verifies CSS variables match Main.dc.html extracted tokens for light and dark modes,
and verifies macros render with proper styling classes.
"""

from __future__ import annotations

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"
CSS_INPUT = ROOT / "static" / "css" / "input.css"
CSS_APP = ROOT / "static" / "css" / "app.css"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def test_input_css_contains_light_tokens():
    """Verify input.css declares extracted light-theme tokens."""
    assert CSS_INPUT.exists(), "input.css must exist"
    content = CSS_INPUT.read_text(encoding="utf-8")
    assert "--bg: #f5f5f7" in content
    assert "--card: #fff" in content or "--card: #ffffff" in content
    assert "--fill: #f0f0f3" in content
    assert "--text: #1d1d1f" in content
    assert "--muted: #6e6e73" in content
    assert "--link: #0066cc" in content
    assert "--up: #1a9c3c" in content


def test_input_css_contains_dark_tokens():
    """Verify input.css declares extracted dark-theme tokens."""
    content = CSS_INPUT.read_text(encoding="utf-8")
    assert 'data-theme="dark"' in content or ".dark" in content
    assert "--bg: #000" in content or "--bg: #000000" in content
    assert "--card: #1c1c1e" in content
    assert "--fill: #2c2c2e" in content
    assert "--text: #f5f5f7" in content
    assert "--muted: #a1a1a6" in content
    assert "--link: #2997ff" in content
    assert "--up: #30d158" in content


def test_brand_macro():
    """Verify brand macro renders QuantAI logo and title."""
    template = env.from_string("{% import 'macros/brand.html' as brand %}{{ brand.render() }}")
    rendered = template.render()
    assert "QuantAI" in rendered
    assert "<svg" in rendered


def test_metric_card_macro():
    """Verify metric_card macro renders label and value with design token classes."""
    template = env.from_string(
        "{% import 'macros/metric_card.html' as mc %}{{ mc.render('MARKET CAP', '$3.42T') }}"
    )
    rendered = template.render()
    assert "MARKET CAP" in rendered
    assert "$3.42T" in rendered
    assert "eyebrow" in rendered


def test_icon_macro():
    """Verify icon macro renders SVG icons."""
    template = env.from_string(
        "{% import 'macros/icon.html' as icon %}{{ icon.render('search') }}"
    )
    rendered = template.render()
    assert "<svg" in rendered


def test_dialog_macro():
    """Verify dialog macro renders dialog container."""
    template = env.from_string(
        "{% import 'macros/dialog.html' as dlg %}{{ dlg.render('test-dialog', 'Dialog Title', 'Body content') }}"
    )
    rendered = template.render()
    assert "test-dialog" in rendered
    assert "Dialog Title" in rendered
    assert "Body content" in rendered
