"""Regression test suite for Part 25: TTL Cache and Request Coalescing.

Verifies:
1. Exact cache TTL constants:
   - Market quote: 60 seconds
   - Price history: 300 seconds
   - News feed: 300 seconds
   - Events radar: 21,600 seconds (6 hours)
   - Entity resolution: 86,400 seconds (24 hours)
   - Provider cooldown: 300 seconds (5 minutes)
2. AsyncTTLCache hit, miss, expiration, and eviction semantics.
3. Concurrent single-flight request coalescing (shared in-flight tasks).
4. Cache key isolation, normalization, and collision resistance.
5. Service-level caching integration across research subsystems.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from api.ai_providers import PERMANENT_FAILURE_COOLDOWN_SECONDS
from api.company_analysis_services import (
    COMPANY_PROFILE_TTL_SECONDS,
    FINANCIALS_TTL_SECONDS,
)
from api.fx_services import FX_TTL_SECONDS
from api.market_intelligence_services import (
    EVENTS_TTL_SECONDS,
    HISTORY_TTL_SECONDS,
    MARKET_PULSE_TTL_SECONDS,
)
from api.research_cache import AsyncTTLCache
from api.research_schemas import (
    CompanyIdentity,
    HistoryPeriod,
    IdentifierConfidence,
    MarketSnapshot,
    ServiceState,
    SourceRecord,
)
from api.research_services import (
    ENTITY_TTL_SECONDS,
    MARKET_TTL_SECONDS,
    NEWS_TTL_SECONDS,
    EntityResolution,
    EntityResolutionService,
    MarketDataResult,
    MarketDataService,
    NewsDataResult,
    NewsService,
    _normalize_symbol,
)


# ---------------------------------------------------------------------------
# 1. EXACT TTL CONSTANTS VERIFICATION
# ---------------------------------------------------------------------------

def test_cache_ttl_constants():
    """Verify all 6 authoritative cache TTL values match the architecture contract."""
    # Quote / Market: 60s
    assert MARKET_TTL_SECONDS == 60
    assert MARKET_PULSE_TTL_SECONDS == 60

    # History: 300s (5 minutes)
    assert HISTORY_TTL_SECONDS == 300

    # News: 300s (5 minutes)
    assert NEWS_TTL_SECONDS == 300

    # Corporate events: 21,600s (6 hours)
    assert EVENTS_TTL_SECONDS == 21_600

    # Entity resolution: 86,400s (24 hours)
    assert ENTITY_TTL_SECONDS == 86_400

    # AI provider cooldown: 300s (5 minutes)
    assert PERMANENT_FAILURE_COOLDOWN_SECONDS == 300

    # Associated auxiliary TTLs
    assert COMPANY_PROFILE_TTL_SECONDS == 3_600
    assert FINANCIALS_TTL_SECONDS == 21_600
    assert FX_TTL_SECONDS == 900


# ---------------------------------------------------------------------------
# 2. ASYNC TTL CACHE HIT, MISS, EXPIRATION, EVICTION
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_ttl_cache_hit_and_miss():
    """First call loads data (miss); subsequent call within TTL returns cached value (hit)."""
    cache: AsyncTTLCache[str] = AsyncTTLCache()
    loader_calls = 0

    async def sample_loader() -> str:
        nonlocal loader_calls
        loader_calls += 1
        return f"value-{loader_calls}"

    # Miss: invokes loader
    val1, hit1 = await cache.get_or_load("key1", 60.0, sample_loader)
    assert val1 == "value-1"
    assert hit1 is False
    assert loader_calls == 1

    # Hit: does not invoke loader
    val2, hit2 = await cache.get_or_load("key1", 60.0, sample_loader)
    assert val2 == "value-1"
    assert hit2 is True
    assert loader_calls == 1


@pytest.mark.asyncio
async def test_async_ttl_cache_expiration_and_eviction():
    """Entries expire after ttl_seconds and are evicted on subsequent access."""
    cache: AsyncTTLCache[str] = AsyncTTLCache()
    calls = 0

    async def loader() -> str:
        nonlocal calls
        calls += 1
        return f"result-{calls}"

    t0 = 500.0
    with patch("time.monotonic", return_value=t0):
        val1, hit1 = await cache.get_or_load("expiring_key", 60.0, loader)
        assert val1 == "result-1"
        assert hit1 is False
        assert calls == 1

    # Access just before expiration (t0 + 59.9) -> HIT
    with patch("time.monotonic", return_value=t0 + 59.9):
        val2, hit2 = await cache.get_or_load("expiring_key", 60.0, loader)
        assert val2 == "result-1"
        assert hit2 is True
        assert calls == 1

    # Access after expiration (t0 + 60.1) -> MISS (evicted and reloaded)
    with patch("time.monotonic", return_value=t0 + 60.1):
        val3, hit3 = await cache.get_or_load("expiring_key", 60.0, loader)
        assert val3 == "result-2"
        assert hit3 is False
        assert calls == 2


@pytest.mark.asyncio
async def test_async_ttl_cache_clear_and_snapshot():
    """Clear empties all stored entries; snapshot returns counts accurately."""
    cache: AsyncTTLCache[int] = AsyncTTLCache()
    await cache.get_or_load("a", 10.0, AsyncMock(return_value=1))
    await cache.get_or_load("b", 10.0, AsyncMock(return_value=2))

    snap = await cache.snapshot()
    assert snap["entries"] == 2
    assert snap["inflight"] == 0

    await cache.clear()
    snap_after = await cache.snapshot()
    assert snap_after["entries"] == 0
    assert snap_after["inflight"] == 0


# ---------------------------------------------------------------------------
# 3. SINGLE-FLIGHT CONCURRENT REQUEST COALESCING
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_single_flight_coalescing():
    """Concurrent requests for the same key share a single active loader execution."""
    cache: AsyncTTLCache[dict[str, str]] = AsyncTTLCache()
    load_count = 0
    gate = asyncio.Event()

    async def slow_upstream_loader() -> dict[str, str]:
        nonlocal load_count
        load_count += 1
        # Wait on gate to simulate real network delay
        await gate.wait()
        return {"data": "coalesced_result", "load_id": str(load_count)}

    # Dispatch 10 concurrent requests simultaneously
    async def caller():
        val, hit = await cache.get_or_load("shared_quote:AAPL", 60.0, slow_upstream_loader)
        return val

    tasks = [asyncio.create_task(caller()) for _ in range(10)]
    await asyncio.sleep(0.01)

    # In-flight task is recorded
    snap = await cache.snapshot()
    assert snap["inflight"] == 1

    # Release the upstream loader
    gate.set()
    results = await asyncio.gather(*tasks)

    # Every caller got identical result, loader was called exactly ONCE
    assert len(results) == 10
    for res in results:
        assert res["data"] == "coalesced_result"
        assert res["load_id"] == "1"
    assert load_count == 1

    # Inflight is cleared and entry is stored
    snap_final = await cache.snapshot()
    assert snap_final["inflight"] == 0
    assert snap_final["entries"] == 1


@pytest.mark.asyncio
async def test_single_flight_exception_does_not_poison_cache():
    """Failed in-flight loader cleans up inflight map so next call can retry."""
    cache: AsyncTTLCache[str] = AsyncTTLCache()
    attempts = 0

    async def failing_loader() -> str:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ConnectionError("Upstream timeout")
        return "recovered"

    with pytest.raises(ConnectionError):
        await cache.get_or_load("retry_key", 60.0, failing_loader)

    # Inflight task was removed
    snap = await cache.snapshot()
    assert snap["inflight"] == 0
    assert snap["entries"] == 0

    # Subsequent request successfully attempts and caches
    val, hit = await cache.get_or_load("retry_key", 60.0, failing_loader)
    assert val == "recovered"
    assert hit is False
    assert attempts == 2


# ---------------------------------------------------------------------------
# 4. CACHE KEY ISOLATION & NORMALIZATION
# ---------------------------------------------------------------------------

def test_symbol_normalization():
    """_normalize_symbol standardizes lowercase, mixed case, and whitespace."""
    assert _normalize_symbol("aapl") == "AAPL"
    assert _normalize_symbol("  AAPL  ") == "AAPL"
    assert _normalize_symbol("brk.b") == "BRK.B"
    assert _normalize_symbol("msft  ") == "MSFT"


@pytest.mark.asyncio
async def test_cache_keys_are_isolated_across_tickers_and_modes():
    """Cache keys for different tickers and time periods do not collide."""
    cache: AsyncTTLCache[str] = AsyncTTLCache()

    async def load_aapl():
        return "AAPL_DATA"

    async def load_msft():
        return "MSFT_DATA"

    async def load_aapl_1d():
        return "AAPL_1D"

    async def load_aapl_1y():
        return "AAPL_1Y"

    await cache.get_or_load("market:AAPL", 60.0, load_aapl)
    await cache.get_or_load("market:MSFT", 60.0, load_msft)
    await cache.get_or_load(f"history:AAPL:{HistoryPeriod.ONE_DAY.value}", 300.0, load_aapl_1d)
    await cache.get_or_load(f"history:AAPL:{HistoryPeriod.ONE_YEAR.value}", 300.0, load_aapl_1y)

    snap = await cache.snapshot()
    assert snap["entries"] == 4

    val_aapl, hit_a = await cache.get_or_load("market:AAPL", 60.0, load_aapl)
    val_msft, hit_m = await cache.get_or_load("market:MSFT", 60.0, load_msft)
    val_1d, hit_1d = await cache.get_or_load(f"history:AAPL:{HistoryPeriod.ONE_DAY.value}", 300.0, load_aapl_1d)
    val_1y, hit_1y = await cache.get_or_load(f"history:AAPL:{HistoryPeriod.ONE_YEAR.value}", 300.0, load_aapl_1y)

    assert val_aapl == "AAPL_DATA" and hit_a is True
    assert val_msft == "MSFT_DATA" and hit_m is True
    assert val_1d == "AAPL_1D" and hit_1d is True
    assert val_1y == "AAPL_1Y" and hit_1y is True


# ---------------------------------------------------------------------------
# 5. SERVICE-LEVEL CACHE INTEGRATION
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_entity_resolution_service_caching():
    """EntityResolutionService caches resolution results under entity:<symbol> for 86,400s."""
    cache: AsyncTTLCache[EntityResolution] = AsyncTTLCache()
    service = EntityResolutionService(cache=cache)

    fake_resolution = EntityResolution(
        company=CompanyIdentity(symbol="AAPL", name="Apple Inc.", identifier_confidence=IdentifierConfidence.HIGH),
        candidates=[],
        source=SourceRecord(source="Yahoo", retrieved_at="2026-01-01T00:00:00Z", data_type="entity"),
    )

    with patch.object(service, "_resolve_uncached", new_callable=AsyncMock) as mock_uncached:
        mock_uncached.return_value = fake_resolution

        # First call: uncached
        res1 = await service.resolve("AAPL")
        assert res1.company.symbol == "AAPL"
        assert mock_uncached.call_count == 1

        # Second call with lowercase: hits cache via normalized key
        res2 = await service.resolve("aapl")
        assert res2.company.symbol == "AAPL"
        assert mock_uncached.call_count == 1

        # Third call with spaces: hits cache
        res3 = await service.resolve("  AAPL  ")
        assert res3.company.symbol == "AAPL"
        assert mock_uncached.call_count == 1


@pytest.mark.asyncio
async def test_market_data_service_caching():
    """MarketDataService caches quote data under market:<symbol> for 60s."""
    cache: AsyncTTLCache[MarketDataResult] = AsyncTTLCache()
    service = MarketDataService(cache=cache)

    company = CompanyIdentity(symbol="NVDA", identifier_confidence=IdentifierConfidence.HIGH)
    fake_result = MarketDataResult(
        company=company,
        market=MarketSnapshot(current_price=120.0, currency="USD"),
        history=[],
        status=ServiceState.AVAILABLE,
        warning=None,
        sources=[],
    )

    with patch.object(service, "_fetch_uncached", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = fake_result

        # First fetch: calls upstream
        m1 = await service.fetch(company)
        assert m1.market.current_price == 120.0
        assert mock_fetch.call_count == 1

        # Second fetch: hits cache
        m2 = await service.fetch(company)
        assert m2.market.current_price == 120.0
        assert mock_fetch.call_count == 1


@pytest.mark.asyncio
async def test_news_service_caching():
    """NewsService caches news feeds under news:<symbol> for 300s."""
    cache: AsyncTTLCache[NewsDataResult] = AsyncTTLCache()
    service = NewsService(cache=cache)

    company = CompanyIdentity(symbol="TSLA", name="Tesla Inc.", identifier_confidence=IdentifierConfidence.HIGH)
    fake_news = NewsDataResult(items=[], status=ServiceState.AVAILABLE, warning=None, sources=[])

    with patch.object(service, "_fetch_uncached", new_callable=AsyncMock) as mock_news:
        mock_news.return_value = fake_news

        n1 = await service.fetch(company)
        assert n1.status == ServiceState.AVAILABLE
        assert mock_news.call_count == 1

        n2 = await service.fetch(company)
        assert n2.status == ServiceState.AVAILABLE
        assert mock_news.call_count == 1
