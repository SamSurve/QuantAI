# Vercel Release Notes

## Exact Files Added or Changed

| File or directory | Change |
| --- | --- |
| `api/__init__.py` | Added Vercel Python function package marker. |
| `api/index.py` | Added FastAPI Vercel entrypoint, `/api/health`, and mounted AgentOS routes. |
| `api/groq_finance_agent.py` | Added the final Groq AgentOS backend to the deployable repository. |
| `requirements.txt` | Added the single flat root Vercel Python dependency manifest. |
| `.python-version` | Pinned Vercel Python runtime to 3.12. |
| `vercel.json` | Added Vite output, API function, no-cache headers, and API-safe SPA fallback. |
| `vite.config.ts` | Changed local proxy from `/agentos` to `/api`. |
| `client/src/lib/agentos.ts` | Changed production default API URL to same-origin `/api` and migrated saved `/agentos` values. |
| `client/src/pages/Home.tsx` | Preserved design while pointing deployment help text and local visual asset paths to the repository. |
| `client/src/components/BrandMark.tsx` | Changed logo reference to the repository-hosted asset. |
| `client/public/assets/` | Added all Analyst’s Ledger visual assets required for local and Vercel deployment. |
| `package.json` and `pnpm-lock.yaml` | Added Vercel build script and refreshed lock metadata. |
| `.gitignore` | Excluded `.vercel/` and retained local secret exclusions. |
| `README.md` and `VERCEL_DEPLOYMENT.md` | Added local setup and exact GitHub-to-Vercel deployment instructions. |

## Required Vercel Environment Variable

| Name | Required environments | Notes |
| --- | --- | --- |
| `GROQ_API_KEY` | Production, Preview, Development | Server-only Groq credential. Never use a `VITE_` prefix or commit it. |

No other production environment variable is required. Leave `VITE_AGENTOS_API_URL` unset to use the deployed same-origin `/api` function.

## GitHub and Vercel Deployment

1. Extract the ZIP and push the repository root to GitHub.
2. Import the repository at Vercel and keep the root directory at the repository root.
3. Confirm **Vite** framework, `pnpm install --frozen-lockfile`, `pnpm run build`, and `dist/public` output directory.
4. Add `GROQ_API_KEY` to Production, Preview, and Development in Vercel Project Settings.
5. Deploy a preview, verify `/api/health`, then submit `AAPL`, `NVDA`, `MSFT`, `TSLA`, and `RELIANCE.NS` through the dashboard before promoting.

## Local Validation

`pnpm run build`, TypeScript checking, Python function compilation, root dependency resolution, Vercel JSON validation, archive integrity, and secret-value scanning passed. Local production-style `/api` route tests completed for AAPL, NVDA, MSFT, and TSLA using AgentOS, Groq GPT-OSS-120B, YFinance, and web/news tools. The final RELIANCE.NS request was rate-limited by Groq’s account-level token quota during re-test, not by the application route or resolver; retry it after quota recovery in the Vercel preview.
