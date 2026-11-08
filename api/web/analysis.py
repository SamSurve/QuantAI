"""AI research brief presentation models and processing."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from api.web.markdown import extract_editorial_lead, render_markdown


class AnalysisBriefView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    has_analysis: bool = False
    is_unavailable: bool = False
    unavailable_notice: str | None = None
    lead: str | None = None
    rendered_html: str = ""

    # Structured fields for premium report rendering
    executive_summary: str | None = None
    what_is_happening: str | None = None
    bullish_factors: list[str] = Field(default_factory=list)
    bearish_factors: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    catalysts: list[str] = Field(default_factory=list)
    what_to_watch: list[str] = Field(default_factory=list)
    market_sentiment: str | None = None
    confidence: str | None = None
    ai_verdict: str | None = None
    as_of: str | None = None
    has_structured: bool = False


def process_analysis_brief(
    analysis_text: str | None,
    is_unavailable: bool = False,
    notice: str | None = None,
    structured: Any = None,
    as_of: str | None = None,
) -> AnalysisBriefView:
    """Format and render optional AI analysis brief with server-side markdown and structured sections."""
    if is_unavailable:
        default_notice = notice or "AI interpretation is temporarily unavailable. Sourced data remains fully accessible."
        return AnalysisBriefView(
            has_analysis=False,
            is_unavailable=True,
            unavailable_notice=default_notice,
            lead=None,
            rendered_html="",
            has_structured=False,
        )

    exec_summary = None
    what_happening = None
    bullish: list[str] = []
    bearish: list[str] = []
    risk_items: list[str] = []
    catalyst_items: list[str] = []
    watch_items: list[str] = []
    sentiment = None
    confidence = None
    verdict = None
    has_structured = False

    if structured is not None:
        exec_summary = getattr(structured, "executive_summary", None)
        what_happening = getattr(structured, "what_is_happening", None) or getattr(structured, "business_model", None)
        bullish = list(getattr(structured, "bullish_factors", []) or getattr(structured, "growth_drivers", []) or [])
        bearish = list(getattr(structured, "bearish_factors", []) or [])
        risk_items = list(getattr(structured, "risks", []) or getattr(structured, "key_risks", []) or [])
        catalyst_items = list(getattr(structured, "catalysts", []) or [])
        watch_items = list(getattr(structured, "what_to_watch", []) or [])
        sentiment = getattr(structured, "market_sentiment", None)
        confidence = getattr(structured, "confidence", None)
        verdict = getattr(structured, "ai_verdict", None) or getattr(structured, "overall_assessment", None)

        has_structured = bool(
            exec_summary
            or what_happening
            or bullish
            or bearish
            or risk_items
            or catalyst_items
            or watch_items
            or sentiment
            or verdict
        )

    raw_text = (analysis_text or "").strip()
    if not raw_text and not has_structured:
        return AnalysisBriefView(
            has_analysis=False,
            is_unavailable=False,
            unavailable_notice=None,
            lead=None,
            rendered_html="",
            has_structured=False,
        )

    lead = None
    if raw_text:
        lead = extract_editorial_lead(raw_text)
    elif exec_summary:
        lead = extract_editorial_lead(exec_summary)

    rendered = render_markdown(raw_text) if raw_text else ""

    return AnalysisBriefView(
        has_analysis=True,
        is_unavailable=False,
        unavailable_notice=None,
        lead=lead,
        rendered_html=rendered,
        executive_summary=exec_summary,
        what_is_happening=what_happening,
        bullish_factors=bullish,
        bearish_factors=bearish,
        risks=risk_items,
        catalysts=catalyst_items,
        what_to_watch=watch_items,
        market_sentiment=sentiment,
        confidence=confidence,
        ai_verdict=verdict,
        as_of=as_of,
        has_structured=has_structured,
    )
