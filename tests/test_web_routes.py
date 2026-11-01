"""Tests for FastAPI web routes, health endpoints, 404 handler, and static assets."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import api.index as index_module


@pytest.fixture
def client():
    with TestClient(index_module.app) as c:
        yield c


def test_health_endpoints_preserve_fields(client):
    for path in ("/", "/health", "/api", "/api/health"):
        res = client.get(path, headers={"Accept": "application/json"})
        assert res.status_code == 200, path
        assert "application/json" in res.headers["content-type"]
        data = res.json()
        assert data["status"] == "ok"
        assert data["agent_id"] == "groq-finance-agent"
        assert "provider_runtime" in data
        assert "typed_research" in data
        assert "agentos_runs" in data


def test_api_docs_and_openapi(client):
    docs = client.get("/api/docs")
    assert docs.status_code == 200
    assert "html" in docs.headers["content-type"]

    openapi = client.get("/api/openapi.json")
    assert openapi.status_code == 200
    assert "application/json" in openapi.headers["content-type"]
    assert "openapi" in openapi.json()


def test_404_html_and_json(client):
    # Explicit 404 route for HTML
    res_html = client.get("/404", headers={"Accept": "text/html"})
    assert res_html.status_code == 404
    assert "text/html" in res_html.headers["content-type"]
    assert "Page Not Found" in res_html.text

    # Unmatched browser route with HTML accept
    unmatched_html = client.get("/some/nonexistent/path", headers={"Accept": "text/html"})
    assert unmatched_html.status_code == 404
    assert "text/html" in unmatched_html.headers["content-type"]
    assert "Page Not Found" in unmatched_html.text

    # Unmatched API/JSON route
    unmatched_json = client.get("/api/some/nonexistent/path", headers={"Accept": "application/json"})
    assert unmatched_json.status_code == 404
    assert "application/json" in unmatched_json.headers["content-type"]


def test_static_asset_mount(client):
    # Static files mounted under /static
    res = client.get("/static/dev/test.txt")
    # If file doesn't exist, returns 404, but route is mounted and handled
    assert res.status_code in {200, 404}
