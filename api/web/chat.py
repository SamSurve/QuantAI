"""AgentOS chat rendering endpoint, size/rate limiting, and error normalization.

Per Correction 3:
- chat.js in the browser posts directly to the existing AgentOS route on the same origin (/api/agents/groq-finance-agent/runs).
- The server never fetches a URL for chat.
- Agent replies are turned into safe HTML by a small server endpoint (/api/chat/render)
  that uses the Part 19 renderer (POST text, get sanitized HTML back), with its own size limit (64 KB)
  and rate limit, both covered by tests.
- api/web/chat.py holds only the drawer rendering and that endpoint.
"""

from __future__ import annotations

import re
import time
from collections import defaultdict
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from api.web.markdown import render_markdown


MAX_PAYLOAD_BYTES = 64 * 1024  # 64 KB


def friendly_agent_error(value: Any, status: int | None = None) -> str:
    """Normalize agent errors with exact parity to original client/src/lib/agentos.ts."""
    message = str(value or "")
    normalized = message.lower()
    if (
        status in (429, 503)
        or re.search(
            r"temporarily unavailable|rate.?limit|quota|too many requests|service unavailable|overloaded",
            normalized,
        )
    ):
        return (
            "AI analysis is temporarily unavailable. Please wait a few minutes and try again; "
            "the dashboard is ready for your next request."
        )
    if status is not None and status >= 500:
        return "The Research Desk is temporarily unavailable. Please try again shortly."
    if status in (401, 403):
        return "The Research Desk is unavailable for this session. Please check the configured endpoint."
    return message or (f"AgentOS request failed ({status})." if status else "AgentOS request failed.")


class RenderRateLimiter:
    """In-memory rate limiter per client IP: max 60 requests per 60 seconds."""

    def __init__(self, max_requests: int = 60, window_seconds: float = 60.0) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        timestamps = self._history[key]
        # Prune older than window
        cutoff = now - self.window_seconds
        valid = [t for t in timestamps if t > cutoff]
        self._history[key] = valid
        if len(valid) >= self.max_requests:
            return False
        valid.append(now)
        return True

    def reset(self) -> None:
        self._history.clear()


render_rate_limiter = RenderRateLimiter()

chat_router = APIRouter()


class RenderRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    text: str = Field(default="")


@chat_router.post("/api/chat/render")
async def render_chat_text(req: RenderRequest, request: Request) -> dict[str, str]:
    """Turn agent markdown text into sanitized HTML with 64 KB size limit and rate limit."""
    # Check 64 KB size limit
    byte_length = len(req.text.encode("utf-8"))
    if byte_length > MAX_PAYLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Payload exceeds 64 KB limit ({byte_length} bytes received)",
        )

    # Check client IP rate limit
    client_ip = request.client.host if request.client else "unknown"
    if not render_rate_limiter.allow(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please wait a moment before sending more messages.",
        )

    html = render_markdown(req.text)
    return {"html": html}
