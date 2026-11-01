"""Shared pytest configuration, fixtures, and test hooks."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import api.index as index_module
from api.research_schemas import CompanyIdentity, IdentifierConfidence


@pytest.fixture
def sample_company() -> CompanyIdentity:
    """Standard sample company identity fixture."""
    return CompanyIdentity(
        symbol="AAPL",
        name="Apple Inc.",
        exchange="NMS",
        sector="Technology",
        identifier_confidence=IdentifierConfidence.HIGH,
    )


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """TestClient fixture for the canonical FastAPI application."""
    with TestClient(index_module.app) as client:
        yield client


@pytest.fixture
def clean_env() -> Generator[dict[str, str], None, None]:
    """Clean environment fixture without provider credentials."""
    empty_env = {
        "GROQ_API_KEY_PRIMARY": "",
        "GROQ_API_KEY_SECONDARY": "",
        "OPENROUTER_API_KEY": "",
    }
    with patch.dict(os.environ, empty_env, clear=False):
        yield empty_env
