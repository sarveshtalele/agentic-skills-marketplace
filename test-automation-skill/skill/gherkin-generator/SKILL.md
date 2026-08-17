---
name: gherkin-generator
description: "Generate executable Gherkin feature files from structured test cases. Use when the user needs BDD scenarios, Cucumber-ready features, or .feature output from a validated test design."
---

# Gherkin Generator

## Purpose

Convert structured test cases and supporting data into deterministic, executable Gherkin feature files that preserve traceability and remain valid for downstream BDD tooling.

## Inputs

This skill consumes the normalized output from the `test-design-generator` step. Supported input shapes include:

- `test_cases[]` — unified array of scenario objects
- `positive_tests[]`, `negative_tests[]`, `boundary_tests[]` — upstream arrays that must be normalized
- Optional `test_data[]` or fixture payloads for parameterized examples
- Optional `traceability_links[]` entries for requirement or validation mapping

## Output Contract

Generate output as one feature file per logical component or business flow. The output must follow these conventions:

- Feature file name: `<component>.feature`
- Feature header: `Feature: <Component Name>`
- Scenario naming: human-readable scenario title matching the test case title
- Tag format: `@positive`, `@negative`, `@boundary`, `@TC-XXX`, `@REQ-XXX`
- Traceability embedding: use tags for IDs and inline comments for local references when needed
- One scenario per test case unless the test cases are parameterized and should become a `Scenario Outline`

### Tag rules

- Always include the test type tag (`@positive`, `@negative`, `@boundary`)
- Add `@TC-XXX` when the source `id` is available
- Add `@REQ-XXX` for each linked requirement if present
- Avoid spaces or unsupported punctuation in tag names

## Pipeline Integration

### Expected input shape from `test-design-generator`

```json
{
  "test_cases": [
    {
      "id": "TC-001",
      "title": "Save payment card successfully",
      "type": "positive",
      "linked_requirements": ["REQ-001"],
      "preconditions": ["User is logged in."],
      "actions": ["Submit a valid payment card."],
      "expected_results": ["The card is stored securely."]
    }
  ]
}
```

### Normalization rules

When the upstream skill emits arrays instead of a single `test_cases` collection, normalize them into the unified shape before generating Gherkin:

| Upstream field | Normalized field |
|---|---|
| `positive_tests[]` | `test_cases[]` with `type: "positive"` |
| `negative_tests[]` | `test_cases[]` with `type: "negative"` |
| `boundary_tests[]` | `test_cases[]` with `type: "boundary"` |
| `traceability_links` on the artifact | inline `traceability_links` on each test case |
| `expected_result` | `expected_results[]` |
| `precondition` | `preconditions[]` |
| `action` | `actions[]` |

If a test case is missing required fields, do not invent them; convert the item into a partial scenario and flag the gap in the output notes or a gap report.

## Processing Rules

1. One scenario per test case by default.
2. Keep Gherkin steps grounded in the available test information only.
3. Use `Given` for preconditions, `When` for actions, and `Then` for expected outcomes.
4. If multiple preconditions exist, combine them with `And` rather than repeating `Given` lines for each.
5. If multiple actions exist, chain them as `When ...` followed by `And ...` steps.
6. Use `Background` when three or more scenarios share the same preconditions.
7. Use `Scenario Outline` for parameterized tests that differ only by data values.
8. Use `Examples` tables for repeated values.
9. Use `Data Tables` when multiple fields are supplied as a structured payload.
10. Use `Doc Strings` for multi-line expected responses or stored payloads.
11. Preserve requirement and validation traceability in tags/comments.

## Edge Cases

- Multiple actions → chain `When` + `And` steps.
- No preconditions → omit `Given` entirely.
- Missing expected results → generate `Then the outcome is as expected # TODO: expected result missing` and flag the scenario for review.
- Unknown test type → skip the scenario and note the reason in a gap report.
- Missing title → use a deterministic fallback like `Scenario: Untitled scenario <id>`.
- Large, repeated setup → move common setup to `Background`.

## Error Handling

- Missing actions → add a comment `# TODO: action missing for TC-XXX` and skip the scenario.
- Incomplete assertions → generate a placeholder `Then the expected outcome is met` and note the missing detail.
- Invalid Gherkin syntax → rewrite the wording to valid Gherkin rather than outputting broken syntax.
- Ambiguous steps → prefer precise language tied to the source text and avoid speculative user actions.

## Anti-Hallucination Rules

- Do not invent steps, endpoints, states, or user journeys that are not present in the source test case.
- Use only the available test title, preconditions, actions, and expected results.
- Never fabricate traceability IDs or link requirements that are not present in the input.
- If a field is missing or unsupported, flag it rather than guessing.

## Self-Check / Validation

Before returning output, Claude MUST validate the generated feature file against the checklist below:

1. Every scenario has at least one `Then` step.
2. No duplicate scenario names exist within a feature.
3. All tags are valid Gherkin identifiers and contain no spaces or punctuation.
4. Background is used when three or more scenarios share the same `Given` setup.
5. Scenario Outline is used for parameterized data instead of duplicating similar scenarios.
6. Each scenario preserves traceability IDs or links to source requirements.
7. The file remains syntactically valid Gherkin with blank lines between scenarios.

If any check fails, fix the output before returning it.

## Example

### Input

```json
{
  "test_cases": [
    {
      "id": "TC-001",
      "title": "Save payment card successfully",
      "type": "positive",
      "linked_requirements": ["REQ-001"],
      "preconditions": ["User is logged in.", "The user has a valid payment profile."],
      "actions": ["Submit a valid payment card.", "Confirm the card is valid."],
      "expected_results": ["The payment card is stored securely.", "The payment is authorized."]
    }
  ]
}
```

### Output

```gherkin
Feature: Payment card management
  In order to manage payment methods securely
  As a registered user
  I want to save a valid payment card.

  Background:
    Given the user is logged in
    And the user has a valid payment profile

  @positive @TC-001 @REQ-001
  Scenario: Save payment card successfully
    When the user submits a valid payment card
    And the user confirms the card is valid
    Then the payment card is stored securely
    And the payment is authorized
```

## Dependencies

- Upstream dependency: `test-design-generator`
- Optional tooling: Cucumber/Behave parser for syntax validation
- Downstream consumers: BDD test runners, documentation pipelines, traceability reporting

## Success Criteria

- Valid Gherkin syntax
- Full scenario coverage for every provided test case
- Traceability preserved via tags/comments
- Deterministic output format across runs
- No invented user actions or assertions
