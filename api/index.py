"""Vercel entrypoint for the stateless QuantAI AgentOS finance research API.

Vercel delivers requests to ``api/index.py`` under the ``/api`` prefix. The
mounted AgentOS app therefore keeps its native ``/agents`` routes while the
public same-origin path becomes ``/api/agents/...``.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from agno.exceptions import ModelProviderError

from .groq_finance_agent import app as agentos_app
from .groq_finance_agent import provider_router
from .ai_providers import provider_runtime_status
from .research_errors import ResearchError
from .research_orchestrator import AnalysisSynthesisService, ResearchOrchestrator
from .research_protection import ResearchConcurrencyGuard, SlidingWindowRateLimiter
from .research_schemas import ErrorCategory, ErrorResponse, ResearchRequest, ResearchResponse
from .web.routes import prefers_html_over_json, register_web_routes, render_not_found

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"

app = FastAPI(title="QuantAI Finance Agent API", docs_url="/api/docs", openapi_url="/api/openapi.json")
LOGGER = logging.getLogger("quantai.api")
MAX_RESEARCH_REQUEST_BYTES = 8_192
MAX_AGENTOS_RUN_REQUEST_BYTES = 8_192
research_orchestrator = ResearchOrchestrator(analysis_service=AnalysisSynthesisService(provider_router))
research_rate_limiter = SlidingWindowRateLimiter(limit=10, window_seconds=60)
research_concurrency_guard = ResearchConcurrencyGuard(max_concurrent=4)
agentos_rate_limiter = SlidingWindowRateLimiter(limit=10, window_seconds=60)
agentos_concurrency_guard = ResearchConcurrencyGuard(max_concurrent=4)


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", str(uuid4()))


def _client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    return forwarded or (request.client.host if request.client else "unknown")


def _error_response(request: Request, error: ResearchError) -> JSONResponse:
    return JSONResponse(
        status_code=error.status_code,
        content=ErrorResponse(
            request_id=_request_id(request),
            category=error.category,
            message=error.message,
            retryable=error.retryable,
        ).model_dump(mode="json"),
    )


@app.middleware("http")
async def request_context_and_body_limit(request: Request, call_next: Any) -> Response:
    request.state.request_id = request.headers.get("x-request-id") or str(uuid4())
    typed_research_path = request.url.path in {"/api/research", "/research"}
    agentos_run_path = request.method == "POST" and request.url.path in {
        "/api/agents/groq-finance-agent/runs",
        "/agents/groq-finance-agent/runs",
    }
    if typed_research_path or agentos_run_path:
        request_limit = MAX_RESEARCH_REQUEST_BYTES if typed_research_path else MAX_AGENTOS_RUN_REQUEST_BYTES
        content_length = request.headers.get("content-length")
        if content_length and content_length.isdigit() and int(content_length) > request_limit:
            return _error_response(
                request,
                ResearchError(ErrorCategory.VALIDATION_ERROR, detail="request body too large"),
            )
        if len(await request.body()) > request_limit:
            return _error_response(
                request,
                ResearchError(ErrorCategory.VALIDATION_ERROR, detail="request body too large"),
            )
    if agentos_run_path:
        await agentos_rate_limiter.check(_client_key(request))
        async with agentos_concurrency_guard.acquire():
            response = await call_next(request)
    else:
        response = await call_next(request)

    # Browser 404 content negotiation for responses that return 404
    if response.status_code == 404:
        accept = request.headers.get("accept")
        if prefers_html_over_json(accept) and not request.url.path.startswith("/api"):
            html_resp = render_not_found(request)
            html_resp.headers["X-Request-ID"] = request.state.request_id
            return html_resp

    response.headers["X-Request-ID"] = request.state.request_id
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> Response:
    if exc.status_code == 404:
        accept = request.headers.get("accept")
        if prefers_html_over_json(accept) and not request.url.path.startswith("/api"):
            return render_not_found(request)
        return JSONResponse(
            status_code=404,
            content={
                "request_id": _request_id(request),
                "category": ErrorCategory.ENTITY_NOT_FOUND.value,
                "message": "Resource not found",
                "retryable": False,
            },
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(ModelProviderError)
async def model_provider_error_handler(_request: Request, error: ModelProviderError) -> JSONResponse:
    """Keep an uncaught provider issue from becoming a raw server error."""
    return JSONResponse(
        status_code=503,
        content={
            "status": "ERROR",
            "detail": "AI analysis is temporarily unavailable. Please try again shortly.",
            "retryable": True,
        },
    )


@app.exception_handler(ResearchError)
async def research_error_handler(request: Request, error: ResearchError) -> JSONResponse:
    LOGGER.info("research_error request_id=%s category=%s retryable=%s", _request_id(request), error.category.value, error.retryable)
    return _error_response(request, error)


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, error: RequestValidationError) -> JSONResponse:
    LOGGER.info("request_validation_error request_id=%s errors=%s", _request_id(request), len(error.errors()))
    return _error_response(request, ResearchError(ErrorCategory.VALIDATION_ERROR, detail="request validation failed"))


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, error: Exception) -> JSONResponse:
    LOGGER.exception("unhandled_api_error request_id=%s type=%s", _request_id(request), type(error).__name__)
    return _error_response(request, ResearchError(ErrorCategory.INTERNAL_ERROR, detail=type(error).__name__))


def health_payload() -> dict[str, Any]:
    """Return a no-secret readiness response without invoking Groq."""
    return {
        "status": "ok",
        "agent_id": "groq-finance-agent",
        "model": "quantai-provider-engine",
        "provider_runtime": provider_runtime_status(provider_router),
        "typed_research": {
            "path": "/api/research",
            "request_limit_bytes": MAX_RESEARCH_REQUEST_BYTES,
            "anonymous_rate_limit": "10 requests per 60 seconds per warm instance",
            "cache": "process-local TTL cache; not shared across Vercel instances",
        },
        "agentos_runs": {
            "path": "/api/agents/groq-finance-agent/runs",
            "request_limit_bytes": MAX_AGENTOS_RUN_REQUEST_BYTES,
            "anonymous_rate_limit": "10 requests per 60 seconds per warm instance",
        },
    }


@app.get("/api", tags=["operations"])
@app.get("/api/health", tags=["operations"])
def prefixed_health() -> dict[str, Any]:
    return health_payload()


@app.get("/health", include_in_schema=False)
def prefix_stripped_health() -> dict[str, Any]:
    """Support Vercel function adapters that strip the function's `/api` prefix."""
    return health_payload()


# Register root content negotiation and web routes
register_web_routes(app, health_payload, research_orchestrator=research_orchestrator)


@app.post("/api/research", response_model=ResearchResponse, responses={
    404: {"model": ErrorResponse},
    409: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    429: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
    503: {"model": ErrorResponse},
    504: {"model": ErrorResponse},
})
async def typed_research(request: Request, payload: ResearchRequest) -> ResearchResponse:
    """Return deterministic market/news data plus best-effort typed AI interpretation."""
    await research_rate_limiter.check(_client_key(request))
    async with research_concurrency_guard.acquire():
        return await research_orchestrator.research(_request_id(request), payload)


@app.post("/research", response_model=ResearchResponse, include_in_schema=False)
async def typed_research_prefix_stripped(request: Request, payload: ResearchRequest) -> ResearchResponse:
    """Adapter fallback for function environments that remove the `/api` prefix."""
    await research_rate_limiter.check(_client_key(request))
    async with research_concurrency_guard.acquire():
        return await research_orchestrator.research(_request_id(request), payload)


# Mount static assets directory
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.mount("/api", agentos_app)
# Vercel's Python adapters normally preserve `/api`, but the fallback mount also
# serves AgentOS when a function adapter forwards `/api/agents` as `/agents`.
app.mount("", agentos_app)
