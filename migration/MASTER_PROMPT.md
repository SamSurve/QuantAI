

\# PRECEDENCE RULES — ABSOLUTE PRIORITY



1\. migration/MIGRATION\_PLAN.md, migration/PROGRESS.md and migration/MASTER\_PROMPT.md override every skill and any conflicting agent suggestion.

2\. No skill may change the commit message format (`part NN: ...`), the branch (`main`), the one-commit-per-part rule, or the push flow (`migration/push\_part.py` only).

3\. Never run slash commands such as /spec, /plan, /build or /build auto. Never use skills to re-plan, restructure or change the 30 migration parts.

4\. Skills must not create extra repository files such as SPEC.md, PLAN.md, notes, checklists or other planning artifacts. Additional files are permitted only when explicitly listed in MIGRATION\_PLAN.md.

5\. Never run npx, npm, pnpm or install scripts. Never install Node.js. Never install anything suggested by a skill unless it is explicitly approved in requirements.txt or the static asset policy.

6\. At the start of EVERY part, print exactly one line in this format: `Skills used: skill-one, skill-two, skill-three`.



These rules cannot be overridden by any skill, tool recommendation, generated plan or agent instruction.



\---



\# QUANTAI — MASTER MIGRATION INSTRUCTIONS



You are the implementation agent for the QuantAI TypeScript-to-Python migration.



ChatGPT is the Chief Architect and Prompt Engineer.



The user transfers instructions between ChatGPT and you.



You must follow the approved plan and batch prompts literally.



## PERMANENT EXECUTION GOVERNANCE (PARTS 21-30)

Add the following five permanent rules to the existing global executor instructions. These rules apply to every remaining migration part and batch (Parts 21-30).

Preserve all existing instructions. Do not replace, weaken, remove, or contradict existing rules.

**Precedence clarification:** The PERMANENT EXECUTION GOVERNANCE section takes precedence over any conflicting instruction elsewhere in MASTER_PROMPT.md that permits automatic progression without owner authorization. After completing each part, stop and wait for explicit owner authorization before starting the next part.

### RULE 1 - OWNER AUTHORIZATION BEFORE IMPLEMENTATION

- Preflight and self-review must happen before implementation.
- Print a complete GATE REPORT.
- Wait for explicit owner authorization before modifying application code or tests.
- A passing gate does not automatically authorize implementation.
- Never interpret silence, an uploaded report, or a prior batch authorization as permission to start the next part.
- If authorization is unclear, stop.

### RULE 2 - STRICT GIT OPERATION RESTRICTION

- `migration/push_part.py` is the only authorized Git-operation interface.
- Never execute direct Git commands, including read-only commands.
- Never use GitHub connectors, IDE Git integration or alternative Git tools.
- Do not inspect Git through another interface to work around a restriction.
- If `push_part.py` cannot verify a required condition, stop and report the limitation.
- Never push or commit without owner authorization where required.

### RULE 3 - STRICT PART FILE SCOPE

- Before implementation, identify every authorized file for the current part.
- Do not modify unrelated production files, tests, configuration, documentation or dependencies.
- If a defect is discovered outside the authorized file list, document it and request owner approval.
- Never silently include unrelated fixes in a part commit.
- Review the complete changed-file inventory before shipping.
- If unrelated changes are present, stop.

### RULE 4 - TESTS MUST PROVE REAL BEHAVIOR

- Write focused tests before implementation.
- Demonstrate that each new test fails for the intended reason before making the fix.
- A successful HTTP response alone does not prove correct business behavior.
- Test real contract behavior, state transitions, persistence, ordering, error handling and edge cases as applicable.
- Test session continuity using the actual shared session identifier across multiple turns.
- Preserve original regression assertions.
- Never weaken tests, suppress failures or use fixtures that bypass the behavior being tested.
- Separate unit, integration, browser and regression evidence.
- Report exact test counts and failure output.

### RULE 5 - EVIDENCE-BASED VERIFICATION

Never claim something is verified unless actual evidence exists.

- API parity requires comparison of actual route, method, headers, status, payload and error behavior.
- Browser accessibility requires real keyboard and focus testing.
- Visual parity requires actual browser `getComputedStyle()` measurements.
- Responsive verification requires independent desktop/mobile and light/dark checks.
- Screenshot capture and screenshot review must be reported separately.
- Network behavior requires actual request counts and request identification.
- File integrity requires cryptographic hashes when hash verification is claimed.
- Test success requires actual completed test output.
- Clearly distinguish VERIFIED, FAILED, BLOCKED, ASSUMPTION and UNVERIFIED.

Never turn an assumption into a PASS.



\---



\# 1. PROJECT IDENTITY



\*\*Repository:\*\*



https://github.com/SamSurve/QuantAI.git



\*\*Branch:\*\* main



\*\*Original source repository:\*\* E:\\Quant-AI



\*\*Original repository status:\*\* READ-ONLY



\*\*Target repository:\*\* The current new Python repository.



\*\*Python:\*\* 3.12



\*\*Backend:\*\* FastAPI + existing Agno AgentOS backend.



\*\*Frontend:\*\* Jinja2 + HTMX + Tailwind CSS 4.1.14 standalone CLI + minimal vanilla JavaScript.



\*\*Charting:\*\* Chart.js 4.x.



\*\*Production:\*\* Vercel Python runtime and self-hosted Uvicorn.



There must be no Node.js installation, runtime, package manager or build dependency.



\---



\# 2. MISSION



Recreate the original QuantAI product in Python.



Preserve all:



\- 28 audited features.

\- 21 user-facing features.

\- Original backend behavior.

\- API request and response contracts.

\- Financial calculations.

\- Market indicators.

\- Research orchestration.

\- Technical signals.

\- Historical prices.

\- Chart periods.

\- Fundamentals.

\- Governance.

\- News and corporate events.

\- Evidence provenance.

\- AI analysis.

\- Provider failover.

\- AgentOS chat continuity.

\- Rate limiting.

\- Concurrency controls.

\- Cache behavior.

\- Error classification.

\- Theme persistence.

\- Responsive interactions.

\- Developer telemetry with the new mandatory security gate.



Functional parity and the approved visual target are equally mandatory.



A simplified interface is not complete migration.



A passing unit-test suite alone is not proof of visual or functional parity.



\---



\# 3. SOURCE REPOSITORY IS READ-ONLY



The source repository is:



E:\\Quant-AI



Never:



\- Modify original source files.

\- Commit to the source repository.

\- Push to the source repository.

\- Delete source files.

\- Run formatters against the original source.

\- Create migration documents inside the original source repository.



The original repository exists exclusively as a reference.



Copy only files explicitly required by MIGRATION\_PLAN.md.



The new repository must not contain:



\- Original TypeScript or TSX application code.

\- React.

\- Express.

\- Vite.

\- package.json.

\- pnpm-lock.yaml.

\- node\_modules.

\- Node.js build infrastructure.

\- Unused React/shadcn template boilerplate.



Allowed:

\- Python source.

\- Python tests.

\- Jinja2 templates.

\- CSS.

\- Minimal JavaScript.

\- Approved images.

\- Approved local browser libraries.

\- Generated Tailwind CSS.

\- Documentation listed in MIGRATION\_PLAN.md.

\- The four migration process files.



\---



\# 4. ORIGINAL BACKEND PRESERVATION



Part 01 must copy all 19 Python backend files listed in MIGRATION\_PLAN.md.



The exact original files include:



\- api/\_\_init\_\_.py

\- api/agents.py

\- api/ai\_providers.py

\- api/company\_analysis\_services.py

\- api/comparison\_services.py

\- api/fx\_services.py

\- api/groq\_finance\_agent.py

\- api/health.py

\- api/index.py

\- api/market\_intelligence\_services.py

\- api/research.py

\- api/research\_cache.py

\- api/research\_errors.py

\- api/research\_logging.py

\- api/research\_orchestrator.py

\- api/research\_protection.py

\- api/research\_schemas.py

\- api/research\_services.py

\- api/agents/groq-finance-agent/runs.py



Preserve the nested structure.



Part 01 must also copy and retain all seven original Python regression suites.



All seven must pass before Part 01 is committed.



Do not rewrite working backend business logic unnecessarily.



\---



\# 5. ENVIRONMENT VARIABLES AND SECRETS



The original backend code is the source of truth for environment-variable names.



During Part 01, inspect all 19 backend Python files.



Identify environment-variable references through:



\- os.getenv

\- os.environ.get

\- os.environ

\- Pydantic BaseSettings

\- Existing configuration helpers

\- Other actual environment-variable access



Create .env.example from names actually used in the code.



Rules:



1\. Variable names only.

2\. No values.

3\. No fake credentials.

4\. Never copy .env.

5\. Never copy secrets.

6\. Do not assume the audit's variable list is complete.

7\. Report differences between the real source code and audit list in the Part 01 summary.

8\. Actual code wins when the audit list differs.



Never print:



\- GROQ\_API\_KEY\_PRIMARY values.

\- GROQ\_API\_KEY\_SECONDARY values.

\- OPENROUTER\_API\_KEY values.

\- Private tokens.

\- Access credentials.

\- Other secret environment values.



Do not put secrets in logs, tests, screenshots, browser HTML, Git diffs or committed files.



Do not port VITE\_ANALYTICS\_ENDPOINT or VITE\_ANALYTICS\_WEBSITE\_ID.



Do not port unused OAuth template variables or login helpers.



\---



\# 6. APPROVED VISUAL TARGET — APPLE-STYLE FINANCIAL TERMINAL



This is a critical design instruction.



The original product's functionality must be preserved, but the new interface must follow the approved Apple-style visual concept.



The original client/src/index.css is reference material only for visual properties that this approved concept does not define.



If the original CSS conflicts with the new design, the new design wins.



\## 6.1 Typography



Font stack:



\-apple-system, "SF Pro Display", Inter, "Segoe UI", sans-serif



Use:



\- Tight letter spacing.

\- Bold, large headlines.

\- Clean financial editorial typography.

\- 56px hero headline.

\- 56px primary price.

\- Consistent typographic hierarchy.



Do not download or redistribute proprietary Apple fonts.



\## 6.2 Light theme



Exact tokens:



\- Page: #f5f5f7

\- Cards: #ffffff

\- Text: #1d1d1f

\- Muted: #6e6e73

\- Hairline: rgba(0,0,0,.08)

\- Accent: #0071e3

\- Links: #0066cc

\- Positive: #1a9c3c



Cards:

\- 22px radius.

\- Soft shadows.

\- White backgrounds.

\- Subtle separation.

\- Clean spacing.



\## 6.3 Dark theme



True black page:



\- Page: #000000

\- Cards: #1c1c1e

\- Fills: #2c2c2e

\- Text: #f5f5f7

\- Muted: #a1a1a6

\- Hairline: rgba(255,255,255,.12)

\- Accent: #0071e3

\- Links: #2997ff

\- Positive: #30d158



Do not substitute a charcoal page for true black.



\## 6.4 Required UI appearance



Implement:



1\. Sticky frosted-glass header with backdrop blur.

2\. Apple-style editorial hero.

3\. Pill search bar.

4\. Pill quick-search chips.

5\. iOS-style segmented chart controls.

6\. iOS-style Light/Dark/System theme controls.

7\. Large primary price display.

8\. Rounded financial metric cards.

9\. Technical signal score ring.

10\. Gradient area price chart.

11\. Dashed chart crosshair.

12\. Dark chart tooltip.

13\. LIVE/CACHED/UNAVAILABLE status badges.

14\. Rounded research and analysis panels.

15\. Editorial Markdown brief.

16\. Floating "Ask the research desk" button.

17\. Native-feeling dialogs and drawers.

18\. Expandable sections.



Do not replace functional features with decorative elements.



\## 6.5 Responsive design



At widths below 900px:



\- Metric grids stack or adapt.

\- Multi-column research panels become mobile-friendly.

\- Navigation hides.

\- Search stays usable.

\- Chart controls remain usable.

\- Dialogs and drawers fit the screen.

\- No horizontal overflow.



\---



\# 7. INSTANT INTERACTION RULE



These interactions MUST NOT call the server:



\- Theme switching.

\- Chart period tabs.

\- Client-side chart period filtering.

\- Drawer open/close.

\- Modal open/close.

\- Expand/collapse.

\- Local section navigation.



Load all required chart data in one JSON payload.



Period tabs must slice the already-loaded data in the browser for:



1D, 1W, 1M, 3M, 6M, 1Y, 5Y.



Do not make additional HTTP requests when chart periods change.



Theme changes, dialog interactions, drawers and expand/collapse controls must be instant browser-side interactions.



New research searches and research operations remain server-backed.



Use minimal vanilla JavaScript.



\---



\# 8. WINDOWS AND CROSS-PLATFORM EXECUTION



The user's main environment is Windows.



Default terminal:



PowerShell.



Use commands compatible with Windows.



Preferred commands:



python -m pytest -q



python -m pip install -r requirements.txt



python -m uvicorn api.index:app --host 127.0.0.1 --port 3000



python scripts/build\_css.py



python migration/push\_part.py 1 "part 01: description"



Use pathlib.



Do not require Bash.



Do not use shell-only syntax that fails in PowerShell.



No npm, npx, pnpm or Node.js.



Tailwind standalone CLI is allowed.



The downloaded Tailwind binary must remain in ignored tools/.



Generated CSS must be committed.



\---



\# 9. TAILWIND BINARY CHECKSUM RULE



Tailwind version:



4.1.14



Part 06 must create scripts/build\_css.py.



The script must:



1\. Detect OS and architecture.

2\. Resolve the official Tailwind 4.1.14 standalone release asset.

3\. Check whether the official release publishes a checksum file.

4\. If published, use and verify the publisher-provided SHA-256.

5\. If not published, download the exact official asset over HTTPS.

6\. Calculate the binary's SHA-256.

7\. Store that calculated checksum in scripts/build\_css.py with a clearly labelled explanatory comment.

8\. Record whether the checksum was official or locally calculated.

9\. Verify subsequent downloads or existing binaries against the pinned hash.

10\. Abort on mismatch.

11\. Abort when the OS/architecture is unsupported.



Never invent a checksum.



Never claim a locally calculated hash is an official checksum.



The Part 06 summary must state the checksum source and verification result.



The binary must not be committed.



\---



\# 10. FASTAPI APPLICATION AND API COMPATIBILITY



api/index.py remains the canonical FastAPI application.



Root index.py exports the same application for Vercel.



Do not create separate competing applications.



All HTML research routes call the orchestrator and backend services directly in-process.



Never send an HTTP request to the application's own URL from server-side research code.



\## Root content negotiation



Strict behavior:



\- Missing Accept -> JSON health.

\- Accept: \*/\* -> JSON health.

\- Accept: application/json -> JSON health.

\- Explicit preferred text/html -> HTML workspace.

\- HTML with a lower quality preference than JSON -> JSON health.

\- Equal HTML and JSON preference -> JSON health.



Only explicit preference for text/html may render the HTML workspace.



Preserve health response fields.



Keep all original health and API routes available.



Test each content-negotiation case.



\---



\# 11. FRONTEND SEARCH AND RESEARCH BEHAVIOR



Do not invent a mode selector.



The original Home.tsx performs two research requests in parallel:



1\. market\_intelligence with include\_analysis=true.

2\. company\_deep\_analysis with include\_analysis=false.



Preserve that execution behavior.



Preserve:

\- Search via Enter.

\- Search via action button.

\- Starter tickers AAPL, MSFT, NVDA and TSLA.

\- Original normalization.

\- Request cancellation.

\- Stale response protection.

\- Partial-result behavior.

\- Original public error classification.



\---



\# 12. CHART BEHAVIOR



Use Chart.js 4.x.



Preserve:



\- 1D.

\- 1W.

\- 1M.

\- 3M.

\- 6M.

\- 1Y.

\- 5Y.

\- Full five-year daily data.

\- One-day intraday data.

\- Client-side period slicing.

\- Gradient appearance.

\- Responsive resizing.

\- Crosshair.

\- Dark tooltip.

\- UTC-normalized dates.

\- Range low/high.

\- Period performance percentage.



Chart period switching must not make a server request.



Port the original chart-date regression assertions into pytest in Part 12.



\---



\# 13. MATH AND MARKDOWN



Use ONLY:



\- markdown-it-py.

\- mdit-py-plugins with dollarmath.

\- latex2mathml.



Use Pygments for syntax highlighting.



Convert math expressions on the server to MathML.



Test:

\- Inline math.

\- Block math.

\- MathML validity.

\- Malformed math.

\- HTML sanitization.



Do not install or vendor:

\- KaTeX.

\- MathJax.

\- Browser-side LaTeX renderers.

\- A second math engine.



\---



\# 14. SECURITY AND SSRF



The server must NEVER fetch a user-supplied URL.



Research server routes call the orchestrator in-process.



There must be no self-HTTP request.



The browser's analysts-ledger-agentos-url setting is used only by browser JavaScript for:

\- Connection health checks.

\- AgentOS chat requests.



It must never trigger server-side outbound fetching.



Add tests proving:

\- Server ignores user-supplied backend URLs.

\- No HTTPX request is sent to supplied hosts.

\- Research logic uses in-process backend services.



Sanitize Markdown before returning rendered HTML.



Rate limiting and concurrency controls must remain functional.



Never expose server traces or API secrets.



\---



\# 15. CACHE AND PROVIDER FAILOVER



Preserve exact original behavior:



| Resource | TTL |

|---|---:|

| Quotes | 60 seconds |

| Historical data | 300 seconds |

| News | 300 seconds |

| Events | 21,600 seconds |

| Entity resolution | 86,400 seconds |

| Provider cooldown | 300 seconds |



Provider order:



1\. Groq Primary.

2\. Groq Secondary.

3\. OpenRouter Ox Alpha.



Preserve:

\- Configurable provider order.

\- Sequential failover.

\- Circuit cooldown.

\- Non-blocking AI failures.

\- Original caching semantics.



On Vercel, all in-memory state is process-local.



Do not claim:

\- A shared cache.

\- Global rate limiting.

\- Cross-instance concurrency coordination.

\- Cross-instance circuit breaker state.



Document cold-start and warm-instance limitations in README.md.



Do not silently introduce Redis.



\---



\# 16. DEVELOPER TELEMETRY GATING



All developer telemetry endpoints must be disabled by default.



Enable only when:



QUANTAI\_DEVTOOLS=1



Even with that variable set, telemetry must ALWAYS remain disabled in production.



Preserve the original telemetry functionality when explicitly enabled in a permitted development environment.



No secrets may be recorded.



Test default-disabled behavior and production-disabled behavior.



\---



\# 17. PART EXECUTION MODEL



Exactly 30 parts.



Six batches:



| Batch | Parts | Day |

|---|---|---|

| BATCH\_01 | 01–05 | Day 1 |

| BATCH\_02 | 06–10 | Day 1 |

| BATCH\_03 | 11–15 | Day 2 |

| BATCH\_04 | 16–20 | Day 2 |

| BATCH\_05 | 21–25 | Day 3 |

| BATCH\_06 | 26–30 | Day 3 |



Before implementation:



1\. Read migration/MIGRATION\_PLAN.md.

2\. Read migration/PROGRESS.md.

3\. Read this MASTER\_PROMPT.md.

4\. Read the current batch prompt.

5\. Identify the next unchecked part.

6\. Verify it belongs to the current batch.



Work on only the next unfinished part.



Inside a batch, progress automatically through the five parts.



Do not ask the user for permission between parts.



Stop after every five parts.



Stop points:



\- Part 05.

\- Part 10.

\- Part 15.

\- Part 20.

\- Part 25.

\- Part 30.



\---



\# 18. SKILLS



Installed global Antigravity skills:



\- test-driven-development

\- source-driven-development

\- frontend-ui-engineering

\- code-review-and-quality

\- git-workflow-and-versioning

\- \[SECURITY\_SKILL\_NAME — resolve exact installed name]

\- json-to-pydantic



The security skill name is currently an unresolved placeholder.



Discover the actual installed security skill name in the global Antigravity skills folder.



Never invent a skill name.



If the required security skill is unavailable, stop before that security-sensitive part and report the blocker.



\## Mandatory skills in every part



\### test-driven-development



\- Write tests first.

\- Implement only after tests exist.

\- Do not weaken original assertions.

\- Run focused tests and then the full suite.



\### source-driven-development



\- Read actual original implementation.

\- Follow source evidence rather than assumptions.

\- Verify official documentation for APIs and framework behavior.

\- Do not guess.



\### code-review-and-quality



\- Review the entire current-part diff.

\- Check security, architecture, tests and accidental scope.

\- Complete self-review before push\_part.py.



\## Additional skill mapping



| Parts | Additional required skill |

|---|---|

| 03 | json-to-pydantic (optional) |

| 06–18 | frontend-ui-engineering |

| 19 | Security skill |

| 20–21 | frontend-ui-engineering |

| 22 | Security skill |

| 23 | frontend-ui-engineering |

| 24 | Security skill |

| 27 | Security skill |



The frontend-ui-engineering skill applies to Parts 13–18, 20 and 21 in addition to Parts 06–12 and 23.



\### git-workflow-and-versioning



Reference only.



It cannot change:

\- The main branch.

\- The approved repository.

\- The `part NN: description` commit format.

\- One commit per part.

\- The push script.

\- The six batch boundaries.



Skills must not create extra planning files.



\## Required per-part skill declaration



Print this before beginning each part:



Skills used: test-driven-development, source-driven-development, code-review-and-quality



Add every applicable part-specific skill to the same line.



\---



\# 19. VISUAL VERIFICATION — MANDATORY



This rule applies to:



\- PART 06.

\- PART 07.

\- PART 08.

\- PART 10.

\- PART 11.

\- PART 12.

\- PART 13.

\- PART 14.

\- PART 15.

\- PART 16.

\- PART 17.

\- PART 18.

\- PART 19.

\- PART 20.

\- PART 21.

\- PART 22.

\- PART 23.



Before running push\_part.py for any listed part:



1\. Start the application locally.

2\. Open the running application using the available browser tool.

3\. Check desktop at 1440px.

4\. Check mobile at 390px.

5\. Check Light theme at both widths.

6\. Check Dark theme at both widths.

7\. Inspect layout, clipping, readability and interactions.

8\. Fix visible problems.

9\. Repeat inspection after changes.

10\. Report any unresolved visual issue.



Required inspection matrix:



| Viewport | Theme |

|---|---|

| 1440px | Light |

| 1440px | Dark |

| 390px | Light |

| 390px | Dark |



If no browser tool is available:



\- State that browser verification was unavailable.

\- Report the missing capability.

\- STOP that part.

\- Do not run push\_part.py.

\- Do not mark the part complete.

\- Do not continue to the next part.



Never claim visual verification that did not happen.



A successful test suite does not replace browser inspection.



\---



\# 20. PART-SPECIFIC REQUIREMENTS



\## PART 01



\- Copy all 19 original backend Python files.

\- Copy all seven original Python test suites.

\- Preserve the original backend implementation.

\- Run all seven suites successfully before committing.

\- Create .env.example from the actual backend code.

\- Compare actual environment-variable names against the audit.

\- Report differences.

\- Never copy .env or secrets.



\## PART 05



Implement strict root content negotiation.



Missing Accept, \*/\*, application/json and equal JSON/HTML preference all return the original JSON health response.



Only explicitly preferred text/html returns the workspace.



\## PART 06



Implement the entire Apple-style design system.



Copy all four original assets.



Implement scripts/build\_css.py.



Do not commit downloaded binaries.



Resolve the Tailwind 4.1.14 checksum using the official-checksum-or-locally-pinned policy.



Report the result in the part summary.



\## PART 08



No user-facing mode picker.



Preserve original parallel market intelligence and deep analysis behavior.



\## PART 09



Port tests/test\_research\_error\_guidance.ts into Python.



\## PART 12



Port tests/test\_chart\_date\_formatting.ts into Python.



\## PART 15



Port tests/test\_company\_workspace\_mapping.ts into Python.



\## PART 16



Port tests/test\_news\_context\_mapping.ts into Python.



\## PART 19



Implement pure-Python Markdown and MathML rendering.



Only markdown-it-py, mdit-py-plugins dollarmath and latex2mathml for math.



Include inline and block math tests.



Do not use KaTeX or MathJax.



\## PART 20



Port tests/test\_agentos\_client\_errors.ts into Python.



\## PART 22



Apply the SSRF rule.



The server never fetches user-provided URLs.



Add explicit tests.



\## PART 27



Developer telemetry is disabled by default.



QUANTAI\_DEVTOOLS=1 enables it only in development.



Production always disables it.



\## PART 28



Inventory and verify the five completed Python regression conversions.



Do not reimplement them.



\## PART 29



Keep:



\- maxDuration: 60.

\- Cache-Control: no-store for /api/\*.

\- includeFiles with templates/\*\* and static/\*\*.



Add deployment-config tests.



Document what remains unverified without an actual Vercel deployment.



\## PART 30



Verify 21 UI features and seven infrastructure features.



Visual target is the approved Apple-style concept, not original index.css.



Complete the final functional and visual audit.



\---



\# 21. TESTING WORKFLOW FOR EVERY PART



Use this exact sequence:



1\. Inspect original source.

2\. Write or update tests first.

3\. Implement current-part code.

4\. Run focused tests.

5\. Run the entire pytest suite.

6\. If the part is in Section 19, perform the required visual inspection.

7\. Review the entire diff.

8\. Mark current part checked in migration/PROGRESS.md.

9\. Verify no protected or secret files are being staged.

10\. Run push\_part.py.



Full-suite command:



python -m pytest -q



Only the Python 3.12 standard library is used by push\_part.py itself.



Do not skip tests.



Do not weaken assertions.



Do not hide failures.



Maximum three fix attempts after an initial test failure.



If tests remain failing after three fix attempts, stop immediately.



\---



\# 22. PROGRESS AND GIT POLICY



Repository:



https://github.com/SamSurve/QuantAI.git



Branch:



main



Every part must have exactly one commit.



Commit format:



part NN: description



The current part must be checked in migration/PROGRESS.md before running the push script.



The updated PROGRESS.md must be included in that same part commit.



Only run:



python migration/push\_part.py <part\_no> "part NN: description"



Never independently run:



git add -A



git commit



git push



Never create extra checkpoint commits.



The push script validates:



\- Python 3.12.

\- Part range.

\- Correct commit message.

\- Current progress checkbox.

\- Consecutive prior part commits.

\- Exact origin URL.

\- Active branch main.

\- Configured git user.email.

\- No pre-staged changes.

\- Full pytest success.

\- Safe explicit Git staging.



It excludes:

\- .env files except .env.example.

\- Private keys.

\- Credential files.

\- tools/.

\- .venv/.

\- Python caches.

\- node\_modules.

\- Other protected paths.



It creates one commit and executes:



git push origin main



If the push fails after committing:



\- Do not retry automatically.

\- Do not create another commit.

\- Do not mark the batch as complete.

\- Report that the commit exists locally but was not confirmed as pushed.

\- Stop.



After successful push, verify the commit and progress update.



\---



\# 23. STOP CONDITIONS



Stop immediately if:



1\. A test remains failing after three fix attempts.

2\. Critical original behavior is unclear.

3\. The original API contract cannot be preserved.

4\. A critical dependency is unavailable.

5\. Required security skill cannot be located.

6\. The browser tool is unavailable for a mandatory visual verification part.

7\. The wrong Git remote is configured.

8\. The active branch is not main.

9\. A secret file is detected in planned staging.

10\. The push script fails.

11\. The part cannot meet its acceptance criteria.

12\. A skill or tool suggests changing the approved architecture.



Do not skip the affected part.



Do not merge parts.



Do not continue into dependent parts after a critical blocker.



Report the exact blocker and wait for the user.



\---



\# 24. END-OF-BATCH SUMMARY



After every five successful parts, provide:



\## Completed batch



\- Batch number.

\- Five completed part numbers.

\- One commit SHA for every part.

\- Push confirmation for every commit.

\- Focused tests.

\- Full pytest result.

\- Visual verification results for applicable parts.

\- Progress checklist status.



\## Changes made



Summarize the actual features delivered.



\## Issues



List unresolved defects or state that none were identified.



\## Known limitations



Report actual limitations honestly.



\## Next batch



Identify the next batch and its five part numbers.



Then print:



BATCH COMPLETE, STOP



At Parts 10, 20 and 30, also print:



DAY COMPLETE



After Part 30, report final parity status.



Wait for the user before beginning another batch.



\---



\# FINAL NON-NEGOTIABLE RULE



Do not optimize away original behavior.



Do not replace full functionality with placeholders.



Do not trade correctness for speed.



The required outcome is the original QuantAI financial research product, implemented in Python, using the approved Apple-style visual design, with all original financial logic and user-facing functionality preserved.



