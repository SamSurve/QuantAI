"""Presentation adapters transforming typed research data into view models."""

from __future__ import annotations

import datetime
import math
from typing import Any, cast

from api.web.contracts import (
    BriefNewsItem,
    ChartPoint,
    CompetitorBrief,
    DeepAnalysisBrief,
    DeepInterpretation,
    DeepProfile,
    GovernanceBrief,
    HistoryPeriod,
    MarketBrief,
    MarketBriefEvent,
    MarketBriefFreshness,
    MarketBriefPriceHistory,
    MarketBriefSignal,
    MarketBriefSource,
    MarketBriefWarning,
    Metric,
    OverviewItem,
    TypedResearchResponse,
    ValuationBrief,
)
from api.web.formatters import (
    compact_money_label,
    format_date,
    money_label,
    number_label,
    percent_label,
    tone_for,
)

METRIC_KEYS = [
    ("Market cap", ["market cap", "market capitalization"]),
    ("P / E ratio", ["p/e", "p/e ratio", "pe ratio", "price to earnings"]),
    ("52-week high", ["52 week high", "52-week high"]),
    ("52-week low", ["52 week low", "52-week low"]),
    ("Volume", ["volume", "avg volume", "average volume"]),
    ("Dividend yield", ["dividend yield"]),
]


def snapshot_metrics_from_market(
    market: MarketSnapshot | None,
    currency: str | None = None,
    market_cap_currency: str | None = None,
    market_cap: float | None = None,
) -> list[Metric]:
    """Generate all seven snapshot metrics with original formatting and fallbacks."""
    mc_curr = market_cap_currency or currency
    resolved_mc = market_cap if market_cap is not None else (market.market_cap if market else None)
    return [
        Metric(
            label="Market cap",
            value=compact_money_label(resolved_mc, mc_curr),
            tone="neutral",
        ),
        Metric(
            label="P / E ratio",
            value=number_label(market.pe_ratio if market else None),
            tone="neutral",
        ),
        Metric(
            label="52-week high",
            value=money_label(market.fifty_two_week_high if market else None, currency),
            tone="neutral",
        ),
        Metric(
            label="52-week low",
            value=money_label(market.fifty_two_week_low if market else None, currency),
            tone="neutral",
        ),
        Metric(
            label="Volume",
            value=number_label(market.volume if market else None, notation="compact"),
            tone="neutral",
        ),
        Metric(
            label="Dividend yield",
            value=(
                percent_label(market.dividend_yield * 100, include_sign=False)
                if (market and market.dividend_yield is not None)
                else "—"
            ),
            tone="neutral",
        ),
        Metric(
            label="EPS",
            value=money_label(market.eps if market else None, currency),
            tone="neutral",
        ),
    ]


PERIOD_DAYS: dict[str, int] = {
    "1W": 7,
    "1M": 31,
    "3M": 92,
    "6M": 184,
    "1Y": 366,
}


def _parse_ts(ts_str: str) -> float:
    try:
        clean = ts_str.strip()
        if clean.endswith("Z"):
            clean = clean[:-1] + "+00:00"
        if len(clean) == 10 and clean.count("-") == 2:
            clean = clean + "T00:00:00+00:00"
        dt = datetime.datetime.fromisoformat(clean)
        return dt.timestamp()
    except Exception:
        try:
            return float(ts_str)
        except Exception:
            return 0.0


def slice_period_series(
    intraday: list[ChartPoint],
    daily: list[ChartPoint],
    period: str,
) -> list[ChartPoint]:
    """Slice price history client/server side matching TypeScript periodSeries."""
    if period == "1D":
        return intraday
    if not daily:
        return []
    if period == "5Y":
        return daily

    days = PERIOD_DAYS.get(period)
    if days is None:
        return daily

    latest_ts = _parse_ts(daily[-1].label)
    cutoff = latest_ts - (days * 24 * 60 * 60)
    return [p for p in daily if _parse_ts(p.label) >= cutoff]


def calculate_performance_summary(
    series: list[ChartPoint] | list[dict[str, Any]],
) -> dict[str, float] | None:
    """Calculate low, high, and percentage change over series."""
    if len(series) < 2:
        return None

    def get_val(item: Any) -> float:
        if isinstance(item, dict):
            return float(item.get("value", 0.0))
        return float(getattr(item, "value", 0.0))

    values = [get_val(p) for p in series]
    first = values[0]
    last = values[-1]
    if first == 0 or not math.isfinite(first) or not math.isfinite(last):
        return None

    low = min(values)
    high = max(values)
    change = ((last - first) / first) * 100.0
    return {"low": low, "high": high, "change": change}


def empty_market_brief() -> MarketBrief:
    """Return default empty MarketBrief structure awaiting research."""
    return MarketBrief(
        companyName="—",
        ticker="—",
        exchange="—",
        sector="—",
        industry="—",
        quoteLabel="Current price",
        quote="—",
        change="Awaiting AgentOS research",
        metrics=[Metric(label=label, value="—", tone="neutral") for label, _ in METRIC_KEYS],
        news=[],
        chart=[],
        priceHistory=MarketBriefPriceHistory(intraday=[], daily=[], availablePeriods=[], defaultPeriod="1M"),
        analysis="",
        aiInterpretationNotice=None,
        signal=None,
        events=[],
        sources=[],
        warnings=[],
        freshness=[],
        deepAnalysis=None,
    )


def typed_analysis_markdown(research: TypedResearchResponse) -> str:
    """Render executive brief analysis into editorial Markdown."""
    deep = research.company_deep_analysis.analyst_interpretation if research.company_deep_analysis else None
    if deep:
        def section(heading: str, values: list[str]) -> str:
            if not values:
                return ""
            items = "\n".join(f"- {v}" for v in values)
            return f"\n\n## {heading}\n{items}"

        val_view = deep.valuation_view
        val_str = ""
        if val_view:
            val_str = f"\n\n## Valuation View — Analyst Interpretation\n{val_view.classification}"
            if val_view.rationale:
                val_str += f" · {val_view.rationale}"

        parts = [
            f"## Executive Assessment\n{deep.executive_summary}" if deep.executive_summary else "",
            f"\n\n## Business Model\n{deep.business_model}" if deep.business_model else "",
            f"\n\n## Financial Health\n{deep.financial_health}" if deep.financial_health else "",
            section("Growth Drivers", deep.growth_drivers),
            f"\n\n## Competitive Position\n{deep.competitive_position}" if deep.competitive_position else "",
            section("Key Risks — Analyst Interpretation", deep.key_risks),
            section("Catalysts", deep.catalysts),
            val_str,
            section("Recent Developments", deep.recent_developments),
            section("What to Watch", deep.what_to_watch),
            f"\n\n## Overall Assessment\n{deep.overall_assessment}" if deep.overall_assessment else "",
        ]
        return "\n".join(p for p in parts if p).strip()

    analysis = (
        research.market_intelligence.executive_brief
        if research.market_intelligence and research.market_intelligence.executive_brief
        else research.analysis
    )
    if not analysis:
        return ""

    def section(heading: str, values: list[str]) -> str:
        if not values:
            return ""
        items = "\n".join(f"- {v}" for v in values)
        return f"\n\n## {heading}\n{items}"

    parts = [
        f"## Executive Summary\n{analysis.executive_summary}" if analysis.executive_summary else "",
        f"\n\n## What is happening\n{analysis.what_is_happening}" if analysis.what_is_happening else "",
        section("Bullish Factors", analysis.bullish_factors),
        section("Bearish Factors", analysis.bearish_factors),
        section("Risks", analysis.risks),
        section("Catalysts", analysis.catalysts),
        section("What to Watch", analysis.what_to_watch or []),
        f"\n\n## Market Sentiment\n{analysis.market_sentiment}" if analysis.market_sentiment else "",
        f"\n\n## AI Verdict\n{analysis.ai_verdict}" if analysis.ai_verdict else "",
    ]
    return "\n".join(p for p in parts if p).strip()


def market_brief_from_research(research: TypedResearchResponse) -> MarketBrief:
    """Build unified presentation model from research response."""
    intelligence = research.market_intelligence
    deep = research.company_deep_analysis

    market = (
        (intelligence.market_pulse if intelligence else None)
        or (deep.market_context if deep else None)
        or research.market
    )

    market_cap = (
        (market.market_cap if market else None)
        or (research.market.market_cap if research.market else None)
        or (deep.market_context.market_cap if deep and deep.market_context else None)
        or (deep.company_overview.market_cap if deep and deep.company_overview else None)
    )

    market_cap_currency = (
        (market.currency if market else None)
        or (research.market.currency if research.market else None)
        or (deep.market_context.currency if deep and deep.market_context else None)
        or (deep.company_overview.currency if deep and deep.company_overview else None)
        or (research.company.currency if research.company else None)
    )

    currency = research.company.currency if research.company else None
    price_history = intelligence.price_history if intelligence else None

    raw_daily = price_history.daily if price_history else research.history
    raw_intraday = price_history.intraday if price_history else []

    daily_points = [
        ChartPoint(label=p.timestamp, value=p.close)
        for p in raw_daily
        if p.close is not None
    ]
    intraday_points = [
        ChartPoint(label=p.timestamp, value=p.close)
        for p in raw_intraday
        if p.close is not None
    ]

    change = market.daily_change_percent if market else None
    change_str = percent_label(change, include_sign=True) if change is not None else "—"

    deterministic_evidence = bool(
        market
        or research.news
        or research.events
        or (deep and (deep.company_overview or deep.financial_health))
        or (intelligence and intelligence.price_history)
    )

    ai_notice = None
    if research.status.ai == "unavailable":
        ai_notice = (
            "Market data and evidence are available. AI interpretation is temporarily unavailable."
            if deterministic_evidence
            else "AI interpretation is temporarily unavailable; no deterministic evidence was returned for this request."
        )

    # Metric tokens
    metrics: list[Metric] = snapshot_metrics_from_market(
        market,
        currency=currency,
        market_cap_currency=market_cap_currency,
        market_cap=market_cap,
    )

    # News items
    raw_news = (
        (intelligence.recent_news if intelligence else None)
        or (deep.recent_news if deep else None)
        or research.news
    )
    news_items = [
        BriefNewsItem(
            title=item.title,
            summary=item.summary.strip() if item.summary else None,
            publisher=item.publisher,
            publishedAt=item.published_at,
            url=item.url,
            sentiment=item.sentiment,
        )
        for item in raw_news
    ]

    # Signal
    sig_model = None
    sig = intelligence.market_signal if intelligence else None
    if sig is None and raw_daily and len([p for p in raw_daily if p.close is not None]) >= 21:
        from api.market_intelligence_services import calculate_market_signal
        sig = calculate_market_signal(raw_daily)

    if sig:
        score_str = f"{sig.score}/100" if sig.score is not None else "—"
        conf_str = f"{sig.confidence}/100" if sig.confidence is not None else "—"
        sig_model = MarketBriefSignal(
            label=sig.signal or "UNAVAILABLE",
            score=score_str,
            confidence=conf_str,
            factors=sig.factors,
            explanation=sig.explanation or "Deterministic signal data is unavailable.",
            methodology=sig.methodology,
        )

    # Events
    raw_events = (
        (intelligence.event_radar if intelligence else None)
        or (deep.events if deep else None)
        or research.events
    )
    event_items = [
        MarketBriefEvent(
            title=e.title,
            date=format_date(e.date),
            importance=e.importance,
            source=e.source or "Source unavailable",
        )
        for e in raw_events
    ]

    # Sources
    source_items = [
        MarketBriefSource(
            source=s.source,
            url=s.url,
            dataType=s.data_type,
            retrievedAt=s.retrieved_at,
        )
        for s in research.sources
    ]

    # Warnings
    warning_items = [
        MarketBriefWarning(category=w.category.value, message=w.message)
        for w in research.warnings
    ]

    # Freshness
    freshness_items: list[MarketBriefFreshness] = []
    if intelligence:
        for lbl, rec in intelligence.freshness:
            freshness_items.append(
                MarketBriefFreshness(
                    label=lbl,
                    state=rec.state.value,
                    asOf=rec.as_of or rec.retrieved_at or "Unavailable",
                )
            )
    elif deep:
        for lbl, rec in deep.freshness:
            freshness_items.append(
                MarketBriefFreshness(
                    label=lbl,
                    state=rec.state.value,
                    asOf=rec.as_of or rec.retrieved_at or "Unavailable",
                )
            )

    # Deep Analysis Brief
    deep_brief = None
    if deep:
        deep_overview: list[OverviewItem] = []
        ov = deep.company_overview
        if ov:
            fields = [
                ("Company", ov.company_name),
                ("Ticker", ov.ticker),
                ("Exchange", ov.exchange),
                ("Sector", ov.sector),
                ("Industry", ov.industry),
                ("Country", ov.country),
                ("Headquarters", ov.headquarters),
                ("Employees", number_label(ov.employees) if ov.employees is not None else None),
                ("Website", ov.website),
            ]
            for lbl, val in fields:
                if val:
                    deep_overview.append(OverviewItem(label=lbl, value=str(val)))

        fh = deep.financial_health
        deep_financials = [
            Metric(label="Revenue", value=compact_money_label(fh.revenue if fh else None, fh.currency if fh else None)),
            Metric(label="Net income", value=compact_money_label(fh.net_income if fh else None, fh.currency if fh else None)),
            Metric(label="EPS", value=money_label(fh.eps if fh else None, fh.currency if fh else None)),
            Metric(label="Profit margin", value=percent_label(fh.profit_margin * 100 if fh and fh.profit_margin is not None else None, include_sign=False)),
            Metric(label="Free cash flow", value=compact_money_label(fh.free_cash_flow if fh else None, fh.currency if fh else None)),
            Metric(label="Total cash", value=compact_money_label(fh.total_cash if fh else None, fh.currency if fh else None)),
            Metric(label="Total debt", value=compact_money_label(fh.total_debt if fh else None, fh.currency if fh else None)),
            Metric(label="Operating margin", value=percent_label(fh.operating_margin * 100 if fh and fh.operating_margin is not None else None, include_sign=False)),
            Metric(label="P / Sales", value=number_label(fh.price_to_sales if fh else None)),
            Metric(label="ROE", value=percent_label(fh.return_on_equity * 100 if fh and fh.return_on_equity is not None else None, include_sign=False)),
            Metric(label="ROA", value=percent_label(fh.return_on_assets * 100 if fh and fh.return_on_assets is not None else None, include_sign=False)),
        ]

        gov = deep.governance
        ceo_str = " · ".join(filter(None, [gov.ceo.name, gov.ceo.title])) if gov and gov.ceo else "Insufficient verified data."
        leadership_items = (
            [" · ".join(filter(None, [p.name, p.title])) for p in gov.key_leadership]
            if gov and gov.key_leadership
            else []
        )
        gov_note = " ".join(gov.notable_developments) if gov and gov.notable_developments else "No sourced management-change assertion is shown."

        interp_brief = None
        if deep.analyst_interpretation:
            interp = deep.analyst_interpretation
            interp_brief = DeepInterpretation(
                businessModel=interp.business_model or "Insufficient verified data.",
                financialHealth=interp.financial_health or "Insufficient verified data.",
                growthDrivers=interp.growth_drivers,
                competitivePosition=interp.competitive_position or "Insufficient verified data.",
                risks=interp.key_risks,
                catalysts=interp.catalysts,
                valuation=ValuationBrief(
                    classification=interp.valuation_view.classification,
                    rationale=interp.valuation_view.rationale or "Insufficient verified data.",
                    evidence=interp.valuation_view.evidence,
                ),
                recentDevelopments=interp.recent_developments,
                whatToWatch=interp.what_to_watch,
                assessment=interp.overall_assessment or "Insufficient verified data.",
                confidence=interp.confidence or "Unavailable",
            )

        deep_brief = DeepAnalysisBrief(
            profile=DeepProfile(
                description=ov.business_description if ov else None,
                country=ov.country if ov else None,
                headquarters=ov.headquarters if ov else None,
                website=ov.website if ov else None,
                employees=number_label(ov.employees) if ov and ov.employees is not None else None,
                fiscalPeriodEnd=fh.fiscal_period_end if fh else None,
            ),
            overview=deep_overview,
            financials=deep_financials,
            governance=GovernanceBrief(ceo=ceo_str, leadership=leadership_items, note=gov_note),
            competitors=CompetitorBrief(note=deep.competitive_evidence.note, items=deep.competitive_evidence.competitors),
            interpretation=interp_brief,
        )

    avail_periods = cast(
        list[HistoryPeriod],
        [p.value for p in price_history.available_periods] if price_history else [],
    )
    def_period = cast(
        HistoryPeriod,
        price_history.default_period.value if price_history else "1M",
    )

    quote_label = "Latest close" if (market and market.market_status == "HISTORY_CLOSE_FALLBACK") else "Current price"

    return MarketBrief(
        companyName=research.company.name if research.company and research.company.name else "—",
        ticker=research.company.symbol if research.company else "—",
        exchange=research.company.exchange if research.company and research.company.exchange else "—",
        sector=research.company.sector if research.company and research.company.sector else "—",
        industry=research.company.industry if research.company and research.company.industry else "—",
        quoteLabel=quote_label,
        quote=money_label(market.current_price if market else None, currency),
        change=change_str,
        metrics=metrics,
        news=news_items,
        chart=daily_points[-60:],
        priceHistory=MarketBriefPriceHistory(
            intraday=intraday_points,
            daily=daily_points,
            availablePeriods=avail_periods,
            defaultPeriod=def_period,
        ),
        analysis=typed_analysis_markdown(research),
        aiInterpretationNotice=ai_notice,
        signal=sig_model,
        events=event_items,
        sources=source_items,
        warnings=warning_items,
        freshness=freshness_items,
        deepAnalysis=deep_brief,
    )
