"""Web research orchestration and error guidance for QuantAI.

Preserves the dual parallel research execution model (Market Intelligence +
Company Deep Analysis) and public error recovery classification.
"""

from __future__ import annotations

import asyncio
import re
from typing import Any

from api.research_errors import ResearchError
from api.research_schemas import (
    ErrorCategory,
    ResearchMode,
    ResearchRequest,
    ResearchResponse,
    ServiceStatus,
)


def classify_research_error(message: str) -> str:
    """Classify error messages into one of five public UI recovery kinds.

    Exact parity with client/src/lib/research.ts researchErrorKind.
    """
    normalized = message.lower()
    if re.search(r"ambiguous|multiple companies match", normalized):
        return "ambiguous"
    if re.search(r"not found|unknown|invalid|no supported listed company", normalized):
        return "not_found"
    if re.search(r"ai analysis is temporarily unavailable|groq service is busy|provider unavailable", normalized):
        return "ai_unavailable"
    if re.search(r"news", normalized):
        return "news_unavailable"
    return "other"


def get_recovery_message(message: str) -> str:
    """Return user-facing recovery guidance based on classified error kind."""
    kind = classify_research_error(message)
    if kind == "ambiguous":
        return "More than one company matched. Try a ticker or a more specific company name."
    if kind == "not_found":
        return "No verified company record was found. Check the spelling or search by ticker."
    if kind == "ai_unavailable":
        return "The sourced research record remains useful, but optional AI interpretation is temporarily unavailable."
    if kind == "news_unavailable":
        return "The research record is available with a missing news source. Other sourced evidence remains visible."
    return "The request could not complete. Check the research endpoint, then try again."


def merge_research_records(
    market: ResearchResponse,
    deep: ResearchResponse | None,
) -> ResearchResponse:
    """Merge Market Intelligence and Company Deep Analysis responses.

    Preserves the TypeScript workspaceResearchRecord merge semantics.
    """
    if deep is None:
        return market

    merged_status = market.status.model_copy()
    if deep.status:
        merged_status.financials = deep.status.financials or merged_status.financials
        merged_status.governance = deep.status.governance or merged_status.governance
        merged_status.competitors = deep.status.competitors or merged_status.competitors

    merged_company = market.company or deep.company
    merged_market = market.market or deep.market
    if merged_market and merged_market.currency is None and merged_company and merged_company.currency:
        merged_market = merged_market.model_copy(update={"currency": merged_company.currency})

    return ResearchResponse(
        request_id=market.request_id,
        query=market.query,
        company=merged_company,
        candidates=market.candidates or deep.candidates,
        market=merged_market,
        history=market.history or deep.history,
        news=market.news if market.news else deep.news,
        analysis=market.analysis or deep.analysis,
        events=market.events if market.events else deep.events,
        sources=[*market.sources, *deep.sources],
        warnings=[*market.warnings, *deep.warnings],
        market_intelligence=market.market_intelligence,
        company_deep_analysis=deep.company_deep_analysis,
        status=merged_status,
    )


async def orchestrate_dual_research(
    query: str,
    request_id: str,
    orchestrator: Any,
) -> ResearchResponse:
    """Execute Market Intelligence and Deep Analysis in parallel.

    Handles partial failures gracefully:
    - If both succeed: merges records.
    - If market succeeds and deep fails: returns market record.
    - If deep succeeds and market fails: returns deep record.
    - If both fail: raises the primary ResearchError.
    """
    market_req = ResearchRequest(
        query=query,
        include_analysis=True,
        mode=ResearchMode.MARKET_INTELLIGENCE,
    )
    deep_req = ResearchRequest(
        query=query,
        include_analysis=False,
        mode=ResearchMode.COMPANY_DEEP_ANALYSIS,
    )

    market_res, deep_res = await asyncio.gather(
        orchestrator.research(request_id, market_req),
        orchestrator.research(request_id, deep_req),
        return_exceptions=True,
    )

    market_ok = isinstance(market_res, ResearchResponse)
    deep_ok = isinstance(deep_res, ResearchResponse)

    if market_ok and deep_ok:
        return merge_research_records(market_res, deep_res)

    if market_ok:
        return market_res

    if deep_ok:
        return deep_res

    # Both failed: propagate the first exception or convert to ResearchError
    if isinstance(market_res, ResearchError):
        raise market_res
    if isinstance(deep_res, ResearchError):
        raise deep_res
    if isinstance(market_res, Exception):
        raise ResearchError(ErrorCategory.INTERNAL_ERROR, str(market_res))
    raise ResearchError(ErrorCategory.DATA_UNAVAILABLE, "Research data unavailable")
