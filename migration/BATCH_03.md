
# BATCH_03.md — Financial Intelligence and Research Experience

**Project:** QuantAI Python Migration  
**Repository:** https://github.com/SamSurve/QuantAI.git  
**Branch:** main  
**Working directory:** E:\QuantAI-Python  
**Original TypeScript source:** E:\Quant-AI (READ-ONLY)  
**Approved design reference:** E:\QuantAI-design\Main.dc.html  
**Batch:** 03 of 06  
**Day:** 2 of 3  
**Parts:** 11–15  
**Required commits:** Exactly 5  
**Required pushes:** Exactly 5  

---

# 0. CRITICAL START INSTRUCTIONS

Before writing any code:

1. Read these files completely:
   - migration/MIGRATION_PLAN.md
   - migration/PROGRESS.md
   - migration/MASTER_PROMPT.md
   - migration/BATCH_03.md

2. Verify:
   - Python 3.12 virtual environment exists.
   - Git remote is https://github.com/SamSurve/QuantAI.git.
   - Current branch is main.
   - Working tree is clean.
   - Parts 01–10 are checked in PROGRESS.md.
   - Exactly 10 migration commits exist on main.

3. Inspect the existing implementations from Parts 01–10.

4. Inspect the original TypeScript source without modifying it.

5. Open E:\QuantAI-design\Main.dc.html in the browser and inspect its visual design.

6. Print:
   `Skills used: ...`

If a required dependency, file or architectural assumption is missing, stop and report it. Do not invent replacements or silently change the migration plan.

**Important:** The approved HTML concept is a visual reference only. The original TypeScript project remains the source of truth for functionality and financial calculations.

---

# 1. GLOBAL RULES

These rules apply to ALL FIVE PARTS.

## 1.1 Source preservation

Original repository:

E:\Quant-AI

- READ ONLY.
- Never modify original TypeScript files.
- Never commit original TypeScript source.
- Never copy sample financial data from the design concept.
- Port actual business logic and behavior.

New repository:

E:\QuantAI-Python

- Python-only application.
- No Node.js.
- No npm.
- No npx.
- No Vite.
- No TypeScript runtime.

## 1.2 Development environment

Use:

`.\.venv\Scripts\python.exe`

For pytest:

`.\.venv\Scripts\python.exe -m pytest`

For the application, use the existing FastAPI development command specified in MASTER_PROMPT.md.

All commands must work in Windows PowerShell.

## 1.3 Behavior preservation

- Preserve original financial calculations.
- Preserve API response semantics.
- Preserve provider fallback behavior.
- Preserve error handling.
- Preserve loading and unavailable states.
- Preserve existing company workspace behavior.
- Never replace deterministic calculations with AI-generated approximations.

## 1.4 Existing tests

Never weaken, delete, skip or remove existing tests.

Current baseline: 96 passing tests.

Every part must:
1. Write its new tests first.
2. Implement the functionality.
3. Run focused tests.
4. Run the complete pytest suite.
5. Fix failures, maximum three attempts.
6. Review the complete Git diff.
7. Perform browser verification.
8. Update PROGRESS.md.
9. Push using migration/push_part.py.

Report any differences from the original test suites.

---

# 2. SKILLS

Use the installed global Antigravity skills.

Required for EVERY part:

- test-driven-development
  - Write tests before implementation.
- source-driven-development
  - Verify library usage against official documentation.
  - Do not guess API behavior.
- code-review-and-quality
  - Review the complete diff before pushing.
- git-workflow-and-versioning
  - Reference only. Must not change the prescribed Git workflow.

Additionally, ALL Parts 11–15 are UI-related:

- frontend-ui-engineering

At the beginning of each part, print:

`Skills used: test-driven-development, source-driven-development, frontend-ui-engineering, code-review-and-quality`

Reference git-workflow-and-versioning without allowing it to change the prescribed commit workflow.

MIGRATION_PLAN.md, PROGRESS.md and MASTER_PROMPT.md override every skill.

Never run slash commands such as /spec, /plan, /build or /build auto.

Never create additional planning files.

---

# 3. VISUAL DESIGN REQUIREMENTS

The application must follow:

`E:\QuantAI-design\Main.dc.html`

The concept is the approved visual target.

Extract and preserve:
- Light and dark color tokens.
- Font stack.
- Typography sizes and tracking.
- Card spacing.
- Border radii.
- Shadows.
- Header geometry.
- Search styling.
- Chart styling.
- Segmented controls.
- Responsive behavior.

Use the existing Tailwind and Jinja2 design system.

Do not copy:
- Main.dc.html.
- support.js.
- vendor runtime.
- Custom elements such as x-dc, sc-for, sc-if or helmet.
- Generated sample data.

Reimplement with Jinja2, HTMX, vanilla JavaScript and Chart.js.

## Mandatory browser verification

Before EVERY push, open the running application and the approved concept side by side.

Verify all four combinations:

| Viewport | Theme |
|---|---|
| 1440px | Light |
| 1440px | Dark |
| 390px | Light |
| 390px | Dark |

For every part, the final report MUST contain:

1. What was clicked or interacted with.
2. What appeared on screen.
3. Whether it matched the concept.
4. What differences were found.
5. What was fixed.
6. What remains unresolved.

A statement such as "Visuals match" is not acceptable evidence.

If no browser tool is available, STOP the current part. Do not push it.

---

# 4. PART EXECUTION

Execute the following five parts sequentially.

Do not ask for confirmation between parts.

---

# PART 11 — Market Quote and Snapshot

## Goal

Implement the live market quote and market snapshot.

IMPORTANT: Part 10 already implemented the company identity block, including:
- Company name.
- Ticker.
- Identity status.
- Market price.
- Price change.
- Percentage change.

Do not rebuild or duplicate this functionality.

Extend the existing identity dossier and integrate the real market snapshot.

## TypeScript files to read

Read completely:

1. E:\Quant-AI\client\src\components\Home.tsx
2. E:\Quant-AI\client\src\components\MetricCard.tsx
3. E:\Quant-AI\client\src\lib\market.ts
4. E:\Quant-AI\api\market_intelligence_services.py
5. E:\Quant-AI\api\research_schemas.py
6. E:\Quant-AI\api\research_orchestrator.py

The existing Python backend is also part of the source of truth.

## Python files to inspect and extend

- api/market_intelligence_services.py
- api/research_schemas.py
- api/research_orchestrator.py
- api/web/routes.py
- templates/partials/identity_dossier.html
- templates/pages/home.html
- static/css/input.css

Add only the additional modules or partials specified in MIGRATION_PLAN.md.

## Critical correction: Negative price color

Currently, negative price movement incorrectly uses the warning-orange color.

Introduce a dedicated `--down` token.

Light theme:

`--down: #e30000`

Dark theme:

`--down: #ff453a`

The exact token values must be checked against the approved design and the established finance UI conventions before finalizing.

Use:
- Green for positive movement.
- Red for negative movement.
- Orange for warnings.
- Neutral for unchanged movement.

Do not use warning orange for negative financial returns.

Update both theme token definitions in static/css/input.css.

Update the existing identity dossier rather than creating a second price display.

## Tests to write first

Create tests for:

1. Positive price movement.
2. Negative price movement.
3. Zero price movement.
4. Negative movement renders the dedicated red token.
5. Light and dark token definitions both include --down.
6. Warning colors remain independent of negative price colors.
7. Existing identity dossier fields remain intact.
8. Missing quote data displays the correct unavailable state.
9. Real backend data is used.
10. No concept sample prices or metrics appear.

## Acceptance criteria

- Existing Part 10 identity block is reused.
- No duplicate price or change display.
- Negative values use --down.
- Positive values use the existing green token.
- Warning orange remains available for warnings.
- Live quote and snapshot preserve original behavior.
- Existing tests pass.

## Browser evidence

At all four viewport/theme combinations:

- Search for a real company.
- Inspect the identity header.
- Inspect a positive price movement.
- Inspect a negative movement using a controlled test fixture.
- Verify that red is used rather than orange.
- Verify responsive layout.

Document the actual clicks and observations.

## Commit

`part 11: implement market quote and snapshot`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 11 "part 11: implement market quote and snapshot"`

---

# PART 12 — Interactive Chart and Performance

## Goal

Port the complete original market chart behavior.

The chart must use real backend-supplied historical data.

No sample data from Main.dc.html.

## TypeScript files to read

1. E:\Quant-AI\client\src\components\MarketChart.tsx
2. E:\Quant-AI\client\src\lib\market.ts
3. E:\Quant-AI\client\src\components\Home.tsx
4. E:\Quant-AI\tests\test_chart_date_formatting.ts

Also inspect the relevant Python historical-price and research services.

## Python files to create or extend

- static/js/market_chart.js
- static/vendor/chart/chart.umd.min.js
- templates/partials/market_chart.html
- templates/pages/home.html
- api/web/routes.py
- Relevant historical-price service modules.
- tests/test_market_chart.py
- tests/test_chart_date_formatting.py

Follow the exact additional file mapping in MIGRATION_PLAN.md.

## Chart.js vendor requirement

Vendor Chart.js 4.x locally.

Requirements:

1. Select a stable pinned 4.x release.
2. Verify the exact version against the official Chart.js release.
3. Obtain the official distribution bundle.
4. Store it at:

`static/vendor/chart/chart.umd.min.js`

5. No npm.
6. No CDN at runtime.
7. No network download when the application starts.
8. Record the exact version, official source URL and SHA-256.

Verify the downloaded file using Python hashlib.

Add a test verifying:
- The file exists.
- The recorded version is correct.
- The SHA-256 matches.
- The application references the local file.
- No CDN reference exists.

If the official release does not provide the expected asset directly, inspect the official release/tag distribution and document the exact source used. Never invent a checksum.

## Data architecture

The backend supplies ONE JSON payload containing the available historical price history.

The browser must use this same payload for every chart period.

Do not make a new server request when the user changes periods.

Required period tabs:

- 1D
- 1W
- 1M
- 3M
- 6M
- 1Y
- 5Y

The frontend filters/slices the existing history client-side.

Preserve the original date formatting and period semantics from MarketChart.tsx.

Do not invent different date boundaries or financial calculations.

## Chart interactions

Implement:

1. Interactive period tabs.
2. Client-side history slicing.
3. Gradient area chart.
4. Crosshair.
5. Vertical and horizontal guide lines where appropriate.
6. Dark tooltip.
7. Date and price formatting.
8. Responsive chart dimensions.
9. Empty historical-data state.
10. Loading and unavailable states.

The chart must not require a server request for:
- Changing chart period.
- Moving the crosshair.
- Opening the tooltip.
- Updating hover information.

## Regression test port

Port:

`tests/test_chart_date_formatting.ts`

into a Python pytest equivalent.

Preserve:
- Date formatting.
- Date boundary behavior.
- Relevant timezone behavior.
- Original edge cases.

Do not weaken assertions.

## Tests to write first

- Historical payload structure.
- All seven periods.
- Client-side filtering.
- Empty history.
- Invalid dates.
- Timezone handling.
- Date formatting regression.
- Chart.js local asset integrity.
- No external CDN.
- No HTTP request triggered by period changes.

## Mandatory browser evidence

At 1440px and 390px, light and dark:

1. Load a real company.
2. Record the initial chart period.
3. Click 1D.
4. Click 1W.
5. Click 1M.
6. Click 3M.
7. Click 6M.
8. Click 1Y.
9. Click 5Y.
10. Hover over multiple chart positions.
11. Verify the crosshair.
12. Verify tooltip date and price.
13. Check browser network activity.

Report:
- What each interaction displayed.
- Whether chart data changed correctly.
- Whether the tooltip followed the pointer.
- Whether any server request occurred.
- Differences from the approved concept.

A test checking only JavaScript source text is insufficient.

## Acceptance criteria

- All seven periods work.
- One historical JSON payload is sufficient.
- Period switching makes no server request.
- Crosshair and tooltip work.
- Local Chart.js bundle loads.
- Original date-formatting regression passes.
- No concept sample data is present.

## Commit

`part 12: implement interactive market chart`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 12 "part 12: implement interactive market chart"`

---

# PART 13 — Deterministic Market Signals

## Goal

Port the original deterministic technical-analysis calculations.

Signals must be calculated using actual market data and the original TypeScript logic.

Do not use an LLM to generate or approximate deterministic signals.

## TypeScript files to read

1. E:\Quant-AI\client\src\lib\market.ts
2. E:\Quant-AI\client\src\components\Home.tsx
3. E:\Quant-AI\client\src\components\MetricCard.tsx

Inspect all relevant functions and calculation boundaries.

## Python files to create or extend

- api/web/signals.py
- api/research_schemas.py
- api/web/routes.py
- templates/partials/signal_score.html
- templates/partials/market_snapshot.html
- static/css/input.css
- tests/test_market_signals.py

Respect the exact target structure in MIGRATION_PLAN.md.

## Functionality

Preserve the original:
- Technical indicators.
- Signal calculations.
- Signal score.
- Buy/sell/neutral classification.
- Thresholds.
- Rounding.
- Missing-data behavior.
- Signal explanation.

The signal score ring must follow the approved concept.

Use the existing design tokens.

## Tests to write first

Test:

1. Each supported indicator.
2. Signal score calculations.
3. Buy classification.
4. Sell classification.
5. Neutral classification.
6. Threshold boundaries.
7. Missing price history.
8. Insufficient history.
9. Rounding behavior.
10. Deterministic repeatability.
11. Original output mapping.

Create controlled numerical fixtures.

Never use generated concept sample data.

## Browser evidence

At all four visual configurations:

- Search for a real company.
- Inspect the signal score ring.
- Inspect signal classification.
- Expand any signal details.
- Verify visual responsiveness.
- Verify the signal remains consistent when changing chart periods.
- Confirm changing chart periods does not trigger a server request.

Report the actual observed score and classification only when backed by the loaded real or controlled test data.

## Acceptance criteria

- Original calculations preserved.
- No AI-generated approximation.
- Correct signal classifications.
- Correct score ring.
- All numerical regression tests pass.
- Chart-period interactions remain independent.

## Commit

`part 13: implement deterministic market signals`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 13 "part 13: implement deterministic market signals"`

---

# PART 14 — Financial Fundamentals

## Goal

Port the original fundamental financial-health analysis.

Preserve the actual data sources, financial metrics, calculations and availability behavior.

## TypeScript files to read

1. E:\Quant-AI\client\src\lib\market.ts
2. E:\Quant-AI\client\src\components\Home.tsx
3. E:\Quant-AI\client\src\components\AnalysisPanel.tsx
4. E:\Quant-AI\client\src\components\MetricCard.tsx

Inspect the corresponding original Python service implementations:

- api/company_analysis_services.py
- api/market_intelligence_services.py
- api/research_services.py
- api/research_schemas.py

## Python files to create or extend

- api/web/fundamentals.py
- api/web/routes.py
- templates/partials/fundamentals.html
- templates/partials/metric_card.html
- templates/pages/home.html
- tests/test_fundamentals.py

Use the existing project structure and exact plan mapping.

## Functionality

Preserve every original financial-health metric.

For each metric:
- Correct label.
- Correct numerical value.
- Correct unit.
- Correct formatting.
- Correct source.
- Correct unavailable state.

Do not:
- Invent financial values.
- Replace missing values with zero.
- Treat missing data as a negative result.
- Change financial calculation formulas.
- Generate financial statements using AI when deterministic data is available.

Use the approved Apple-style card design.

## Tests to write first

Test:

1. Metric mapping.
2. Numerical formatting.
3. Currency formatting.
4. Percentage formatting.
5. Missing values.
6. Null values.
7. Invalid values.
8. Unavailable financial data.
9. Correct source attribution.
10. Existing fundamental-analysis behavior.

Use fixed fixtures with known expected results.

## Browser evidence

At all four visual configurations:

- Search for a real company.
- Inspect the financial fundamentals section.
- Expand and collapse sections.
- Inspect metric cards.
- Verify formatting and alignment.
- Check the mobile stacked layout.
- Verify unavailable states using controlled fixtures.

Report specific interactions and actual findings.

## Acceptance criteria

- All original fundamental metrics preserved.
- No invented values.
- Correct formatting.
- Correct unavailable behavior.
- Responsive layout.
- All existing and new tests pass.

## Commit

`part 14: implement financial fundamentals`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 14 "part 14: implement financial fundamentals"`

---

# PART 15 — Company Profile, Governance and Mapping

## Goal

Port the original company profile and executive governance experience.

This part must also port the original company workspace mapping regression test.

## TypeScript files to read

1. E:\Quant-AI\client\src\components\Home.tsx
2. E:\Quant-AI\client\src\components\AnalysisPanel.tsx
3. E:\Quant-AI\client\src\lib\research.ts
4. E:\Quant-AI\client\src\lib\market.ts
5. E:\Quant-AI\tests\test_company_workspace_mapping.ts

Inspect the associated original backend services:

- api/company_analysis_services.py
- api/research_services.py
- api/research_orchestrator.py
- api/research_schemas.py

## Python files to create or extend

- api/web/company_profile.py
- api/web/routes.py
- templates/partials/company_profile.html
- templates/partials/governance.html
- templates/pages/home.html
- tests/test_company_profile.py
- tests/test_governance.py
- tests/test_company_workspace_mapping.py

Follow MIGRATION_PLAN.md if the exact target filenames differ.

## Company profile

Preserve all original company profile fields.

Check:
- Company description.
- Sector.
- Industry.
- Exchange.
- Headquarters.
- Company metadata.
- Source information.
- Missing-data behavior.

Do not fabricate company information.

## Governance

Preserve the original executive roster and mapping.

For each executive, preserve available:
- Name.
- Position.
- Role.
- Relevant metadata.
- Source.
- Availability status.

Do not invent executives or titles.

## Company workspace mapping regression

Port:

`tests/test_company_workspace_mapping.ts`

into pytest.

This is mandatory.

Preserve all original assertions and verify:
- Correct company identity mapping.
- Correct workspace record association.
- Correct field mapping.
- Correct missing-data behavior.
- Correct partial research result mapping.
- Correct compatibility with Parts 09–14.

Do not simplify the mapping logic to make tests pass.

## Tests to write first

1. Company profile mapping.
2. Company metadata.
3. Missing company fields.
4. Executive roster mapping.
5. Executive role formatting.
6. Missing governance data.
7. Company workspace mapping regression.
8. Partial research results.
9. Incorrect company association protection.
10. Existing original test compatibility.

## Browser evidence

At all four visual configurations:

- Search for a real company.
- Inspect the company profile.
- Expand/collapse profile sections.
- Inspect governance roster.
- Verify long executive names do not break layout.
- Verify mobile layout at 390px.
- Verify missing governance data.
- Verify workspace data belongs to the selected company.

Report actual browser interactions and differences from the concept.

## Acceptance criteria

- Company profile parity.
- Governance roster parity.
- Correct source mapping.
- Original workspace mapping regression passes.
- No invented company or executive data.
- Existing research workflow remains functional.

## Commit

`part 15: implement company profile and governance`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 15 "part 15: implement company profile and governance"`

---

# 5. TEST EXECUTION POLICY

For EACH part:

### Step 1 — Tests first

Create focused tests before implementation.

### Step 2 — Implement

Implement only the current part.

Do not begin the next part early.

### Step 3 — Focused tests

Run the tests created for that part.

### Step 4 — Full regression

Run:

`.\.venv\Scripts\python.exe -m pytest`

The entire suite must pass.

### Step 5 — Fix failures

Maximum three fix attempts after the initial failure.

If tests still fail:
- Do not push.
- Do not mark the part complete.
- Report the failure.
- Stop the batch.

### Step 6 — Code review

Use code-review-and-quality.

Inspect:

`git diff`

Check:
- No secrets.
- No accidental source copies.
- No weakened assertions.
- No unrelated changes.
- No sample financial data.
- No unnecessary dependencies.

### Step 7 — Browser verification

Complete all four viewport/theme combinations.

For interactive parts, collect concrete interaction evidence.

If browser verification is unavailable, stop without pushing.

### Step 8 — Update progress

Mark only the current part complete.

Do not mark it complete until the push succeeds.

### Step 9 — Push

Use ONLY:

`.\.venv\Scripts\python.exe migration\push_part.py <part_no> "part NN: <message>"`

Never use git commit or git push directly.

---

# 6. REQUIRED COMMIT ORDER

| Part | Commit message |
|---|---|
| 11 | part 11: implement market quote and snapshot |
| 12 | part 12: implement interactive market chart |
| 13 | part 13: implement deterministic market signals |
| 14 | part 14: implement financial fundamentals |
| 15 | part 15: implement company profile and governance |

Exactly one commit per part.

Exactly five commits in this batch.

Never amend, squash or combine commits.

Never push a failing part.

---

# 7. FINAL BATCH REPORT

After Part 15 successfully pushes, stop.

Provide:

## A. Part-by-part results

For Parts 11–15:
- Implementation summary.
- Files created.
- Files modified.
- Tests added.
- Focused test results.
- Full pytest count.
- Commit SHA.
- Push confirmation.

## B. Financial correctness

Report:
- Negative price token verification.
- Positive/negative/neutral price tests.
- Chart period functionality.
- Chart data source.
- Signal calculation verification.
- Fundamentals mapping.
- Governance mapping.

## C. Browser evidence

For each part, report:

| Part | 1440 Light | 1440 Dark | 390 Light | 390 Dark |
|---|---|---|---|---|

Also include actual interaction evidence for:
- Price changes.
- Chart tabs.
- Crosshair and tooltip.
- Signal ring.
- Expand/collapse.
- Company profile.
- Governance.

Include differences discovered and fixes made.

Do not claim browser verification without actual observations.

## D. Regression integrity

Report:
- Initial test baseline: 96.
- Final collected pytest count.
- Total passing.
- Total failing.
- Original seven suite status.
- Chart date-formatting regression status.
- Company workspace mapping regression status.
- Any differences in original tests.

## E. Git verification

Confirm:
- Branch: main.
- Remote: correct.
- Five new commits.
- All five pushes successful.
- Working tree clean.
- Parts 01–15 checked.
- BATCH 03 complete.
- Day 2 in progress.

## F. Stop condition

Print exactly:

`BATCH COMPLETE, STOP`

Do not begin Part 16.

Do not begin BATCH_04.

Wait for my next instruction.

---

**FINAL RULE: Functional parity comes from E:\Quant-AI. Visual design comes from E:\QuantAI-design\Main.dc.html. Financial correctness comes before visual convenience. Never invent data, never weaken tests, and never skip verification.**
