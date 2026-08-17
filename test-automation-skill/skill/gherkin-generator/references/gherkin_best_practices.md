# Gherkin Best Practices

This guide defines the expected behavior for high-quality Gherkin generated from structured test cases.

## Feature design

- Group related scenarios under a single `Feature` that reflects the business capability or workflow.
- Use a feature name in the form: `Feature: <Business capability>`.
- Keep features cohesive and limited to one domain area.
- Preserve traceability metadata as tags or inline comments rather than burying it in prose.

## Scenario structure

- Prefer one scenario per test case.
- Keep scenarios small and outcome-focused.
- Avoid mixing unrelated behaviors into a single scenario.
- Use scenario names that match the underlying business intent.

## Step semantics

- `Given` establishes context or preconditions.
- `When` describes the user or system action under test.
- `Then` asserts the expected result.
- Use `And`/`But` only to add supporting context or validation after the primary step type.

## Background usage

- Use `Background` when at least three scenarios share the same preconditions.
- Keep the background short and stable.
- Do not put scenario-specific logic into the background.

## Scenario Outline usage

Use `Scenario Outline` when the same behavior is repeated across a range of values:

```gherkin
Scenario Outline: Validate password length
  Given the user enters "<password>"
  When the form is submitted
  Then the validation result is "<result>"

  Examples:
    | password | result |
    | short    | invalid |
    | valid123 | valid |
```

## Tags and traceability

- Use tags such as `@positive`, `@negative`, `@boundary` for classification.
- Always include `@TC-XXX` if the scenario maps to a test case ID.
- Include `@REQ-XXX` when the scenario links back to a requirement.
- Keep tag names lowercase and remove spaces and punctuation.

## Data tables and doc strings

Use `Data Table` syntax when the test has structured input:

```gherkin
When the user submits the following payload:
  | field | value |
  | amount | 25.00 |
  | currency | USD |
```

Use `Doc Strings` for multi-line payloads or expected responses:

```gherkin
Then the API response should be:
  """
  {
    "status": "success",
    "message": "created"
  }
  """
```

## Anti-patterns to avoid

- Imperative, UI-specific wording that describes clicks instead of behavior.
- Repeating the same setup in every scenario when `Background` is appropriate.
- Inventing details that are not in the source test case.
- Mixing multiple business behaviors in one scenario.
- Outputting duplicate scenario titles in the same feature.

## Naming conventions

- Scenario titles should be short and descriptive.
- Prefer business language over implementation details.
- Use consistent verbs like `creates`, `updates`, `blocks`, `validates`, `returns`.

## Error handling and incomplete data

When a test case is incomplete, do not guess. Write a placeholder that preserves intent without inventing unsupported behavior:

```gherkin
# TODO: action missing for TC-123
Scenario: Handle incomplete action
  Given the user is on the form
  Then the outcome is as expected
```

## Syntax rules

- Indent steps consistently with two spaces.
- Separate scenarios with a blank line.
- Ensure each scenario has at least one `Then` step.
- Keep tags immediately above the scenario or feature declaration.

## Anti-hallucination

Generated Gherkin must remain grounded in evidence. If the source test case provides no action, expected result, or requirement ID, the generator should note the gap instead of manufacturing details.
