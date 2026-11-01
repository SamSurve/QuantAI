
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
