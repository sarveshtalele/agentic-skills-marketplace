---
name: playwright-test-generator
version: 1.0.0
description: >
  Generates robust, production-ready Playwright end-to-end test scripts from requirements,
  acceptance criteria, manual test cases, or user journeys using data-test selectors and Page
  Object Model patterns. Use when automated UI tests need to be written or scaffolded from a
  test design. For running tests and diagnosing failures, use playwright-test-executor instead.
author: AI CoE
tags: [playwright, testing, automation, generation]
---

# Skill: AI-Assisted Playwright Test Script Generator

## Purpose
Convert plain English test steps, acceptance criteria, or manual test cases into high-quality, resilient Playwright automation scripts (.spec.ts).

## Workflow (Plan-Execute-Validate)

### 1. Planning & Context Gathering
- **Identify Target**: Confirm the URL and the core user journey.
- **Peek at Page**: If possible, inspect the page HTML to find the most robust locators (prioritize `data-test` or `id`).
- **Handle Ambiguity**: If a step is vague (e.g., "Login"), assume standard fields but mark them for verification.

### 2. Implementation Rules
- **Selector Hierarchy (The Default)**:
    1.  `page.locator('[data-test="..."]')` (Best)
    2.  `page.getByRole()` or `page.getByLabel()` (Good, but check for technical linkage in HTML)
    3.  `page.getByPlaceholder()`
    4.  `page.locator('input[type="..."]')` (Fallback for unlinked labels)
- **Wait Management**: Use auto-waiting; never use `waitForTimeout`.
- **Assertions**: 
    - Use web-first assertions (e.g., `expect(locator).toBeVisible()`).
    - **Case Sensitivity**: For text-based assertions like `toContainText`, always use `{ ignoreCase: true }` unless specific casing is a requirement. This ensures resilience against minor UI text changes.

### 3. Validation Checklist
Before outputting the script, verify:
- [ ] Are all locators specific enough to avoid **Strict Mode Violations** (e.g., "Male" vs "FeMale")?
- [ ] Does the script handle the full flow from `goto` to the final assertion?
- [ ] Is the code clean, commented, and following the Page Object Model (if requested)?

## 🛠️ Resources & Tools
- **MCP Configuration**: `scripts/mcp.json` - Use this to initialize the Playwright MCP server for browser-based context gathering.
- **Input Datasets**: `test-data/inputs/playwright-test-generator/` - Reference these for standard testing scenarios.
- **Execution Output**: All generated scripts should be saved to the project root's `test-data/outputs/playwright-test-generator/` directory.
- **Templates**: `assets/templates.md` - Use these as base structures for generated scripts.
- **Reference Material**: `references/` - Contains testing guides and presentation materials.

## ⚠️ Gotchas
- **Strict Mode**: `getByRole('radio', { name: 'Male' })` will fail if "FeMale" is also present. **Always use `{ exact: true }` for short text matches.**
- **Unlinked Labels**: Some sites (e.g., registration forms) have labels that aren't linked to inputs via `for` attributes. If `getByLabel` fails, fall back to `page.locator('input[value="..."]')`, `type`, `name`, or `id`. Always verify locator count before clicking/checking.
- **Shadow DOM**: Standard locators might fail inside Shadow roots; use deep combinators if necessary.

## 🧪 Testing Scenarios

### Positive Scenario: Standard User Journey
**Goal**: Verify a successful linear flow (e.g., login and navigate to a dashboard).
**Expected Behavior**: Agent generates a script using robust selectors and web-first assertions.
**Success Criteria**: The script runs and passes on the first try.

### Negative Scenario: Form Validation
**Goal**: Verify handling of invalid inputs and error messages.
**Expected Behavior**: Agent generates steps to input invalid data and asserts that specific error messages become visible.
**Success Criteria**: The test accurately validates the error handling logic.

### Negative Scenario: Robustness against Ambiguity
**Goal**: Handle pages with multiple similar elements.
**Expected Behavior**: Agent uses specific parent locators or unique attributes (like `id` or `data-test`) to target the correct element among duplicates.
**Success Criteria**: The script avoids strict mode violations and clicks the intended target.
