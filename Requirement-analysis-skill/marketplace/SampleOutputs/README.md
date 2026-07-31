# Sample Output

A real, unedited run of the skill's analysis engine — not a mockup.

```bash
python skill/requirement-analysis/scripts/requirement_analysis_skill.py \
    --repo-path marketplace/SampleOutputs/sample-app-source \
    --requirement "Add a discount_code field to the Order model and expose it on the orders API" \
    --output marketplace/SampleOutputs/sample-app-report
```

## Contents

| Folder | What it is |
|--------|------------|
| [`sample-app-source/`](sample-app-source/) | The input — a small Flask order-management app (11 files: controllers, services, repositories, models, templates) — the same sample app used by [`reverse-engineering-skill`](../../../reverse-engineering-skill/marketplace/SampleOutputs/) and [`change-impact-analysis-skill`](../../../change-impact-analysis-skill/marketplace/SampleOutputs/) |
| [`sample-app-report/`](sample-app-report/) | The output — everything the engine wrote for that input |

## What the engine found

| Field | Result |
|-------|--------|
| Parsed action | `add` |
| Target type(s) | `api_endpoint`, `database` |
| Entities | `API`, `discount_code` |
| Domain tag(s) | `financial_critical` |
| Top candidate file | `controllers/order_controller.py` (score 9) |
| Files indexed | 11 |
| Security & compliance items | 14 |

## Files in `sample-app-report/`

| File | Purpose |
|------|---------|
| [`implementation_plan.md`](sample-app-report/implementation_plan.md) | The primary artifact — open this first |
| [`requirement_analysis.json`](sample-app-report/requirement_analysis.json) | Machine-readable result |

This is exactly what you get when you point the skill at your own project — same file
names, same structure, just with your own requirement and codebase's numbers.

## The next step in the pipeline

This plan pointed at `models/order.py` and `controllers/order_controller.py` as the
files to change. Once those edits are made, run
[`change-impact-analysis-skill`](../../../change-impact-analysis-skill/) on the same
two files to see the deployment risk score — its
[`SampleOutputs/`](../../../change-impact-analysis-skill/marketplace/SampleOutputs/)
uses this exact scenario as its worked example.
