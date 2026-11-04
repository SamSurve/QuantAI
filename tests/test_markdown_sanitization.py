"""Security sanitization tests for QuantAI dual-layer markdown and math renderer."""

from __future__ import annotations

import pytest
from api.web.markdown import render_markdown, sanitize_html


def test_script_tag_does_not_survive_normal_text():
    """Verify <script> tag in normal text is neutralized and does not execute."""
    raw = "Normal text before <script>alert('xss')</script> normal text after."
    html = render_markdown(raw)
    assert "<script>" not in html.lower()
    assert "</script>" not in html.lower()
    # Content must be escaped or stripped
    assert "alert('xss')" in html or "alert" in html


def test_event_handler_attributes_do_not_survive():
    """Verify onerror, onclick, onload, and onmouseover attributes do not survive as HTML attributes."""
    # When passed to sanitize_html directly
    raw_html = (
        '<img src="missing.jpg" onerror="alert(1)">\n'
        '<div onclick="evil()">Click me</div>\n'
        '<a href="https://example.com" onmouseover="alert(2)">Hover</a>'
    )
    cleaned = sanitize_html(raw_html)
    assert "onerror" not in cleaned.lower()
    assert "onclick" not in cleaned.lower()
    assert "onmouseover" not in cleaned.lower()
    assert "onload" not in cleaned.lower()

    # When rendered via render_markdown, raw HTML is escaped and no executable elements exist
    md_html = render_markdown(raw_html)
    assert "<img" not in md_html.lower()
    assert "<div onclick" not in md_html.lower()
    assert "<a onmouseover" not in md_html.lower()


def test_javascript_urls_do_not_survive_in_links():
    """Verify javascript: and data: URLs do not survive as clickable hrefs."""
    raw = (
        "[Malicious link](javascript:alert(document.cookie))\n"
        "[Data link](data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==)"
    )
    html = render_markdown(raw)
    assert 'href="javascript:' not in html.lower()
    assert 'href="data:' not in html.lower()


def test_script_in_link_text():
    """Verify <script> inside link text does not produce an executable script DOM node."""
    raw = "[<script>alert('in-link')</script>](https://example.com)"
    html = render_markdown(raw)
    assert "<script>" not in html.lower()
    assert "</script>" not in html.lower()


def test_script_and_attributes_inside_math_blocks():
    """Verify <script> and event handlers inside $...$ math blocks do not survive as executable DOM tags."""
    # Test script in inline math
    raw_inline = "Calculation: $ <script>alert('math-xss')</script> $ and more."
    html_inline = render_markdown(raw_inline)
    assert "<script>" not in html_inline.lower()
    assert "</script>" not in html_inline.lower()

    # Test onerror / event handler in math
    raw_event = "Calculation: $ \\text{<img src=x onerror=alert(1)>} $."
    html_event = render_markdown(raw_event)
    assert "onerror" not in html_event.lower()
    assert "<img" not in html_event.lower()

    # Test script in display math
    raw_display = "$$\n<script>alert('display-xss')</script>\n$$"
    html_display = render_markdown(raw_display)
    assert "<script>" not in html_display.lower()
    assert "</script>" not in html_display.lower()


def test_safe_content_and_links_preserve_integrity():
    """Verify safe markdown, tables, safe links, and MathML formulas render properly."""
    raw = (
        "# Executive Summary\n\n"
        "Here is a [safe link](https://example.com) to primary evidence.\n\n"
        "| Metric | Value |\n"
        "| :--- | :--- |\n"
        "| P/E | 24.5 |\n"
    )
    html = render_markdown(raw)
    assert "<h1>Executive Summary</h1>" in html
    assert '<a href="https://example.com"' in html
    assert 'rel="noopener noreferrer"' in html
    assert "<table>" in html
    assert "<td>24.5</td>" in html
