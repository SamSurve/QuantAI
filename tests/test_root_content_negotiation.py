"""Tests for root / content negotiation between JSON health and HTML workspace."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import api.index as index_module


@pytest.fixture
def client():
    with TestClient(index_module.app) as c:
        yield c


def test_missing_accept_returns_json_health(client):
    response = client.get("/", headers={})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    data = response.json()
    assert data["status"] == "ok"
    assert data["agent_id"] == "groq-finance-agent"


def test_wildcard_accept_returns_json_health(client):
    response = client.get("/", headers={"Accept": "*/*"})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json()["status"] == "ok"


def test_application_json_accept_returns_json_health(client):
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json()["status"] == "ok"


def test_explicit_text_html_returns_html_workspace(client):
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<!doctype html>" in response.text.lower()
    assert "QuantAI" in response.text


def test_equal_html_json_preference_returns_json_health(client):
    response = client.get("/", headers={"Accept": "text/html,application/json"})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json()["status"] == "ok"


def test_higher_html_quality_returns_html_workspace(client):
    response = client.get("/", headers={"Accept": "text/html;q=0.9,application/json;q=0.8"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<!doctype html>" in response.text.lower()


def test_higher_json_quality_returns_json_health(client):
    response = client.get("/", headers={"Accept": "application/json;q=1,text/html;q=0.9"})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json()["status"] == "ok"


def test_default_json_with_lower_html_quality_returns_json_health(client):
    response = client.get("/", headers={"Accept": "application/json,text/html;q=0.5"})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json()["status"] == "ok"


def test_html_quality_zero_returns_json_health(client):
    response = client.get("/", headers={"Accept": "text/html;q=0"})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json()["status"] == "ok"
