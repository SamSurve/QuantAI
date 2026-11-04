"""Dual-layer server-side Markdown and pure-python LaTeX/MathML renderer.

Layer 1: markdown-it-py with html=False (raw HTML escaped) + dollarmath + Pygments.
Layer 2: nh3 with strict allowlist covering standard markup and MathML tags.
"""

from __future__ import annotations

import html
import re
from typing import Any

import nh3
from latex2mathml.converter import convert as latex_to_mathml
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

# Allowed tags for Layer 2 nh3 sanitizer
ALLOWED_TAGS: set[str] = {
    # Structural and typographic
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "s",
    "del",
    "blockquote",
    "code",
    "pre",
    "ul",
    "ol",
    "li",
    "hr",
    "br",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "a",
    "span",
    "div",
    # MathML elements
    "math",
    "mrow",
    "mi",
    "mo",
    "mn",
    "msup",
    "msub",
    "msubsup",
    "mfrac",
    "msqrt",
    "mroot",
    "munder",
    "mover",
    "munderover",
    "mtable",
    "mtr",
    "mtd",
    "mtext",
    "mspace",
    "semantics",
    "annotation",
    "mstyle",
}

# Allowed attributes for Layer 2 nh3 sanitizer
ALLOWED_ATTRIBUTES: dict[str, set[str]] = {
    "a": {"href", "title", "target"},
    "code": {"class"},
    "pre": {"class"},
    "span": {"class"},
    "div": {"class"},
    "math": {"display", "xmlns"},
    "mstyle": {"displaystyle"},
    "*": {"class"},
}

ALLOWED_URL_SCHEMES: set[str] = {"http", "https", "mailto"}


def _highlight_code(code: str, name: str, attrs: str) -> str:
    """Highlight code fences using Pygments when a valid lexer name is given."""
    if name:
        try:
            lexer = get_lexer_by_name(name.strip().lower())
            return highlight(code, lexer, HtmlFormatter(nowrap=True))
        except Exception:
            pass
    return html.escape(code)


def _math_renderer(content: str, options: dict[str, Any]) -> str:
    """Convert LaTeX math to MathML using latex2mathml; fallback safely on syntax error."""
    display = "block" if options.get("display_mode") else "inline"
    try:
        return latex_to_mathml(content, display=display)
    except Exception:
        return f'<span class="math-fallback">{html.escape(content)}</span>'


def _build_markdown_parser() -> MarkdownIt:
    """Build and configure the Layer 1 markdown-it-py parser."""
    md = MarkdownIt("commonmark", {
        "html": False,  # Layer 1: disable raw HTML (escapes all raw tags)
        "xhtmlOut": False,
        "breaks": False,
        "langPrefix": "language-",
        "highlight": _highlight_code,
    })
    md.enable("table")
    md.enable("strikethrough")
    dollarmath_plugin(md, renderer=_math_renderer)
    return md


_MD_PARSER = _build_markdown_parser()


def sanitize_html(raw_html: str) -> str:
    """Layer 2 sanitizer: run nh3 with strict allowlist and automatic rel='noopener noreferrer'."""
    if not raw_html:
        return ""
    return nh3.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes=ALLOWED_URL_SCHEMES,
        link_rel="noopener noreferrer",
    )


def render_markdown(markdown_text: str | None) -> str:
    """Render markdown to secure, sanitized HTML using Layer 1 (parser) + Layer 2 (nh3)."""
    if not markdown_text:
        return ""
    # Layer 1: markdown-it with html=False and math/code highlighting
    intermediate_html = _MD_PARSER.render(markdown_text)
    # Layer 2: nh3 sanitization
    return sanitize_html(intermediate_html)


def extract_editorial_lead(markdown_text: str | None) -> str | None:
    """Extract first meaningful paragraph line for the editorial pull quote."""
    if not markdown_text:
        return None
    for line in markdown_text.splitlines():
        cleaned = re.sub(r"^#+\s*", "", line)
        cleaned = re.sub(r"^[-*]\s*", "", cleaned).strip()
        if (
            len(cleaned) > 45
            and not cleaned.startswith("|")
            and not cleaned.startswith("```")
            and not cleaned.startswith("$")
        ):
            return cleaned[:180]
    return None
