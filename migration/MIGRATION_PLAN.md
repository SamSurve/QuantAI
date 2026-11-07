
# REPLACEMENT: SECTION 2 — MATH TECHNOLOGY MAPPING

| Original TypeScript technology | Python replacement | Reason |
|---|---|---|
| Streamdown Markdown rendering | markdown-it-py | Server-side Markdown rendering |
| Streamdown dollar-math support | mdit-py-plugins dollarmath | Inline and block dollar-math parsing |
| Browser-side math rendering | latex2mathml | Convert LaTeX expressions into MathML on the server |
| Streamdown code highlighting | Pygments | Server-side syntax highlighting |

Math rendering must use only:
- markdown-it-py
- mdit-py-plugins with dollarmath
- latex2mathml

The application must produce server-rendered MathML.

Do not install, vendor or load KaTeX.

Do not introduce a second JavaScript math-rendering engine.

Inline math and block math must both be tested.


---

# REPLACEMENT: SECTION 4 — ENVIRONMENT VARIABLE DISCOVERY

## Environment variable source of truth

Part 01 must inspect the actual contents of all 19 copied backend Python files.

Discover environment variables by examining:
- os.getenv(...)
- os.environ.get(...)
- os.environ[...]
- Pydantic BaseSettings configuration
- Existing settings/configuration helpers
- Other explicit environment-variable access in the original API backend

The actual original Python code is the authoritative source.

Do NOT assume that an audit environment-variable list is complete or correct.

Create .env.example from the variable names actually found in the original backend code.

Rules:

1. Include variable names only.
2. Never include actual values.
3. Never include placeholder credentials.
4. Never copy source .env files.
5. Do not include unused VITE_* variables.
6. Do not include unused OAuth template variables.
7. Preserve existing environment-variable names.
8. Report any discrepancy between the actual code and the audit's environment-variable list in the Part 01 summary.

If an environment variable listed by the audit is not actually used in the original backend code, do not silently add it as an active backend requirement.

If the original code uses a variable not listed in the audit, include its name in .env.example and report the discrepancy.


---

# REPLACEMENT: SECTION 5 — STATIC ASSET TREE

The final static vendor structure must be:

```text
static/
├── css/
│   ├── input.css
│   └── app.css
├── js/
├── vendor/
│   └── chart/
├── assets/
│   ├── analysts-ledger-briefing.jpg
│   ├── analysts-ledger-hero.jpg
│   ├── analysts-ledger-logo.png
│   └── analysts-ledger-market.jpg
└── dev/
```

Do not create static/vendor/katex/.

Math is converted into MathML on the server by latex2mathml.

Chart.js is stored locally under static/vendor/chart/.


---

# REPLACEMENT: SECTION 9 — TAILWIND, DESIGN SYSTEM AND STATIC ASSET POLICY

## 9.1 Tailwind standalone CLI

Version: Tailwind CSS 4.1.14.

Do not commit any Tailwind executable.

The downloaded binary must remain in tools/, which is gitignored.

scripts/build_css.py must:

1. Detect the current operating system and architecture.
2. Identify the matching official Tailwind 4.1.14 standalone release asset.
3. Obtain the release SHA-256 checksum from an official Tailwind checksum file if one is published.
4. Verify the downloaded binary against that official checksum.
5. If no official checksum file is published, download the correct official release asset over HTTPS, calculate its SHA-256, and store the calculated value in scripts/build_css.py with a clearly labelled comment identifying it as a locally calculated, pinned checksum.
6. Never invent or guess a SHA-256 value.
7. On subsequent runs, verify the downloaded executable against the stored checksum before execution.
8. Abort when checksum verification fails.
9. Abort on unsupported operating systems or architectures.
10. Execute the standalone binary without Node.js.
11. Scan Jinja2 templates and static JavaScript for Tailwind classes.
12. Generate static/css/app.css.
13. Support execution through Windows PowerShell.
14. Never invoke npm, npx, pnpm or an install script.

The Part 06 summary must explicitly state:

- Which official release asset was used.
- Whether an official checksum file was available.
- Whether a SHA-256 was obtained from an official published checksum or calculated locally.
- Where the checksum is pinned.
- Whether verification passed.

A locally calculated checksum must never be described as an official publisher checksum.

Commit generated CSS, not downloaded binaries.

## 9.2 Approved visual target

The original application functionality and behavior must remain intact.

However, the original client/src/index.css is NOT the visual target for the migrated application.

Use the approved Apple-style financial research terminal design below.

### Typography

Font stack:

```css
-apple-system,
"SF Pro Display",
Inter,
"Segoe UI",
sans-serif
```

Use:
- Tight letter spacing.
- Bold, large headlines.
- 56px hero headline.
- 56px main price.
- Clear editorial hierarchy.
- Restrained use of font weights and sizes.

Do not download or redistribute proprietary Apple fonts.

Use locally available system fonts and fallbacks.

### Light theme tokens

```css
--page: #f5f5f7;
--card: #ffffff;
--text: #1d1d1f;
--muted: #6e6e73;
--hairline: rgba(0, 0, 0, 0.08);

--accent: #0071e3;
--link: #0066cc;
--positive: #1a9c3c;
```

Cards:
- 22px corner radius.
- Soft shadows.
- White background.
- Subtle separators.

### Dark theme tokens

True black background:

```css
--page: #000000;
--card: #1c1c1e;
--fill: #2c2c2e;
--text: #f5f5f7;
--muted: #a1a1a6;
--hairline: rgba(255, 255, 255, 0.12);

--accent: #0071e3;
--link: #2997ff;
--positive: #30d158;
```

Do not replace true black with a dark grey page background.

Maintain readability and clear surface separation.

### Application components

Implement the following visual system:

1. Sticky frosted-glass header with backdrop blur.
2. Large editorial hero.
3. Pill-shaped search bar.
4. Pill-shaped quick-search chips.
5. iOS-style segmented controls.
6. Chart period segmented control.
7. Light/Dark/System segmented theme control.
8. Large price display.
9. Technical signal score ring.
10. Gradient area price chart.
11. Dashed crosshair.
12. Dark chart tooltip.
13. LIVE, CACHED and UNAVAILABLE status badges.
14. Rounded financial metric cards.
15. Executive research brief with editorial typography.
16. Floating "Ask the research desk" button.
17. Clean drawers, dialogs and expandable sections.

### Responsive behavior

At viewport widths below 900px:

- Metric grids must stack or adapt.
- Research panels must become single-column where appropriate.
- Navigation must hide.
- Search and chart controls must remain usable.
- Drawers and dialogs must fit the viewport.
- No horizontal overflow.

Desktop and mobile designs must both be implemented and visually inspected.

### Original CSS usage

Use original client/src/index.css only for any visual implementation details that the approved visual concept does not define.

If the original CSS conflicts with the approved visual tokens or component appearance, the new approved concept wins.

Do not blindly port the original palette or styling.

## 9.3 Local browser assets

The original four images must be copied from:

E:\Quant-AI\client\public\assets\

to:

static/assets/

The exact filenames are:

- analysts-ledger-briefing.jpg
- analysts-ledger-hero.jpg
- analysts-ledger-logo.png
- analysts-ledger-market.jpg

Chart.js must be vendored locally under static/vendor/chart/.

No essential functionality may depend on an external CDN.

## 9.4 Immediate browser interactions

The following interactions must not cause a server request:

- Light/Dark/System theme switching.
- Chart period switching.
- Chart history filtering.
- Drawers opening and closing.
- Modal opening and closing.
- Expand/collapse controls.
- Local navigation and section scrolling.

Send the full chart data as one JSON payload when the research response is loaded.

Slice this data client-side for 1D, 1W, 1M, 3M, 6M, 1Y and 5Y.

Do not send a new HTTP request each time the user selects a chart period.

Use JavaScript local state for instant interactions.

Search and new research requests remain server-backed.


---

# REPLACEMENT: PART 06 — VISUAL SYSTEM, TAILWIND AND ASSETS

**Goal:** Build the approved Apple-style financial research terminal design system while preserving the original QuantAI assets and functional requirements.

**Original files to read:**

- client/src/index.css
- client/index.html
- client/src/components/BrandMark.tsx
- client/src/components/MetricCard.tsx
- client/src/components/MarketChart.tsx
- client/src/components/ui/button.tsx
- client/src/components/ui/card.tsx
- client/src/components/ui/dialog.tsx
- client/src/components/ui/input.tsx
- client/src/components/ui/label.tsx
- client/src/components/ui/sheet.tsx
- client/src/components/ui/separator.tsx
- client/src/components/ui/skeleton.tsx
- client/src/components/ui/sonner.tsx
- client/src/components/ui/toggle.tsx
- client/src/components/ui/tooltip.tsx
- client/public/assets/analysts-ledger-briefing.jpg
- client/public/assets/analysts-ledger-hero.jpg
- client/public/assets/analysts-ledger-logo.png
- client/public/assets/analysts-ledger-market.jpg

**Files to create/update:**

- static/css/input.css
- static/css/app.css
- static/assets/analysts-ledger-briefing.jpg
- static/assets/analysts-ledger-hero.jpg
- static/assets/analysts-ledger-logo.png
- static/assets/analysts-ledger-market.jpg
- templates/macros/brand.html
- templates/macros/metric_card.html
- templates/macros/icon.html
- templates/macros/dialog.html
- scripts/build_css.py
- tests/test_css_build.py
- tests/test_static_assets.py

**Dependencies:** Part 05.

**Acceptance criteria:**

- Implement the complete approved visual token system in Section 9.
- Use the specified system font stack.
- Recreate the Apple-style header, cards, spacing and typography.
- Large hero headline is 56px.
- Main price typography is 56px.
- Cards use 22px radius.
- Light mode uses #f5f5f7 page background.
- Dark mode uses true #000000 page background.
- Buttons, links and positive colors match their specified tokens.
- Implement the pill search design.
- Implement pill shortcut chips.
- Implement segmented controls.
- Implement rounded reusable metric card macros.
- Support responsive layouts below 900px.
- Hide desktop navigation at mobile widths.
- Copy all four original images.
- Use Tailwind CSS 4.1.14 standalone CLI.
- Obtain official checksum when published.
- If no official checksum exists, calculate and locally pin the checksum with an explicit comment.
- Never invent or guess a checksum.
- Download binary into tools/.
- Never commit the binary.
- Commit generated static/css/app.css.
- No Node.js, npm, npx or pnpm.
- Original index.css is used only for styling not defined by the approved concept.

**Tests:**

- CLI version validation.
- Operating-system detection.
- Official checksum lookup, or local checksum pinning.
- SHA-256 verification.
- Failed checksum abort behavior.
- CSS output generation.
- Four static asset existence checks.
- Template macro rendering.
- Responsive design inspection.

**Required visual verification before push:**

Start the Python application and open it using the available browser tool.

Check:
- 1440px width, Light.
- 1440px width, Dark.
- 390px width, Light.
- 390px width, Dark.

Fix visible problems.

Report anything that remains unresolved.

If the browser tool is unavailable, report this and STOP the part without running push_part.py.

**Commit:**

part 06: recreate Apple-style visual system and assets


---

# REPLACEMENT: PART 19 — MARKDOWN, AI BRIEF AND PURE-PYTHON MATH RENDERING

**Goal:** Recreate the complete executive research analysis panel using safe server-side Markdown and MathML rendering.

**Original files to read:**

- client/src/components/AnalysisPanel.tsx
- client/src/pages/Home.tsx
- client/src/lib/market.ts
- Original Streamdown math configuration and usage.

**Files to create:**

- api/web/markdown.py
- templates/partials/analysis_brief.html
- templates/macros/markdown.html
- tests/test_analysis_brief.py
- tests/test_markdown_math.py
- tests/test_markdown_sanitization.py

**Dependencies:** Parts 03–04, 06, 09 and 18.

**Acceptance criteria:**

- Full executive analysis brief.
- Editorial lead quote extraction.
- Executive Assessment.
- Business Model.
- Financial Health.
- Growth Drivers.
- Competitive Position.
- Key Risks.
- Catalysts.
- Valuation View.
- What to Watch.
- Markdown headings and lists.
- Code block rendering.
- Pygments syntax highlighting.
- Inline math rendering.
- Block math rendering.
- Server-side MathML conversion.
- HTML sanitization.
- Shimmer loading skeleton.
- Non-blocking AI-unavailable banner.
- Deterministic financial data remains available when AI fails.

**Allowed math stack — no alternatives:**

1. markdown-it-py.
2. mdit-py-plugins with dollarmath.
3. latex2mathml.

All math conversion must occur on the Python server.

Use:
- `$...$` for inline math.
- `$$...$$` for block math.

Convert parsed LaTeX expressions into MathML using latex2mathml.

The generated HTML must contain valid MathML markup.

Do not install or vendor:
- KaTeX.
- MathJax.
- Browser-side LaTeX renderers.
- Any second math rendering engine.

Use Pygments for code block highlighting.

Apply HTML sanitization to rendered Markdown before returning it to the browser.

**Tests:**

- Each original structured analysis section.
- Lead quote extraction.
- Markdown headings.
- Inline lists.
- Code block rendering.
- Pygments output.
- Inline math: `$a^2+b^2=c^2$`.
- Block math: `$$a^2+b^2=c^2$$`.
- MathML output validation.
- Malformed math handling.
- Unsafe raw HTML sanitization.
- AI failure without loss of market data.

**Commit:**

part 19: implement AI brief and MathML rendering


---

# REPLACEMENT: PART 30 — FULL PARITY AND RELEASE AUDIT

**Goal:** Confirm complete behavioral parity with the original QuantAI product and visual compliance with the newly approved Apple-style design concept.

**Original files to review:**

- client/src/App.tsx
- client/src/pages/Home.tsx
- client/src/pages/NotFound.tsx
- client/src/components/AnalysisPanel.tsx
- client/src/components/BrandMark.tsx
- client/src/components/ChatPanel.tsx
- client/src/components/MarketChart.tsx
- client/src/components/MetricCard.tsx
- client/src/components/StartupReveal.tsx
- client/src/components/ThemeToggle.tsx
- client/src/contexts/ThemeContext.tsx
- client/src/hooks/useComposition.ts
- client/src/hooks/useMobile.tsx
- client/src/hooks/usePersistFn.ts
- client/src/lib/agentos.ts
- client/src/lib/market.ts
- client/src/lib/research.ts
- client/src/lib/utils.ts
- client/src/index.css
- client/index.html
- client/public/assets/*
- client/public/__manus__/debug-collector.js
- tests/*.ts

**Files to create/update:**

- PARITY_CHECKLIST.md
- tests/test_full_stack_parity.py
- tests/test_route_contracts.py
- tests/test_release_inventory.py
- README.md

**Dependencies:** Parts 01–29.

## Acceptance criteria

### Functional parity

- All 21 user-facing UI features work.
- All seven internal/infrastructure features work.
- All original research modes and parallel execution semantics remain intact.
- All financial metrics, units and calculation behavior remain intact.
- All seven chart time periods work.
- Client-side chart filtering is instant.
- Technical market signals remain deterministic.
- All fundamentals are preserved.
- Executive governance and competitor evidence are preserved.
- News and corporate events remain sourced and correctly ordered.
- Provenance and freshness remain available.
- AI research brief remains functional.
- Inline and block MathML rendering works.
- Chat sessions remain continuous.
- Recent research history works.
- Connection health works.
- Theme persists.
- Startup animation and error recovery work.
- Telemetry is correctly gated.
- Rate limits and concurrency controls are preserved.
- Cache TTLs and AI failover work.
- Existing API contracts remain unchanged.

### Visual parity against the NEW approved target

Visual parity means matching the Apple-style design concept in Section 9, NOT matching the original index.css.

Verify:

- Specified font stack.
- Specified typography and letter spacing.
- 56px hero headline.
- 56px main price.
- Specified light and dark color tokens.
- True-black dark mode.
- White/light cards and dark cards.
- 22px corner radius.
- Soft shadows and hairlines.
- Sticky frosted-glass header.
- Pill search input.
- Pill ticker shortcuts.
- iOS segmented controls.
- Technical signal score ring.
- Gradient area chart.
- Dashed chart crosshair.
- Dark chart tooltip.
- LIVE/CACHED/UNAVAILABLE badges.
- Floating Ask the research desk button.
- Responsive layout below 900px.
- Mobile navigation hiding.
- No horizontal overflow.

### Automated verification

- All seven original Python regression suites pass.
- All five converted TypeScript regression suites pass.
- All part-specific tests pass.
- Full python -m pytest -q passes.
- All API contract tests pass.
- Security tests pass.
- Chart period and date formatting tests pass.
- MathML tests pass.
- Cache and provider tests pass.
- Static asset checks pass.
- Deployment configuration tests pass.

### Repository cleanliness

The new repository must not contain:

- .ts files.
- .tsx files.
- React application source.
- package.json.
- pnpm-lock.yaml.
- node_modules.
- Vite build infrastructure.
- Node.js build or runtime requirements.
- Secrets.
- .env files other than the names-only .env.example.
- Downloaded Tailwind binaries.
- Python runtime caches.

### Vercel verification honesty

A passing local configuration test is not proof of a successful Vercel deployment.

README must clearly identify which Vercel runtime, packaging, route and CDN behaviors have not been verified because no real deployment was performed.

Do not claim successful production deployment without actual evidence.

### Required final visual inspection

Use the available browser tool to inspect:

- 1440px Light.
- 1440px Dark.
- 390px Light.
- 390px Dark.

If no browser tool is available, stop and report that visual verification was not possible. Never claim visual parity without inspection.

**Tests:**

- Full pytest suite.
- Browser smoke tests if available.
- Mocked AAPL, MSFT, NVDA and TSLA research workflows.
- Optional live test with QUANTAI_LIVE_SMOKE=1.
- Final deployment configuration tests.
- Static and import inventory.

**Commit:**

part 30: complete migration and verify feature parity

---

# MIGRATION PLAN ADDENDUM — PARTS 21–25

**Authority:** This addendum is part of `migration/MIGRATION_PLAN.md` and is authoritative for Parts 21–25. `BATCH_05.md` must mirror the acceptance criteria in this addendum verbatim, one criterion per item. If a batch prompt differs, this migration-plan addendum wins.

**Source of the criteria:** Owner-provided original Step D text for Parts 21–25. The acceptance-criteria bullets below are copied verbatim from that text. Owner-approved corrections and additional controls are clearly separated from those original criteria.

---

## Cross-part execution and protection rules — Parts 21–25

1. Inspect and reuse the implementation from earlier parts before creating or rebuilding anything. In particular, Part 21 must extend the chat files already introduced in Part 20; Part 24 and Part 25 are primarily verification of existing backend behavior.
2. Write focused tests before implementation. Demonstrate that each new test detects the intended behavior before changing production code.
3. Verify FastAPI, Starlette, HTTPX, browser, Python, pytest, and other framework/library usage against their official documentation. Do not guess API behavior.
4. Do not use or install third-party skills. Do not add a skills declaration section or skill-usage line to reports.
5. Do not use the built-in permissioned-GitHub skill, GitHub connectors, IDE Git integration, direct Git commands, or any other tool for Git operations. `migration/push_part.py` is the sole permitted Git-operation interface. Invoke it using the exact PowerShell command for the current part. If the script cannot complete or report the required verification, stop; do not use another Git tool as a workaround.
6. Do not use slash commands such as `/spec`, `/plan`, `/build`, `/ship`, or `/land-and-deploy`. Do not create issues, tickets, pull requests, specs, or additional planning/report documents. Only update the existing `migration/PROGRESS.md` and the files explicitly listed in the migration plan, in addition to part-specific implementation and test files.
7. The original repository `E:\Quant-AI` is read-only. Do not modify it. Preserve original backend behavior, API contracts, and original test assertions in the Python migration.
8. `tests/test_production_readiness.py` and `tests/test_provider_failover.py` are original baseline suites. Never overwrite, edit, delete, skip, weaken, or relax either file. Preserve every other original baseline test as well. Record pre-batch and post-batch SHA-256 hashes of both protected files and prove they are identical.
9. New test fixtures must use unmistakably fake data, such as `Testco`, `TST`, and `100.00`. Never use sample values from `Main.dc.html`, screenshots, mockups, or prior visual reports as production values or test fixtures.
10. Do not add a package unless the owner explicitly approves it. If a dependency appears necessary, stop and report its exact name, pinned version, official package/release URL, and publication/release date proving it is at least 14 days old; include the proposed install/import check. Do not install it without approval. No unapproved package may be added to a requirements file or lock file.
11. Never print, expose, log, or commit API keys, credentials, tokens, `.env` values, cookies, or secret-bearing payloads. Keep provider secrets server-side.
12. Never return raw Python exceptions, traceback text, internal file paths, prompt templates, credentials, or secret-bearing diagnostics to browser clients. Capture diagnostics server-side and return normalized public errors.
13. No server-side code may fetch a user-supplied URL. Do not create URL proxies, self-HTTP requests, or server-side hops through the configured AgentOS URL. Research routes must call the research orchestrator in-process.
14. Security-sensitive inputs must be explicitly validated and bounded. Reject malformed or oversized requests safely. Resolve client IPs only through a correctly configured trusted-proxy policy; do not blindly trust arbitrary `X-Forwarded-For` values.
15. Before each part's push, inspect the complete proposed part change set and its staged export using the mechanisms supported by `push_part.py`. Confirm it contains only that part's authorized files. If the script cannot prove the staged change set is isolated from unrelated uncommitted work, stop; do not use direct Git commands or another Git tool.
16. A part is complete only after its tests pass, review passes, required browser checks pass, `PROGRESS.md` is updated, and `push_part.py` reports a successful push and the required remote verification.

### Mandatory browser evidence for every UI-affecting part

1. Use a real browser to inspect the approved concept at `E:\QuantAI-design\Main.dc.html` and the running Python application separately.
2. Measure actual browser `getComputedStyle()` values on both pages. Never copy the concept column from CSS source, inline declarations, screenshots, previous reports, or memory.
3. Record the four configurations independently: 1440px Light, 1440px Dark, 390px Light, and 390px Dark. Do not combine mobile Light and Dark into one result.
4. Record at least two meaningful computed-style properties per relevant component in each applicable configuration, with the actual concept selector/element and app selector/element identified.
5. If a drawer/dialog has no equivalent in the concept, report exactly: `No concept equivalent — no direct concept measurement is available.` Do not invent a concept comparator.
6. For every tested interaction, capture actual browser Network-panel or equivalent instrumentation counts immediately before and after. Identify the request types and URLs/categories involved. A no-request interaction must show equal before/after counts. An interaction that intentionally performs a request must show the actual delta and explain it.
7. Capture browser evidence/screenshots, check console errors, and check for overflow, clipping, keyboard/focus issues, and theme regressions. If the browser is unavailable, stop the affected UI part and do not push it.

---

# PART 21 — CHAT CONTINUITY AND QUICK PROMPTS

**Goal:** Complete chat continuity and controls while preserving the original chat behavior and exact original quick-prompt strings.

**Original files to read (verified against `AUDIT.md`):**

- `client/src/components/ChatPanel.tsx`
- `client/src/lib/agentos.ts`
- `client/src/pages/Home.tsx`

**Files to create or update:**

- Update existing `api/web/chat.py` (created/introduced in Part 20; reuse it, do not recreate it).
- Update existing `templates/partials/chat_drawer.html` (introduced in Part 20; reuse it).
- Update existing `static/js/chat.js` (introduced in Part 20; reuse it).
- Create `tests/test_chat_session.py`.
- Create `tests/test_chat_quick_prompts.py`.
- Create `tests/test_news_dedup_distinct_publishers.py` for the owner-approved Part 16 regression guard; production news code is changed only if this test fails.

**Dependencies:** Part 20.

**Acceptance criteria — verbatim from the owner-provided Step D:**

1. Session reuse.
2. Ordered message history.
3. Turn counter.
4. Three original quick prompts.
5. Correct message submission.
6. Session continuity.

**Tests — verbatim from the owner-provided Step D:**

1. Multiple turns.
2. Session reuse.
3. Turn counter.
4. Quick prompts.
5. Message ordering.
6. Session errors.

**Additional owner-approved requirements:**

1. Before changing the Part 20 quick prompts, inspect `client/src/components/ChatPanel.tsx` and report the exact original strings, preserving spelling, capitalization, punctuation, and order. The expected strings to verify are `Pressure-test the thesis`, `Trace the source lane`, and `Separate evidence from interpretation`. The actual original source is authoritative; if it differs, report the discrepancy and stop before replacing any values.
2. Replace Part 20's incorrect prompts `Catalysts & risks`, `Operating margin`, and `Peer context` with the exact strings confirmed from the original source. Add tests proving the three original prompts are present and actionable and the incorrect Part 20 prompts are no longer used.
3. Demonstrate two real browser chat messages in one conversation. Record the exact message 1 and message 2, the session ID after each message, whether those IDs are identical, the initial turn counter and observed counter after each message, and browser request counts before message 1, after message 1, and after message 2. Count AgentOS requests separately from `/api/chat/render` requests and report unexpected requests. Evidence must come from the real browser Network panel or equivalent instrumentation, not source inspection or direct Python calls.
4. Add a news regression test with two articles that have the same headline, different publishers, and different URLs. Both must remain. Run the test against the existing Part 16 implementation first. Change production news code only if the test fails; preserve genuine duplicate-URL deduplication.
5. Inspect Part 20 commit `28dca40ed8231ebd9560ac3babb400e419138dd4` and its `api/index.py` change, comparing it with that commit's parent version and `E:\Quant-AI\api\index.py`. Report every import, middleware, route/router registration, application configuration, response/status behavior, and error-handling change. State whether any original backend contract changed and support the conclusion with tests. Do not make unrelated changes to `api/index.py`.
6. Preserve session errors, loading/failure states, ordered message display, and the existing safe Markdown rendering behavior.

**Validation commands (PowerShell):**

```powershell
cd E:\QuantAI-Python
.\.venv\Scripts\python.exe -m pytest tests/test_chat_session.py tests/test_chat_quick_prompts.py tests/test_news_dedup_distinct_publishers.py -q
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

Run the full browser verification matrix and interaction request-count evidence described in the cross-part rules before pushing.

**Commit:**

```powershell
.\.venv\Scripts\python.exe migration\push_part.py 21 "part 21: complete chat continuity and controls"
```

---

# PART 22 — ACTIVITY, CONNECTION SETTINGS AND SSRF PROTECTION

**Goal:** Implement recent activity and connection settings while enforcing the strict browser/server network boundary.

**Original files to read (verified against `AUDIT.md`):**

- `client/src/pages/Home.tsx` (the exact audited path; not a root-level `Home.tsx`).
- `client/src/lib/agentos.ts`.
- `client/src/const.ts`.

**Files to create or update:**

- Create `api/web/activity.py`.
- Create `api/web/connection.py`.
- Create `templates/partials/recent_activity.html`.
- Create `templates/partials/connection_health.html`.
- Create `templates/partials/endpoint_settings.html`.
- Create `static/js/connection.js`.
- Create `tests/test_activity_tracker.py`.
- Create `tests/test_connection_settings.py`.
- Create `tests/test_backend_url_ssrf.py`.

**Path note:** The owner-provided Step D groups `connection_health.html` and `endpoint_settings.html` after `templates/partials/recent_activity.html`; the `templates/partials/` prefix is applied to both as the grouped target directory. These are new target paths, not original source paths. Confirm the existing template convention before creation; if the repository structure contradicts this grouping, stop and report rather than silently choosing another path.

**Dependencies:** Parts 05–09 and 21.

**Acceptance criteria — verbatim from the owner-provided Step D:**

1. Five recent searches.
2. Query label, mode, completion and confidence.
3. Ready, Checking and Offline.
4. Refresh/re-check button.
5. Endpoint settings dialog.
6. Browser storage key analysts-ledger-agentos-url.
7. Custom endpoint used ONLY by browser-side JS for health checks and AgentOS chat.
8. Research server routes call orchestrator in-process.
9. No self-HTTP requests.
10. Server never fetches user-supplied URLs.
11. User-provided backend URL values cannot trigger server-side outbound requests.

**Tests — verbatim from the owner-provided Step D:**

1. Activity ordering.
2. Five-item limit.
3. Connection statuses.
4. URL persistence in browser.
5. Backend URL passed to a server request is ignored.
6. No HTTPX request to the user-supplied host.
7. Browser chat and health logic isolated from server research.

**Additional owner-approved security requirements:**

1. The localStorage key is exactly `analysts-ledger-agentos-url`. It is browser storage only. Browser-side JavaScript may use the configured value for health checks and AgentOS chat. Python server code must not read that key, accept it as a server fetch destination, resolve it, or use HTTPX/another client to contact it.
2. Research server routes call the Python research orchestrator directly in-process. Do not self-HTTP to the application's own route and do not proxy browser-supplied URLs.
3. Test loopback (`127.0.0.1`), link-local/cloud metadata (`169.254.169.254`), private IPv4 ranges (including `10.0.0.0/8`), private IPv6, and DNS names that resolve to prohibited addresses. Include a controlled DNS-rebinding scenario. Use mocked HTTP clients/resolvers; never contact these destinations.
4. Add tests proving that sending a user-provided backend URL to a server route is ignored and creates zero HTTPX outbound requests to that host. Verify browser chat/health code uses the browser-side endpoint while server research stays in-process.
5. Validate endpoint input on the browser side for correct URL structure and safe user feedback, but do not mistake browser validation for server-side SSRF protection. The server must not fetch it at all.
6. Do not print or expose configured URLs if they contain credentials or sensitive query values. Do not expose provider secrets.
7. Connection states must use the exact semantic labels `Ready`, `Checking`, and `Offline` (case/presentation may follow the established UI convention while preserving these states). Handle timeout and failure states without exposing raw exceptions.

**Validation commands (PowerShell):**

```powershell
cd E:\QuantAI-Python
.\.venv\Scripts\python.exe -m pytest tests/test_activity_tracker.py tests/test_connection_settings.py tests/test_backend_url_ssrf.py -q
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

Run the full browser verification matrix. For saving endpoint settings, refresh/re-check, and chat/health actions, record actual browser request counts before and after each interaction and distinguish browser-to-AgentOS traffic from application-server requests. Prove that changing/saving the endpoint never triggers a server-side outbound request.

**Commit:**

```powershell
.\.venv\Scripts\python.exe migration\push_part.py 22 "part 22: implement activity settings and SSRF protection"
```

---

# PART 23 — STARTUP, RESPONSIVE APPLICATION AND ERROR RECOVERY

**Goal:** Complete application startup, responsiveness, keyboard accessibility, and error recovery without breaking existing research workflows.

**Original files to read (verified against `AUDIT.md`):**

- `client/src/App.tsx`.
- `client/src/pages/NotFound.tsx`.
- `client/src/components/StartupReveal.tsx`.
- `client/src/components/ErrorBoundary.tsx`.
- `client/src/hooks/useMobile.tsx`.
- `client/src/components/BrandMark.tsx`.

**Files to create or update:**

- Create `static/js/app.js`.
- Create `templates/partials/startup_reveal.html`.
- Create `templates/pages/not_found.html`.
- Create `tests/test_ui_resilience.py`.
- Create `tests/test_responsive_layout.py`.

**Dependencies:** Parts 05–22.

**Acceptance criteria — verbatim from the owner-provided Step D:**

1. Original 1.2-second reveal.
2. Reduced-motion support.
3. Error recovery.
4. Reload action.
5. Responsive layout.
6. Original anchor IDs.
7. Keyboard-accessible dialogs.
8. Focus management.
9. Toast notifications.
10. No broken layout after research errors.

**Tests — verbatim from the owner-provided Step D:**

1. Reduced motion.
2. Startup.
3. Recovery.
4. 404.
5. Anchor links.
6. Keyboard interaction.
7. Desktop/mobile visual tests.

**Additional implementation and verification rules:**

1. Reuse existing base templates, dialog macros, theme controller, error handling, and toast implementation wherever they already satisfy the requirement. Do not duplicate an existing solution.
2. Preserve the original 1.2-second startup reveal timing and respect `prefers-reduced-motion`; reduced-motion users must not be forced to wait for decorative animation.
3. Error recovery and reload controls must be keyboard accessible. Ensure focus is moved into dialogs when opened, trapped only while the dialog is modal, and restored to the invoking control when closed. Verify Escape and keyboard navigation.
4. Preserve the original anchor IDs and confirm each navigation target exists in the migrated page.
5. Research/API errors must not collapse, corrupt, or overflow the rest of the workspace. Error/empty/loading states must remain understandable.
6. Use no new package unless the owner separately approves it under the cross-part dependency rule.

**Validation commands (PowerShell):**

```powershell
cd E:\QuantAI-Python
.\.venv\Scripts\python.exe -m pytest tests/test_ui_resilience.py tests/test_responsive_layout.py -q
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

Run real-browser checks at 1440px Light, 1440px Dark, 390px Light, and 390px Dark. Measure concept and app independently using `getComputedStyle()`. For reduced-motion preference, startup reveal, dialog open/close, toast, reload/recovery and anchor navigation, record before/after browser request counts. Identify interactions expected to be local-only and prove zero additional requests.

**Commit:**

```powershell
.\.venv\Scripts\python.exe migration\push_part.py 23 "part 23: complete application UI resilience"
```

---

# PART 24 — API SECURITY AND REQUEST PROTECTION

**Goal:** Verify and preserve API security, input limits, request identity, concurrency/rate controls, safe client-IP handling, and public error sanitization.

**Original files to read (verified against `AUDIT.md`):**

- `api/index.py`.
- `api/research_protection.py`.
- `api/research_errors.py`.
- `api/research_logging.py`.
- `client/src/lib/research.ts`.
- `client/src/lib/agentos.ts`.

**Files to create or update:**

- Add new tests only in `tests/test_api_security.py`.
- Do not edit `tests/test_production_readiness.py` or any other original baseline suite.
- Do not modify the original backend modules unless a new failing test proves a specific defect or an exact requirement cannot otherwise be met. If a production change is necessary, make the smallest correction and report the complete diff and reason.

**Dependencies:** Parts 01–23.

**Acceptance criteria — verbatim from the owner-provided Step D:**

1. 8192-byte research body limit.
2. 8192-byte AgentOS body limit.
3. 10 requests per 60 seconds per client IP per process.
4. Four concurrent protected research operations per process.
5. Correct sliding-window reset.
6. Request IDs.
7. Server-only diagnostics.
8. Public exception sanitization.
9. Cache-Control no-store.
10. Safe forwarded-IP handling.
11. Provider secrets never appear in browser content.

**Tests — verbatim from the owner-provided Step D:**

1. Payload size.
2. Rate limit.
3. Window reset.
4. Concurrency.
5. Error sanitization.
6. Request ID.
7. Security headers.
8. Existing production readiness tests.

**Additional owner-approved security requirements:**

1. Treat Parts 24 and 25 primarily as verification. Write tests first against existing code. If those tests pass, add tests only and do not rewrite backend code for cosmetic or stylistic reasons.
2. Keep the research body limit at exactly 8,192 bytes and AgentOS body limit at exactly 8,192 bytes. Test both below and above the boundary, and prove the correct public status/error behavior.
3. Verify a sliding-window limit of 10 requests in 60 seconds per client IP per process, including precise reset/expiration behavior. Verify the maximum of four concurrent protected research operations per process and that capacity is released on success and failure.
4. Verify request IDs are created/propagated safely and appear in the appropriate response/log context without exposing sensitive internals.
5. Server logs may contain controlled diagnostic details, but public responses must never include raw exceptions, stack traces, local paths, prompts, provider credentials, or secret-bearing request payloads.
6. Verify `Cache-Control: no-store` on all required `/api/*` responses according to the established deployment behavior.
7. Forwarded IP handling must use the configured trusted-proxy policy and must not allow an untrusted client to spoof its address by supplying arbitrary `X-Forwarded-For` values. Cover single-hop and multi-hop cases if supported by the existing implementation and plan.
8. Provider keys and secret configuration must never appear in HTML, JavaScript, JSON responses, browser storage, or browser-visible error messages.
9. SSRF boundary remains strict: no server-side fetch of user-supplied URLs, including any URL originating from browser localStorage. No self-HTTP request is allowed.
10. Validate malformed headers, malformed payloads, unsupported content types, and oversized bodies with safe, deterministic public errors.
11. Do not add packages. If a package is believed necessary, stop and request owner approval under the cross-part dependency rule.
12. `tests/test_production_readiness.py` is an original baseline suite and must run unchanged. Record and compare its SHA-256 before and after the batch.

**Validation commands (PowerShell):**

```powershell
cd E:\QuantAI-Python
.\.venv\Scripts\python.exe -m pytest tests/test_api_security.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_production_readiness.py -q
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

If all tests prove that existing backend behavior already satisfies these requirements, do not change backend files. Report this honestly as test-only verification.

**Commit:**

```powershell
.\.venv\Scripts\python.exe migration\push_part.py 24 "part 24: harden API security and request protection"
```

---

# PART 25 — TTL CACHE AND PROVIDER FAILOVER

**Goal:** Verify and preserve cache TTL behavior and the configured sequential AI provider failover chain.

**Original files to read (verified against `AUDIT.md`):**

- `api/research_cache.py`.
- `api/ai_providers.py`.
- `api/research_orchestrator.py`.
- `api/market_intelligence_services.py`.
- `client/src/pages/Home.tsx`.
- `client/src/components/AnalysisPanel.tsx`.

**Files to create or update:**

- Create `tests/test_provider_failover_web.py`.
- Create `tests/test_research_cache_ttl.py`.
- Never overwrite or edit original `tests/test_provider_failover.py`.
- Never edit `tests/test_production_readiness.py`.
- Do not modify original backend modules unless a new failing test proves a specific defect or an exact requirement cannot otherwise be met. If a production change is necessary, make the smallest correction and report the complete diff and reason.

**Dependencies:** Parts 09, 19, 21, and 24.

**Acceptance criteria — verbatim from the owner-provided Step D:**

1. Quotes 60 s.
2. History 300 s.
3. News 300 s.
4. Events 21,600 s.
5. Entity resolution 86,400 s.
6. Provider cooldown 300 s.
7. Groq Primary -> Groq Secondary -> OpenRouter Ox Alpha.
8. Provider ordering configurable.
9. Sequential fallback.
10. AI failure non-blocking.
11. No unapproved change to process-local caching.

**Tests — verbatim from the owner-provided Step D:**

1. TTLs.
2. Hit/miss.
3. Expiration.
4. Provider order.
5. Provider failures.
6. Circuit cooldown.
7. All providers unavailable.
8. Existing failover regression suite.

**Additional owner-approved verification rules:**

1. Part 25 is primarily verification. Write tests first against the existing cache and provider implementation. If the tests pass, add tests only; do not rewrite the backend.
2. Preserve process-local caching. Do not add Redis, a database, distributed cache, or another storage layer. Do not change TTL values, cache keys, cache invalidation, or cache architecture without a failing test and a plan-authorized reason.
3. Verify these exact TTLs: quote 60 seconds; historical series 300 seconds; news 300 seconds; events 21,600 seconds; entity resolution 86,400 seconds; provider error/circuit cooldown 300 seconds.
4. Verify hit/miss behavior and expiration using a controllable/fake clock where practical. Do not sleep for long real-world TTL periods.
5. Verify sequential provider failover in this exact order unless the existing configured provider ordering explicitly overrides the order: Groq Primary, Groq Secondary, OpenRouter Ox Alpha. Verify provider ordering is configurable and that calls are sequential, not parallel.
6. Verify failures advance to the next provider, circuit cooldown is honored, and all-providers-unavailable produces a safe normalized AI-unavailable result without taking down deterministic market/research data.
7. Use only the new tests `tests/test_provider_failover_web.py` and `tests/test_research_cache_ttl.py` for this part. Keep the original `tests/test_provider_failover.py` unchanged and run it as a regression suite.
8. Provider tests must mock all external providers. Never print API keys or send real provider requests during tests.
9. If existing behavior passes every test, do not change `api/research_cache.py`, `api/ai_providers.py`, `api/research_orchestrator.py`, or `api/market_intelligence_services.py`. Report test-only verification honestly.

**Validation commands (PowerShell):**

```powershell
cd E:\QuantAI-Python
.\.venv\Scripts\python.exe -m pytest tests/test_provider_failover_web.py tests/test_research_cache_ttl.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_provider_failover.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_production_readiness.py -q
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

**Commit:**

```powershell
.\.venv\Scripts\python.exe migration\push_part.py 25 "part 25: preserve caching and AI failover"
```

---

## Part 21–25 completion boundary

After Part 25 only:

1. Re-run the full test suite and Ruff.
2. Verify the hashes of `tests/test_production_readiness.py` and `tests/test_provider_failover.py` match their pre-batch hashes.
3. Verify all five part pushes succeeded through `migration/push_part.py` and each part has one part-specific commit.
4. Complete the six-section final report required by `BATCH_05.md`.
5. Write the end-of-batch retrospective in that final report: what went wrong, what was corrected, and which permanent rule should be added. Do not create a separate retrospective document.
6. Stop. Do not start Part 26 or BATCH_06.
