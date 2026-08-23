"""
Groq-powered AgentOS finance research service.

The service resolves company names and ticker symbols through Yahoo Finance at run time,
then asks the model to combine real YFinance and web/news tool output into a sourced brief.
No market values are stored or simulated in this module.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
import re
import time
from typing import Any

import yfinance as yf
from agno.agent import Agent
from agno.exceptions import ModelProviderError
from agno.models.groq import Groq
from agno.os import AgentOS
from agno.tools.duckduckgo import DuckDuckGoTools
from ddgs import DDGS
from dotenv import load_dotenv


load_dotenv()


class ResilientGroq(Groq):
    """Apply bounded backoff and clean errors for temporary Groq provider failures."""

    retry_attempts = 2
    retry_delays = (1.0, 2.0)

    @staticmethod
    def _is_quota_exhaustion(error: ModelProviderError) -> bool:
        message = str(error).lower()
        return any(marker in message for marker in ("quota", "tokens per day", "tokens per minute", "billing"))

    def _can_retry(self, error: ModelProviderError) -> bool:
        if self._is_quota_exhaustion(error):
            return False
        status = getattr(error, "status_code", 0)
        message = str(error).lower()
        return status in {429, 500, 502, 503, 504, 529} or any(
            marker in message for marker in ("rate limit", "temporarily unavailable", "timeout", "overloaded")
        )

    def _temporary_unavailability(self, error: ModelProviderError) -> ModelProviderError:
        return ModelProviderError(
            message=(
                "AI analysis is temporarily unavailable because the Groq service is busy or its quota is temporarily exhausted. "
                "Please wait a few minutes and try again. Your dashboard and live market-data tools remain available."
            ),
            status_code=503,
            model_name=self.name,
            model_id=self.id,
        )

    def invoke(self, *args: Any, **kwargs: Any) -> Any:
        for attempt in range(self.retry_attempts + 1):
            try:
                return super().invoke(*args, **kwargs)
            except ModelProviderError as error:
                if not self._can_retry(error) or attempt == self.retry_attempts:
                    if self._can_retry(error) or self._is_quota_exhaustion(error):
                        raise self._temporary_unavailability(error) from error
                    raise
                time.sleep(self.retry_delays[attempt])
        raise RuntimeError("Unreachable Groq retry state.")

    async def ainvoke(self, *args: Any, **kwargs: Any) -> Any:
        for attempt in range(self.retry_attempts + 1):
            try:
                return await super().ainvoke(*args, **kwargs)
            except ModelProviderError as error:
                if not self._can_retry(error) or attempt == self.retry_attempts:
                    if self._can_retry(error) or self._is_quota_exhaustion(error):
                        raise self._temporary_unavailability(error) from error
                    raise
                await asyncio.sleep(self.retry_delays[attempt])
        raise RuntimeError("Unreachable Groq retry state.")


def _json_value(value: Any) -> Any:
    """Convert provider values to JSON-safe primitives without manufacturing missing data."""
    if value is None:
        return None
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)):
        return value
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass
    return str(value)


def resolve_company_and_market_data(query: str) -> dict[str, Any]:
    """
    Resolve a company name or ticker using Yahoo Finance and return a compact, live research record.

    Use this tool first for every company or ticker query. It supports exchange-qualified
    symbols such as RELIANCE.NS and TCS.NS. If no supported listed result is found, return
    the error field to the user rather than guessing a ticker.
    """
    cleaned_query = (query or "").strip()
    if not cleaned_query:
        return {"error": "Please provide a company name or ticker symbol."}

    candidates: list[dict[str, Any]] = []
    try:
        search = yf.Search(
            cleaned_query,
            max_results=8,
            news_count=0,
            lists_count=0,
            include_cb=False,
            raise_errors=False,
        )
        candidates = [
            {
                "symbol": item.get("symbol"),
                "name": item.get("longname") or item.get("shortname"),
                "exchange": item.get("exchange"),
                "quote_type": item.get("quoteType"),
            }
            for item in search.quotes
            if item.get("symbol") and item.get("quoteType") in {"EQUITY", "ETF", "MUTUALFUND"}
        ]
    except Exception as error:
        search_error = str(error)
    else:
        search_error = None

    if not candidates:
        try:
            fuzzy_search = yf.Search(
                cleaned_query,
                max_results=8,
                news_count=0,
                lists_count=0,
                include_cb=False,
                enable_fuzzy_query=True,
                raise_errors=False,
            )
            candidates = [
                {
                    "symbol": item.get("symbol"),
                    "name": item.get("longname") or item.get("shortname"),
                    "exchange": item.get("exchange"),
                    "quote_type": item.get("quoteType"),
                }
                for item in fuzzy_search.quotes
                if item.get("symbol") and item.get("quoteType") in {"EQUITY", "ETF", "MUTUALFUND"}
            ]
        except Exception as error:
            search_error = search_error or str(error)

    normalized_query = cleaned_query.upper().replace(" ", "")
    direct_symbols = [candidate for candidate in candidates if candidate["symbol"].upper() == normalized_query]
    stem_symbols = [
        candidate
        for candidate in candidates
        if candidate["symbol"].upper().split(".")[0] == normalized_query
    ]
    selected = direct_symbols[0] if direct_symbols else (stem_symbols[0] if stem_symbols else (candidates[0] if candidates else None))

    # Yahoo Finance searches can occasionally omit exchange-qualified symbols. Preserve a
    # clearly supplied symbol as a provider-validated fallback, not a static company map.
    explicit_symbol = bool(re.fullmatch(r"[A-Z0-9.-]{1,12}", cleaned_query))
    if selected is None and explicit_symbol:
        selected = {"symbol": normalized_query, "name": None, "exchange": None, "quote_type": "EQUITY"}

    if selected is None:
        return {
            "error": f"No supported listed company or ticker was found for '{cleaned_query}'.",
            "query": cleaned_query,
            "candidates": candidates,
            "provider_note": search_error,
        }

    symbol = selected["symbol"]
    ticker = yf.Ticker(symbol)
    try:
        info = ticker.info or {}
        history = ticker.history(period="1mo", interval="1d", auto_adjust=False)
    except Exception as error:
        return {
            "error": f"Yahoo Finance could not retrieve market data for '{symbol}'.",
            "query": cleaned_query,
            "resolved_symbol": symbol,
            "provider_note": str(error),
            "candidates": candidates,
        }

    if not info and history.empty:
        return {
            "error": f"No live market data was returned for '{symbol}'. Verify the exchange-qualified symbol.",
            "query": cleaned_query,
            "resolved_symbol": symbol,
            "candidates": candidates,
        }

    latest_price = None
    day_change = None
    if not history.empty:
        closes = history["Close"].dropna()
        if not closes.empty:
            latest_price = _json_value(closes.iloc[-1])
            if len(closes) > 1 and closes.iloc[-2] != 0:
                day_change = _json_value(((closes.iloc[-1] / closes.iloc[-2]) - 1) * 100)

    price_history = []
    if not history.empty:
        for index, row in history.tail(15).iterrows():
            price_history.append(
                {
                    "date": index.date().isoformat() if hasattr(index, "date") else str(index),
                    "close": _json_value(row.get("Close")),
                }
            )

    company_name = info.get("longName") or info.get("shortName") or selected.get("name")
    if not company_name and latest_price is None and not price_history:
        return {
            "error": f"No live market data was returned for '{symbol}'. Verify the exchange-qualified symbol.",
            "query": cleaned_query,
            "resolved_symbol": symbol,
            "candidates": candidates,
            "provider_note": info.get("description") if isinstance(info, dict) else None,
        }

    market_record = {
        "query": cleaned_query,
        "resolved_symbol": symbol,
        "company_name": company_name,
        "exchange": info.get("exchange") or selected.get("exchange"),
        "currency": info.get("currency"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "current_price": latest_price or info.get("currentPrice") or info.get("regularMarketPrice"),
        "day_change_percent": day_change,
        "market_cap": info.get("marketCap"),
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "volume": info.get("regularMarketVolume") or info.get("volume"),
        "average_volume": info.get("averageVolume"),
        "dividend_yield": info.get("dividendYield"),
        "price_history": price_history,
        "as_of": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "source": "Yahoo Finance via yfinance",
        "candidates": candidates[:5],
    }
    return {key: _json_value(value) for key, value in market_record.items()}


def search_recent_news(query: str) -> dict[str, Any]:
    """
    Search current news for a resolved company or ticker using DDGS.

    Use this tool after resolve_company_and_market_data with the resolved company name
    and ticker. The returned records retain only provider-supplied title, URL, source,
    date, and a short body excerpt so the research prompt remains within model limits.
    """
    cleaned_query = (query or "").strip()
    if not cleaned_query:
        return {"error": "Provide a company name or ticker for the news search."}
    try:
        results = DDGS(timeout=15).news(cleaned_query, max_results=3)
    except Exception as error:
        return {"error": f"No current news search result was available: {error}"}

    items = []
    for result in results[:3]:
        items.append(
            {
                "title": result.get("title"),
                "url": result.get("url"),
                "source": result.get("source"),
                "date": result.get("date"),
                "body": (result.get("body") or "")[:160],
            }
        )
    return {"query": cleaned_query, "source": "DDGS news search", "items": items}


agent = Agent(
    name="Groq Finance Agent",
    model=ResilientGroq(id="openai/gpt-oss-120b", max_tokens=1600, temperature=0.2, max_retries=0),
    tools=[
        resolve_company_and_market_data,
        search_recent_news,
        DuckDuckGoTools(enable_news=False),
    ],
    instructions=[
        "For every company or ticker research request, call resolve_company_and_market_data first. Never guess a ticker from the company name.",
        "If the resolver returns an error, explain the problem plainly, show only provider-returned candidates if available, and ask for a ticker or exchange-qualified symbol. Do not fabricate a match.",
        "After a successful resolution, call search_recent_news once using the resolved company name and ticker. You may use web_search only when needed for context; do not call additional finance-data tools because the resolver already returns the complete live market record.",
        "Use the resolved ticker for all subsequent web searches. For Indian companies, retain supported suffixes such as .NS or .BO.",
        "Return markdown using these sections exactly: ## Market Snapshot, ## Price History, ## Recent News, ## Analysis, and ## Sources.",
        "In Market Snapshot, use a two-column markdown table with Company Name, Ticker, Exchange, Sector, Industry, Current Price, Day Change, Market Cap, Trailing P/E, 52-Week High, 52-Week Low, Volume, and Dividend Yield whenever the live source provides them. Mark unavailable source fields as Unavailable.",
        "In Price History, provide a dated two-column markdown table named Date and Close from the resolver record whenever it contains price_history; otherwise state why no chart data is available.",
        "In Recent News, provide at least two current, relevant, source-linked bullet points from search_recent_news when it returns items; otherwise say that no current sourced news was returned.",
        "Separate sourced facts from interpretation. Do not invent metrics, dates, prices, company details, or news. Conclude analysis with key catalysts and risks, not a personalized investment recommendation.",
    ],
    debug_mode=False,
    markdown=True,
)

agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()


if __name__ == "__main__":
    agent_os.serve(app="groq_finance_agent:app", reload=True)
