"""Vercel entrypoint for the stateless Groq AgentOS finance research API.

Vercel delivers requests to ``api/index.py`` under the ``/api`` prefix. The
mounted AgentOS app therefore keeps its native ``/agents`` routes while the
public same-origin path becomes ``/api/agents/...``.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from agno.exceptions import ModelProviderError

from .groq_finance_agent import app as agentos_app


app = FastAPI(title="Groq Finance Agent API", docs_url="/api/docs", openapi_url="/api/openapi.json")


@app.exception_handler(ModelProviderError)
async def model_provider_error_handler(_request: Request, error: ModelProviderError) -> JSONResponse:
    """Keep an uncaught Groq provider issue from becoming a raw server error."""
    return JSONResponse(
        status_code=503,
        content={
            "status": "ERROR",
            "detail": (
                "AI analysis is temporarily unavailable because the Groq service is busy or its quota is temporarily exhausted. "
                "Please wait a few minutes and try again."
            ),
            "retryable": True,
        },
    )


@app.get("/api/health", tags=["operations"])
def health() -> dict[str, str]:
    """Return a no-secret readiness response without invoking Groq."""
    return {
        "status": "ok",
        "agent_id": "groq-finance-agent",
        "model": "openai/gpt-oss-120b",
    }


app.mount("/api", agentos_app)
