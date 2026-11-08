"""Tests for AI research brief presentation, non-blocking fallback, and template rendering."""

from __future__ import annotations

import pytest
from fastapi.templating import Jinja2Templates

from api.research_schemas import StructuredAnalysis, CompanyDeepAnalysisInterpretation
from api.web.analysis import AnalysisBriefView, process_analysis_brief


def test_analysis_brief_processing_with_markdown_and_lead():
    """Verify analysis brief extracts editorial lead and renders sanitized HTML."""
    raw = (
        "# Executive Assessment\n"
        "A services-led margin story, priced for perfection and exposed to regulatory changes in key jurisdictions.\n\n"
        "Here is formula $E = mc^2$ and key risks:\n"
        "- Supply chain volatility\n"
        "- Regulatory compliance\n"
    )

    view = process_analysis_brief(raw)
    assert view.has_analysis is True
    assert view.is_unavailable is False
    assert view.lead == "A services-led margin story, priced for perfection and exposed to regulatory changes in key jurisdictions."
    assert "<math" in view.rendered_html
    assert "Supply chain volatility" in view.rendered_html


def test_analysis_brief_unavailable_non_blocking():
    """Verify unavailable state sets friendly notice without crashing or inventing text."""
    view = process_analysis_brief(None, is_unavailable=True, notice="AI service busy")
    assert view.has_analysis is False
    assert view.is_unavailable is True
    assert "AI service busy" in (view.unavailable_notice or "")


def test_analysis_brief_empty():
    """Verify empty or None analysis returns clean empty view."""
    view = process_analysis_brief(None)
    assert view.has_analysis is False
    assert view.lead is None
    assert view.rendered_html == ""


def test_analysis_brief_template_rendering():
    """Verify partials/analysis_brief.html renders correctly."""
    templates = Jinja2Templates(directory="templates")

    view = AnalysisBriefView(
        has_analysis=True,
        is_unavailable=False,
        lead="A services-led margin story, priced for perfection and exposed to regulation.",
        rendered_html="<p>Detailed analysis body with <math display='inline'><mi>x</mi></math></p>",
    )

    html = templates.get_template("partials/analysis_brief.html").render({"analysis_brief": view})

    assert 'id="analysis"' in html
    assert "AI research brief" in html
    assert "Interpretation · not evidence" in html
    assert "A services-led margin story" in html
    assert "<math" in html


def test_analysis_brief_unavailable_template_rendering():
    """Verify partials/analysis_brief.html renders non-blocking unavailable notice."""
    templates = Jinja2Templates(directory="templates")

    view = AnalysisBriefView(
        has_analysis=False,
        is_unavailable=True,
        unavailable_notice="AI interpretation is temporarily unavailable.",
    )

    html = templates.get_template("partials/analysis_brief.html").render({"analysis_brief": view})

    assert 'id="analysis"' in html
    assert "Interpretation · not evidence" in html
    assert "AI interpretation is temporarily unavailable" in html
    assert "The sourced market record remains visible" in html


def test_process_analysis_brief_structured_model():
    """Verify structured fields are extracted from StructuredAnalysis."""
    structured = StructuredAnalysis(
        executive_summary="Reliance continues robust expansion across retail, telecoms and petrochemicals.",
        what_is_happening="Capital expenditure in 5G network rollout is maturing with margin expansion.",
        bullish_factors=["Jio subscriber growth", "Retail footprint expansion", "New energy investments"],
        bearish_factors=["Petrochemical cyclical softness", "High gross debt levels"],
        risks=["Regulatory tariff delays", "Global refining margin compression"],
        catalysts=["Potential retail or telecoms IPO", "Green hydrogen project commissioning"],
        what_to_watch=["ARPU trends in next quarter", "Capex trajectory guidance"],
        market_sentiment="positive",
        confidence="high",
        ai_verdict="Constructive long-term outlook anchored by domestic consumption leadership.",
    )

    view = process_analysis_brief(
        analysis_text="Fallback markdown text",
        structured=structured,
        as_of="2026-11-08 15:30 UTC",
    )

    assert view.has_analysis is True
    assert view.has_structured is True
    assert view.executive_summary == structured.executive_summary
    assert view.what_is_happening == structured.what_is_happening
    assert len(view.bullish_factors) == 3
    assert len(view.bearish_factors) == 2
    assert len(view.risks) == 2
    assert len(view.catalysts) == 2
    assert len(view.what_to_watch) == 2
    assert view.market_sentiment == "positive"
    assert view.confidence == "high"
    assert view.ai_verdict == structured.ai_verdict
    assert view.as_of == "2026-11-08 15:30 UTC"


def test_process_analysis_brief_deep_interpretation():
    """Verify structured mapping handles CompanyDeepAnalysisInterpretation gracefully."""
    deep = CompanyDeepAnalysisInterpretation(
        executive_summary="TCS demonstrates resilient BFSI execution.",
        business_model="Global IT services and digital transformation consulting.",
        growth_drivers=["Cloud migration contracts", "Generative AI enterprise proofs-of-concept"],
        key_risks=["Discretionary tech spend contraction", "Visa regulation updates"],
        catalysts=["Major deal renewals in North America"],
        what_to_watch=["Deal total contract value (TCV)"],
        overall_assessment="High quality market leader with superior operating margins.",
        confidence="medium",
    )

    view = process_analysis_brief(analysis_text=None, structured=deep)

    assert view.has_analysis is True
    assert view.has_structured is True
    assert view.executive_summary == "TCS demonstrates resilient BFSI execution."
    assert view.what_is_happening == "Global IT services and digital transformation consulting."
    assert "Cloud migration contracts" in view.bullish_factors
    assert "Discretionary tech spend contraction" in view.risks
    assert "Major deal renewals in North America" in view.catalysts
    assert "Deal total contract value (TCV)" in view.what_to_watch
    assert view.ai_verdict == "High quality market leader with superior operating margins."
    assert view.confidence == "medium"


def test_analysis_brief_structured_template_rendering():
    """Verify partials/analysis_brief.html renders all redesigned sections."""
    templates = Jinja2Templates(directory="templates")

    view = AnalysisBriefView(
        has_analysis=True,
        has_structured=True,
        is_unavailable=False,
        lead="Reliance Industries delivers balanced growth across telecom and digital commerce.",
        executive_summary="Reliance continues robust expansion across retail, telecoms and petrochemicals.",
        what_is_happening="Capital expenditure in 5G rollout is stabilizing while cash generation increases.",
        bullish_factors=["Jio ARPU expansion", "Consumer retail sales volume up 18%"],
        bearish_factors=["Refining margin moderation", "Finance costs elevated"],
        risks=["Geopolitical crude supply fluctuations", "Tariff intervention risk"],
        catalysts=["Upcoming annual shareholder meeting", "Jio IPO roadmap clarity"],
        what_to_watch=["Quarterly gross margin trends", "Clean energy capacity additions"],
        market_sentiment="positive",
        confidence="high",
        ai_verdict="Long-term overweight with durable competitive moats in Indian consumer markets.",
        as_of="2026-11-08 16:00 UTC",
    )

    context = {
        "analysis_brief": view,
        "company": {"name": "Reliance Industries Limited", "symbol": "RELIANCE.NS"},
    }

    html = templates.get_template("partials/analysis_brief.html").render(context)

    # Header elements
    assert 'id="analysis"' in html
    assert "AI research brief" in html
    assert "Reliance Industries Limited (RELIANCE.NS)" in html
    assert "Interpretation · not evidence" in html
    assert "Retrieved 2026-11-08 16:00 UTC" in html
    assert "Positive" in html
    assert "High confidence" in html
    assert "Reliance Industries delivers balanced growth" in html

    # Structured sections
    assert "Executive Summary" in html
    assert "Reliance continues robust expansion" in html

    assert "What Is Happening" in html
    assert "Capital expenditure in 5G rollout" in html

    assert "Bullish Factors" in html
    assert "Jio ARPU expansion" in html
    assert "Consumer retail sales volume up 18%" in html

    assert "Bearish Factors" in html
    assert "Refining margin moderation" in html
    assert "Finance costs elevated" in html

    assert "Key Risks" in html
    assert "Geopolitical crude supply fluctuations" in html

    assert "Upcoming Catalysts" in html
    assert "Jio IPO roadmap clarity" in html

    assert "What to Watch" in html
    assert "Quarterly gross margin trends" in html

    assert "AI Research Verdict" in html
    assert "Long-term overweight with durable competitive moats" in html
