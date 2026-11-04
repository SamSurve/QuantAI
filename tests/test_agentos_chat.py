"""Tests for AgentOS chat render endpoint, 64 KB size limit, rate limit, and security."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.web.chat import render_rate_limiter


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset the render rate limiter state before each test."""
    render_rate_limiter.reset()


def test_render_chat_markdown_success():
    """Verify POST /api/chat/render returns sanitized HTML with math and markdown support."""
    client = TestClient(app)
    payload = {
        "text": "# Summary\n\nProfit margin formula: $\\frac{P}{R}$ and **bold** text."
    }
    response = client.post("/api/chat/render", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "html" in data
    assert "<h1>Summary</h1>" in data["html"]
    assert "<strong>bold</strong>" in data["html"]
    assert "<math" in data["html"]


def test_render_chat_markdown_sanitization():
    """Verify script tags, event handlers, and javascript URLs are sanitized."""
    client = TestClient(app)
    payload = {
        "text": "Attack: <script>alert(1)</script> <img src=x onerror=alert(1)> [Click](javascript:alert(1))"
    }
    response = client.post("/api/chat/render", json=payload)
    assert response.status_code == 200
    html = response.json()["html"]
    assert "<script>" not in html.lower()
    assert "</script>" not in html.lower()
    assert "<img" not in html.lower()
    assert 'href="javascript:' not in html.lower()


def test_render_chat_size_limit_64kb():
    """Verify request exceeding 64 KB is rejected with HTTP 413 Payload Too Large."""
    client = TestClient(app)
    # 65 KB payload
    large_text = "A" * (65 * 1024)
    response = client.post("/api/chat/render", json={"text": large_text})
    assert response.status_code == 413
    assert "exceeds" in response.json()["detail"].lower()


def test_render_chat_rate_limiting():
    """Verify exceeding rate limit returns HTTP 429 Too Many Requests."""
    client = TestClient(app)
    # Rate limit allows 60 renders per minute per client
    payload = {"text": "Simple test"}
    for _ in range(60):
        res = client.post("/api/chat/render", json=payload)
        assert res.status_code == 200

    # 61st request triggers 429
    res = client.post("/api/chat/render", json=payload)
    assert res.status_code == 429
    assert "rate limit" in res.json()["detail"].lower()
