# BATCH_01.md — QuantAI Migration

**Batch:** BATCH_01  
**Day:** 1  
**Parts:** 01–05  
**Repository:** https://github.com/SamSurve/QuantAI.git  
**Branch:** main  
**Original source:** E:\Quant-AI (READ-ONLY)  
**Target repository:** E:\QuantAI-Python  
**Python:** 3.12.7  
**Terminal:** Windows PowerShell

---

# 1. READ FIRST

Before doing anything, read these four files completely:

1. migration/MIGRATION_PLAN.md
2. migration/PROGRESS.md
3. migration/MASTER_PROMPT.md
4. migration/BATCH_01.md

MASTER_PROMPT.md and MIGRATION_PLAN.md are authoritative.

Follow all precedence rules, security requirements, testing requirements and Git restrictions.

Do not re-plan the migration.

Do not start BATCH_02.

Complete Parts 01, 02, 03, 04 and 05 sequentially without asking the user between parts.

Stop immediately on an unresolved critical blocker or after three unsuccessful fix attempts.

---

# 2. SKILLS

## Mandatory for every part

- test-driven-development
- source-driven-development
- code-review-and-quality

## Additional skill

- Part 03: json-to-pydantic (optional, only if useful).

## Reference only

- git-workflow-and-versioning

Do not use git-workflow-and-versioning to change the approved Git workflow.

Do not use frontend-ui-engineering in this batch.

The security skill is not required in Parts 01–05.

At the start of EVERY part, print:

`Skills used: test-driven-development, source-driven-development, code-review-and-quality`

For Part 03, append `json-to-pydantic` if used.

For each skill, follow its useful instructions only where they do not conflict with MASTER_PROMPT.md or MIGRATION_PLAN.md.

Never create extra planning or specification files.

---

# 3. EXECUTION ENVIRONMENT

Use the existing virtual environment.

Python executable:

`.\.venv\Scripts\python.exe`

Working directory:

`E:\QuantAI-Python`

All commands must work in Windows PowerShell.

Use:

`.\.venv\Scripts\python.exe -m pytest -q`

For dependency installation:

`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

Do not rely on the Microsoft Store Python alias.

Do not require Node.js.

Never run npm, npx, pnpm or Bash commands.

---

# PART 01 — PYTHON FOUNDATION AND SOURCE PRESERVATION

## Goal

Create the Python-only project foundation.

Import all existing Python backend code and all seven original Python test suites from the original repository without unnecessarily rewriting existing functionality.

The original repository must remain untouched.

## Exact original source files to read and copy

Source root:

`E:\Quant-AI`

Copy all 19 Python backend files, preserving their relative paths.

1. `api/__init__.py`
2. `api/agents.py`
3. `api/ai_providers.py`
4. `api/company_analysis_services.py`
5. `api/comparison_services.py`
6. `api/fx_services.py`
7. `api/groq_finance_agent.py`
8. `api/health.py`
9. `api/index.py`
10. `api/market_intelligence_services.py`
11. `api/research.py`
12. `api/research_cache.py`
13. `api/research_errors.py`
14. `api/research_logging.py`
15. `api/research_orchestrator.py`
16. `api/research_protection.py`
17. `api/research_schemas.py`
18. `api/research_services.py`
19. `api/agents/groq-finance-agent/runs.py`

Copy these seven existing Python regression suites:

1. `tests/test_agentos_entity_resolution.py`
2. `tests/test_company_comparison.py`
3. `tests/test_company_deep_analysis.py`
4. `tests/test_market_intelligence.py`
5. `tests/test_production_readiness.py`
6. `tests/test_provider_failover.py`
7. `tests/test_typed_research_backend.py`

Inspect:

- `E:\Quant-AI\requirements.txt`
- `E:\Quant-AI\.python-version`
- Actual imports and environment-variable access in all 19 Python backend files.

Do not copy original TypeScript files, `package.json`, pnpm lockfiles, `.env`, private credentials or other secrets.

## Exact Python files to create

- `index.py`
- `api/settings.py`
- `requirements.txt`
- `pyproject.toml`
- `.python-version`
- `.env.example`
- `.gitignore` (verify the already saved root file; update only if necessary)
- `README.md`
- `tests/test_bootstrap_imports.py`

Do not recreate the four migration files. They already exist.

## Implementation requirements

### A. Preserve the existing backend

Copy all 19 files.

Keep their nested directories.

Preserve existing:
- Imports.
- API behavior.
- Pydantic schemas.
- Research services.
- Orchestration.
- Market calculations.
- Provider failover.
- TTL caching.
- Rate limiting.
- Concurrency controls.
- AgentOS functionality.
- Error handling.

Do not refactor working backend modules just to introduce a different coding style.

Adapt only when necessary for the new Python project to import and execute correctly.

Document necessary changes.

### B. Environment-variable discovery

The actual backend code is the source of truth.

Inspect all 19 files for:

- `os.getenv`
- `os.environ.get`
- `os.environ[...]`
- Pydantic BaseSettings
- Other explicit environment access.

Create `.env.example` from the real variable names discovered in the code.

Rules:

- Names only.
- No values.
- No dummy credentials.
- Never copy `.env`.
- Do not include unused VITE variables.
- Do not include unused OAuth template variables.
- Do not assume that the audit's variable list is complete.

Compare the actual code against the audit's environment-variable list.

Report differences in the Part 01 summary.

If the code disagrees with the audit, actual code wins.

Never print environment-variable values.

### C. Python configuration

Use Python 3.12.

Preserve compatible existing dependencies.

Create a reproducible requirements.txt.

Include approved dependencies required for the existing backend and test baseline.

Do not introduce unapproved packages.

Set up pyproject.toml with pytest and Ruff configuration.

Create root index.py exporting the canonical FastAPI application from api.index.

Do not create a second independent FastAPI application.

### D. Test-first requirements

Write `tests/test_bootstrap_imports.py` before implementing the bootstrap changes.

Copy all seven original Python suites without weakening their assertions.

All seven existing suites must pass before Part 01 can be committed.

Install dependencies:

`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

Run:

`.\.venv\Scripts\python.exe -m pytest -q`

Check imports for:

- `api.index:app`
- AgentOS modules.
- Research orchestrator.
- Market intelligence services.
- Existing Python backend services.

A missing dependency must be resolved through the approved requirements.txt, not by manually installing undocumented packages.

## Acceptance criteria

- All 19 backend files copied.
- All seven original Python suites copied.
- Existing backend functionality preserved.
- All required imports resolve.
- Root Python entrypoint works.
- Environment variable names discovered from actual source.
- `.env.example` contains names only.
- Differences from audit's environment-variable list reported.
- No secrets copied.
- Original repository untouched.
- Full seven-suite regression baseline passes.
- Bootstrap tests pass.
- Working tree contains no accidental Node.js files.

## Commit

`part 01: establish Python-only foundation`

## Push command

After implementation, testing and review:

`.\.venv\Scripts\python.exe migration\push_part.py 1 "part 01: establish Python-only foundation"`

This is the first commit. The new GitHub repository currently has no commits. The push script supports an unborn main branch.

---

# PART 02 — TEST INFRASTRUCTURE

## Goal

Create the permanent Python regression testing infrastructure while retaining all seven existing suites.

## Exact original source files to read

- `E:\Quant-AI\requirements.txt`
- `E:\Quant-AI\tests\test_agentos_entity_resolution.py`
- `E:\Quant-AI\tests\test_company_comparison.py`
- `E:\Quant-AI\tests\test_company_deep_analysis.py`
- `E:\Quant-AI\tests\test_market_intelligence.py`
- `E:\Quant-AI\tests\test_production_readiness.py`
- `E:\Quant-AI\tests\test_provider_failover.py`
- `E:\Quant-AI\tests\test_typed_research_backend.py`

Inspect existing dependency versions and test patterns.

## Exact Python files to create or update

- `tests/conftest.py`
- `tests/test_backend_baseline.py`
- `tests/test_pytest_configuration.py`
- `pyproject.toml`
- `requirements.txt` (only if a required approved test dependency is missing)

## Dependencies

Part 01.

## Implementation requirements

1. Configure pytest discovery.
2. Provide shared pytest fixtures.
3. Support asynchronous tests.
4. Configure clean temporary test directories.
5. Support HTTP mocking through approved `respx`.
6. Preserve original test isolation.
7. Configure Ruff.
8. Avoid requiring external API keys for ordinary tests.
9. Ensure test output does not expose secrets.
10. Do not introduce a database.

Use test-driven development.

Create the new tests first.

Do not modify the seven copied test suites just to make them pass.

The original seven tests form a permanent regression baseline.

## Acceptance criteria

- pytest discovers all tests.
- Shared fixtures work.
- Async test support works.
- HTTP mocking works.
- Ruff configuration is valid.
- Tests do not require real AI-provider credentials.
- The seven original suites still pass.
- Full test command works from PowerShell.

## Tests

- Existing seven Python suites.
- `tests/test_backend_baseline.py`
- `tests/test_pytest_configuration.py`

Run:

`.\.venv\Scripts\python.exe -m pytest -q`

## Commit

`part 02: establish regression test infrastructure`

## Push command

`.\.venv\Scripts\python.exe migration\push_part.py 2 "part 02: establish regression test infrastructure"`

---

# PART 03 — PYDANTIC CONTRACTS AND RESPONSE MODELS

## Goal

Port the TypeScript frontend's research and market data interfaces to Python using Pydantic v2.

Preserve all field names, optional fields, nested structures, literal unions and serialization behavior.

## Exact TypeScript source files to read

1. `E:\Quant-AI\client\src\lib\research.ts`
2. `E:\Quant-AI\client\src\lib\agentos.ts`
3. `E:\Quant-AI\client\src\lib\market.ts`

Also read:

4. `E:\Quant-AI\api\research_schemas.py`
5. Relevant backend tests from `E:\Quant-AI\tests\`

Inspect all source definitions, not just the interface names.

## Exact Python files to create or update

- `api/research_schemas.py`
- `api/web/__init__.py`
- `api/web/contracts.py`
- `tests/test_research_contract_parity.py`

## Skills

Mandatory:

- test-driven-development
- source-driven-development
- code-review-and-quality

Optional:

- json-to-pydantic

## Dependencies

Parts 01 and 02.

## Models to preserve

### Research contracts

- TypedResearchResponse
- MarketPulse
- PriceHistory
- MarketSignal
- CompanyDeepAnalysis
- CompanyComparison

### Market presentation contracts

- MarketBrief
- Metric
- ChartPoint
- BriefNewsItem

### AgentOS contracts

- AgentRunResponse
- AgentInfo

Check the actual original source for every additional nested model.

Do not assume the above list is exhaustive.

## Implementation requirements

1. Use Pydantic v2.
2. Use Literal for true TypeScript literal unions.
3. Use Optional/nullable types exactly where source permits missing or null data.
4. Preserve nested arrays and objects.
5. Preserve original field names and casing.
6. Preserve numeric types and values.
7. Preserve winner values including:
   - A
   - B
   - TIE
   - INSUFFICIENT_DATA
8. Distinguish an absent field from an explicit null when the original contract does.
9. Preserve existing backend response contracts.
10. Extend existing models only when needed for accurate frontend parity.
11. Do not create duplicate incompatible versions of the same public response model.
12. Do not invent fields.

Create contract tests before implementation.

## Acceptance criteria

- Every original frontend contract is represented.
- All TypeScript optionality is retained.
- Discriminated unions work.
- Serialization remains compatible.
- Existing Python backend models remain compatible.
- No original JSON response field is silently renamed or removed.
- Nested model validation is covered.

## Tests

- Model validation.
- Missing optional fields.
- Explicit null values.
- Literal union cases.
- Nested arrays and objects.
- Serialization/deserialization.
- Existing typed research regression suite.
- `tests/test_research_contract_parity.py`.

Run full pytest:

`.\.venv\Scripts\python.exe -m pytest -q`

## Commit

`part 03: preserve typed research contracts`

## Push command

`.\.venv\Scripts\python.exe migration\push_part.py 3 "part 03: preserve typed research contracts"`

---

# PART 04 — MARKET FORMATTING AND DATA PRESENTERS

## Goal

Port the frontend's market formatting, number formatting, date formatting and data presentation helpers into reusable Python functions.

Do not change financial calculations.

## Exact TypeScript source files to read

1. `E:\Quant-AI\client\src\lib\market.ts`
2. `E:\Quant-AI\client\src\lib\utils.ts`

Read all functions and their callers.

## Exact Python files to create

- `api/web/formatters.py`
- `api/web/presenters.py`
- `tests/test_web_formatters.py`
- `tests/test_web_presenters.py`

## Dependencies

Part 03.

## Implementation requirements

Port the actual original rules for:

- Currency formatting.
- Compact money formatting.
- Compact large-number formatting.
- Percentage formatting.
- Decimal precision.
- Sign display.
- Price formatting.
- Financial metric labels.
- Metric tone selection.
- Missing-value fallbacks.
- Null handling.
- Date formatting.
- UTC-normalized dates.
- Market brief presentation.

Read the TypeScript implementation before selecting Python formatting functions.

Do not substitute generic formatting behavior when the original has a specific rule.

Keep formatting utilities separate from research services.

Keep presenters separate from raw financial data models.

Use deterministic functions wherever possible.

Create tests first.

## Acceptance criteria

- Currency formatting matches original behavior.
- Positive and negative values retain sign behavior.
- Percentage formatting matches original precision.
- Missing values use the original fallbacks.
- UTC dates are not shifted across time zones.
- Original market metric tones are preserved.
- Presenter output preserves required information.
- No financial calculation is changed.

## Tests

- Positive values.
- Negative values.
- Zero.
- Currency cases.
- Large values.
- Decimal precision.
- Percentage sign.
- Missing values.
- Null values.
- Date boundaries.
- UTC date handling.
- Presenter metric fallback.
- Existing backend regression tests.

Run:

`.\.venv\Scripts\python.exe -m pytest -q`

## Commit

`part 04: port market formatting utilities`

## Push command

`.\.venv\Scripts\python.exe migration\push_part.py 4 "part 04: port market formatting utilities"`

---

# PART 05 — FASTAPI WEB APPLICATION AND BASE HTML SHELL

## Goal

Integrate the Python web interface into the existing FastAPI application.

Create the first server-rendered HTML workspace foundation without breaking original JSON health and API contracts.

## Exact TypeScript/source files to read

1. `E:\Quant-AI\client\index.html`
2. `E:\Quant-AI\client\src\App.tsx`
3. `E:\Quant-AI\client\src\main.tsx`
4. `E:\Quant-AI\client\src\pages\NotFound.tsx`
5. `E:\Quant-AI\server\index.ts`
6. `E:\Quant-AI\vite.config.ts`
7. `E:\Quant-AI\api\index.py`

Also inspect the existing backend route registration and health handlers.

Do not port unused Node or Vite functionality.

## Exact Python files to create or update

- `index.py`
- `api/index.py`
- `api/web/routes.py`
- `templates/base.html`
- `templates/pages/home.html`
- `templates/pages/not_found.html`
- `tests/test_root_content_negotiation.py`
- `tests/test_web_routes.py`

## Dependencies

Parts 01–04.

## Implementation requirements

### A. One canonical FastAPI application

`api/index.py` remains the canonical application.

Root `index.py` re-exports the same FastAPI application.

Do not create a second independent FastAPI instance.

### B. Jinja2 setup

Configure Jinja2 templates.

Mount static assets correctly.

Create a minimal base HTML template.

Create the initial workspace page.

Create a not-found page.

This is the route and rendering foundation, not the final Apple design. The approved visual system will be implemented in Part 06.

### C. Root content negotiation — CRITICAL

The original root `/` endpoint also serves JSON health information.

Preserve that behavior.

Only an Accept header that explicitly prefers `text/html` may receive the HTML workspace.

Required behavior:

| Accept header | Response |
|---|---|
| Missing | Original JSON health |
| `*/*` | Original JSON health |
| `application/json` | Original JSON health |
| `text/html` | HTML workspace |
| `text/html,application/json` | JSON health because preference is equal |
| `text/html;q=0.9,application/json;q=0.8` | HTML workspace |
| `application/json;q=1,text/html;q=0.9` | JSON health |
| `application/json,text/html;q=0.5` | JSON health |
| Explicit `text/html` with higher quality than JSON | HTML workspace |
| `text/html;q=0` | JSON health |

Parse quality values correctly.

A wildcard alone must never cause the workspace to render.

An equal JSON/HTML preference must resolve to JSON.

Add explicit regression tests for all these cases.

Do not rely on a generic wildcard content-negotiation shortcut.

### D. Preserve health endpoints

Keep the following available:

- GET /
- GET /health
- GET /api
- GET /api/health

Preserve the original JSON health response fields.

Do not rename or remove fields.

### E. Preserve backend API routes

Keep existing routes available:

- POST /api/research
- GET /api/agents
- POST /api/agents/groq-finance-agent/runs
- GET /api/docs
- GET /api/openapi.json

Inspect the original route mounting and preserve compatibility.

### F. Not-found handling

Implement:

- `/404`
- Unmatched browser routes

Return the correct HTTP status code.

Render the server-side not-found template for browser HTML requests.

Do not break API JSON errors.

### G. Static files

Use FastAPI/Starlette StaticFiles.

Do not introduce Express or another Node server.

## Acceptance criteria

- One canonical FastAPI application.
- Root HTML only for explicitly preferred text/html.
- Missing Accept returns JSON health.
- */* returns JSON health.
- application/json returns JSON health.
- Equal JSON/HTML preference returns JSON.
- Correct q-value preference handling.
- All health aliases remain functional.
- API routes remain available.
- Swagger UI and OpenAPI JSON remain available.
- Jinja2 rendering works.
- Static mounting works.
- Correct 404 status and rendering.
- No Node.js dependency.

## Tests

Create and run:

- `tests/test_root_content_negotiation.py`
- `tests/test_web_routes.py`

Test every root Accept-header case listed above.

Test:
- Root JSON health response.
- Root HTML workspace response.
- `/health`.
- `/api`.
- `/api/health`.
- Existing API route registration.
- API docs.
- OpenAPI JSON.
- Static asset route.
- `/404`.
- Unmatched route behavior.
- Correct content types.
- Correct status codes.

Run:

`.\.venv\Scripts\python.exe -m pytest -q`

## Commit

`part 05: integrate FastAPI web application`

## Push command

`.\.venv\Scripts\python.exe migration\push_part.py 5 "part 05: integrate FastAPI web application"`

---

# 4. COMMON WORKFLOW FOR EACH PART

For each part, follow this exact sequence:

1. Print the required Skills used line.
2. Read every specified original source file.
3. Inspect callers and dependencies where necessary.
4. Write tests first.
5. Implement only the current part.
6. Run focused tests.
7. Run the complete pytest suite.
8. Fix failures, maximum three fix attempts after the initial failure.
9. Perform code-review-and-quality self-review.
10. Inspect the Git diff.
11. Confirm no secrets or protected files will be staged.
12. Update migration/PROGRESS.md.
13. Run the push script.
14. Verify commit and push.
15. Continue automatically to the next part.

Do not start the next part if the current part is incomplete.

Do not mark later parts checked.

The current part's checkbox must be set before invoking push_part.py because the script explicitly validates the checked state and includes PROGRESS.md in the current commit. Treat this as implementation-and-test readiness until the push is confirmed. A failed push is a blocker, not a completed part.

## Mandatory full test command

`.\.venv\Scripts\python.exe -m pytest -q`

## Mandatory push commands

Part 01:

`.\.venv\Scripts\python.exe migration\push_part.py 1 "part 01: establish Python-only foundation"`

Part 02:

`.\.venv\Scripts\python.exe migration\push_part.py 2 "part 02: establish regression test infrastructure"`

Part 03:

`.\.venv\Scripts\python.exe migration\push_part.py 3 "part 03: preserve typed research contracts"`

Part 04:

`.\.venv\Scripts\python.exe migration\push_part.py 4 "part 04: port market formatting utilities"`

Part 05:

`.\.venv\Scripts\python.exe migration\push_part.py 5 "part 05: integrate FastAPI web application"`

The push script is the only approved commit/push mechanism.

Never run git add -A.

Never run separate git commit or git push commands.

---

# 5. STOP CONDITIONS

Immediately stop the batch if:

- Tests still fail after three fix attempts.
- A critical original behavior is unclear.
- An original API contract cannot be preserved.
- An essential dependency cannot be resolved.
- Secrets are detected in planned changes.
- Repository origin or branch is incorrect.
- The push script fails.
- A local commit is created but push fails.

Never bypass the push script.

Never create a second commit to compensate for a failed push.

Do not silently skip work.

---

# 6. BATCH COMPLETION

After Part 05 has successfully passed all tests and has been pushed:

Verify:

- Five parts completed.
- Five distinct commits.
- Five successful pushes.
- Five progress updates.
- All seven original Python suites preserved.
- Full pytest passes.
- Correct repository and branch.
- No unrelated or secret files committed.

Provide the user with:

## BATCH_01 SUMMARY

For each part:
- Part number.
- What was implemented.
- Commit SHA.
- Push confirmation.
- Focused test result.
- Full test result.

Also report:
- Discovered environment variables.
- Differences from audit's variable list.
- Existing backend changes, if any.
- Any remaining limitations.

Then print:

BATCH COMPLETE, STOP

Do not begin BATCH_02.

Wait for the user's next instruction.

---

# FINAL INSTRUCTION

The original E:\Quant-AI repository is read-only.

The new Python project is E:\QuantAI-Python.

Every implementation, test, progress update, commit and push must happen in the new repository only.

Preserve the original QuantAI behavior.

Do not invent functionality.

Do not simplify the migration.

Complete all five parts in order and stop after Part 05.