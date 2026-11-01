"""QuantAI root entrypoint for production and Vercel execution.

Re-exports the canonical FastAPI application from api.index.
"""

from api.index import app

__all__ = ["app"]
