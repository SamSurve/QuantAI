"""Evidence appendix and provenance ledger formatting models and views."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse
from pydantic import BaseModel, ConfigDict

from api.research_schemas import FreshnessState


def is_safe_evidence_url(url: str | None) -> bool:
    """Validate that URL uses http or https scheme only."""
    if not url or not isinstance(url, str):
        return False
    trimmed = url.strip()
    try:
        parsed = urlparse(trimmed)
        return parsed.scheme.lower() in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


class FreshnessItemView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    label: str
    state: str
    state_display: str
    badge_class: str
    as_of: str = "Unavailable"
    source_description: str = "Provider source"


class SourceRecordView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source: str
    data_type: str = "general"
    retrieved_at: str = "Timestamp unavailable"
    url: str | None = None


class WarningItemView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    category: str
    message: str


class EvidenceAppendixView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    freshness: list[FreshnessItemView] = []
    sources: list[SourceRecordView] = []
    warnings: list[WarningItemView] = []
    has_content: bool = False


# Map internal field names to human-readable section labels
_LABEL_NAMES: dict[str, str] = {
    "company": "Company identity",
    "market": "Market quote",
    "history": "Price history",
    "news": "Recent news",
    "events": "Corporate events",
    "financials": "Fundamentals",
    "governance": "Governance",
    "competitors": "Competitive evidence",
    "analysis": "AI Analysis",
}


def format_freshness_item(label: str, record: Any) -> FreshnessItemView:
    """Format a single freshness record into a presentation view."""
    raw_state = getattr(record, "state", record if isinstance(record, str) else "unavailable")
    if hasattr(raw_state, "value"):
        state_str = str(raw_state.value).lower()
    else:
        state_str = str(raw_state).lower()

    as_of = getattr(record, "as_of", None) or getattr(record, "retrieved_at", None)
    as_of_str = str(as_of).strip() if as_of else "Unavailable"

    display_label = _LABEL_NAMES.get(label.lower(), label)

    if state_str == FreshnessState.LIVE.value:
        state_code = "LIVE"
        state_display = "LIVE"
        badge_class = "b live"
        desc = f"Provider · retrieved {as_of_str}" if as_of else "Live market feed"
    elif state_str == FreshnessState.CACHED.value:
        state_code = "CACHED"
        state_display = "CACHED"
        badge_class = "b cache"
        desc = f"Provider · cached as of {as_of_str}" if as_of else "Cached provider record"
    elif state_str == FreshnessState.RECENT.value:
        state_code = "RECENT"
        state_display = "RECENT"
        badge_class = "b cache"
        desc = f"Provider · period ending {as_of_str}" if as_of else "Recent provider record"
    elif state_str == FreshnessState.NOT_REQUESTED.value:
        state_code = "NOT_REQUESTED"
        state_display = "Not requested"
        badge_class = "b lo"  # Neutral badge, never live or na
        desc = "Optional interpretation not requested"
    else:  # unavailable or unknown
        state_code = "UNAVAILABLE"
        state_display = "UNAVAILABLE"
        badge_class = "b na"
        desc = "No source returned"

    return FreshnessItemView(
        label=display_label,
        state=state_code,
        state_display=state_display,
        badge_class=badge_class,
        as_of=as_of_str,
        source_description=desc,
    )


def format_source_record(source: Any) -> SourceRecordView:
    """Format a source record, preserving metadata and sanitizing URLs."""
    if isinstance(source, dict):
        src_name = str(source.get("source") or "Unknown Provider").strip()
        data_type = str(source.get("data_type") or "record").strip()
        raw_retrieved = source.get("retrieved_at")
        raw_url = source.get("url")
    else:
        src_name = str(getattr(source, "source", "") or "Unknown Provider").strip()
        data_type = str(getattr(source, "data_type", "record") or "record").strip()
        raw_retrieved = getattr(source, "retrieved_at", None)
        raw_url = getattr(source, "url", None)

    retrieved_str = str(raw_retrieved).strip() if (raw_retrieved and str(raw_retrieved).strip()) else "Timestamp unavailable"
    safe_url = raw_url.strip() if (raw_url and is_safe_evidence_url(raw_url)) else None

    return SourceRecordView(
        source=src_name,
        data_type=data_type,
        retrieved_at=retrieved_str,
        url=safe_url,
    )


def format_warning_item(warning: Any) -> WarningItemView:
    """Format a research warning record."""
    if isinstance(warning, dict):
        cat = str(warning.get("category") or "general").strip()
        msg = str(warning.get("message") or "").strip()
    else:
        raw_cat = getattr(warning, "category", "general")
        cat = str(getattr(raw_cat, "value", raw_cat)).strip()
        msg = str(getattr(warning, "message", "") or "").strip()

    return WarningItemView(category=cat, message=msg)


def process_evidence_appendix(
    freshness_records: list[tuple[str, Any]] | Any = None,
    sources: list[Any] | None = None,
    warnings: list[Any] | None = None,
) -> EvidenceAppendixView:
    """Construct full EvidenceAppendixView from freshness, sources, and warnings."""
    items: list[FreshnessItemView] = []

    # Unpack freshness records
    if freshness_records:
        if isinstance(freshness_records, list):
            for entry in freshness_records:
                if isinstance(entry, tuple) and len(entry) == 2:
                    lbl, rec = entry
                    items.append(format_freshness_item(lbl, rec))
                elif hasattr(entry, "label"):
                    items.append(format_freshness_item(entry.label, entry))
        elif hasattr(freshness_records, "__iter__"):
            # Pydantic model iteration yields (field_name, field_value)
            try:
                for lbl, rec in freshness_records:
                    items.append(format_freshness_item(lbl, rec))
            except Exception:
                pass

    source_views = [format_source_record(s) for s in (sources or [])]
    warning_views = [format_warning_item(w) for w in (warnings or [])]

    has_content = bool(items or source_views or warning_views)

    return EvidenceAppendixView(
        freshness=items,
        sources=source_views,
        warnings=warning_views,
        has_content=has_content,
    )
