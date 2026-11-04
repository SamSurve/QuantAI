"""Tests for AgentOS client error normalization and friendly error messages.

Ported from original test suite E:\\Quant-AI\\tests\\test_agentos_client_errors.ts
with 100% assertion parity.
"""

from __future__ import annotations

import pytest
from api.web.chat import friendly_agent_error


PROVIDER_MESSAGE = (
    "AI analysis is temporarily unavailable. Please wait a few minutes and try again; "
    "the dashboard is ready for your next request."
)


def test_upstream_provider_500_error():
    """Verify HTTP 500 status returns standardized temporarily unavailable message."""
    result = friendly_agent_error("upstream provider stack trace", 500)
    assert result == "The Research Desk is temporarily unavailable. Please try again shortly."


def test_unauthorized_401_error():
    """Verify HTTP 401 status returns endpoint configuration guidance."""
    result = friendly_agent_error("unauthorized", 401)
    assert result == "The Research Desk is unavailable for this session. Please check the configured endpoint."


def test_rate_limited_429_error():
    """Verify HTTP 429 status returns friendly provider message."""
    result = friendly_agent_error("quota exceeded", 429)
    assert result == PROVIDER_MESSAGE


def test_temporarily_unavailable_in_message_200():
    """Verify rate limit / availability phrases in body map to provider message regardless of status."""
    result = friendly_agent_error("AI analysis is temporarily unavailable", 200)
    assert result == PROVIDER_MESSAGE


def test_custom_conflict_message_409():
    """Verify specific error messages like ambiguous matches are preserved."""
    result = friendly_agent_error("Multiple companies match this query.", 409)
    assert result == "Multiple companies match this query."


def test_rate_limit_patterns():
    """Verify regex patterns for quota, rate limit, and overloaded service."""
    assert friendly_agent_error("rate limit exceeded", 200) == PROVIDER_MESSAGE
    assert friendly_agent_error("Service unavailable due to high load", 200) == PROVIDER_MESSAGE
    assert friendly_agent_error("Groq system overloaded", 503) == PROVIDER_MESSAGE
