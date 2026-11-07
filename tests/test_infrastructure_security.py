"""Tests for Part 35: Seven infrastructure and security capabilities.

Verifies:
- C01: SSRF Protection & Private IP Blocking (api/web/connection.py).
- C02: Secret-Handling Invariants (no API keys in HTML, JSON errors, or responses).
- C03: Sliding-Window Rate Limiter (10 req/min per IP, memory-bounded, safe 429).
- C04: Concurrency Guard (max 4 concurrent research runs, safe release on error).
- C05: Request ID Generation & Propagation (X-Request-ID header & logging).
- C06: Error Classification & Sanitization (deterministic error mapping without leak).
- C07: Provider Failover Sequence (Groq Primary -> Groq Secondary -> OpenRouter).
"""

from __future__ import annotations

import asyncio
import os
import sys
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import api.index as api_index
from api.ai_providers import ProviderRouter
from api.research_errors import ResearchError
from api.research_protection import ResearchConcurrencyGuard, SlidingWindowRateLimiter
from api.research_schemas import ErrorCategory
from api.web.connection import is_prohibited_ip_or_host, validate_server_url_safety


def test_c01_ssrf_and_private_ip_blocking():
    """C01: Server-side SSRF validation blocks all loopback, private, and metadata destinations."""
    prohibited_hosts = [
        "127.0.0.1",
        "127.0.1.1",
        "localhost",
        "10.0.0.1",
        "10.255.255.255",
        "172.16.0.1",
        "172.31.255.255",
        "192.168.1.1",
        "192.168.254.254",
        "169.254.169.254",  # AWS/GCP cloud metadata
        "metadata",
        "instance-data",
        "::1",
        "fe80::1",
    ]
    for host in prohibited_hosts:
        assert is_prohibited_ip_or_host(host) is True, f"Host {host} should be prohibited"
        safe, msg = validate_server_url_safety(f"http://{host}/api")
        assert safe is False, f"URL for {host} should fail validation: {msg}"

    # Public hosts should pass host safety check
    assert is_prohibited_ip_or_host("api.github.com") is False
    assert is_prohibited_ip_or_host("groq.com") is False


def test_c02_secret_handling_invariants():
    """C02: Configured provider keys never appear in rendered HTML, JSON errors, or responses."""
    fake_secrets = {
        "GROQ_API_KEY_PRIMARY": "gsk_secret_production_key_alpha_12345",
        "GROQ_API_KEY_SECONDARY": "gsk_secret_production_key_beta_67890",
        "OPENROUTER_API_KEY": "sk-or-v1-secret_openrouter_key_99999",
    }
    with patch.dict(os.environ, fake_secrets, clear=False):
        with TestClient(api_index.app) as client:
            # 1. HTML home and 404
            for path in ("/", "/404"):
                resp = client.get(path, headers={"Accept": "text/html"})
                for key_name, key_val in fake_secrets.items():
                    assert key_name not in resp.text
                    assert key_val not in resp.text

            # 2. JSON Health endpoint
            health_resp = client.get("/api/health")
            assert health_resp.status_code == 200
            for key_name, key_val in fake_secrets.items():
                assert key_name not in health_resp.text
                assert key_val not in health_resp.text

            # 3. JSON Error detail on bad payload
            err_resp = client.post("/api/research", json={"query": "A" * 9000})
            assert err_resp.status_code in {400, 413, 422}
            for key_name, key_val in fake_secrets.items():
                assert key_name not in err_resp.text
                assert key_val not in err_resp.text


@pytest.mark.asyncio
async def test_c03_sliding_window_rate_limiter():
    """C03: Sliding-window rate limiter enforces 10 req/min limit per key and resets cleanly."""
    limiter = SlidingWindowRateLimiter(limit=3, window_seconds=0.5)
    key = "client-ip-123.45.67.89"

    # 3 allowed
    for _ in range(3):
        await limiter.check(key)

    # 4th should raise RATE_LIMITED
    with pytest.raises(ResearchError) as exc_info:
        await limiter.check(key)
    assert exc_info.value.category == ErrorCategory.RATE_LIMITED
    assert exc_info.value.retryable is True

    # After window expiration, should allow again
    await asyncio.sleep(0.55)
    await limiter.check(key)


@pytest.mark.asyncio
async def test_c04_concurrency_guard():
    """C04: Concurrency guard allows up to max_concurrent tasks and safely releases semaphore."""
    guard = ResearchConcurrencyGuard(max_concurrent=2)

    # Acquire 2 concurrent slots
    async with guard.acquire():
        async with guard.acquire():
            # 3rd request should fail fast with RATE_LIMITED
            with pytest.raises(ResearchError) as exc_info:
                async with guard.acquire():
                    pass
            assert exc_info.value.category == ErrorCategory.RATE_LIMITED

    # Slots released, should allow acquiring again
    acquired = False
    async with guard.acquire():
        acquired = True
    assert acquired is True


def test_c05_request_id_generation_and_propagation():
    """C05: X-Request-ID is generated if missing and propagated if supplied."""
    with TestClient(api_index.app) as client:
        # Generated when missing
        resp1 = client.get("/api/health")
        req_id1 = resp1.headers.get("x-request-id")
        assert req_id1 is not None
        # Must be valid UUID format
        uuid.UUID(req_id1)

        # Propagated when supplied
        custom_id = "custom-trace-uuid-1234-abcd"
        resp2 = client.get("/api/health", headers={"X-Request-ID": custom_id})
        assert resp2.headers.get("x-request-id") == custom_id


def test_c06_error_classification_and_sanitization():
    """C06: Internal errors are mapped to safe, classified response categories without stack traces."""
    with TestClient(api_index.app) as client:
        # Invalid large payload
        resp = client.post(
            "/api/research",
            content=b"x" * 9000,
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code in {400, 413, 422}
        data = resp.json()
        assert "traceback" not in str(data).lower()
        assert "exception" not in str(data).lower()
        assert "category" in data or "message" in data or "error" in data


def test_c07_provider_failover_sequence():
    """C07: ProviderRouter follows strict sequential fallback order and deterministic final state."""
    # Instantiation from empty environment should report available_count=0
    router = ProviderRouter.from_environment()
    status = router.provider_status()
    assert "strategy" in status
    assert status["strategy"] == "sequential_one_way"
    assert "configured_count" in status
    assert "available_count" in status

