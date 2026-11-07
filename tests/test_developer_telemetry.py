"""Unit tests for developer telemetry gating.

Verifies:
1. Telemetry is disabled by default.
2. QUANTAI_DEVTOOLS=1 enables telemetry in development.
3. Telemetry is strictly disabled in production even if QUANTAI_DEVTOOLS=1.
4. No sensitive keys, prompts, responses, or credentials can be recorded.
5. In-memory rolling event buffer and clearance.
"""

from unittest.mock import patch

from api.web.telemetry import (
    DeveloperTelemetrySink,
    is_production,
    is_telemetry_enabled,
    record_developer_event,
)


def test_telemetry_disabled_by_default():
    """Telemetry is disabled when QUANTAI_DEVTOOLS is unset or non-1."""
    with patch.dict("os.environ", {}, clear=True):
        assert is_telemetry_enabled() is False
        assert record_developer_event("test_event", metric=1) is False

    with patch.dict("os.environ", {"QUANTAI_DEVTOOLS": "0"}, clear=True):
        assert is_telemetry_enabled() is False

    with patch.dict("os.environ", {"QUANTAI_DEVTOOLS": "true"}, clear=True):
        assert is_telemetry_enabled() is False


def test_telemetry_enabled_in_development():
    """QUANTAI_DEVTOOLS=1 enables telemetry when not in production."""
    with patch.dict("os.environ", {"QUANTAI_DEVTOOLS": "1"}, clear=True):
        assert is_production() is False
        assert is_telemetry_enabled() is True


def test_telemetry_strictly_disabled_in_production():
    """Production flags unconditionally disable telemetry even if QUANTAI_DEVTOOLS=1."""
    production_flags = [
        {"ENVIRONMENT": "production", "QUANTAI_DEVTOOLS": "1"},
        {"VERCEL_ENV": "production", "QUANTAI_DEVTOOLS": "1"},
        {"NODE_ENV": "production", "QUANTAI_DEVTOOLS": "1"},
        {"QUANTAI_ENV": "production", "QUANTAI_DEVTOOLS": "1"},
        {"ENVIRONMENT": "prod", "QUANTAI_DEVTOOLS": "1"},
    ]

    for env_dict in production_flags:
        with patch.dict("os.environ", env_dict, clear=True):
            assert is_production() is True
            assert is_telemetry_enabled() is False
            sink = DeveloperTelemetrySink()
            assert sink.record("prod_event", count=1) is False
            assert len(sink.get_events()) == 0


def test_telemetry_strips_sensitive_keys():
    """Sensitive keys (prompts, responses, tokens, keys) are stripped from event payloads."""
    sink = DeveloperTelemetrySink()
    with patch.dict("os.environ", {"QUANTAI_DEVTOOLS": "1"}, clear=True):
        recorded = sink.record(
            "model_call",
            safe_latency=120,
            symbol="AAPL",
            api_key="gsk_secret_123",
            authorization="Bearer secret",
            prompt="Analyze confidential insider filing",
            response="Extracted predictions",
            secret="supersecret",
            token="bearer_token",
        )
        assert recorded is True

        events = sink.get_events()
        assert len(events) == 1
        props = events[0]["properties"]
        assert props["safe_latency"] == 120
        assert props["symbol"] == "AAPL"
        assert "api_key" not in props
        assert "authorization" not in props
        assert "prompt" not in props
        assert "response" not in props
        assert "secret" not in props
        assert "token" not in props


def test_telemetry_rolling_limit_and_clear():
    """Sink respects max_events limit and supports clear."""
    sink = DeveloperTelemetrySink(max_events=3)
    with patch.dict("os.environ", {"QUANTAI_DEVTOOLS": "1"}, clear=True):
        for i in range(5):
            sink.record(f"event_{i}", index=i)

        events = sink.get_events()
        assert len(events) == 3
        # Should have retained events 2, 3, 4
        assert events[0]["event"] == "event_2"
        assert events[2]["event"] == "event_4"

        sink.clear()
        assert len(sink.get_events()) == 0
