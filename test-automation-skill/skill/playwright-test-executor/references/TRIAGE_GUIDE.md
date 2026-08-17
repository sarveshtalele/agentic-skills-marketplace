# Playwright Triage & Failure Analysis Guide

This guide provides best practices for interpreting Playwright test failures and providing meaningful AI-assisted triage.

## 1. Understanding Playwright Failures

### Timeout Errors
- **Common Cause**: Element doesn't appear within the default timeout (e.g., 30s).
- **Diagnosis**: Check if the application was slow, the page changed, or if the locator is incorrect.
- **Fix**: Adjust locator or increase timeout (if necessary), but prioritize checking locator accuracy first.

### Strict Mode Violations
- **Common Cause**: `page.locator()` or `getBy...` found more than one element.
- **Diagnosis**: Review the HTML to see if multiple elements share the same attribute or text.
- **Fix**: Use more specific selectors (e.g., parent-child relationships) or `first()` / `nth()`.

### Assertion Failures
- **Common Cause**: UI state changed (e.g., text update, price change).
- **Diagnosis**: Compare the actual text/value captured in the report vs. the code.
- **Fix**: Update the expected value in the test or investigate if the app logic is broken.

---

## 2. Best Practices for Explanations

1. **Be Specific**: Don't just say "it failed." Say "The agent could not find the 'Check Out' button on the cart page because the locator used was for a 'Buy Now' button."
2. **Translate Technical Logs**: Convert `TimeoutError: waiting for locator('button#submit')` into "The submit button failed to appear on the registration form within 30 seconds."
3. **Check Artifacts**: Always look at screenshots and traces (if available) before finalizing an explanation.

---

## 3. Recommended Fixes

- **Locator Fixes**: Suggest using `data-test` IDs if they exist.
- **Wait Fixes**: Recommend `page.waitForLoadState('networkidle')` only as a last resort; prefer web-first assertions.
- **Data Fixes**: Identify if the test data used (e.g., expired user account) caused the failure.
