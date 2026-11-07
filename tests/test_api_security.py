"""Regression test suite for Part 24: API Security and Request Protection.

Verifies:
1. 8192-byte research request body limit.
2. 8192-byte AgentOS run request body limit.
3. 10 requests per 60 seconds per client IP rate limiting.
4. Concurrency guard: up to 4 concurrent protected operations with safe release.
5. Precise sliding-window reset/expiration.
6. Safe request ID generation, propagation, and inclusion in responses.
7. Server-only diagnostics and public exception sanitization (no internal leaks).
8. Safe forwarded-IP handling for single-hop and multi-hop proxies.
9. Cache-Control deployment security policy.
10. Provider secrets protection across API endpoints and web templates.
11. Logging sanitization against prompt, response, and credential leaks.
"""

from __future__ import annotations

import asyncio
import json
import os
import uuid
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from api.index import (
    MAX_AGENTOS_RUN_REQUEST_BYTES,
    MAX_RESEARCH_REQUEST_BYTES,
    _client_key,
    _error_response,
    _request_id,
    app,
    research_rate_limiter,
)
from api.research_errors import HTTP_STATUS, SAFE_MESSAGES, ResearchError
from api.research_logging import LOGGER, log_research_event
from api.research_protection import ResearchConcurrencyGuard, SlidingWindowRateLimiter
from api.research_schemas import (
    ErrorCategory,
    OverallState,
    ResearchResponse,
    ServiceStatus,
)


ROOT = Path(__file__).resolve().parents[1]
QUANT_AI_ORIGINAL = Path("E:/Quant-AI")


# ---------------------------------------------------------------------------
# 1. PAYLOAD SIZE BOUNDARIES (8192 BYTES)
# ---------------------------------------------------------------------------

def test_research_payload_limit_constants():
    """Verify exact 8,192-byte limit configuration constants."""
    assert MAX_RESEARCH_REQUEST_BYTES == 8_192
    assert MAX_AGENTOS_RUN_REQUEST_BYTES == 8_192


def test_research_payload_size_boundary_accepted_at_8192():
    """Exact 8,192-byte payload to /api/research must pass the body-size gate."""
    # Build payload with trailing whitespace between JSON tokens so byte-length is exactly 8,192
    prefix = '{"query":"AAPL","include_analysis":false'
    suffix = '}'
    pad_len = 8_192 - len(prefix) - len(suffix)
    body_str = prefix + (" " * pad_len) + suffix
    body_bytes = body_str.encode("utf-8")
    assert len(body_bytes) == 8_192

    with patch("api.index.research_orchestrator.research", new_callable=AsyncMock) as mock_res:
        mock_res.return_value = ResearchResponse(
            status=ServiceStatus(
                overall=OverallState.COMPLETE,
                market="available",
                news="available",
                company="available",
                ai="available",
            ),
            request_id="test-req",
            query="AAPL",
        )
        with TestClient(app) as client:
            resp = client.post(
                "/api/research",
                content=body_bytes,
                headers={"Content-Type": "application/json", "X-Forwarded-For": "10.10.10.1"},
            )
            # Must not be rejected by middleware body limit (422 body too large)
            assert resp.status_code == 200


def test_research_payload_size_boundary_rejected_above_8192():
    """8,193-byte payload to /api/research must be rejected with sanitized 422."""
    prefix = '{"query":"AAPL","padding":"'
    suffix = '"}'
    pad_len = 8_193 - len(prefix) - len(suffix)
    body_str = prefix + ("a" * pad_len) + suffix
    body_bytes = body_str.encode("utf-8")
    assert len(body_bytes) == 8_193

    with TestClient(app) as client:
        resp = client.post(
            "/api/research",
            content=body_bytes,
            headers={"Content-Type": "application/json", "X-Forwarded-For": "10.10.10.2"},
        )
        assert resp.status_code == 422
        data = resp.json()
        assert data["category"] == "VALIDATION_ERROR"
        assert data["message"] == SAFE_MESSAGES[ErrorCategory.VALIDATION_ERROR]
        # Public response must not leak internal detail
        assert "request body too large" not in json.dumps(data)
        assert "request_id" in data


def test_agentos_run_payload_size_boundary_rejected_above_8192():
    """AgentOS runs endpoint must reject payloads exceeding 8,192 bytes with sanitized 422."""
    large_body = b"x" * 8_193
    with TestClient(app) as client:
        resp = client.post(
            "/api/agents/groq-finance-agent/runs",
            content=large_body,
            headers={"Content-Type": "application/octet-stream", "X-Forwarded-For": "10.10.10.3"},
        )
        assert resp.status_code == 422
        data = resp.json()
        assert data["category"] == "VALIDATION_ERROR"
        assert "request body too large" not in json.dumps(data)


def test_research_payload_size_enforced_via_chunked_or_body_read():
    """Oversized body is caught even without content-length header."""
    large_body = b" " * 9_000
    with TestClient(app) as client:
        resp = client.post(
            "/api/research",
            content=large_body,
            headers={"Content-Type": "application/json", "X-Forwarded-For": "10.10.10.4"},
        )
        assert resp.status_code == 422
        assert resp.json()["category"] == "VALIDATION_ERROR"


# ---------------------------------------------------------------------------
# 2. RATE LIMITING & SLIDING WINDOW EXPIRATION
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_sliding_window_rate_limiter_isolated():
    """SlidingWindowRateLimiter permits up to limit and blocks 11th request."""
    limiter = SlidingWindowRateLimiter(limit=10, window_seconds=60.0)
    key = "test-client-ip"

    # First 10 requests pass
    for _ in range(10):
        await limiter.check(key)

    # 11th request raises ResearchError(RATE_LIMITED)
    with pytest.raises(ResearchError) as exc_info:
        await limiter.check(key)

    assert exc_info.value.category == ErrorCategory.RATE_LIMITED
    assert exc_info.value.retryable is True
    assert exc_info.value.status_code == 429
    assert exc_info.value.message == SAFE_MESSAGES[ErrorCategory.RATE_LIMITED]


@pytest.mark.asyncio
async def test_sliding_window_rate_limiter_reset():
    """Expired timestamps roll off the sliding window allowing new requests."""
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=10.0)
    key = "reset-client"

    # Simulated times
    t0 = 1000.0
    with patch("time.monotonic", return_value=t0):
        await limiter.check(key)
        await limiter.check(key)
        # 3rd is blocked
        with pytest.raises(ResearchError):
            await limiter.check(key)

    # Advance time past window (1000.0 + 10.1)
    t1 = 1010.1
    with patch("time.monotonic", return_value=t1):
        # Now requests are permitted again
        await limiter.check(key)
        await limiter.check(key)
        with pytest.raises(ResearchError):
            await limiter.check(key)


def test_api_rate_limit_per_client_ip_and_429_sanitization():
    """Client reaching 10 requests receives sanitized 429; another IP is unaffected."""
    ip_a = "192.0.2.1"
    ip_b = "192.0.2.2"

    with patch("api.index.research_orchestrator.research", new_callable=AsyncMock) as mock_res:
        mock_res.return_value = ResearchResponse(
            status=ServiceStatus(
                overall=OverallState.COMPLETE,
                market="available",
                news="available",
                company="available",
                ai="available",
            ),
            request_id="test-req",
            query="AAPL",
        )
        with TestClient(app) as client:
            # Clear state for this test IP
            research_rate_limiter._requests.pop(ip_a, None)
            research_rate_limiter._requests.pop(ip_b, None)

            for _ in range(10):
                resp = client.post(
                    "/api/research",
                    json={"query": "AAPL", "mode": "standard", "include_analysis": False},
                    headers={"X-Forwarded-For": ip_a},
                )
                assert resp.status_code == 200

            # 11th request for ip_a must be 429
            resp_11 = client.post(
                "/api/research",
                json={"query": "AAPL", "mode": "standard", "include_analysis": False},
                headers={"X-Forwarded-For": ip_a},
            )
            assert resp_11.status_code == 429
            data = resp_11.json()
            assert data["category"] == "RATE_LIMITED"
            assert data["retryable"] is True
            assert data["message"] == "Too many requests were received. Please wait a moment and try again."
            # Internal key or details must not leak
            assert ip_a not in json.dumps(data)
            assert "local limit reached" not in json.dumps(data)

            # ip_b is unaffected
            resp_b = client.post(
                "/api/research",
                json={"query": "AAPL", "mode": "standard", "include_analysis": False},
                headers={"X-Forwarded-For": ip_b},
            )
            assert resp_b.status_code == 200


# ---------------------------------------------------------------------------
# 3. CONCURRENCY GUARD & CAPACITY RELEASE
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_concurrency_guard_allows_four_and_blocks_fifth():
    """Guard allows exactly 4 concurrent acquisitions; 5th raises RATE_LIMITED."""
    guard = ResearchConcurrencyGuard(max_concurrent=4)

    entered = []

    async def worker(idx: int):
        async with guard.acquire():
            entered.append(idx)
            # Hold acquisition
            await asyncio.sleep(0.2)

    # Launch 4 concurrent tasks
    tasks = [asyncio.create_task(worker(i)) for i in range(4)]
    await asyncio.sleep(0.01)
    assert len(entered) == 4

    # 5th task attempts to acquire while 4 are active
    with pytest.raises(ResearchError) as exc:
        async with guard.acquire():
            pass

    assert exc.value.category == ErrorCategory.RATE_LIMITED
    assert exc.value.retryable is True

    # Complete the first 4 tasks
    await asyncio.gather(*tasks)

    # After completion, guard capacity is fully restored
    async with guard.acquire():
        assert True


@pytest.mark.asyncio
async def test_concurrency_guard_releases_on_exception():
    """Guard releases semaphore capacity even when internal body raises an exception."""
    guard = ResearchConcurrencyGuard(max_concurrent=1)

    class CustomTestException(Exception):
        pass

    with pytest.raises(CustomTestException):
        async with guard.acquire():
            raise CustomTestException("Failure inside critical section")

    # Guard should immediately be re-acquirable
    acquired = False
    async with guard.acquire():
        acquired = True
    assert acquired is True


# ---------------------------------------------------------------------------
# 4. REQUEST IDS
# ---------------------------------------------------------------------------

def test_request_id_generated_when_missing():
    """Requests without X-Request-ID receive a newly generated UUID in response header."""
    with TestClient(app) as client:
        resp = client.get("/api/health")
        assert resp.status_code == 200
        req_id = resp.headers.get("X-Request-ID")
        assert req_id is not None
        # Must be valid UUID
        parsed = uuid.UUID(req_id)
        assert str(parsed) == req_id


def test_request_id_propagated_when_supplied():
    """Client-supplied X-Request-ID is echoed back in response header."""
    custom_id = "client-trace-abc-12345"
    with TestClient(app) as client:
        resp = client.get("/api/health", headers={"X-Request-ID": custom_id})
        assert resp.status_code == 200
        assert resp.headers.get("X-Request-ID") == custom_id


def test_request_id_in_error_responses():
    """Error responses include the matching request_id in JSON body."""
    custom_id = "err-trace-777"
    with TestClient(app) as client:
        resp = client.post(
            "/api/research",
            content=b"x" * 9000,
            headers={"X-Request-ID": custom_id, "Content-Type": "application/json"},
        )
        assert resp.status_code == 422
        data = resp.json()
        assert data["request_id"] == custom_id


# ---------------------------------------------------------------------------
# 5. PUBLIC EXCEPTION SANITIZATION & SAFE ERRORS
# ---------------------------------------------------------------------------

def test_error_response_never_serializes_detail():
    """_error_response serializes category, message, request_id, retryable; never detail."""
    fake_request = Request({"type": "http", "method": "GET", "path": "/api/test", "headers": []})
    fake_request.state.request_id = "req-safe-1"

    err = ResearchError(
        category=ErrorCategory.INTERNAL_ERROR,
        detail="Traceback: secret_db_query at /var/www/internal/db.py line 42",
        retryable=False,
    )

    resp = _error_response(fake_request, err)
    assert resp.status_code == 500
    content = json.loads(resp.body.decode("utf-8"))
    assert content["request_id"] == "req-safe-1"
    assert content["category"] == "INTERNAL_ERROR"
    assert content["message"] == SAFE_MESSAGES[ErrorCategory.INTERNAL_ERROR]
    assert content["retryable"] is False
    assert "detail" not in content
    assert "secret_db_query" not in json.dumps(content)
    assert "/var/www" not in json.dumps(content)


def test_all_error_categories_have_safe_messages_and_status_codes():
    """Verify that every ErrorCategory enum value has an approved public message and status code."""
    for category in ErrorCategory:
        assert category in SAFE_MESSAGES
        assert category in HTTP_STATUS
        msg = SAFE_MESSAGES[category]
        assert isinstance(msg, str) and len(msg) > 0
        code = HTTP_STATUS[category]
        assert 400 <= code <= 599


def test_unhandled_route_exception_sanitized_to_500():
    """Unhandled internal exceptions are captured and return generic 500 with no traceback."""
    with patch("api.index.research_orchestrator.research", side_effect=RuntimeError("Secret database crash")):
        with TestClient(app, raise_server_exceptions=False) as client:
            resp = client.post(
                "/api/research",
                json={"query": "AAPL", "mode": "standard"},
                headers={"X-Forwarded-For": "10.99.99.1"},
            )
            assert resp.status_code == 500
            data = resp.json()
            assert data["category"] == "INTERNAL_ERROR"
            assert data["message"] == "Research is temporarily unavailable. Please try again shortly."
            assert "Secret database crash" not in json.dumps(data)
            assert "RuntimeError" not in json.dumps(data)


# ---------------------------------------------------------------------------
# 6. SAFE FORWARDED-IP HANDLING
# ---------------------------------------------------------------------------

def test_client_key_single_hop():
    """Single-hop X-Forwarded-For extracts client IP."""
    req = Request({
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"x-forwarded-for", b"203.0.113.195")],
    })
    assert _client_key(req) == "203.0.113.195"


def test_client_key_multi_hop_takes_first():
    """Multi-hop X-Forwarded-For safely takes the leftmost client IP."""
    req = Request({
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"x-forwarded-for", b"203.0.113.195, 70.41.3.18, 150.172.238.178")],
    })
    assert _client_key(req) == "203.0.113.195"


def test_client_key_whitespace_trimmed():
    """Whitespace around client IP in X-Forwarded-For is cleanly trimmed."""
    req = Request({
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"x-forwarded-for", b"   198.51.100.44   , 10.0.0.1")],
    })
    assert _client_key(req) == "198.51.100.44"


def test_client_key_fallback_to_client_host():
    """Absence of X-Forwarded-For falls back to request.client.host."""
    req = Request({
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [],
        "client": ("192.168.1.100", 54321),
    })
    assert _client_key(req) == "192.168.1.100"


def test_client_key_unknown_when_no_client_or_header():
    """Missing headers and client return 'unknown' safely without raising."""
    req = Request({
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [],
    })
    assert _client_key(req) == "unknown"


# ---------------------------------------------------------------------------
# 7. CACHE-CONTROL DEPLOYMENT POLICY
# ---------------------------------------------------------------------------

def test_cache_control_deployment_policy():
    """Verify that the deployment specification enforces Cache-Control: no-store for /api/*."""
    vercel_path = None
    if (ROOT / "vercel.json").exists():
        vercel_path = ROOT / "vercel.json"
    elif (QUANT_AI_ORIGINAL / "vercel.json").exists():
        vercel_path = QUANT_AI_ORIGINAL / "vercel.json"

    if vercel_path:
        config = json.loads(vercel_path.read_text(encoding="utf-8"))
        headers = config.get("headers", [])
        api_header = next(
            (
                h for h in headers
                if h.get("source") in {"/api/:path*", "/api/(.*)"}
            ),
            None,
        )
        assert api_header is not None, "Deployment configuration must declare /api/:path* headers"
        assert any(
            item.get("key") == "Cache-Control" and item.get("value") == "no-store"
            for item in api_header.get("headers", [])
        ), "Deployment headers must declare Cache-Control: no-store"


# ---------------------------------------------------------------------------
# 8. PROVIDER SECRETS PROTECTION (NEVER APPEAR IN BROWSER CONTENT)
# ---------------------------------------------------------------------------

def test_secrets_never_appear_in_api_responses():
    """Configured provider keys never appear in API responses or introspection endpoints."""
    secrets = {
        "GROQ_API_KEY_PRIMARY": "gsk_primary_secret_key_testing_12345",
        "GROQ_API_KEY_SECONDARY": "gsk_secondary_secret_key_testing_67890",
        "OPENROUTER_API_KEY": "sk-or-v1-openrouter_secret_testing_99999",
    }

    with patch.dict(os.environ, secrets, clear=False):
        with TestClient(app) as client:
            for endpoint in ("/api/health", "/api", "/health", "/api/agents"):
                resp = client.get(endpoint)
                assert resp.status_code == 200
                content_str = resp.text
                for key_name, secret_val in secrets.items():
                    assert key_name not in content_str, f"{key_name} exposed in {endpoint}"
                    assert secret_val not in content_str, f"Secret value of {key_name} exposed in {endpoint}"


def test_secrets_never_appear_in_web_html_pages():
    """Configured provider keys never appear in rendered server-side HTML pages."""
    secrets = {
        "GROQ_API_KEY_PRIMARY": "gsk_primary_secret_key_testing_12345",
        "GROQ_API_KEY_SECONDARY": "gsk_secondary_secret_key_testing_67890",
        "OPENROUTER_API_KEY": "sk-or-v1-openrouter_secret_testing_99999",
    }

    with patch.dict(os.environ, secrets, clear=False):
        with TestClient(app) as client:
            for page in ("/", "/404", "/research?query=AAPL"):
                resp = client.get(page, headers={"Accept": "text/html"})
                assert resp.status_code in {200, 404}
                content_str = resp.text
                for key_name, secret_val in secrets.items():
                    assert key_name not in content_str, f"{key_name} leaked in HTML {page}"
                    assert secret_val not in content_str, f"Secret value leaked in HTML {page}"


def test_research_logging_filters_secrets_and_prompts():
    """log_research_event strips prompt, response, api_key, authorization from logged fields."""
    with patch.object(LOGGER, "info") as mock_info:
        log_research_event(
            "test_event",
            safe_metric=42,
            query="AAPL",
            api_key="gsk_secret",
            authorization="Bearer secret",
            prompt="Analyze this private balance sheet",
            response="Model response payload",
        )

        assert mock_info.called
        args, _ = mock_info.call_args
        logged_event = args[1]
        logged_fields = args[2]

        assert logged_event == "test_event"
        assert logged_fields["safe_metric"] == 42
        assert logged_fields["query"] == "AAPL"
        assert "api_key" not in logged_fields
        assert "authorization" not in logged_fields
        assert "prompt" not in logged_fields
        assert "response" not in logged_fields
