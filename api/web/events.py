"""Corporate events calendar radar presentation models, sorting, and formatting."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict

from api.web.formatters import format_date


class EventItemView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str
    event_type: str = "corporate"
    date: str | None = None
    formatted_date: str = "Date unavailable"
    importance: str = "medium"
    importance_class: str = "pill"
    source: str = "Source unavailable"


class EventsRadarView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    events: list[EventItemView] = []
    has_events: bool = False
    is_unavailable: bool = False


def format_event_item(event: Any) -> EventItemView:
    """Format a raw research event (dict, Pydantic model, or MarketBriefEvent)."""
    if isinstance(event, dict):
        title = str(event.get("title") or "").strip()
        event_type = str(event.get("event_type") or "corporate").strip()
        raw_date = event.get("date")
        importance = str(event.get("importance") or "medium").strip().lower()
        source = event.get("source")
    else:
        title = str(getattr(event, "title", "") or "").strip()
        event_type = str(getattr(event, "event_type", "corporate") or "corporate").strip()
        raw_date = getattr(event, "date", None)
        importance = str(getattr(event, "importance", "medium") or "medium").strip().lower()
        source = getattr(event, "source", None)

    formatted_date = format_date(raw_date, fallback="Date unavailable")
    source_str = source.strip() if (source and isinstance(source, str) and source.strip()) else "Source unavailable"

    # Styling class for importance matching Main.dc.html .b .hi / .lo
    if importance == "high":
        imp_class = "b hi"
    elif importance == "low":
        imp_class = "b lo"
    else:
        imp_class = "b"

    return EventItemView(
        title=title,
        event_type=event_type,
        date=raw_date,
        formatted_date=formatted_date,
        importance=importance,
        importance_class=imp_class,
        source=source_str,
    )


def process_events_radar(
    raw_events: list[Any] | None,
    is_unavailable: bool = False,
) -> EventsRadarView:
    """Sort chronologically and process events into a presentation view."""
    if is_unavailable or not raw_events:
        return EventsRadarView(
            events=[],
            has_events=False,
            is_unavailable=is_unavailable,
        )

    # Chronological sort (ascending by date)
    def date_key(x: Any) -> str:
        if isinstance(x, dict):
            return str(x.get("date") or "")
        return str(getattr(x, "date", None) or "")

    sorted_events = sorted(raw_events, key=date_key)
    events = [format_event_item(e) for e in sorted_events]

    return EventsRadarView(
        events=events,
        has_events=len(events) > 0,
        is_unavailable=False,
    )
