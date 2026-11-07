# QuantAI

Apple-style financial research terminal and Agno AgentOS backend implemented in pure Python 3.12.

## Overview

QuantAI delivers deterministic financial intelligence, company deep analysis, technical market signals, and AI-synthesized executive briefs. Originally built with a hybrid TypeScript/Python stack, QuantAI has been completely migrated to a unified, pure Python architecture powered by FastAPI, Jinja2, Chart.js 4.x, and Tailwind CSS.

For the certified parity matrix across all 21 UI features, Apple visual system tokens, and 7 infrastructure security capabilities, see [PARITY_CHECKLIST.md](PARITY_CHECKLIST.md).

## Production Architecture (Vercel Serverless)

- **Mandatory Production Platform:** Vercel Serverless Functions (Python 3.12 runtime).
- **ASGI Entrypoint:** `api/index.py` exporting the canonical `app` instance.
- **Routing & Rewrite Rules:** Configured in `vercel.json` with 60s execution timeout and explicit inclusion of `templates/**`, `static/**`, and `api/**`.
- **Security & Secret Invariants:** Zero provider credentials leak in client-facing HTML, JSON error details, client JavaScript, or URL parameters. Server-side SSRF validation blocks all private/internal IPs, RFC 1918 subnets, and cloud metadata endpoints.
- **Deployment Documentation:** See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for full configuration, edge caching policies, and deployment honesty boundaries.

## Local Development & Supplementary Testing

Local Uvicorn execution is supported strictly for local development and offline test execution:

```powershell
# Create and activate virtual environment (Python 3.12)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Start local development server
.\.venv\Scripts\uvicorn.exe index:app --port 8000 --host 127.0.0.1 --reload

# Run complete pytest verification suite
.\.venv\Scripts\python.exe -m pytest -q
```

## Environment Variables

Copy `.env.example` to `.env` and configure credentials:
- `GROQ_API_KEY_PRIMARY`: Primary Groq API key for AgentOS and AI briefs.
- `GROQ_MODEL_PRIMARY`: Primary Groq model (default: `openai/gpt-oss-120b`).
- `GROQ_API_KEY_SECONDARY`: Secondary Groq API key for sequential failover.
- `GROQ_MODEL_SECONDARY`: Secondary Groq model.
- `OPENROUTER_API_KEY`: OpenRouter API key for tertiary fallback.
- `OPENROUTER_MODEL`: OpenRouter fallback model (default: `stealth/ox-alpha`).
- `AI_PROVIDER_ORDER`: Comma-separated provider priority order.
- `QUANTAI_DEVTOOLS`: Strictly set to `0` in production (enables debug endpoints only in local dev).
