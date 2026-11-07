"""Recent research activity tracking, 5-item limit, ordering, and presentation models."""

from __future__ import annotations

import uuid
from typing import Any
from pydantic import BaseModel, Field


class ResearchActivityItem(BaseModel):
    """Represents a single research activity history record."""

    id: str = Field(default_factory=lambda: f"act-{uuid.uuid4().hex[:8]}")
    type: str  # e.g., "market_intelligence", "company_deep_analysis"
    query: str  # ticker or company name
    status: str  # "completed", "partial", "error"
    confidence: str | None = None


def format_activity_mode(raw_mode: str) -> str:
    """Format raw research mode into title-cased display label."""
    cleaned = (raw_mode or "").replace("_", " ").strip()
    return cleaned.title() if cleaned else "Research"


def format_activity_entry(entry: ResearchActivityItem | dict[str, Any]) -> dict[str, Any]:
    """Format an activity item into a view model for rendering."""
    if isinstance(entry, ResearchActivityItem):
        data = entry.model_dump()
    else:
        data = dict(entry)

    mode_display = format_activity_mode(data.get("type", ""))
    status = data.get("status", "completed")
    confidence = data.get("confidence")

    parts = [mode_display, status]
    if confidence:
        parts.append(confidence)

    subtitle = " · ".join(parts)

    return {
        "id": data.get("id"),
        "query": data.get("query", ""),
        "type": mode_display,
        "status": status,
        "confidence": confidence,
        "subtitle": subtitle,
    }


def add_research_activity(
    history: list[dict[str, Any]],
    query: str,
    mode: str,
    status: str = "completed",
    confidence: str | None = None,
) -> list[dict[str, Any]]:
    """Prepend a new research search to activity history, strictly capping at 5 items."""
    new_item = {
        "id": f"act-{uuid.uuid4().hex[:8]}",
        "type": mode,
        "query": query.strip().upper() if len(query.strip()) <= 5 else query.strip(),
        "status": status,
        "confidence": confidence,
    }
    updated = [new_item, *history]
    return updated[:5]
