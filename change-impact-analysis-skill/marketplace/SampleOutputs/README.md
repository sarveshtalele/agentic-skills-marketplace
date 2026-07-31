# Sample Output

A real, unedited run of the skill's analysis engine — not a mockup.

```bash
python skill/change-impact-analysis/scripts/change_impact_skill.py \
    --repo-path marketplace/SampleOutputs/sample-app-source \
    --changed-files models/order.py controllers/order_controller.py \
    --output marketplace/SampleOutputs/sample-app-report
```

## Contents

| Folder | What it is |
|--------|------------|
| [`sample-app-source/`](sample-app-source/) | The input — a small Flask order-management app (11 files: controllers, services, repositories, models, templates) — the same sample app used by [`reverse-engineering-skill`](../../../reverse-engineering-skill/marketplace/SampleOutputs/) and [`requirement-analysis-skill`](../../../Requirement-analysis-skill/marketplace/SampleOutputs/) |
| [`sample-app-report/`](sample-app-report/) | The output — everything the engine wrote for that input |

## What the engine found

| Metric | Result |
|--------|--------|
| Change detection | Explicit file list |
| Direct impact | 2 modules |
| Transitive impact | 3 modules |
| Impacted API endpoints | 1 |
| Contract violations | 0 |
| Consumer apps affected | 4 |
| **Deployment risk score** | **25/100 — LOW** |

## Files in `sample-app-report/`

| File | Purpose |
|------|---------|
| [`impact_report.md`](sample-app-report/impact_report.md) | The primary artifact — open this first |
| [`impact_analysis.json`](sample-app-report/impact_analysis.json) | Machine-readable result (CI/CD integration) |
| [`deployment_checklist.md`](sample-app-report/deployment_checklist.md) | Pre/post deploy sign-off checklist |

This is exactly what you get when you point the skill at your own project — same file
names, same structure, just with your own changed files and codebase's numbers.

## Where this scenario comes from

`models/order.py` and `controllers/order_controller.py` are the two files
[`requirement-analysis-skill`](../../../Requirement-analysis-skill/) recommended for
*"Add a discount_code field to the Order model and expose it on the orders API"* — see
its [`SampleOutputs/`](../../../Requirement-analysis-skill/marketplace/SampleOutputs/)
for that plan. This report shows the deployment risk **after** that change is made,
completing the plan → implement → impact-analyze pipeline.
