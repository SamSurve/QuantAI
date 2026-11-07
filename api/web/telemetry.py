"""Developer telemetry with strict environment gating for QuantAI.

Telemetry is disabled by default.
QUANTAI_DEVTOOLS=1 enables it only in development environments.
Production environments (ENVIRONMENT=production, VERCEL_ENV=production, NODE_ENV=production)
always disable telemetry unconditionally.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

_SENSITIVE_KEYS = frozenset({
    "prompt",
    "response",
    "api_key",
    "authorization",
    "secret",
    "password",
    "token",
    "cookie",
})


def is_production() -> bool:
    """Return True if any production environment variable is set."""
    for var in ("ENVIRONMENT", "VERCEL_ENV", "NODE_ENV", "QUANTAI_ENV"):
        val = os.getenv(var, "").strip().lower()
        if val in {"production", "prod"}:
            return True
    return False


def is_telemetry_enabled() -> bool:
    """Return True only if QUANTAI_DEVTOOLS=1 and NOT in a production environment."""
    if is_production():
        return False
    return os.getenv("QUANTAI_DEVTOOLS", "").strip() == "1"


@dataclass(frozen=True)
class TelemetryEvent:
    event_name: str
    timestamp: float
    properties: dict[str, Any]


class DeveloperTelemetrySink:
    """In-memory developer telemetry sink active only when explicitly enabled."""

    def __init__(self, max_events: int = 100) -> None:
        self._max_events = max_events
        self._events: list[TelemetryEvent] = []

    def record(self, event_name: str, **properties: Any) -> bool:
        """Record an event if telemetry is enabled. Returns True if recorded, False if disabled."""
        if not is_telemetry_enabled():
            return False

        safe_props = {
            k: v for k, v in properties.items()
            if k.lower() not in _SENSITIVE_KEYS
        }
        event = TelemetryEvent(
            event_name=event_name,
            timestamp=time.time(),
            properties=safe_props,
        )
        self._events.append(event)
        if len(self._events) > self._max_events:
            self._events.pop(0)
        return True

    def get_events(self) -> list[dict[str, Any]]:
        """Return recorded events if enabled, else empty list."""
        if not is_telemetry_enabled():
            return []
        return [
            {
                "event": e.event_name,
                "timestamp": e.timestamp,
                "properties": e.properties,
            }
            for e in self._events
        ]

    def clear(self) -> None:
        self._events.clear()


telemetry_sink = DeveloperTelemetrySink()


def record_developer_event(event_name: str, **properties: Any) -> bool:
    """Public helper to record developer telemetry when gated on."""
    return telemetry_sink.record(event_name, **properties)
