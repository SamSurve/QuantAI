"""Tests for evidence appendix, provenance ledger, freshness mapping, and disclosure."""

from __future__ import annotations

import pytest
from fastapi.templating import Jinja2Templates

from api.research_schemas import (
    FreshnessRecord,
    FreshnessState,
    MarketIntelligenceFreshness,
    ResearchWarning,
    SourceRecord,
)
from api.web.evidence import (
    EvidenceAppendixView,
    FreshnessItemView,
    SourceRecordView,
    WarningItemView,
    format_freshness_item,
    format_source_record,
    process_evidence_appendix,
)


def test_freshness_states_mapping():
    """Verify all 5 freshness states map to expected text and CSS badge classes."""
    live = format_freshness_item("Market quote", FreshnessRecord(state=FreshnessState.LIVE, as_of="2026-09-05T16:00:00Z"))
    assert live.state == "LIVE"
    assert "live" in live.badge_class
    assert "na" not in live.badge_class

    cached = format_freshness_item("Price history", FreshnessRecord(state=FreshnessState.CACHED, as_of="2026-09-05T15:55:00Z"))
    assert cached.state == "CACHED"
    assert "cache" in cached.badge_class

    recent = format_freshness_item("Fundamentals", FreshnessRecord(state=FreshnessState.RECENT, as_of="2026-06-30"))
    assert recent.state == "RECENT"
    assert "cache" in recent.badge_class

    unavail = format_freshness_item("Corporate events", FreshnessRecord(state=FreshnessState.UNAVAILABLE))
    assert unavail.state == "UNAVAILABLE"
    assert "na" in unavail.badge_class
    assert "live" not in unavail.badge_class


def test_not_requested_badge_neutrality():
    """Verify NOT_REQUESTED is styled neutrally and never as LIVE or UNAVAILABLE."""
    not_req = format_freshness_item("AI Analysis", FreshnessRecord(state=FreshnessState.NOT_REQUESTED))
    assert not_req.state == "NOT_REQUESTED"
    assert not_req.state_display == "Not requested"
    # Must be neutral: never styled as LIVE or UNAVAILABLE
    assert "live" not in not_req.badge_class
    assert "na" not in not_req.badge_class
    assert "b" in not_req.badge_class


def test_source_records_mapping_and_url_safety():
    """Verify source records preserve provider, data type, timestamp, and sanitize unsafe URLs."""
    safe_rec = SourceRecord(
        source="SEC EDGAR",
        data_type="financial",
        retrieved_at="2026-09-05T16:00:00Z",
        url="https://www.sec.gov/edgar/searchedgar/companysearch",
    )
    view = format_source_record(safe_rec)
    assert view.source == "SEC EDGAR"
    assert view.data_type == "financial"
    assert view.retrieved_at == "2026-09-05T16:00:00Z"
    assert view.url == "https://www.sec.gov/edgar/searchedgar/companysearch"

    unsafe_rec = SourceRecord(
        source="Malicious Source",
        data_type="news",
        retrieved_at="2026-09-05T16:00:00Z",
        url="javascript:alert(1)",
    )
    unsafe_view = format_source_record(unsafe_rec)
    assert unsafe_view.url is None


def test_missing_source_urls_and_timestamps():
    """Verify missing source URLs and timestamps fall back cleanly without inventing data."""
    raw = {
        "source": "Minimal Provider",
        "data_type": "history",
        "retrieved_at": None,
        "url": None,
    }
    view = format_source_record(raw)
    assert view.source == "Minimal Provider"
    assert view.url is None
    assert view.retrieved_at == "Timestamp unavailable"


def test_warnings_preservation():
    """Verify research warnings preserve category and message."""
    warning = ResearchWarning(
        category="DATA_UNAVAILABLE",
        message="Historical series contains unadjusted non-trading gaps.",
    )
    appendix = process_evidence_appendix(
        freshness_records=[("Market", FreshnessRecord(state=FreshnessState.LIVE))],
        sources=[],
        warnings=[warning],
    )
    assert len(appendix.warnings) == 1
    assert appendix.warnings[0].category == "DATA_UNAVAILABLE"
    assert "Historical series contains unadjusted" in appendix.warnings[0].message


def test_evidence_ai_separation():
    """Verify AI interpretation is never represented as provider evidence or given LIVE status."""
    appendix = process_evidence_appendix(
        freshness_records=[
            ("Market quote", FreshnessRecord(state=FreshnessState.LIVE)),
            ("AI Analysis", FreshnessRecord(state=FreshnessState.NOT_REQUESTED)),
        ],
        sources=[
            SourceRecord(source="Exchange Feed", data_type="market", retrieved_at="2026-09-05T16:00:00Z", url="https://example.com/feed")
        ],
        warnings=[],
    )
    ai_item = next(item for item in appendix.freshness if item.label == "AI Analysis")
    assert ai_item.badge_class != "b live"
    assert ai_item.state_display == "Not requested"

    # Verify no source record is invented for AI
    for src in appendix.sources:
        assert "AI" not in src.source
        assert "Agent" not in src.source


def test_evidence_appendix_template_rendering():
    """Verify the evidence appendix renders native details/summary, records, and badges."""
    templates = Jinja2Templates(directory="templates")

    appendix = EvidenceAppendixView(
        freshness=[
            FreshnessItemView(
                label="Market quote",
                state="LIVE",
                state_display="LIVE",
                badge_class="b live",
                as_of="2026-09-05 · Retrieved 16:00 UTC",
                source_description="Provider · retrieved 16:00 UTC",
            ),
            FreshnessItemView(
                label="Corporate events",
                state="UNAVAILABLE",
                state_display="UNAVAILABLE",
                badge_class="b na",
                as_of="Unavailable",
                source_description="No source returned",
            ),
            FreshnessItemView(
                label="AI Analysis",
                state="NOT_REQUESTED",
                state_display="Not requested",
                badge_class="b lo",
                as_of="Not requested",
                source_description="Optional interpretation disabled",
            ),
        ],
        sources=[
            SourceRecordView(
                source="NASDAQ Consolidated Feed",
                data_type="quote",
                retrieved_at="2026-09-05 16:00:00",
                url="https://example.com/nasdaq",
            )
        ],
        warnings=[
            WarningItemView(
                category="freshness",
                message="Corporate calendar returned 0 upcoming filings.",
            )
        ],
        has_content=True,
    )

    html = templates.get_template("partials/evidence_appendix.html").render({"evidence_appendix": appendix})

    assert "Evidence appendix" in html
    assert "<details" in html
    assert "<summary" in html
    assert "Show sources and freshness" in html
    assert "Market quote" in html
    assert "b live" in html
    assert "LIVE" in html
    assert "Corporate events" in html
    assert "b na" in html
    assert "UNAVAILABLE" in html
    assert "AI Analysis" in html
    assert "Not requested" in html
    assert "NASDAQ Consolidated Feed" in html
    assert "https://example.com/nasdaq" in html
    assert 'rel="noopener noreferrer"' in html
    assert "Corporate calendar returned 0 upcoming filings." in html
