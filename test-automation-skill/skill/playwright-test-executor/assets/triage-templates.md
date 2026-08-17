# Playwright Triage Templates

Use these templates to ensure consistency in failure analysis and reporting.

## 1. Execution Summary Template
Use this to provide a high-level overview of a test run.

```markdown
# Test Execution Summary: [Date/Time]

- **Total Tests**: [Number]
- **Passed**: [Number]
- **Failed**: [Number]
- **Duration**: [e.g., 45s]

## Failing Scenarios
1. [Test Name] - [Short Reason]
```

## 2. Failure Analysis Template
Use this for detailed reporting of individual test failures.

```markdown
# Failure Analysis: [Test File Name]

## 1. Failure Summary
- **Test Case**: [Name]
- **Error Type**: [e.g., TimeoutError, AssertionError]
- **Line Number**: [Line number from stack trace]
- **Snippet**: `[The failing line of code]`

## 2. AI-Generated Explanation
[A human-readable explanation of why the test failed, explaining the gap between expected and actual behavior.]

## 3. Suggested Fix
[Specific code changes or environment adjustments needed to resolve the issue.]

```diff
- [Old Code]
+ [New Code]
```
```

---

## 3. Triage Categories
When classifying failures, use these standard categories:
- **Locator Issue**: Element not found, or matches multiple elements (Strict mode violation).
- **Wait Issue**: Timeout exceeded before element reached state (e.g., visible, enabled).
- **Assertion Mismatch**: `expect` failed because actual value != expected value.
- **Environmental**: Page crash, network error, or dependency failure.
