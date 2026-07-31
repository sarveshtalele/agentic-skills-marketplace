# sample-app — Pipeline Evaluation Report

> **Auto-generated** by the Reverse Engineer Skill Evaluator · 2026-07-24T05:40:42.889504+00:00Z

---

## Overall Score

```
█████████████████░░░  84/100 pts
```

**Confidence:** ✅ HIGH

The pipeline produced high-quality, verifiable outputs across all sections. Results can be used with high confidence for planning.

---

## Section Scores

| Section | Score | Status |
|---------|-------|--------|
| 1. Parsing Quality | 20/20 | ✅ PASS |
| 2. API Endpoint Detection | 13/20 | ⚠️ WARN |
| 3. Dead Code Analysis | 15/15 | ✅ PASS |
| 4. Entity / Data Architecture | 8/15 | ⚠️ WARN |
| 5. Dependency Graph | 13/15 | ⚠️ WARN |
| 6. AI Analysis Quality | 15/15 | ✅ PASS |
| **TOTAL** | **84/100** | **✅ HIGH** |

---

## Section Details

### 1. Parsing Quality — 20/20 pts

**Status:** ✅ PASS

> 11 files | 7 classes | 35 methods

| Check | Status | Points | Message |
|-------|--------|--------|---------|
| Files Parsed | ✅ PASS | +5/5 | 11 files parsed successfully |
| Parse Success Rate | ✅ PASS | +5/5 | 100% of attempted files parsed |
| Classes Extracted | ✅ PASS | +5/5 | 7 classes identified across parsed files |
| Methods Extracted | ✅ PASS | +5/5 | 35 methods/functions identified |

### 2. API Endpoint Detection — 13/20 pts

**Status:** ⚠️ WARN

> 9 endpoints extracted from 11 files

| Check | Status | Points | Message |
|-------|--------|--------|---------|
| Endpoints Detected | ⚠️ WARN | +4/8 | Only 9 endpoints detected — repo may have few routes, or use dynamic registration patterns |
| HTTP Method Variety | ⚠️ WARN | +3/6 | Only 2 HTTP method type(s) found: GET, POST |
| Path Format Validity | ✅ PASS | +6/6 | 9/9 paths have valid route format |

### 3. Dead Code Analysis — 15/15 pts

**Status:** ✅ PASS

> 1 dead files | 7 dead classes

| Check | Status | Points | Message |
|-------|--------|--------|---------|
| Dead File Ratio | ✅ PASS | +5/5 | 1 dead files = 9% of total (plausible range) |
| Analysis Completed | ✅ PASS | +5/5 | Dead code analysis ran and returned a structured result |
| Class-Level Analysis | ✅ PASS | +5/5 | 7 potentially unreferenced classes found |

**Recommendations:**
- Always manually verify dead code results before deletion — static analysis cannot detect runtime-loaded modules, reflection-based usage, or files loaded via config

### 4. Entity / Data Architecture — 8/15 pts

**Status:** ⚠️ WARN

> 0 entities | 0 relationships | 4 bounded contexts

| Check | Status | Points | Message |
|-------|--------|--------|---------|
| Entities Detected | ⚠️ WARN | +2/7 | 0 entities detected. If repo uses SQLAlchemy/Django (Python), check that domain/entity files are in the analyzed set and use standard ORM annotations or namespace conventions |
| Microservice Boundaries | ✅ PASS | +5/5 | 4 bounded contexts identified |
| Relationships Detected | ⚠️ WARN | +1/3 | Cannot assess — no entities detected |

**Recommendations:**
- No entities detected. Ensure domain/model/entity files are within the 300-file cap — increase the layer-3 quota in SLOTS dict in pipeline.py if needed. Expected ORM: SQLAlchemy/Django (Python)

### 5. Dependency Graph — 13/15 pts

**Status:** ⚠️ WARN

> 11 dep nodes | 19 edges | 1 tech items

| Check | Status | Points | Message |
|-------|--------|--------|---------|
| Dependency Map Built | ✅ PASS | +5/5 | 11 modules with 19 dependency edges |
| Graphviz Diagram | ✅ PASS | +5/5 | Graphviz diagram generated (18 edges shown) |
| Tech Stack Detection | ⚠️ WARN | +3/5 | Only 1 technology/technologies detected: Flask |

### 6. AI Analysis Quality — 15/15 pts

**Status:** ✅ PASS

> AI-powered (Claude claude-sonnet-4-6) | 4 roadmap phases | target: FastAPI, Python 3.12, SQLAlchemy 2.0

| Check | Status | Points | Message |
|-------|--------|--------|---------|
| Executive Summary | ✅ PASS | +5/5 | AI-generated executive summary present and substantive |
| Architecture Pattern | ✅ PASS | +5/5 | Pattern identified: 'MVC Monolith' |
| Modernization Phases | ✅ PASS | +5/5 | 4 phases: Assessment & Quick Wins, Incremental Modernization, Cloud & Container Readiness... |


---

## Recommendations

- Always manually verify dead code results before deletion — static analysis cannot detect runtime-loaded modules, reflection-based usage, or files loaded via config
- No entities detected. Ensure domain/model/entity files are within the 300-file cap — increase the layer-3 quota in SLOTS dict in pipeline.py if needed. Expected ORM: SQLAlchemy/Django (Python)

---

## Interpretation Guide

### What the Scores Mean

| Confidence | Score | Meaning |
|------------|-------|---------|
| HIGH       | ≥ 80  | All key pipeline sections produced verifiable output |
| MEDIUM     | ≥ 60  | Most sections reliable; some manual spot-checks advised |
| LOW        | ≥ 40  | Partial results — likely pattern coverage gaps |
| VERY LOW   | < 40  | Major gaps; treat as rough estimates only |

### Check Statuses

| Status | Meaning |
|--------|---------|
| ✅ PASS | Check passed — result is reliable |
| ⚠️ WARN | Partial or borderline result — review advised |
| ❌ FAIL | Check failed — result in this area may be missing or wrong |

### What Is Reliable vs Heuristic

| Output Area | Reliability | Notes |
|-------------|-------------|-------|
| File count & language distribution | HIGH | Exact filesystem walk |
| Class / method extraction | MEDIUM-HIGH | Regex-based; edge cases exist |
| Import / dependency detection | MEDIUM | Pattern-matched; dynamic imports missed |
| API endpoint extraction | MEDIUM | Attribute/decorator patterns; dynamic routes missed |
| Dead code detection | LOW-MEDIUM | Heuristic only — validate before deleting |
| Entity / DB schema | MEDIUM | ORM annotation & namespace heuristics |
| Microservice boundaries | LOW-MEDIUM | Keyword clustering — AI fallback |
| AI executive summary | HIGH (with API key) | Claude claude-sonnet-4-6; fallback text if no key |
| AI modernization roadmap | HIGH (with API key) | Claude claude-sonnet-4-6; fallback text if no key |

---

## How to Spot-Check Results

### Parsing Quality
- Open the SDD JSON → `module_inventory` array; pick 5 random files
- Verify the `classes` and `methods` lists match the actual source file content

### API Endpoints
- Compare `api_catalog.endpoints` in the SDD JSON against the actual
  controller files in the repository
- Check that HTTP methods (`GET`, `POST`, etc.) are correct

### Dead Code
- Pick 3 files from `dead_code_analysis.unreferenced_files`
- Search the repository for any import or reference to that file
- If found → false positive (this is expected; always validate before deleting)

### Entity Detection
- Open the SDD JSON → `data_architecture.entities`
- Cross-reference entity names against actual ORM model files in the repository

### Dependency Graph
- The Mermaid diagram in the Markdown report's "Module Dependency Graph"
  section shows module-to-module edges
- Verify a known dependency exists as an edge in the graph

---

_Generated by Reverse Engineer Skill · Claude Code_
