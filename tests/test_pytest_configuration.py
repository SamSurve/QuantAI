"""Tests for pytest test infrastructure, fixtures, async execution, and mocking."""

from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
import pytest
import respx

from api.research_schemas import CompanyIdentity


def test_shared_fixtures_availability(sample_company: CompanyIdentity, test_client):
    """Verify shared pytest fixtures from conftest.py."""
    assert sample_company.symbol == "AAPL"
    assert sample_company.name == "Apple Inc."

    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["agent_id"] == "groq-finance-agent"


@pytest.mark.asyncio
async def test_asyncio_support():
    """Verify that asyncio tests run cleanly under pytest-asyncio."""
    await asyncio.sleep(0.01)
    assert True


@respx.mock
def test_respx_http_mocking():
    """Verify that respx HTTP mocking works cleanly."""
    mock_route = respx.get("https://api.quantai.internal/test").mock(
        return_value=httpx.Response(200, json={"status": "mocked"})
    )
    response = httpx.get("https://api.quantai.internal/test")
    assert response.status_code == 200
    assert response.json() == {"status": "mocked"}
    assert mock_route.called


def test_tmp_directory_isolation(tmp_path: Path):
    """Verify that clean temporary test directory fixture works."""
    test_file = tmp_path / "temp.txt"
    test_file.write_text("isolated", encoding="utf-8")
    assert test_file.read_text(encoding="utf-8") == "isolated"
