# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**Change Impact Analysis Skill** — a polyglot, deterministic agent skill that performs deployment-phase risk analysis on any codebase. Given a set of changed files, it:

1. **Builds a dependency graph** — parses AST in Python, JavaScript/TypeScript, Java, C#, Go
2. **Computes blast radius** — reverse-BFS to find all transitively affected modules
3. **Validates API contracts** — detects breaking changes in OpenAPI, GraphQL, Protobuf specs
4. **Parses ownership** — maps affected files to owners via CODEOWNERS / package.json
5. **Scores risk deterministically** — 0–100 score based on six factors (volume, spread, contracts, sensitivity, etc.)
6. **Generates reports** — markdown + JSON + deployment checklist

Works with **GitHub Copilot**, **Claude Code**, and **Cursor**.

---

## Architecture

**Two-layer design:**

1. **Static Analysis** (Python, pure function) — `scripts/engine/*`
   - Graph builder: AST parsing + dependency extraction
   - Impact analyzer: reverse-BFS traversal
   - Risk scorer: deterministic 0–100 calculation
   - Contract validator: OpenAPI / GraphQL / Protobuf checks
   - Ownership parser: CODEOWNERS extraction
   - Report generator: markdown + JSON output

2. **AI Narrative** (agent) — `SKILL.md`
   - Runs static analysis engine
   - Reads structured JSON output
   - Provides human context (why this matters, what to test, rollback triggers)
   - Writes AI analysis back into report

**Entry points:**
- **CLI:** `skill/change-impact-analysis/scripts/change_impact_skill.py` — runs standalone (no agent needed)
- **GitHub Copilot:** natural language triggers skill via `SKILL.md` frontmatter
- **Claude Code:** skill auto-discovered in `.claude/skills/change-impact-analysis/`
- **Cursor:** rule in `.cursor/rules/` triggers skill workflow

---

## Core Concepts

**Dependency Graph** — directed edges represent imports. Node = module. Edge A→B means "A imports B".
- Built via AST parsing (Python `ast`, JS via regex, Java via regex, etc.)
- Immutable once built; all analyses read from it

**Blast Radius** — set of modules affected by a change.
- Direct: changed files themselves
- Transitive: reverse-reachable from changed files (imports change → dependents affected)

**Risk Score** — 0–100 deterministic calculation driven by six factors:
- Change volume (files + lines)
- Transitive spread (module count)
- API contract violations
- Module type risk (database/core vs. utils)
- Code sensitivity (test vs. business logic)
- Consumer breadth (how many apps depend on this)

See `skill/change-impact-analysis/references/risk-scoring.md` for weights and examples.

---

## Key Commands

### Run from CLI (standalone)

```bash
# Auto-detect changed files from git diff
python skill/change-impact-analysis/scripts/change_impact_skill.py --from-git --base-branch main

# Explicit file list
python skill/change-impact-analysis/scripts/change_impact_skill.py --changed-files src/api/users.py src/models/user.py

# Custom output directory
python skill/change-impact-analysis/scripts/change_impact_skill.py --from-git --base-branch main --output /tmp/impact-report

# JSON-only (stdout, for CI/CD piping)
python skill/change-impact-analysis/scripts/change_impact_skill.py --from-git --json-only

# Fallback window for mtime scan (if no git available)
python skill/change-impact-analysis/scripts/change_impact_skill.py --repo-path . --from-git --since-minutes 120
```

### Run via Claude Code

1. In `.claude/skills/` place the skill folder
2. Type naturally: *"Analyse the change impact for my current changes"*
3. Or invoke explicitly: `/change-impact-analysis`

### Run via GitHub Copilot

Place skill in `.github/skills/change-impact-analysis/`, open Copilot Chat, type:
- *"What is the deployment risk for my PR?"*
- *"Analyse the change impact"*
- Copilot recognises trigger phrases in `SKILL.md` frontmatter

### Run via Cursor

Create `.cursor/rules/change-impact-analysis.mdc`, then use natural language or `@SKILL.md` in chat.

---

## Project Structure

```
change-impact-analysis-skill/
  skill/
    change-impact-analysis/          ← the installable skill (copy into .claude/skills/)
      SKILL.md                       ← Agent skill definition (8-step workflow)
      manifest.yaml
      scripts/
        change_impact_skill.py       ← CLI orchestrator (argparse, runs all engines)
        engine/
          graph_builder.py           ← AST-based dependency graph
          impact_analyzer.py         ← Reverse-BFS blast radius
          risk_scorer.py             ← Deterministic 0–100 scoring
          contract_validator.py      ← OpenAPI/GraphQL/Protobuf breach detection
          ownership_parser.py        ← CODEOWNERS parsing
          report_generator.py        ← Markdown + JSON output
      templates/
        impact_report.md             ← Report template (agent fills in AI sections)
        deployment_checklist.md      ← Pre/post deploy checklist
      references/
        dependency-analysis.md       ← Graph algorithm reference
        risk-scoring.md               ← Scoring formula, factors, examples
      assets/requirements.txt        ← Optional: PyYAML for YAML spec parsing
  marketplace/                       ← docs, guide, samples
    README.md                        ← Installation, usage examples
    QuickStart.md                    ← Fast first-run walkthrough
    UserGuide.pdf                    ← Full technical documentation
    Architecture.png
    SamplePrompts.md
    SampleOutputs/
```

---

## Requirements

| Tool | Version | Required | Notes |
|------|---------|----------|-------|
| Python | 3.8+ | ✓ | Core engine language |
| Git | any | ✓ | For `--from-git` change detection; optional if using `--changed-files` |
| PyYAML | 6.0+ | Optional | Enables YAML-format OpenAPI spec parsing; JSON specs always work |

Check Python: `python --version`

---

## Output

Every run produces (in `./change-impact-output/` by default):

```
impact_report.md           ← Markdown report with static analysis + AI narrative
impact_analysis.json       ← Machine-readable: changed files, impacted modules, risk score, API violations
deployment_checklist.md    ← Pre-deploy & post-deploy sign-off template
```

JSON schema (see `impact_analysis.json` in any run):
```json
{
  "change_detection_method": "git|mtime|explicit",
  "impact": {
    "changed_files": [...],
    "impacted_modules": [...],
    "regression_areas": [...],
    "required_test_suites": [...],
    "direct_impact_count": N,
    "transitive_impact_count": N
  },
  "contract_violations": [...],
  "risk": {
    "score": 0-100,
    "level": "LOW|MEDIUM|HIGH|CRITICAL",
    "action": "...",
    "factors": [...]
  }
}
```

---

## Development Workflow

**Adding support for a new language:**
1. Extend `graph_builder.py` with a parser for that language's import syntax
2. Add to polyglot switch: detect file type → invoke correct parser
3. Test on a small repository with that language

**Tuning risk score:**
1. Edit `risk_scorer.py` — weight factors or add new ones
2. Update `skill/change-impact-analysis/references/risk-scoring.md` with new weights
3. Run on example repos and verify against intuition

**Adding contract types:**
1. Extend `contract_validator.py` — detect new spec file format (e.g., gRPC, AsyncAPI)
2. Implement parsing + breach detection
3. Test on repos with that contract type

**Debugging change detection:**
1. If `--from-git` picks wrong files, check `change_detection_method` in JSON output
2. Falls back to `mtime` if git diff empty; use `--changed-files` to force exact list
3. Check `--since-minutes` window (default 1440 = 24h)

---

## No-Git Fallback

`--from-git` has 5 layers; picks first that succeeds:

1. `git diff --name-only <base>...HEAD` — PR-style diff
2. `git diff --name-only HEAD` — staged/uncommitted changes
3. `git diff --name-only HEAD~1 HEAD` — last commit
4. **Filesystem mtime scan** — files modified in last `--since-minutes` (default 24h)
5. Exits if all fail; use `--changed-files` explicitly

Output includes `change_detection_method` so agent can report which was used.

---

## Risk Score Reference

| Score | Level | Action |
|-------|-------|--------|
| 0–30 | LOW | Standard release |
| 31–60 | MEDIUM | Deploy + notify on-call |
| 61–80 | HIGH | Senior review + rollback plan |
| 81–100 | CRITICAL | Block; tech lead escalation |

Driven by six factors (see `risk_scoring.md` for weights):
- Change volume (files, lines)
- Transitive spread (module count)
- API contract violations
- Module type (database, core, utils, etc.)
- Code sensitivity (business logic vs. test)
- Consumer breadth (downstream apps)

---

## Common Edits

**Adding a new risk factor:** Edit `RiskScorer.__compute_factors()` in `risk_scorer.py`, add tuple `(name, value)` to `factors` list, update `skill/change-impact-analysis/references/risk-scoring.md`.

**Adjusting module type risk:** `risk_scorer.py`, line ~100, dict `MODULE_TYPE_RISK`.

**Changing default output location:** `change_impact_skill.py`, line ~170, default for `--output`.

**Detecting new ownership format:** `ownership_parser.py`, extend `parse()` method.

---

## CI/CD Integration

```bash
# Exit with error if risk > threshold
SCORE=$(python skill/change-impact-analysis/scripts/change_impact_skill.py --from-git --json-only \
  | python -c "import sys,json; print(json.load(sys.stdin)['risk']['score'])")
if [ "$SCORE" -gt "80" ]; then
  echo "CRITICAL risk ($SCORE/100) — blocked"
  exit 1
fi
```

Or in GitHub Actions (see marketplace/README.md Example 3).

---

## Testing Approach

No test suite in repo. Validation via:
1. **Real-world runs** — run against known codebases, verify output matches intuition
2. **Determinism check** — same repo + same git state → identical output, every time
3. **Agent validation** — ask GitHub Copilot / Claude Code to review impact narrative, flag misses

---

## References

- **Architecture diagram:** `marketplace/Architecture.png` (square PNG) / `skill/change-impact-analysis/assets/architecture-diagram.svg` (source diagram)
- **Dependency analysis algorithm:** `skill/change-impact-analysis/references/dependency-analysis.md`
- **Risk scoring breakdown:** `skill/change-impact-analysis/references/risk-scoring.md` (formulas, weights, examples)
- **Full technical docs:** `marketplace/UserGuide.pdf`
- **Setup guide:** `marketplace/QuickStart.md`
