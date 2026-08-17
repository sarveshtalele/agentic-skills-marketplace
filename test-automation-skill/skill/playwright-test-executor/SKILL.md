---
name: playwright-test-executor
version: 1.0.0
description: >
  Executes Playwright test suites, parses test results and failure logs, and explains failures
  in plain language with actionable fixes. Use when a Playwright test run fails, when triaging
  flaky or failing UI tests, or when interpreting Playwright HTML reports and traces. For writing
  new test scripts, use playwright-test-generator instead.
author: AI CoE
tags: [playwright, testing, execution, triage]
---

# Skill: Playwright Test Execution & Failure Explanation

## Purpose
Execute Playwright tests, read test results and failure logs, explain failures in simple, human-readable language, and suggest likely fixes.

## Workflow (Execute-Analyze-Explain)

### 1. Execution
- **Trigger Tests**: Use MCP to run the Playwright test suites (e.g., `npx playwright test`).
- **Default Input Source**: When the user asks to execute a test, automatically look for the requested script in `test-data/inputs/playwright-test-executor/` unless the user explicitly provides another path.
- **Do Not Use Generator Output by Default**: Do not read from `test-data/outputs/playwright-test-generator/` unless the user explicitly asks to execute a generated script from there.
- **Default Output Destination**: Save execution logs, failure analysis, and reports to `test-data/outputs/playwright-test-executor/` without requiring the user to mention the folder.
- **Fast Failure Mode**: For failing scenarios, prefer the shortest practical timeout and avoid extra waits so the command returns quickly.
- **Report Handling**: After execution, open the Playwright HTML report from the output folder in the browser when possible.
- **Fresh Report View**: If the browser is still showing an older scenario, reload the report or open the latest report URL before responding.
- **Report Regeneration**: The HTML report reflects the most recently generated Playwright run. If the browser keeps showing an older run, rerun the target scenario with the HTML reporter so the report folder is regenerated before opening it.

### 2. Analysis
- **Fetch Logs**: Use MCP to read the generated test logs, standard error, and Playwright HTML/JSON reports.
- **Differentiate Failure Types**:
  - *Locator Issue*: Element not found or strict mode violation.
  - *Wait Issue*: Timeout exceeded while waiting for element or condition.
  - *Assertion Mismatch*: Expected value does not match the actual value.
  - *Network/Environment Issue*: API failures, page crash, etc.

### 3. Summary Output
- **Always Save a Short Summary**: Write a concise execution summary for every run, even when all tests pass.
- **Pass Summary**: Include the test name, pass/fail count, and a one-line success note.
- **Fail Summary**: Include the test name, failure count, plain-English failure reason, and suggested fix.
- **Save Location**: Store each scenario summary in its own file under `test-data/outputs/playwright-test-executor/` using a scenario-specific name such as `scenario-1-ecommerce.md` or `scenario-2-failing.md`.
- **Do Not Overwrite**: Never reuse a single shared summary file for multiple scenarios.
- **Report Selection**: When opening the Playwright HTML report, navigate to the report for the most recently executed scenario and verify the visible test name matches that scenario before responding.
- **If Report Is Stale**: State clearly that the report is stale and must be regenerated from the latest scenario run; do not claim the browser changed when it did not.

### 4. Explanation & Suggestion
- **Failure Summary**: Provide a clear, non-technical summary of what broke.
- **AI-Generated Explanation**: Explain the "why" behind the failure in human-readable language.
- **Suggested Fix**: Provide textual guidance on how to fix the issue (e.g., updating a locator, fixing test data, adjusting a wait state).

## 🛠️ Resources & Tools
- **MCP Configuration**: `scripts/mcp.json` - Use this to trigger execution and fetch results.
- **Input Datasets**: `test-data/inputs/playwright-test-executor/`
- **Execution Output**: `test-data/outputs/playwright-test-executor/`

## User Prompt Guidance
- If the user says "execute the script" or similar, infer the input from `test-data/inputs/playwright-test-executor/` and write all outputs to `test-data/outputs/playwright-test-executor/`.
- The user does not need to specify file or folder locations unless they want a non-default script.
- If the user asks for speed, keep the run focused on the single requested scenario and avoid any extra validation steps beyond the report save and open.

## ⚠️ Gotchas
- **Timeouts**: Distinguish between an element that never appeared and an element that appeared too late.
- **Flaky Tests**: Consider if the failure is deterministic or flaky before suggesting a definitive fix.
