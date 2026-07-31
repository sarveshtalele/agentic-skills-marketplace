# Sample Output

A real, unedited run of the skill's analysis engine — not a mockup.

```bash
python skill/reverse-engineering-skill/scripts/reverse_engineer_skill.py \
    marketplace/SampleOutputs/sample-app-source --heuristic \
    --output marketplace/SampleOutputs
```

## Contents

| Folder | What it is |
|--------|------------|
| [`sample-app-source/`](sample-app-source/) | The input — a small Flask order-management app (11 files: controllers, services, repositories, models, templates) with real RBAC (`@role_required("admin")`) and ReBAC (`canEditOrder`) checks — the same sample app used by [`requirement-analysis-skill`](../../../Requirement-analysis-skill/marketplace/SampleOutputs/) and [`change-impact-analysis-skill`](../../../change-impact-analysis-skill/marketplace/SampleOutputs/) |
| [`sample-app-report/`](sample-app-report/) | The output — everything the pipeline wrote for that input |

## What the engine found

| Metric | Result |
|--------|--------|
| Files analyzed | 11 |
| Classes | 7 |
| Methods | 35 |
| API endpoints | 9 |
| Auth model | Hybrid RBAC + ReBAC |
| Screens detected | 5 |
| Business domain | E-Commerce / Online Retail |
| Quality score | 84/100 (HIGH confidence) |

## Files in `sample-app-report/`

| File | Purpose |
|------|---------|
| [`sample-app_report.md`](sample-app-report/sample-app_report.md) | The 4-section report — open this first |
| [`sample-app_sdd.json`](sample-app-report/sample-app_sdd.json) | Full System Design Document (machine-readable) |
| [`sample-app_evaluation.md`](sample-app-report/sample-app_evaluation.md) | 100-point quality score for this run |
| [`manifest.json`](sample-app-report/manifest.json) | Run metrics |

This is exactly what you get when you point the skill at your own project — same file
names, same structure, same four sections, just with your own codebase's numbers.
