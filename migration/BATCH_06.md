# BATCH 06 — PARTS 26–30 (DAY 3 FINAL RELEASE)

## Objective

Complete the final five migration parts (Parts 26–30) for QuantAI, achieving 100% full parity with the original TypeScript application, verifying all 21 user-facing UI features and 7 infrastructure features, and ensuring all 30 atomic commits are verified and pushed to `origin/main`.

---

## Batch 06 Parts Overview

| Part | Title | Focus Area | Key Output Files |
|---|---|---|---|
| **Part 26** | Legacy Markdown parser | Port conversational AgentOS markdown/table parser from `market.ts` | `api/web/legacy_parser.py`, `tests/test_legacy_parser.py` |
| **Part 27** | Developer telemetry with strict gating | Environment-gated devtools telemetry, strictly disabled in production | `api/web/telemetry.py`, `tests/test_developer_telemetry.py` |
| **Part 28** | Five TypeScript regression inventory | Inventory, catalog, and verify all 5 converted Python regression suites | `tests/test_regression_inventory.py` |
| **Part 29** | Vercel & self-hosted deployment | Deployment configs, serverless headers, environment documentation | `vercel.json`, `VERCEL_DEPLOYMENT.md`, `tests/test_deployment_config.py` |
| **Part 30** | Full parity and release audit | Comprehensive release audit across 21 UI + 7 infra features | `tests/test_final_release_audit.py`, Final Report |

---

## Rules of Engagement

1. All parts must be executed strictly in numerical order (26 -> 27 -> 28 -> 29 -> 30).
2. All mutating Git operations must use `migration/push_part.py`.
3. The baseline protected test files `tests/test_production_readiness.py` and `tests/test_provider_failover.py` must never be modified.
4. Each part must have dedicated focused tests and 100% pass rate on full pytest suite before push.
5. All code must pass `ruff check .` with zero errors.
6. The working tree must remain clean after every part.
