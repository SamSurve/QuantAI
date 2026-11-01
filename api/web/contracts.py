"""Pydantic presentation and interaction contracts for QuantAI.

Preserves full parity with TypeScript research, market, and AgentOS interfaces.
"""

from __future__ import annotations

import re
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

from api.research_schemas import (
    CompanyComparisonReport,
    CompanyDeepAnalysisReport,
    ErrorCategory,
    MarketSignal as SchemaMarketSignal,
    MarketSnapshot,
    PriceHistoryBundle,
    ResearchResponse,
)

# Canonical aliases matching TypeScript frontend names
TypedResearchResponse = ResearchResponse
MarketPulse = MarketSnapshot
PriceHistory = PriceHistoryBundle
MarketSignal = SchemaMarketSignal
CompanyDeepAnalysis = CompanyDeepAnalysisReport
CompanyComparison = CompanyComparisonReport
ResearchErrorCategory = ErrorCategory

ResearchErrorKind = Literal["ambiguous", "not_found", "ai_unavailable", "news_unavailable", "other"]


def research_error_kind(message: str) -> ResearchErrorKind:
    """Classify safe public error-envelope copy for UI messaging."""
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


class Metric(BaseModel):
    """Evidence Briefing metric token."""

    model_config = ConfigDict(extra="forbid")

    label: str
    value: str
    tone: Literal["neutral", "positive", "negative"] = "neutral"


class ChartPoint(BaseModel):
    """Individual time/value coordinate for client charting."""

    model_config = ConfigDict(extra="forbid")

    label: str
    value: float


class BriefNewsItem(BaseModel):
    """Compact news presentation record."""

    model_config = ConfigDict(extra="forbid")

    title: str
    summary: str | None = None
    publisher: str | None = None
    publishedAt: str | None = None
    url: str | None = None
    sentiment: str | None = None


HistoryPeriod = Literal["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"]


class MarketBriefPriceHistory(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intraday: list[ChartPoint] = Field(default_factory=list)
    daily: list[ChartPoint] = Field(default_factory=list)
    availablePeriods: list[HistoryPeriod] = Field(default_factory=list)
    defaultPeriod: HistoryPeriod = "1M"


class MarketBriefSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    score: str
    confidence: str
    factors: list[str] = Field(default_factory=list)
    explanation: str
    methodology: str


class MarketBriefEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    date: str
    importance: str
    source: str


class MarketBriefSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    url: str | None = None
    dataType: str
    retrievedAt: str


class MarketBriefWarning(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: str
    message: str


class MarketBriefFreshness(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    state: str
    asOf: str


class DeepProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str | None = None
    country: str | None = None
    headquarters: str | None = None
    website: str | None = None
    employees: str | None = None
    fiscalPeriodEnd: str | None = None


class OverviewItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    value: str


class GovernanceBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo: str
    leadership: list[str] = Field(default_factory=list)
    note: str


class CompetitorBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    note: str
    items: list[str] = Field(default_factory=list)


class ValuationBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    classification: str
    rationale: str
    evidence: list[str] = Field(default_factory=list)


class DeepInterpretation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    businessModel: str
    financialHealth: str
    growthDrivers: list[str] = Field(default_factory=list)
    competitivePosition: str
    risks: list[str] = Field(default_factory=list)
    catalysts: list[str] = Field(default_factory=list)
    valuation: ValuationBrief
    recentDevelopments: list[str] = Field(default_factory=list)
    whatToWatch: list[str] = Field(default_factory=list)
    assessment: str
    confidence: str


class DeepAnalysisBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: DeepProfile
    overview: list[OverviewItem] = Field(default_factory=list)
    financials: list[Metric] = Field(default_factory=list)
    governance: GovernanceBrief
    competitors: CompetitorBrief
    interpretation: DeepInterpretation | None = None


class MarketBrief(BaseModel):
    """Complete presentation model corresponding to TypeScript MarketBrief."""

    model_config = ConfigDict(extra="forbid")

    companyName: str
    ticker: str
    exchange: str
    sector: str
    industry: str
    quoteLabel: Literal["Current price", "Latest close"] = "Current price"
    quote: str
    change: str
    metrics: list[Metric] = Field(default_factory=list)
    news: list[BriefNewsItem] = Field(default_factory=list)
    chart: list[ChartPoint] = Field(default_factory=list)
    priceHistory: MarketBriefPriceHistory
    analysis: str
    aiInterpretationNotice: str | None = None
    signal: MarketBriefSignal | None = None
    events: list[MarketBriefEvent] = Field(default_factory=list)
    sources: list[MarketBriefSource] = Field(default_factory=list)
    warnings: list[MarketBriefWarning] = Field(default_factory=list)
    freshness: list[MarketBriefFreshness] = Field(default_factory=list)
    deepAnalysis: DeepAnalysisBrief | None = None


class AgentRunResponse(BaseModel):
    """AgentOS run endpoint response contract."""

    model_config = ConfigDict(extra="ignore")

    run_id: str | None = None
    session_id: str | None = None
    content: str | None = None
    status: str | None = None
    detail: str | None = None


class AgentModelInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    model: str | None = None
    provider: str | None = None


class AgentInfo(BaseModel):
    """AgentOS agent discovery record."""

    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    model: dict[str, Any] | None = None


def friendly_agent_error(value: Any, status: int | None = None) -> str:
    """Port of TypeScript friendlyAgentError logic."""
    message = str(value or "")
    normalized = message.lower()
    if (
        status in {429, 503}
        or re.search(r"temporarily unavailable|rate.?limit|quota|too many requests|service unavailable|overloaded", normalized)
    ):
        return "AI analysis is temporarily unavailable. Please wait a few minutes and try again; the dashboard is ready for your next request."
    if status and status >= 500:
        return "The Research Desk is temporarily unavailable. Please try again shortly."
    if status in {401, 403}:
        return "The Research Desk is unavailable for this session. Please check the configured endpoint."
    if message:
        return f"{message}." if not message.endswith(".") else message
    return f"AgentOS request failed ({status})." if status else "AgentOS request failed."
