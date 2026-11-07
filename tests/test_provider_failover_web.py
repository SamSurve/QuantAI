"""Regression test suite for Part 25: Provider Failover and Deterministic Fallback.

Verifies:
1. Sequential provider failover in exact order:
   Groq Primary -> Groq Secondary -> OpenRouter Ox Alpha.
2. Health-store cooldown transitions:
   - 300-second cooldown on authentication failure and model unavailable.
   - 60-second cooldown on repeated failures (threshold >= 2).
   - Skipping cooled-down providers and restoring availability after cooldown expiration.
3. Structured provider engine failover:
   - Recovers valid typed schema from secondary or tertiary provider when primary fails.
4. Orchestrator fallback to deterministic market data when all AI providers fail:
   - Deterministic quote, history, news, and company profile remain available.
   - AI status accurately reports UNAVAILABLE without failing the request.
5. Provider health reporting secrecy:
   - safe_status never reveals provider credentials, model names, or internal URLs.
"""

from __future__ import annotations

import asyncio
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from agno.exceptions import ModelProviderError
from agno.models.response import ModelResponse
from pydantic import BaseModel

from api.ai_providers import (
    DEFAULT_PROVIDER_ORDER,
    PERMANENT_FAILURE_COOLDOWN_SECONDS,
    REPEATED_FAILURE_COOLDOWN_SECONDS,
    AIProvider,
    ProviderFailure,
    ProviderFailureCategory,
    ProviderHealthStore,
    ProviderRouter,
    StructuredProviderEngine,
    USER_FRIENDLY_UNAVAILABLE,
    classify_provider_failure,
    provider_runtime_status,
)
from api.research_orchestrator import AnalysisSynthesisService, ResearchOrchestrator
from api.research_schemas import (
    CompanyIdentity,
    ErrorCategory,
    IdentifierConfidence,
    MarketSnapshot,
    OverallState,
    ResearchRequest,
    ResearchResponse,
    ServiceState,
    ServiceStatus,
    SourceRecord,
    StructuredAnalysis,
)
from api.research_services import EntityResolution, MarketDataResult, NewsDataResult


class DummySchema(BaseModel):
    verdict: str
    score: int


class MockModel:
    def __init__(self, outcomes: list[object]) -> None:
        self.outcomes = list(outcomes)
        self.calls = 0

    def invoke(self, *_args, **_kwargs):
        self.calls += 1
        if not self.outcomes:
            raise RuntimeError("Exhausted outcomes")
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return ModelResponse(content=outcome)

    async def ainvoke(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)


def make_test_router(primary_outcomes: list[object], secondary_outcomes: list[object], ox_outcomes: list[object]):
    p_mod = MockModel(primary_outcomes)
    s_mod = MockModel(secondary_outcomes)
    ox_mod = MockModel(ox_outcomes)

    router = ProviderRouter(
        id="quantai-provider-engine",
        name="QuantAI Provider Engine",
        provider="QuantAI",
        providers=(
            AIProvider("Groq primary", "groq/primary-model", p_mod, True),
            AIProvider("Groq secondary", "groq/secondary-model", s_mod, True),
            AIProvider("OpenRouter Ox Alpha", "stealth/ox-alpha", ox_mod, True),
        ),
        retries=0,
        retry_with_guidance=False,
        retry_with_guidance_limit=0,
    )
    return router, p_mod, s_mod, ox_mod


# ---------------------------------------------------------------------------
# 1. SEQUENTIAL PROVIDER FAILOVER IN EXACT ORDER
# ---------------------------------------------------------------------------

def test_default_provider_order_is_authoritative():
    """Verify DEFAULT_PROVIDER_ORDER matches approved specification."""
    assert DEFAULT_PROVIDER_ORDER == ("groq_primary", "groq_secondary", "openrouter_ox_alpha")


def test_sequential_failover_primary_success():
    """When primary succeeds, secondary and OpenRouter are never invoked."""
    router, p, s, ox = make_test_router(["primary-ok"], ["unexpected"], ["unexpected"])
    resp = router.response([MagicMock(role="user", content="Test")])
    assert resp.content == "primary-ok"
    assert (p.calls, s.calls, ox.calls) == (1, 0, 0)


def test_sequential_failover_primary_429_secondary_succeeds():
    """When primary encounters 429 rate-limit, execution falls forward to secondary."""
    rate_err = Exception("rate limit exceeded")
    rate_err.status_code = 429

    router, p, s, ox = make_test_router([rate_err], ["secondary-ok"], ["unexpected"])
    resp = router.response([MagicMock(role="user", content="Test")])
    assert resp.content == "secondary-ok"
    assert (p.calls, s.calls, ox.calls) == (1, 1, 0)


def test_sequential_failover_to_tertiary_openrouter():
    """When primary (503) and secondary (429) fail, tertiary OpenRouter succeeds."""
    err_503 = Exception("service unavailable")
    err_503.status_code = 503
    err_429 = Exception("rate limited")
    err_429.status_code = 429

    router, p, s, ox = make_test_router([err_503], [err_429], ["ox-alpha-ok"])
    resp = router.response([MagicMock(role="user", content="Test")])
    assert resp.content == "ox-alpha-ok"
    assert (p.calls, s.calls, ox.calls) == (1, 1, 1)


def test_all_providers_fail_raises_model_provider_error():
    """When all providers fail, a safe ModelProviderError with sanitized message is raised."""
    err_a = Exception("rate limited")
    err_a.status_code = 429
    err_b = Exception("internal server error")
    err_b.status_code = 500
    err_c = Exception("timeout")
    err_c.status_code = 408

    router, p, s, ox = make_test_router([err_a], [err_b], [err_c])
    with pytest.raises(ModelProviderError) as exc_info:
        router.response([MagicMock(role="user", content="Test")])

    assert USER_FRIENDLY_UNAVAILABLE in str(exc_info.value)
    assert (p.calls, s.calls, ox.calls) == (1, 1, 1)


# ---------------------------------------------------------------------------
# 2. STRUCTURED ENGINE FAILOVER
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_structured_engine_failover():
    """StructuredProviderEngine falls forward across providers to parse schema."""
    health_store = ProviderHealthStore()

    p_provider = AIProvider("Groq primary", "m1", MagicMock(), True)
    s_provider = AIProvider("Groq secondary", "m2", MagicMock(), True)

    expected = DummySchema(verdict="BULLISH", score=85)

    async def mock_runner(provider: AIProvider, _prompt: str, _schema):
        if provider.name == "Groq primary":
            err = Exception("Primary rate limit")
            err.status_code = 429
            raise err
        return expected

    engine = StructuredProviderEngine(
        providers=(p_provider, s_provider),
        health_store=health_store,
        runner=mock_runner,
    )

    result = await engine.generate_structured("prompt", DummySchema, request_id="test-struct")
    assert result.verdict == "BULLISH"
    assert result.score == 85


# ---------------------------------------------------------------------------
# 3. COOLDOWN DURATIONS, SKIPPING, AND RESTORATION
# ---------------------------------------------------------------------------

def test_permanent_failure_cooldown_duration():
    """Authentication failure and model not found trigger 300-second cooldown."""
    fail_auth = classify_provider_failure(Exception("invalid api key 401"))
    assert fail_auth.category == ProviderFailureCategory.AUTHENTICATION_FAILURE
    assert fail_auth.cooldown_seconds == PERMANENT_FAILURE_COOLDOWN_SECONDS
    assert fail_auth.cooldown_seconds == 300

    fail_model = classify_provider_failure(Exception("model does not exist 404"))
    assert fail_model.category == ProviderFailureCategory.MODEL_NOT_FOUND
    assert fail_model.cooldown_seconds == PERMANENT_FAILURE_COOLDOWN_SECONDS
    assert fail_model.cooldown_seconds == 300


def test_repeated_failure_cooldown_duration():
    """Two consecutive non-permanent failures trigger 60-second cooldown."""
    store = ProviderHealthStore()
    provider_name = "test-provider"

    fail_503 = classify_provider_failure(Exception("service unavailable 503"))
    assert fail_503.cooldown_seconds is None

    # First failure: no cooldown yet
    store.record_failure(provider_name, fail_503)
    assert store.is_available(provider_name) is True

    # Second failure (threshold >= 2): enters 60s cooldown
    t0 = 1000.0
    with patch("time.monotonic", return_value=t0):
        store.record_failure(provider_name, fail_503)
        assert store.is_available(provider_name) is False

    # After 59s: still in cooldown
    with patch("time.monotonic", return_value=t0 + 59.0):
        assert store.is_available(provider_name) is False

    # After 60.1s: restored to available
    with patch("time.monotonic", return_value=t0 + 60.1):
        assert store.is_available(provider_name) is True


def test_provider_skipped_during_cooldown():
    """A cooled-down provider is skipped without calling its underlying model."""
    fail_auth = Exception("unauthorized 401")
    fail_auth.status_code = 401

    router, p, s, ox = make_test_router(
        [fail_auth, "never-called-during-cooldown"],
        ["secondary-first", "secondary-second"],
        ["unexpected"],
    )

    # First request: primary fails with 401, enters 300s cooldown; secondary succeeds
    assert router.response([MagicMock(role="user", content="1")]).content == "secondary-first"
    assert (p.calls, s.calls, ox.calls) == (1, 1, 0)

    # Second request: primary is skipped immediately due to cooldown; secondary handles
    assert router.response([MagicMock(role="user", content="2")]).content == "secondary-second"
    assert (p.calls, s.calls, ox.calls) == (1, 2, 0)


# ---------------------------------------------------------------------------
# 4. ORCHESTRATOR FALLBACK TO DETERMINISTIC DATA WHEN ALL AI FAILS
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_deterministic_data_preserved_when_ai_fails():
    """Deterministic market/news data is preserved when AI synthesis is unavailable."""
    # Router where all AI providers encounter failures
    err_503 = Exception("service unavailable 503")
    err_503.status_code = 503
    err_429 = Exception("rate limit 429")
    err_429.status_code = 429
    err_timeout = TimeoutError("deadline exceeded")

    router, _, _, _ = make_test_router([err_503], [err_429], [err_timeout])
    analysis_svc = AnalysisSynthesisService(router=router)
    orchestrator = ResearchOrchestrator(analysis_service=analysis_svc)

    # Mock deterministic upstream services
    entity = CompanyIdentity(
        symbol="AAPL",
        name="Apple Inc.",
        identifier_confidence=IdentifierConfidence.HIGH,
    )
    resolution = EntityResolution(
        company=entity,
        candidates=[],
        source=SourceRecord(source="Yahoo", retrieved_at="2026-01-01T00:00:00Z", data_type="entity"),
    )
    quote_result = MarketDataResult(
        company=entity,
        market=MarketSnapshot(current_price=180.5, currency="USD"),
        history=[],
        status=ServiceState.AVAILABLE,
        warning=None,
        sources=[],
    )
    news_result = NewsDataResult(
        items=[],
        status=ServiceState.AVAILABLE,
        warning=None,
        sources=[],
    )

    with patch.object(orchestrator.entity_service, "resolve", new_callable=AsyncMock) as mock_ent, \
         patch.object(orchestrator.market_service, "fetch", new_callable=AsyncMock) as mock_mkt, \
         patch.object(orchestrator.news_service, "fetch", new_callable=AsyncMock) as mock_news:

        mock_ent.return_value = resolution
        mock_mkt.return_value = quote_result
        mock_news.return_value = news_result

        req = ResearchRequest(query="AAPL", include_analysis=True)
        response = await orchestrator.research("req-det-fallback", req)

        # Factual data remains available
        assert response.company is not None
        assert response.company.symbol == "AAPL"
        assert response.market is not None
        assert response.market.current_price == 180.5
        assert response.status.market == ServiceState.AVAILABLE
        assert response.status.news == ServiceState.AVAILABLE

        # AI status is correctly reported as UNAVAILABLE without crashing the response
        assert response.status.ai == ServiceState.UNAVAILABLE
        assert response.analysis is None
        assert any(w.category == ErrorCategory.AI_UNAVAILABLE for w in response.warnings)


# ---------------------------------------------------------------------------
# 5. SAFE HEALTH STATUS REPORTING
# ---------------------------------------------------------------------------

def test_safe_health_status_never_exposes_names_or_secrets():
    """safe_status and provider_runtime_status expose only counts and scopes."""
    store = ProviderHealthStore()
    configured = ("Groq primary", "Groq secondary", "OpenRouter Ox Alpha")

    status = store.safe_status(configured)
    assert status == {
        "configured_count": 3,
        "available_count": 3,
        "health_scope": "process_local",
    }

    # Record failure on one provider
    fail = classify_provider_failure(Exception("401 unauthorized"))
    store.record_failure("Groq primary", fail)

    status2 = store.safe_status(configured)
    assert status2["configured_count"] == 3
    assert status2["available_count"] == 2

    # Verify no secret or internal identifier leaks in string serialization
    status_str = str(status2)
    for sensitive in ("Groq", "OpenRouter", "ox-alpha", "key", "token", "password"):
        assert sensitive.lower() not in status_str.lower()
