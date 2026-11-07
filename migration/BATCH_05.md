# BATCH_05 — COMPLETE EXECUTOR INSTRUCTIONS
## QuantAI Python Migration — Parts 21–25

**Repository:** `E:\QuantAI-Python`  
**Original source (READ-ONLY):** `E:\Quant-AI`  
**Design concept (READ-ONLY):** `E:\QuantAI-design\Main.dc.html`  
**Branch:** `main`  
**Remote:** `https://github.com/SamSurve/QuantAI.git`  
**Python:** 3.12.7  
**Virtual environment:** `E:\QuantAI-Python\.venv`  
**Shell:** Windows PowerShell

## OWNER-APPROVED BATCH 05 DECISIONS — OVERRIDE PRIOR CONFLICTING WORDING

These explicit owner decisions supersede any earlier conflicting wording in this batch or other project instructions for BATCH_05:

1. **Design concept:** Use only `E:\QuantAI-design\Main.dc.html`. No alternate concept path is approved.
2. **Protected-test baseline:** The baseline is the exact content of `tests/test_production_readiness.py` and `tests/test_provider_failover.py` at commit `2862d10`. Compare current/final files to that commit snapshot. `test_production_readiness.py` legitimately differs from the original `E:\Quant-AI` repository; do not use the original repository as its baseline.
3. **Automatic progression:** Once BATCH_05 execution is owner-authorized and Part 21 is successfully pushed, continue Parts 22, 23, 24 and 25 automatically without asking for per-part authorization. Stop only on a blocker or after Part 25. Do not start Part 26.
4. **Git policy:** Read-only Git commands are allowed. All mutating Git operations are allowed only through `migration/push_part.py`.
5. **No further forensics/helper scripts:** Do not repeat the completed Part 20 forensic investigation, create helper scripts in the repository, or perform unrelated forensic work. Use already-reconciled evidence. Keep all reports compact while retaining required evidence.

These decisions do not waive any acceptance criterion, test, security control, browser requirement, review, progress update or push verification.

---

# GATE REPORT — BATCH_05 SELF-REVIEW BEFORE EXECUTION

<badge>PASS — READY AFTER LOCAL PLAN APPEND IS VERIFIED</badge>

| Gate | Result | Evidence in this file |
|---|---|---|
| 1. Acceptance criteria copied one by one | PASS | Parts 21–25 reproduce every owner-provided Step D acceptance criterion and test item individually, verbatim. Additional owner corrections are separately labelled. |
| 2. Original paths verified or marked ASSUMPTION | PASS | Original source paths are grounded in `AUDIT.md`; `client/src/pages/Home.tsx` is used instead of a root-level `Home.tsx`. The two Part 22 template-directory normalizations are explicitly marked as assumptions to verify before creation. |
| 3. Per-part files, dependencies, tests and push commands | PASS | Every part lists exact original read paths, create/update targets, dependencies, validation commands and the exact `push_part.py` command. |
| 4. Reuse before create | PASS | Part 21 reuses Part 20 chat modules. Parts 24–25 require tests first and prohibit backend rewrites when existing behavior passes. |
| 5. Dependencies | PASS | No unapproved package additions. Any dependency proposal requires owner approval, a pinned version, official source, age proof (at least 14 days), and an install check. |
| 6. Original backend/tests protected | PASS | Original baseline suites are immutable; hashes, full diffs, and reasons are required for any justified backend change. |
| 7. Fake data and design numbers | PASS | Fixtures use clearly fake identifiers/values; concept/sample values are forbidden in production and tests. |
| 8. SSRF and secrets | PASS | Parts 22 and 24 include explicit SSRF, input validation, secrets, server-only diagnostics and no-raw-exception rules; global rules forbid server-side user-URL fetching. |
| 9. Browser measurements and network evidence | PASS | UI-affecting parts require real `getComputedStyle()` measurements on concept and app, separately at 1440 Light/Dark and 390 Light/Dark, plus before/after interaction request counts. |
| 10. Fixed final report | PASS | Sections A–F are defined with required contents; omission of any section makes the report incomplete. |

**Pre-execution condition:** Before Part 21, verify that the approved Part 21–25 addendum has been appended to `migration/MIGRATION_PLAN.md` and that its criteria match this file exactly. Do not begin if the local authority file and this batch differ.

---

# 1. OBJECTIVE AND BATCH BOUNDARY

Execute Parts 21, 22, 23, 24 and 25 in order. Complete the approved chat continuity, activity/connection settings, responsive UI resilience, API security verification, TTL cache verification and provider failover verification.

This is an implementation and verification task. Do not create a new architecture or reimplement working backend behavior. Preserve the original TypeScript application's semantics, existing backend contracts, factual data behavior, security boundaries and previous-part functionality.

**This batch contains exactly five parts: 21–25.** Do not start Part 26 or BATCH_06.

# 2. AUTHORITY AND EXECUTION PROCESS

Authority order:

1. `migration/MIGRATION_PLAN.md` — canonical acceptance criteria.
2. `migration/MASTER_PROMPT.md` — global project constraints.
3. `migration/PROGRESS.md` — actual completion state.
4. This `BATCH_05.md` — execution instructions mirroring the canonical criteria and adding owner-approved evidence/safety requirements.

The canonical migration plan governs feature acceptance criteria, except where the explicit owner-approved Batch 05 decisions above directly override earlier conflicting operating instructions. Do not silently reconcile any other conflict; stop and report it.

Use this process for each part:

**Think → Plan → Build → Review → Test → Ship → Reflect.**

- Think: inspect current state and requirements. Ask no more than five questions only when a decision truly cannot be made from the repository and authority files. Do not repeat questions already answered.
- Plan: identify minimal files and dependencies. List unverified paths as `ASSUMPTION` before implementation.
- Build: write tests first, prove they fail for the intended reason, then make the smallest required change.
- Review: self-review the entire diff and exact proposed part file set.
- Test: run focused tests, protected baseline tests, the full suite and Ruff.
- Ship: invoke only `migration/push_part.py` using the exact command listed for the part.
- Reflect: after Part 25, include an end-of-batch retrospective in the final report: what went wrong, what was corrected, and what permanent rule should be added. Do not create a separate retrospective file.

# 3. GLOBAL RULES — NON-NEGOTIABLE

1. **No third-party skills.** Do not use or install skills. Do not add a skills declaration section or skill-usage line to reports. Follow the plain engineering rules in this file.
2. **Tests first.** Add focused tests before production changes. Prove each new test detects the intended behavior. Never edit an existing assertion to make a test pass.
3. **Official documentation.** Verify FastAPI, Starlette, HTTPX, browser APIs, Python, pytest, and other framework/library behavior against official documentation. Do not guess API semantics.
4. **Reuse before create.** Inspect existing project files and reuse working code, macros, routes and tests. Do not rebuild features already delivered by Parts 01–20.
5. **Dependencies.** Do not install or add unapproved packages. If a package seems necessary, stop and request owner approval. The proposal must include exact pinned version, official package/release URL, publication/release date proving it is at least 14 days old, and an install/import verification command. No package is approved by this batch.
6. **Original repo.** `E:\Quant-AI` is read-only. Never edit, format, rename, delete or commit anything from it.
7. **Original test protection.** `tests/test_production_readiness.py` and `tests/test_provider_failover.py` are protected baseline suites. Never overwrite, edit, delete, skip, weaken or relax them. Preserve every other original baseline test. Their authoritative baseline is the exact file content at commit `2862d10`. Use read-only Git inspection to obtain each file from that commit and record its SHA-256; compare the working files before execution and after BATCH_05 against those baseline hashes. Do not compare `test_production_readiness.py` against `E:\Quant-AI`; its difference from the original repository is an accepted prior migration change.
8. **Backend preservation.** Original backend modules copied into `E:\QuantAI-Python` remain protected. Modify one only when a new test demonstrates a concrete defect or a canonical plan criterion cannot otherwise be met. Make the smallest fix and report the complete diff, reason, plan criterion and contract impact in Section E.
9. **Fixtures.** Use clearly fake fixtures such as `Testco`, `TST`, and `100.00`. Never put sample market values from `Main.dc.html`, screenshots, concept mockups or earlier reports into production code or test fixtures.
10. **Secrets.** Never print, expose, log or commit API keys, tokens, credentials, cookies, `.env` values or secret-bearing payloads. Provider secrets must remain server-side.
11. **Public errors.** Never expose raw exceptions, stack traces, local filesystem paths, prompts or secret-bearing diagnostics to clients. Log controlled diagnostic details server-side and return normalized safe public errors.
12. **SSRF/network boundary.** Server-side code must never fetch user-supplied URLs. Never use a URL from browser localStorage in Python, HTTPX or another server-side client. Never introduce a server-side URL proxy or self-HTTP hop. Research routes call the orchestrator in-process.
13. **Input validation.** Validate and bound untrusted input, content types, headers and payload sizes. Do not trust arbitrary forwarded-IP headers; follow only the existing explicitly trusted-proxy policy.
14. **Fix attempts.** Allow at most three focused fix attempts for a test or implementation failure. If unresolved, stop and report. Never weaken tests or continue to the next part with a known failure.
15. **No extra docs.** Do not create issues, tickets, PRs, specs, plans or additional report files. Update only files specified by the canonical plan and this batch, plus existing `migration/PROGRESS.md`.
16. **Git operations.** Read-only Git commands are allowed for inspection only, including `git status`, `git diff`, `git diff --cached`, `git show`, `git log`, `git rev-parse`, `git branch` and `git remote -v`. Do not use GitHub connectors, IDE Git integration or other alternate Git interfaces. All mutating Git operations—including staging, commits and pushes—must be performed only through `migration/push_part.py`. Never run direct `git add`, `git commit`, `git push`, `git reset`, `git checkout`, `git clean`, `git stash`, `git rebase`, `git merge` or other mutating Git commands. If the wrapper cannot prove file isolation, push success or remote state, stop and report the limitation.
17. **Sequential batch progression.** Execute one part at a time. Each part must pass its tests, review, required browser checks and progress update, then be pushed through `push_part.py` before starting the next. Once BATCH_05 has been owner-authorized and Part 21 is successfully pushed, continue Parts 22–25 automatically without asking for owner authorization between parts. Stop only if a part encounters a blocker/stop condition or after Part 25. Do not start Part 26.
18. **Exactly one commit per part.** Use only the exact `push_part.py` command shown in the relevant part. No extra checkpoint commits.
19. **No helper scripts or further forensics.** Do not create helper scripts in the repository or elsewhere for this batch. Do not repeat the completed Part 20 forensic investigation or perform unrelated forensic work. Use the already-reconciled Part 20 API audit evidence; report any genuinely missing item as `UNVERIFIED` rather than investigating again.
20. **Compact reports.** Keep gate, progress and completion reports concise, preferably tables/bullets. Include every required result and evidence reference, but do not repeat background narrative or create extra reports.

# 4. REQUIRED SOURCE AND BASELINE PREFLIGHT

Before Part 21:

1. Read `migration/MIGRATION_PLAN.md`, `migration/MASTER_PROMPT.md`, `migration/PROGRESS.md`, and `AUDIT.md` to confirm current plan and preceding-part state.
2. Verify every original source path below against `AUDIT.md` and the read-only source. The exact Home page path is `client/src/pages/Home.tsx`.
3. Use read-only Git inspection to obtain the exact contents of both protected files at commit `2862d10`; calculate and record their baseline SHA-256 values. These commit snapshots—not the original `E:\Quant-AI` repository—are authoritative.
4. Confirm the current protected files match the `2862d10` baseline before execution. If either differs, stop and report; do not repair it. In particular, the accepted prior difference in `test_production_readiness.py` versus `E:\Quant-AI` is not a failure.
5. Inspect `migration/push_part.py` and its supported behavior. Confirm it can isolate the current part's file set, test the staged/exported change set where supported, commit once, push and report remote verification. If it cannot isolate uncommitted work or prove remote success, stop.
6. Confirm branch `main` and the expected remote. Read-only Git commands may be used for this inspection. If branch or remote does not match, stop and report it.

# 5. VERIFIED ORIGINAL PATHS AND ASSUMPTIONS

The following original source paths are present in the supplied `AUDIT.md` inventory:

- `client/src/components/ChatPanel.tsx`
- `client/src/lib/agentos.ts`
- `client/src/pages/Home.tsx`
- `client/src/const.ts`
- `client/src/App.tsx`
- `client/src/pages/NotFound.tsx`
- `client/src/components/StartupReveal.tsx`
- `client/src/components/ErrorBoundary.tsx`
- `client/src/hooks/useMobile.tsx`
- `client/src/components/BrandMark.tsx`
- `client/src/components/AnalysisPanel.tsx`
- `client/src/lib/research.ts`
- `api/index.py`
- `api/research_protection.py`
- `api/research_errors.py`
- `api/research_logging.py`
- `api/research_cache.py`
- `api/ai_providers.py`
- `api/research_orchestrator.py`
- `api/market_intelligence_services.py`

Do not use a root-level `Home.tsx` path. The audited path is `client/src/pages/Home.tsx`.

**ASSUMPTION to verify before creating:** The owner-provided Step D groups `connection_health.html` and `endpoint_settings.html` after `templates/partials/recent_activity.html`. This batch normalizes them to `templates/partials/connection_health.html` and `templates/partials/endpoint_settings.html`. Confirm the existing template convention; if contradicted, stop rather than silently changing the target paths.

All implementation/test paths in the part sections are migration-repository targets. Inspect for an existing implementation before creating them.

## Cross-part execution and protection rules — Parts 21–25

1. Inspect and reuse the implementation from earlier parts before creating or rebuilding anything. In particular, Part 21 must extend the chat files already introduced in Part 20; Part 24 and Part 25 are primarily verification of existing backend behavior.
2. Write focused tests before implementation. Demonstrate that each new test detects the intended behavior before changing production code.
3. Verify FastAPI, Starlette, HTTPX, browser, Python, pytest, and other framework/library usage against their official documentation. Do not guess API behavior.
4. Do not use or install third-party skills. Do not add a skills declaration section or skill-usage line to reports.
5. Do not use the built-in permissioned-GitHub skill, GitHub connectors or IDE Git integration. Read-only Git CLI commands are permitted for inspection. All mutating Git operations must use `migration/push_part.py` with the exact PowerShell command for the current part. If the script cannot complete or report required verification, stop; do not use another mutating Git interface as a workaround.
6. Do not use slash commands such as `/spec`, `/plan`, `/build`, `/ship`, or `/land-and-deploy`. Do not create issues, tickets, pull requests, specs, or additional planning/report documents. Only update the existing `migration/PROGRESS.md` and the files explicitly listed in the migration plan, in addition to part-specific implementation and test files.
7. The original repository `E:\Quant-AI` is read-only. Do not modify it. Preserve original backend behavior, API contracts, and original test assertions in the Python migration.
8. `tests/test_production_readiness.py` and `tests/test_provider_failover.py` are protected baseline suites. Never overwrite, edit, delete, skip, weaken or relax either file. Preserve every other original baseline test. The baseline is their exact content at commit `2862d10`; record SHA-256 values from those commit snapshots and compare the working files before and after BATCH_05. Do not compare `test_production_readiness.py` with the original `E:\Quant-AI` file; its prior migration difference is accepted.
9. New test fixtures must use unmistakably fake data, such as `Testco`, `TST`, and `100.00`. Never use sample values from `Main.dc.html`, screenshots, mockups, or prior visual reports as production values or test fixtures.
10. Do not add a package unless the owner explicitly approves it. If a dependency appears necessary, stop and report its exact name, pinned version, official package/release URL, and publication/release date proving it is at least 14 days old; include the proposed install/import check. Do not install it without approval. No unapproved package may be added to a requirements file or lock file.
11. Never print, expose, log, or commit API keys, credentials, tokens, `.env` values, cookies, or secret-bearing payloads. Keep provider secrets server-side.
12. Never return raw Python exceptions, traceback text, internal file paths, prompt templates, credentials, or secret-bearing diagnostics to browser clients. Capture diagnostics server-side and return normalized public errors.
13. No server-side code may fetch a user-supplied URL. Do not create URL proxies, self-HTTP requests, or server-side hops through the configured AgentOS URL. Research routes must call the research orchestrator in-process.
14. Security-sensitive inputs must be explicitly validated and bounded. Reject malformed or oversized requests safely. Resolve client IPs only through a correctly configured trusted-proxy policy; do not blindly trust arbitrary `X-Forwarded-For` values.
15. Before each part's push, inspect the complete proposed part change set and its staged export using `push_part.py`'s supported mechanisms. Read-only Git commands may be used to independently inspect the working tree and diffs. Confirm the staged/exported set contains only that part's authorized files. If isolation cannot be proven, stop.
16. A part is complete only after its tests pass, review passes, required browser checks pass, `PROGRESS.md` is updated, and `push_part.py` reports a successful push and required remote verification.

### Mandatory browser evidence for every UI-affecting part

1. Use a real browser to inspect only the approved concept at `E:\QuantAI-design\Main.dc.html` and the running Python application separately. No alternate concept path is approved.
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
5. Use the already-completed Part 20 `api/index.py` audit in the existing incident/evidence reports. Do not repeat the forensic commit/source investigation or create helper scripts. Preserve the documented findings: root `/` behavior changed, the API 404 JSON payload changed, and the added web/chat/static routes are additive. Clearly distinguish unchanged successful API endpoint behavior from changed root/404 behavior. Do not modify `api/index.py`.
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
12. `tests/test_production_readiness.py` is a protected baseline suite and must remain unchanged from its exact content at commit `2862d10`. Record and compare its SHA-256 against that commit snapshot; do not compare it to the original `E:\Quant-AI` file.

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
2. Verify the final contents of `tests/test_production_readiness.py` and `tests/test_provider_failover.py` match their authoritative snapshots at commit `2862d10` by SHA-256. Do not compare `test_production_readiness.py` against `E:\Quant-AI`.
3. Verify all five part pushes succeeded through `migration/push_part.py` and each part has one part-specific commit.
4. Complete the six-section final report required by `BATCH_05.md`.
5. Write the end-of-batch retrospective in that final report: what went wrong, what was corrected, and which permanent rule should be added. Do not create a separate retrospective document.
6. Stop. Do not start Part 26 or BATCH_06.

# 7. MANDATORY FINAL REPORT — EXACT A–F FORMAT

A report missing any section A, B, C, D, E or F is incomplete and must be rejected. Do not omit a section because no code change was needed. State `No change`, `Not applicable`, `Not verified`, or the evidence-backed result explicitly.

## A. PART RESULTS — FILES, TESTS, SHA, PUSH

Provide one row per part:

| Part | Exact plan title | Files created/changed | Focused tests (collected/passed/failed) | Full-suite result after part | Commit SHA reported by push_part.py | Push/remote result |
|---|---|---|---|---|---|---|
| 21 | Chat continuity and quick prompts | ... | ... | ... | ... | ... |
| 22 | Activity, connection settings and SSRF protection | ... | ... | ... | ... | ... |
| 23 | Startup, responsive application and error recovery | ... | ... | ... | ... | ... |
| 24 | API security and request protection | ... | ... | ... | ... | ... |
| 25 | TTL cache and provider failover | ... | ... | ... | ... | ... |

For every part, include its acceptance criteria one by one with PASS/FAIL/NOT RUN and cite actual tests or browser observations. List all files changed and created; do not write `all relevant files` or omit paths. State the exact commit SHA returned by `push_part.py` and whether remote verification succeeded. Do not invent SHA values.

Part 21 must additionally include:

- The exact original quick-prompt strings read from `client/src/components/ChatPanel.tsx`, in source order.
- The correction from the three incorrect Part 20 labels to the original strings.
- The quick-prompt regression test result.
- Message 1 exact text and observed response/result.
- Message 2 exact text and observed response/result.
- Session ID after each message and explicit equality comparison.
- Initial turn counter, after-message-1 counter and after-message-2 counter.
- Browser request count before message 1, after message 1 and after message 2.
- AgentOS request count and `/api/chat/render` count separately; unexpected requests explicitly listed or zero.
- Real browser Network evidence. Source inspection or direct Python calls are not proof of two-message continuity.

Part 21 must also include a compact summary of the already-completed Part 20 `api/index.py` audit (use the reconciled incident/evidence report; do not repeat the forensic investigation):

- Exact Part 20 changes to `api/index.py`, including imports, middleware, app configuration, route/router registration, request handling, responses/statuses and error handling.
- State the already-established comparison findings against the parent version and original `E:\Quant-AI\api\index.py`.
- Explicit conclusion on whether any original backend contract changed, supported by tests.
- Do not perform another commit-diff investigation. Use the already-reconciled findings; mark any detail not supported by that evidence `UNVERIFIED`.

Part 21 news regression must include:

- The same headline, two different publishers, two different URLs.
- Result before any production code change.
- Both article-presence assertions.
- Whether production code was changed; change it only if the test fails.

Part 22 must include:

- Browser-only endpoint key audit for `analysts-ledger-agentos-url`.
- Evidence that health/chat browser code can use that configured endpoint.
- Evidence that Python research routes call the orchestrator in-process.
- Evidence of zero HTTPX/other server outbound requests to a supplied host.
- All listed SSRF cases and results, including controlled DNS-rebinding coverage.

Part 24 and Part 25 must explicitly say whether the backend was unchanged because existing behavior passed, or list the exact backend diffs and the failing tests that justified each one.

## B. FEATURE CHECKS

Provide a feature-level matrix covering every Part 21–25 criterion and every owner-approved additional requirement.

| Part | Feature/criterion | Verification method | Observed evidence | Result |
|---|---|---|---|---|

At minimum include:

- Chat turns, ordered history, session reuse, turn counter, exact quick prompts, loading/error states.
- Recent activity five-item cap, labels, modes, completion/confidence.
- Ready/Checking/Offline statuses, refresh/re-check and endpoint settings persistence.
- Browser-only custom AgentOS URL; no server fetch; in-process research; no self-HTTP.
- Startup timing, reduced motion, error recovery, reload, 404, anchor IDs, keyboard dialogs, focus, toasts, error layout resilience.
- 8,192-byte body limits, 10-per-60-second rate limit, four-way concurrency, sliding-window reset, request IDs, server-only diagnostics, public error sanitization, no-store, trusted forwarded IP and browser secret absence.
- Each exact cache TTL, cache hit/miss/expiry, provider order/configuration, sequential fallback, cooldown, AI-unavailable non-blocking behavior and original failover suite.

Do not say a feature is verified merely because the code contains a corresponding function. Give the executed test or actual browser observation.

## C. VISUAL EVIDENCE

For every UI-affecting part, provide actual browser evidence for all four configurations, separately:

1. 1440px Light.
2. 1440px Dark.
3. 390px Light.
4. 390px Dark.

Measure the concept page and Python application separately with browser `getComputedStyle()`. Do not copy the Concept column from CSS source, inline declarations, screenshots, or prior reports.

Use this exact table shape for relevant components:

| Property | Concept — browser getComputedStyle() + selector | App 1440 Light | App 1440 Dark | App 390 Light | App 390 Dark |
|---|---|---|---|---|---|
| [property] | [actual concept computed value] | [actual app computed value] | [actual app computed value] | [actual app computed value] | [actual app computed value] |

Provide at least two meaningful style measurements for each relevant UI component. Include the element/selector and actual measured values. Keep 390px Light and 390px Dark separate.

For a drawer/dialog with no corresponding concept component, state exactly: `No concept equivalent — no direct concept measurement is available.` Do not invent a selector or compare it with an unrelated concept element. Report app-only measured values separately.

For each actual interaction, include:

- Interaction and configuration.
- Browser request count before.
- Browser request count after.
- Delta and request categories/paths.
- Expected request behavior and whether the observation matched it.

Include screenshot/evidence references and browser console outcome. State any clipping, overflow, focus, keyboard or layout issue. If browser verification was impossible, the part is not complete and must not have been pushed.

## D. REGRESSION INTEGRITY

This section is mandatory. Include:

1. Number of tests collected, passed, failed, skipped and deselected for each focused run and the full suite. Do not confuse script-style checks with pytest-collected tests; original verify/check suites must be run through their established wrapper where pytest does not collect them directly.
2. Full baseline and final full-suite counts, duration and warnings.
3. Results for all seven original Python regression suites, with each filename and PASS/FAIL.
4. Results for all five converted TypeScript regression cases, with each filename and PASS/FAIL.
5. Results for `tests/test_production_readiness.py` and `tests/test_provider_failover.py` specifically.
6. Whether any original test file was edited. Expected answer: NO.
7. Whether any original assertion changed, test was skipped, excluded, weakened, relaxed, replaced or deleted. Expected answer: NO.
8. Baseline and final SHA-256 for `tests/test_production_readiness.py` and `tests/test_provider_failover.py`; explicitly confirm equality.
9. Any failure and fix, including the exact file/test and number of attempts.
10. Any pre-existing discrepancy, reported separately from batch-created changes.

A passing test count is not sufficient if original tests were modified. If either protected file hash differs, report BATCH_05 as noncompliant.

## E. ORIGINAL BACKEND FILES CHANGED AND WHY

This section is mandatory. List every original backend source file changed during BATCH_05. Distinguish original backend modules from new `api/web` modules, templates, JavaScript and tests.

| Original backend file | Changed in BATCH_05? | Exact diff | Why change was necessary | Plan criterion | API/backend contract impact | Test evidence |
|---|---|---|---|---|---|---|

Include `api/index.py`, `api/research_protection.py`, `api/research_errors.py`, `api/research_logging.py`, `api/research_cache.py`, `api/ai_providers.py`, `api/research_orchestrator.py`, and `api/market_intelligence_services.py` if changed. Do not omit a modified original module.

If no original backend source file changed during BATCH_05, state exactly: `No original backend source files were modified in BATCH_05.`

Still include the compact, already-reconciled Part 20 `api/index.py` audit summary under Section A. Explicitly disclose the known root `/` and API 404 response changes; do not claim complete API parity.

## F. GIT VERIFICATION

This section is mandatory. Read-only Git commands may be used to inspect branch, remote, status, diffs and commit history. All mutating Git operations must use `migration/push_part.py`. Do not use GitHub connectors, skills or IDE Git integration.

Report:

- Current branch is `main`.
- Remote is `https://github.com/SamSurve/QuantAI.git`.
- Exactly five new BATCH_05 commits exist, one per part.
- Each commit message follows `part NN: ...`.
- Each push was invoked using `migration/push_part.py`.
- Every expected commit is confirmed on `origin/main` by the wrapper's remote verification.
- Local `main` and `origin/main` are synchronized, using wrapper push/remote evidence and permitted read-only inspection.
- Working tree is clean, verified with permitted read-only inspection.
- No untracked or unexpected files remain.
- No `.env`, secrets, virtual environment, browser profile, scratch server, sample data, binary or concept/runtime file was committed.
- The wrapper's staged/exported part-file set contained only authorized files for that part.

If `push_part.py` cannot report a mutation/push result, write `NOT VERIFIED — push_part.py did not provide this evidence` and stop. Read-only Git commands may verify local branch, remote, status, diffs and history; do not use GitHub API/connectors or IDE integrations.

**Batch retrospective (include as the final subsection of F):**

- What went wrong during BATCH_05.
- What was corrected and how verified.
- The permanent rule(s) that should be added to prevent recurrence.
- Any unresolved risks or evidence gaps.

# 8. STOP CONDITIONS

Stop the affected part and report the exact blocker if:

- The local `MIGRATION_PLAN.md` has not been updated with the approved Part 21–25 sections or criteria differ from this batch.
- A criterion conflicts with the existing repository or another authority file, except for the five explicit owner-approved Batch 05 overrides at the top of this document.
- An original source path cannot be verified.
- A required test, dependency or browser capability is unavailable.
- A security boundary is unclear or a server-side arbitrary URL fetch would be required.
- A breaking API contract change is necessary.
- A test fails after three focused fix attempts.
- A protected original test changes or its hash changes.
- Visual evidence cannot be captured for a UI-affecting part.
- The push script cannot isolate the part, verify the commit, push or confirm the remote state.

Do not mark an incomplete part complete. If any stop condition occurs, halt the batch and report the blocker. Otherwise, after a successful Part 21 push, automatically proceed through Parts 22–25 without a per-part owner-authorization pause.

# 9. FINAL BATCH BOUNDARY

After Part 25:

1. Run the final full test suite and Ruff.
2. Recheck both protected test files against their authoritative commit `2862d10` SHA-256 baselines. `test_production_readiness.py` may legitimately differ from the original `E:\Quant-AI` repository.
3. Ensure Parts 21–25 each have exactly one successful `push_part.py` push.
4. Complete Sections A–F, including the retrospective.
5. State clearly `BATCH_05 COMPLETE` only if all required evidence exists; otherwise state `BATCH_05 BLOCKED` and list blockers.
6. Stop. Do not start Part 26 or BATCH_06.

**BATCH_05 COMPLETE, STOP**
