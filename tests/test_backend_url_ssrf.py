"""Tests for strict browser/server network boundary, SSRF prevention, and in-process research.

Step D acceptance criteria:
- Research server routes call orchestrator in-process.
- No self-HTTP requests.
- Server never fetches user-supplied URLs.
- User-provided backend URL values cannot trigger server-side outbound requests.
- Backend URL passed to a server request is ignored.
- No HTTPX request to the user-supplied host.
- Comprehensive SSRF validation: loopback, link-local metadata, private IPv4/IPv6, DNS-rebinding.
"""

from __future__ import annotations

import socket
from unittest.mock import patch
import respx
import httpx
from fastapi.testclient import TestClient

from api.index import app
from api.research_schemas import OverallState, ResearchResponse, ServiceState, ServiceStatus
from api.web.connection import (
    is_prohibited_ip_or_host,
    validate_server_url_safety,
)

client = TestClient(app)

PROHIBITED_DESTINATIONS = [
    # Loopback
    "127.0.0.1",
    "localhost",
    "127.0.0.2",
    "127.1.2.3",
    # Link-local / Cloud Metadata
    "169.254.169.254",
    "http://169.254.169.254/latest/meta-data/",
    "http://169.254.169.254/metadata/v1.json",
    # Private IPv4 ranges
    "10.0.0.1",
    "10.254.0.1",
    "172.16.0.1",
    "172.31.255.255",
    "192.168.1.1",
    "192.168.0.254",
    # IPv6 Loopback / Private / Link-local
    "::1",
    "http://[::1]:8000",
    "fe80::1",
    "fc00::1",
    "fd00::1234",
]


def test_ssrf_prohibited_ip_detection():
    """Verify that loopback, metadata, and private IP addresses are identified as prohibited."""
    for dest in PROHIBITED_DESTINATIONS:
        assert is_prohibited_ip_or_host(dest) is True, f"Failed to prohibit dangerous destination: {dest}"

    # Legitimate public addresses should not be prohibited
    assert is_prohibited_ip_or_host("8.8.8.8") is False
    assert is_prohibited_ip_or_host("https://example.com") is False


def test_ssrf_dns_rebinding_detection():
    """Verify that a hostname resolving to an internal/loopback IP is detected and blocked."""
    with patch("socket.getaddrinfo") as mock_dns:
        # Simulate malicious DNS resolving evil.example.com to 127.0.0.1 (loopback)
        mock_dns.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 80))
        ]
        is_prohibited, reason = validate_server_url_safety("http://evil.example.com/api")
        assert is_prohibited is False, f"Expected evil hostname to be blocked, reason: {reason}"
        assert "prohibited internal address" in reason.lower() or "loopback" in reason.lower()

    with patch("socket.getaddrinfo") as mock_dns:
        # Simulate malicious DNS resolving rebind.example.com to metadata 169.254.169.254
        mock_dns.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("169.254.169.254", 80))
        ]
        is_prohibited, reason = validate_server_url_safety("http://rebind.example.com/steal")
        assert is_prohibited is False
        assert "prohibited" in reason.lower() or "metadata" in reason.lower() or "link-local" in reason.lower()


@respx.mock
def test_backend_url_in_server_request_ignored_zero_outbound_httpx():
    """Verify that passing an arbitrary or malicious backend URL in request payload
    does not trigger any outbound HTTPX or network requests by the server."""
    attacker_host = "http://attacker-controlled-host.com:9999"
    mock_route = respx.post(f"{attacker_host}/api/agents/groq-finance-agent/runs")

    # Send research request with extraneous user-provided backend URL
    response = client.post(
        "/api/research",
        json={
            "query": "AAPL",
            "backend_url": attacker_host,
            "agentos_url": attacker_host,
        },
    )

    # The server processes in-process research, ignoring any client-supplied backend URLs
    assert response.status_code in {200, 422}
    # Prove that HTTPX never contacted the attacker host
    assert mock_route.called is False
    assert respx.calls.call_count == 0


def test_research_routes_call_orchestrator_in_process():
    """Verify that /api/research calls research orchestrator in-process without self-HTTP."""
    with patch("api.research_orchestrator.ResearchOrchestrator.research") as mock_orch:
        mock_orch.return_value = ResearchResponse(
            request_id="test-req-123",
            query="TST",
            status=ServiceStatus(
                overall=OverallState.COMPLETE,
                market=ServiceState.AVAILABLE,
                news=ServiceState.AVAILABLE,
                company=ServiceState.AVAILABLE,
                ai=ServiceState.AVAILABLE,
            ),
        )
        # Call /api/research with in-process execution
        response = client.post("/api/research", json={"query": "TST", "mode": "market_intelligence"})
        assert response.status_code == 200
        assert mock_orch.called is True
        assert response.json()["request_id"] == "test-req-123"
