"""Web routes, Jinja2 template rendering, and root content negotiation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

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


def register_web_routes(app: FastAPI, health_provider: Callable[[], dict[str, Any]]) -> None:
    """Register server-rendered workspace routes with root content negotiation."""

    @app.get("/", include_in_schema=False)
    async def root_endpoint(request: Request) -> Response:
        accept = request.headers.get("accept")
        if prefers_html_over_json(accept):
            return templates.TemplateResponse(
                request=request,
                name="pages/home.html",
                context={},
            )
        return JSONResponse(content=health_provider())

    @app.get("/404", include_in_schema=False)
    async def explicit_404_endpoint(request: Request) -> HTMLResponse:
        return render_not_found(request)

    @app.get("/research", include_in_schema=False)
    async def web_research_endpoint(request: Request, query: str = "") -> Response:
        accept = request.headers.get("accept")
        if prefers_html_over_json(accept):
            return templates.TemplateResponse(
                request=request,
                name="pages/home.html",
                context={"query": query},
            )
        return JSONResponse(status_code=400, content={"message": "Use POST /api/research for JSON API"})
