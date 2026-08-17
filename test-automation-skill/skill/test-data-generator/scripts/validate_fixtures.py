#!/usr/bin/env python3
"""Validate generated fixture output against the bundled JSON Schema template."""

import json
import sys
from pathlib import Path

try:
    import jsonschema
except Exception as exc:  # pragma: no cover - CLI feedback path
    raise SystemExit(f"jsonschema package is required: {exc}")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python validate_fixtures.py <fixture-output.json>")
        return 2

    fixture_path = Path(sys.argv[1])
    if not fixture_path.exists():
        print(f"File not found: {fixture_path}")
        return 2

    template_path = Path(__file__).resolve().parents[1] / "assets" / "fixture_templates.yaml"
    if not template_path.exists():
        print(f"Template not found: {template_path}")
        return 2

    try:
        fixture_data = json.loads(fixture_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}")
        return 1

    # Convert the YAML schema to a Python dict. Since this repo keeps YAML templates,
    # this validator checks the required top-level structure and representative keys
    # without requiring PyYAML to be installed. If PyYAML is available, it is used.
    try:
        import yaml
    except Exception:  # pragma: no cover
        yaml = None

    if yaml is not None:
        schema_text = template_path.read_text(encoding="utf-8")
        schema = yaml.safe_load(schema_text)
        schema_def = schema["templates"]["fixture_model"]
        validator = jsonschema.Draft7Validator(schema_def)
        errors = sorted(validator.iter_errors(fixture_data), key=lambda e: list(e.path))

        if errors:
            print("VALIDATION FAILED")
            for error in errors:
                path = "/".join(str(part) for part in error.absolute_path) or "root"
                print(f"- {path}: {error.message}")
            return 1

        print("VALIDATION PASSED")
        return 0

    required_top = {
        "positive_fixtures",
        "negative_fixtures",
        "boundary_fixtures",
        "api_payload_examples",
        "summary_metadata",
        "gaps_report",
    }
    missing = sorted(required_top - fixture_data.keys())
    if missing:
        print(f"VALIDATION FAILED: missing top-level sections: {missing}")
        return 1

    print("VALIDATION PASSED (structural check only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
