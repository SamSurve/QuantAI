# QuantAI

Apple-style financial research terminal and Agno AgentOS backend implemented in Python 3.12.

## Overview

QuantAI delivers deterministic financial intelligence, company deep analysis, technical market signals, and AI-synthesized executive briefs. Originally built with a hybrid TypeScript/Python stack, QuantAI is migrated to a pure Python architecture powered by FastAPI, Jinja2, HTMX, Tailwind CSS standalone CLI, and Chart.js.

## Architecture

- **Backend:** FastAPI application with Agno AgentOS orchestration (`api.index:app`).
- **Frontend:** Server-rendered HTML with Jinja2, dynamic client interactions with vanilla JavaScript, and Chart.js 4.x.
- **Styling:** Apple-style financial terminal design system compiled via Tailwind CSS 4.1.14 standalone CLI.
- **Runtime:** Python 3.12 with process-local TTL caching, rate limiting, and circuit-breaker failover across Groq and OpenRouter providers.
- **Deployment:** Vercel Python runtime and self-hosted Uvicorn server (`uvicorn index:app --host 127.0.0.1 --port 3000`).

## Setup

```powershell
# Create and activate virtual environment (Python 3.12)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Run test suite
.\.venv\Scripts\python.exe -m pytest -q
```

## Environment Variables

Copy `.env.example` to `.env` and provide credentials as needed:
- `GROQ_API_KEY_PRIMARY`: Primary Groq API key.
- `GROQ_MODEL_PRIMARY`: Primary Groq model (default: `openai/gpt-oss-120b`).
- `GROQ_API_KEY_SECONDARY`: Secondary Groq API key for failover.
- `GROQ_MODEL_SECONDARY`: Secondary Groq model.
- `OPENROUTER_API_KEY`: OpenRouter API key for tertiary fallback.
- `OPENROUTER_MODEL`: OpenRouter fallback model (default: `stealth/ox-alpha`).
- `AI_PROVIDER_ORDER`: Comma-separated provider priority order.
- `QUANTAI_DEVTOOLS`: Set to `1` in development to enable telemetry endpoints (strictly disabled in production).
