# Groq Finance Agent

This repository contains the final **Groq Finance Agent** and its **Analyst’s Ledger** frontend. The browser application is a Vite/React dashboard and the research API is an AgentOS application exposed through a Vercel-compatible FastAPI function.

## What is included

| Component | Location | Role |
| --- | --- | --- |
| Analyst’s Ledger | `client/` | Responsive React dashboard, price cards, chart, news, analysis, loading, and error states. |
| Vercel API function | `api/index.py` | Same-origin FastAPI entrypoint mounted under `/api`. |
| Groq finance agent | `api/groq_finance_agent.py` | GPT-OSS-120B via Groq, AgentOS, YFinance company/ticker resolution, DDGS news research. |
| Vercel configuration | `vercel.json` | Vite build output, SPA fallback excluding `/api`, function duration, and no-cache API headers. |

## Local development

For the quickest two-terminal workflow, start the AgentOS server and Vite frontend separately:

```bash
# Terminal 1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your-key"
python api/groq_finance_agent.py

# Terminal 2
pnpm install
pnpm dev
```

The Vite development server proxies browser requests from `/api/*` to the local AgentOS server, so the frontend retains the same API URL in development and deployment.

## Vercel

Read [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md) for the exact environment variables, GitHub import workflow, Vercel project settings, preview checks, and deployment validation steps.

> `GROQ_API_KEY` is server-only. Do not commit it, do not use a `VITE_` prefix, and configure it exclusively through Vercel Environment Variables.
