
# BATCH_02.md — QuantAI Python Migration

**Batch:** BATCH_02  
**Day:** 1  
**Parts:** 06–10  
**Repository:** https://github.com/SamSurve/QuantAI.git  
**Branch:** main  
**Project:** E:\QuantAI-Python  
**Original source:** E:\Quant-AI (READ-ONLY)  
**Design reference:** E:\QuantAI-design\Main.dc.html  
**Python:** 3.12.7  
**Environment:** .venv  
**Terminal:** Windows PowerShell

---

# 1. READ FIRST

Read these documents completely:

1. migration/MIGRATION_PLAN.md
2. migration/PROGRESS.md
3. migration/MASTER_PROMPT.md
4. migration/BATCH_02.md

MASTER_PROMPT.md and MIGRATION_PLAN.md are authoritative.

Do not restructure the 30-part migration.

Do not modify E:\Quant-AI.

Do not start BATCH_03.

Complete Parts 06, 07, 08, 09 and 10 sequentially.

Stop immediately on a critical blocker or after three unsuccessful fix attempts.

Do not ask the user for permission between parts.

---

# 2. BATCH_01 COMPLETION VERIFICATION

Before beginning Part 06, verify:

Repository root:
E:\QuantAI-Python

Branch:
main

Remote:
https://github.com/SamSurve/QuantAI.git

Verify:

- Parts 01–05 are checked in migration/PROGRESS.md.
- Exactly five prior migration part commits exist.
- All five commits are on main.
- Their pushes have been completed.
- The latest commit is Part 05.
- Full pytest is passing.
- The original seven Python regression suites are retained.

The expected five previous commits are:

1. f3d55702490d29457d92c0397de93dc88a177140
2. dd116222b21a42a4b6e62550693370639260c819
3. 4b5fe9340ef3e84a7a512e64471128da58ed6e70
4. 2c46c414b1870aa2565bdb6408fca6d124e7ee28
5. 9b9dd621b422a75d423936c3bc84d3e3f9a71a91

Inspect actual Git history rather than trusting this list alone.

Inspect git status before beginning.

If an unexpected untracked file remains from BATCH_01, inspect it and determine whether it was intended to be committed previously.

Do not blindly include unrelated leftover files in Part 06.

If the repository is not in a safe sequential state, stop and report the blocker.

---

# 3. SKILLS

## Mandatory for EVERY part

- test-driven-development
- source-driven-development
- code-review-and-quality

## Required additional skill

| Part | Additional skill |
|---|---|
| 06 | frontend-ui-engineering |
| 07 | frontend-ui-engineering |
| 08 | frontend-ui-engineering |
| 09 | None |
| 10 | frontend-ui-engineering |

## Reference only

- git-workflow-and-versioning

Do not let git-workflow-and-versioning change the approved Git workflow.

The exact security skill name is not required for this batch.

At the start of each part, print one line.

For Part 06:

Skills used: test-driven-development, source-driven-development, frontend-ui-engineering, code-review-and-quality

For Part 07:

Skills used: test-driven-development, source-driven-development, frontend-ui-engineering, code-review-and-quality

For Part 08:

Skills used: test-driven-development, source-driven-development, frontend-ui-engineering, code-review-and-quality

For Part 09:

Skills used: test-driven-development, source-driven-development, code-review-and-quality

For Part 10:

Skills used: test-driven-development, source-driven-development, frontend-ui-engineering, code-review-and-quality

Follow skill instructions only when they do not conflict with the migration plan or master prompt.

Skills must not create extra files.

Do not run /spec, /plan, /build or /build auto.

Never install Node.js, npm, npx or pnpm.

---

# 4. NEW APPROVED DESIGN REFERENCE

## 4.1 Exact design file

The approved HTML design reference is:

E:\QuantAI-design\Main.dc.html

The uploaded archive contains:

- Main.dc.html
- support.js
- vendor/react.js
- vendor/react-dom.js
- README.md

The main HTML document is the visual reference.

The archive README identifies it as a design mockup, not production code.

Verify the exact file exists before starting Part 06.

If the expected file is unavailable, stop and report the missing reference.

Do not substitute an imagined design.

## 4.2 Open the concept in the browser

Antigravity must open:

E:\QuantAI-design\Main.dc.html

in its browser.

The reference may need its external local support files to render.

If opening with file:// fails, serve the external reference folder temporarily using Python's built-in HTTP server.

Example PowerShell workflow:

Terminal A:

```powershell
cd E:\QuantAI-design
python -m http.server 8765 --bind 127.0.0.1
```

Open:

http://127.0.0.1:8765/Main.dc.html

Run the temporary server outside E:\QuantAI-Python.

Do not add the reference folder to the project.

Do not change the original reference files.

Keep the concept and the running QuantAI application separate.

## 4.3 Extract design tokens from the actual HTML

Do not rely only on the written design-token summary from previous instructions.

Inspect Main.dc.html directly.

Extract and document in the implementation:

- Light theme colors.
- Dark theme colors.
- Backgrounds.
- Cards.
- Secondary fills.
- Text.
- Muted text.
- Links.
- Positive status.
- Warning status.
- Information status.
- Borders and hairlines.
- Shadows.
- Glass effect.
- Tooltip colors.
- Segmented control colors.
- Chart grid colors.
- Typography.
- Font weights.
- Letter spacing.
- Font sizes.
- Spacing.
- Border radii.
- Card padding.
- Grid structure.
- Responsive breakpoints.
- Header geometry.
- Button dimensions.
- Chart tooltip dimensions.

Use the extracted tokens as the authoritative styling reference.

Implement them through:

- static/css/input.css
- static/css/app.css
- Tailwind utility classes
- Jinja2 macros
- Reusable template classes

Avoid duplicating the same token values throughout unrelated templates.

Create reusable CSS variables.

Use the original index.css only for visual properties not defined by the approved HTML concept.

Do not replace the concept's defined styling with the old React styling.

## 4.4 Important: prohibited concept content

The design file is a READ-ONLY visual and interaction reference.

Never copy the concept HTML into the new repository.

Never copy its runtime into the new repository.

Specifically, DO NOT copy:

- Main.dc.html
- support.js
- vendor/react.js
- vendor/react-dom.js
- Any generated runtime code
- Any React runtime
- Any generated sample dataset
- Any sample chart data
- Any embedded sample market metrics

Never implement these custom elements:

- x-dc
- sc-for
- sc-if
- helmet

Never import, execute or depend on these custom elements in the production application.

Do not copy the concept's DCLogic JavaScript class.

Do not copy its generated sample financial data.

Do not copy its embedded sample price arrays or random chart generator.

Do not reproduce its sample Apple market figures.

The reference is for the design and interaction patterns only.

All actual values must originate from the existing QuantAI backend and original research contracts.

Never display the concept's illustrative prices, metrics, chart points, dates, earnings events or placeholder headlines as real application data.

Use Jinja2, HTMX, vanilla JavaScript and Chart.js to independently recreate the desired functionality.

## 4.5 Concept interaction behavior to reproduce

The following interactions are mandatory:

### Theme

Three theme options:

- Light
- Dark
- System

Persist with:

quantai-theme

System must follow the operating system's prefers-color-scheme.

### Chart

Periods:

- 1D
- 1W
- 1M
- 3M
- 6M
- 1Y
- 5Y

All periods must be instant browser-side interactions.

Crosshair and tooltip work on pointer movement.

Tooltip displays the correct date and price for the actual data point.

No server request when changing periods or moving the crosshair.

Use Chart.js with a suitable custom crosshair/tooltip implementation.

Load one JSON payload containing the available chart history.

Filter periods client-side.

### Expandable sections

Use native HTML:

<details>
<summary>...</summary>
...
</details>

Use browser-native expand/collapse interactions.

No server request for opening and closing these sections.

### System interaction rule

Instant interactions must not call the server:

- Theme switching.
- Chart period switching.
- Crosshair.
- Tooltip interaction.
- Drawer open/close.
- Modal open/close.
- Expand/collapse.

This rule applies to the relevant Parts 06–10 and must be preserved in future parts.

---

# 5. VISUAL VERIFICATION — MANDATORY FOR EVERY PART

Before every push in this batch, perform the following comparison:

1. Start the running QuantAI application.
2. Open the running application in the browser tool.
3. Open the original design concept in the browser tool.
4. Compare the application and concept side by side.
5. Use identical viewport widths.
6. Inspect Light theme.
7. Inspect Dark theme.
8. Fix all visible differences relevant to the current part.
9. Repeat inspection after fixing.
10. Report the final result.

Required comparison matrix:

| Viewport | Theme | Required |
|---|---|---|
| 1440px | Light | Yes |
| 1440px | Dark | Yes |
| 390px | Light | Yes |
| 390px | Dark | Yes |

The browser comparison must be side by side.

Do not merely inspect a screenshot of the concept and assume the new application matches.

Use the actual browser tool to inspect both.

For the current implementation, compare all currently implemented sections and confirm that the new work matches the reference.

For a backend-focused Part 09, still perform the comparison to confirm no visual regressions were introduced.

Fix:
- Incorrect spacing.
- Color mismatches.
- Typography differences.
- Card radius and shadow differences.
- Broken alignment.
- Mobile overflow.
- Incorrect segmented controls.
- Broken chart or theme presentation.
- Inconsistent responsive layouts.

Do not invent design features when the concept does not specify them.

For UI areas that the concept does not define, derive the design from its extracted tokens and component patterns.

If the browser tool is unavailable:

- Report that visual verification cannot be performed.
- Do not claim visual parity.
- Stop the current part.
- Do not run push_part.py.
- Do not mark the part complete.
- Do not continue to the next part.

Visual inspection is a mandatory pre-push acceptance criterion for Parts 06–10.

---

# PART 06 — DESIGN SYSTEM, TAILWIND AND ASSETS

## Goal

Implement the new Apple-style QuantAI interface using the exact design reference.

This part establishes the reusable design system for all subsequent UI work.

The main goal is not to copy the reference code.

The main goal is to reproduce its visual appearance using the approved Python architecture.

## Exact original source files to read

From E:\Quant-AI:

1. client/src/index.css
2. client/index.html
3. client/src/components/BrandMark.tsx
4. client/src/components/MetricCard.tsx
5. client/src/components/MarketChart.tsx
6. client/src/components/AnalysisPanel.tsx
7. client/src/components/ChatPanel.tsx
8. client/src/components/ThemeToggle.tsx
9. client/src/components/ui/button.tsx
10. client/src/components/ui/card.tsx
11. client/src/components/ui/dialog.tsx
12. client/src/components/ui/input.tsx
13. client/src/components/ui/label.tsx
14. client/src/components/ui/sheet.tsx
15. client/src/components/ui/separator.tsx
16. client/src/components/ui/skeleton.tsx
17. client/src/components/ui/sonner.tsx
18. client/src/components/ui/toggle.tsx
19. client/src/components/ui/tooltip.tsx

From the design reference:

E:\QuantAI-design\Main.dc.html

Also read the reference README.md if present.

## Exact static assets to copy

Source:

E:\Quant-AI\client\public\assets\

Destination:

E:\QuantAI-Python\static\assets\

Copy all four original images:

- analysts-ledger-briefing.jpg
- analysts-ledger-hero.jpg
- analysts-ledger-logo.png
- analysts-ledger-market.jpg

Do not modify the source assets.

Do not copy assets from the concept archive unless they are explicitly part of the approved original brand asset inventory.

## Exact project files to create/update

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
- tests/test_design_tokens.py
- tests/test_static_assets.py

## Dependencies

Parts 01–05.

## A. Tailwind 4.1.14 standalone CLI

Do not commit the standalone Tailwind binary.

Create scripts/build_css.py.

Requirements:

1. Detect operating system and architecture.
2. Select the official Tailwind 4.1.14 standalone executable for the current OS.
3. Resolve the correct official release asset.
4. Check whether an official checksum file is published.
5. If an official checksum exists, download/use and verify it.
6. If no official checksum is available, calculate SHA-256 after downloading the exact official release asset.
7. Pin the locally calculated checksum in scripts/build_css.py with an explanatory comment.
8. Never invent a checksum.
9. Verify the downloaded binary against its pinned checksum before executing it.
10. Abort on a mismatch.
11. Abort on unsupported platforms.
12. Store the executable under tools/.
13. Keep tools/ gitignored.
14. Never commit the executable.
15. Commit generated static/css/app.css.

The implementation must run on Windows PowerShell.

No Node.js, npm, npx or pnpm.

The Part 06 summary must report:

- Official asset name.
- Official checksum availability.
- Checksum source.
- Whether it was publisher-provided or locally calculated.
- Where it was pinned.
- Verification result.

Do not claim a locally calculated checksum is an official published checksum.

## B. Extract and implement design tokens

Use Main.dc.html as the authoritative source.

Extract both themes.

The inspected light-theme tokens include:

- Background: #f5f5f7
- Card: #ffffff
- Fill: #f0f0f3
- Text: #1d1d1f
- Muted: #6e6e73
- Hairline: rgba(0,0,0,.08)
- Link: #0066cc
- Positive: #1a9c3c
- Positive strong: #1a7f37
- Positive background: #e6f4ea
- Warning: #b25000
- Warning background: #fff1e0
- Information: #0050a0
- Information background: #eaf2fd
- Shadow: 0 1px 2px rgba(0,0,0,.04), 0 8px 28px rgba(0,0,0,.05)
- Frosted glass: rgba(245,245,247,.8)
- Tooltip background: #1d1d1f
- Tooltip text: #ffffff
- Tooltip secondary: #a1a1a6
- Segmented selected surface: #ffffff
- Chart track: #e5e5ea
- Chip: #ffffff
- Brand: #1d1d1f
- Chart grid: #ececf0

The inspected dark-theme tokens include:

- Background: #000000
- Card: #1c1c1e
- Fill: #2c2c2e
- Text: #f5f5f7
- Muted: #a1a1a6
- Hairline: rgba(255,255,255,.12)
- Link: #2997ff
- Positive: #30d158
- Positive background: rgba(48,209,88,.16)
- Warning: #ffb340
- Warning background: rgba(255,179,64,.16)
- Information: #64b5ff
- Information background: rgba(10,132,255,.2)
- Shadow: 0 0 0 1px rgba(255,255,255,.06)
- Frosted glass: rgba(0,0,0,.72)
- Tooltip background: #f5f5f7
- Tooltip text: #1d1d1f
- Tooltip secondary: #6e6e73
- Segmented selected surface: #636366
- Chart track: #3a3a3c
- Chip: #1c1c1e
- Brand: #f5f5f7
- Chart grid: #2c2c2e

Recheck every value against the actual HTML.

Use CSS variables for all tokens.

If another token exists in the concept that has not been listed above, capture it too.

Do not blindly limit extraction to this list.

## C. Typography and dimensions

Reproduce the actual reference values, including:

- Font stack: -apple-system, BlinkMacSystemFont, SF Pro Display, Inter, Segoe UI, sans-serif.
- Tight letter spacing.
- Hero size: 56px desktop.
- Hero line height: 1.05.
- Main price: 56px desktop.
- Company title: 40px.
- Secondary heading: 22px.
- Eyebrow: 12px.
- Card radius: 22px.
- Card padding: 28px.
- Metric radius: 16px.
- Metric padding: 18px.
- Chip radius: 999px.
- Segmented control radius: 10px.
- Segmented button radius: 8px.
- Header height: 56px.
- Header maximum width: 1160px.
- Main content maximum width: 1160px.
- Desktop page spacing and grid gaps from the source.
- 900px responsive breakpoint.
- Reduced-motion behavior.

Use exact reference values where defined, not approximations from memory.

Do not redistribute proprietary fonts.

Use the system font stack and Inter only as an available local fallback.

Do not introduce an essential Google Fonts CDN dependency.

## D. Reusable components

Implement Jinja2 macros for:

- Brand mark.
- Metric cards.
- Icons.
- Dialogs.

Create consistent CSS classes for:

- Cards.
- Eyebrows.
- Chips.
- Segmented controls.
- Status badges.
- Metrics.
- Responsive grids.
- Charts.
- Tooltips.
- Buttons.
- Layout rows.

Do not copy React component code.

## E. Functional appearance

Build the following visual foundations:

- Sticky frosted-glass header.
- Responsive brand/navigation header.
- Editorial hero.
- Pill-shaped search styling.
- Quick-search pill styling.
- Primary action buttons.
- Company identity layout foundations.
- Market price typography.
- Metric card styling.
- Chart container.
- Signal score ring foundations.
- Research cards.
- News/event card foundations.
- Expandable details styling.
- Toast and dialog styling.
- Floating chat button foundation.

Some sections will become functional in later parts. This part establishes their reusable design primitives.

Do not introduce fake market data to demonstrate the design.

## F. Static assets

Copy all four approved original images into static/assets/.

Verify their dimensions and non-zero file sizes.

## Tests

Create tests before implementation.

Required:

- tests/test_css_build.py
- tests/test_design_tokens.py
- tests/test_static_assets.py

Test:

- Tailwind executable resolution.
- Supported OS detection.
- Official checksum lookup or locally pinned checksum.
- SHA-256 verification.
- Mismatch abort.
- CSS output generation.
- CSS token declarations.
- Light-theme variables.
- Dark-theme variables.
- Four image assets.
- Jinja macro output.

## Visual verification

Mandatory.

Compare the concept and running application side by side:

- 1440px Light.
- 1440px Dark.
- 390px Light.
- 390px Dark.

Fix every difference related to the design system.

## Acceptance criteria

- Exact reference design tokens extracted.
- Both themes implemented.
- Typography and dimensions match.
- Tailwind 4.1.14 standalone build works.
- Binary is not committed.
- CSS is committed.
- All four original images are committed.
- Reusable Jinja macros work.
- Mobile layout is responsive.
- No Node.js.
- No concept runtime or generated sample content in the repository.
- All tests pass.
- Browser comparison completed.

## Commit

part 06: implement approved design system and assets

## Push

.\.venv\Scripts\python.exe migration\push_part.py 6 "part 06: implement approved design system and assets"

---

# PART 07 — PERSISTENT LIGHT / DARK / SYSTEM THEME

## Goal

Recreate the complete theme behavior from the original application while matching the design reference's segmented theme controls.

The interface must support Light, Dark and System modes.

## Exact original source files to read

1. E:\Quant-AI\client\src\contexts\ThemeContext.tsx
2. E:\Quant-AI\client\src\components\ThemeToggle.tsx
3. E:\Quant-AI\client\index.html

Design reference:

E:\QuantAI-design\Main.dc.html

## Exact Python/static files to create or update

- static/js/theme.js
- templates/partials/theme_toggle.html
- templates/base.html
- tests/test_theme_system.py

## Dependencies

Parts 05–06.

## Skills

- test-driven-development
- source-driven-development
- frontend-ui-engineering
- code-review-and-quality

## Implementation requirements

### A. Theme modes

Implement:

- Light.
- Dark.
- System.

The selected theme must be represented by an accessible segmented control.

Match the reference appearance.

### B. localStorage

Use exactly:

quantai-theme

Persist the user's explicit selection.

Handle invalid stored values safely.

Keep storage behavior compatible with the original app.

### C. System mode

Read:

window.matchMedia("(prefers-color-scheme: dark)")

When System is selected:

- Light OS preference activates the light design.
- Dark OS preference activates the dark design.
- Changes to the OS preference update the current page immediately.

Register and clean up the media query listener appropriately.

### D. Anti-flicker behavior

The original HTML contains an initial theme script to prevent theme flashing.

Recreate this in the Jinja2 base template.

The script must execute before the page paints.

Restore the selected theme from localStorage.

Correctly resolve System using the OS setting.

### E. Instant behavior

Theme switching must:

- Work immediately.
- Make no server request.
- Not reload the page.
- Not reset research state.
- Update all theme-dependent tokens.
- Update cards, headers, chart surfaces and tooltip styles.
- Preserve the current theme selection.

Do not use HTMX for the theme switch.

Use vanilla JavaScript.

### F. Visual parity

Match the actual reference control:

- Segmented background.
- Selected segment.
- Inactive segment.
- Typography.
- Padding.
- Corner radius.
- Light and dark state.

## Tests

Create:

tests/test_theme_system.py

Cover:

- Default state.
- Stored Light.
- Stored Dark.
- Stored System.
- Invalid stored preference.
- System light.
- System dark.
- OS preference change.
- Persistent reload.
- Correct localStorage key.
- No server request on theme switching.

## Visual verification

Compare app and concept side by side:

- 1440px Light.
- 1440px Dark.
- 390px Light.
- 390px Dark.

Verify the theme selector and all theme-dependent surfaces.

Fix visible differences before push.

## Acceptance criteria

- Light/Dark/System all work.
- Correct localStorage key.
- Anti-flicker script works.
- System preference tracks OS changes.
- Theme updates instantly without network requests.
- No page reload is required.
- Accessibility and keyboard use are preserved.
- Visual appearance matches the design reference.
- All tests pass.

## Commit

part 07: implement persistent three-mode theme

## Push

.\.venv\Scripts\python.exe migration\push_part.py 7 "part 07: implement persistent three-mode theme"

---

# PART 08 — COMPANY SEARCH AND QUICK-SEARCH INTERFACE

## Goal

Rebuild the original company search interface using the approved concept's pill-shaped search design and shortcut chips.

Search behavior must come from the original QuantAI code.

Visual appearance must come from Main.dc.html.

## Exact original source files to read

1. E:\Quant-AI\client\src\pages\Home.tsx
2. E:\Quant-AI\client\src\hooks\useComposition.ts
3. E:\Quant-AI\client\src\hooks\usePersistFn.ts
4. E:\Quant-AI\client\src\hooks\useMobile.tsx
5. E:\Quant-AI\client\src\lib\research.ts

Also inspect the current Python web application from Parts 05–07.

Design reference:

E:\QuantAI-design\Main.dc.html

## Exact Python/static files to create or update

- api/web/search.py
- templates/partials/search_form.html
- static/js/search.js
- templates/pages/home.html
- tests/test_search_flow.py
- tests/test_search_ime.py

## Dependencies

Parts 03–07.

## Skills

- test-driven-development
- source-driven-development
- frontend-ui-engineering
- code-review-and-quality

## Implementation requirements

### A. Search behavior

Preserve:

- Search by ticker symbol.
- Search by company name.
- Enter-key submission.
- Search button submission.
- Original query normalization.
- Original empty-input behavior.
- Existing error behavior.

Inspect Home.tsx and its callers before implementing.

### B. Quick search shortcuts

Preserve:

- AAPL.
- MSFT.
- NVDA.
- TSLA.

Each chip must trigger the intended search.

Do not hardcode sample company results.

### C. Search design

Use the concept's actual design:

- Rounded pill input.
- Search icon.
- Large readable input text.
- Primary blue action button.
- Pill-shaped shortcuts.
- Correct hover/focus states.
- Correct spacing.
- Responsive wrapping.

Use extracted design tokens rather than copied concept markup.

### D. No mode picker

IMPORTANT:

The original Home.tsx does not contain a user-selectable mode picker.

Do not invent one.

Preserve the original automatic dual research execution:

- Market Intelligence.
- Company Deep Analysis.

Their actual orchestration is handled in Part 09.

### E. IME behavior

Preserve the original useComposition.ts behavior.

Enter while composing an IME character must not prematurely submit the search.

Handle keyboard events correctly.

### F. Request cancellation

Prepare the search integration for original stale-request protection.

Use HTMX `hx-sync` appropriately.

Do not allow a stale search response to overwrite a newer query.

The detailed research sequencing remains implemented and tested in Part 09.

### G. Responsive behavior

At 390px:

- Search input must remain usable.
- Action button must remain accessible.
- Chips must wrap without horizontal overflow.
- No clipped or overlapping controls.

## Tests

Create:

- tests/test_search_flow.py
- tests/test_search_ime.py

Cover:

- Ticker search.
- Company-name search.
- AAPL quick action.
- MSFT quick action.
- NVDA quick action.
- TSLA quick action.
- Empty input.
- Whitespace normalization.
- Enter submission.
- Button submission.
- IME composition.
- Keyboard accessibility.
- Mobile layout.
- Correct absence of a user-selectable research mode.

## Visual verification

Compare application and concept side by side:

- 1440px Light.
- 1440px Dark.
- 390px Light.
- 390px Dark.

Pay particular attention to:

- Hero spacing.
- Search width.
- Search pill height.
- Search padding.
- Button dimensions.
- Quick-chip shape.
- Chip spacing.
- Responsive wrapping.

Fix visible differences.

## Acceptance criteria

- Search behavior matches original Home.tsx.
- Four quick-search shortcuts work.
- Enter and action button work.
- IME behavior works.
- No invented search-mode selector.
- No sample data.
- Search UI visually matches the reference.
- Mobile layout works.
- Relevant tests pass.

## Commit

part 08: implement company search interface

## Push

.\.venv\Scripts\python.exe migration\push_part.py 8 "part 08: implement company search interface"

---

# PART 09 — RESEARCH ORCHESTRATION AND ERROR GUIDANCE

## Goal

Connect the new search interface to the existing research backend while preserving the original TypeScript execution semantics.

Implement proper parallel requests, independent success/failure handling, stale-response protection and normalized error guidance.

This part focuses primarily on business logic and API orchestration.

## Exact original source files to read

1. E:\Quant-AI\client\src\pages\Home.tsx
2. E:\Quant-AI\client\src\lib\research.ts
3. E:\Quant-AI\client\src\lib\agentos.ts
4. E:\Quant-AI\tests\test_research_error_guidance.ts

Also read:

- Existing api/research_orchestrator.py.
- Existing api/research_errors.py.
- Existing api/web/presenters.py.
- Existing api/web/search.py.
- Relevant Part 01–08 tests.

## Exact Python/static files to create or update

- api/web/research.py
- api/web/routes.py
- api/web/presenters.py
- static/js/research.js
- tests/test_web_research_orchestration.py
- tests/test_research_error_guidance.py

## Dependencies

Parts 03–08.

## Skills

- test-driven-development
- source-driven-development
- code-review-and-quality

No additional frontend-ui-engineering skill is required for this part.

## Implementation requirements

### A. Preserve dual research execution

Read the actual original Home.tsx implementation.

The application automatically starts two research operations in parallel:

1. Market Intelligence:
   - mode: market_intelligence
   - include_analysis=true

2. Company Deep Analysis:
   - mode: company_deep_analysis
   - include_analysis=false

These operations are not controlled by a user-selected mode.

Preserve the exact original semantics.

### B. Partial result handling

Use asynchronous execution and an equivalent of Promise.allSettled.

Required behavior:

- Both operations can succeed.
- Market Intelligence can succeed while Deep Analysis fails.
- Deep Analysis can succeed while Market Intelligence fails.
- One failure must not erase valid results from the other operation.
- Both failures must produce the correct guidance.
- AI unavailability must not destroy deterministic market data.

### C. Request ordering and cancellation

Preserve the original request sequence behavior.

Implement:

- A new sequence ID for each submitted research query.
- Stale response rejection.
- Cancellation of obsolete client requests where supported.
- HTMX `hx-sync` replacement behavior.
- Safe cleanup of previous requests.

A slow previous request must never overwrite newer research.

Avoid introducing duplicated execution.

### D. Public error classification

Port the original `researchErrorKind` logic.

Supported categories:

- ambiguous
- not_found
- ai_unavailable
- news_unavailable
- other

Preserve the actual original text/classification behavior.

Do not expose raw Python exceptions to the browser.

### E. Server integration

Use the existing FastAPI backend.

Do not create a second research backend.

Do not introduce a self-HTTP call.

Use the canonical existing research orchestrator and services.

### F. Browser behavior

New search submissions remain server-backed.

Loading status and stale-response handling must remain correct.

Previous results must not be incorrectly overwritten.

### G. Regression test port

Port the original:

E:\Quant-AI\tests\test_research_error_guidance.ts

into:

tests/test_research_error_guidance.py

Preserve every original assertion.

Do not weaken or remove any case.

## Tests

Create:

- tests/test_web_research_orchestration.py
- tests/test_research_error_guidance.py

Cover:

- Both requests succeed.
- Market Intelligence succeeds alone.
- Deep Analysis succeeds alone.
- Both requests fail.
- Correct mode arguments.
- Correct include_analysis flags.
- Parallel execution.
- Partial failure.
- Request sequence handling.
- Stale response rejection.
- Abort/cancellation.
- Each of the five original public error categories.
- Unknown error fallback.
- Original TypeScript error-guidance assertions.

## Visual verification

Before push, compare the current running application and concept side by side at:

- 1440px Light.
- 1440px Dark.
- 390px Light.
- 390px Dark.

Even though this part is primarily orchestration, confirm that the research submission, loading and result state changes have not caused visible regressions.

If no UI changes were necessary, state that the comparison was performed and no visual regressions were observed.

## Acceptance criteria

- Both research requests preserve original semantics.
- Parallel execution is correct.
- Partial results survive independent failures.
- Stale responses cannot replace newer results.
- Correct error categories are displayed.
- No user-facing mode picker.
- No self-HTTP server requests.
- The TypeScript error guidance test is ported completely.
- Full pytest passes.
- Browser comparison is completed.

## Commit

part 09: implement research orchestration and error guidance

## Push

.\.venv\Scripts\python.exe migration\push_part.py 9 "part 09: implement research orchestration and error guidance"

---

# PART 10 — COMPANY IDENTITY DOSSIER AND RESEARCH STATES

## Goal

Implement the complete company identity section and research status presentation.

The functional behavior comes from the original QuantAI application.

The visual appearance comes from Main.dc.html.

## Exact original source files to read

1. E:\Quant-AI\client\src\pages\Home.tsx
2. E:\Quant-AI\client\src\components\MetricCard.tsx
3. E:\Quant-AI\client\src\components\ErrorBoundary.tsx
4. E:\Quant-AI\client\src\lib\market.ts
5. E:\Quant-AI\client\src\lib\research.ts

Also read:

- api/research_schemas.py.
- api/web/contracts.py.
- api/web/presenters.py.
- api/web/research.py.
- templates/partials already created in Parts 05–09.

Design reference:

E:\QuantAI-design\Main.dc.html

## Exact Python/template files to create

- templates/partials/identity_dossier.html
- templates/partials/research_status.html
- templates/partials/research_skeleton.html
- tests/test_identity_dossier.py
- tests/test_research_states.py

Update only already-approved existing templates where required.

## Dependencies

Parts 03–09.

## Skills

- test-driven-development
- source-driven-development
- frontend-ui-engineering
- code-review-and-quality

## Implementation requirements

### A. Company identity

Display actual backend-provided information:

- Ticker symbol.
- Full company name.
- Sector.
- Industry.
- Exchange.

Do not use sample Apple values from the concept.

Do not hardcode company identity information.

### B. Verified and pending status

Preserve the original distinction between:

- Verified identity.
- Pending identity.

Render states using the approved design's badge and typography patterns.

Do not infer verification status from arbitrary frontend guesses.

Use the actual response and original mapping behavior.

### C. Price/banner integration

Use the original company identity layout from the new design reference.

The actual quote information must come from the existing QuantAI backend.

This includes:

- Current market price when available.
- Latest historical close when markets are closed.
- Absolute change.
- Percentage change.
- Semantic positive/negative display.

Do not hardcode the design concept's illustrative price.

### D. Research status

Implement distinguishable states:

- Idle.
- Checking/loading.
- Success.
- Partial success.
- Ambiguous entity.
- Not found.
- AI unavailable.
- News unavailable.
- Other errors.

Use the previously implemented Part 09 classification.

### E. Loading skeleton

Implement the original shimmer/loading behavior.

Follow the design reference's card, surface and spacing language.

Honor `prefers-reduced-motion`.

Avoid layout jumps when loading content replaces the skeleton.

### F. Error handling

Preserve useful recovery guidance.

Do not expose:

- Stack traces.
- Internal file paths.
- Prompt templates.
- Provider API credentials.
- Raw exception details.

Valid deterministic market data must remain visible when AI is unavailable.

### G. Visual structure

Recreate the design concept's identity arrangement:

- Ticker badge.
- Verified identity badge.
- Company title.
- Sector/industry/exchange line.
- Prominent price display.
- Price change.
- Appropriate supporting text.

Use the design tokens from Part 06.

Use responsive alignment matching the concept.

On mobile, identity and pricing sections must stack properly and maintain readable spacing.

### H. Native interactions

Use native details/summary when implementing any expandable information.

Do not send an HTTP request simply to expand or collapse a section.

## Tests

Create:

- tests/test_identity_dossier.py
- tests/test_research_states.py

Test:

- Complete verified identity.
- Pending identity.
- Missing ticker.
- Missing company name.
- Missing sector.
- Missing industry.
- Missing exchange.
- Market open price.
- Market closed historical close.
- Positive change.
- Negative change.
- Zero change.
- Ambiguous entity.
- Not found.
- Loading.
- Partial success.
- AI unavailable with deterministic data preserved.
- Sanitized error guidance.
- Skeleton behavior.
- Reduced-motion behavior.

## Visual verification

Compare the app and the reference side by side:

- 1440px Light.
- 1440px Dark.
- 390px Light.
- 390px Dark.

Fix:

- Identity layout differences.
- Title typography.
- Ticker badge.
- Verification badge.
- Price size and positioning.
- Change colors.
- Responsive stacking.
- Card spacing.
- Status presentation.
- Skeleton sizing and animation.

No unresolved visible problems may be silently ignored.

## Acceptance criteria

- Full company identity displayed.
- Verified/pending logic preserved.
- Actual financial values used.
- No design sample values in application data.
- All research states supported.
- Error details sanitized.
- Loading state works.
- Reduced-motion honored.
- Responsive layout works.
- Visual comparison completed.
- Tests pass.

## Commit

part 10: implement company identity dossier and research states

## Push

.\.venv\Scripts\python.exe migration\push_part.py 10 "part 10: implement company identity dossier and research states"

---

# 6. COMMON TESTING AND REVIEW WORKFLOW

For EVERY part:

1. Print the required Skills used line.
2. Read exact original source files.
3. Inspect relevant existing Python implementation.
4. Write tests first.
5. Implement only the current part.
6. Run focused tests.
7. Run the complete suite.
8. Fix failures up to the approved maximum.
9. Review the complete Git diff.
10. Perform the mandatory browser comparison.
11. Check for protected files and secrets.
12. Update migration/PROGRESS.md.
13. Run push_part.py.
14. Verify commit and push.
15. Continue automatically to the next part.

Use the project's virtual environment:

`.\.venv\Scripts\python.exe`

Full suite:

`.\.venv\Scripts\python.exe -m pytest -q`

Do not rely on a global Python executable.

---

# 7. PROGRESS FILE RULE

Before every part push:

- Mark the current part checked in migration/PROGRESS.md.
- Include the modified PROGRESS.md in that part's commit.

The checkbox is a pre-push completion-intent marker.

Only a successful push confirms that the part is actually complete.

If push fails, stop and report the local commit state.

Never mark a failed push as complete.

---

# 8. MANDATORY COMMIT AND PUSH RULES

Each part must have exactly one commit.

Use ONLY:

`.\.venv\Scripts\python.exe migration\push_part.py <part_no> "part NN: description"`

Approved commands:

PART 06:

`.\.venv\Scripts\python.exe migration\push_part.py 6 "part 06: implement approved design system and assets"`

PART 07:

`.\.venv\Scripts\python.exe migration\push_part.py 7 "part 07: implement persistent three-mode theme"`

PART 08:

`.\.venv\Scripts\python.exe migration\push_part.py 8 "part 08: implement company search interface"`

PART 09:

`.\.venv\Scripts\python.exe migration\push_part.py 9 "part 09: implement research orchestration and error guidance"`

PART 10:

`.\.venv\Scripts\python.exe migration\push_part.py 10 "part 10: implement company identity dossier and research states"`

Never run:

- git add -A
- git commit
- git push

as independent commands.

The only approved commit/push flow is push_part.py.

The push script must verify:
- Correct repository.
- Correct origin.
- Branch main.
- Git author email.
- Progress checkbox.
- Prior consecutive part commits.
- No staged changes.
- Full pytest success.
- Safe explicit staging.

It must create exactly one commit and push exactly once.

If the push fails after committing, do not retry automatically and do not create another commit.

---

# 9. STOP CONDITIONS

Stop immediately if:

1. Tests remain failing after three fix attempts.
2. A critical original behavior is unclear.
3. A critical visual reference is unavailable.
4. The browser tool is unavailable.
5. A visual verification checkpoint cannot be completed.
6. An essential dependency is unavailable.
7. The approved architecture would need to change.
8. A source/API contradiction is found.
9. A secret is detected in planned staging.
10. The Git remote or branch is wrong.
11. The push script fails.
12. A previous part is incomplete.

Do not skip the part.

Do not merge commits.

Do not continue beyond a critical blocker.

---

# 10. FINAL BATCH COMPLETION

After PART 10 successfully passes tests, visual verification and push:

Verify:

- Parts 06–10 checked.
- Five new part commits.
- Five successful pushes.
- Parts 01–10 all checked.
- Ten total migration part commits exist.
- Full pytest passes.
- All visual checkpoints for Parts 06–10 completed.
- Design reference was used correctly.
- Concept code and generated data were not copied.
- The original source repository remains untouched.

Provide a BATCH_02 summary containing:

## Part-by-part results

For every part:
- Part number.
- Implementation summary.
- Focused test count/result.
- Full pytest result.
- Commit SHA.
- Push confirmation.
- Visual comparison at all four required states.

## Design extraction summary

Report:
- Design tokens extracted.
- Light and dark theme implementation.
- Typography.
- Spacing and radii.
- Shadows.
- Components created.
- Any visual differences still unresolved.

## Tailwind checksum report

For Part 06:
- Official release asset.
- Whether an official checksum existed.
- Official or locally calculated hash.
- Hash verification result.
- CSS output committed.
- Binary excluded from Git.

## Repository status

Report:
- Git branch.
- Remote.
- Commit count.
- Progress checklist.
- Remaining limitations.

## Next batch

BATCH_03 — Parts 11–15.

Do not begin BATCH_03.

After successful Part 10, print:

BATCH COMPLETE, STOP

Then print:

DAY COMPLETE

Wait for the user's next instruction.

---

# FINAL NON-NEGOTIABLE RULE

The design reference determines the appearance.

The original QuantAI source determines the functionality.

Never confuse sample design data with real financial information.

Never copy the design runtime.

Never replace original business logic with design mockup logic.

Rebuild the design independently using the approved Python stack.

Complete all five parts, verify them, commit them individually and stop after Part 10.
