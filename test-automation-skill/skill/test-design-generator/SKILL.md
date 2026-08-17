---
name: test-design-generator
description: >
  Transforms structured requirements, validation rules, and API contracts into comprehensive
  test designs covering positive, negative, boundary, validation, and contract test cases.
  Use when designing test suites or generating test cases from specs. Trigger on: test design,
  generate test cases, create test plan, positive and negative tests, boundary test design.
license: Apache-2.0
metadata:
  sdlc: Design
  tags:
    - SDLC:Design
    - SDLC:Testing
    - SDLC:Test-Design
---

# Test Design Generator

## Purpose

Generate structured test cases from requirements, acceptance criteria, validation rules, and API contracts.

## Inputs

- Requirement Model
- Validation Rules
- Optional API Contracts

## Outputs

- Positive Test Cases
- Negative Test Cases
- Boundary Test Cases
- Validation Test Cases
- Contract Test Cases

## Responsibilities

1. Generate happy-path tests.
2. Generate negative tests.
3. Generate boundary tests.
4. Generate validation tests.
5. Generate API contract tests.
6. Assign traceability links.
7. Generate deterministic test IDs.

## Processing Rules

- At least one positive test per acceptance criterion.
- At least one negative test per validation rule.
- Generate boundary tests for min/max constraints.
- Generate contract tests only when API contracts exist.

## Output Contract

- Test Cases
  - positive_tests
  - negative_tests
  - boundary_tests
  - validation_tests
  - contract_tests
  - traceability_links

## Anti-Hallucination Rules

- Never invent business rules.
- Never invent validations.
- Never invent API responses.

## Error Handling
- Report incomplete requirements without generating stub tests.
- Create gaps report for missing validations.

## Success Criteria

- 100% acceptance criteria coverage.
- Deterministic test generation.
- Complete traceability.

## Dependencies

The skill relies on the following Python packages (or their equivalents in other runtimes):

- `pydantic` for schema validation of input models.
- `jsonschema` for additional JSON contract validation.
- `uuid` (standard library) for deterministic ID generation using UUID v5 with a fixed namespace.
- `typing` for type hints and static analysis.

These should be listed in the repository's `requirements.txt` and installed in the execution environment.

## Configuration

| Setting | Description | Default |
|---|---|---|
| `deterministic_namespace` | Namespace UUID used for deterministic test ID generation. | `6ba7b810-9dad-11d1-80b4-00c04fd430c8` |
| `max_boundary_cases` | Maximum number of boundary variations per numeric constraint. | `3` |
| `traceability_prefix` | Prefix for traceability links to map tests back to source artifacts. | `REQ-` |

Configuration can be supplied via a `config.yaml` file placed alongside the skill or via environment variables prefixed with `TEST_DESIGN_`.

## Example Input / Output

### Input (excerpt)
```json
{
  "requirements": [
    {"id": "REQ-001", "description": "User can log in with valid credentials"}
  ],
  "validation_rules": [
    {"field": "email", "type": "format", "pattern": "^[^@]+@[^@]+\\.com$"}
  ],
  "api_contracts": null
}
```

### Output (excerpt)
```json
{
  "positive_tests": [{"id": "TEST-REQ-001-01", "scenario": "Valid login", "steps": [...]}],
  "negative_tests": [{"id": "TEST-REQ-001-NEG-01", "scenario": "Invalid password", "steps": [...]}],
  "boundary_tests": [],
  "validation_tests": [{"id": "TEST-VAL-EMAIL-01", "scenario": "Invalid email format", "steps": [...]}],
  "contract_tests": [],
  "traceability_links": [{"test_id": "TEST-REQ-001-01", "requirement_id": "REQ-001"}]
}
```

Providing concrete examples helps downstream consumers understand the expected contract.

## Traceability Format

Each generated test must include a `traceability_links` entry mapping the test ID to one or more source artifact IDs (requirements, acceptance criteria, validation rules, or API contract IDs). The format is:

```json
{"test_id": "<test-id>", "source_id": "<artifact-id>", "type": "requirement|validation|api"}
```

This enables automated coverage reporting and impact analysis.

## Error Object Schema

When the skill encounters unrecoverable issues (e.g., malformed input), it should return a structured error object instead of raising an exception:

```json
{
  "error": true,
  "code": "INVALID_INPUT",
  "message": "Detailed description of the problem",
  "details": {"field": "requirements", "issue": "missing id"}
}
```

Consumers can programmatically react to these errors.

## Performance Considerations

- The skill should process input models in a streaming fashion when possible to keep memory usage low.
- Generation of boundary tests can be expensive for large numeric ranges; limit to `max_boundary_cases` as configured.
- Cache deterministic UUID generation for repeated runs with identical inputs to improve speed.

## Best Practice Checklist (for maintainers)

- [ ] Validate input schemas against `pydantic` models.
- [ ] Ensure deterministic IDs are reproducible across runs.
- [ ] Include at least one positive test per acceptance criterion.
- [ ] Include negative tests for each validation rule.
- [ ] Generate boundary tests only for defined min/max constraints.
- [ ] Produce a traceability matrix linking every test to its source.
- [ ] Return structured error objects on failure.
- [ ] Document any new dependencies in `requirements.txt`.
