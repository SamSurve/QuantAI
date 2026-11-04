"""AI research brief presentation models and processing."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from api.web.markdown import extract_editorial_lead, render_markdown


class AnalysisBriefView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    has_analysis: bool = False
    is_unavailable: bool = False
    unavailable_notice: str | None = None
    lead: str | None = None
    rendered_html: str = ""


def process_analysis_brief(
    analysis_text: str | None,
    is_unavailable: bool = False,
    notice: str | None = None,
) -> AnalysisBriefView:
    """Format and render optional AI analysis brief with server-side markdown and math."""
    if is_unavailable:
        default_notice = notice or "AI interpretation is temporarily unavailable. Sourced data remains fully accessible."
        return AnalysisBriefView(
            has_analysis=False,
            is_unavailable=True,
            unavailable_notice=default_notice,
            lead=None,
            rendered_html="",
        )

    if not analysis_text or not analysis_text.strip():
        return AnalysisBriefView(
            has_analysis=False,
            is_unavailable=False,
            unavailable_notice=None,
            lead=None,
            rendered_html="",
        )

    lead = extract_editorial_lead(analysis_text)
    rendered = render_markdown(analysis_text)

    return AnalysisBriefView(
        has_analysis=True,
        is_unavailable=False,
        unavailable_notice=None,
        lead=lead,
        rendered_html=rendered,
    )
