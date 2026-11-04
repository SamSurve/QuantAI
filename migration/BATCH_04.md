
# BATCH_04.md — News, Events, Evidence, AI Brief and AgentOS Chat

**Project:** QuantAI Python Migration  
**Repository:** https://github.com/SamSurve/QuantAI.git  
**Branch:** main  
**Working directory:** E:\QuantAI-Python  
**Original source:** E:\Quant-AI (READ-ONLY)  
**Approved design:** E:\QuantAI-design\Main.dc.html  
**Batch:** 04 of 06  
**Day:** 2 of 3  
**Parts:** 16–20  
**Required commits:** 5  
**Required pushes:** 5  
**Python:** 3.12.7

---

# 0. MANDATORY PRE-FLIGHT

Read completely:

1. migration/MIGRATION_PLAN.md
2. migration/PROGRESS.md
3. migration/MASTER_PROMPT.md
4. migration/BATCH_04.md

Verify:

- Parts 01–15 are checked.
- Exactly 15 migration commits exist on main.
- The latest commit is Part 15.
- All previous pushes succeeded.
- Working tree is clean.
- The virtual environment works.
- Full pytest passes before starting.

Use:

`.\.venv\Scripts\python.exe`

Verify the repository:

`https://github.com/SamSurve/QuantAI.git`

Do not modify:

`E:\Quant-AI`

Do not begin BATCH_05.

## 0.1 Acceptance-criteria reconciliation

IMPORTANT:

The original AUDIT.md is the source inventory available for this prompt.

The local MIGRATION_PLAN.md is authoritative for exact part dependencies, target Python files and additional acceptance criteria.

Before each part:

1. Open its corresponding section in MIGRATION_PLAN.md.
2. Copy every acceptance criterion into the current part's working checklist.
3. Preserve every criterion in the original wording.
4. Add the explicit criteria in this batch.
5. Verify that no criterion has been omitted.

Do not replace multiple criteria with phrases such as:
- All original fields.
- Full parity.
- Everything works.
- Complete implementation.

If the local plan has additional requirements, they are mandatory.

If a file path cannot be confirmed against AUDIT.md or the actual source repository, label it:

`ASSUMPTION — verify before implementation`

Never silently convert an assumption into a verified path.

If the plan conflicts with the original source, stop and report the discrepancy.

---

# 1. BATCH_03 REVIEW ITEMS

Before Part 16, inspect the following previous implementation details.

### 1.1 Part 15 schema modification

The previous batch added:

`FreshnessState.NOT_REQUESTED`

to:

`api/research_schemas.py`

This was reported as necessary for the workspace mapping regression.

Review whether the same compatibility behavior can be achieved by extending:

`api/web/contracts.py`

Do not revert the existing behavior blindly.

Do not break the Part 15 regression test.

Do not make additional changes to original backend contracts unless the migration plan explicitly requires them.

Report the reason for any unavoidable original backend modification.

### 1.2 Existing signal implementation

Preserve the existing deterministic signal output.

Classifications are:

- BULLISH
- NEUTRAL
- BEARISH

Do not introduce BUY or SELL classifications.

### 1.3 Existing chart

Preserve:
- Chart.js 4.4.7.
- Local vendor file.
- Existing SHA-256 verification.
- Seven period tabs.
- Single historical JSON payload.
- Client-side filtering.
- Crosshair.
- Tooltip.

Do not rewrite the chart.

Do not introduce a second charting implementation.

### 1.4 Existing financial fundamentals

Preserve:
- EPS.
- Profit Margin.
- Total Cash.
- Total Debt.
- Operating Margin.
- Fiscal period end.
- Revenue.
- Net Income.
- Free Cash Flow.
- Price-to-Sales.
- ROE.
- ROA.

Preserve strict null handling.

---

# 2. GLOBAL RULES

## 2.1 Functional source of truth

Original TypeScript functionality determines behavior.

Approved design concept determines appearance.

Real backend responses determine application data.

Never use sample data from:

`E:\QuantAI-design\Main.dc.html`

## 2.2 Fake test fixtures

NEW MANDATORY RULE:

All newly introduced controlled fixtures must use clearly artificial data.

Example:

Company: `Testco`

Ticker: `TST`

Price: `100.00`

News headline: `Testco announces fictional test update`

Publisher: `Example Test Publisher`

Event: `Testco fictional quarterly event`

Do not use:
- Apple sample figures.
- Design concept prices.
- Design concept chart points.
- Design concept news.
- Design concept dates.
- Design concept financial metrics.
- Design concept event records.

No number from the design concept may appear in any newly created production template, application page or test fixture.

Use inline Python dictionaries or existing test fixtures where possible.

Do not create extra production routes or unrelated fixture files.

A test-only fixture must never become production application data.

## 2.3 Contract protection

Do not edit:

- api/research_schemas.py
- api/market_intelligence_services.py
- api/research_orchestrator.py
- api/ai_providers.py
- api/groq_finance_agent.py

unless the migration plan explicitly permits it or a genuine compatibility requirement makes it unavoidable.

Prefer extensions in:

`api/web/contracts.py`

and presentation adapters under:

`api/web/`

If a change to an original backend file is unavoidable:

1. Explain why.
2. Identify the exact contract affected.
3. Show why a web-layer extension is insufficient.
4. Add regression tests.
5. Report the change in the final summary.

Never modify provider credentials or environment configuration.

## 2.4 API key protection

NEVER print:
- GROQ_API_KEY_PRIMARY.
- GROQ_API_KEY_SECONDARY.
- OPENROUTER_API_KEY.
- Any other provider credential.

Never print `.env` contents.

Never include secrets in test failure messages.

Use mocked providers for Part 19 and mocked AgentOS responses for Part 20.

Tests must not make real paid AI calls.

## 2.5 Existing tests

Initial baseline:

142 passing tests.

Never:
- Delete existing tests.
- Weaken assertions.
- Add blanket skips.
- Change expected values merely to make implementation pass.
- Suppress failures.

If an existing test requires a legitimate compatibility adjustment, report the exact diff and reason.

## 2.6 Skills

Mandatory for every part:

- test-driven-development
- source-driven-development
- frontend-ui-engineering
- code-review-and-quality

Reference only:

- git-workflow-and-versioning

Print at the start of each part:

`Skills used: test-driven-development, source-driven-development, frontend-ui-engineering, code-review-and-quality`

Follow official documentation when implementing:
- FastAPI.
- Jinja2.
- HTMX.
- markdown-it-py.
- mdit-py-plugins.
- latex2mathml.
- Pygments.
- pytest.

Do not guess API behavior.

Never run:
- /spec
- /plan
- /build
- /build auto

Do not install Node.js, npm, npx or pnpm.

---

# 3. VISUAL VERIFICATION

Before each of the five pushes:

Open:
- Running QuantAI Python application.
- E:\QuantAI-design\Main.dc.html.

Compare side by side.

Required:

| Viewport | Theme |
|---|---|
| 1440px | Light |
| 1440px | Dark |
| 390px | Light |
| 390px | Dark |

## 3.1 NEW: Measured visual difference requirement

For EACH part, provide at least TWO concrete visual comparisons against the design concept.

Valid evidence includes:

- Heading font size: concept 22px, application 20px.
- Card padding: concept 28px, application 24px.
- Border radius: concept 22px, application 20px.
- Card background: concept #ffffff, application #f5f5f7.
- Text color.
- Shadow values.
- Line height.
- Button dimensions.
- Typography weight.
- Measured spacing.

For each difference:

1. Record the concept measurement.
2. Record the application measurement.
3. Explain the difference.
4. State the correction made.
5. Reinspect after correction.

If two or more properties are genuinely identical, state exactly what was measured and report identical values for both.

Example:

| Property | Concept | Application | Result |
|---|---|---|---|
| Card radius | 22px | 24px | Corrected to 22px |
| Card padding | 28px | 28px | Identical |

Structure-only checks such as grid layout and overflow are not visual parity evidence.

A statement saying "matches the concept" without measurements is unacceptable.

## 3.2 Browser evidence

For interactive components, report:

- What was clicked.
- What appeared.
- What changed.
- Whether the action triggered a request.
- Differences found.
- Corrections made.

If testing an interaction that must not call the server, record:

`Network request count before interaction: N`

`Network request count after interaction: N`

Use actual browser network evidence.

If the browser tool is unavailable, stop the current part.

Do not push without visual verification.

---

# PART 16 — SOURCED RECENT NEWS FEED

## Goal

Implement the original sourced recent news experience.

Display a maximum of six articles, in chronological order, with duplicate removal and safe external links.

Missing news must never break the company workspace.

## 16.1 Original source paths

VERIFIED against AUDIT.md:

1. `E:\Quant-AI\client\src\pages\Home.tsx`
2. `E:\Quant-AI\client\src\lib\market.ts`
3. `E:\Quant-AI\client\src\lib\research.ts`
4. `E:\Quant-AI\tests\test_news_context_mapping.ts`

Also inspect the original Python backend:

- `E:\Quant-AI\api\market_intelligence_services.py`
- `E:\Quant-AI\api\research_schemas.py`
- `E:\Quant-AI\api\research_orchestrator.py`

These backend paths are verified in AUDIT.md.

Read the relevant news extraction and mapping code completely.

## 16.2 Existing Python implementation

Inspect before changing:

- api/web/presenters.py
- api/web/routes.py
- api/web/contracts.py
- templates/pages/home.html
- Existing news partials.
- Existing research response mapping.

## 16.3 Target files

The exact Part 16 target files must be reconciled against MIGRATION_PLAN.md.

Proposed targets:

ASSUMPTION — verify exact plan mapping:

- `api/web/news.py`
- `templates/partials/news_feed.html`
- `tests/test_news_feed.py`
- `tests/test_news_context_mapping.py`

Reuse existing files where they already provide the functionality.

Do not create a duplicate news component.

## 16.4 Required functionality

### Article limit

Maximum six articles.

Never render more than six.

### Chronological order

Sort articles chronologically according to the original behavior.

Verify whether the original uses ascending or descending publication order.

Do not guess.

### Deduplication

Remove duplicate articles.

Inspect the original TypeScript deduplication logic.

Preserve its identity matching behavior.

Where appropriate, use normalized canonical URL and existing stable article identifiers.

Do not merge two distinct articles simply because their headlines are similar.

### Required article fields

Every article must support:

1. Headline.
2. Publisher.
3. Formatted publication date.
4. Provider-supplied summary context.
5. External source URL.

Preserve optional fields only where supported by the actual response contract.

Never generate a missing summary.

### Safe links

Allow only:

- http
- https

Reject:
- javascript:
- data:
- file:
- vbscript:
- protocol-relative URLs without validated scheme.

External links must use:

`target="_blank" rel="noopener noreferrer"`

Unsafe or missing links must not become clickable.

### Missing news behavior

Implement distinct states:

- Loading.
- Success.
- Empty.
- Unavailable/error.

Missing news must not:
- Crash the workspace.
- Hide market data.
- Hide fundamentals.
- Hide deterministic signals.
- Break the AI analysis panel.
- Break the chat drawer.

## 16.5 TypeScript regression migration

Port:

`tests/test_news_context_mapping.ts`

to:

`tests/test_news_context_mapping.py`

Preserve every original assertion.

Verify:
- Headline extraction.
- URL preservation.
- Publisher attribution.
- Summary extraction.
- Missing values.
- Optional values.
- Mapping behavior.
- Original edge cases.

Do not weaken assertions.

## 16.6 Tests to write first

Create:

- tests/test_news_feed.py
- tests/test_news_context_mapping.py

Cover:

1. Six-article maximum.
2. Seven or more input articles result in six output articles.
3. Chronological ordering.
4. Duplicate URL removal.
5. Duplicate article identifier removal.
6. Distinct headlines are retained.
7. Headline preservation.
8. Publisher preservation.
9. Publication date formatting.
10. Provider summary preservation.
11. Missing summary.
12. Missing publisher.
13. Missing publication date.
14. Missing source URL.
15. HTTP link accepted.
16. HTTPS link accepted.
17. JavaScript URL rejected.
18. Data URL rejected.
19. File URL rejected.
20. Unsafe URL never rendered as clickable.
21. External links include `noopener noreferrer`.
22. Empty news state.
23. Unavailable news state.
24. Workspace remains operational when news is missing.
25. All original TypeScript news-context assertions.

Use fake Testco fixtures only.

Do not create production routes solely for tests.

## 16.7 Browser verification

At all four required visual configurations:

- Search a real company.
- Inspect the Recent News section.
- Inspect article ordering.
- Open a source link.
- Inspect publisher and publication date.
- Inspect summary text.
- Test the empty state with a controlled test fixture.
- Verify the workspace remains visible when news is unavailable.

Record at least two measured visual differences.

## 16.8 Acceptance criteria

All following criteria are mandatory:

- Maximum six articles.
- Articles are chronologically ordered.
- Duplicate articles are removed.
- Headlines are displayed.
- Publisher names are displayed.
- Publication dates are formatted.
- Provider-supplied summary context is displayed.
- Source URLs are preserved.
- Only HTTP/HTTPS external links are allowed.
- External links use `rel="noopener noreferrer"`.
- Unsafe URLs are not clickable.
- Empty news state works.
- Unavailable news state works.
- Missing news does not break the workspace.
- Missing news does not remove deterministic market information.
- The original TypeScript news-context mapping test is ported.
- All original assertions are preserved.
- No design sample data is introduced.
- Full pytest passes.
- Four browser visual checks pass.
- At least two measured visual comparisons are reported.

## Commit

`part 16: implement sourced recent news feed`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 16 "part 16: implement sourced recent news feed"`

---

# PART 17 — CORPORATE EVENTS CALENDAR RADAR

## Goal

Implement the original corporate events calendar.

Display real upcoming and historical earnings dates and corporate events.

## 17.1 Original source paths

VERIFIED against AUDIT.md:

1. `E:\Quant-AI\client\src\pages\Home.tsx`
2. `E:\Quant-AI\client\src\lib\market.ts`
3. `E:\Quant-AI\client\src\lib\research.ts`

Backend sources:

4. `E:\Quant-AI\api\market_intelligence_services.py`
5. `E:\Quant-AI\api\research_schemas.py`
6. `E:\Quant-AI\api\research_orchestrator.py`

Inspect the actual event response structure.

## 17.2 Existing Python files to inspect

- api/web/presenters.py
- api/web/routes.py
- api/web/contracts.py
- Existing market event service functions.
- Existing market event templates.

## 17.3 Target files

ASSUMPTION — reconcile with MIGRATION_PLAN.md:

- `api/web/events.py`
- `templates/partials/events_radar.html`
- `tests/test_events_radar.py`

Do not duplicate existing event implementations.

## 17.4 Required functionality

Preserve the actual original event categories and response mapping.

The radar must support the original event information:

1. Earnings dates.
2. Other supported corporate events.
3. Event date.
4. Event title.
5. Event type.
6. Importance badge.
7. Source attribution.

Use the original response's supported fields.

Do not fabricate event importance or event classifications.

### Ordering

Display events chronologically.

Preserve the correct relationship between past and upcoming events.

Do not discard historical events if the original response includes them.

### Event states

Support:

- Loading.
- Success.
- Empty.
- Unavailable/error.

A missing event record must not appear as an application crash.

### Data integrity

Do not:
- Generate earnings dates.
- Invent dividends.
- Invent stock splits.
- Infer unreported corporate actions.
- Invent event importance.
- Generate source attribution.

## 17.5 Tests to write first

Create:

`tests/test_events_radar.py`

Test:

1. Earnings event mapping.
2. Corporate event mapping.
3. Date formatting.
4. Chronological ordering.
5. Past events.
6. Upcoming events.
7. Event title.
8. Event type.
9. Importance badge.
10. Source attribution.
11. Missing event date.
12. Missing title.
13. Missing event type.
14. Missing source.
15. Empty event state.
16. Unavailable event state.
17. Invalid event data.
18. No fabricated events.
19. Workspace remains operational when events are unavailable.

Use fake Testco fixtures.

Do not add production endpoints solely to support test fixtures.

## 17.6 Browser verification

At all four required configurations:

- Search a company.
- Inspect event radar.
- Inspect event dates.
- Inspect importance badges.
- Inspect source attribution.
- Expand/collapse relevant sections.
- Verify empty and unavailable states using controlled fixtures.

Report at least two measured visual differences.

## 17.7 Acceptance criteria

- Earnings events are displayed when returned.
- Supported corporate events are displayed.
- Event dates are formatted.
- Event titles are displayed.
- Event types are displayed.
- Importance badges are displayed.
- Source attribution is displayed.
- Events are chronologically ordered.
- Past and upcoming events are handled correctly.
- Missing event fields are handled safely.
- Empty state works.
- Unavailable state works.
- No fabricated event information exists.
- No design sample data is used.
- Existing market workspace remains functional.
- All tests pass.
- Four browser visual checks pass.
- At least two measured visual comparisons are reported.

## Commit

`part 17: implement corporate events radar`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 17 "part 17: implement corporate events radar"`

---

# PART 18 — EVIDENCE APPENDIX AND PROVENANCE LEDGER

## Goal

Implement the expandable evidence appendix showing the provenance and freshness of research data.

Evidence must remain clearly separate from AI interpretation.

The user must be able to understand where a fact came from and how fresh it is.

## 18.1 Original source paths

VERIFIED against AUDIT.md:

1. `E:\Quant-AI\client\src\pages\Home.tsx`
2. `E:\Quant-AI\client\src\lib\market.ts`
3. `E:\Quant-AI\client\src\lib\research.ts`
4. `E:\Quant-AI\client\components\AnalysisPanel.tsx`

IMPORTANT:

The fourth path above is not confirmed.

Correct verified location from the audit:

`E:\Quant-AI\client\src\components\AnalysisPanel.tsx`

Use that path.

Also inspect:

- `E:\Quant-AI\api\research_schemas.py`
- `E:\Quant-AI\api\research_orchestrator.py`
- `E:\Quant-AI\api\research_services.py`

## 18.2 Existing Python files to inspect

- api/web/contracts.py
- api/web/presenters.py
- api/web/routes.py
- api/research_schemas.py
- templates/pages/home.html
- Existing freshness/provenance presentation.

## 18.3 Target files

ASSUMPTION — verify against MIGRATION_PLAN.md:

- `api/web/evidence.py`
- `templates/partials/evidence_appendix.html`
- `tests/test_evidence_appendix.py`

Reuse existing files if equivalent functionality exists.

## 18.4 Required freshness states

Implement exactly these statuses:

- LIVE
- CACHED
- RECENT
- UNAVAILABLE

Preserve existing status values and mapping.

Do not invent alternative values.

Do not change the original backend enum without a documented necessity.

## 18.5 Evidence fields

The appendix must expose every supported original evidence field:

1. Section/source category.
2. Freshness state.
3. Source URL.
4. Retrieval timestamp.
5. Research warning notices.

Preserve optional metadata from the original response.

Do not invent source URLs or timestamps.

### Evidence separation

Evidence and AI interpretation must remain separate.

The appendix represents factual provenance.

The AI brief represents generated interpretation.

Never:
- Treat an AI statement as a verified data source.
- Present an AI-generated summary as a provider source.
- Assign LIVE status to AI interpretation.
- Invent a source to support a narrative.
- Combine evidence and opinion without clear distinction.

## 18.6 Expandable behavior

Use native:

`<details>` and `<summary>`.

Opening or closing the appendix must not require a server request.

Preserve keyboard accessibility.

Use the design concept's card, disclosure and spacing language.

## 18.7 Tests to write first

Create:

`tests/test_evidence_appendix.py`

Test:

1. LIVE state.
2. CACHED state.
3. RECENT state.
4. UNAVAILABLE state.
5. Correct state mapping.
6. Source URL preservation.
7. Retrieval timestamp preservation.
8. Warning notice preservation.
9. Missing source URL.
10. Missing timestamp.
11. Multiple evidence sections.
12. Evidence/AI interpretation separation.
13. AI narrative is not marked as provider evidence.
14. No invented provenance.
15. Native details/summary rendering.
16. No server request requirement for disclosure.
17. Responsive rendering.

Use fake Testco fixtures.

Do not create production routes for controlled fixtures.

## 18.8 Browser verification

At all four required configurations:

- Search a company.
- Open the evidence appendix.
- Inspect LIVE records.
- Inspect CACHED records.
- Inspect RECENT records.
- Inspect UNAVAILABLE records.
- Inspect source links.
- Inspect retrieval timestamps.
- Inspect warnings.
- Collapse the appendix.
- Verify the AI interpretation is visually separate.

Report at least two measured visual differences.

For expand/collapse behavior, report actual network request counts before and after.

## 18.9 Acceptance criteria

- Evidence appendix exists.
- Appendix is expandable.
- LIVE state is supported.
- CACHED state is supported.
- RECENT state is supported.
- UNAVAILABLE state is supported.
- Source URLs are preserved.
- Retrieval timestamps are preserved.
- Research warnings are displayed.
- Evidence remains separate from AI interpretation.
- AI interpretation is never misrepresented as verified evidence.
- Missing metadata is handled safely.
- Disclosure uses native details/summary.
- Expand/collapse does not call the server.
- No fabricated sources or timestamps.
- No design sample data.
- Existing research behavior is preserved.
- All tests pass.
- Four browser visual checks pass.
- At least two measured visual comparisons are reported.

## Commit

`part 18: implement evidence appendix and provenance ledger`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 18 "part 18: implement evidence appendix and provenance ledger"`

---

# PART 19 — MARKDOWN, AI RESEARCH BRIEF AND MATH RENDERING

## Goal

Port the original AnalysisPanel and structured AI research brief.

The brief must render server-side using Python.

Preserve the distinction between deterministic market evidence and optional AI interpretation.

AI provider failure must never make deterministic research disappear.

## 19.1 Original source paths

VERIFIED against AUDIT.md:

1. `E:\Quant-AI\client\src\components\AnalysisPanel.tsx`
2. `E:\Quant-AI\client\src\lib\market.ts`
3. `E:\Quant-AI\client\src\lib\research.ts`
4. `E:\Quant-AI\client\src\pages\Home.tsx`

Backend sources:

5. `E:\Quant-AI\api\ai_providers.py`
6. `E:\Quant-AI\api\research_orchestrator.py`
7. `E:\Quant-AI\api\research_schemas.py`

Read the original brief structure and markdown extraction logic.

## 19.2 Target files

ASSUMPTION — verify exact plan mapping:

- `api/web/markdown.py`
- `api/web/analysis.py`
- `templates/partials/analysis_brief.html`
- `templates/partials/analysis_skeleton.html`
- `templates/partials/ai_unavailable.html`
- `tests/test_markdown_rendering.py`
- `tests/test_analysis_brief.py`

Do not create duplicate providers or a second research orchestrator.

## 19.3 Mandatory Python libraries

Use ONLY the approved stack for markdown and math:

- markdown-it-py
- mdit-py-plugins
- latex2mathml
- Pygments

Do not use KaTeX.

Do not vendor KaTeX.

Do not use MathJax.

Do not introduce a client-side math renderer.

### Math rendering

Use:
- markdown-it-py for Markdown.
- mdit-py-plugins dollarmath for dollar-delimited math.
- latex2mathml for server-side MathML conversion.
- Pygments for syntax-highlighted code blocks.

Render:
- Inline mathematics.
- Block mathematics.
- Code fences.
- Headings.
- Lists.
- Tables.
- Links.
- Emphasis.
- Blockquotes.

Preserve the original markdown content and formatting behavior.

Math output must be MathML generated server-side.

Do not emit unprocessed LaTeX as though it were rendered mathematics.

If invalid mathematical input is returned, handle it safely without crashing the entire research brief.

## 19.4 HTML sanitization

AI output is untrusted.

Sanitize generated HTML before inserting it into Jinja2 templates.

Prevent:
- Script injection.
- Event-handler attributes.
- JavaScript URLs.
- Unsafe HTML elements.
- Unsafe embedded resources.
- Attribute-based HTML injection.

Use an established HTML sanitizer.

Preserve safe:
- Headings.
- Paragraphs.
- Lists.
- Tables.
- Code blocks.
- Links.
- MathML elements required by the approved rendering strategy.

Do not bypass sanitization for mathematical content.

Verify the sanitizer permits only the minimum MathML and HTML elements required.

## 19.5 Structured AI brief sections

The original audit lists the following sections:

1. Executive Assessment.
2. Business Model.
3. Financial Health.
4. Growth Drivers.
5. Competitive Position.
6. Key Risks.
7. Catalysts.
8. Valuation View.
9. What to Watch.

Preserve the original section extraction and ordering.

Do not invent missing sections.

Preserve the prominent editorial lead quote extracted from the original analysis narrative where supported.

## 19.6 Loading and unavailable states

Implement the original shimmer loading skeleton.

Respect:

`prefers-reduced-motion`

When AI is unavailable:

- Display a clear non-blocking banner.
- Preserve market snapshot.
- Preserve historical price chart.
- Preserve deterministic signal.
- Preserve fundamentals.
- Preserve company profile.
- Preserve news.
- Preserve events.
- Preserve evidence appendix.

AI failure must not replace the complete workspace with a fatal error.

The banner must clearly indicate that AI interpretation is unavailable while deterministic information remains available.

## 19.7 Provider mocking

All provider-related tests must use mocks.

Never:
- Make paid provider calls during tests.
- Print provider credentials.
- Log environment variable values.
- Include secrets in assertion output.
- Expose raw provider exceptions in HTML.

Use mock responses and monkeypatching.

Use a controlled fake Testco research brief.

## 19.8 Tests to write first

Create:

- tests/test_markdown_rendering.py
- tests/test_analysis_brief.py

Cover:

### Markdown

1. Heading rendering.
2. Paragraph rendering.
3. Bold and italic.
4. Lists.
5. Tables.
6. Links.
7. Blockquotes.
8. Code fences.
9. Pygments highlighting.
10. Inline mathematics.
11. Block mathematics.
12. Valid MathML output.
13. Invalid LaTeX handling.
14. Markdown escaping.
15. Unsafe HTML sanitization.
16. Script injection prevention.
17. Event-handler attribute prevention.
18. JavaScript URL prevention.
19. Unsafe embedded resource prevention.

### Analysis

20. Executive Assessment.
21. Business Model.
22. Financial Health.
23. Growth Drivers.
24. Competitive Position.
25. Key Risks.
26. Catalysts.
27. Valuation View.
28. What to Watch.
29. Lead quote extraction.
30. Missing sections.
31. AI success.
32. AI unavailable.
33. Non-blocking unavailable banner.
34. Deterministic data preservation.
35. Loading skeleton.
36. Reduced-motion behavior.
37. Provider exception sanitization.
38. No API key leakage.

Tests must not require new production routes or unrelated files.

## 19.9 Browser verification

At all four required configurations:

- Search fake Testco through a controlled test harness where appropriate.
- Inspect the brief.
- Inspect section order.
- Inspect headings.
- Inspect inline math.
- Inspect block math.
- Inspect code highlighting.
- Inspect links.
- Inspect the AI unavailable banner using mocked provider failure.
- Verify deterministic information remains visible.
- Inspect mobile readability.

Do not use concept sample data.

Report at least two measured visual differences.

## 19.10 Acceptance criteria

- Original AnalysisPanel behavior preserved.
- Server-side Markdown rendering implemented.
- markdown-it-py used.
- mdit-py-plugins dollarmath used.
- latex2mathml used.
- MathML generated server-side.
- No KaTeX.
- No MathJax.
- Pygments code highlighting works.
- Inline math works.
- Block math works.
- Invalid LaTeX handled safely.
- Unsafe HTML sanitized.
- Script injection prevented.
- Event-handler injection prevented.
- Unsafe URL handling implemented.
- All nine original brief sections supported.
- Lead quote extraction preserved.
- Missing sections handled correctly.
- Loading skeleton implemented.
- Reduced-motion respected.
- AI-unavailable banner is non-blocking.
- Deterministic market data remains visible during AI failure.
- Providers mocked in tests.
- No API keys printed or exposed.
- No design sample data used.
- All tests pass.
- Four browser visual checks pass.
- At least two measured visual comparisons are reported.

## Commit

`part 19: implement markdown research brief and math rendering`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 19 "part 19: implement markdown research brief and math rendering"`

---

# PART 20 — AGENTOS CHAT CLIENT AND ERROR NORMALIZATION

## Goal

Port the original conversational AgentOS client and error normalization.

Implement the research chat drawer with session continuity.

The existing Python AgentOS backend must remain the source of truth.

Do not create a duplicate agent.

## 20.1 Original source paths

VERIFIED against AUDIT.md:

1. `E:\Quant-AI\client\src\components\ChatPanel.tsx`
2. `E:\Quant-AI\client\src\lib\agentos.ts`
3. `E:\Quant-AI\client\src\lib\research.ts`
4. `E:\Quant-AI\client\src\pages\Home.tsx`
5. `E:\Quant-AI\tests\test_agentos_client_errors.ts`

Backend sources:

6. `E:\Quant-AI\api\agents.py`
7. `E:\Quant-AI\api\index.py`
8. `E:\Quant-AI\api\agents\groq-finance-agent\runs.py`
9. `E:\Quant-AI\api\groq_finance_agent.py`

All paths above are present in the original audit inventory.

Inspect actual request/response behavior before implementation.

## 20.2 Target files

ASSUMPTION — verify exact plan mapping:

- `api/web/chat.py`
- `static/js/chat.js`
- `templates/partials/chat_drawer.html`
- `templates/partials/chat_messages.html`
- `tests/test_agentos_chat.py`
- `tests/test_agentos_client_errors.py`

Reuse existing chat modules if they already exist.

Do not create a duplicate backend agent.

## 20.3 Chat drawer

Implement the original secondary research desk.

It must include:

- Drawer open/close.
- Message stream.
- User messages.
- Agent messages.
- Input field.
- Send action.
- Loading/working state.
- Error state.
- Markdown formatting.
- User and agent avatars where originally supported.

Use the approved design tokens.

The drawer must work responsively.

Do not let the drawer obscure the main research workspace unnecessarily.

## 20.4 Quick prompt pills

Preserve the exact original quick prompts:

1. Pressure-test the thesis.
2. Trace the source lane.
3. Separate evidence from interpretation.

Each pill must submit its corresponding prompt.

Do not invent new prompt semantics.

## 20.5 Session continuity

Preserve backend:

`session_id`

Requirements:

- Use the original session semantics.
- Preserve the session across consecutive messages.
- Associate responses with the correct session.
- Handle missing session IDs according to the original client behavior.
- Do not invent a new persistence backend.
- Do not introduce a database.

## 20.6 Turn counter

Implement the original real-time turn counter.

Use actual message/turn state.

Do not invent turn counts.

## 20.7 Error normalization

Port the original AgentOS error normalization behavior.

Preserve the mapping of HTTP status and provider error information to user-friendly messages.

Inspect the original test for exact cases.

At minimum, verify:
- HTTP 401.
- HTTP 429.
- HTTP 500.
- Provider unavailable.
- Network failure.
- Invalid response.
- Unknown error.

Use the original messages and mapping rules rather than inventing new wording.

Do not expose raw stack traces or credentials.

## 20.8 TypeScript regression migration

Port:

`tests/test_agentos_client_errors.ts`

to:

`tests/test_agentos_client_errors.py`

Preserve every original assertion.

Do not weaken or omit cases.

## 20.9 Security and request handling

Respect the established security architecture.

- Do not expose provider credentials.
- Do not print API keys.
- Do not accept arbitrary server-side backend URLs.
- Do not introduce self-HTTP calls.
- Use the existing in-process backend/orchestrator.
- Preserve request size and rate-limit protections.
- Sanitize error responses.

The browser-side custom AgentOS endpoint setting must remain consistent with the established architecture from Part 22's SSRF rule.

Do not create a second server-side URL-fetching mechanism.

## 20.10 Tests to write first

Create:

- tests/test_agentos_chat.py
- tests/test_agentos_client_errors.py

Cover:

1. Drawer rendering.
2. Drawer open/close.
3. Message input.
4. Message submission.
5. User message rendering.
6. Agent message rendering.
7. Markdown response rendering.
8. Loading state.
9. Error state.
10. Session ID preservation.
11. Session continuity across consecutive turns.
12. Missing session ID.
13. Turn counter.
14. Pressure-test quick prompt.
15. Trace-source quick prompt.
16. Separate-evidence quick prompt.
17. HTTP 401 mapping.
18. HTTP 429 mapping.
19. HTTP 500 mapping.
20. Provider error mapping.
21. Network error mapping.
22. Invalid response handling.
23. Unknown error fallback.
24. No API key exposure.
25. No raw stack traces.
26. No self-HTTP backend calls.
27. No arbitrary server-side URL fetching.
28. Existing chat backend compatibility.

Mock the agent.

Do not call real AI providers.

Use fake Testco conversation fixtures.

Do not add test-only production endpoints.

## 20.11 Browser verification

At all four required configurations:

- Open the research chat drawer.
- Close the drawer.
- Submit a user message using a mocked/test-safe agent.
- Inspect user message.
- Inspect agent response.
- Inspect loading indicator.
- Inspect markdown formatting.
- Send a second message.
- Verify the same session ID is retained.
- Verify turn counter updates.
- Click all three quick prompts.
- Inspect error state using a mocked failure.
- Verify responsive drawer behavior.

Record at least two measured visual differences.

Report actual interactions and observed results.

## 20.12 Acceptance criteria

- AgentOS chat drawer implemented.
- Drawer opens.
- Drawer closes.
- User messages display.
- Agent messages display.
- Message input works.
- Send action works.
- Loading state works.
- Error state works.
- Markdown rendering works.
- User/agent avatars preserved where supported.
- Session continuity uses backend `session_id`.
- Missing session IDs handled correctly.
- Turn counter uses real conversation state.
- Pressure-test the thesis prompt works.
- Trace the source lane prompt works.
- Separate evidence from interpretation prompt works.
- HTTP 401 normalization preserved.
- HTTP 429 normalization preserved.
- HTTP 500 normalization preserved.
- Provider error normalization preserved.
- Network failure normalization preserved.
- Invalid response handling works.
- Unknown error fallback works.
- Original TypeScript AgentOS client-error test is ported.
- All original assertions preserved.
- No API keys exposed.
- No raw stack traces exposed.
- No arbitrary server-side URL fetching.
- No self-HTTP backend calls.
- Existing AgentOS backend is reused.
- No design sample data used.
- All tests pass.
- Four browser visual checks pass.
- At least two measured visual comparisons are reported.

## Commit

`part 20: implement AgentOS chat client and error mapping`

Push:

`.\.venv\Scripts\python.exe migration\push_part.py 20 "part 20: implement AgentOS chat client and error mapping"`

---

# 4. AUTOMATED TEST POLICY

For each part:

1. Tests first.
2. Focused tests.
3. Full pytest.
4. Code review.
5. Browser verification.
6. Progress update.
7. Push.

Full suite:

`.\.venv\Scripts\python.exe -m pytest -q`

## Important: interaction tests beyond source-text checks

For chart-related or interactive behavior, a text-only assertion is insufficient.

At least one additional automated test must verify the actual server-rendered contract or data payload.

Examples:

- News JSON/presenter structure.
- Event payload structure.
- Evidence data attributes.
- Sanitized server-rendered Markdown.
- MathML output.
- Chat form attributes.
- Session ID propagation.

Node.js is prohibited, so do not install a JavaScript test runner.

Use Python pytest to validate server-rendered HTML, JSON structures, response contracts and data attributes.

Browser verification is still required for actual client-side behavior.

Do not claim a JavaScript interaction passed merely because its source contains the expected string.

---

# 5. VISUAL EVIDENCE REPORT FORMAT

For every part, provide:

### Visual comparison

| Property | Design concept | Application | Action |
|---|---|---|---|
| Font size | Measured value | Measured value | Fixed/Identical |
| Card padding | Measured value | Measured value | Fixed/Identical |

Use actual measured values.

### Browser interaction evidence

| Interaction | Action | Actual observation |
|---|---|---|
| Example | Clicked article link | Opened verified HTTPS source |
| Example | Opened disclosure | Appendix expanded |
| Example | Sent message | Agent response rendered |

### Network evidence

Where an interaction must be client-side:

| Measurement | Count |
|---|---:|
| Requests before interaction | Actual count |
| Requests after interaction | Actual count |
| Additional requests | Difference |

Never invent network counts.

---

# 6. COMMIT AND PUSH RULES

Exactly one commit per part.

Only use:

PART 16:

`.\.venv\Scripts\python.exe migration\push_part.py 16 "part 16: implement sourced recent news feed"`

PART 17:

`.\.venv\Scripts\python.exe migration\push_part.py 17 "part 17: implement corporate events radar"`

PART 18:

`.\.venv\Scripts\python.exe migration\push_part.py 18 "part 18: implement evidence appendix and provenance ledger"`

PART 19:

`.\.venv\Scripts\python.exe migration\push_part.py 19 "part 19: implement markdown research brief and math rendering"`

PART 20:

`.\.venv\Scripts\python.exe migration\push_part.py 20 "part 20: implement AgentOS chat client and error mapping"`

Never use direct git commit or git push.

Never use git add -A.

Do not amend, squash or merge commits.

Update PROGRESS.md before the push.

A part is complete only after its push succeeds.

---

# 7. STOP CONDITIONS

Stop immediately if:

1. Full pytest fails after three fix attempts.
2. A critical original behavior is unclear.
3. A source file is missing.
4. A required acceptance criterion cannot be implemented safely.
5. A backend contract conflict is found.
6. A secret is exposed or detected.
7. HTML sanitization is insufficient.
8. An unsafe URL can reach a clickable link.
9. The design reference is unavailable.
10. Browser verification cannot be performed.
11. Required visual measurements cannot be obtained.
12. Git configuration is invalid.
13. A previous part is incomplete.
14. push_part.py fails.
15. A required library is unavailable.

Do not skip the part.

Do not continue after a critical blocker.

---

# 8. FINAL BATCH REPORT

After Part 20 has successfully pushed, stop.

Report the following.

## A. Part-by-part results

For Parts 16–20:

- Part number.
- Implementation summary.
- Exact files created.
- Exact files modified.
- Focused tests.
- Full pytest count.
- Commit SHA.
- Push confirmation.

## B. Feature verification

### News

Report:
- Maximum article count.
- Sorting direction.
- Deduplication rule.
- Headline.
- Publisher.
- Date.
- Summary.
- HTTP/HTTPS validation.
- External link security.
- Missing-news behavior.
- Original TypeScript regression test.

### Events

Report:
- Event types.
- Date formatting.
- Importance.
- Source attribution.
- Past/upcoming handling.
- Empty/unavailable behavior.

### Evidence

Report:
- LIVE.
- CACHED.
- RECENT.
- UNAVAILABLE.
- Source URLs.
- Retrieval timestamps.
- Warning notices.
- Separation from AI interpretation.

### AI brief

Report:
- Markdown features.
- All nine brief sections.
- Inline MathML.
- Block MathML.
- Pygments.
- HTML sanitization.
- Mocked provider tests.
- Non-blocking AI unavailable state.
- Deterministic data preservation.

### AgentOS

Report:
- Drawer behavior.
- Message behavior.
- Quick prompts.
- Session ID continuity.
- Turn counter.
- Error mapping.
- Original TypeScript regression test.
- No secrets or self-HTTP calls.

## C. Visual evidence

For every part, report:

- 1440px Light.
- 1440px Dark.
- 390px Light.
- 390px Dark.
- At least two measured visual comparisons.
- Differences discovered.
- Fixes made.
- Remaining differences.

## D. Regression integrity

Baseline entering batch:

142 passing tests.

Report:

- Total collected tests.
- Total passing.
- Total failing.
- Original seven Python suites.
- News context mapping regression.
- AgentOS client error regression.
- Any original test modifications.
- Exact reasons for every modification.

## E. Contract changes

List every modified original backend file.

If none:

State explicitly that no original backend contracts were modified.

If modified:

Explain why, and why extending api/web/contracts.py was insufficient.

## F. Git status

Verify:

- Branch main.
- Correct origin.
- 20 migration commits.
- Five new pushes.
- Clean working tree.
- Parts 01–20 checked.
- BATCH_04 complete.

## G. Stop

Print:

`BATCH COMPLETE, STOP`

Then wait for the user's next instruction.

Do not begin Part 21.

Do not begin BATCH_05.

---

# FINAL NON-NEGOTIABLE RULE

The original application determines functionality.

The approved HTML determines visual design.

The backend determines factual data.

AI interpretation must never masquerade as evidence.

Never invent a news article, event, source, metric or financial conclusion.

Never expose provider secrets.

Never weaken original tests.

Never change original backend contracts casually.

Every part must be tested, visually inspected, measured, reviewed, committed individually and pushed successfully.

Complete exactly Parts 16–20 and stop.
