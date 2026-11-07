# QuantAI — Vercel Production Deployment Guide

This document establishes the production deployment configuration, environment variables, runtime architecture, and verification boundaries for QuantAI on Vercel.

---

## 1. Production Deployment Target: Vercel Serverless

QuantAI is deployed as a 100% Python/FastAPI serverless application on Vercel.

- **Platform**: Vercel Serverless Functions
- **Runtime**: Python 3.12 (pinned via `.python-version` and `pyproject.toml`)
- **Framework Architecture**: ASGI / FastAPI application with Jinja2 server-rendered UI and AgentOS streaming JSON APIs.
- **Entrypoints**:
  - `api/index.py` (canonical ASGI application entrypoint)
  - `index.py` (root ASGI re-export for local development (`uvicorn index:app --reload`))
  - Modular file routes:
    - `api/health.py`
    - `api/agents.py`
    - `api/research.py`
    - `api/agents/groq-finance-agent/runs.py`

---

## 2. Configuration (`vercel.json`)

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "functions": {
    "api/**/*.py": {
      "maxDuration": 60,
      "includeFiles": "templates/**,static/**,api/**",
      "excludeFiles": "{tests/**,**/__pycache__/**,**/*.pyc,**/*.pyo,**/.pytest_cache/**,.vercel/**,dist/**,node_modules/**}"
    }
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-store"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/api/index.py"
    }
  ]
}
```

### Key Properties:
- **`maxDuration: 60`**: Extends the function execution timeout to 60 seconds to accommodate complex dual-provider research pipelines (market pulse, history, news, events, and AI interpretation synthesis).
- **`includeFiles`**: Explicitly bundles server-side Jinja2 templates (`templates/**`), pre-built static assets (`static/**`), and backend modules (`api/**`) into the serverless function bundle.
- **`excludeFiles`**: Strips test suites, cache directories, and build artifacts to maintain lean bundle sizes well under Vercel's 500 MB limit.
- **`headers`**: Enforces strict `Cache-Control: no-store` on all `/api/(.*)` endpoints to guarantee fresh, uncached financial intelligence.
- **`rewrites`**: Routes all incoming traffic (`/(.*)`) to the FastAPI ASGI application at `/api/index.py`, which performs internal routing for HTML pages, API endpoints, and static mounts.

---

## 3. Required Environment Variables

Configure these environment variables in your Vercel Project Settings (`Settings -> Environment Variables`):

| Variable Name | Required | Description | Example / Default |
|---|---|---|---|
| `GROQ_API_KEY_PRIMARY` | Yes | Primary Groq API key for high-speed LLM inference | `gsk_...` |
| `GROQ_MODEL_PRIMARY` | No | Primary Groq model identifier | `llama-3.3-70b-versatile` |
| `GROQ_API_KEY_SECONDARY` | No | Secondary Groq API key for automatic failover | `gsk_...` |
| `GROQ_MODEL_SECONDARY` | No | Secondary Groq model identifier | `llama-3.1-8b-instant` |
| `OPENROUTER_API_KEY` | No | OpenRouter API key for tertiary failover | `sk-or-...` |
| `OPENROUTER_MODEL` | No | OpenRouter model identifier | `anthropic/claude-3.5-sonnet` |
| `DEVELOPER_TELEMETRY` | No | Developer debug telemetry (must remain unset or 0 in production) | `0` |

---

## 4. Verification Boundaries: Local vs Live Cloud

To maintain strict deployment honesty:

### Locally Verified Behavior:
1. **ASGI Application Routing**: All routes (`/`, `/health`, `/api/health`, `/api/research`, `/api/agents/...`) mount and route correctly under Uvicorn and TestClient.
2. **Template & Static Bundling**: Jinja2 templates render server-side with zero client-side JavaScript math compilation (server-rendered MathML).
3. **API Headers & Security**: Strict CORS headers, request ID propagation, body size enforcement (8 KB), sliding-window rate limiting, and concurrency guards (max 4).
4. **Graceful Failover**: When API keys are missing or invalid, endpoints degrade gracefully to deterministic financial data with clear, user-friendly status banners.

### Behaviors Requiring Live Vercel Deployment:
1. **Edge CDN Routing**: Physical Vercel edge node distribution, TLS termination, and anycast DNS routing.
2. **Real Serverless Cold Starts**: Sub-second container provisioning on AWS Lambda / Firecracker microVMs.
3. **Cloudflare / Vercel Edge Headers**: Headers injected solely by Vercel edge infrastructure (`x-vercel-id`, `x-real-ip`).
4. **Upstream Quota Latency**: Live network round-trip latency to Groq and OpenRouter edge nodes.
