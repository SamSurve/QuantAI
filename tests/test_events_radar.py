"""Tests for corporate events radar, chronological ordering, importance mapping, and template rendering."""

from __future__ import annotations

import pytest
from fastapi.templating import Jinja2Templates

from api.research_schemas import ResearchEvent
from api.web.events import (
    EventItemView,
    EventsRadarView,
    format_event_item,
    process_events_radar,
)


def test_earnings_event_mapping():
    """Verify earnings event maps title, event type, date, importance, and source."""
    raw = ResearchEvent(
        event_type="earnings",
        title="Testco Q3 Fictional Earnings Release",
        date="2026-10-15T20:00:00Z",
        importance="high",
        source="Testco Investor Relations",
    )

    item = format_event_item(raw)
    assert item.title == "Testco Q3 Fictional Earnings Release"
    assert item.event_type == "earnings"
    assert item.formatted_date == "2026-10-15"
    assert item.importance.lower() == "high"
    assert item.source == "Testco Investor Relations"


def test_corporate_event_mapping():
    """Verify general corporate event fields are mapped correctly."""
    raw = {
        "event_type": "conference",
        "title": "Testco Synthetic Tech Showcase",
        "date": "2026-11-02",
        "importance": "medium",
        "source": "Fictional PR Wire",
    }

    item = format_event_item(raw)
    assert item.title == "Testco Synthetic Tech Showcase"
    assert item.event_type == "conference"
    assert item.formatted_date == "2026-11-02"
    assert item.importance.lower() == "medium"
    assert item.source == "Fictional PR Wire"


def test_chronological_ordering():
    """Verify events are sorted chronologically by date."""
    events = [
        {"title": "Late event", "date": "2026-11-10", "importance": "low"},
        {"title": "Early event", "date": "2026-09-15", "importance": "high"},
        {"title": "Middle event", "date": "2026-10-01", "importance": "medium"},
    ]

    radar = process_events_radar(events)
    assert len(radar.events) == 3
    assert radar.events[0].title == "Early event"
    assert radar.events[1].title == "Middle event"
    assert radar.events[2].title == "Late event"


def test_missing_optional_fields():
    """Verify missing event fields render standardized fallbacks."""
    raw = {
        "title": "Testco minimal event",
        "date": None,
        "source": None,
        "importance": "unknown",
    }

    item = format_event_item(raw)
    assert item.title == "Testco minimal event"
    assert item.formatted_date == "Date unavailable"
    assert item.source == "Source unavailable"


def test_empty_events_state():
    """Verify empty event list produces empty radar view."""
    radar = process_events_radar([])
    assert len(radar.events) == 0
    assert radar.has_events is False
    assert radar.is_unavailable is False


def test_unavailable_events_state():
    """Verify unavailable flag is passed through."""
    radar = process_events_radar([], is_unavailable=True)
    assert len(radar.events) == 0
    assert radar.has_events is False
    assert radar.is_unavailable is True


def test_events_template_rendering():
    """Verify template renders event rows, dates, and importance badges."""
    templates = Jinja2Templates(directory="templates")

    radar = EventsRadarView(
        events=[
            EventItemView(
                title="Testco Fictional Annual Meeting",
                event_type="shareholder_meeting",
                date="2026-10-20",
                formatted_date="2026-10-20",
                importance="high",
                source="SEC Form 8-K",
            ),
            EventItemView(
                title="Synthetic Product Demonstration",
                event_type="product",
                date="2026-11-05",
                formatted_date="2026-11-05",
                importance="medium",
                source="Testco Press",
            ),
        ],
        has_events=True,
    )

    html = templates.get_template("partials/events_radar.html").render({"events_radar": radar})

    assert "Events radar" in html
    assert "Testco Fictional Annual Meeting" in html
    assert "2026-10-20" in html
    assert "SEC Form 8-K" in html
    assert "high" in html.lower()
    assert "Synthetic Product Demonstration" in html
