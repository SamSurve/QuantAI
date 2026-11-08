"""Web routes, Jinja2 template rendering, and root content negotiation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from api.research_errors import ResearchError
from api.research_schemas import ErrorCategory
from api.web.company_profile import (
    format_company_profile,
    format_competitor_evidence,
    format_governance,
)
from api.web.fundamentals import format_financial_health
from api.web.news import process_news_feed
from api.web.events import process_events_radar
from api.web.evidence import process_evidence_appendix
from api.web.analysis import process_analysis_brief
from api.web.presenters import market_brief_from_research
from api.web.research import classify_research_error, orchestrate_dual_research

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
from api.web.formatters import money_label, compact_money_label, number_label, percent_label
templates.env.filters["money"] = money_label
templates.env.filters["compact_money"] = compact_money_label
templates.env.filters["number"] = number_label
templates.env.filters["percent"] = percent_label

router = APIRouter()


def parse_accept_header(accept: str | None) -> tuple[float, float]:
    """Parse Accept header returning (html_q, json_q).

    Only explicit media ranges 'text/html' and 'application/json' are evaluated.
    Wildcards (*/* or text/*) do not qualify as explicit text/html or application/json.
    """
    if not accept:
        return 0.0, 0.0

    html_q = 0.0
    json_q = 0.0

    for part in accept.split(","):
        part = part.strip()
        if not part:
            continue
        params = [p.strip() for p in part.split(";")]
        media_type = params[0].lower()
        q = 1.0
        for param in params[1:]:
            if param.lower().startswith("q="):
                try:
                    q = float(param[2:].strip())
                except ValueError:
                    q = 0.0
                break
        if media_type == "text/html":
            html_q = max(html_q, q)
        elif media_type == "application/json":
            json_q = max(json_q, q)

    return html_q, json_q


def prefers_html_over_json(accept: str | None) -> bool:
    """Return True only when explicit text/html has strictly higher quality than application/json."""
    html_q, json_q = parse_accept_header(accept)
    if html_q <= 0.0:
        return False
    return html_q > json_q


def render_not_found(request: Request) -> HTMLResponse:
    """Render the server-side 404 template with 404 HTTP status."""
    return templates.TemplateResponse(
        request=request,
        name="pages/not_found.html",
        status_code=404,
    )


def register_web_routes(
    app: FastAPI,
    health_provider: Callable[[], dict[str, Any]],
    research_orchestrator: Any = None,
) -> None:
    """Register server-rendered workspace routes with root content negotiation."""

    @app.get("/", include_in_schema=False)
    async def root_endpoint(request: Request) -> Response:
        accept = request.headers.get("accept")
        if prefers_html_over_json(accept):
            return templates.TemplateResponse(
                request=request,
                name="pages/home.html",
                context={"state": "idle"},
            )
        return JSONResponse(content=health_provider())

    @app.get("/404", include_in_schema=False)
    async def explicit_404_endpoint(request: Request) -> HTMLResponse:
        return render_not_found(request)

    @app.get("/research", include_in_schema=False)
    async def web_research_endpoint(request: Request, query: str = "") -> Response:
        accept = request.headers.get("accept")
        if prefers_html_over_json(accept):
            normalized = query.strip()
            if normalized and research_orchestrator:
                try:
                    req_id = getattr(request.state, "request_id", "web-req")
                    result = await orchestrate_dual_research(normalized, req_id, research_orchestrator)
                    brief = market_brief_from_research(result)
                    deep = result.company_deep_analysis
                    fh = deep.financial_health if deep else None
                    overview = deep.company_overview if deep else None
                    gov = deep.governance if deep else None
                    comp = deep.competitive_evidence if deep else None

                    fundamentals_data = format_financial_health(fh)
                    profile_data = format_company_profile(overview, result.company)
                    governance_data = format_governance(gov)
                    competitors_data = format_competitor_evidence(comp)
                    news_unavail = (result.status.news == "unavailable") if (result and result.status) else False
                    news_feed = process_news_feed(brief.news, is_unavailable=news_unavail)
                    events_unavail = (result.status.events == "unavailable") if (result and result.status) else False
                    events_radar = process_events_radar(brief.events, is_unavailable=events_unavail)

                    is_ai_unavail = (result.status.ai == "unavailable") if (result and result.status) else False
                    ai_text = brief.analysis if (brief and brief.analysis) else None
                    structured_ai = (
                        result.analysis
                        or (result.market_intelligence.executive_brief if result.market_intelligence else None)
                        or (result.company_deep_analysis.analyst_interpretation if result.company_deep_analysis else None)
                    )
                    analysis_as_of = None
                    if result and result.market_intelligence and result.market_intelligence.freshness and result.market_intelligence.freshness.analysis:
                        analysis_as_of = result.market_intelligence.freshness.analysis.retrieved_at
                    elif result and result.company_deep_analysis and result.company_deep_analysis.freshness and result.company_deep_analysis.freshness.analysis:
                        analysis_as_of = result.company_deep_analysis.freshness.analysis.retrieved_at

                    analysis_brief = process_analysis_brief(
                        ai_text,
                        is_unavailable=is_ai_unavail,
                        notice=brief.aiInterpretationNotice if brief else None,
                        structured=structured_ai,
                        as_of=analysis_as_of,
                    )

                    freshness_src = None
                    if result and result.market_intelligence and result.market_intelligence.freshness:
                        freshness_src = result.market_intelligence.freshness
                    elif result and result.company_deep_analysis and result.company_deep_analysis.freshness:
                        freshness_src = result.company_deep_analysis.freshness
                    elif brief and brief.freshness:
                        freshness_src = [(f.label, f.state) for f in brief.freshness]

                    evidence_appendix = process_evidence_appendix(
                        freshness_records=freshness_src,
                        sources=result.sources if result else [],
                        warnings=result.warnings if result else [],
                    )

                    resolved_chart_currency = (
                        brief.priceHistory.currency
                        or (result.company.currency if result.company else None)
                        or (result.market.currency if result.market else None)
                    )
                    chart_payload = {
                        "intraday": [p.model_dump() for p in brief.priceHistory.intraday],
                        "daily": [p.model_dump() for p in brief.priceHistory.daily],
                        "defaultPeriod": brief.priceHistory.defaultPeriod,
                        "currency": resolved_chart_currency,
                    }
                    return templates.TemplateResponse(
                        request=request,
                        name="pages/home.html",
                        context={
                            "query": normalized,
                            "company": result.company,
                            "market": result.market,
                            "brief": brief,
                            "metrics": brief.metrics,
                            "quote_label": brief.quoteLabel,
                            "signal": brief.signal,
                            "fundamentals": fundamentals_data,
                            "analysis_brief": analysis_brief,
                            "profile": profile_data,
                            "governance": governance_data,
                            "competitors": competitors_data,
                            "news_feed": news_feed,
                            "events_radar": events_radar,
                            "evidence_appendix": evidence_appendix,
                            "chart_points": brief.priceHistory.daily,
                            "chart_data_json": json.dumps(chart_payload),
                            "default_period": brief.priceHistory.defaultPeriod,
                            "state": "success" if result.status.overall == "complete" else "partial",
                        },
                    )
                except ResearchError as err:
                    if err.category == ErrorCategory.AMBIGUOUS_ENTITY and err.candidates:
                        formatted_candidates = []
                        for c in err.candidates:
                            raw_ex = (c.exchange or "").upper()
                            display_exchange = "NSE" if raw_ex in {"NSI", "NSE"} else raw_ex
                            raw_type = (c.quote_type or "Equity").title()
                            formatted_candidates.append({
                                "symbol": c.symbol,
                                "name": c.name or c.symbol,
                                "exchange": display_exchange,
                                "quote_type": raw_type,
                            })
                        return templates.TemplateResponse(
                            request=request,
                            name="pages/home.html",
                            context={
                                "query": normalized,
                                "state": "disambiguation",
                                "candidates": formatted_candidates,
                                "candidate_count": len(formatted_candidates),
                            },
                        )
                    return templates.TemplateResponse(
                        request=request,
                        name="pages/home.html",
                        context={
                            "query": normalized,
                            "state": "error",
                            "error_kind": classify_research_error(err.message),
                            "error_message": err.message,
                        },
                    )
            return templates.TemplateResponse(
                request=request,
                name="pages/home.html",
                context={"query": query, "state": "idle"},
            )
        return JSONResponse(status_code=400, content={"message": "Use POST /api/research for JSON API"})
