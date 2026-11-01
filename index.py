"""QuantAI root entrypoint for production and Vercel execution.

Re-exports the canonical FastAPI application from api.index.
"""

from __future__ import annotations

import sys
import api.index

app = api.index.app


def __getattr__(name: str):
    if name == "app":
        import api.index as api_idx
        return api_idx.app
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = ["app"]
